"""Gunicorn configuration for Render deployment."""
import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"
workers = 2
worker_class = "sync"
timeout = 120

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
