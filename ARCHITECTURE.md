# Architecture of LLM Agri Bot

## Overview

LLM Agri Bot is a full‑stack chatbot tailored for agriculture queries. It combines a Flask backend with OpenAI’s GPT models for text understanding and HuggingFace Transformers for voice processing. The frontend is a simple HTML/CSS/JS interface that supports both text and voice input.

## High‑Level Architecture

```
+-------------------+      HTTP/WebSocket      +----------------------+
|   Frontend        |  ------------------->   |   Flask Backend      |
| (HTML/CSS/JS)     |  <-------------------   |   (Python)           |
| - text input      |                          | - /chat endpoint     |
| - voice recording  |                          | - /voice endpoint    |
+-------------------+                          +----------------------+
                                                       |
                                                       v
                                              +----------------------+
                                              | OpenAI API           |
                                              | (GPT-3.5/4)          |
                                              +----------------------+
                                                       ^
                                                       |
                                              +----------------------+
                                              | HuggingFace          |
                                              | (Wav2Vec2 STT)       |
                                              +----------------------+
```

## Component Breakdown

### 1. Frontend (HTML/CSS/JS)
- **Location**: `templates/` and `static/` directories.
- **Functionality**:
  - Renders a chat interface with a text input box and a microphone button.
  - Sends text messages to the backend via HTTP POST to `/chat`.
  - Captures audio from the user’s microphone using the browser’s `MediaRecorder` API, then sends the audio blob to `/voice`.
- **Key files**:
  - `templates/index.html` – main page layout.
  - `static/script.js` – handles AJAX calls and voice recording logic.
  - `static/style.css` – styling for the chat UI.

### 2. Backend (Flask)
- **Location**: `app.py` (or main application file).
- **Endpoints**:
  - `GET /` – serves the frontend page.
  - `POST /chat` – accepts JSON with `{"message": "..."}`, calls OpenAI API, and returns the assistant’s reply.
  - `POST /voice` – accepts an audio file, transcribes it using HuggingFace’s Wav2Vec2, then forwards the transcribed text to the OpenAI API for a response.
- **Configuration**:
  - OpenAI API key and HuggingFace token are loaded from environment variables (`OPENAI_API_KEY`, `HUGGINGFACE_TOKEN`).
- **Dependencies**:
  - Flask
  - openai
  - transformers (HuggingFace)
  - torch (for model inference)
  - soundfile / librosa (for audio processing)

### 3. Text Model (OpenAI GPT-3.5/4)
- **Usage**:
  - The backend constructs a prompt with the user’s message and optional context (e.g., “You are an agriculture expert.”).
  - Sends the prompt to OpenAI’s Chat Completion API.
  - Returns the generated response.
- **Configuration**:
  - Model selection (gpt-3.5-turbo or gpt-4) can be set via environment variable `GPT_MODEL`.
  - Temperature, max tokens, etc., are configurable in `app.py`.

### 4. Voice Processing (HuggingFace Wav2Vec2)
- **Model**: `facebook/wav2vec2-base-960h` (or a fine‑tuned variant for agricultural domain).
- **Pipeline**:
  - Receive audio blob (WAV format) from frontend.
  - Convert to mono, 16kHz sample rate.
  - Run through the Wav2Vec2 model to obtain transcription.
  - Return the text to the user or feed it into the OpenAI pipeline.
- **Caching**: The model is loaded once at startup and reused for all requests to reduce latency.

## Data Flow

1. **Text Chat Flow**:
   - User types a question → frontend sends `POST /chat` with JSON body.
   - Backend receives message → sends to OpenAI API → receives response → returns JSON `{"reply": "..."}`.
   - Frontend displays the reply in the chat window.

2. **Voice Chat Flow**:
   - User clicks microphone → frontend records audio → sends blob as `POST /voice` (multipart/form-data).
   - Backend receives audio → runs HuggingFace ASR → gets transcription.
   - Backend sends transcription to OpenAI API → gets reply.
   - Backend returns JSON `{"transcript": "...", "reply": "..."}`.
   - Frontend displays both the transcribed text and the assistant’s reply.

## Security & Configuration

- All API keys are stored as environment variables. Never hardcode secrets.
- Input validation: Backend sanitizes user messages to prevent injection attacks.
- Rate limiting: Consider adding Flask‑Limiter to prevent abuse.
- Logging: All requests and errors are logged to `app.log` for debugging.

## Deployment Considerations

- **Local**: Run with `python app.py` after setting environment variables.
- **Production**: Use a WSGI server (Gunicorn) behind Nginx. Consider containerization with Docker.
- **Scaling**: If voice processing becomes a bottleneck, offload it to a separate microservice or use a cloud ASR service.

## Future Improvements

- Add a memory layer (e.g., Redis) to maintain conversation context across sessions.
- Integrate a vector database (Pinecone, FAISS) for retrieval‑augmented generation (RAG) using agricultural documents.
- Support multiple languages via HuggingFace multilingual models.
- Implement a feedback loop to improve responses over time.

## References

- [OpenAI API documentation](https://platform.openai.com/docs)
- [HuggingFace Wav2Vec2](https://huggingface.co/facebook/wav2vec2-base-960h)
- [Flask documentation](https://flask.palletsprojects.com/)

---

*This document was generated to help new contributors understand the system architecture. For setup instructions, see [README.md](README.md).*