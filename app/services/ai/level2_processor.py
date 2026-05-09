"""Level 2 輕量處理模組 - 陪伴式整理與釐清"""

from __future__ import annotations

import random
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class Level2ProcessResult:
    """Level 2 處理結果"""
    acknowledge: Dict[str, Any]
    clarify: Dict[str, Any]
    direction: Dict[str, Any]
    summary: Dict[str, Any]
    processing_flow: List[str]
    # 新增：人類狀態解析結果
    human_state: Dict[str, Any]


class Level2Processor:
    """Level 2 陪伴式整理處理器 - 三段式流程"""

    def __init__(self):
        self.acknowledge_templates = self._init_acknowledge_templates()
        self.clarify_templates = self._init_clarify_templates()
        self.direction_templates = self._init_direction_templates()
        # 初始化狀態解析模板
        self.state_patterns = self._init_state_patterns()

    def process(self, user_input: str, analysis_data: Dict[str, Any]) -> Level2ProcessResult:
        """
        執行 Level 2 三段式處理流程

        Args:
            user_input: 用戶輸入
            analysis_data: 從 level_detector 來的分析結果

        Returns:
            Level2ProcessResult: 完整的處理結果
        """
        # 步驟 1: 溫和承接
        acknowledge_result = self.step1_acknowledge(user_input, analysis_data)

        # 步驟 2: 陪伴釐清
        clarify_result = self.step2_clarify(user_input, analysis_data, acknowledge_result)

        # 步驟 3: 輕柔引導
        direction_result = self.step3_direction(user_input, analysis_data, clarify_result)

        # 新增：人類狀態解析
        human_state_result = self.parse_human_state(user_input, analysis_data)

        # 整合總結
        summary = self._create_summary(acknowledge_result, clarify_result, direction_result)

        return Level2ProcessResult(
            acknowledge=acknowledge_result,
            clarify=clarify_result,
            direction=direction_result,
            summary=summary,
            processing_flow=["acknowledge", "clarify", "direction"],
            human_state=human_state_result
        )

    def step1_acknowledge(self, user_input: str, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        步驟 1: 溫和承接
        - 承認對方的困擾
        - 表達理解與支持
        """
        keywords = analysis_data.get("keywords", [])

        # 根據關鍵字選擇承接方式
        acknowledge_type = self._detect_acknowledge_type(keywords)
        template = random.choice(self.acknowledge_templates[acknowledge_type])

        return {
            "type": acknowledge_type,
            "message": template,
            "validation": "你的感受是可以理解的",
            "support": "我們可以一起慢慢整理",
            "tone": "溫和理解"
        }

    def step2_clarify(self, user_input: str, analysis_data: Dict[str, Any], acknowledge_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        步驟 2: 陪伴釐清
        - 幫助整理混亂的感受
        - 溫和地協助梳理
        """
        keywords = analysis_data.get("keywords", [])

        # 檢測需要釐清的類型
        clarify_type = self._detect_clarify_type(keywords, user_input)
        template = random.choice(self.clarify_templates[clarify_type])

        return {
            "clarify_type": clarify_type,
            "approach": template,
            "gentle_inquiry": "想要試著一起理一理嗎？",
            "no_pressure": "沒有壓力，可以慢慢來",
            "companionship": "我會陪著你一起整理"
        }

    def step3_direction(self, user_input: str, analysis_data: Dict[str, Any], clarify_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        步驟 3: 輕柔引導
        - 提供溫和的方向建議
        - 不急著解決，只是陪伴
        """
        clarify_type = clarify_data["clarify_type"]

        # 根據釐清類型選擇引導方式
        direction_type = self._select_direction_type(clarify_type)
        template = random.choice(self.direction_templates[direction_type])

        return {
            "type": direction_type,
            "guidance": template,
            "gentle_steps": self._generate_gentle_steps(direction_type),
            "companionship": "我會陪著你，不需要急",
            "flexibility": "這些只是建議，你可以選擇適合的"
        }

    def parse_human_state(self, user_input: str, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        人類狀態解析引擎 - MVP Mock 版本

        根據用戶輸入解析：
        - domain: 生活領域 (工作/關係/學習/健康/其他)
        - state: 當前狀態 (困惑/壓力/迷茫/疲憊/焦慮)
        - drive: 內在驅動 (想理解/想改變/想休息/想突破/想陪伴)
        - message: 兩句話回應
        """
        keywords = analysis_data.get("keywords", [])
        user_input_lower = user_input.lower()

        # Domain 判斷 (生活領域)
        domain = self._detect_domain(user_input_lower, keywords)

        # State 判斷 (當前狀態)
        state = self._detect_state(user_input_lower, keywords)

        # Drive 判斷 (內在驅動)
        drive = self._detect_drive(user_input_lower, keywords)

        # 生成回應訊息
        message = self._generate_state_message(domain, state, drive)

        return {
            "domain": domain,
            "state": state,
            "drive": drive,
            "message": message
        }

    def _detect_domain(self, user_input: str, keywords: List[str]) -> str:
        """檢測生活領域"""
        if any(word in user_input for word in ["work", "job", "工作", "上班", "同事", "老闆", "專案"]):
            return "工作"
        elif any(word in user_input for word in ["relationship", "friend", "關係", "朋友", "家人", "伴侶"]):
            return "關係"
        elif any(word in user_input for word in ["study", "school", "學習", "學校", "考試", "成績"]):
            return "學習"
        elif any(word in user_input for word in ["health", "body", "健康", "身體", "睡眠", "運動"]):
            return "健康"
        else:
            return "生活"

    def _detect_state(self, user_input: str, keywords: List[str]) -> str:
        """檢測當前狀態"""
        if any(word in user_input for word in ["confused", "困惑", "不知道", "搞不懂"]):
            return "困惑"
        elif any(word in user_input for word in ["pressure", "stress", "壓力", "壓迫", "緊張"]):
            return "壓力"
        elif any(word in user_input for word in ["lost", "迷茫", "沒方向", "不知道要"]):
            return "迷茫"
        elif any(word in user_input for word in ["tired", "exhausted", "累", "疲憊", "沒力", "空掉", "有點空掉", "不太想做", "什麼都不太想做", "有點空", "不太想動", "沒什麼力氣", "不想動"]):
            return "疲憊"
        elif any(word in user_input for word in ["anxious", "worried", "焦慮", "擔心", "不安"]):
            return "焦慮"
        else:
            return "混亂"

    def _detect_drive(self, user_input: str, keywords: List[str]) -> str:
        """檢測內在驅動"""
        if any(word in user_input for word in ["understand", "know", "想了解", "想知道", "理解"]):
            return "想理解"
        elif any(word in user_input for word in ["change", "improve", "想改變", "想進步", "想突破"]):
            return "想改變"
        elif any(word in user_input for word in ["rest", "break", "想休息", "想放鬆", "想停下"]):
            return "想休息"
        elif any(word in user_input for word in ["breakthrough", "growth", "想突破", "想成長", "想進步"]):
            return "想突破"
        else:
            return "想陪伴"

    def _generate_state_message(self, domain: str, state: str, drive: str) -> str:
        """根據解析結果生成兩句話回應"""
        messages = {
            ("工作", "壓力"): "工作上的壓力確實不容易處理。我們可以一起想想有什麼地方能夠調整。",
            ("工作", "疲憊"): "工作讓人感到疲憊是很常見的。也許可以先從照顧自己的狀態開始。",
            ("關係", "困惑"): "人際關係有時候真的很複雜。讓我們慢慢理一理你的感受。",
            ("關係", "焦慮"): "關係中的焦慮感我能理解。這些擔心的確很真實，想說說是什麼讓你這麼在意？",
            ("學習", "迷茫"): "學習路上感到迷茫很正常。我們可以一步步找到適合你的方向。",
            ("健康", "疲憊"): "身心的疲憊需要被好好照顧。讓我們想想什麼對你來說最重要。",
        }

        # 優先使用特定組合，否則用通用回應
        key = (domain, state)
        if key in messages:
            return messages[key]
        else:
            return f"在{domain}方面感到{state}是可以理解的。我們可以一起慢慢整理這些感受。"

    def _create_summary(self, acknowledge: Dict, clarify: Dict, direction: Dict) -> Dict[str, Any]:
        """創建整合總結"""
        return {
            "main_message": f"{acknowledge['message']} {clarify['approach'][:30]}...",
            "key_approach": clarify['gentle_inquiry'],
            "light_direction": direction['guidance'][:40] + "...",
            "overall_tone": "陪伴式整理與釐清",
            "next_step": "繼續溫和地整理或深入討論"
        }

    # === 初始化模板 ===

    def _init_acknowledge_templates(self) -> Dict[str, List[str]]:
        return {
            "stress_acknowledge": [
                "聽起來你最近遇到了一些挑戰",
                "感受到你現在的壓力了",
                "這種感覺確實不太容易"
            ],
            "confusion_acknowledge": [
                "看起來有些事情讓你感到困惑",
                "感覺你現在有點搞不清楚狀況",
                "這種混亂的感覺我能理解"
            ],
            "overwhelm_acknowledge": [
                "感覺事情有點多，讓人喘不過氣",
                "聽起來你現在要處理的事情不少",
                "這種被淹沒的感覺確實不好受"
            ]
        }

    def _init_clarify_templates(self) -> Dict[str, List[str]]:
        return {
            "emotional_clarify": [
                "我們可以先試著理一理這些感受",
                "也許可以慢慢把這些情緒分開來看",
                "讓我們溫和地整理一下你的感覺"
            ],
            "situational_clarify": [
                "我們可以一步步把情況梳理清楚",
                "也許可以先從最主要的事情開始整理",
                "讓我們試著把這些事情分類整理一下"
            ],
            "decision_clarify": [
                "我們可以一起看看有哪些選擇",
                "也許可以把不同的選項列出來看看",
                "讓我們溫和地整理一下你的想法"
            ]
        }

    def _init_direction_templates(self) -> Dict[str, List[str]]:
        return {
            "gentle_exploration": [
                "也許我們可以先從一個小角度開始探索",
                "可以選一個感覺比較容易的地方先談談",
                "我們可以慢慢地、一點一點來理解"
            ],
            "light_structuring": [
                "也許可以試著把這些事情簡單分個類",
                "我們可以溫和地給這些感受一些順序",
                "試著從最重要的或最急的開始整理"
            ],
            "supportive_pacing": [
                "不需要一次把所有事情都想清楚",
                "我們可以慢慢來，一次處理一件事",
                "給自己一些時間，慢慢整理就好"
            ]
        }

    # === 檢測與選擇邏輯 ===

    def _detect_acknowledge_type(self, keywords: List[str]) -> str:
        """檢測承接類型"""
        if any(word in keywords for word in ["累", "壓力", "忙", "疲憊", "tired", "stress"]):
            return "stress_acknowledge"
        elif any(word in keywords for word in ["困惑", "迷茫", "不知道", "confused", "unsure"]):
            return "confusion_acknowledge"
        else:
            return "overwhelm_acknowledge"

    def _detect_clarify_type(self, keywords: List[str], user_input: str) -> str:
        """檢測釐清類型"""
        if any(word in keywords for word in ["感覺", "情緒", "心情", "feel", "emotion"]):
            return "emotional_clarify"
        elif any(word in keywords for word in ["選擇", "決定", "該怎麼", "怎麼辦", "decide", "choice"]):
            return "decision_clarify"
        else:
            return "situational_clarify"

    def _select_direction_type(self, clarify_type: str) -> str:
        """選擇引導類型"""
        direction_map = {
            "emotional_clarify": "gentle_exploration",
            "situational_clarify": "light_structuring",
            "decision_clarify": "supportive_pacing"
        }
        return direction_map.get(clarify_type, "gentle_exploration")

    def _generate_gentle_steps(self, direction_type: str) -> List[str]:
        """生成溫和步驟"""
        steps = {
            "gentle_exploration": [
                "先從最有感覺的地方開始說",
                "選一個比較容易談的角度",
                "不用擔心說得不夠完整"
            ],
            "light_structuring": [
                "把事情簡單地分成幾個部分",
                "先處理比較急迫的事情",
                "一次專注在一件事上"
            ],
            "supportive_pacing": [
                "給自己足夠的時間思考",
                "不需要立刻有答案",
                "可以先休息一下再決定"
            ]
        }
        return steps.get(direction_type, ["慢慢來就好"])

    def _init_state_patterns(self) -> Dict[str, List[str]]:
        """初始化狀態解析模式（預留給未來擴展）"""
        return {
            "domain_keywords": ["工作", "關係", "學習", "健康", "生活"],
            "state_keywords": ["困惑", "壓力", "迷茫", "疲憊", "焦慮"],
            "drive_keywords": ["想理解", "想改變", "想休息", "想突破", "想陪伴"]
        }