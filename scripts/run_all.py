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
    utc_now = datetime.now(timezone.utc)
    utc_date_str = utc_now.strftime('%Y-%m-%d')
    utc_time_str = utc_now.strftime('%H:%M:%S')

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
            # fetch_functionは辞書を返すことを想定
            trends_by_source = fetch_function()
            
            # 辞書からソース名とトレンドリストを取得
            for fetched_source_name, trends_list in trends_by_source.items():
                # all_trends_for_ranking にはキーワードのみを追加
                all_trends_for_ranking.extend([item['term'] for item in trends_list])
                
                # categories_for_html にはソース名とトレンドリストをそのまま追加
                categories_for_html.append({"name": fetched_source_name, "trends": trends_list})
                
                # data_for_sheet には各トレンドの詳細を追加
                for item in trends_list:
                    data_for_sheet.append({
                        "date": utc_date_str,
                        "time": utc_time_str,
                        "source": fetched_source_name,
                        "keyword": item['term'],
                        "rank": item['rank']
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
            message_lines.append(f"\n**--- {cat['name']} ---**")
            for item in cat['trends']:
                message_lines.append(f"{item['rank']}. {item['term']}")
        else:
            message_lines.append(f"\n**--- {cat['name']} (データなし) ---**")
    
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
