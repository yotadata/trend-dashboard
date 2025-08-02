import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

def send_discord_notification(message_content):
    """
    Discordにメッセージを送信する
    """
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("Warning: DISCORD_WEBHOOK_URL environment variable not set. Skipping notification.")
        return

    payload = {
        "content": message_content,
    }

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("Successfully sent Discord notification.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending Discord notification: {e}")

if __name__ == '__main__':
    test_message = "これはテスト通知です。\n- トレンド1\n- トレンド2"
    send_discord_notification(test_message)

