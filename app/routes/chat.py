"""Chat route blueprint.

Handles text, voice, and image chat interactions with session management,
Redis-backed memory, and LLM processing.
"""

import base64
import logging
import os
from datetime import datetime
from typing import Dict, Optional, Tuple

from flask import (
    Blueprint, current_app, jsonify, request, session
)
from werkzeug.utils import secure_filename

from app.config import AppConfig

logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)


# --------------------------------------------------------------------------- #
#  Helper Functions                                                           #
# --------------------------------------------------------------------------- #

def _get_session_id() -> str:
    """Get or create a unique session ID for the current user.

    Uses Flask's built-in session object with a session ID.
    Falls back to a simple session.sid if available.

    Returns:
        A string session identifier.
    """
    if not session.get('user_id'):
        import uuid
        session['user_id'] = str(uuid.uuid4())
        session.permanent = True
    return session['user_id']


def _allowed_audio_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed audio extension."""
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower()
        in AppConfig.ALLOWED_AUDIO_EXTENSIONS
    )


def _allowed_image_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed image extension."""
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower()
        in AppConfig.ALLOWED_IMAGE_EXTENSIONS
    )


def _get_mime_type(filename: str) -> str:
    """Get MIME type from file extension."""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    mime_map = {
        'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
        'png': 'image/png', 'gif': 'image/gif', 'webp': 'image/webp',
    }
    return mime_map.get(ext, 'image/jpeg')


def _get_services():
    """Retrieve initialized services from the Flask app."""
    return (
        current_app.llm_service,
        current_app.memory_service,
        current_app.stt_service,
        current_app.tts_service,
    )


# --------------------------------------------------------------------------- #
#  Routes                                                                     #
# --------------------------------------------------------------------------- #

@chat_bp.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages (text and audio).

    Accepts:
        - Text via form field 'text'
        - Audio via file upload field 'audio'

    Returns:
        JSON response with 'text' (response) and optionally 'voice' (audio URL).
    """
    session_id = _get_session_id()
    llm_service, memory_service, stt_service, tts_service = _get_services()

    # --- Handle Audio Input ---
    if 'audio' in request.files:
        audio_file = request.files['audio']
        if audio_file.filename and _allowed_audio_file(audio_file.filename):
            try:
                # Save uploaded audio
                filename = secure_filename(audio_file.filename)
                upload_path = os.path.join(
                    current_app.config['UPLOAD_FOLDER'], filename
                )
                audio_file.save(upload_path)

                # Transcribe audio to text
                transcription = stt_service.transcribe(upload_path)

                # Clean up uploaded file
                try:
                    os.remove(upload_path)
                except OSError:
                    pass

                if not transcription:
                    return jsonify({
                        'error': 'Could not transcribe audio. Please try again.'
                    }), 400

                # Process the transcribed text
                response_data = _process_text_query(
                    session_id, transcription,
                    llm_service, memory_service, tts_service
                )
                response_data['transcription'] = transcription
                return jsonify(response_data)

            except Exception as exc:
                logger.error("Audio processing error [%s]: %s", session_id, exc)
                return jsonify({'error': 'Audio processing failed.'}), 500

        return jsonify({'error': 'Invalid audio file format.'}), 400

    # --- Handle Image Input ---
    if 'image' in request.files:
        image_file = request.files['image']
        text = request.form.get('text', 'What do you see in this image? Please analyze it from an agricultural perspective.')

        if image_file.filename and _allowed_image_file(image_file.filename):
            try:
                # Read and encode image
                image_data = image_file.read()
                if len(image_data) > AppConfig.MAX_IMAGE_SIZE:
                    return jsonify({'error': 'Image too large. Max 4MB allowed.'}), 400

                image_b64 = base64.b64encode(image_data).decode('utf-8')
                mime_type = _get_mime_type(image_file.filename)

                # Generate vision response
                history = memory_service.get_conversation_history(session_id)
                llm_result = llm_service.generate_with_image(
                    user_query=text,
                    image_base64=image_b64,
                    image_mime=mime_type,
                    session_id=session_id,
                )

                # Save to memory (text only, not the image)
                memory_service.add_to_conversation(session_id, 'user', f"[Image] {text}")
                memory_service.add_to_conversation(session_id, 'assistant', llm_result.text)

                # Generate audio
                voice_filename = tts_service.synthesize(llm_result.text)
                result: Dict = {
                    'text': llm_result.text,
                    'cache': {
                        'prompt_tokens': llm_result.prompt_tokens,
                        'cached_tokens': llm_result.cached_tokens,
                        'hit_rate': round(llm_result.cache_hit_rate, 1),
                        'completion_tokens': llm_result.completion_tokens,
                    },
                }
                if voice_filename:
                    result['voice'] = f'/static/audio/{voice_filename}'

                return jsonify(result)

            except Exception as exc:
                logger.error("Image processing error [%s]: %s", session_id, exc)
                return jsonify({'error': 'Image processing failed.'}), 500

        return jsonify({'error': 'Invalid image format. Use JPG, PNG, GIF, or WebP.'}), 400

    # --- Handle Text Input ---
    text = request.form.get('text')
    if not text and request.is_json:
        text = request.json.get('text') if request.json else None
    if not text:
        return jsonify({'error': 'No text provided.'}), 400

    response_data = _process_text_query(
        session_id, text, llm_service, memory_service, tts_service
    )
    return jsonify(response_data)


@chat_bp.route('/chat/clear', methods=['POST'])
def clear_conversation():
    """Clear the conversation history for the current session.

    Returns:
        JSON confirmation message.
    """
    session_id = _get_session_id()
    memory_service = current_app.memory_service
    memory_service.clear_conversation(session_id)
    logger.info("Conversation cleared for session %s", session_id)
    return jsonify({'status': 'ok', 'message': 'Conversation cleared.'})


@chat_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring.

    Returns:
        JSON with service health status.
    """
    memory_service = current_app.memory_service
    memory_healthy = memory_service.health_check()

    return jsonify({
        'status': 'healthy' if memory_healthy else 'degraded',
        'redis': 'connected' if memory_healthy else 'disconnected',
        'timestamp': datetime.utcnow().isoformat(),
    })


# --------------------------------------------------------------------------- #
#  Internal Processing                                                        #
# --------------------------------------------------------------------------- #

def _process_text_query(
    session_id: str,
    user_text: str,
    llm_service,
    memory_service,
    tts_service,
) -> Dict:
    """Process a text query through the LLM pipeline.

    Steps:
        1. Retrieve conversation history from Redis.
        2. Generate response using LangChain + LLM.
        3. Save user and assistant messages to Redis.
        4. Generate audio response via TTS.

    Args:
        session_id: Current user session.
        user_text: The user's input text.
        llm_service: LLM service instance.
        memory_service: Memory service instance.
        tts_service: TTS service instance.

    Returns:
        Dict with 'text' (response) and optionally 'voice' (audio file URL).
    """
    # 1. Get conversation history
    history = memory_service.get_conversation_history(session_id)

    # 2. Generate LLM response (with prompt caching)
    llm_result = llm_service.generate(
        user_query=user_text,
        conversation_history=history,
        session_id=session_id,
    )

    # 3. Save to memory
    memory_service.add_to_conversation(session_id, 'user', user_text)
    memory_service.add_to_conversation(session_id, 'assistant', llm_result.text)

    # 4. Generate audio
    voice_filename = tts_service.synthesize(llm_result.text)
    result: Dict = {'text': llm_result.text}

    # Add cache metrics for monitoring
    result['cache'] = {
        'prompt_tokens': llm_result.prompt_tokens,
        'cached_tokens': llm_result.cached_tokens,
        'hit_rate': round(llm_result.cache_hit_rate, 1),
        'completion_tokens': llm_result.completion_tokens,
    }

    if voice_filename:
        result['voice'] = f'/static/audio/{voice_filename}'

    return result