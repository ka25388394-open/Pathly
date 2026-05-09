# Pathly 本地開發地基

## 🎯 端口配置
- **後端**: 8007 (固定)
- **前端**: Live Server (通常 5500)
- **API**: `http://localhost:8007/api/v1`

## 🚀 啟動流程

### 1. 啟動後端
```bash
python start_pathly.py
```

### 2. 啟動前端
- 使用 Live Server 打開 `pathly_simple_ui.html`
- 或直接在瀏覽器打開: `http://localhost:5500/pathly_simple_ui.html`

## 🔍 健康檢查

### 快速檢查
```bash
curl http://localhost:8007/health
# 應該回傳: {"status":"ok","service":"pathly"}
```

### 完整檢查
```bash
# Windows
.\health_check.bat

# 或手動檢查
curl -X POST http://localhost:8007/api/v1/ai/support \
    -H "Content-Type: application/json" \
    -d "{\"message\":\"test\"}"
```

## ⚠️ 故障排除

### 端口被占用
```bash
python cleanup_services.py
```

### 前後端無法連接
1. 檢查後端是否在 8007 運行: `curl http://localhost:8007/health`
2. 檢查前端是否指向正確 API: 搜尋 `localhost:8007`
3. 檢查 CORS: `curl -X OPTIONS http://localhost:8007/api/v1/ai/support -H "Origin: http://localhost:5500"`

## 📁 配置文件

- **`.env`**: 端口和環境配置
- **`PORT_MAP.md`**: 端口分配規則
- **`pathly_simple_ui.html`**: 前端 (API 指向 8007)

## ✅ 驗證清單

啟動後確認：
- [ ] 後端在 8007 回應 health
- [ ] API 在 `/api/v1/ai/support` 正常
- [ ] 前端可以調用後端 API
- [ ] 無 CORS 錯誤

## 🚫 注意事項

- 不要手動指定端口啟動: `uvicorn app.main:app --port xxxx`
- 不要修改核心業務邏輯 (Level 1/2/3, state_engine)
- 端口配置只能在 `.env` 中修改