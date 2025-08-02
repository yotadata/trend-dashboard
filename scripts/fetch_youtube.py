import os
import requests
from dotenv import load_dotenv

load_dotenv()

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
        "&maxResults=25"
        f"&key={api_key}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        trends_data = []
        for i, item in enumerate(data.get("items", []), 1):
            title = item["snippet"]["title"]
            trends_data.append({
                "rank": i,
                "term": title
            })
            
        return {"YouTube": trends_data}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching YouTube trends: {e}")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

if __name__ == '__main__':
    trends_by_source = fetch_youtube_trends()
    if trends_by_source:
        for source, trends_list in trends_by_source.items():
            print(f"--- {source} Popular Videos (Japan): ---")
            for item in trends_list:
                print(f"{item['rank']}. {item['term']}")
    else:
        print("Failed to fetch YouTube trends.")
