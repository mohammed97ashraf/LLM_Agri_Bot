# Contributing to Krishi Sahayak

Thank you for considering contributing to this project! We welcome improvements in documentation, bug fixes, feature enhancements, and new ideas.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager
- A [Groq API key](https://console.groq.com/keys)

## Development Setup

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/LLM_Agri_Bot.git
cd LLM_Agri_Bot

# 2. Install dependencies
uv sync

# 3. Configure environment
cp .env.example LLM_Agri_Bot/.env
# Edit .env and add your GROQ_API_KEY

# 4. Run the app
uv run python LLM_Agri_Bot/run.py
```

## How to Contribute

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes.
4. Test your changes thoroughly.
5. Commit and push to your fork.
6. Open a Pull Request against the `main` branch.

## Project Structure

```
LLM_Agri_Bot/
├── app/
│   ├── routes/         # Flask blueprints (main, chat)
│   ├── services/       # LLM, Memory, STT, TTS, PromptManager
│   ├── static/         # CSS (glassmorphism), JS, images
│   └── templates/      # HTML (index.html)
├── llms.txt            # AI crawler disclosure
├── .env.example        # Environment template
├── run.py              # Dev entry point
└── gunicorn.conf.py    # Production config
```

## Code Style

- Follow PEP 8 for Python code.
- Use type hints on all function signatures.
- Write docstrings for all public functions and classes.
- Keep comments concise but helpful.
- Class-based approach for services (SOLID principles).

## Reporting Issues

- Use the GitHub issue tracker.
- Provide a clear description, steps to reproduce, and expected behavior.
- Include relevant logs, screenshots, or code snippets.

## Security

- Never commit API keys, passwords, or other secrets.
- Always use environment variables for sensitive data.
- The `.env` file is git-ignored — never force-add it.

## Pull Request Process

1. Ensure your PR description summarizes changes clearly.
2. Reference any related issues.
3. Maintainers will review and may request changes.
4. Once approved, your PR will be merged.

Thank you for helping make this project better!