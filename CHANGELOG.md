# Changelog

All notable changes to **LLM Agri Bot (Krishi Sahayak)** are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## [2.0.0] - 2026-06-22

### Added
- **Image-based crop disease diagnosis** — upload a photo and get AI analysis using Llama 4 Scout vision model.
- **Groq TTS** — text-to-speech via Groq Orpheus model (replaced gTTS).
- **Groq STT** — speech-to-text via Groq Whisper (replaced HuggingFace).
- **Prompt caching** — automatic caching on Groq for faster responses and 50% cost savings.
- **In-memory fallback** — conversation memory works without Redis (Redis is optional).
- **Glassmorphism UI** — frosted glass panels, backdrop blur, gradient mesh background.
- **Dark/light theme toggle** with localStorage persistence.
- **Image preview** with upload button and thumbnail before sending.
- **Cache badge** showing hit rate on bot messages.
- **Post-processing sanitizer** — strips any markdown (`**bold**`, `*italic*`, etc.) from LLM output.
- **SEO package** — robots.txt, sitemap.xml, llms.txt, Open Graph, Twitter Cards, JSON-LD.
- **Deployment files** — Dockerfile, render.yaml, gunicorn.conf.py for Render/Docker.
- **`.env.example`** — template for easy setup.
- **uv support** — `pyproject.toml` with full dependency management.

### Changed
- Migrated from monolithic `app.py` to class-based `app/` package structure.
- Replaced `openai` SDK with `groq` SDK for all LLM interactions.
- Replaced LangChain wrapper with direct Groq SDK calls.
- System prompt rewritten with XML + Chain-of-Thought (CoT) format.
- Response length increased — more thorough, actionable answers.
- UI completely redesigned (Bootstrap 5 → custom glassmorphism).
- All project documentation updated for v2.0.

### Removed
- `asgi.py` — no longer using uvicorn (Flask dev server).
- `gTTS` dependency — replaced by Groq Orpheus TTS.
- `langchain` / `langchain-groq` dependencies — replaced by direct Groq SDK.
- `openai` dependency — replaced by Groq SDK.

### Fixed
- Model no longer generates markdown (`**bold**`) — stronger prompt + post-processing strip.
- Redis connection failure no longer breaks the app — graceful in-memory fallback.

## [0.2.0] - 2025-04-15

### Added
- `requirements.txt` with pinned versions.
- Persistent conversation history via Redis.
- Multilingual voice input (Hindi, Hinglish).

### Changed
- Upgraded Flask to 2.x with async support.
- Improved frontend for mobile responsiveness.

## [0.1.0] - 2025-03-23

### Added
- Initial release.
- Text chat with OpenAI GPT-3.5/4.
- Voice input via HuggingFace Wav2Vec2.
- Flask backend with `/chat` and `/voice` endpoints.
- Basic HTML/CSS/JS frontend.