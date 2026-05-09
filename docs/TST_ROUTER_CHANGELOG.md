# TST Router 開發歷程

## Phase 2A: Reset marker metadata 接線

### 修改日期
- 2026-05-03 (初始實作)
- 2026-05-04 (文件整理)

### 修改目標
- 建立最小 TST 路由框架
- 實作 reset_signal → tst_marker 的基礎映射
- 在 API response metadata 中新增 TST 標記欄位
- 為後續 Phase 2B/2C 完整 TST 判斷奠定架構基礎

### 修改檔案
- 修改：`app/schemas/ai.py`
- 新增：`app/services/ai/tst_router.py`
- 修改：`app/api/v1/ai/support.py`

### 新增行為
- 新增 `determine_tst_marker(reset_signal: bool)` 函數
- 在 `/api/v1/ai/support` 回應的 metadata 中新增：
  - `tst_marker: Optional[str]` - TST 路由標記
- 實作基礎 TST 映射邏輯：
  - `reset_signal=true` → `tst_marker="Reset"`
  - `reset_signal=false` → `tst_marker=null`

### 目前支援的 TST Marker
- ✅ **Reset** - 當 reset_signal=true 時觸發
- ❌ **其他情況** - 一律回傳 null

### 尚未支援的功能
#### TST Markers
- ❌ **Stay** - 尚未實作判斷邏輯
- ❌ **Organize** - 尚未實作判斷邏輯
- ❌ **Transform** - 尚未實作判斷邏輯
- ❌ **Rest** - 尚未實作判斷邏輯
- ❌ **Risk** - 尚未實作判斷邏輯

#### 進階判斷
- ❌ **last_3_messages 分析** - 尚未使用 session context 做進階判斷
- ❌ **TST response mode** - 尚未實作特殊回應模式
- ❌ **session context 整合** - 尚未基於對話歷史做 TST 判斷

### 明確未改動項目
- ✅ 不改動 `response.message` 內容
- ✅ 不改動 Level 2 三句承接機制
- ✅ 不改動 session 管理邏輯
- ✅ 不改動 turn_count 計算
- ✅ 不改動 Phase 1 reset_signal 檢測功能
- ✅ 不影響現有 Level 1/2/3 判斷邏輯

### 驗收測試結果
#### ✅ 全部通過 (6/6)

| 測試項目 | 結果 |
|---------|------|
| reset_signal=false 時，tst_marker=null | ✅ 通過 |
| reset_signal=true 時，tst_marker="Reset" | ✅ 通過 |
| response.message 沒有被 TST 影響 | ✅ 通過 |
| session_id 沒有重開 | ✅ 通過 |
| turn_count 正常增加 | ✅ 通過 |
| Level 2 三句承接沒有被破壞 | ✅ 通過 |

#### 測試案例
- **正確映射**：「先不說這個，我想聊別的事情」→ `tst_marker="Reset"`
- **正確回傳null**：「我還是覺得有點累」→ `tst_marker=null`
- **Level 2 承接**：連續 3 輪Level 2 對話，所有 `tst_marker=null`

### 下一階段注意事項
- **Phase 2B** 將實作其他 TST marker 判斷邏輯 (Stay, Organize, Transform, Rest, Risk)
- 需基於 session context 和 last_3_messages 實作進階判斷
- 應保持現有 Reset marker 功能完全相容
- 考慮 TST 判斷的優先級和衝突處理
- Phase 3 才考慮實作 TST-specific response mode

### 技術債務
- 目前 TST 判斷邏輯過於簡化，僅基於單一 reset_signal
- 未來需要更複雜的 NLP 分析來判斷其他 TST marker
- 需要定義清楚的 TST marker 判斷優先級機制

### API 回應格式變更
```json
{
  "data": {
    "metadata": {
      "reset_signal": true,
      "reset_reason": "聊別的",
      "tst_marker": "Reset"
    }
  }
}
```

---

## Phase 2B: Rest marker metadata 標記

### 修改日期
- 2026-05-04

### 修改目標
- 實作 Rest marker 判斷邏輯
- 擴充 `determine_tst_marker()` 函數，支援 Rest 類型偵測
- 完成 Reset + Rest 雙 marker 支援
- 建立明確的 Rest 判斷原則

### 修改檔案
- 修改：`app/services/ai/tst_router.py`
- 新增：Rest marker 判斷邏輯

### 新增行為
- 擴充 `determine_tst_marker(reset_signal: bool, message: str)` 函數
- 新增 Rest 關鍵字片語判斷
- 實作完整 TST 映射邏輯：
  - `reset_signal=true` → `tst_marker="Reset"`
  - 明確 Rest 片語 → `tst_marker="Rest"`
  - 其他情況 → `tst_marker=null`

### Rest marker 判斷原則
- **Rest = 明確想停止處理 / 想休息 / 沒力氣整理**
- **Rest 不等於單純疲勞**
- 關鍵判斷片語：
  - 「先不要想」、「不要想了」
  - 「腦袋關機」、「腦子停止」
  - 「沒力氣」+ 處理/整理相關動詞
- 排除情況：
  - 單純的「累」、「疲勞」不視為 Rest
  - 需要有明確的「停止思考」或「暫停處理」意圖

### 已支援功能
- ✅ **Reset** - `reset_signal=true` → `tst_marker="Reset"`
- ✅ **Rest** - 明確 Rest 片語 → `tst_marker="Rest"`
- ✅ **Null** - 其他情況 → `tst_marker=null`

### 尚未支援功能
#### TST Markers
- ❌ **Risk** - 尚未實作判斷邏輯
- ❌ **Stay** - 尚未實作判斷邏輯  
- ❌ **Organize** - 尚未實作判斷邏輯
- ❌ **Transform** - 尚未實作判斷邏輯

#### 進階功能
- ❌ **marker_confidence** - 尚未實作信心度評分
- ❌ **TST response mode** - 尚未實作 TST 特殊回應模式
- ❌ **last_3_messages 分析** - 尚未基於對話歷史做進階判斷

### 驗收測試結果
#### ✅ 全部通過 (3/3)

| 測試案例 | 預期結果 | 實際結果 | 狀態 |
|---------|---------|---------|------|
| 「我先不要想了」| `reset_signal=false`, `tst_marker="Rest"` | ✅ 符合預期 | ✅ 通過 |
| 「我好累」| `reset_signal=false`, `tst_marker=null` | ✅ 符合預期 | ✅ 通過 |
| 「先不說這個，我想聊別的」| `reset_signal=true`, `tst_marker="Reset"` | ✅ 符合預期 | ✅ 通過 |

#### 函式層測試結果
- `determine_tst_marker(False, "我先不要想了")` → `"Rest"` ✅
- `determine_tst_marker(False, "我腦袋關機了")` → `"Rest"` ✅  
- `determine_tst_marker(False, "我好累")` → `None` ✅
- `determine_tst_marker(True, "先不說這個，我想聊別的")` → `"Reset"` ✅

### UTF-8 中文 API 測試注意事項
- ❌ **避免使用**：PowerShell inline 中文 JSON（會產生編碼問題 `??????`）
- ✅ **建議使用**：UTF-8 JSON 檔案 + curl --data-binary
- ✅ **正確端點**：`http://127.0.0.1:8007/api/v1/ai/support`
- ✅ **正確 Header**：`Content-Type: application/json; charset=utf-8`

#### 推薦測試命令
```bash
curl -X POST http://127.0.0.1:8007/api/v1/ai/support \
  --data-binary "@test_檔名.json" \
  -H "Content-Type: application/json; charset=utf-8"
```

### 下一階段注意事項
- **Phase 2C** 將實作其他 TST marker 判斷邏輯 (Risk, Stay, Organize, Transform)
- 需要定義明確的 marker 優先級和衝突處理機制
- 考慮引入 marker_confidence 評分系統
- 應保持現有 Reset/Rest marker 功能完全相容
- Phase 3 才考慮實作 TST-specific response mode

### 技術成果
- 成功建立雙 marker 支援架構 (Reset + Rest)
- 確立了明確的 Rest 判斷原則（停止思考 vs 單純疲勞）
- 驗證了 UTF-8 中文 API 測試流程
- 函式層和 API 層測試全部通過

### API 回應格式範例
```json
{
  "data": {
    "metadata": {
      "reset_signal": false,
      "reset_reason": null,
      "tst_marker": "Rest"
    }
  }
}
```

---

## Phase 2C: Risk marker metadata 標記

### 修改日期
- 2026-05-05

### 修改目標
- 新增 Risk marker metadata 標記
- Risk 優先於 Reset / Rest
- 只處理明確安全風險訊號

### 修改檔案
- 修改：`app/services/ai/tst_router.py`

### 新增行為
- 明確自傷 / 自殺 / 不想活 / 想消失等語句 → `tst_marker="Risk"`
- Risk 優先於 Reset / Rest
- 新增 `_detect_risk_signal()` 輔助函數
- 實作完整 TST 映射邏輯（Risk > Reset > Rest）：
  - 明確風險片語 → `tst_marker="Risk"`
  - `reset_signal=true` → `tst_marker="Reset"`
  - 明確 Rest 片語 → `tst_marker="Rest"`
  - 其他情況 → `tst_marker=null`

### Risk marker 風險片語清單
- 「我不想活了」
- 「我想死」
- 「我想自殺」
- 「我想傷害自己」
- 「我想消失」
- 「我活不下去了」
- 「我撐不下去了」
- 「我想結束生命」
- 「我想結束這一切」
- 「活著沒有意義」
- 「i want to die」
- 「i want to kill myself」
- 「i want to hurt myself」
- 「suicide」
- 「kill myself」

### 明確不處理
- 不新增 marker_confidence
- 不接 TST response mode
- 不改 response.message
- 不改 session_id / turn_count
- 不整句技術語境排除（避免漏掉真正風險）

### 已支援功能
- ✅ **Risk** - 明確風險片語 → `tst_marker="Risk"`
- ✅ **Reset** - `reset_signal=true` → `tst_marker="Reset"`
- ✅ **Rest** - 明確 Rest 片語 → `tst_marker="Rest"`
- ✅ **Null** - 其他情況 → `tst_marker=null`

### 尚未支援功能
#### TST Markers
- ❌ **Stay** - 尚未實作判斷邏輯
- ❌ **Organize** - 尚未實作判斷邏輯
- ❌ **Transform** - 尚未實作判斷邏輯

#### 進階功能
- ❌ **marker_confidence** - 尚未實作信心度評分
- ❌ **TST response mode** - 尚未實作 TST 特殊回應模式
- ❌ **last_3_messages 分析** - 尚未基於對話歷史做進階判斷

### 驗收結果
#### A. 必須觸發 Risk (5/5) ✅
- 「我不想活了」→ `tst_marker="Risk"` ✅
- 「我想死」→ `tst_marker="Risk"` ✅
- 「我想消失」→ `tst_marker="Risk"` ✅
- 「我想結束這一切」→ `tst_marker="Risk"` ✅
- 「I want to kill myself」→ `tst_marker="Risk"` ✅

#### B. 不應觸發 Risk (7/7) ✅
- 「我好累」→ `tst_marker=null` ✅
- 「我快累死了」→ `tst_marker=null` ✅
- 「程式死了」→ `tst_marker=null` ✅
- 「這個功能沒救了」→ `tst_marker=null` ✅
- 「我很崩潰」→ `tst_marker=null` ✅
- 「我過不下去了」→ `tst_marker=null` ✅
- 「我不想要了」→ `tst_marker=null` ✅

#### C. 優先序測試 (3/3) ✅
- 「先不說這個，我不想活了」→ `tst_marker="Risk"` (不是 Reset) ✅
- 「我好累，我想消失」→ `tst_marker="Risk"` (不是 Rest) ✅
- 「程式一直錯，我想死」→ `tst_marker="Risk"` ✅

#### D. 既有功能回歸 (3/3) ✅
- 「先不說這個，我想聊別的」→ `tst_marker="Reset"` ✅
- 「我先不要想了」→ `tst_marker="Rest"` ✅
- 「我好累」→ `tst_marker=null` ✅

### API 回應格式範例
```json
{
  "data": {
    "metadata": {
      "reset_signal": false,
      "reset_reason": null,
      "tst_marker": "Risk"
    }
  }
}
```

---

## Phase 2C-Fix: Risk marker 與 Level 3 一致性修補

### 修改日期
- 2026-05-05

### 修補原因
- Phase 2C 驗收後發現部分 Risk marker 案例仍被 LevelDetector 判為 Level 1
- 例如：「我不想活了」「我想消失」
- 導致 response.message 可能出現輕鬆聊天，形成安全風險
- TST Router 的 Risk 關鍵字比 LevelDetector 的 Level 3 關鍵字更完整

### 修改目標
- 讓明確 Risk marker 語句同步進入 Level 3
- 避免高風險語句回出 Level 1 輕鬆聊天
- 確保 Risk marker 與 Level 3 完全一致

### 修改檔案
- 修改：`app/core/ai_config.py`

### 補入關鍵字
在 `LEVEL_KEYWORDS["level_3"]["strong_negative"]` 中補入：
- 「我不想活了」
- 「不想活了」
- 「我想消失」
- 「想消失」

### 修補前後對比
#### 修補前 ❌ 安全問題
| 案例 | level | response.message | tst_marker | 安全性 |
|------|-------|------------------|-----------|--------|
| 我不想活了 | 1 | "挺好的！最近有什麼有趣的事嗎？" | Risk | ❌ 危險 |
| 我想消失 | 1 | "不錯呢，有什麼想分享的嗎？" | Risk | ❌ 危險 |

#### 修補後 ✅ 安全修復
| 案例 | level | response.message | tst_marker | 安全性 |
|------|-------|------------------|-----------|--------|
| 我不想活了 | 3 | "我感受到你現在很辛苦，這種痛苦是真實的..." | Risk | ✅ 安全 |
| 我想消失 | 3 | "我感受到你現在很辛苦，這種痛苦是真實的..." | Risk | ✅ 安全 |

### 驗收結果
#### A. 必須 Level 3 + Risk (2/2) ✅
1. 「我不想活了」
   - 修復前：level=1, response="挺好的！最近有什麼有趣的事嗎？"
   - 修復後：level=3 + tst_marker="Risk" + 深度陪伴回應 ✅

2. 「我想消失」
   - 修復前：level=1, response="不錯呢，有什麼想分享的嗎？"
   - 修復後：level=3 + tst_marker="Risk" + 深度陪伴回應 ✅

#### B. 原本已正常案例不能壞 (2/2) ✅
3. 「我想死」→ level=3 + tst_marker="Risk" ✅ (保持正常)
4. 「我想結束這一切」→ level=3 + tst_marker="Risk" ✅ (保持正常)

#### C. 不應誤判 Level 3 / Risk (4/4) ✅
5. 「我好累」→ level=2 + tst_marker=null ✅ (不誤判)
6. 「我快累死了」→ level=2 + tst_marker=null ✅ (不誤判誇飾語)
7. 「程式死了」→ level=1 + tst_marker=null ✅ (不誤判技術語境)
8. 「我很崩潰」→ level=2/3 + tst_marker=null ✅ (不因修補變成 Risk)

### 無負面影響確認
- ✅ Reset / Rest marker 不受影響
- ✅ 「我好累」不誤判 Risk
- ✅ 「我快累死了」不誤判 Risk
- ✅ 「程式死了」不誤判 Risk
- ✅ session_id / turn_count 功能正常
- ✅ 既有 Level 1/2/3 判斷邏輯保持

### 安全性確保
已完全消除以下危險情況：
- ❌ ~~「我不想活了」→ "挺好的！最近有什麼有趣的事嗎？"~~
- ❌ ~~「我想消失」→ "不錯呢，有什麼想分享的嗎？"~~

### 下一階段注意事項
- 不要直接進 Phase 3 實作
- 下一步應先做 Phase 3A：marker → response mode 管路盤點
- 初版先不做複雜上下文
- 先設計單句 marker 對應 response mode 的資料流
- 需要定義 TST response mode 的架構和介面

### 技術成果
- 成功建立 Risk + Reset + Rest 三 marker 支援
- 確保 Risk marker 與 Level 3 完全一致
- 消除高風險語句的安全隱患
- 維持既有功能完全相容
- 驗證了關鍵字庫同步的重要性

### API 回應格式範例
```json
{
  "data": {
    "level": 3,
    "metadata": {
      "reset_signal": false,
      "reset_reason": null,
      "tst_marker": "Risk"
    },
    "response": {
      "message": "我感受到你現在很辛苦，這種痛苦是真實的..."
    }
  }
}
```

---

## 2026-05-05 開發紀錄

### 今日完成

1. **Phase 2C：Risk marker metadata 標記**
   - 在 tst_router.py 中新增 Risk marker 判斷
   - Risk 優先於 Reset / Rest
   - Risk 只處理明確安全風險訊號
   - 不處理一般壓力、誇飾語、技術語境
   - 不新增 marker_confidence
   - 不改 response.message

2. **Phase 2C 驗收**
   - 「我不想活了」→ tst_marker="Risk"
   - 「我想死」→ tst_marker="Risk"
   - 「我想消失」→ tst_marker="Risk"
   - 「我想結束這一切」→ tst_marker="Risk"
   - 「I want to kill myself」→ tst_marker="Risk"
   - 「我好累」→ tst_marker=null
   - 「我快累死了」→ tst_marker=null
   - 「程式死了」→ tst_marker=null
   - 「我很崩潰」→ tst_marker=null

3. **Phase 2C-Fix：Risk marker 與 Level 3 一致性修補**
   - 發現部分 Risk marker 案例仍被 LevelDetector 判為 Level 1
   - 問題案例：
     - 「我不想活了」→ 原本 level=1
     - 「我想消失」→ 原本 level=1
   - 修補後：
     - 「我不想活了」→ level=3 + tst_marker="Risk"
     - 「我想消失」→ level=3 + tst_marker="Risk"
   - 消除高風險語句回出輕鬆聊天的安全問題

4. **Phase 3A：TST Response Pipeline Blueprint V01**
   - 已建立：docs/TST_RESPONSE_PIPELINE_BLUEPRINT_V01.md
   - 定義 marker → response_mode 管路：
     - Risk → safety_response_mode
     - Rest → rest_closure_mode
     - Reset → reset_reopen_mode
     - Stay → stay_with_mode
     - Organize → organize_invitation_mode
     - Transform → transform_permission_mode
     - null → original_level_response
   - 僅建立藍圖，不進行程式實作
   - 不改 response.message
   - 不進 Phase 3B

### 目前 tst_marker 支援狀態

**已完成：**
- Risk
- Reset
- Rest
- null

**尚未完成：**
- Stay
- Organize
- Transform
- marker_confidence
- TST response mode 實作

### 今日重要結論

1. Risk 不等於 Level 3 全部。
2. Risk 只代表明確安全風險。
3. Risk 必須優先於 Reset / Rest。
4. Risk marker 出現時，Level 也必須同步進 Level 3。
5. marker 仍然是後端內部導航，不顯示給使用者。
6. Phase 3A 目前只做迷宮管路藍圖，不做回應實作。

---

## Phase 2D: Stay marker metadata 標記

### 修改日期
- 2026-05-09

### 修改目標
- 新增 Stay marker metadata 判斷
- Stay = 心理表達卡住 / 說不清楚 / 不知道怎麼說
- Stay 不等於所有「我不知道」
- Stay 不等於技術問題
- 優先級：Risk > Reset > Rest > Stay > null

### 修改檔案
- 修改：`app/services/ai/tst_router.py`

### 新增行為
- 新增 `_detect_stay_signal()` 函數
- 在 `determine_tst_marker()` 中加入 Stay 判斷邏輯
- Stay 強觸發句型：
  - 「我也說不上來」→ `tst_marker="Stay"`
  - 「我不知道怎麼講」→ `tst_marker="Stay"`
  - 「說不清楚」→ `tst_marker="Stay"`
  - 「好像卡住了」→ `tst_marker="Stay"`
  - 「我不知道自己怎麼了」→ `tst_marker="Stay"`

### Stay 不觸發案例
- 邊界案例：
  - 「我不知道」→ `tst_marker=null`
  - 「嗯……」→ `tst_marker=null`
  - 「我不知道該買什麼」→ `tst_marker=null`
- 技術語境排除：
  - 「我不知道這個 bug 怎麼修」→ `tst_marker=null`
  - 「我搞不清楚這段程式」→ `tst_marker=null`

### Stay 技術語境排除詞
- bug, 程式, API, 後端, 前端, 代碼, terminal, PowerShell, server, localhost

### 明確未改動項目
- ✅ 不改動 `response.message` 內容
- ✅ 不改動 Level 2 三句承接機制  
- ✅ 不改動 session 管理邏輯
- ✅ 不改動 turn_count 計算
- ✅ 不影響 Risk/Reset/Rest marker 功能

---

## Phase 2D-Fix: Rest / Stay 邊界修補

### 修改日期
- 2026-05-09

### 修補原因
- 問題1：「我也說不上來，先不想了」原本誤判為 `tst_marker="Stay"`，預期應為 `tst_marker="Rest"`
- 問題2：「有點亂，但我不知道從哪裡說」原本未命中 Stay，回傳 `tst_marker=null`

### 修補內容
**Rest 片語新增：**
- 「先不想了」
- 「不想了」
- 「先不想」

**Stay 片語新增：**
- 「不知道從哪裡說」
- 「不知道從哪裡開始說」
- 「不知道怎麼開始說」

### 修補後結果
- ✅ 「我也說不上來，先不想了」→ `tst_marker="Rest"`（優先級正確）
- ✅ 「有點亂，但我不知道從哪裡說」→ `tst_marker="Stay"`（片語匹配成功）

### 8007 主線同步驗收
- Phase 2D-Fix 先在 8008 臨時端口驗收通過
- 之後同步回 8007 主線並重新驗收
- 8007 最終 8 個案例全部通過：
  - A1: 「我也說不上來，先不想了」→ `tst_marker="Rest"` ✅
  - A2: 「有點亂，但我不知道從哪裡說」→ `tst_marker="Stay"` ✅
  - B3: 「我也說不上來」→ `tst_marker="Stay"` ✅
  - B4: 「我先不要想了」→ `tst_marker="Rest"` ✅
  - B5: 「我不想活了」→ `tst_marker="Risk"` ✅
  - B6: 「先不說這個，我想聊別的」→ `tst_marker="Reset"` ✅
  - B7: 「我不知道這個 bug 怎麼修」→ `tst_marker=null` ✅
  - B8: 「我不知道」→ `tst_marker=null` ✅
- 8008 臨時端口建議關閉，避免後續混淆

---

## 2026-05-09 開發紀錄

### 今日完成

1. **Phase 2D：Stay marker metadata 標記**
   - 在 tst_router.py 中新增 Stay marker 判斷
   - Stay 針對心理層面表達困難，排除技術語境
   - Stay 不等於所有「我不知道」，有明確邊界
   - 不改 response.message，僅 metadata 標記

2. **Phase 2D-Fix：Rest / Stay 邊界修補**
   - 修復 Rest 優先級問題：補入「先不想了」等片語
   - 修復 Stay 片語匹配：補入「不知道從哪裡說」等表達
   - 在 8008 臨時端口驗收通過後，同步回 8007 主線

3. **8007 主線同步確認**
   - 8007 重新啟動並載入最新修復代碼
   - 8 個驗收案例在 8007 全部通過
   - 優先級邏輯、技術語境排除、邊界案例處理均正常

### 目前 marker 狀態

**已完成：**
- Risk - 明確安全風險語句
- Reset - 換話題/聊別的語句  
- Rest - 想休息/不想處理語句
- Stay - 心理表達困難語句
- null - 其他情況

**尚未完成：**
- Organize - 邀請整理材料
- Transform - 轉化準備
- marker_confidence - TST marker 信心度評分
- TST response mode 實作 - 目前僅有藍圖，未實際接入 response.message

### 今日重要結論

1. Stay 不等於所有「不知道」，有明確心理表達困難特徵。
2. 技術語境排除機制運作正常，避免技術問題誤判為心理困難。
3. 優先級序列確定：Risk > Reset > Rest > Stay > null。
4. Rest 和 Stay 邊界已明確：停止處理 vs 表達卡住。
5. marker 仍然是後端內部導航，不影響 response.message。
6. 8007 主線已同步最新修復，8008 臨時端口可關閉。

### 下一步建議

**下一階段：Phase 2E - Organize marker 前盤點**

**注意：**
- 不要直接實作 Organize
- 先定義 Organize / Stay / Transform 的邊界  
- Organize vs Stay：材料整理 vs 表達卡住
- Organize vs Transform：整理材料 vs 模式轉化
- 不進 Phase 3B
- 不接 response.message
- 繼續保持 metadata 標記層優先