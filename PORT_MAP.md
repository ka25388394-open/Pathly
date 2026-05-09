# Pathly 端口配置地圖

## 🎯 Pathly 專案端口

| 用途 | 端口 | 說明 |
|------|------|------|
| **後端服務** | 8007 | FastAPI 主服務 |
| **前端頁面** | Live Server | pathly_simple_ui.html |

## 📋 端口使用規則

1. **後端固定 8007**：避免與其他專案衝突
2. **前端使用 Live Server**：通常是 5500 或 5501
3. **API 基礎路徑**：`http://localhost:8007/api/v1`

## 🚫 其他專案端口（避免使用）

| 專案 | 端口 | 狀態 |
|------|------|------|
| 大富翁 | 8010 | 預留 |
| 排班表 | 8020 | 預留 |
| 測試環境 | 8080 | 預留 |

## ✅ 檢查指令

```bash
# 檢查 Pathly 後端
curl http://localhost:8007/health

# 檢查 Pathly API
curl -X POST http://localhost:8007/api/v1/ai/support -H "Content-Type: application/json" -d "{\"message\":\"test\"}"
```