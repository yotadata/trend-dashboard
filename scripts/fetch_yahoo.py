import requests
from bs4 import BeautifulSoup

def fetch_yahoo_trends():
    """
    Yahoo!リアルタイム検索からトレンドワードを取得する
    """
    url = "https://search.yahoo.co.jp/realtime"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.text, 'lxml')
        
        # Yahoo!リアルタイムのトレンドワードは特定のクラスを持つ要素に入っている
        # ページの構造は変更される可能性がある
        trend_items = soup.select('div.TopicsListItem_word_1z4Gg') # セレクタは実際のHTML構造に合わせる必要がある
        
        trends = []
        for item in trend_items:
            trends.append(item.get_text(strip=True))
            
        return trends[:10]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Yahoo Trends: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == '__main__':
    trends = fetch_yahoo_trends()
    if trends:
        print("Yahoo! Real-time Trends:")
        for i, trend in enumerate(trends, 1):
            print(f"{i}. {trend}")
    else:
        print("Failed to fetch Yahoo! Real-time Trends.")
