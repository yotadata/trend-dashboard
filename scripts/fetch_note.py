import requests
import xml.etree.ElementTree as ET

def fetch_note_trends():
    """
    noteのRSSフィードから人気記事のタイトルを取得する
    """
    url = "https://note.com/rss/popular"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        
        trends = []
        # RSSフィードの各アイテムからタイトルを抽出
        for item in root.findall('.//item'):
            title = item.find('title')
            if title is not None:
                trends.append(title.text)
        
        return trends[:10] # 上位10件を返す

    except requests.exceptions.RequestException as e:
        print(f"Error fetching note RSS: {e}")
        return []
    except ET.ParseError as e:
        print(f"Error parsing note XML: {e}")
        return []

if __name__ == '__main__':
    trends = fetch_note_trends()
    if trends:
        print("note Popular Articles:")
        for i, trend in enumerate(trends, 1):
            print(f"{i}. {trend}")
    else:
        print("Failed to fetch note articles.")
