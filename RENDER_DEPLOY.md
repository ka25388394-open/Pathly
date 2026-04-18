# 🚀 Render快速部署指南

## 步驟1：登入Render
前往：https://render.com
用你的GitHub帳號登入

## 步驟2：創建新服務 
1. 點擊 "New +" 
2. 選擇 "Web Service"
3. 連接GitHub倉庫：`ka25388394-open/Pathly`
4. 選擇分支：`main-clean` (重要！)

## 步驟3：部署設定
- **Name**: pathly (或你喜歡的名稱)
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Plan**: Free (每月750小時免費)

## 步驟4：環境變數設定
在 "Environment Variables" 區域添加：

```
APP_ENV=production
APP_DEBUG=false
DATABASE_URL=(Render會自動提供PostgreSQL)
MOCK_AI=true
```

如果你有Gemini API密鑰，也可以添加：
```
GEMINI_API_KEY=你的密鑰
MOCK_AI=false
```

## 步驟5：部署！
點擊 "Create Web Service"

部署大約需要2-3分鐘，完成後你會得到：
🌐 `https://pathly-xxx.onrender.com`

## 🎁 然後就可以分享給朋友了！
- 完整的pathly功能
- 全球可訪問
- 自動SSL證書
- 專業級託管