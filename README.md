# 📊 TrendDashboard

コンテンツ発想の種となる「絶妙に一般的なトレンドワード」を収集し、  
**日次／週次／月次で1ページに一覧表示するダッシュボード**を、**無料で自動更新・GitHub Pagesにて公開**します。

---

## ⚙️ セットアップと実行

本ダッシュボードは、トレンド情報の取得、通知、データ蓄積のために外部サービスとの連携が必要です。  
以下の手順に従って、必要なキーや設定を準備してください。

### 1. Google Cloud Platform (GCP) の設定

1.  **APIの有効化:**
    *   お使いのGCPプロジェクトで、以下の **3つのAPI** を有効化してください。
        *   **YouTube Data API v3** （トレンド取得用）
        *   **Google Sheets API** （データ保存用）
        *   **Google Drive API** （データ保存用）

2.  **サービスアカウントの作成:**
    *   GCPの「IAMと管理」>「サービスアカウント」で、新しいサービスアカウントを作成します。
    *   作成したサービスアカウントに、以下の **2つのロール** を付与してください。
        *   `閲覧者` (roles/viewer) - 基本的な閲覧権限
        *   `Workflows 実行者` (roles/workflows.invoker) - API実行権限
    *   サービスアカウントのキーを作成し、**JSON形式**でダウンロードします。

### 2. Googleスプレッドシートの準備

1.  **スプレッドシートの作成:**
    *   Googleドライブで、データを蓄積するためのスプレッドシートを新規に作成します。
    *   シートの1行目に、ヘッダーとして以下の4つを順番に入力してください。
        `timestamp`, `source`, `keyword`, `rank`

2.  **サービスアカウントとの共有:**
    *   作成したスプレッドシートの右上の「共有」ボタンを押します。
    *   共有相手として、先ほど作成したサービスアカウントのメールアドレス（JSONキーファイル内の `client_email` の値）を追加し、「**編集者**」の権限を与えます。

### 3. GitHubリポジトリへの設定

取得したキーやIDを、このリポジトリの `Settings` > `Secrets and variables` > `Actions` に設定します。

*   **`YOUTUBE_API_KEY`**:
    *   GCPの「認証情報」で作成した**APIキー**を設定します。
*   **`GCP_SA_KEY`**:
    *   ダウンロードした**サービスアカウントのJSONキーの中身全体**を貼り付けます。
*   **`SPREADSHEET_KEY`**:
    *   作成したGoogleスプレッドシートの**キー（ID）**を設定します。
    *   **キーの確認方法:** スプレッドシートを開いたときのURL `https://docs.google.com/spreadsheets/d/【この部分がキーです】/edit` の、`/d/` と `/edit` の間にある長い文字列です。
*   **`DISCORD_WEBHOOK_URL`**:
    *   通知を送りたいDiscordチャンネルで作成した**WebhookのURL**を設定します。

### 4. GitHub Pages の設定

ダッシュボードをインターネットに公開するために、GitHub Pagesを有効化します。

1.  このリポジトリの `Settings` タブ > `Pages` を選択します。
2.  **Source** (または Build and deployment) の項目で、Branchを `gh-pages` に設定します。
3.  `Save` をクリックします。

設定が完了すると、`https://<あなたのユーザー名>.github.io/<リポジトリ名>/daily.html` でダッシュボードが公開されます。

### 5. 自動更新

上記の設定が完了していれば、毎日午前9時（日本時間）に自動でトレンド情報が更新されます。  
手動で更新したい場合は、リポジトリの `Actions` タブから `Update Trend Dashboard` ワークフローを選択し、`Run workflow` を実行してください。

---

## ⚠️ 現在の状況と今後の課題

-   **データソース:**
    -   [✅] **YouTube:** API経由で安定取得可能。
    -   [✅] **Google:** Selenium経由で取得可能。
    -   [⚠️] **Yahoo, Togetter, note:** 各サービスの仕様変更やRSSフィードの提供終了により、現在スクリプトでの安定した自動取得が困難な状況です。
-   **データ保存:**
    -   [✅] Google Sheets
-   **通知:**
    -   [✅] Discord
-   **出力ページ:**
    -   [✅] `daily.html`
    -   [🚧] `weekly.html`, `monthly.html` （Looker Studioでの可視化を推奨）

---
