# YouTube Data API v3 を使用するには、Google Cloud PlatformでAPIキーを取得する必要があります。
# 取得したAPIキーは、環境変数 'YOUTUBE_API_KEY' に設定してこのスクリプトを実行してください。
#
# APIキー取得手順の概要：
# 1. Google Cloud Platform (https://console.cloud.google.com/) にアクセス
# 2. 新しいプロジェクトを作成
# 3. 「APIとサービス」>「ライブラリ」で "YouTube Data API v3" を検索して有効化
# 4. 「APIとサービス」>「認証情報」で「認証情報を作成」>「APIキー」を選択
# 5. 作成されたAPIキーをコピーする

import os
import requests

def fetch_youtube_trends():
    """
    YouTube Data API v3 を使って、日本の急上昇動画のタイトルを取得する
    """
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        print("Error: YOUTUBE_API_KEY environment variable not set.")
        return []

    # 日本の急上昇動画を取得するAPIエンドポイント
    url = (
        "https://www.googleapis.com/youtube/v3/videos"
        "?part=snippet"
        "&chart=mostPopular"
        "&regionCode=JP"
        "&maxResults=10"
        f"&key={api_key}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        trends = []
        for item in data.get("items", []):
            title = item["snippet"]["title"]
            trends.append(title)
            
        return trends

    except requests.exceptions.RequestException as e:
        print(f"Error fetching YouTube trends: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == '__main__':
    # このスクリプトをテスト実行するには、以下のように環境変数を設定して実行してください
    # YOUTUBE_API_KEY="ここにあなたのAPIキー" python3 scripts/fetch_youtube.py
    trends = fetch_youtube_trends()
    if trends:
        print("YouTube Popular Videos (Japan):")
        for i, trend in enumerate(trends, 1):
            print(f"{i}. {trend}")
    else:
        print("Failed to fetch YouTube trends.")
