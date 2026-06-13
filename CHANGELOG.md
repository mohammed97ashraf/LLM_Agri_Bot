# Changelog

All notable changes to the **LLM Agri Bot** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Changelog file (this document) to track version history and updates.
- CONTRIBUTING.md with guidelines for new contributors.

### Changed
- (Future) Improved voice recognition accuracy by tuning HuggingFace model parameters.
- (Future) Enhanced error handling for API rate limits and timeouts.

### Fixed
- (Future) Corrected cross‑origin resource sharing (CORS) issues when frontend is served from a different port.

## [0.1.0] - 2025-03-23

### Added
- Initial release of **LLM Agri Bot**.
- **Text chat** functionality using OpenAI GPT‑3.5/4 API – allows users to ask any agriculture‑related question and receive intelligent answers.
- **Voice input** feature using HuggingFace Transformers (Wav2Vec2 for speech‑to‑text) – users can speak naturally, and the bot transcribes and responds.
- **Smart responses** powered by OpenAI’s language models, contextualized for agricultural queries (crop diseases, weather impact, fertilizer recommendations, etc.).
- **Flask backend** serving a REST API that integrates both text and voice endpoints.
- **Frontend** (HTML/CSS/JS) with a simple, user‑friendly interface for chat and voice recording.
- **Environment configuration** via `.env` file for securely storing API keys.
- **Sample image** (`Sample_image/voicechat_web.png`) showing the web interface.
- **README.md** with comprehensive setup instructions, architecture overview, and prerequisites.

### Technical Details
- Backend: Python Flask with endpoints `/chat` (text) and `/voice` (audio upload + transcription).
- Text model: OpenAI GPT‑3.5‑turbo / GPT‑4 (configurable via environment variable).
- Voice processing: HuggingFace pipeline for automatic speech recognition (Wav2Vec2 model).
- Frontend: Vanilla JavaScript with MediaRecorder API for capturing audio.
- Dependencies managed in `requirements.txt` (later should be added; see [Known Issues](#known-issues)).

### Known Issues
- `requirements.txt` file is missing – users must manually install dependencies listed in README.
- No automated tests yet; manual testing required for both chat and voice endpoints.
- Voice input only supports English; future versions will add multilingual support.
- Error messages for invalid API keys are not user‑friendly (generic 400 responses).

## [0.2.0] - Planned

### Added
- `requirements.txt` with pinned versions for reproducibility.
- Docker support for one‑command deployment.
- Persistent conversation history (database or session storage).
- Support for agriculture‑specific knowledge base (e.g., PDF embeddings via LangChain).
- Multilingual voice input (Hindi, Arabic, Spanish) using alternative HuggingFace models.

### Changed
- Upgrade Flask to version 2.x and use async endpoints for better concurrency.
- Sanitize user input to prevent injection attacks.
- Improve frontend styling for mobile responsiveness.

### Fixed
- CORS issues when frontend is hosted separately.
- Audio file cleanup after processing to avoid disk overflow.

---

## How to Use This Changelog

- The **Unreleased** section lists changes that are ready but not yet part of a formal release.
- Each version entry follows the format `[Major.Minor.Patch] - YYYY-MM-DD`.
- Types of changes: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
- For contributors: please add entries under the appropriate heading in the Unreleased section when opening pull requests.

---

## Migration Guide (if upgrading from previous versions)

This is the first release, so no migration needed. Future versions will provide upgrade steps here.