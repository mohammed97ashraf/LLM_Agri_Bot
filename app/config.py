"""Application Configuration Module.

Centralizes all configuration from environment variables following
the principle of single responsibility and enabling easy testing.
"""

import os
from typing import Optional


class AppConfig:
    """Application configuration loaded from environment variables.

    Follows the Singleton pattern conceptually - one configuration
    object is created at app startup and reused throughout.
    """

    # Flask
    SECRET_KEY: str = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG: bool = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'

    # File uploads
    UPLOAD_FOLDER: str = os.getenv('UPLOAD_FOLDER', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads'))
    AUDIO_FOLDER: str = os.getenv('AUDIO_FOLDER', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'static', 'audio'))
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16 MB
    ALLOWED_AUDIO_EXTENSIONS: set = {'webm', 'wav', 'mp3', 'ogg', 'm4a'}

    # LLM (Groq)
    GROQ_API_KEY: Optional[str] = os.getenv('GROQ_API_KEY')
    LLM_MODEL: str = os.getenv('LLM_MODEL', 'openai/gpt-oss-120b')
    LLM_VISION_MODEL: str = os.getenv('LLM_VISION_MODEL', 'meta-llama/llama-4-scout-17b-16e-instruct')
    LLM_TEMPERATURE: float = float(os.getenv('LLM_TEMPERATURE', '0.3'))
    LLM_MAX_TOKENS: int = int(os.getenv('LLM_MAX_TOKENS', '1024'))

    # Speech-to-Text (HuggingFace / Groq Whisper)
    STT_MODEL: str = os.getenv('STT_MODEL', 'whisper-large-v3-turbo')
    STT_PROVIDER: str = os.getenv('STT_PROVIDER', 'groq')  # groq or huggingface
    HUGGINGFACE_TOKEN: Optional[str] = os.getenv('HUGGINGFACE_TOKEN', None)

    # Text-to-Speech (Groq Orpheus)
    TTS_PROVIDER: str = os.getenv('TTS_PROVIDER', 'groq')  # groq or gtts
    TTS_MODEL: str = os.getenv('TTS_MODEL', 'canopylabs/orpheus-v1-english')
    TTS_VOICE: str = os.getenv('VOICE', 'autumn')

    # File upload extensions
    ALLOWED_AUDIO_EXTENSIONS: set = {'webm', 'wav', 'mp3', 'ogg', 'm4a'}
    ALLOWED_IMAGE_EXTENSIONS: set = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    MAX_IMAGE_SIZE: int = 4 * 1024 * 1024  # 4 MB for base64

    # Redis (Session Memory)
    REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_USERNAME: Optional[str] = os.getenv('USERNAME', None)
    REDIS_PASSWORD: Optional[str] = os.getenv('PASSWORD', None)
    REDIS_SSL: bool = os.getenv('REDIS_SSL', 'true').lower() == 'true'
    REDIS_SESSION_TTL: int = int(os.getenv('REDIS_SESSION_TTL', '3600'))  # 1 hour

    # Session
    SESSION_TYPE: str = 'redis'
    SESSION_PERMANENT: bool = False
    SESSION_USE_SIGNER: bool = True
    SESSION_KEY_PREFIX: str = 'agri_bot:session:'

    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
