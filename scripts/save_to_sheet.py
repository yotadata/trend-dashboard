import gspread
import os
import json
from datetime import datetime, timezone, timedelta

def save_trends_to_sheet(trends_data):
    """
    取得したトレンドデータを、月ごとのワークシートに追記する。
    ただし、同日のデータが既に存在する場合は追記しない。
    """
    try:
        # --- 認証 ---
        sa_key_str = os.environ.get("GCP_SA_KEY")
        if not sa_key_str:
            print("Warning: GCP_SA_KEY environment variable not set. Skipping sheet save.")
            return
        
        sa_key_json = json.loads(sa_key_str)
        gc = gspread.service_account_from_dict(sa_key_json)

        # --- スプレッドシートとワークシートの準備 ---
        spreadsheet_key = os.environ.get("SPREADSHEET_KEY")
        if not spreadsheet_key:
            print("Warning: SPREADSHEET_KEY environment variable not set. Skipping sheet save.")
            return
            
        spreadsheet = gc.open_by_key(spreadsheet_key)
        current_month_str = datetime.now(timezone.utc).strftime('%Y-%m')
        
        try:
            worksheet = spreadsheet.worksheet(current_month_str)
        except gspread.exceptions.WorksheetNotFound:
            print(f"Worksheet '{current_month_str}' not found. Creating a new one.")
            worksheet = spreadsheet.add_worksheet(title=current_month_str, rows="1000", cols="4")
            worksheet.append_row(["timestamp", "source", "keyword", "rank"], value_input_option='USER_ENTERED')
            print(f"Worksheet '{current_month_str}' created and header added.")
        
        # --- 今日の日付のデータが既に存在するかチェック ---
        jst = timezone(timedelta(hours=+9), 'JST')
        today_jst_str = datetime.now(jst).strftime('%Y-%m-%d')
        
        all_values = worksheet.get_all_values()
        
        if len(all_values) > 1: # ヘッダー行以外にデータがある場合のみチェック
            for row in all_values[1:]:
                if row and row[0]: # タイムスタンプ列が存在する場合
                    utc_timestamp = datetime.fromisoformat(row[0])
                    row_jst_date_str = utc_timestamp.astimezone(jst).strftime('%Y-%m-%d')
                    
                    if row_jst_date_str == today_jst_str:
                        print(f"Data for today ({today_jst_str}) already exists. Skipping save.")
                        return # 処理を終了

        # --- 追記するデータを作成 ---
        rows_to_append = []
        for item in trends_data:
            rows_to_append.append([
                item["timestamp"],
                item["source"],
                item["keyword"],
                item["rank"]
            ])
            
        if not rows_to_append:
            print("No new data to save to sheet.")
            return

        # --- シートに追記 ---
        worksheet.append_rows(rows_to_append, value_input_option='USER_ENTERED')
        print(f"Successfully saved {len(rows_to_append)} new rows to worksheet '{current_month_str}'.")

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Error: Spreadsheet with key '{spreadsheet_key}' not found or permission denied.")
    except Exception as e:
        print(f"An error occurred while saving to Google Sheet: {e}")

if __name__ == '__main__':
    test_data = [
        {"timestamp": datetime.now(timezone.utc).isoformat(), "source": "Test Source", "keyword": "Test Keyword 1", "rank": 1},
        {"timestamp": datetime.now(timezone.utc).isoformat(), "source": "Test Source", "keyword": "Test Keyword 2", "rank": 2},
    ]
    save_trends_to_sheet(test_data)
