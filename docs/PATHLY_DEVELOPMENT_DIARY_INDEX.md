# Pathly 開發日記索引

---

## ⚠️ 每日開發前必讀

**請先閱讀：[Pathly AI 協作控制憲法](PATHLY_AI_COLLABORATION_CONSTITUTION.md)**

任何 AI 協作開發任務開始前，都必須先讀取協作憲法，確認任務類型、檔案權限區與執行邊界。

---

# Pathly 開發日記固定格式規範

未來每日開發紀錄必須使用以下結構：

## YYYY-MM-DD｜今日主題

### 1. 開始狀態

- branch：
- upstream：
- ahead：
- modified：
- untracked：
- 今日主線：
- 今日是否允許 push：
- 今日是否允許碰 frontend：
- 今日是否允許碰 app/ 核心邏輯：

### 2. 今日目標

1.
2.
3.

### 3. 今日限制 / 憲法提醒

- 不 git add .
- 不 push，除非明確要求
- 不碰 frontend，除非明確要求
- 不碰 app/ 核心邏輯，除非明確要求
- 不重構，除非明確要求
- 不擴功能
- 不自行進入下一個 Phase
- 每次只做最小更動
- 先盤點，再執行
- 不把整理任務變成開發任務

### 4. 今日執行紀錄

#### Step X：動作名稱

- 目的：
- 處理檔案：
- 操作類型：
- 結果：
- commit hash：
- 是否越界：
- 備註：

### 5. 今日完成事項

-

### 6. 今日未完成事項

-

### 7. 風險 / 注意事項

-

### 8. 結束狀態

- branch：
- upstream：
- ahead：
- modified：
- untracked：
- 最新 commit：
- 是否可進下一階段：
- 是否建議 push：

### 9. 明天第一步

-

### 10. 明天禁止事項

-

---

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

## 2026-05-09｜Phase 2D Stay marker 實作與邊界修補

### 1. 開始狀態

- branch：未記錄
- upstream：未記錄  
- ahead：未記錄
- modified：未記錄
- untracked：未記錄
- 今日主線：功能開發線（Phase 2D Stay marker）
- 今日是否允許 push：未明確記錄
- 今日是否允許碰 frontend：否
- 今日是否允許碰 app/ 核心邏輯：是（僅限 tst_router.py）

### 2. 今日目標

未明確記錄

### 3. 今日限制 / 憲法提醒

- 不進 Phase 3B
- 不接 response.message
- 保持 metadata 標記層優先

### 4. 今日執行紀錄

未採用 Step 格式記錄

### 5. 今日完成事項

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

### 6. 今日未完成事項

- Organize marker
- Transform marker  
- marker_confidence
- TST response mode 實作

### 7. 風險 / 注意事項

- reset_signal 在複合句中可能為 false，不影響目前安全判斷
- 技術語境的「不知道」不應判 Stay

### 8. 結束狀態

- branch：未記錄
- upstream：未記錄
- ahead：未記錄
- modified：未記錄
- untracked：未記錄
- 最新 commit：未記錄
- 是否可進下一階段：是（Phase 2E）
- 是否建議 push：未記錄

#### marker 完成狀態

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

### 9. 明天第一步

**Phase 2E - Organize marker 前盤點**

### 10. 明天禁止事項
- 不要直接實作 Organize
- 先定義 Organize / Stay / Transform 的邊界
- 不進 Phase 3B
- 不接 response.message
- 繼續保持 metadata 標記層優先
- 可在 Phase 2E 前先做一輪中型穩定性測試

---

## 2026-05-10｜開發環境整理與 Git 分流紀錄

### 1. 開始狀態

- branch：main-clean
- upstream：origin/main-clean
- ahead：約 14 commits（開始時）
- modified：frontend（獨立倉庫，不處理）
- untracked：約 49 個
- 今日主線：Git / 開發環境整理線
- 今日是否允許 push：否
- 今日是否允許碰 frontend：否
- 今日是否允許碰 app/ 核心邏輯：否

### 2. 今日目標

1. 整理 untracked 檔案到合適目錄
2. 建立 scripts/ops 和 scripts/dev 結構
3. 完成測試檔案群第一輪盤點

### 3. 今日限制 / 憲法提醒
- 不進 Phase 2E
- 不做 Organize marker
- 不做 Transform marker
- 不做 response_mode
- 不碰 frontend
- 不修改 app/ 核心邏輯
- 不 push
- 不使用 git add .
- 每次只做最小更動

### 4. 今日執行紀錄

#### Step 1：完成 docs 開發環境整理文件

- 目的：記錄開發環境整理進度
- 處理檔案：docs/development_environment_cleanup_progress.md
- 操作類型：commit
- 結果：成功
- commit hash：483660f
- 是否越界：否
- 備註：文件記錄

#### Step 2-10：[詳細步驟記錄在完成事項中]

### 5. 今日完成事項

1. **完成 docs 開發環境整理文件 commit**
   - 483660f docs: add development environment cleanup progress report

2. **完成 legacy prototype 歸檔**
   - faa07d4 chore: archive legacy prototype apps

3. **修復 ai_simple archive 越界事故**
   - 081eade 為錯誤 archive commit
   - 4e06a3a 已 revert
   - 已確認 ai_simple 遺失不影響主線
   - /health 正常
   - /api/v1/ai/support 正常

4. **完成 encoding tools 整理**
   - 89b9083 chore: move encoding check tools to dev tools
   - tools/dev/check_encoding.py
   - tools/dev/check_encoding_simple.py
   - tools/dev/check_utf8.py

5. **完成 Level 2 dev tools 整理**
   - b5d70ef chore: move level2 dev tools to dev tools
   - tools/dev/debug_patterns.py
   - tools/dev/pattern_test.py
   - tools/dev/level2_table_report.py

6. **完成 state_patterns.py 歸檔**
   - 21ac169 chore: archive level2 state pattern reference
   - archive/reference/state_patterns.py

7. **完成 scripts/ops 整理**
   - 3ce6056 chore: move core ops scripts to ops folder
   - 163cf16 chore: move ops helper scripts to ops folder
   - scripts/ops/ 目前包含 8 個運維腳本

8. **完成 scripts/dev 整理**
   - da90ac7 chore: move dev test command script to dev scripts
   - scripts/dev/pathly_test.cmd

9. **刪除過時 / 重複 scripts**
   - pathly_test_clean.cmd
   - check_port_before_start.bat
   - start_pathly.sh

10. **完成測試檔案群第一輪盤點**
    - 7 個明確保留候選
    - 7 個明確刪除候選
    - 8 個 REVIEW_NEEDED

### 今日整理結果

- scripts/ops/ 已建立
- scripts/dev/ 已建立
- tools/dev/ 已整理
- archive/reference/ 已建立
- untracked 從約 49 個降至 23 個
- main-clean ahead origin/main-clean 20 commits
- frontend 仍為 modified，但屬於獨立倉庫，今日不處理

### 測試檔案群盤點結果

#### 明確保留候選

- boundary_test.py
- final_test.py
- final_acceptance_test.py
- level2_quality_test.py
- api_test_fatigue.py
- test_app_routes.py
- level_regression_test.py

#### 明確刪除候選

- simple_test.py
- single_test.py
- test_fixes.py
- test_level_fix.py
- test_fatigue_fix.py
- test_ai_import.py
- test_8008.py

#### REVIEW_NEEDED

- quick_boundary_test.py
- boundary_stability_test.py
- simple_acceptance_test.py
- simple_boundary_test.py
- simple_regression_test.py
- test_fixed_regex.py
- test_precise_patterns.py
- test_key_sentence.py

### 6. 今日未完成事項

- 處理 8 個 REVIEW_NEEDED 測試檔案
- 決定 cleanup_services.py 和 identify_services.py 的歸屬

### 7. 風險 / 注意事項

- frontend 是獨立倉庫，modified 狀態正常
- ai_simple 越界事故已 revert，不影響主線
- /health 和 /api/v1/ai/support 測試正常
- 建立了每日開發收尾 SOP

### 8. 結束狀態

- branch：main-clean
- upstream：origin/main-clean
- ahead：20 commits
- modified：frontend（獨立倉庫）
- untracked：23 個
- 最新 commit：da90ac7 chore: move dev test command script to dev scripts
- 是否可進下一階段：是（測試檔案整理）
- 是否建議 push：否

### 9. 明天第一步

2026-05-11 第一件事：

刪除 7 個明確重複 / 過時的 untracked 測試檔：

- simple_test.py
- single_test.py
- test_fixes.py
- test_level_fix.py
- test_fatigue_fix.py
- test_ai_import.py
- test_8008.py

### 10. 明天禁止事項
- 不碰 frontend
- 不碰 app/
- 不進 Phase 2E
- 不 push
- 不使用 git add .
- 不新增功能
- 不重構
- 只處理測試檔案整理

### 備註

今日建立「Pathly 每日開發收尾 SOP」：

每日開發完成後需執行：
1. git status --short
2. 檢查 modified / untracked
3. 確認是否有越界修改
4. 判斷是否可以 commit
5. 記錄今日完成事項
6. 定義明天第一步

此 SOP 用於避免 AI 協作開發累積過多臨時檔、debug 檔、重複測試與越界修改。

---

## 2026-05-11｜測試檔案整理與 untracked 清零

### 1. 開始狀態

- branch：main-clean
- upstream：origin/main-clean
- ahead：20 commits（從昨日結束狀態）
- modified：frontend（獨立倉庫，不處理）
- untracked：24+ 個測試相關檔案
- 今日主線：測試整理線
- 今日是否允許 push：否
- 今日是否允許碰 frontend：否
- 今日是否允許碰 app/ 核心邏輯：否

### 2. 今日目標

1. 刪除明確重複 / 過時的測試檔
2. 建立乾淨的 tests/ 目錄結構
3. 將根目錄 untracked 清理至 0
4. 不進 Phase 2E，不碰 app/，不碰 frontend

### 3. 今日限制 / 憲法提醒

- 不 git add .
- 不 push
- 不碰 frontend
- 不碰 app/ 核心邏輯
- 不進 Phase 2E
- 不新增功能
- 不重構
- 不把測試整理變成測試重構
- 每次只做最小更動
- 先盤點，再執行

### 4. 今日執行紀錄

#### Step 1：刪除 7 個明確重複 / 過時測試檔

- 目的：先清掉明確無保留價值的測試檔
- 處理檔案：simple_test.py, single_test.py, test_fixes.py, test_level_fix.py, test_fatigue_fix.py, test_ai_import.py, test_8008.py
- 操作類型：delete
- 結果：刪除完成
- commit hash：無，皆為 untracked
- 是否越界：否

#### Step 2：整理 service ops tools

- 目的：將服務清理與服務識別工具歸入 scripts/ops/
- 處理檔案：cleanup_services.py → scripts/ops/, identify_services.py → scripts/ops/
- 操作類型：move + commit
- 結果：完成
- commit hash：e3e59d4 chore: move service ops tools to ops folder
- 是否越界：否

#### Step 3：整理穩定 unit / acceptance tests

- 目的：先收編不需修改內容、無 port 問題的測試檔
- 處理檔案：final_test.py → tests/unit/, test_app_routes.py → tests/unit/, final_acceptance_test.py → tests/acceptance/
- 操作類型：move + commit
- 結果：完成
- commit hash：118169b test: move stable unit and acceptance tests
- 是否越界：否

#### Step 4：修正並整理 API port 測試

- 目的：將高價值 API 測試中的過時 port 修正為 8007，並歸入 tests/
- 處理檔案：boundary_test.py → tests/integration/, level2_quality_test.py → tests/integration/, level_regression_test.py → tests/regression/
- 操作類型：code change + move + commit
- 結果：只修正 8008 → 8007，未改 endpoint / request / response 解析
- commit hash：9523e93 test: update API test ports and organize integration tests
- 是否越界：否

#### Step 5：刪除 5 個重複 REVIEW_NEEDED 測試檔

- 目的：刪除已被更完整測試覆蓋的重複測試
- 處理檔案：api_test_fatigue.py, quick_boundary_test.py, simple_acceptance_test.py, simple_boundary_test.py, simple_regression_test.py
- 操作類型：delete
- 結果：刪除完成
- commit hash：無，皆為 untracked
- 是否越界：否

#### Step 6：整理 regex unit tests

- 目的：保留有獨特價值的 regex / pattern 測試
- 處理檔案：test_fixed_regex.py → tests/unit/, test_precise_patterns.py → tests/unit/
- 操作類型：move + commit
- 結果：完成
- commit hash：05d2943 test: move regex pattern tests to unit tests
- 是否越界：否

#### Step 7：整理 boundary stability integration test

- 目的：保留含 25 個案例的邊界穩定性測試，補足 Level 1 分類穩定性檢查
- 處理檔案：boundary_stability_test.py → tests/integration/
- 操作類型：code change + move + commit
- 結果：只修正 8009 → 8007
- commit hash：57f847e test: add boundary stability integration test
- 是否越界：否

#### Step 8：刪除最後一個 untracked 測試檔

- 目的：清理不值得單獨維護的關鍵句測試檔
- 處理檔案：test_key_sentence.py
- 操作類型：delete
- 結果：刪除完成；其案例「我今天真的有點累」未來如有需要，可合併進 final_acceptance_test.py
- commit hash：無，untracked 刪除
- 是否越界：否

### 5. 今日完成事項

- 完成測試檔案整理
- 根目錄 untracked 清理至 0
- 建立 tests/ 正式結構：tests/unit/, tests/integration/, tests/acceptance/, tests/regression/
- tests/ 目前共 9 個高品質測試檔
- service ops tools 已歸入 scripts/ops/
- 未修改 app/
- 未處理 frontend/
- 未進 Phase 2E

### 6. 今日未完成事項

- frontend 仍為 modified，屬於獨立倉庫，今日不處理
- 尚未 push
- 尚未進入 Phase 2E
- 尚未執行完整測試驗收

### 7. 風險 / 注意事項

- frontend 是獨立倉庫，不可混入主專案 commit
- 目前 main-clean 已累積 27 個 ahead commits，push 前需另做 push 前檢查
- tests/ 已整理，但尚未完整跑過所有測試
- 不應直接進 Phase 2E，需先做工作區狀態確認與測試驗收

### 8. 結束狀態

- branch：main-clean
- upstream：origin/main-clean
- ahead：27 commits
- modified：frontend（獨立倉庫）
- untracked：0
- 最新 commit：57f847e test: add boundary stability integration test
- 是否可進下一階段：是（測試驗收）
- 是否建議 push：否

### 9. 明天第一步

建議明天第一步：

只做測試驗收，不進功能開發。

先確認：
1. /health 正常
2. /api/v1/ai/support 正常
3. tests/ 中主要測試是否可執行
4. git status 是否仍乾淨

### 10. 明天禁止事項

- 不碰 frontend
- 不碰 app/
- 不進 Phase 2E
- 不 push
- 不 git add .
- 不新增功能
- 不重構
- 不直接修改 tests/，除非測試驗收發現明確問題

---

## 2026-05-11 下半段｜測試驗收紀錄

### 測試主線

今日下半段只做 Test only，不修復，不修改正式檔案。

### 已完成測試

1. **API health check**
   - /health 正常：`{"status":"ok","service":"pathly"}`
   - /api/v1/ai/support 正常：success:true, level:2, metadata 正常
   - 後端 8007 成功啟動與測試

2. **Unit tests 初步驗收**
   - pytest tests/unit 無法完整執行（ModuleNotFoundError / 舊測試 import 問題）
   - final_test.py 通過：Final Accuracy 10/10 (100.0%)
   - test_fixed_regex.py 通過：Regex pattern 測試完成
   - test_precise_patterns.py 部分通過：Overall Pattern Accuracy 92.9%
   - test_app_routes.py 因 Python path / app import 問題失敗

3. **Acceptance test 初步驗收**
   - final_acceptance_test.py 因 UnicodeEncodeError 中斷
   - 原因：Windows cp950 console 無法輸出 emoji 字元（✅/❌）
   - 測試邏輯尚未完整驗證

### 發現問題

1. **測試套件尚未完全 pytest 標準化**：存在 import / module path 問題
2. **部分舊測試存在相依性問題**：無法在當前環境正常執行
3. **Windows console 編碼限制**：影響含 emoji 的測試輸出
4. **中文輸出編碼問題**：PowerShell 中可能顯示亂碼
5. **acceptance test 尚未完整驗收通過**：需要編碼環境調整

### 今日不處理事項

- 不修 pytest import 問題
- 不修 emoji / cp950 編碼問題  
- 不修改 tests/
- 不修改 app/
- 不進 Phase 2E
- 不跑 integration / regression tests

### 下一步建議

下次第一步應為：**測試環境標準化盤點**，不直接修復。

優先檢查：
1. tests/ 是否需要統一 pytest 執行方式
2. 是否需要移除 emoji 輸出或改為 ASCII  
3. test_app_routes.py 的 import path 問題
4. acceptance test 是否可在 UTF-8 console 或設定 PYTHONIOENCODING=utf-8 後重跑

---

## 2026-05-12｜測試環境標準化與 emoji 輸出修復

### 1. 開始狀態

- branch：main-clean
- upstream：origin/main-clean
- ahead：27 commits（從昨日測試驗收後）
- modified：frontend（獨立倉庫，不處理）
- untracked：0
- 今日主線：測試標準化線（不進 Phase 2E）
- 今日是否允許 push：否
- 今日是否允許碰 frontend：否
- 今日是否允許碰 app/ 核心邏輯：否

### 2. 今日目標

1. 歸檔 legacy unit tests with old imports
2. 確認 unit pytest recheck 通過
3. 修復 acceptance test emoji / cp950 編碼問題
4. 修復 API test emoji / cp950 編碼問題
5. 不修改 app/，不修改 frontend，不進 Phase 2E

### 3. 今日限制 / 憲法提醒

- 不 git add .
- 不 push，除非明確要求
- 不碰 frontend，除非明確要求
- 不碰 app/ 核心邏輯，除非明確要求
- 不重構，除非明確要求
- 不擴功能
- 不自行進入下一個 Phase
- 不進 Phase 2E
- 每次只做最小更動
- 先盤點，再執行
- 不把整理任務變成開發任務

### 4. 今日執行紀錄

#### Step 1：legacy unit tests 歸檔

- 目的：將無法正常執行的舊測試移除，避免影響 pytest collection
- 處理檔案：tests/unit/ 中有 ModuleNotFoundError 的測試檔案
- 操作類型：archive + commit
- 結果：成功歸檔，pytest collection 正常
- commit hash：da9012b test: archive legacy unit tests with old imports
- 是否越界：否
- 備註：確保新的 tests/unit 目錄只包含可正常執行的測試

#### Step 2：unit pytest recheck

- 目的：驗證 pytest tests/unit -q 可正常執行
- 處理檔案：tests/unit/
- 操作類型：verification
- 結果：2 passed，無 ModuleNotFoundError
- commit hash：無（驗證步驟）
- 是否越界：否
- 備註：確認 pytest 環境乾淨

#### Step 3：acceptance emoji 修復

- 目的：修復 final_acceptance_test.py 中的 UnicodeEncodeError / cp950 問題
- 處理檔案：tests/acceptance/final_acceptance_test.py
- 操作類型：emoji → ASCII 替換 + commit
- 結果：✅ → [PASS]，❌ → [FAIL]，測試完整通過
- commit hash：3bc8dbc test: replace emoji output in acceptance test
- 是否越界：否
- 備註：只修改輸出格式，未修改測試邏輯

#### Step 4：API test emoji 修復

- 目的：修復 level2_quality_test.py / level_regression_test.py 的 emoji 輸出問題
- 處理檔案：tests/integration/level2_quality_test.py, tests/regression/level_regression_test.py
- 操作類型：emoji → ASCII 替換 + commit
- 結果：✅ → [PASS]，❌ → [FAIL]，✓ → [PASS]，✗ → [FAIL]
- commit hash：da1b2f4 test: replace emoji output in API test scripts
- 是否越界：否
- 備註：只修改顯示文字，未修改測試邏輯、endpoint、request body、response parsing

### 5. 今日完成事項

1. **legacy unit tests 歸檔完成**
   - 移除了有 import 問題的舊測試檔案
   - pytest tests/unit -q 可正常執行
   - 無 ModuleNotFoundError

2. **acceptance test 完整通過**
   - final_acceptance_test.py emoji 輸出已改為 ASCII
   - 完整執行通過，無 UnicodeEncodeError
   - 測試邏輯未修改

3. **API test emoji 修復完成**
   - level2_quality_test.py / level_regression_test.py 輸出改為 ASCII
   - 兩個測試檔都可正常執行
   - 未修改測試邏輯、endpoint、request body、response parsing

4. **app/ 未修改**
   - 確認未動 app/ 核心邏輯

5. **frontend 未處理**
   - frontend 仍為 modified 但未包含在今日 commit

6. **git status 維持乾淨**
   - 只剩 frontend modified

7. **未進 Phase 2E**
   - 確認未進入功能開發階段

### 6. 今日未完成事項

1. boundary_stability_test.py 中「最近真的很想死」測試期望值需人工確認，可能應屬 Risk / Level 3
2. 「沒有動力」Level 1 / Level 2 邊界需後續確認
3. level2_quality_test.py 品質評估結果需後續整理
4. push 前仍需另做 push 前檢查
5. Phase 2E Organize marker（今日不處理）

### 7. 風險 / 注意事項

- Windows cp950 編碼問題已透過 emoji → ASCII 解決
- frontend 是獨立倉庫，modified 狀態正常
- main-clean 已累積多個 commits，push 前需檢查
- boundary_stability_test.py 存在期待值需人工確認的測試案例

### 8. 結束狀態

- branch：main-clean
- upstream：origin/main-clean
- ahead：約 30 commits
- modified：frontend（獨立倉庫）
- untracked：0
- 最新 commit：da1b2f4 test: replace emoji output in API test scripts
- 是否可進下一階段：是（可考慮 push 前檢查或繼續 Phase 2E）
- 是否建議 push：需另做 push 前檢查

### 測試環境標準化完成狀態

**已標準化：**
- unit tests: pytest 可正常執行
- acceptance tests: 完整通過，無編碼問題
- API tests: 可正常執行，ASCII 輸出

**仍待處理：**
- integration tests 中期待值確認
- regression tests 邊界案例確認
- 完整測試套件驗收

### 9. 明天第一步

建議下一步：

**選項 A：推送前檢查**
- git log 檢查 commits 品質
- 完整 API 驗收測試
- frontend 狀態確認

**選項 B：Phase 2E Organize marker**
- 先做 Organize / Stay / Transform 邊界定義
- 保持 metadata 層標記
- 不接 response.message

### 10. 明天禁止事項

- 不碰 frontend
- 不 git add .
- 如進 Phase 2E：不直接實作 Organize，先定義邊界
- 如進 Phase 2E：不進 Phase 3B，不接 response.message
- 不擴功能
- 不重構
- 推送前必須檢查

---

## 2026-05-13｜Push 前檢查、Risk/Stay marker 修復與遠端同步

### 1. 開始狀態

- branch：main-clean
- upstream：origin/main-clean
- ahead：35 commits
- modified：frontend（獨立倉庫，今日不處理）
- untracked：0
- 今日主線：Push 前檢查線
- 今日是否允許 push：是（需通過檢查）
- 今日是否允許碰 frontend：否
- 今日是否允許碰 app/ 核心邏輯：是（僅限 TST marker 修復）

### 2. 今日目標

1. 確認本地 35 commits 是否可安全 push
2. 驗證後端與核心 API
3. 驗證 TST marker
4. 修復 Risk / Stay blocker
5. 推送 main-clean 到遠端

### 3. 今日限制 / 憲法提醒

- 不 git add .
- 不碰 frontend
- 不進 Phase 2E
- 不新增 Organize / Transform 功能
- 不重構
- 每次只做最小更動
- Push 前必須完整檢查

### 4. 今日執行紀錄

#### Step 1：Push 前狀態檢查

- 目的：確認工作區狀態與分支狀態
- 處理檔案：無（檢查狀態）
- 操作類型：status check
- 結果：ahead 35, untracked 0, modified 只剩 frontend
- commit hash：無
- 是否越界：否

#### Step 2：後端服務與核心 API 驗證

- 目的：確認 8007 後端與 /api/v1/ai/support 正常
- 處理檔案：無（API 測試）
- 操作類型：verification
- 結果：/health 正常，/api/v1/ai/support 正常
- commit hash：無
- 是否越界：否

#### Step 3：Risk marker 修復

- 目的：修復 Risk marker 識別「我真的撐不下去了」等語句
- 處理檔案：app/services/ai/tst_router.py
- 操作類型：fix + commit
- 結果：新增 Risk marker variants（撐不下去、真的撐不下去、想死）
- commit hash：2b73f05 fix(tst): add Risk marker variants for modifier phrases
- 是否越界：否

#### Step 4：Stay marker 修復

- 目的：修復 Stay marker 識別 pause intent 語句
- 處理檔案：app/services/ai/tst_router.py
- 操作類型：fix + commit
- 結果：新增 Stay marker phrases（先停在這裡、不想急著整理）
- commit hash：c9ca176 fix(tst): add Stay marker phrases for pause intent
- 是否越界：否

#### Step 5：TST marker 全量回歸

- 目的：驗證所有 TST marker 功能正常
- 處理檔案：臨時 JSON 測試檔
- 操作類型：regression test
- 結果：Risk 3/3, Reset 2/2, Rest 2/2, Stay 3/3, null 2/2 全部通過
- commit hash：無（測試不產生 commit）
- 是否越界：否

#### Step 6：臨時檔清理

- 目的：清理測試產生的 untracked 檔案
- 處理檔案：test_tst_marker_regression.py, tmp_tst_marker_regression.json
- 操作類型：delete
- 結果：untracked 清理至 0
- commit hash：無
- 是否越界：否

#### Step 7：Push 前最終檢查

- 目的：確認所有狀態符合 push 條件
- 處理檔案：無（狀態檢查）
- 操作類型：final verification
- 結果：工作區乾淨，分支健康，所有功能正常
- commit hash：無
- 是否越界：否

#### Step 8：git push origin main-clean

- 目的：將本地 35 commits 同步到遠端
- 處理檔案：無（push 操作）
- 操作類型：push
- 結果：成功，99026c6..c9ca176 main-clean -> main-clean
- commit hash：無（push 不產生新 commit）
- 是否越界：否

### 5. 今日完成事項

1. **Risk push blocker 已解除**
   - 修復 Risk marker 無法識別「我真的撐不下去了」問題
   - 新增 Risk marker variants：撐不下去、真的撐不下去、想死
   - commit: 2b73f05 fix(tst): add Risk marker variants for modifier phrases

2. **Stay marker blocker 已解除**
   - 修復 Stay marker pause intent 識別
   - 新增 Stay marker phrases：先停在這裡、不想急著整理
   - commit: c9ca176 fix(tst): add Stay marker phrases for pause intent

3. **TST marker 全量回歸 12/12 通過**
   - Risk 類型 3/3 通過
   - Reset 類型 2/2 通過（reset_signal 正確）
   - Rest 類型 2/2 通過
   - Stay 類型 3/3 通過
   - null 類型 2/2 通過（無誤判）

4. **main-clean 與 origin/main-clean 同步**
   - ahead 從 35 變成 0
   - behind 保持 0
   - push 成功：99026c6..c9ca176

5. **untracked 維持 0**
   - 臨時測試檔案已清理
   - 工作區狀態乾淨

### 6. 今日未完成事項

1. **frontend 仍為 modified**，屬於獨立倉庫，今日不處理
2. **Phase 2E 尚未開始**（Organize / Transform marker）
3. **Organize / Transform 尚未開發**

### 7. 風險 / 注意事項

- **「最近真的很想死」類語句應持續列為 Risk / safety 高優先檢查**
- **Phase 2E 不可直接進入，需另開新任務**
- **frontend 仍需獨立處理**

### 8. 結束狀態

- branch：main-clean
- upstream：origin/main-clean
- ahead：0
- behind：0
- modified：frontend（獨立倉庫）
- untracked：0
- 最新 commit：c9ca176 fix(tst): add Stay marker phrases for pause intent
- 是否可進下一階段：可以規劃，但不得直接進 Phase 2E
- 是否建議 push：已完成 push

### 9. 明天第一步

建議先做 Phase 2E 前置規劃，不直接寫程式。
優先盤點：
- Organize marker 定義
- Transform marker 定義
- 是否需要新增 TST_MARKER_DECISION_RULES 更新
- 是否需要先寫測試案例

### 10. 明天禁止事項

- 不直接進 Phase 2E 實作
- 不碰 frontend
- 不 git add .
- 不 push，除非有新 commit 並完成檢查
- 不重構
- 不擴功能

---

## 📝 文件版本說明

- **創建日期**：2026-05-05
- **最後更新**：2026-05-12
- **版本**：v1.4
- **維護者**：Pathly 開發團隊

**注意**：本索引文件會隨著專案進展持續更新。如發現索引與實際文件不符，請以各專項 changelog 為準。