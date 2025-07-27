# 📊 TrendDashboard

コンテンツ発想の種となる「絶妙に一般的なトレンドワード」を収集し、  
**日次／週次／月次で1ページに一覧表示するダッシュボード**を、**無料で自動更新・GitHub Pagesにて公開**します。

---

## ✅ プロジェクト概要

- **名称（仮）：** TrendDashboard  
- **目的：** トレンドワードを視認性重視の一覧形式で毎日チェックできるダッシュボードを提供し、コンテンツ企画に役立てる

---

## ⚙️ セットアップと実行

### 1. APIキーの取得と設定

本ダッシュボードは、YouTubeのトレンド情報を取得するために **YouTube Data API v3** を使用します。  
APIを利用するには、Google Cloud Platform (GCP) で **APIキー** を取得し、このリポジトリに設定する必要があります。

1.  **APIキーの取得:**
    1.  [Google Cloud Platform](https://console.cloud.google.com/) にアクセスし、Googleアカウントでログインします。
    2.  新しいプロジェクトを作成するか、既存のプロジェクトを選択します。
    3.  左上のメニューから「APIとサービス」>「ライブラリ」を選択します。
    4.  `YouTube Data API v3` を検索し、有効化します。
    5.  左メニューの「APIとサービス」>「認証情報」を選択します。
    6.  画面上部の「認証情報を作成」をクリックし、「APIキー」を選択します。
    7.  作成されたAPIキーが表示されたら、コピーしておきます。

2.  **GitHubリポジトリへの設定:**
    1.  このGitHubリポジトリのページにアクセスします。
    2.  `Settings` タブ > `Secrets and variables` > `Actions` を選択します。
    3.  `New repository secret` ボタンをクリックします。
    4.  **Name** に `YOUTUBE_API_KEY` と入力します。
    5.  **Secret** に、先ほどコピーしたAPIキーを貼り付けます。
    6.  `Add secret` をクリックして保存します。

### 2. GitHub Pages の設定

ダッシュボードをインターネットに公開するために、GitHub Pagesを有効化します。

1.  このリポジトリの `Settings` タブ > `Pages` を選択します。
2.  **Source** (または Build and deployment) の項目で、Branchを `gh-pages` に設定します。
3.  `Save` をクリックします。

設定が完了すると、`https://<あなたのユーザー名>.github.io/<リポジトリ名>/` でダッシュボードが公開されます。

### 3. 自動更新

上記の設定が完了していれば、毎日午前9時（日本時間）に自動でトレンド情報が更新されます。  
手動で更新したい場合は、リポジトリの `Actions` タブから `Update Trend Dashboard` ワークフローを選択し、`Run workflow` を実行してください。

---

## ⚠️ 現在の状況と今後の課題

-   **データソース:**
    -   [✅] **YouTube:** API経由で安定取得可能。
    -   [⚠️] **Google, Yahoo, Togetter, note:** 各サービスの仕様変更やRSSフィードの提供終了により、現在スクリプトでの安定した自動取得が困難な状況です。今後、代替ソースを探すか、ヘッドレスブラウザの導入などを検討する可能性があります。
-   **出力ページ:**
    -   [✅] `daily.html`
    -   [🚧] `weekly.html`, `monthly.html` （未実装）
-   **通知:**
    -   [🚧] Discord通知 （未実装）

---

## ✅ 全体構成

| 区分 | 内容 |
|------|------|
| 🎯 入力 | トレンド収集：Googleトレンド・Yahooリアルタイム・YouTube急上昇・Togetterまとめ・note人気記事 |
| ⚙️ 処理 | Pythonでスクレイピング/API → Jinja2でHTML出力 |
| 🚀 出力 | HTML一覧ページ（`daily.html`など）としてGitHub Pagesで公開 |
| 🔁 自動化 | GitHub Actions（cron）で毎朝自動更新（+ 任意でDiscord通知） |

---

## ✅ 機能要件（Functional Requirements）

| 機能 | 説明 |
|------|------|
| [F-1] トレンド収集 | 各データソースからTOP5〜10の話題語句を取得する |
| [F-2] カテゴリ分け | ソースごとに区切って表示（Google / Yahoo / YouTube / Togetter / note） |
| [F-3] 表示UI | モバイルでも読みやすいシンプルなカード型一覧 |
| [F-4] 日/週/月出力 | Daily / Weekly / MonthlyごとにHTML出力を分ける |
| [F-5] 自動更新 | GitHub Actionsで09:00 JSTに更新 |
| [F-6] 公開 | GitHub Pagesで公開（`/daily.html`, `/weekly.html`, `/monthly.html`） |
| [F-7] 通知（任意） | Discord Webhookで「更新された」通知を送信可能（オプション） |

---

## ✅ 非機能要件（Non-functional Requirements）

| 項目 | 要件 |
|------|------|
| セキュリティ | Discord Webhookなどの秘密情報はGitHub Secretsで管理 |
| 費用 | すべて無料枠内で完結する（GitHub Actions + Pages + 公開RSS等） |
| 保守性 | 各ソース別に取得モジュールを分離（fetch_google.py など） |
| 拡張性 | 今後ソースを増やす／フィルタする際にも柔軟に対応可能 |
| 使用言語 | Python（Gemini CLI 上でも編集しやすいようシンプル構成） |

---

## ✅ 想定ディレクトリ構成

```plaintext
trend-dashboard/
├─ scripts/
│   ├─ fetch_google.py
│   ├─ fetch_yahoo.py
│   ├─ fetch_youtube.py
│   ├─ fetch_togetter.py
│   ├─ fetch_note.py
│   └─ generate_html.py
├─ templates/
│   └─ dashboard_template.html
├─ output/
│   ├─ daily.html
│   ├─ weekly.html
│   └─ monthly.html
├─ .github/workflows/
│   └─ update_trends.yml
├─ requirements.txt
└─ README.md
