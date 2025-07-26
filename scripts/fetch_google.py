import requests
import xml.etree.ElementTree as ET

def fetch_google_trends():
    """
    GoogleトレンドのRSSフィードから日本の急上昇ワードを取得する
    """
    url = "https://trends.google.co.jp/trends/trendingsearches/daily/rss?geo=JP"
    try:
        response = requests.get(url)
        response.raise_for_status()  # エラーがあれば例外を発生させる

        root = ET.fromstring(response.content)
        trends = []
        # RSSフィードの各アイテムからタイトル（キーワード）を抽出
        for item in root.findall('.//item'):
            title = item.find('title')
            if title is not None:
                trends.append(title.text)
        
        return trends[:10] # 上位10件を返す
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Google Trends RSS: {e}")
        return []
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []

if __name__ == '__main__':
    trends = fetch_google_trends()
    if trends:
        print("Google Trends (Japan) from RSS:")
        for i, trend in enumerate(trends, 1):
            print(f"{i}. {trend}")
    else:
        print("Failed to fetch Google Trends.")