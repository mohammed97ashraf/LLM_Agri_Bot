"""Speech-to-Text Service using Groq Whisper API.

Provides audio transcription via Groq's Whisper model.
"""

import logging
from pathlib import Path
from typing import Optional

import requests

from app.config import AppConfig

logger = logging.getLogger(__name__)


class STTService:
    """Speech-to-Text transcription service using Groq Whisper.

    Transcribes audio files to text using Groq's Whisper API.
    """

    def __init__(self) -> None:
        """Initialize the STT service with Groq configuration."""
        self.config = AppConfig

        # Groq Whisper API endpoint
        self._endpoint = "https://api.groq.com/openai/v1/audio/transcriptions"
        self._headers = {
            "Authorization": f"Bearer {self.config.GROQ_API_KEY}"
        }

        logger.info("STT Service initialized with Groq Whisper: %s",
                    self.config.STT_MODEL)

    def transcribe(self, audio_file_path: str) -> str:
        """Transcribe an audio file to text using Groq Whisper.

        Args:
            audio_file_path: Path to the audio file.

        Returns:
            Transcribed text string, empty on failure.
        """
        if not self.config.GROQ_API_KEY:
            logger.error("GROQ_API_KEY not set, cannot transcribe")
            return ""

        try:
            audio_path = Path(audio_file_path)
            if not audio_path.exists():
                logger.error("Audio file not found: %s", audio_file_path)
                return ""

            with open(audio_path, "rb") as audio_file:
                files = {"file": (audio_path.name, audio_file, "audio/webm")}
                data = {
                    "model": self.config.STT_MODEL,
                    "response_format": "json",
                }

                response = requests.post(
                    self._endpoint,
                    headers=self._headers,
                    files=files,
                    data=data,
                    timeout=60,
                )

            if response.status_code == 200:
                result = response.json()
                text = result.get("text", "")
                logger.debug("Transcription successful: %.50s...", text)
                return text
            else:
                logger.error("Groq STT error %s: %s",
                             response.status_code, response.text[:200])
                return ""

        except requests.exceptions.Timeout:
            logger.error("Groq STT request timed out for %s", audio_file_path)
            return ""
        except Exception as exc:
            logger.error("STT transcription failed: %s", exc)
            return ""