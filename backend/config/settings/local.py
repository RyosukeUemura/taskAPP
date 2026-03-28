"""
Local development settings.
"""

from .base import *  # noqa: F401, F403

DEBUG = True

# Allow all hosts locally
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# ---------------------------------------------------------------------------
# Development-only apps
# ---------------------------------------------------------------------------
INSTALLED_APPS += []  # noqa: F405

# ---------------------------------------------------------------------------
# Email backend (console for local)
# ---------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
