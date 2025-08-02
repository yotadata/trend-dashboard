import os
import json
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

def fetch_google_trends():
    """
    BigQueryのgoogle_trends.international_top_termsテーブルから、
    前日の日本のトレンドデータを取得する。
    """
    sa_key_str = os.environ.get("GCP_SA_KEY")
    project_id = os.environ.get("GCP_PROJECT_ID")

    if not sa_key_str:
        print("Warning: GCP_SA_KEY environment variable not set. Skipping Google trends.")
        return []

    try:
        sa_key_json = json.loads(sa_key_str)
        credentials = service_account.Credentials.from_service_account_info(
            sa_key_json,
            scopes=["https://www.googleapis.com/auth/bigquery"],
        )
        client = bigquery.Client(credentials=credentials, project=project_id)

        # クエリの日付を昨日に設定
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_str = yesterday.strftime('%Y-%m-%d')

        query = f"""
            SELECT
              term
            FROM `bigquery-public-data.google_trends.international_top_terms`
            WHERE
                refresh_date = DATE('{yesterday_str}')
                AND country_name = "Japan"
            GROUP BY term, rank
            ORDER BY rank asc
            LIMIT 25
        """

        query_job = client.query(query)
        results = query_job.result()  # Waits for the job to complete.

        trends = [row.term for row in results]
        return trends

    except Exception as e:
        print(f"An error occurred while fetching from BigQuery: {e}")
        return []

if __name__ == '__main__':
    # .envファイルにGCP_PROJECT_IDも設定してください
    if not os.environ.get("GCP_PROJECT_ID"):
        print("Please set the GCP_PROJECT_ID environment variable in your .env file.")
    else:
        trends = fetch_google_trends()
        if trends:
            print("Google Trends (Yesterday from BigQuery):")
            for i, trend in enumerate(trends, 1):
                print(f"{i}. {trend}")
        else:
            print("Failed to fetch Google Trends from BigQuery.")