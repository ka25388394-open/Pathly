# Session Memory Changelog

## 日期
2026-04-28

## 今日完成

- 確認 /api/v1/ai/support 原本是單輪分流回應系統
- 新增 app/services/ai/session_store.py
- 在 app/api/v1/ai/support.py 接入 session context
- 在 app/services/ai/response_builder.py 接入 Level 2 第二句與第三句模板
- 加入 Level 2 continuity guard
- 修正 turn_count off-by-one 問題
- 完成三句順流承接測試

## 測試案例

同一個 session_id：

1. 我今天真的很累
2. 整個人有點空掉
3. 什麼都不太想做

## 測試結果

- 第一句：Level 2 / 疲勞中 / 第一層承接
- 第二句：Level 2 / 疲勞中 / 第二句承接模板
- 第三句：Level 2 / 疲勞中 / 輕量狀態辨識第三句模板

## 目前狀態

Level 2 三句順流承接 MVP 完成。

## 尚未處理

- Level 2 低認知負荷工程規則尚未正式獨立整理
- session memory 目前為 in-memory，重啟後會清空
- 尚未接資料庫
- 尚未做長期多輪對話記憶
- 尚未做完整前端 session 串接檢查

## 下一步建議

下一步只做一件事：

正式補上 Level 2 低認知負荷規則，限制第二句與第三句輸出保持短句、低負擔、好回覆。

---

## 2026-04-29 更新

## 今日完成

- 重新啟動後完成 Level 2 三句順流承接回歸測試
- 確認 server /health 正常
- 確認同一個 session_id 下 turn_count 可正確跑出 1 → 2 → 3
- 修正 metadata 中 turn_count 顯示不準的問題
- 確認模板選擇未受影響
- 建立 docs/LEVEL2_THREE_TURN_FLOW_SPEC.md
- 完成三類核心狀態流規格：
  - 疲勞流
  - 混亂流
  - 任務壓力流
- 將 D 自我觀察流補入文件，標記為補充流
- 修正 D 自我觀察流中兩句低認知負荷風險句
- 確認目前文件與 response_builder.py 實作同步
- 已建立 docs/LEVEL2_LOW_COGNITIVE_LOAD_RULES.md
- 已完成 response_builder.py Level 2 模板低認知負荷盤點
- 盤點結果：目前所有 Level 2 第二句與第三句模板均符合低認知負荷工程標準
- 不需要進行程式修正
- 兩句稍長模板目前判定可接受，暫不修改，避免過度優化

## 目前狀態

Level 2 三句順流承接已完成：
- session memory 可運作
- turn_count 顯示正確
- 三句模板可正確觸發
- 三類核心狀態流已文件化
- 自我觀察補充流已文件化
- 低認知負荷工程規格已建立
- 現有模板已通過低認知負荷盤點

## 下一步

先不要繼續優化 Level 2 模板。
下一步再考慮前端是否正確傳遞 session_id。

---

## 2026-04-29 補充更新：簡易前端 session_id 打通

## 今日完成

- 盤點 pathly_simple_ui.html 是否正確傳遞 session_id
- 確認原本 pathly_simple_ui.html 缺少 session_id
- 僅修改 pathly_simple_ui.html
- 使用 sessionStorage 保存 pathly_session_id
- 每次呼叫 /api/v1/ai/support 時帶入同一個 session_id
- 完成簡易 UI 三句測試

## 測試案例

同一個 session_id 連續輸入：

1. 我今天真的很累
2. 整個人有點空掉
3. 什麼都不太想做

## 測試結果

- 第一句：turn_1 / Level 2 / 疲勞中 / 第一句承接
- 第二句：turn_2 / Level 2 / 疲勞中 / 第二句承接
- 第三句：turn_3 / Level 2 / 疲勞中 / 第三句輕量狀態辨識

## 目前狀態

Level 2 三句順流承接已完成簡易前端與後端整合。

## 尚未處理

- 正式 frontend/ Next.js 尚未接入 /api/v1/ai/support
- 正式 frontend/ 尚未傳遞 session_id
- 目前僅 pathly_simple_ui.html 完成測試

## 下一步建議

先不要修改正式 frontend/。
下一步可先盤點正式 frontend/ 接入 /api/v1/ai/support 的最小方案。

---

## 2026-04-30 更新：正式 dialogue 頁接入完成

## 今日完成

- 盤點正式 frontend/ Next.js 接入 /api/v1/ai/support 的最小方案
- 確認最小修改範圍為：
  - frontend/lib/api.ts
  - frontend/app/dialogue/page.tsx
- 在 frontend/lib/api.ts 新增 sendSupportMessage
- 在 frontend/app/dialogue/page.tsx 改用 sendSupportMessage
- 使用 sessionStorage 管理 pathly:session_id
- 調整 response mapping：
  - data.data.response.message 作為 assistant message
  - data.data.response.suggestions 作為建議
  - data.data.level 作為 level
  - data.data.response.state 作為 state
- 確認正式 dialogue 頁可成功接入 /api/v1/ai/support
- 確認正式前端可完成前三句 Level 2 順流承接測試

## 測試案例

同一個 session_id 連續輸入：

1. 我今天真的很累
2. 整個人有點空掉
3. 什麼都不太想做

## 測試結果

- 第一句：turn_1 / Level 2 / 疲勞中 / 第一句承接
- 第二句：turn_2 / Level 2 / 疲勞中 / 第二句承接
- 第三句：turn_3 / Level 2 / 疲勞中 / 第三句輕量狀態辨識

## 目前狀態

Level 2 三句順流承接已完成正式 dialogue 頁接入。

## 尚未處理

- 第四句以後的對話策略尚未設計
- enter/step、enter/state、enter/thing 尚未接入新 API
- 尚未決定正式前端其他入口是否要全部統一到 /api/v1/ai/support
- 尚未做正式 UI 長流程測試

## 下一步建議

先不要新增第四句功能。
下一步先設計「三句後策略 v0.1」，決定第 4 句以後是：
- 維持第三句承接
- 重新開始一輪
- 轉成整理模式
- 給使用者一個小選擇

---

## 2026-04-30 補充更新：TST / STL 定位修正完成

## 今日完成

- 修正 docs/LEVEL2_AFTER_THREE_TURNS_ROUTER_SPEC.md 的核心概念
- 明確定義 TST 為三句後的判斷層
- 明確定義 STL 為 TST 判斷後，獲得使用者允許才啟動的語言轉化工具
- 移除 STL / TST 並列分流設計
- 將三句後分流修正為 TST 判斷結果：
  - Stay｜停留承接
  - Organize｜可邀請 STL 整理
  - Transform｜可進一步轉化
  - Rest｜休息即收束
  - Risk｜升級 Level 3
  - Reset｜重新開一輪
- 明確寫入休息、停止、放下都是有效收束，不是失敗
- 保持 v0.1 為規格文件，不實作、不新增 router、不改後端

## 目前狀態

Pathly 三句後分流藍圖已修正為正確架構：

Level 2 三句承接
→ TST 判斷層
→ 視狀態邀請 STL 或停留 / 休息 / 升級 / 重開
→ 使用者允許後才前進

## 下一步建議

不要直接實作 Router。
下一步先盤點目前後端是否已有足夠欄位支援 TST 判斷層。

---

## 2026-04-30 補充更新：「空 / 空掉 / 沒感覺」Level 2 入口判斷修正

## 今日完成

- 盤點 Pathly 判斷引擎與回應資料來源
- 確認 /api/v1/ai/support 目前主要依賴程式碼 keyword rules
- 確認 pathly.db 目前未參與 /api/v1/ai/support 判斷
- 確認 session memory 目前為 in-memory
- 確認「空 / 空掉 / 空空的 / 沒感覺 / 無感」原本問題出在 Level 2 keyword 缺漏
- 在 app/core/ai_config.py 補入「空」類低能量詞
- 修正後，「我今天好空」、「整個人空空的」、「腦袋空掉」、「我有點空」、「整個人沒感覺」、「最近很無感」皆可進入 Level 2
- 大多數「空」類語句可落在「疲勞中」狀態

## 測試結果

- 我今天好空 → Level 2 / 疲勞中
- 整個人空空的 → Level 2 / 疲勞中
- 腦袋空掉 → Level 2 / 疲勞中
- 我有點空 → Level 2 / 疲勞中
- 整個人沒感覺 → Level 2 / 疲勞中
- 最近很無感 → Level 2 / 穩定中

## 備註

「最近很無感」目前雖已進 Level 2，但 state 為「穩定中」，後續可再觀察是否需要細分為低能量 / 麻木 / 空掉相關狀態。

## 目前狀態

Level 2 第一輪入口判斷對「空」類低能量語句的敏感度已提升。

## 下一步建議

先不要繼續補大量 keyword。
下一步回到 TST 判斷邏輯與暫時迷宮標記設計。

---

## 2026-05-01 更新：TST 後端盤點與最小實作方案完成

## 今日完成

- 完成 Step 6：TST v0.1 後端欄位盤點整理
- 檢查七個核心後端檔案：
  - app/schemas/ai.py
  - app/services/ai/session_store.py
  - app/api/v1/ai/support.py
  - app/services/ai/response_builder.py
  - app/services/ai/state_classifier.py
  - app/services/ai/level_detector.py
  - app/core/ai_config.py
- 確認 TST v0.1 所需 15 項資料的支援度
- 識別三大缺口：reset_signal、tst_marker、marker_confidence
- 建立 docs/TST_MINIMAL_IMPLEMENTATION_PLAN_V01.md
- 設計四階段漸進式實作策略：
  - Phase 0：確認基線（純測試）
  - Phase 1：Reset Signal Detector（解決最大缺口）
  - Phase 2：TST Marker Metadata（建立基礎架構）
  - Phase 3：TST Marker 判斷邏輯（完整標記系統）
  - Phase 4：TST Response Mode（才影響回應）

## 後端盤點結論

**大致足夠，但需要補少量欄位**

| 支援狀況 | 項目數 | 備註 |
|---|---|---|
| ✅ 完全支援 | 11/15 | current_message、session_id、turn_count 等 |
| ❌ 缺少 | 3/15 | reset_signal、tst_marker、marker_confidence |
| 📝 需擴充 | 1/15 | Response Schema metadata |

## 最大缺口

1. **Reset Signal 檢測機制** - 完全沒有「換主題」判斷
2. **TST Response Mode 框架** - 第4句後沒有正式處理
3. **Response Builder 術語** - 仍使用舊「STL-lite」術語

## 目前狀態

TST 後續開發七步驟已完成：
- ✅ Step 1-5：文件架構與一致性
- ✅ Step 6：後端欄位盤點
- 📋 Step 7：最小實作方案已制定

## 下一步建議

**強烈建議先做 Phase 1：reset_signal detector**

理由：
- 解決唯一完全缺失的功能
- 最低風險（只檢測，不影響邏輯）
- 可獨立驗證（metadata 直接觀察）
- 為後續 TST 實作鋪路

**重要原則：寧可不做 TST，也不能破壞現有 Level 2 三句承接功能。**