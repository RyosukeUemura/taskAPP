#!/usr/bin/env bash
# =============================================================================
# deploy.sh — Cloud Run へのデプロイスクリプト
# 使い方: bash deploy.sh
# =============================================================================
set -euo pipefail

# -----------------------------------------------------------------------------
# ★ ここを自分の環境に合わせて書き換える ★
# -----------------------------------------------------------------------------

# GCP プロジェクト ID（例: my-project-123456）
GCP_PROJECT_ID="YOUR_GCP_PROJECT_ID"

# Cloud SQL インスタンスの接続名（例: my-project:asia-northeast1:my-instance）
# GCP コンソール > Cloud SQL > インスタンス詳細 > 「接続名」に記載されている値
CLOUD_SQL_CONNECTION_NAME="YOUR_PROJECT:asia-northeast1:YOUR_INSTANCE_NAME"

# Cloud SQL の接続情報
DB_PASSWORD="YOUR_DB_PASSWORD"      # Cloud SQL 作成時に設定したパスワード
DB_NAME="tracker_db"                # 使用するデータベース名（必要に応じて変更）
DB_USER="postgres"                  # データベースユーザー名

# Cloud Run サービス名・リージョン（変更不要であればそのまま）
SERVICE_NAME="task-app"
REGION="asia-northeast1"

# -----------------------------------------------------------------------------
# ここから下は通常変更不要
# -----------------------------------------------------------------------------

# Django の SECRET_KEY をランダム生成（デプロイのたびに新しい値を使用）
SECRET_KEY=$(python3 -c "
import secrets, string
chars = string.ascii_letters + string.digits + '-_+='
print(''.join(secrets.choice(chars) for _ in range(50)))
")

# Cloud Run から Cloud SQL へ接続する Unix ソケット形式の DATABASE_URL
DATABASE_URL="postgres://${DB_USER}:${DB_PASSWORD}@/${DB_NAME}?host=/cloudsql/${CLOUD_SQL_CONNECTION_NAME}"

echo "======================================================"
echo " デプロイ開始: ${SERVICE_NAME} → ${REGION}"
echo " プロジェクト: ${GCP_PROJECT_ID}"
echo " Cloud SQL   : ${CLOUD_SQL_CONNECTION_NAME}"
echo "======================================================"

# gcloud のアクティブプロジェクトを設定
gcloud config set project "${GCP_PROJECT_ID}"

# Cloud Run へデプロイ
gcloud run deploy "${SERVICE_NAME}" \
  --source . \
  --region "${REGION}" \
  --platform managed \
  --allow-unauthenticated \
  --add-cloudsql-instances "${CLOUD_SQL_CONNECTION_NAME}" \
  --set-env-vars "DJANGO_SETTINGS_MODULE=config.settings.production" \
  --set-env-vars "ALLOWED_HOSTS=*" \
  --set-env-vars "SECRET_KEY=${SECRET_KEY}" \
  --set-env-vars "DATABASE_URL=${DATABASE_URL}" \
  --set-env-vars "GCP_PROJECT_ID=${GCP_PROJECT_ID}"

echo ""
echo "======================================================"
echo " デプロイ完了！"
echo " サービス URL は上記ログの 'Service URL' を確認してください"
echo "======================================================"
