"""LLM Agri Bot - Agricultural AI Assistant

A Flask-based async web application providing agricultural advisory
using LangChain, Redis-backed conversation memory, and speech capabilities.
"""

import os
import logging
from typing import Any

from flask import Flask
from dotenv import load_dotenv

# Load environment variables BEFORE importing config
load_dotenv()

from app.config import AppConfig


def create_app(config_object: Any = None) -> Flask:
    """Application factory for LLM Agri Bot.

    Implements the Factory Method pattern for flexible app creation
    with different configurations (development, testing, production).

    Args:
        config_object: Optional configuration object or module.

    Returns:
        Configured Flask application instance.
    """
    app = Flask(
        __name__,
        static_folder='static',
        static_url_path='/static',
        template_folder='templates'
    )

    # Load configuration
    if config_object is None:
        app.config.from_object(AppConfig)
    else:
        app.config.from_object(config_object)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, app.config.get('LOG_LEVEL', 'INFO')),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Register routes (blueprints)
    register_blueprints(app)

    # Initialize services
    initialize_services(app)

    return app


def register_blueprints(app: Flask) -> None:
    """Register all route blueprints."""
    from app.routes.chat import chat_bp
    from app.routes.main import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp)


def initialize_services(app: Flask) -> None:
    """Initialize application services and attach to app instance.

    All core services are created eagerly at startup to detect
    configuration issues early.
    """
    from app.services.llm_service import LLMService
    from app.services.memory_service import MemoryService
    from app.services.stt_service import STTService
    from app.services.tts_service import TTSService
    from app.services.prompt_manager import PromptManager

    app.llm_service = LLMService()
    app.memory_service = MemoryService()
    app.stt_service = STTService()
    app.tts_service = TTSService()
    app.prompt_manager = PromptManager()

    app.logger.info("All services initialized successfully.")
