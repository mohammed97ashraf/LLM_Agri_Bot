# Architecture — Krishi Sahayak v2.0

## Overview

Krishi Sahayak is a full-stack AI agriculture assistant. Flask backend + Groq SDK for all AI services, Redis for session memory, glassmorphism frontend. Class-based services following SOLID principles.

## Architecture Diagram

```
Browser (jQuery + Glassmorphism CSS)
    │
    ├── GET /             → index.html
    ├── POST /chat        → text query
    ├── POST /chat        → image + text (multipart)
    ├── POST /chat        → audio blob (multipart)
    ├── POST /chat/clear  → clear session
    └── GET /health       → health check
    │
Flask (WSGI)
    │
    ├── main_bp          → index, robots.txt, sitemap.xml, llms.txt
    ├── chat_bp          → /chat, /chat/clear, /health
    │
    └── Services (attached to app)
         ├── LLMService       → Groq SDK (openai/gpt-oss-120b)
         ├── MemoryService    → Redis + in-memory fallback
         ├── STTService       → Groq Whisper (whisper-large-v3-turbo)
         ├── TTSService       → Groq Orpheus (canopylabs/orpheus-v1-english)
         └── PromptManager    → XML + CoT system prompt
```

## Components

### 1. Frontend (`app/templates/` + `app/static/`)

| File | Purpose |
|------|---------|
| `templates/index.html` | Main template with SEO, JSON-LD, OG tags |
| `static/css/style.css` | Glassmorphism UI, dark/light theme |
| `static/js/chat.js` | Chat logic, image upload, voice recording |

Features: Text input, image upload with preview, voice recording, theme toggle, cache badge display.

### 2. Backend (`app/`)

**App Factory** (`app/__init__.py`):
- `create_app()` → Flask factory with config, blueprints, services

**Routes** (`app/routes/`):

| Blueprint | Endpoints | Purpose |
|-----------|-----------|---------|
| `main_bp` | `GET /`, `/robots.txt`, `/sitemap.xml`, `/llms.txt` | Pages + SEO |
| `chat_bp` | `POST /chat`, `POST /chat/clear`, `GET /health` | Chat API |

**Services** (`app/services/`):

| Service | Responsibility |
|---------|---------------|
| `LLMService` | Groq SDK calls, vision model, cache tracking, markdown stripping |
| `MemoryService` | Redis conversation history with in-memory fallback |
| `STTService` | Groq Whisper audio transcription |
| `TTSService` | Groq Orpheus text-to-speech |
| `PromptManager` | XML + CoT system prompt, message building |

### 3. AI Models (all Groq)

| Model | Use | Endpoint |
|-------|-----|----------|
| `openai/gpt-oss-120b` | Text chat | Chat Completions |
| `meta-llama/llama-4-scout-17b-16e-instruct` | Image analysis | Chat Completions (multimodal) |
| `whisper-large-v3-turbo` | Speech-to-text | Audio Transcriptions |
| `canopylabs/orpheus-v1-english` | Text-to-speech | Audio Speech |

### 4. Memory (Redis)

- Session-scoped conversation history stored as JSON lists in Redis.
- Automatic TTL expiry (configurable, default 1 hour).
- **In-memory fallback** when Redis is unavailable — conversations persist within the same process but are lost on restart.

## Data Flows

### Text Chat
```
User types message → POST /chat (text)
  → MemoryService.get_conversation_history()
  → LLMService.generate(user_query, history)
    → build_messages(system_prompt + history + query)
    → Groq API call (text model)
    → strip_markdown(response)
  → MemoryService.add_to_conversation(user + assistant)
  → TTSService.synthesize(response)
  → Return JSON { text, voice, cache }
```

### Image Analysis
```
User uploads image → POST /chat (image + text)
  → Read + base64-encode image
  → LLMService.generate_with_image(query, image_b64)
    → build_messages with image_url (multimodal)
    → Groq API call (vision model)
    → strip_markdown(response)
  → MemoryService.add_to_conversation
  → TTSService.synthesize
  → Return JSON { text, voice, cache }
```

### Voice Chat
```
User records audio → POST /chat (audio)
  → Save audio file
  → STTService.transcribe(file)
    → Groq Whisper API
  → _process_text_query(transcription)
  → Delete temp audio file
  → Return JSON { text, voice, transcription }
```

## Prompt Caching

Groq automatically caches static prompt prefixes across requests:
- System prompt (~500 tokens) → cached from request 1
- Conversation history → prefix grows but cached on subsequent requests
- Only the new user query is processed fresh
- 50% cost discount on cached tokens
- Cache stats returned in every response

## Deployment

| Method | Config |
|--------|--------|
| Local dev | `uv run python LLM_Agri_Bot/run.py` |
| Render | `render.yaml` + `Dockerfile` |
| Docker | `docker build . && docker run -p 10000:10000` |
| Production | Gunicorn via `gunicorn.conf.py` |