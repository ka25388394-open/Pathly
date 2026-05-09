"""人類狀態解析引擎 - 第3階段：AI Prompt 骨架"""

from typing import Dict, Any
import random


# ========== Prompt 模板結構 ==========
# 未來接 AI 時使用的完整 Prompt

STATE_ANALYSIS_PROMPT = """
你是 Pathly 的人類狀態解析專家。

## 任務
分析用戶輸入，返回結構化的狀態解析結果。

## 輸出格式
嚴格按照以下 JSON 格式回傳：
{
    "domain": "[關係/工作/生活/創作/挑戰]",
    "state": "[痛苦中/拉扯中/修復中/穩定中/成長中]",
    "drive": "[防衛型/追尋型/混合型]",
    "message": "[兩句話回應：第一句映照，第二句選擇問句]"
}

## 分析維度

### domain（生活領域）
- 關係：人際關係、家庭、伴侶、友情
- 工作：職場、事業、專業發展
- 生活：日常生活、健康、作息、環境
- 創作：藝術、寫作、設計、表達
- 挑戰：困難、目標、突破、成長

### state（當前狀態）
- 痛苦中：明顯的痛苦、受傷、創傷
- 拉扯中：矛盾、衝突、左右為難
- 修復中：療癒、調整、重建過程
- 穩定中：平衡、維持、鞏固狀態
- 成長中：學習、進步、發展、提升

### drive（內在驅動）
- 防衛型：保護、避免、防禦、安全
- 追尋型：主動追求、探索、改變
- 混合型：既想保護又想前進

## 語氣調整原則
- 痛苦中/防衛型：輕、慢、不推進
- 拉扯中/混合型：描述兩股力量
- 修復中/穩定中：幫助聚焦縮小
- 成長中/追尋型：微微往前引導

## 回應格式
第一句：映照用戶狀態
第二句：「你比較想先...還是...？」或「你現在比較卡的是...還是...？」

---

用戶輸入：{user_input}

請分析並回傳結構化結果：
"""


class StateEngine:
    """人類狀態解析引擎 - AI Prompt 版本"""

    def __init__(self, use_ai: bool = False):
        """
        初始化引擎

        Args:
            use_ai: 是否使用 AI（目前階段固定為 False）
        """
        self.use_ai = use_ai
        self.mock_responses = self._init_mock_responses()

    def generate_state_response_with_prompt(self, text: str) -> Dict[str, str]:
        """
        使用 Prompt 生成狀態解析回應

        Args:
            text: 用戶輸入文本

        Returns:
            Dict 包含 domain, state, drive, message
        """
        if self.use_ai:
            # 第3階段：目前不實作，保留接口
            return self._call_ai_with_prompt(text)
        else:
            # 第3階段：使用智能 mock（比 rule-based 更靈活）
            return self._generate_smart_mock_response(text)

    def _call_ai_with_prompt(self, text: str) -> Dict[str, str]:
        """
        未來階段：真正呼叫 AI 的方法

        TODO: 實作 AI 調用邏輯
        - 將 STATE_ANALYSIS_PROMPT 填入 user_input
        - 呼叫 OpenAI/Claude/Gemini API
        - 解析 JSON 回應
        - 驗證輸出格式
        """
        raise NotImplementedError("AI 調用將在未來階段實作")

    def _generate_smart_mock_response(self, text: str) -> Dict[str, str]:
        """
        智能 Mock 回應（比純 rule-based 更接近 AI 效果）

        使用更細緻的關鍵字匹配 + 隨機變化，
        模擬 AI 的多樣性回應
        """
        text_lower = text.lower()

        # 分析輸入特徵
        features = self._extract_text_features(text_lower)

        # 根據特徵選擇回應模板
        response_template = self._select_response_template(features)

        # 在模板基礎上增加變化
        final_response = self._add_variation(response_template, features)

        return final_response

    def _extract_text_features(self, text: str) -> Dict[str, Any]:
        """提取文本特徵（模擬 AI 的理解過程）"""
        features = {
            "pain_level": 0,
            "conflict_level": 0,
            "growth_intent": 0,
            "domain_signals": [],
            "emotional_intensity": "medium"
        }

        # 痛苦程度
        pain_words = ["痛苦", "受傷", "痛", "崩潰", "hurt", "pain", "傷心"]
        features["pain_level"] = sum(1 for word in pain_words if word in text)

        # 衝突程度
        conflict_words = ["矛盾", "困惑", "拉扯", "不知道", "糾結", "confused", "torn"]
        features["conflict_level"] = sum(1 for word in conflict_words if word in text)

        # 成長意圖
        growth_words = ["想要", "成長", "進步", "學習", "提升", "want", "grow", "improve"]
        features["growth_intent"] = sum(1 for word in growth_words if word in text)

        # 領域信號
        domain_signals = {
            "關係": ["關係", "朋友", "家人", "伴侶", "同事", "friend", "relationship"],
            "工作": ["工作", "職場", "事業", "專案", "work", "job", "career"],
            "生活": ["生活", "日常", "健康", "睡眠", "life", "daily"],
            "創作": ["創作", "寫作", "設計", "藝術", "create", "art", "design"],
            "挑戰": ["挑戰", "困難", "目標", "突破", "challenge", "goal"]
        }

        for domain, words in domain_signals.items():
            if any(word in text for word in words):
                features["domain_signals"].append(domain)

        return features

    def _select_response_template(self, features: Dict[str, Any]) -> Dict[str, str]:
        """根據特徵選擇回應模板"""

        # 優先判斷 state
        if features["pain_level"] >= 2:
            state = "痛苦中"
            drive = "防衛型"
        elif features["conflict_level"] >= 2:
            state = "拉扯中"
            drive = "混合型"
        elif features["growth_intent"] >= 2:
            state = "成長中"
            drive = "追尋型"
        elif features["growth_intent"] >= 1:
            state = "穩定中"
            drive = "追尋型"
        else:
            state = "修復中"
            drive = "混合型"

        # 判斷 domain
        if features["domain_signals"]:
            domain = features["domain_signals"][0]  # 取第一個匹配的
        else:
            domain = "生活"  # 預設

        # 根據 state/drive 組合生成 message
        message = self._generate_contextual_message(domain, state, drive, features)

        return {
            "domain": domain,
            "state": state,
            "drive": drive,
            "message": message
        }

    def _generate_contextual_message(self, domain: str, state: str, drive: str, features: Dict[str, Any]) -> str:
        """根據上下文生成 message（比固定模板更靈活）"""

        # 映照句（第一句）
        reflection_templates = {
            ("關係", "痛苦中"): [
                "關係中的痛苦感覺很沉重。",
                "這種關係上的痛苦很真實。",
                "感覺關係帶來的痛苦很深。"
            ],
            ("工作", "拉扯中"): [
                "工作上的兩難讓人很為難。",
                "感覺工作中有些矛盾的地方。",
                "工作上似乎有些左右為難。"
            ],
            ("生活", "成長中"): [
                "生活中的成長動力很明顯。",
                "感覺你在生活上想要一些改變。",
                "生活成長的意圖很清楚。"
            ]
        }

        # 選擇問句（第二句）
        choice_templates = {
            ("痛苦中", "防衛型"): [
                "你現在比較卡的是想保護自己，還是想面對痛苦？",
                "你現在比較卡的是想要遠離，還是想要療癒？"
            ],
            ("拉扯中", "混合型"): [
                "你比較想先理清内心的矛盾，還是先做個選擇？",
                "你比較想先探索兩邊的想法，還是先找個平衡點？"
            ],
            ("成長中", "追尋型"): [
                "你比較想先穩固現在的基礎，還是先嘗試新的可能？",
                "你比較想先深化目前的，還是先拓展新的？"
            ]
        }

        # 獲取模板
        reflection = reflection_templates.get((domain, state), [f"在{domain}方面感到{state}。"])[0]
        choice = choice_templates.get((state, drive), ["你比較想先聊聊感受，還是先想想方向？"])[0]

        return f"{reflection} {choice}"

    def _add_variation(self, template: Dict[str, str], features: Dict[str, Any]) -> Dict[str, str]:
        """在模板基礎上增加隨機變化（模擬 AI 的多樣性）"""

        # 目前保持模板不變，未來可以加入更多變化
        # 例如：根據情緒強度調整語氣、根據文本長度調整回應等

        return template

    def _init_mock_responses(self) -> Dict[str, Any]:
        """初始化 Mock 回應庫（預留）"""
        return {
            "fallback": {
                "domain": "生活",
                "state": "穩定中",
                "drive": "混合型",
                "message": "生活中感到穩定中。你比較想先維持現狀，還是先嘗試調整？"
            }
        }


# ========== 公用接口 ==========

def create_state_engine(use_ai: bool = False) -> StateEngine:
    """創建狀態解析引擎實例"""
    return StateEngine(use_ai=use_ai)


def generate_state_response_with_prompt(text: str, use_ai: bool = False) -> Dict[str, str]:
    """
    快捷函數：使用 Prompt 生成狀態解析回應

    Args:
        text: 用戶輸入
        use_ai: 是否使用真實 AI（目前固定 False）

    Returns:
        狀態解析結果
    """
    engine = create_state_engine(use_ai=use_ai)
    return engine.generate_state_response_with_prompt(text)


# ========== 測試函數 ==========

def test_state_engine():
    """測試狀態解析引擎"""
    print("=== 第3階段：AI 引擎骨架測試 ===\n")

    test_cases = [
        "關係中很痛苦想保護自己",
        "工作讓我很矛盾不知道怎麼選擇",
        "生活中想要成長和進步",
        "創作遇到困難想突破",
        "面對挑戰想要修復信心"
    ]

    for case in test_cases:
        result = generate_state_response_with_prompt(case)
        print(f"輸入: {case}")
        print(f"AI 引擎回應: {result}")
        print("---")


if __name__ == "__main__":
    test_state_engine()