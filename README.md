# 鼎泰豐等候時間監控系統

自動監控鼎泰豐高雄店現場等候時間，每 10 分鐘抓取一次數據並存到 Google Sheet。

## 功能

- ⏱️ 每 10 分鐘自動抓取一次等候時間
- 📊 數據自動寫入 Google Sheet
- ☁️ 運行在 GitHub Actions（無需本地電腦開著）
- 📈 長期累積數據，方便分析

## 追蹤內容

- **等候時間** - 現場等候分鐘數
- **現場叫號** - 目前叫號的號碼
- **外帶叫號** - 外帶叫號的號碼
- **時間戳** - 抓取的時間

## 快速開始

### 必備條件

- GitHub 帳號
- Google 帳號
- Google Cloud 專案（有服務帳戶金鑰）

### 安裝步驟

#### 1. 準備 Google Sheet

1. 建立新的 Google 試算表：https://sheets.google.com
2. 命名為「鼎泰豐等候時間」
3. 在第一列加上標題：
   - A1: `時間`
   - B1: `等候時間(分鐘)`
   - C1: `現場號碼`
   - D1: `外帶號碼`
4. 記下 Sheet ID（網址中的這段）：
   ```
   https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
   ```

#### 2. 設定 Google Cloud API

1. 進入 Google Cloud Console：https://console.cloud.google.com
2. 建立新專案
3. 啟用 API：
   - Google Sheets API
   - Google Drive API
4. 建立服務帳戶：
   - 左邊菜單 → 認證資訊 → 建立認證資訊 → 服務帳戶
5. 建立金鑰：
   - 進入服務帳戶 → 金鑰標籤 → 新增金鑰 → JSON 格式
   - 下載金鑰檔案
6. 分享 Google Sheet 給服務帳戶：
   - 從 JSON 檔案複製 `client_email`
   - 在 Google Sheet 點分享 → 貼入 email → 給予編輯權限

#### 3. 上傳檔案到 GitHub

1. 在你的 GitHub repository 上傳這些檔案：
   - wait_time_scraper.py
   - requirements.txt
   - .github/workflows/main.yml（在 .github 資料夾內）
2. 編輯 wait_time_scraper.py：
   - 修改 SHEET_ID 為你的 Google Sheet ID
3. 在 Settings → Secrets and variables → Actions
4. 新增 Secret：
   - Name: GOOGLE_CREDENTIALS
   - Value: 貼入整個 JSON 金鑰檔案內容

#### 4. 啟動 GitHub Actions

1. 進入倉庫的 Actions 標籤
2. 點左邊「DinTaiFung Wait Time Scraper」工作流
3. 點「Run workflow」手動執行一次測試

## 檔案說明

### `wait_time_scraper.py`
主程式，負責：
- 抓取鼎泰豐 API 的等候時間數據
- 認證 Google Sheet API
- 將數據寫入 Google Sheet

### `requirements.txt`
Python 套件清單：
- `requests` - HTTP 請求
- `google-api-python-client` - Google Sheets API
- `google-auth-oauthlib` - Google 認證

### `.github/workflows/main.yml`
GitHub Actions 工作流配置：
- 排程：每 10 分鐘執行一次
- 環境：Ubuntu 最新版本
- 步驟：安裝套件 → 執行爬蟲 → 寫入 Google Sheet

## 監控結果

### 查看執行狀態

1. 進入倉庫 → **Actions** 標籤
2. 左邊選「DinTaiFung Wait Time Scraper」
3. 看執行紀錄：
   - ✅ 綠色 = 成功
   - ❌ 紅色 = 失敗

### 查看數據

打開你的 Google Sheet，新增的資料會自動追加到最後一列。

## 常見問題

### 1. 執行失敗了

點擊失敗的執行紀錄 → 看「Run scraper」的輸出訊息，檢查：
- GOOGLE_CREDENTIALS Secret 是否正確設定
- Google Sheet ID 是否正確
- Sheet 是否有分享給服務帳戶

### 2. 數據沒有寫入 Google Sheet

確認：
- 工作表名稱是否為 `工作表1`（如果改了名稱，需要修改程式）
- Sheet 有沒有分享給服務帳戶 email

### 3. 排程沒有自動執行

GitHub Actions 排程可能延遲 5-10 分鐘，這是正常的。

### 4. 想改成其他門市

編輯 `wait_time_scraper.py`，修改 `STORE_ID`：
```python
STORE_ID = '0010'  # 改成其他門市代碼
```

## 門市代碼參考

| 門市 | 代碼 |
|------|------|
| 高雄店 | 0010 |
| 其他門市 | 待補充 |

## 更新備註

### 最近更新

- ✅ 加了 `pytz` 套件（時區設定） - 確保 GitHub Actions 顯示正確的台北時間
- ✅ 改了寫入 Google Sheet 的格式（加單引號） - 防止號碼被當成數字處理
- ✅ 改了 cron 排程（只在營業時間執行） - 節省 GitHub Actions 免費額度

### 營業時間設定

預設排程為每 10 分鐘執行一次，營業時間 11:00-21:00（台北時間）

如需調整，編輯 `.github/workflows/main.yml`：
```yaml
- cron: '*/10 11-21 * * *'  # 修改這行的時間範圍
```

## 改進計畫

- [ ] 監控多間門市
- [ ] 添加異常通知（例如等候時間過長）
- [ ] 數據分析和視覺化
- [ ] 支持動態設定營業時間

## 授權

MIT License

## 相關資源

- [鼎泰豐官網](https://www.dintaifung.tw/)
- [Google Sheets API 文檔](https://developers.google.com/sheets/api)
- [GitHub Actions 文檔](https://docs.github.com/en/actions)
