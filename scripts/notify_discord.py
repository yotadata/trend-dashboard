import requests
import os
import json

def send_discord_notification(message_content):
    """
    Discordにメッセージを送信する

    Args:
        message_content (str): 送信するメッセージ本文
    """
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("Warning: DISCORD_WEBHOOK_URL environment variable not set. Skipping notification.")
        return

    # Discordの埋め込み形式(embeds)を使うと見栄えが良くなる
    # メッセージが長すぎる場合も考慮し、descriptionに本文を入れる
    payload = {
        "embeds": [
            {
                "title": "📊 トレンドダッシュボード更新通知",
                "description": message_content,
                "color": 5814783  # 16進数カラーコード 0x58B9FF
            }
        ]
    }

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("Successfully sent Discord notification.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending Discord notification: {e}")

if __name__ == '__main__':
    # テスト実行用のコード
    # 環境変数にDISCORD_WEBHOOK_URLを設定して実行してください
    # DISCORD_WEBHOOK_URL="your_webhook_url" python3 scripts/notify_discord.py
    test_message = "これはテスト通知です。\n- トレンド1\n- トレンド2"
    send_discord_notification(test_message)
