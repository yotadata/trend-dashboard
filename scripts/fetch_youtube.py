import os
import requests

def fetch_youtube_trends():
    """
    YouTube Data API v3 を使って、日本の急上昇動画のタイトルを取得する
    """
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        print("Warning: YOUTUBE_API_KEY environment variable not set. Skipping YouTube trends.")
        return []

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
    trends = fetch_youtube_trends()
    if trends:
        print("YouTube Popular Videos (Japan):")
        for i, trend in enumerate(trends, 1):
            print(f"{i}. {trend}")
    else:
        print("Failed to fetch YouTube trends.")
