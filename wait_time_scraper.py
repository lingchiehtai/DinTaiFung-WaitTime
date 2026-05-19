import requests
import json
from datetime import datetime
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
os.environ['TZ'] = 'Asia/Taipei'

# 設定
STORE_ID = '0010'  # 高雄店
API_URL = 'https://www.dintaifung.tw/Queue/Home/WebApiTest'
SHEET_ID = '1OOmgcaofJtwCCFVZi74n2_wLcrxkKLziZzrXsJArosk'
SHEET_NAME = '工作表1'  # Google Sheet 預設工作表名稱

# Google Sheets API 認證
def get_sheet_service():
    creds_json = os.getenv('GOOGLE_CREDENTIALS')
    creds_dict = json.loads(creds_json)
    
    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    
    return build('sheets', 'v4', credentials=creds)

# 抓取等候時間
def fetch_wait_time():
    try:
        payload = {'storeid': STORE_ID}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        response = requests.post(API_URL, data=payload, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        store_data = data[0]
        
        timestamp = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        wait_time = store_data['wait_time']
        dine_in_num = f"{store_data['num_1']},{store_data['num_2']}"
        takeout_num = store_data['togo_numbers']
        
        # 印出結果
        print(f"[{timestamp}] 等候時間: {wait_time} 分鐘")
        print(f"            現場叫號: {dine_in_num}")
        print(f"            外帶叫號: {takeout_num}")
        
        # 寫入 Google Sheet
        write_to_sheet(timestamp, wait_time, dine_in_num, takeout_num)
        print('✅ 已寫入 Google Sheet')
    
    except requests.exceptions.RequestException as error:
        print(f"❌ 請求失敗: {error}")
    except Exception as error:
        print(f"❌ 錯誤: {error}")

# 寫入 Google Sheet
def write_to_sheet(timestamp, wait_time, dine_in_num, takeout_num):
    service = get_sheet_service()
    
    values = [[timestamp, wait_time, dine_in_num, takeout_num]]
    
    body = {
        'values': values
    }
    
    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=f'{SHEET_NAME}!A:D',
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()

# 主程式
if __name__ == '__main__':
    print('🚀 開始抓取高雄店等候時間...')
    fetch_wait_time()
