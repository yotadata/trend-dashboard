import gspread
import os
import json
from datetime import datetime, timezone

def save_trends_to_sheet(trends_data):
    """
    取得したトレンドデータをGoogleスプレッドシートに追記する
    """
    try:
        sa_key_str = os.environ.get("GCP_SA_KEY")
        if not sa_key_str:
            print("Warning: GCP_SA_KEY environment variable not set. Skipping sheet save.")
            return
        
        sa_key_json = json.loads(sa_key_str)
        gc = gspread.service_account_from_dict(sa_key_json)

        spreadsheet_key = os.environ.get("SPREADSHEET_KEY")
        if not spreadsheet_key:
            print("Warning: SPREADSHEET_KEY environment variable not set. Skipping sheet save.")
            return
            
        spreadsheet = gc.open_by_key(spreadsheet_key)
        worksheet = spreadsheet.sheet1

        rows_to_append = []
        for item in trends_data:
            rows_to_append.append([
                item["timestamp"],
                item["source"],
                item["keyword"],
                item["rank"]
            ])
            
        if not rows_to_append:
            print("No data to save to sheet.")
            return

        worksheet.append_rows(rows_to_append, value_input_option='USER_ENTERED')
        print(f"Successfully saved {len(rows_to_append)} rows to the spreadsheet.")

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Error: Spreadsheet with key '{spreadsheet_key}' not found or permission denied.")
        print("Please make sure the spreadsheet key is correct and you have shared it with the service account's email.")
    except Exception as e:
        print(f"An error occurred while saving to Google Sheet: {e}")

if __name__ == '__main__':
    test_data = [
        {"timestamp": datetime.now(timezone.utc).isoformat(), "source": "Test Source", "keyword": "Test Keyword 1", "rank": 1},
        {"timestamp": datetime.now(timezone.utc).isoformat(), "source": "Test Source", "keyword": "Test Keyword 2", "rank": 2},
    ]
    save_trends_to_sheet(test_data)
