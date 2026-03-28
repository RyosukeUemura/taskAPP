"""
Production settings for Cloud Run deployment.
Secrets are injected via GCP Secret Manager / environment variables.
"""

from .base import *  # noqa: F401, F403

DEBUG = False  # NEVER change this to True in production

# ALLOWED_HOSTS is set via the ALLOWED_HOSTS env var (comma-separated)

# ---------------------------------------------------------------------------
# Security hardening
# ---------------------------------------------------------------------------
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ---------------------------------------------------------------------------
# Static files (Cloud Storage via whitenoise or GCS backend)
# ---------------------------------------------------------------------------
MIDDLEWARE = ["whitenoise.middleware.WhiteNoiseMiddleware"] + MIDDLEWARE  # noqa: F405
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
