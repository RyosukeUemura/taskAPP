# ============================================================
# Build stage — 依存関係のインストール
# ============================================================
FROM python:3.13-slim AS builder

WORKDIR /build

# 依存関係だけを先にコピーしてキャッシュを最大活用
COPY backend/requirements/ ./requirements/

RUN pip install --upgrade pip \
 && pip install --no-cache-dir --prefix=/install -r requirements/production.txt


# ============================================================
# Runtime stage — 軽量な最終イメージ
# ============================================================
FROM python:3.13-slim

# 非 root ユーザーで実行（セキュリティベストプラクティス）
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# ビルドステージでインストールしたパッケージをコピー
COPY --from=builder /install /usr/local

# アプリケーションコードをコピー
COPY backend/ .

# 静的ファイルを収集（ビルド時にダミーキーを使用）
ENV DJANGO_SETTINGS_MODULE=config.settings.production
RUN SECRET_KEY=dummy-build-time-key \
    DATABASE_URL=sqlite:////tmp/dummy.db \
    ALLOWED_HOSTS=localhost \
    python manage.py collectstatic --noinput

# 非 root ユーザーに切り替え
USER appuser

# Cloud Run が要求する 8080 番ポート
EXPOSE 8080

# Gunicorn で起動（Cloud Run は PORT 環境変数で上書き可）
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8080", \
     "--workers", "2", \
     "--threads", "4", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "config.wsgi:application"]
