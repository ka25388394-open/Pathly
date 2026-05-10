# Pathly 開發環境整理進度｜2026-05-09

## 1. 今日功能開發已完成

- Phase 2D：Stay marker 前盤點完成
- Phase 2D：Stay marker metadata 實作完成
- Phase 2D-Fix：Rest / Stay 邊界修補完成
- Phase 2D marker 層穩定性測試完成
- 目前 TST marker 支援：
  - Risk
  - Reset
  - Rest
  - Stay
  - null
- 優先序：
  Risk > Reset > Rest > Stay > null

## 2. 今日文件已更新

- docs/TST_ROUTER_CHANGELOG.md 已更新
- docs/PATHLY_DEVELOPMENT_DIARY_INDEX.md 已更新至 v1.1
- Phase 2D 與穩定性測試結果已記錄

## 3. 今日 Git 本地備份已完成

目前已完成 4 個本地 commit：

1. 453cff8 chore: stop tracking Claude local settings
2. ef92eac security: clean debug logs and tighten CORS in FastAPI app
3. 30aeb4d chore: remove Python cache from Git tracking
4. 9fa1de2 feat: complete TST markers through Stay and update development docs

目前尚未 push GitHub。

## 4. app/main.py 清理狀態

- 已移除 debug print
- 已移除 debug request middleware
- 已移除 route debug log
- CORS 已從 allow_origins=["*"] 改回本地白名單
- 8007 啟動測試通過
- /health 測試通過
- 五個 marker smoke test 通過
- CORS localhost:5500 測試通過

## 5. .claude/settings.local.json 狀態

目前已完成：

- .claude/settings.local.json 已從 Git tracking 移除 ✅
- 本地檔案仍保留 ✅
- .gitignore 已有 .claude/ 規則 ✅
- 已建立獨立 commit (453cff8) ✅

## 6. 目前尚未處理項目

### A. deleted 舊檔案

尚未處理：

- app_simple.py
- railway.json
- simple_chat_endpoint.py

需判斷：

- 接受刪除
- 移到 archive/
- 或還原

### B. 核心 modified 檔案

尚未決定是否 commit：

- app/api/v1/__init__.py
- app/api/v1/dialogue.py
- app/config.py
- app/core/unified_ai_client.py
- app/modules/dialogue/response_modes.py

初步判斷：

可能可 commit：
- app/api/v1/__init__.py
- app/config.py
- app/core/unified_ai_client.py
- app/modules/dialogue/response_modes.py

需要 review：
- app/api/v1/dialogue.py

### C. pathly_simple_ui.html

尚未處理。

需判斷：

- 是否保留 localhost:8007 接線
- 是否移除原始 JSON debug 顯示
- 是否獨立 commit
- 或暫時不 commit

### D. frontend

frontend/ 是獨立 Git 倉庫。

暫時不要混入主專案 commit。

### E. tests / scripts / archive 分流

尚未開始整理：

- tests/fixtures/marker/
- tests/fixtures/level2/
- tests/fixtures/encoding/
- tests/integration/
- tests/unit/
- scripts/dev/
- scripts/ops/
- archive/prototypes/
- archive/debug/

## 7. 明天建議整理順序

1. 先確認 git status
2. ~~先 commit .claude/settings.local.json tracking 移除~~ ✅ 已完成
3. 再處理 deleted 舊檔案
4. 再確認核心 modified 檔案
5. 再處理 pathly_simple_ui.html
6. frontend 暫時不要動
7. 最後才整理 tests / scripts / archive
8. 全部穩定後再評估 push GitHub

## 8. 明天開工注意事項

- 不要 git add .
- 不要直接 push
- 不要一次大搬家
- 不要直接 commit frontend
- 不要移動 app/ 核心程式
- 不要刪除業務邏輯檔案
- 每一步都要先盤點，再修改
- 明天先做開發環境整理，不要直接進 Phase 2E

---

# 2026-05-10 更新紀錄

## 1. 今日已完成

### Git 狀態確認

- 已確認 main-clean 目前領先 origin/main-clean
- 已確認 .claude/settings.local.json tracking removal 已完成並 commit
- 已確認 docs/DEV_ENV_CLEANUP_PLAN_2026-05-09.md 中「4 個 commit」記錄正確

### Deleted 舊檔案處理

已完成 commit：

571b93b chore: remove legacy prototypes and archive Railway config

內容：
- app_simple.py：舊 prototype，已接受刪除
- simple_chat_endpoint.py：舊聊天 endpoint，已接受刪除
- railway.json：舊 Railway 設定，已移至 archive/railway.json 保留參考

### 核心架構整理

已完成 commit：

3e8e494 feat: add AI router and dialogue mode selection infrastructure

內容：
- app/api/v1/__init__.py：新增 /api/v1/ai router 註冊
- app/modules/dialogue/response_modes.py：新增 A/B/C/D mode 判斷基礎

已完成 commit：

3206149 feat: enhance dialogue response with A/B/C/D mode support

內容：
- app/core/unified_ai_client.py：新增 level_used、format_type、next_suggestions、confidence_score
- 支援 A/B/C/D mode 對應
- Unicode 顯示問題記為後續觀察，不在此 commit 處理

已完成 commit：

be4358a refactor: connect dialogue endpoints to UnifiedAIClient

內容：
- app/api/v1/dialogue.py 接入 UnifiedAIClient
- /dialogue/chat 測試可用
- /dialogue/analyze 測試可用
- test_all_levels 與 analysis_engine 仍為 TODO，記為後續工作

已完成 commit：

8fdd82d fix: restore AI config fields and dynamic database detection

內容：
- app/config.py 補回 gemini_model_deep、gemini_model_fast、tone_reviewer_enabled、app_host
- 保留 backend_port、frontend_port、project_name、env、alias 支援
- 恢復 is_sqlite 動態判斷
- 本地測試通過：/health、/api/v1/ai/support、/dialogue/chat、/dialogue/analyze

### 開發工具整理

已完成 commit：

21ba575 chore: move AI support test UI into dev tools

內容：
- pathly_simple_ui.html 移動為 tools/dev/pathly_ai_support_test_ui.html
- 明確標註 DEV ONLY
- 保留 raw JSON、metadata、session_id、tst_marker 顯示
- 定位為本地開發測試工具，不是正式前端

---

## 2. 目前已完成的本地 commits

目前 main-clean 領先 origin/main-clean 10 個 commit，尚未 push。

Commits 列表：

1. 9fa1de2 feat: complete TST markers through Stay and update development docs
2. 30aeb4d chore: remove Python cache from Git tracking
3. ef92eac security: clean debug logs and tighten CORS in FastAPI app
4. 453cff8 chore: stop tracking Claude local settings
5. 571b93b chore: remove legacy prototypes and archive Railway config
6. 3e8e494 feat: add AI router and dialogue mode selection infrastructure
7. 3206149 feat: enhance dialogue response with A/B/C/D mode support
8. be4358a refactor: connect dialogue endpoints to UnifiedAIClient
9. 8fdd82d fix: restore AI config fields and dynamic database detection
10. 21ba575 chore: move AI support test UI into dev tools

---

## 3. 目前剩餘項目

### A. frontend 子倉庫

目前狀態：
- frontend 顯示 modified
- frontend 是獨立 Git 倉庫
- 暫時不要混入主專案 commit

待處理：
- 之後需單獨進入 frontend/ 檢查
- 目前不要動

### B. 大量 untracked 測試 / 工具檔案

尚未整理：
- 測試腳本
- debug 腳本
- 啟動腳本
- 檢查腳本
- archive 備份檔案

下一步建議：
先盤點，不要直接移動。

### C. 測試 / 腳本 / archive 分流

尚未正式整理：

- tests/fixtures/marker/
- tests/fixtures/level2/
- tests/fixtures/encoding/
- tests/integration/
- tests/unit/
- scripts/dev/
- scripts/ops/
- archive/debug/
- archive/prototypes/

---

## 4. 下一步建議

下一步進入：

Step：Untracked 檔案分流盤點

目標：
整理大量測試腳本與工具腳本，分成：

- 正式測試資料
- 正式測試腳本
- 本地開發工具
- 維運腳本
- debug / 臨時檔
- archive 檔
- 應被 .gitignore 排除的檔案

注意：
- 不要直接搬檔
- 不要 git add .
- 不要 commit
- 不要 push
- 先盤點，再決定移動策略

---

## 5. 目前狀態總結

目前後端核心整理已基本完成：

- TST marker 系統完成至 Stay
- AI router 已接入
- A/B/C/D mode 基礎架構已建立
- UnifiedAIClient 已支援 A/B/C/D 回應格式
- dialogue endpoint 已接入 UnifiedAIClient
- config.py 相容性已修復
- dev test UI 已移至 tools/dev/

尚未 push GitHub，等 untracked 檔案整理完成後再評估。