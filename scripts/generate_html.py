import os
import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timezone, timedelta
from collections import Counter

# 各トレンド取得スクリプトをインポート
from .fetch_google import fetch_google_trends
from .fetch_yahoo import fetch_yahoo_trends
from .fetch_togetter import fetch_togetter_trends
from .fetch_youtube import fetch_youtube_trends
from .notify_discord import send_discord_notification

def aggregate_and_generate():
    """
    各ソースからトレンドデータを取得し、集約、HTML生成、Discord通知、データ保存を行う
    """
    # --- 1. データの取得 ---
    sources = {
        "Google Trends": fetch_google_trends,
        "YouTube": fetch_youtube_trends,
        "Yahoo! Real-time": fetch_yahoo_trends,
        "Togetter": fetch_togetter_trends,
    }
    
    all_trends = []
    categories_for_html = []
    
    for name, fetch_function in sources.items():
        print(f"Fetching {name}...")
        try:
            trends = fetch_function()
            all_trends.extend(trends)
            categories_for_html.append({"name": name, "trends": trends})
        except Exception as e:
            print(f"  Error fetching {name}: {e}")
            categories_for_html.append({"name": name, "trends": []})

    # --- 2. 日次ランキングの集計 ---
    daily_ranking = Counter(all_trends).most_common(10)

    # --- 3. Discord通知メッセージの作成と送信 ---
    jst = timezone(timedelta(hours=+9), 'JST')
    today_str = datetime.now(jst).strftime('%Y年%m月%d日')
    
    message_lines = [f"**🏆 {today_str}のトレンドランキング Top 10**\n"]
    for i, (word, count) in enumerate(daily_ranking, 1):
        message_lines.append(f"**{i}位:** {word} `(x{count})`")
    
    # 各ソースのトレンドもメッセージに含める
    message_lines.append("\n**🔍 各ソースのトレンド**")
    for cat in categories_for_html:
        if cat['trends']:
            message_lines.append(f"- **{cat['name']}:** {', '.join(cat['trends'][:3])}...")
    
    send_discord_notification("\n".join(message_lines))

    # --- 4. HTMLの生成 ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '..')
    templates_dir = os.path.join(project_root, 'templates')
    output_dir = os.path.join(project_root, 'output')

    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('dashboard_template.html')

    html_data = {
        "categories": categories_for_html,
        "last_updated": datetime.now(jst).strftime('%Y-%m-%d %H:%M:%S JST')
    }
    html_content = template.render(html_data)
    
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'daily.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Successfully generated {output_path}")

    # --- 5. 日次データの保存 ---
    data_dir = os.path.join(project_root, 'data')
    data_path = os.path.join(data_dir, 'daily_trends.json')
    os.makedirs(data_dir, exist_ok=True)
    
    daily_data = {}
    if os.path.exists(data_path):
        with open(data_path, 'r', encoding='utf-8') as f:
            daily_data = json.load(f)
            
    date_key = datetime.now(jst).strftime('%Y-%m-%d')
    daily_data[date_key] = all_trends
    
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(daily_data, f, ensure_ascii=False, indent=4)
    print(f"Successfully saved daily trends to {data_path}")


if __name__ == '__main__':
    aggregate_and_generate()