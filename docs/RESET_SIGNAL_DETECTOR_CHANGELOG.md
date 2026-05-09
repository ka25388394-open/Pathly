# Reset Signal Detector 開發歷程

## Phase 1: 基礎檢測器實作

### 修改日期
- 2026-05-03

### 修改目標
- 在 AI Support API 中新增換話題訊號檢測功能
- 將檢測結果加入 response metadata，不影響現有邏輯
- 為後續 Phase 2 TST 路由奠定基礎

### 修改檔案
- 新增：`app/services/ai/reset_detector.py`
- 修改：`app/api/v1/ai/support.py`
- 修改：`app/schemas/ai.py` (已存在 reset_signal/reset_reason 欄位)

### 新增行為
- 新增 `detect_reset_signal(message: str)` 函數
- 檢測關鍵詞：「換個話題」、「換話題」、「聊別的」、「不說了」、「算了」、「另一個問題」、「問別的」、「別的事」、「重新開始」、「換個方向」
- 在 `/api/v1/ai/support` 回應的 metadata 中加入：
  - `reset_signal: bool` - 是否偵測到換話題訊號
  - `reset_reason: Optional[str]` - 觸發的關鍵詞

### 明確未改動項目
- ✅ 不改動 `response.message` 內容
- ✅ 不改動 session 管理邏輯
- ✅ 不改動 turn_count 計算
- ✅ 不改動 Level 2 三句承接機制
- ✅ 不新增 TST marker 或 routing 功能
- ✅ 不影響現有 Level 1/2/3 判斷邏輯

### 驗收測試結果
#### ✅ 全部通過 (5/5)

| 測試項目 | 結果 |
|---------|------|
| metadata 包含 reset_signal/reset_reason | ✅ 通過 |
| 一般延續句不誤判 | ✅ 通過 |
| 換話題句正確觸發 | ✅ 通過 |
| Level 2 三句承接未破壞 | ✅ 通過 |
| 功能範圍控制 | ✅ 通過 |

#### 測試案例
- **正確檢測**：「算了，換個話題吧」→ `reset_signal=true`
- **不誤判**：「我今天心情不太好」→ `reset_signal=false`
- **Level 2 承接**：同 session 連續 3 輪正確維持 Level 2

### 下一階段注意事項
- Phase 2 將實作 TST (Topic Switch Transition) 路由功能
- 需基於 Phase 1 的 reset_signal 檢測結果進行流程分支
- 應保持現有 API 介面相容性
- 注意 session 狀態在 topic switch 時的處理邏輯

### 技術債務
- 目前僅支援中文關鍵詞檢測，未來可考慮多語言支援
- 關鍵詞匹配為簡單字串包含，可考慮更精確的 NLP 方法