# TST Phase 2E Test Cases V01

## 1. 文件目的

本文件用於 Phase 2E Organize / Transform marker 實作前的測試案例基準。

**重要說明：**
- 此文件只定義測試案例，不代表已實作
- 為 Phase 2E-1 / Phase 2E-2 實作提供測試依據
- 所有測試案例需要在程式實作完成後驗證
- 人工確認案例需要額外評估

---

## 2. 測試範圍

### 包含：
- Organize marker 正向案例
- Transform marker 正向案例
- Transform vs Risk 邊界案例
- Organize vs Stay 邊界案例
- Rest vs Organize 能量邊界案例
- 不應誤判案例
- 全量回歸案例

### 不包含：
- response.message 測試（屬於 Phase 3）
- Phase 3 response mode 測試
- frontend 測試（獨立倉庫）
- 長期記憶或會話記錄測試

---

## 3. Marker 預期優先順序

**優先順序：** Risk → Reset → Rest → Stay → Transform → Organize

**重要說明：** null 是 fallback，不是 marker priority member。當所有 marker 都未命中時的預設結果。

---

## 4. Organize 正向測試案例

| ID | Input | Expected marker | 說明 |
|---|---|---|---|
| ORG-001 | 好像是因為工作壓力 | Organize | 初步原因描述，需要進一步整理 |
| ORG-002 | 我覺得可能跟睡眠有關 | Organize | 片段推測，有材料但需引導 |
| ORG-003 | 其實我在意的是別人的看法 | Organize | 開始能說出在意點 |
| ORG-004 | 我想把這件事講清楚一點 | Organize | 明確整理意願 |
| ORG-005 | 可能是我想太多了 | Organize | 自我反思，有材料可深入 |
| ORG-006 | 我想理一理最近的狀況 | Organize | 直接表達整理需求 |
| ORG-007 | 有一部分是家裡的事 | Organize | 片段描述，可進一步分析 |
| ORG-008 | 我覺得主要是時間管理問題 | Organize | 有初步歸因，需要整理細節 |
| ORG-009 | 應該跟我的習慣有關係 | Organize | 開始連結行為模式 |
| ORG-010 | 我開始有點頭緒了 | Organize | 有材料出現，可協助整理 |
| ORG-011 | 讓我想想怎麼說比較好 | Organize | 想要表達但需要整理思緒 |
| ORG-012 | 我想整理一下思緒 | Organize | 明確表達整理需求 |
| ORG-013 | 有幾件事混在一起 | Organize | 需要協助分開不同議題 |
| ORG-014 | 我想把原因理清楚 | Organize | 主動尋求澄清與整理 |

---

## 5. Transform 正向測試案例

| ID | Input | Expected marker | 說明 |
|---|---|---|---|
| TRF-001 | 我好像每次都這樣逃避 | Transform | 看見重複模式 |
| TRF-002 | 我發現我一直在重複同樣的錯誤 | Transform | 模式覺察，有洞察語言 |
| TRF-003 | 其實我是在害怕被拒絕 | Transform | 看見深層動機 |
| TRF-004 | 原來我是不相信自己 | Transform | 自我覺察，理解內在機制 |
| TRF-005 | 我總是在壓力來的時候就想逃 | Transform | 看見觸發條件與反應模式 |
| TRF-006 | 我發現我很在乎別人的評價 | Transform | 洞察內在驅動力 |
| TRF-007 | 其實我一直在逃避面對問題 | Transform | 看見行為模式與內在矛盾 |
| TRF-008 | 我看到自己的矛盾了 | Transform | 明確的內在矛盾覺察 |
| TRF-009 | 我明白了，我其實是想要被認同 | Transform | 深層需求洞察 |
| TRF-010 | 我總是這麼做的原因是缺乏安全感 | Transform | 看見行為背後的深層原因 |
| TRF-011 | 我發現自己的規律了 | Transform | 模式辨識與自我覺察 |
| TRF-012 | 這就是我一直以來的模式 | Transform | 長期模式的清晰認知 |
| TRF-013 | 我終於看到自己在做什麼了 | Transform | 行為覺察與模式理解 |
| TRF-014 | 我意識到我的內在衝突了 | Transform | 深層心理動力覺察 |

---

## 6. Transform vs Risk 邊界案例

| ID | Input | Expected marker | 說明 |
|---|---|---|---|
| TvR-001 | 我發現我總是在逃避問題 | Transform | 純模式覺察，語氣穩定 |
| TvR-002 | 我發現我總是在逃避問題，但我真的覺得自己很沒用 | Risk 或人工確認 | 模式覺察 + 自我否定，安全優先 |
| TvR-003 | 我看到自己的模式了，我每次壓力一來就躲起來 | Transform | 模式描述，無危機語言 |
| TvR-004 | 我看到自己的問題了，但我真的撐不下去了 | Risk | 洞察 + 撐不下去訊號，優先安全 |
| TvR-005 | 我發現我一直重複同樣的錯誤 | Transform | 模式覺察，情緒相對穩定 |
| TvR-006 | 我一直重複同樣的錯誤，我是不是根本沒救了 | Risk 或人工確認 | 模式 + 自我價值否定，需要確認 |
| TvR-007 | 我每次都這樣，我真的是個失敗者 | Risk | 明確自我攻擊，非 Transform |
| TvR-008 | 我看到自己的規律了，雖然不舒服但我想面對 | Transform | 洞察 + 承受力表達 |

---

## 7. Organize vs Stay 邊界案例

| ID | Input | Expected marker | 說明 |
|---|---|---|---|
| OvS-001 | 我想理一理最近的狀況 | Organize | 有整理意願與能量 |
| OvS-002 | 我想整理一下，但我現在說不上來 | Stay 或人工確認 | 整理意願但缺乏材料 |
| OvS-003 | 好像跟工作有關，我想講清楚一點 | Organize | 有片段材料且想澄清 |
| OvS-004 | 好像跟工作有關，但我現在腦袋一片空白 | Stay | 有模糊感知但表達困難 |
| OvS-005 | 我也不知道是怎麼回事，就是很亂 | Stay | 缺乏語言材料，需要陪伴 |
| OvS-006 | 可能是因為...但我不太確定 | Organize | 有初步材料，不確定感可以整理 |

---

## 8. Rest vs Organize 能量邊界案例

| ID | Input | Expected marker | 說明 |
|---|---|---|---|
| RvO-001 | 我想理清楚，但現在真的太累了 | Rest | 整理意願但能量不足 |
| RvO-002 | 我有點累，但我想先整理一下發生什麼事 | Organize 或人工確認 | 微疲憊但仍有整理動力 |
| RvO-003 | 我現在沒力氣想，只想休息 | Rest | 明確能量耗盡與休息需求 |
| RvO-004 | 我想整理但我好累喔 | Rest 或人工確認 | 意願與能量衝突，需要評估 |
| RvO-005 | 先不要想了，我需要休息 | Rest | 明確停止訊號 |

---

## 9. 不應誤判案例

### Risk 類（應判 Risk，不判其他）
| ID | Input | Expected marker | 說明 |
|---|---|---|---|
| RISK-001 | 我想死 | Risk | 明確自殺意念 |
| RISK-002 | 我真的撐不下去了 | Risk | 危機語言 |
| RISK-003 | 我活著沒意義 | Risk | 生命價值否定 |
| RISK-004 | 我什麼都做不好 | Risk | 強烈自我否定 |

### Reset 類（應判 Reset，不判其他）
| ID | Input | Expected marker | 說明 |
|---|---|---|---|
| RST-001 | 算了，先不要聊這個 | Reset | 明確話題轉換 |
| RST-002 | 我想換個話題 | Reset | 直接表達換主題 |
| RST-003 | 對了，還有另一件事 | Reset | 新主題提出 |

### Rest 類（應判 Rest，不判其他）
| ID | Input | Expected marker | 說明 |
|---|---|---|---|
| REST-001 | 我現在只想休息 | Rest | 明確休息需求 |
| REST-002 | 我沒有力氣整理 | Rest | 能量不足想停止 |
| REST-003 | 今天夠了，先停下來 | Rest | 收束訊號 |

### Stay 類（應判 Stay，不判其他）
| ID | Input | Expected marker | 說明 |
|---|---|---|---|
| STAY-001 | 我說不上來 | Stay | 表達困難 |
| STAY-002 | 我不知道怎麼講 | Stay | 缺乏語言材料 |
| STAY-003 | 就是很混亂 | Stay | 低清晰度狀態 |

### null 類（應為 null，不判特殊 marker）
| ID | Input | Expected marker | 說明 |
|---|---|---|---|
| NULL-001 | 今天早上喝了一杯咖啡 | null | 日常描述 |
| NULL-002 | 我今天去買早餐 | null | 事實陳述 |
| NULL-003 | 天氣不錯 | null | 一般對話 |

---

## 10. 全量回歸案例

### 已實作 marker 回歸測試

**Risk marker：**
- 我不想活了 → Risk
- 我很沒用 → Risk
- 我撐不下去了 → Risk

**Reset marker：**
- 聊別的吧 → Reset
- 換個話題 → Reset

**Rest marker：**
- 我先不想了 → Rest
- 我想休息 → Rest

**Stay marker：**
- 我不知道 → Stay
- 說不上來 → Stay

**null marker：**
- 今天很忙 → null

**註明：** Organize / Transform 尚未實作，正式測試前 expected marker 只是未來目標。

---

## 11. 驗收標準

### Phase 2E 實作前要求：
- **測試案例文件必須先確認**
- **人工邊界案例必須先評估**
- **與產品需求確認測試覆蓋度**

### Phase 2E-1 Organize 實作完成後，需通過：
- ✅ Organize 正向案例 (ORG-001 到 ORG-014)
- ✅ 不應誤判既有 Risk / Reset / Rest / Stay / null 案例
- ✅ Organize vs Stay 邊界案例 (OvS-001 到 OvS-006)
- ✅ Rest vs Organize 邊界案例 (RvO-001 到 RvO-005)

### Phase 2E-2 Transform 實作完成後，需通過：
- ✅ Transform 正向案例 (TRF-001 到 TRF-014)
- ✅ Transform vs Risk 邊界案例 (TvR-001 到 TvR-008)
- ✅ 不應破壞 Organize 與既有 marker
- ✅ 全量 6-marker 回歸測試

### 人工確認案例處理：
- 標註「人工確認」的案例需要額外評估
- 邊界模糊案例可以接受合理的替代判斷
- 安全相關案例（Transform vs Risk）寧可保守

---

## 12. 明確禁止事項

### 測試範圍限制：
- ❌ **本文件不代表程式已實作**
- ❌ **不測 response.message**（屬於 Phase 3）
- ❌ **不接 Phase 3 response mode**
- ❌ **不修改 frontend**（獨立倉庫）
- ❌ **不跳過人工確認案例**

### 實作階段限制：
- ❌ **不一次實作兩個 marker**
- ❌ **不跳過測試驗證**
- ❌ **不忽略邊界安全性**
- ❌ **不破壞既有 marker 穩定性**

---

*文件版本：V01*  
*建立日期：2026-05-28*  
*狀態：Phase 2E 測試案例基準 - 待實作前確認*  
*案例總數：65 個測試案例*