import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timezone, timedelta

# 各トレンド取得スクリプトをインポート
from fetch_google import fetch_google_trends
from fetch_yahoo import fetch_yahoo_trends
from fetch_togetter import fetch_togetter_trends
from fetch_youtube import fetch_youtube_trends

def generate_html():
    """
    各ソースからトレンドデータを取得し、HTMLを生成する
    """
    # 日本時間のタイムゾーン
    jst = timezone(timedelta(hours=+9), 'JST')
    
    # データソースと対応する関数を定義
    sources = {
        "Google Trends": fetch_google_trends,
        "Yahoo! Real-time": fetch_yahoo_trends,
        "Togetter": fetch_togetter_trends,
        "YouTube": fetch_youtube_trends,
        # "note": fetch_note_trends,
    }
    
    categories = []
    for name, fetch_function in sources.items():
        print(f"Fetching {name}...")
        try:
            trends = fetch_function()
        except Exception as e:
            print(f"  Error: {e}")
            trends = []
        categories.append({"name": name, "trends": trends})

    # Jinja2のセットアップ
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '..')
    templates_dir = os.path.join(project_root, 'templates')
    output_dir = os.path.join(project_root, 'output')

    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('dashboard_template.html')

    # テンプレートに渡すデータ
    data = {
        "categories": categories,
        "last_updated": datetime.now(jst).strftime('%Y-%m-%d %H:%M:%S JST')
    }

    # HTMLをレンダリング
    html_content = template.render(data)

    # outputディレクトリにHTMLファイルを出力
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'daily.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"Successfully generated {output_path}")

if __name__ == '__main__':
    generate_html()
