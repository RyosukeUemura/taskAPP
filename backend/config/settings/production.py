"""
Production settings for Cloud Run deployment.
Secrets are injected via GCP Secret Manager / environment variables.
"""

import os

import dj_database_url

from .base import *  # noqa: F401, F403

# ---------------------------------------------------------------------------
# Security — DEBUG は絶対に True にしない
# ---------------------------------------------------------------------------
DEBUG = False

ALLOWED_HOSTS: list[str] = os.environ.get("ALLOWED_HOSTS", "").split(",")

# Cloud Run のヘルスチェック等に備えて空文字エントリを除去
ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS if h.strip()]

# ---------------------------------------------------------------------------
# Database — DATABASE_URL 環境変数から dj_database_url で上書き
# ---------------------------------------------------------------------------
_db_url = os.environ.get("DATABASE_URL")
if _db_url:
    DATABASES = {  # noqa: F405
        "default": dj_database_url.parse(
            _db_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

# ---------------------------------------------------------------------------
# Static files — WhiteNoise で本番配信
# ---------------------------------------------------------------------------
# SecurityMiddleware の直後に挿入して圧縮・キャッシュを有効化
MIDDLEWARE = [  # noqa: F405
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
] + MIDDLEWARE[1:]  # noqa: F405

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}

# ---------------------------------------------------------------------------
# HTTPS / Security hardening
# ---------------------------------------------------------------------------
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000        # 1 年
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")  # Cloud Run LB 対応
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ---------------------------------------------------------------------------
# GCP Secret Manager — シークレット取得ヘルパー（必要時にコメントアウト解除）
# ---------------------------------------------------------------------------
# from google.cloud import secretmanager
#
# def get_secret(secret_id: str, project_id: str | None = None) -> str:
#     """Secret Manager からシークレット値を取得する。"""
#     project = project_id or os.environ["GCP_PROJECT_ID"]
#     client = secretmanager.SecretManagerServiceClient()
#     name = f"projects/{project}/secrets/{secret_id}/versions/latest"
#     response = client.access_secret_version(request={"name": name})
#     return response.payload.data.decode("UTF-8")
#
# SECRET_KEY = get_secret("django-secret-key")
