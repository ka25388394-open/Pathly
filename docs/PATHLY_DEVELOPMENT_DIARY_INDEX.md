# Pathly 開發日記索引

## 📋 開發歷程總覽

### 🏗️ **2026年4月：架構建構期**
- 建立 Session Memory 系統
- 完成 Level 2 三句順流承接
- 前後端完整打通
- TST 架構設計與規格文件化

### ⚙️ **2026年5月：TST 系統實作期**
- TST 四階段實作方案執行
- Reset / Rest / Risk / Stay marker 實作
- 安全一致性修補
- Response Pipeline 藍圖設計
- Marker 層穩定性驗證

---

## 🗓️ 按時間序列索引

| 日期 | 主要完成事項 | 對應文件 | 對應階段 | 驗收 |
|------|-------------|----------|----------|------|
| **2026-04-25** | Level Detector 技術語境修正 | `LEVEL_DETECTOR_CHANGELOG.md` | 基礎優化 | ✅ |
| **2026-04-28** | Session Memory 系統上線 | `SESSION_MEMORY_CHANGELOG.md` | Session 建構 | ✅ |
| **2026-04-29** | 前端打通 + 規格文件化 | `SESSION_MEMORY_CHANGELOG.md`<br>`LEVEL2_THREE_TURN_FLOW_SPEC.md`<br>`LEVEL2_LOW_COGNITIVE_LOAD_RULES.md` | 架構完善 | ✅ |
| **2026-04-30** | 正式接入 + TST 定位 + 空掉修正 | `SESSION_MEMORY_CHANGELOG.md` | 架構確立 | ✅ |
| **2026-05-01** | TST 實作方案制定 | `TST_MINIMAL_IMPLEMENTATION_PLAN_V01.md` | Phase 規劃 | ✅ |
| **2026-05-03** | Phase 1: Reset Signal 實作 | `RESET_SIGNAL_DETECTOR_CHANGELOG.md` | Phase 1 | ✅ |
| **2026-05-03** | Phase 2A: Reset marker | `TST_ROUTER_CHANGELOG.md` | Phase 2A | ✅ |
| **2026-05-04** | Phase 2B: Rest marker | `TST_ROUTER_CHANGELOG.md` | Phase 2B | ✅ |
| **2026-05-05** | Phase 2C: Risk marker | `TST_ROUTER_CHANGELOG.md` | Phase 2C | ✅ |
| **2026-05-05** | Phase 2C-Fix: 安全修補 | `TST_ROUTER_CHANGELOG.md` | Phase 2C-Fix | ✅ |
| **2026-05-05** | Phase 3A: Response Pipeline 藍圖 | `TST_RESPONSE_PIPELINE_BLUEPRINT_V01.md` | Phase 3A | ✅ |
| **2026-05-09** | Phase 2D: Stay marker + 邊界修補 + 穩定性驗收 | `TST_ROUTER_CHANGELOG.md` | Phase 2D + Fix | ✅ |

---

## 📂 按功能模組索引

### 🔍 **Level Detector**
- **文件**：`LEVEL_DETECTOR_CHANGELOG.md`
- **內容**：技術語境誤判修正、Level 3 判斷邏輯優化
- **關鍵成果**：技術挫折不再誤判為心理危機

### 💾 **Session Memory**
- **文件**：`SESSION_MEMORY_CHANGELOG.md`
- **內容**：Session 系統建立、多輪對話記憶
- **關鍵成果**：支援 Level 2 三句順流承接

### 🔄 **Level 2 三句承接**
- **文件**：`SESSION_MEMORY_CHANGELOG.md`、`LEVEL2_THREE_TURN_FLOW_SPEC.md`、`LEVEL2_LOW_COGNITIVE_LOAD_RULES.md`
- **內容**：三句承接流程、低認知負荷工程規則
- **關鍵成果**：溫和漸進的使用者狀態承接

### 🔄 **Reset Signal**
- **文件**：`RESET_SIGNAL_DETECTOR_CHANGELOG.md`
- **內容**：換話題訊號檢測
- **關鍵成果**：「換個話題」「聊別的」檢測功能

### 🧭 **TST Router**
- **文件**：`TST_ROUTER_CHANGELOG.md`
- **內容**：Risk/Reset/Rest marker 判斷系統
- **關鍵成果**：三種 TST marker + 優先級設計

### 🗺️ **TST Response Pipeline**
- **文件**：`TST_RESPONSE_PIPELINE_BLUEPRINT_V01.md`
- **內容**：marker → response_mode 管路藍圖
- **關鍵成果**：六大 response mode 設計架構

### 🌏 **UTF-8 中文測試流程**
- **文件**：`TST_ROUTER_CHANGELOG.md` (Phase 2B 章節)
- **內容**：UTF-8 JSON 檔案 + curl --data-binary 測試方式
- **關鍵成果**：解決 PowerShell inline 中文編碼問題

---

## 🚀 按開發階段索引

### **Phase 0：基線確認**
- **目標**：確認現有功能正常運作
- **狀態**：✅ 已完成
- **文件**：各 changelog 測試部分

### **Phase 1：reset_signal detector**
- **目標**：建立換話題訊號檢測
- **狀態**：✅ 已完成
- **文件**：`RESET_SIGNAL_DETECTOR_CHANGELOG.md`

### **Phase 2A：Reset marker**
- **目標**：reset_signal → tst_marker="Reset"
- **狀態**：✅ 已完成
- **文件**：`TST_ROUTER_CHANGELOG.md`

### **Phase 2B：Rest marker**
- **目標**：明確休息意圖 → tst_marker="Rest"
- **狀態**：✅ 已完成
- **文件**：`TST_ROUTER_CHANGELOG.md`

### **Phase 2C：Risk marker**
- **目標**：明確安全風險 → tst_marker="Risk"
- **狀態**：✅ 已完成
- **文件**：`TST_ROUTER_CHANGELOG.md`

### **Phase 2C-Fix：Risk 與 Level 3 一致性修補**
- **目標**：確保 Risk marker 案例同步進入 Level 3
- **狀態**：✅ 已完成
- **文件**：`TST_ROUTER_CHANGELOG.md`

### **Phase 3A：Response Pipeline 藍圖**
- **目標**：設計 marker → response_mode 管路
- **狀態**：✅ 已完成（僅藍圖）
- **文件**：`TST_RESPONSE_PIPELINE_BLUEPRINT_V01.md`

---

## 🎯 當前狀態

### ✅ **已完成 TST Marker**
- **Risk** - 明確自傷/自殺/不想活/想消失語句
- **Reset** - 換話題/聊別的語句  
- **Rest** - 想休息/不想處理語句
- **null** - 其他情況

### ✅ **已完成架構**
- **TST Response Pipeline Blueprint V01** - 六大 response mode 藍圖
- **優先級系統** - Risk > Reset > Rest > null
- **安全一致性** - Risk marker 與 Level 3 完全一致

### ❌ **尚未完成 TST Marker**
- **Stay** - 陪使用者停在原地
- **Organize** - 邀請整理材料
- **Transform** - 轉化準備

### ❌ **尚未完成功能**
- **marker_confidence** - TST marker 信心度評分
- **TST response mode 實作** - 目前僅有藍圖，未實際接入 response.message
- **last_3_messages 分析** - 上下文判斷
- **session context 整合** - 基於對話歷史的 TST 判斷

---

## 🔮 下一步建議

### 🎯 **Phase 2D：Stay marker 前盤點**
- ⚠️ **不要直接實作 Stay**
- ✅ **先定義 Stay / Rest / Organize 的邊界**
- ✅ **保持 metadata 標記層優先**
- ✅ **不進 Phase 3B**
- ✅ **不接 response.message**

### 📋 **邊界定義重點**
- Stay vs Rest：停留承接 vs 收束休息
- Stay vs Organize：原地陪伴 vs 邀請整理
- Organize vs Transform：材料整理 vs 模式轉化

---

## 🔍 快速查找區

### 📖 **想查 Level 2 三句承接**
- **主文件**：`SESSION_MEMORY_CHANGELOG.md`
- **規格文件**：`LEVEL2_THREE_TURN_FLOW_SPEC.md`
- **工程規則**：`LEVEL2_LOW_COGNITIVE_LOAD_RULES.md`
- **搜索關鍵字**：三句承接、turn_count、continuity guard

### 💾 **想查 session memory**
- **主文件**：`SESSION_MEMORY_CHANGELOG.md`
- **搜索關鍵字**：session_store.py、session_id、turn_count

### 🧭 **想查 Reset / Rest / Risk marker**
- **主文件**：`TST_ROUTER_CHANGELOG.md`
- **搜索關鍵字**：tst_marker、determine_tst_marker、Phase 2A/2B/2C

### 🗺️ **想查迷宮管路**
- **主文件**：`TST_RESPONSE_PIPELINE_BLUEPRINT_V01.md`
- **搜索關鍵字**：response_mode、safety_response_mode、rest_closure_mode

### 🌏 **想查 UTF-8 中文測試**
- **主文件**：`TST_ROUTER_CHANGELOG.md` (Phase 2B 章節)
- **搜索關鍵字**：UTF-8、curl --data-binary、PowerShell inline

### ⚠️ **想查安全問題修復**
- **主文件**：`TST_ROUTER_CHANGELOG.md` (Phase 2C-Fix 章節)
- **搜索關鍵字**：安全一致性、「我不想活了」、Level 3 修補

### 🚀 **想查實作方案**
- **主文件**：`TST_MINIMAL_IMPLEMENTATION_PLAN_V01.md`
- **搜索關鍵字**：Phase 0-4、漸進式實作、最小可驗證增量

---

## 2026-05-09 開發紀錄

### 今日完成

1. **Phase 2D：Stay marker 前盤點**
   - 定義 Stay marker 產品邊界
   - Stay = 心理表達卡住 / 說不清楚 / 不知道怎麼說
   - Stay 不等於所有「我不知道」
   - Stay 不等於技術問題
   - Stay 不等於 Rest / Reset / Risk

2. **Phase 2D：Stay marker metadata 實作**
   - 只修改 app/services/ai/tst_router.py
   - 新增 _detect_stay_signal()
   - 在 determine_tst_marker() 中加入 Stay 判斷
   - 優先順序確認：Risk > Reset > Rest > Stay > null

3. **Phase 2D-Fix：Rest / Stay 邊界修補**
   - 修正「我也說不上來，先不想了」應判 Rest，不應判 Stay
   - 修正「有點亂，但我不知道從哪裡說」應判 Stay
   - Rest 片語補充：先不想了、不想了、先不想
   - Stay 片語補充：不知道從哪裡說、不知道從哪裡開始說、不知道怎麼開始說

4. **8007 主線同步驗收**
   - Phase 2D-Fix 曾先在 8008 臨時端口驗收
   - 已同步回 8007 主線
   - 8007 最終驗收通過
   - 8008 臨時端口已關閉，避免後續混淆

5. **TST_ROUTER_CHANGELOG.md 已更新**
   - 已記錄 Phase 2D
   - 已記錄 Phase 2D-Fix
   - 已記錄 8007 主線同步結果

6. **Phase 2D marker 層穩定性測試完成**
   - Risk / Reset / Rest / Stay / null 五種 marker 穩定性確認
   - 優先順序確認：Risk > Reset > Rest > Stay > null
   - Stay 技術語境排除確認
   - Rest / Stay 邊界修補後驗收通過
   - Level 2 三句承接回歸測試通過
   - response.message 未被 TST marker 影響
   - session_id / turn_count 正常

### 目前 marker 狀態

**已完成：**
- Risk
- Reset
- Rest
- Stay
- null

**尚未完成：**
- Organize
- Transform
- marker_confidence
- TST response mode 實作

### 今日重要結論

1. Stay 是心理表達卡住，不是所有「我不知道」
2. 技術語境的「不知道」不應判 Stay
3. Rest 優先於 Stay
4. Risk / Reset / Rest / Stay 優先序已確認：Risk > Reset > Rest > Stay > null
5. 目前仍只在 metadata 層標記，不改 response.message

### 觀察項

- 「先不說這個，我不想活了」最終 tst_marker 正確為 Risk
- reset_signal 在該複合句中為 false，可記錄為後續 reset_detector 優化觀察，不影響目前安全判斷

### 下一步建議

**下一次從：Phase 2E - Organize marker 前盤點**

**注意：**
- 不要直接實作 Organize
- 先定義 Organize / Stay / Transform 的邊界
- 不進 Phase 3B
- 不接 response.message
- 繼續保持 metadata 標記層優先
- 可在 Phase 2E 前先做一輪中型穩定性測試

---

## 📝 文件版本說明

- **創建日期**：2026-05-05
- **最後更新**：2026-05-09  
- **版本**：v1.1
- **維護者**：Pathly 開發團隊

**注意**：本索引文件會隨著專案進展持續更新。如發現索引與實際文件不符，請以各專項 changelog 為準。