# taskAPP — CLAUDE.md

## プロジェクト概要

**サブスクリプション＆定期タスク管理アプリ**

ユーザーのサブスクリプション契約（サービス名・金額・更新日など）と定期タスク（毎月の支払い確認、契約見直しなど）を一元管理するWebアプリケーション。

---

## 技術スタック

### バックエンド
- **言語**: Python 3.12+
- **フレームワーク**: Django 5.x + Django REST Framework
- **タスクキュー**: Cloud Scheduler + Cloud Tasks（または Celery on Cloud Run）
- **認証**: Django Allauth / JWT（djangorestframework-simplejwt）

### フロントエンド（予定）
- React または Next.js（別リポジトリまたは `frontend/` ディレクトリ）

### インフラ（GCP）
| サービス | 用途 |
|---|---|
| Cloud Run | Django アプリのコンテナ実行 |
| Cloud SQL (PostgreSQL) | メインデータベース |
| Cloud Scheduler | 定期タスクのcronトリガー |
| Cloud Tasks | 非同期タスクキュー |
| Cloud Storage | 静的ファイル・メディアファイル |
| Secret Manager | 機密情報（DB パスワード、API キーなど）の管理 |
| Artifact Registry | Docker イメージの保存 |
| Cloud Build | CI/CD パイプライン |

---

## ディレクトリ構成（方針）

```
taskAPP/
├── backend/
│   ├── config/          # Django プロジェクト設定
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── local.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── subscriptions/   # サブスクリプション管理
│   │   ├── tasks/           # 定期タスク管理
│   │   └── users/           # ユーザー・認証
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── local.txt
│   │   └── production.txt
│   ├── Dockerfile
│   └── manage.py
├── infra/               # Terraform / デプロイ設定
├── .github/
│   └── workflows/       # GitHub Actions CI/CD
├── CLAUDE.md
└── README.md
```

---

## 開発ルール

### 全般
- 過度な抽象化・早期の汎用化は避ける。現在の要件に対して最小限の実装を行う
- セキュリティ上の問題（SQLインジェクション、XSS、認証漏れ等）が見つかった場合は即座に修正する
- 環境変数・シークレットは Secret Manager で管理し、コードに直接記述しない
- `DEBUG=True` の設定は本番環境に絶対に含めない

### Python / Django
- フォーマッター: **Black**（行長 88）
- リンター: **Ruff**
- 型ヒント: 新規コードには積極的に付ける
- マイグレーションは `makemigrations` 後に必ずレビューしてからコミットする
- テストは `pytest-django` を使用する

---

## Git ルール

### ブランチ戦略

```
main          # 本番環境に対応。直接プッシュ禁止
develop       # 統合ブランチ。PR経由でのみマージ
feature/*     # 新機能開発
fix/*         # バグ修正
hotfix/*      # 本番の緊急修正（main から分岐）
chore/*       # 依存関係更新・設定変更など
```

- `main` および `develop` への直接プッシュは禁止
- すべての変更は PR（Pull Request）経由でマージする
- `main` へのマージは `develop` からのみ行う

### コミットメッセージ規約（Conventional Commits）

```
<type>(<scope>): <summary>

[body]

[footer]
```

**type の種類:**
| type | 用途 |
|---|---|
| `feat` | 新機能 |
| `fix` | バグ修正 |
| `docs` | ドキュメントのみの変更 |
| `style` | フォーマット変更（動作に影響なし） |
| `refactor` | リファクタリング |
| `test` | テストの追加・修正 |
| `chore` | ビルド・依存関係・CI の変更 |
| `perf` | パフォーマンス改善 |

**例:**
```
feat(subscriptions): サブスクリプション一覧APIを追加

GET /api/subscriptions/ でユーザーの契約一覧を返す。
フィルタリング（カテゴリ・更新月）にも対応。
```

- サマリーは **日本語または英語** で統一（プロジェクト内で一方に揃える）
- サマリーは50文字以内を目安にする
- 本文が必要な場合は1行空けて記述する

### PR ルール
- タイトルはコミットメッセージと同じ形式（`feat: ...`）
- レビュワーを最低1名アサインする
- CI（テスト・lint）が通過してからマージする
- マージ後はブランチを削除する

### タグ・リリース
- リリースには `v1.0.0` 形式のセマンティックバージョニングを使用する
- `main` マージ時に GitHub Actions でタグを自動付与する（予定）

---

## 環境変数

ローカル開発では `.env` ファイルを使用する（`.gitignore` に必ず含めること）。

```
# .env.example
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/taskapp
ALLOWED_HOSTS=localhost,127.0.0.1
GCP_PROJECT_ID=your-project-id
```

本番環境の値は GCP Secret Manager に保存し、Cloud Run の環境変数として注入する。

---

## デプロイフロー

1. `develop` ブランチへ PR をマージ → Cloud Build が自動でステージング環境へデプロイ
2. ステージング確認後、`develop` → `main` へ PR を作成・マージ
3. `main` マージ → Cloud Build が本番 Cloud Run へデプロイ

---

## ローカル開発セットアップ（予定）

```bash
# リポジトリのクローン
git clone <repo-url>
cd taskAPP

# Python 仮想環境
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements/local.txt

# 環境変数
cp backend/.env.example backend/.env
# .env を編集

# DB マイグレーション
cd backend
python manage.py migrate

# 開発サーバー起動
python manage.py runserver
```
