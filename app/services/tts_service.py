"""Text-to-Speech Service using Groq TTS API.

Generates speech audio from text using Groq's Orpheus TTS model.
"""

import logging
import string
import random
import time
from pathlib import Path
from typing import Optional

import requests

from app.config import AppConfig

logger = logging.getLogger(__name__)


class TTSService:
    """Text-to-Speech service using Groq's audio/speech API.

    Uses the Orpheus TTS model via Groq for speech synthesis.
    """

    def __init__(self) -> None:
        """Initialize the TTS service."""
        self.config = AppConfig
        self.audio_folder: str = self.config.AUDIO_FOLDER
        self._endpoint = "https://api.groq.com/openai/v1/audio/speech"
        self._headers = {
            "Authorization": f"Bearer {self.config.GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

        Path(self.audio_folder).mkdir(parents=True, exist_ok=True)
        logger.info("TTS initialized: %s (voice: %s)",
                     self.config.TTS_MODEL, self.config.TTS_VOICE)

    def synthesize(self, text: str) -> Optional[str]:
        """Convert text to speech via Groq TTS.

        Args:
            text: The text to convert.

        Returns:
            Filename of the generated wav file, or None.
        """
        if not text or not text.strip():
            logger.warning("Empty text for TTS")
            return None

        if not self.config.GROQ_API_KEY:
            logger.error("GROQ_API_KEY not set")
            return None

        try:
            payload = {
                "model": self.config.TTS_MODEL,
                "input": text,
                "voice": self.config.TTS_VOICE,
                "response_format": "wav",
            }

            response = requests.post(
                self._endpoint,
                headers=self._headers,
                json=payload,
                timeout=30,
            )

            if response.status_code == 200:
                filename = self._generate_filename()
                filepath = Path(self.audio_folder) / filename
                with open(filepath, "wb") as f:
                    f.write(response.content)
                logger.debug("TTS saved: %s", filename)
                return filename
            else:
                logger.error("Groq TTS error %s: %s",
                             response.status_code, response.text[:200])
                return None

        except requests.exceptions.Timeout:
            logger.error("Groq TTS timed out")
            return None
        except Exception as exc:
            logger.error("TTS failed: %s", exc)
            return None

    @staticmethod
    def _generate_filename() -> str:
        """Generate a random .wav filename."""
        rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f"{rand}.wav"

    def cleanup_old_files(self, max_age_hours: int = 24) -> int:
        """Remove audio files older than max_age_hours."""
        cutoff = time.time() - (max_age_hours * 3600)
        cleaned = 0
        try:
            for ext in ("*.wav", "*.mp3"):
                for f in Path(self.audio_folder).glob(ext):
                    if f.stat().st_mtime < cutoff:
                        f.unlink()
                        cleaned += 1
            if cleaned:
                logger.info("Cleaned %d old audio files", cleaned)
        except Exception as exc:
            logger.error("Audio cleanup failed: %s", exc)
        return cleaned