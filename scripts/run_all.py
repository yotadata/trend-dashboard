import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timezone, timedelta
from collections import Counter

from .fetch_google import fetch_google_trends
from .fetch_yahoo import fetch_yahoo_trends
from .fetch_togetter import fetch_togetter_trends
from .fetch_youtube import fetch_youtube_trends
from .notify_discord import send_discord_notification
from .save_to_sheet import save_trends_to_sheet

def run_all_tasks():
    jst = timezone(timedelta(hours=+9), 'JST')
    utc_now_iso = datetime.now(timezone.utc).isoformat()

    sources = {
        "Google Trends": fetch_google_trends,
        "YouTube": fetch_youtube_trends,
        "Yahoo! Real-time": fetch_yahoo_trends,
        "Togetter": fetch_togetter_trends,
    }
    
    all_trends_for_ranking = []
    categories_for_html = []
    data_for_sheet = []
    
    for source_name, fetch_function in sources.items():
        print(f"Fetching {source_name}...")
        try:
            trends = fetch_function()
            all_trends_for_ranking.extend(trends)
            categories_for_html.append({"name": source_name, "trends": trends})
            
            for i, keyword in enumerate(trends, 1):
                data_for_sheet.append({
                    "timestamp": utc_now_iso,
                    "source": source_name,
                    "keyword": keyword,
                    "rank": i
                })
        except Exception as e:
            print(f"  Error fetching {source_name}: {e}")
            categories_for_html.append({"name": source_name, "trends": []})

    if data_for_sheet:
        save_trends_to_sheet(data_for_sheet)

    daily_ranking = Counter(all_trends_for_ranking).most_common(10)
    
    today_str = datetime.now(jst).strftime('%Y年%m月%d日')
    message_lines = [f"**🏆 {today_str}のトレンドランキング Top 10**\n"]
    for i, (word, count) in enumerate(daily_ranking, 1):
        message_lines.append(f"**{i}位:** {word} `(x{count})`")
    
    message_lines.append("\n**🔍 各ソースのトレンド**")
    for cat in categories_for_html:
        if cat['trends']:
            message_lines.append(f"- **{cat['name']}:** {', '.join(cat['trends'][:3])}...")
    
    send_discord_notification("\n".join(message_lines))

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

if __name__ == '__main__':
    run_all_tasks()
