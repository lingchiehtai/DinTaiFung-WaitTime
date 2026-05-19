import requests
import csv
import schedule
import time
from datetime import datetime
from pathlib import Path

# 設定
STORE_ID = '0010'  # 高雄店
API_URL = 'https://www.dintaifung.tw/Queue/Home/WebApiTest'
LOG_FILE = 'wait_time_log.csv'
INTERVAL = 10  # 分鐘

# 初始化 CSV 標頭
def init_csv():
    if not Path(LOG_FILE).exists():
        with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['時間', '等候時間(分鐘)', '現場號碼', '外帶號碼'])

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
        
        timestamp = datetime.now().strftime('%Y/%m/%d %H:%M')
        wait_time = store_data['wait_time']
        dine_in_num = f"{store_data['num_1']},{store_data['num_2']}"
        takeout_num = store_data['togo_numbers']
        
        # 印出結果
        print(f"[{timestamp}] 等候時間: {wait_time} 分鐘")
        print(f"            現場叫號: {dine_in_num}")
        print(f"            外帶叫號: {takeout_num}")
        print('---')
        
        # 存到 CSV
        with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, wait_time, dine_in_num, takeout_num])
    
    except requests.exceptions.RequestException as error:
        print(f"[{datetime.now().strftime('%Y/%m/%d %H:%M')}] 請求失敗: {error}")
    except Exception as error:
        print(f"[{datetime.now().strftime('%Y/%m/%d %H:%M')}] 解析失敗: {error}")

# 主程式
if __name__ == '__main__':
    init_csv()
    print('🚀 開始監控高雄店等候時間...')
    print(f'⏱️  每 {INTERVAL} 分鐘抓取一次')
    print(f'📁 數據存在: {LOG_FILE}')
    print('---')
    
    fetch_wait_time()  # 立即執行一次
    
    # # 排程每 10 分鐘執行一次
    # schedule.every(INTERVAL).minutes.do(fetch_wait_time)
    
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
