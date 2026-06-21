"""Redis-backed Conversation Memory Service.

Provides persistent, session-scoped conversation memory using Redis.
Falls back to in-memory dict storage when Redis is unavailable.
"""

import json
import logging
import threading
import time
from typing import Dict, List, Optional

import redis
from redis import Redis as RedisClient

from app.config import AppConfig

logger = logging.getLogger(__name__)


class MemoryService:
    """Manages conversation memory with Redis primary and in-memory fallback.

    Uses Redis for persistence. If Redis is unreachable, conversations
    are stored in-memory so the bot still remembers within the same process.
    """

    def __init__(self) -> None:
        """Initialize the Redis connection with in-memory fallback."""
        self.config = AppConfig
        self._client: Optional[RedisClient] = None
        self._fallback: Dict[str, List[Dict[str, str]]] = {}
        self._lock = threading.Lock()
        self._redis_available = False
        self._connect()

    def _connect(self) -> None:
        """Establish connection to Redis server."""
        try:
            connection_params = {
                'host': self.config.REDIS_HOST,
                'port': self.config.REDIS_PORT,
                'decode_responses': True,
            }

            if self.config.REDIS_USERNAME:
                connection_params['username'] = self.config.REDIS_USERNAME
            if self.config.REDIS_PASSWORD:
                connection_params['password'] = self.config.REDIS_PASSWORD
            if self.config.REDIS_SSL:
                connection_params['ssl'] = True

            self._client = redis.Redis(**connection_params)
            self._client.ping()
            self._redis_available = True
            logger.info("Connected to Redis at %s:%s",
                        self.config.REDIS_HOST, self.config.REDIS_PORT)
        except Exception as exc:
            logger.warning("Redis unavailable, using in-memory fallback: %s", exc)
            self._client = None
            self._redis_available = False

    @property
    def client(self) -> Optional[RedisClient]:
        """Get the Redis client."""
        return self._client

    def _get_session_key(self, session_id: str) -> str:
        """Generate the Redis key for a given session."""
        return f"agri_bot:conversation:{session_id}"

    def get_conversation_history(
        self, session_id: str, max_turns: int = 10
    ) -> List[Dict[str, str]]:
        """Retrieve conversation history for a session.

        Tries Redis first, falls back to in-memory dict.

        Args:
            session_id: Unique session identifier.
            max_turns: Maximum number of recent message pairs to return.

        Returns:
            List of message dicts with 'role' and 'content' keys.
        """
        # Try Redis
        if self._redis_available and self._client is not None:
            try:
                key = self._get_session_key(session_id)
                raw = self._client.lrange(key, 0, -1)
                messages = [json.loads(item) for item in raw]
                return messages[-(max_turns * 2):]
            except Exception as exc:
                logger.error("Redis read error [%s]: %s", session_id, exc)
                # Fall through to in-memory

        # Fallback: in-memory
        with self._lock:
            messages = self._fallback.get(session_id, [])
        return messages[-(max_turns * 2):]

    def add_to_conversation(
        self, session_id: str, role: str, content: str
    ) -> None:
        """Add a message to the conversation history.

        Writes to both Redis (if available) and in-memory dict.

        Args:
            session_id: Unique session identifier.
            role: Either 'user' or 'assistant'.
            content: The message text.
        """
        message = {"role": role, "content": content}

        # Always write to in-memory fallback
        with self._lock:
            if session_id not in self._fallback:
                self._fallback[session_id] = []
            self._fallback[session_id].append(message)

        # Also try Redis
        if self._redis_available and self._client is not None:
            try:
                key = self._get_session_key(session_id)
                self._client.rpush(key, json.dumps(message))
                self._client.expire(key, self.config.REDIS_SESSION_TTL)
            except Exception as exc:
                logger.error("Redis write error [%s]: %s", session_id, exc)
                self._redis_available = False

    def clear_conversation(self, session_id: str) -> None:
        """Delete all conversation history for a session."""
        # Clear in-memory
        with self._lock:
            self._fallback.pop(session_id, None)

        # Clear Redis
        if self._redis_available and self._client is not None:
            try:
                self._client.delete(self._get_session_key(session_id))
            except Exception as exc:
                logger.error("Redis delete error [%s]: %s", session_id, exc)

    def health_check(self) -> bool:
        """Check if Redis connection is healthy."""
        if not self._redis_available or self._client is None:
            return False
        try:
            return self._client.ping()
        except Exception:
            return False
