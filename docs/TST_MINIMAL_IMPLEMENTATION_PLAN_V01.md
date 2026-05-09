# TST 最小實作切分方案 v0.1

## 文件定位

**這是實作規劃文件，不是功能文件。**

本文件將 TST v0.1 實作拆分為 4 個可控階段，每個階段都可以獨立測試、驗證和回退。

避免一次性實作完整 TST 系統，降低開發風險。

## 核心原則

### 1. 最小可驗證增量
每個 Phase 都必須能產生可觀察、可測試的結果。

### 2. 向後兼容
每個 Phase 都不能破壞現有 Level 2 三句承接功能。

### 3. 漸進式驗證
先做基礎檢測，再做判斷邏輯，最後才做回應模式。

### 4. 安全第一
Risk 相關功能必須小心處理，不與現有 Level 3 衝突。

## Phase 劃分

---

## Phase 0：確認基線（不實作任何 TST）

### 目的
1. 確認目前 Level 2 三句承接功能完全正常
2. 建立基線測試案例
3. 確保實作前後對比基準

### 允許修改的檔案
- **無**（純測試階段）

### 禁止做的事
- 不修改任何程式碼
- 不新增任何檔案
- 不改 metadata
- 不改 response

### 測試方式

#### 測試案例 1：疲勞流三句承接
```
同一個 session_id 連續輸入：
1. "我今天真的很累"
2. "整個人有點空掉" 
3. "什麼都不太想做"
```

#### 預期結果
```
第一句：turn_1 / Level 2 / 疲勞中 / 第一句承接
第二句：turn_2 / Level 2 / 疲勞中 / 第二句承接
第三句：turn_3 / Level 2 / 疲勞中 / 第三句輕量狀態辨識
```

#### 確認項目
- [ ] turn_count 正確遞增 1 → 2 → 3
- [ ] Level 2 continuity guard 正常運作
- [ ] 第三句使用輕量狀態辨識，不是完整 STL
- [ ] session context 正確保存 last_3_messages
- [ ] metadata 包含正確的 turn 資訊

### 回退方式
- 無需回退（純測試）

### 通過條件
- **所有現有 Level 2 三句測試案例通過**
- **metadata 格式符合預期**
- **無任何回歸問題**

---

## Phase 1：Reset Signal Detector

### 目的
1. 解決最大功能缺口：換主題檢測
2. 建立 Reset 信號基礎檢測能力
3. 不影響主要回應邏輯

### 允許修改的檔案
- `app/core/ai_config.py`（新增 RESET_SIGNAL_KEYWORDS）
- `app/services/ai/level_detector.py`（新增 detect_reset_signal 方法）
- `app/schemas/ai.py`（ResponseMetadata 新增 reset_signal 欄位）
- `app/api/v1/ai/support.py`（調用 reset_signal 檢測並放入 metadata）

### 禁止做的事
- **不修改 response_builder.py**
- **不修改 session_store.py**
- **不讓 reset_signal 影響主要回應**
- **不重開 session**
- **不改變 Level 2 三句邏輯**
- **不接入 TST marker**

### 實作內容

#### 1. 新增 Reset Signal 關鍵字
```python
# ai_config.py
RESET_SIGNAL_KEYWORDS = [
    "另外一件事", "對了", "我想問別的", "先不說這個", 
    "其實不是這個", "我剛剛想到", "換個話題", "不是這個",
    "我想說別的", "算了", "我想問", "對了對了"
]
```

#### 2. 檢測方法
```python
# level_detector.py
def detect_reset_signal(self, message: str) -> bool:
    """檢測是否為換主題信號"""
```

#### 3. Metadata 擴充
```python
# schemas/ai.py ResponseMetadata
reset_signal: Optional[bool] = Field(None, description="是否檢測到重開信號")
```

### 測試方式

#### 測試案例 1：Reset Signal 檢測
```
輸入："對了，我想問別的事"
預期：metadata.reset_signal = true
```

#### 測試案例 2：非 Reset Signal
```
輸入："我今天真的很累"
預期：metadata.reset_signal = false
```

#### 測試案例 3：不影響原有邏輯
```
連續輸入：
1. "我很累"（正常 Level 2）
2. "對了我想問別的"（reset_signal=true，但回應仍用 Level 2 第二句模板）
```

### 回退方式
1. 移除 `RESET_SIGNAL_KEYWORDS`
2. 移除 `detect_reset_signal` 方法
3. 移除 metadata 中 `reset_signal` 欄位
4. 移除 support.py 中的調用

### 通過條件
- [ ] Reset signal 能正確檢測
- [ ] 不影響任何現有 Level 2 邏輯
- [ ] metadata 正確包含 reset_signal
- [ ] 所有 Phase 0 測試案例仍通過

---

## Phase 2：TST Marker Metadata

### 目的
1. 讓後端可以回傳 TST marker，但不影響使用者體驗
2. 建立 TST marker 基礎架構
3. 只在 dev/debug mode 觀察 marker 分配

### 允許修改的檔案
- `app/schemas/ai.py`（ResponseMetadata 新增 TST 相關欄位）
- `app/services/ai/session_store.py`（SessionContext 新增 TST 欄位）
- `app/api/v1/ai/support.py`（計算並保存 TST marker）

### 禁止做的事
- **不在一般 UI 顯示 marker**
- **不讓 marker 決定回應內容**
- **不把 marker 說給使用者**
- **不修改 response_builder.py 邏輯**
- **不接入完整 TST router**

### 實作內容

#### 1. Metadata 擴充
```python
# schemas/ai.py ResponseMetadata
tst_marker: Optional[str] = Field(None, description="TST 暫時迷宮標記")
marker_confidence: Optional[float] = Field(None, description="標記信心度")
marker_reason: Optional[str] = Field(None, description="標記原因")
previous_tst_marker: Optional[str] = Field(None, description="上一輪標記")
```

#### 2. SessionContext 擴充
```python
# session_store.py SessionContext
tst_markers: List[str] = field(default_factory=list)  # 最近3次標記

@property
def previous_tst_marker(self) -> Optional[str]:
    return self.tst_markers[-1] if len(self.tst_markers) > 0 else None
```

#### 3. 最小標記邏輯
```python
# support.py（新增函數）
def calculate_minimal_tst_marker(
    current_level: int,
    current_state: str,
    turn_count: int,
    reset_signal: bool,
    has_strong_negation: bool
) -> Tuple[str, float, str]:
    """最小 TST marker 計算"""
```

### 測試方式

#### 測試案例 1：基礎 marker 分配
```
輸入："我今天真的很累"
預期：metadata.tst_marker = "stay"
```

#### 測試案例 2：Reset signal marker
```
輸入："對了我想問別的"
預期：metadata.tst_marker = "reset"
```

#### 測試案例 3：Risk signal marker
```
輸入："我覺得自己很沒用"
預期：metadata.tst_marker = "risk"
```

### 回退方式
1. 移除 metadata 中所有 TST 欄位
2. 移除 SessionContext 中 tst_markers
3. 移除 support.py 中 TST marker 計算

### 通過條件
- [ ] TST marker 能正確分配到六種類型
- [ ] marker_confidence 在合理範圍（0.1-0.9）
- [ ] 不影響使用者看到的任何內容
- [ ] 所有前階段測試案例仍通過

---

## Phase 3：TST Marker 最小判斷邏輯

### 目的
1. 建立完整但最小的 TST marker 判斷規則
2. 使用現有後端資料做標記決策
3. 實作標記調整規則（維持/升級/退回/覆蓋/重開）

### 允許修改的檔案
- `app/api/v1/ai/support.py`（完整 TST marker 判斷邏輯）
- `app/core/ai_config.py`（TST 判斷規則配置）

### 禁止做的事
- **不接 AI**
- **不接資料庫**
- **不用 H-Type**
- **不新增複雜 state**
- **不直接改 response**
- **不新增檔案（如 tst_detector.py）**

### 實作內容

#### 1. TST 判斷規則配置
```python
# ai_config.py
TST_MARKER_RULES = {
    "priority_order": ["risk", "reset", "rest", "stay", "transform", "organize"],
    "state_mapping": {
        "疲勞中": ["stay", "rest"],
        "拉扯中": ["organize"],
        "成長中": ["transform"],
        "痛苦中": ["risk"]
    },
    "turn_threshold": 3
}
```

#### 2. 標記調整規則
- 維持：連續相同狀態 → 維持原標記
- 升級：Risk > Reset > Rest > Stay > Transform > Organize
- 退回：能量恢復 → 降級標記
- 覆蓋：高優先級直接覆蓋低優先級
- 重開：明確 reset signal → 重置為 reset

#### 3. 完整判斷邏輯
使用 `docs/TST_MARKER_DECISION_RULES_V01.md` 規則。

### 測試方式

#### 測試案例 1：優先順序測試
```
輸入："我覺得自己很沒用，對了我想問別的"
預期：tst_marker = "risk"（Risk 優先於 Reset）
```

#### 測試案例 2：標記調整測試
```
session 連續輸入：
1. "我很累" → stay
2. "整個人空掉" → stay（維持）
3. "我想整理一下" → organize（升級）
```

#### 測試案例 3：六種標記完整測試
每種標記都要有對應測試案例。

### 回退方式
1. 移除 `TST_MARKER_RULES`
2. 恢復 Phase 2 的簡化標記邏輯
3. 移除標記調整相關程式碼

### 通過條件
- [ ] 六種標記都能正確觸發
- [ ] 優先順序規則正確執行
- [ ] 標記調整規則正確執行
- [ ] 複雜測試案例通過（如同時觸發多種標記）
- [ ] 所有前階段測試案例仍通過

---

## Phase 4：TST Response Mode（選擇性）

### 目的
1. 讓 TST marker 開始影響第4句後的回應
2. 先只接入低風險的回應模式
3. 建立 TST response mode 基礎框架

### 允許修改的檔案
- `app/services/ai/response_builder.py`（新增 TST response mode）
- `app/core/ai_config.py`（TST response templates）

### 禁止做的事
- **不一次接入全部六種回應模式**
- **不重構現有 response_builder**
- **不修改前三句邏輯**
- **Risk 模式必須與 Level 3 協調，避免衝突**

### 實作優先順序
1. **第一批：Stay / Rest / Reset**（低風險）
2. **第二批：Organize / Transform**（中風險）
3. **第三批：Risk**（高風險，需要特別小心）

### 實作內容

#### 1. TST Response Templates
```python
# ai_config.py
TST_RESPONSE_TEMPLATES = {
    "stay": [
        "先不用急著整理，我在。",
        "那我們先停一下也可以。"
    ],
    "rest": [
        "那今天先不用再逼自己了。",
        "有時候，先停下來就是最小的一步。"
    ],
    "reset": [
        "好，我們可以先看這件新的。",
        "你想先從哪一小段開始說？"
    ]
}
```

#### 2. Response Builder 擴充
```python
# response_builder.py
def _build_level2_response_with_tst(
    self, 
    analysis: Dict[str, Any], 
    user_input: str, 
    turn_count: int,
    tst_marker: Optional[str] = None
) -> ResponseContent:
```

### 測試方式

#### 測試案例 1：Stay 模式承接
```
session 連續輸入：
1-3. 正常三句承接
4. "還是很累" + tst_marker="stay"
預期：使用 Stay 承接模式回應
```

#### 測試案例 2：Reset 模式承接
```
第4句："對了我想問別的" + tst_marker="reset"
預期：使用 Reset 重開模式回應
```

### 回退方式
1. 移除 `TST_RESPONSE_TEMPLATES`
2. 移除 `_build_level2_response_with_tst`
3. 恢復原本第4句後使用第3句模板的邏輯

### 通過條件
- [ ] Stay / Rest / Reset 三種模式正確承接
- [ ] 不影響前三句邏輯
- [ ] 第4句後回應符合 `TST_RESPONSE_MODE_V01.md` 規格
- [ ] 所有前階段測試案例仍通過

---

## 整體測試流程

### 端到端測試案例

#### 測試案例 1：完整 Stay 流程
```
session_id: "test-stay-001"
1. "我今天真的很累" → Level 2 第一句
2. "整個人有點空掉" → Level 2 第二句  
3. "什麼都不太想做" → Level 2 第三句
4. "還是很累" → TST Stay 承接模式
```

#### 測試案例 2：Reset 觸發流程
```
session_id: "test-reset-001"
1. "我很累"
2. "對了我想問別的事" → TST Reset 模式
```

#### 測試案例 3：Risk 優先處理
```
session_id: "test-risk-001"
1. "我覺得自己很沒用" → Level 3 + TST Risk 標記
```

### 回退總方案

如果任何階段出現問題，提供完整回退路徑：

1. **Phase 4 → Phase 3**：移除 TST response mode，保留 marker 判斷
2. **Phase 3 → Phase 2**：簡化為基礎 marker，移除複雜判斷邏輯  
3. **Phase 2 → Phase 1**：移除 TST metadata，保留 reset_signal
4. **Phase 1 → Phase 0**：移除所有 TST 相關功能
5. **Phase 0**：回到純 Level 2 三句承接

## 最終結論與建議

### 是否建議 Step 7 第一刀只做 Phase 1：reset_signal detector？

**強烈建議。**

### 理由

1. **最大價值**：Reset signal 是目前唯一完全缺失的功能
2. **最低風險**：只做檢測，不影響任何現有邏輯
3. **可獨立驗證**：reset_signal 可以直接在 metadata 觀察
4. **為後續鋪路**：是 TST marker 的必要基礎

### 建議執行順序

1. **先做 Phase 0**：確認基線，建立測試基準
2. **再做 Phase 1**：專注解決 reset_signal 檢測
3. **觀察一段時間**：確認 reset_signal 檢測準確度
4. **再決定是否進入 Phase 2**

### 停止條件

如果任何 Phase 出現以下情況，立即停止並回退：

- 破壞現有 Level 2 三句承接功能
- reset_signal 誤判率過高（>20%）
- 對系統穩定性造成影響
- 開發複雜度超出預期

**最重要原則：寧可不做 TST，也不能破壞現有功能。**

---

*文件版本：v0.1*  
*最後更新：2026-05-01*  
*狀態：實作規劃 - 等待 Phase 0 確認*