# RUNBOOK - core-pathly-main

## 專案資訊

- **專案名稱**: core-pathly-main
- **技術棧**: FastAPI + uvicorn
- **正式 Port**: 8007（生產環境）
- **備援 Port**: 8008（本機 debug 專用，非正式）
- **環境**: development

---

## 快速啟動

### 1. 啟動指令

```bash
# 標準啟動方式（推薦）
python start_pathly.py

# 備用腳本方式
./start_pathly.bat    # Windows
./start_pathly.sh     # Linux/Mac
```

### 🔄 **乾淨重啟 SOP（重要）**

**Windows 本機多重實例問題處理：**

1. **啟動前必檢**：
   ```bash
   netstat -an | findstr :8007
   ```

2. **如果看到多個 LISTENING**：
   ```bash
   # 找出 PID
   netstat -ano | findstr :8007
   
   # 手動關閉對應 PID
   taskkill /PID <PID號碼> /F
   ```

3. **確認乾淨後啟動**：
   ```bash
   python start_pathly.py
   ```

**重要規則：**
- **正式 Port**: 8007（不可隨便改）
- **Host**: 使用 `127.0.0.1`（本機開發），非 `0.0.0.0`
- **8008**: 僅作 debug 備援，非正式 port
- **啟動指令**: `python -m uvicorn app.main:app --host 127.0.0.1 --port 8007 --reload`
- **只清理 8007**：不要亂殺 5000/8006/其他專案端口

### 2. 確認啟動成功

看到以下輸出表示啟動成功：
```
PROJECT_NAME: core-pathly-main
ENV: development
BACKEND_PORT: 8007
FRONTEND_PORT: 5500
MOCK_AI: false
```

### 3. 測試連線

```bash
# 瀏覽器訪問
http://127.0.0.1:8007/health

# 或使用 curl
curl http://127.0.0.1:8007/health
```

預期回應：
```json
{"status": "ok", "service": "pathly"}
```

---

## 啟動前檢查

### ✅ 必要檢查

1. **檢查 Port 是否可用**
   ```bash
   python check_port.py
   ```

2. **確認環境設定**
   ```bash
   # 檢查 .env 文件存在
   ls .env
   
   # 確認必要變數
   grep -E "PROJECT_NAME|PORT|ENV" .env
   ```

3. **檢查依賴**
   ```bash
   pip list | grep -E "fastapi|uvicorn|pydantic"
   ```

---

## 常見錯誤

### ❌ Port 8007 被佔用

**錯誤訊息**: `OSError: [Errno 48] Address already in use`

**解決方法**:
```bash
# 1. 檢查誰在用 port 8007
netstat -an | grep 8007

# 2. 停止佔用的服務 (Ctrl+C)

# 3. 或使用清理腳本
python cleanup_services.py
```

### ❌ 找不到模組

**錯誤訊息**: `ModuleNotFoundError: No module named 'app'`

**解決方法**:
```bash
# 確保在專案根目錄
pwd
ls app/

# 如果不在根目錄，切換到正確位置
cd C:\Users\USER\Desktop\pathly
```

### ❌ .env 文件問題

**錯誤訊息**: 設定值不正確

**解決方法**:
```bash
# 檢查 .env 格式
cat .env

# 確保沒有空格
PROJECT_NAME=core-pathly-main  # ✅ 正確
PROJECT_NAME = core-pathly-main  # ❌ 錯誤
```

### ❌ 虛擬環境問題

**錯誤訊息**: 找不到 fastapi 或其他依賴

**解決方法**:
```bash
# 啟動虛擬環境（如果有）
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安裝依賴
pip install -r requirements.txt
```

---

## 停止服務

```bash
# 在啟動終端機中按 Ctrl+C
# 或關閉終端機視窗
```

---

## 開發提醒

- 啟動時會自動印出專案資訊，確保是正確的專案
- 使用 `--reload` 開發模式，檔案變更會自動重啟
- PORT 8007 專屬於 core-pathly-main，避免與其他專案衝突
- 如需修改設定，編輯 `.env` 文件即可

---

**最後更新**: 2026-04-20