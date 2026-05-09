# TST Response Pipeline Blueprint V01

## 1. 文件目的

說明 tst_marker 如何在未來對應到 response mode。

本文件只定義管路藍圖，不進行程式實作。

---

## 2. 目前狀態

已完成 marker：
- Risk
- Reset
- Rest
- null

尚未完成 marker：
- Stay
- Organize
- Transform

目前 marker 僅存在 metadata，不影響 response.message。

---

## 3. 核心原則

- marker 是後端內部導航，不對使用者顯示
- 前台不說「你現在是 Risk / Rest / Reset」
- response mode 只決定承接策略
- 不直接診斷使用者
- 不直接推行動
- 不直接分析
- 每次只問一個小問題
- Risk 永遠安全優先

---

## 4. 迷宮管路總覽

tst_marker → response_mode

- Risk → safety_response_mode
- Rest → rest_closure_mode
- Reset → reset_reopen_mode
- Stay → stay_with_mode
- Organize → organize_invitation_mode
- Transform → transform_permission_mode
- null → original_level_response

---

## 5. 各 marker 的 response mode 定義

### Risk

目的：
安全優先，避免輕鬆聊天。

策略：
- 承接痛苦
- 不開玩笑
- 不推整理
- 不問太多
- 必要時引導求助

禁止：
- 不回「最近有什麼有趣的事嗎？」
- 不回輕鬆聊天
- 不要求使用者立刻分析原因

---

### Rest

目的：
允許使用者停止處理。

策略：
- 收束
- 不推進
- 不要求整理
- 讓使用者知道可以先停

禁止：
- 不繼續追問原因
- 不推行動
- 不說「那我們來整理一下」

---

### Reset

目的：
重新開一輪，不混上一個主題。

策略：
- 接住新主題
- 不把上一輪情緒硬套過來
- 重新給一個小入口

禁止：
- 不延續上一輪問題
- 不強行拉回舊主題

---

### Stay

目的：
陪使用者停在原地。

策略：
- 降低壓力
- 允許說不清楚
- 給一個很小的表達入口

禁止：
- 不分析
- 不整理
- 不轉化

---

### Organize

目的：
邀請整理材料。

策略：
- 協助分開幾件事
- 問一個小問題
- 取得使用者允許

禁止：
- 不直接下結論
- 不直接分析原因
- 不一次列太多東西

---

### Transform

目的：
進入轉化準備，但仍需取得允許。

策略：
- 看見模式
- 輕輕指出可能的重複
- 詢問是否願意一起看

禁止：
- 不直接替使用者定義
- 不強行轉化
- 不過早深挖

---

### null

目的：
沒有特殊 TST marker，走原本 Level 1 / 2 / 3 流程。

策略：
- 保持原本 response_builder
- 不額外介入