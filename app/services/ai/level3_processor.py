"""Level 3 深度處理模組 - 四段式心理整理流程"""

from __future__ import annotations

import random
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class Level3ProcessResult:
    """Level 3 處理結果"""
    empathy: Dict[str, Any]
    awareness: Dict[str, Any]
    reframe: Dict[str, Any]
    action: Dict[str, Any]
    summary: Dict[str, Any]
    processing_flow: List[str]


class Level3Processor:
    """Level 3 深度處理器 - 四段式流程"""

    def __init__(self):
        self.empathy_templates = self._init_empathy_templates()
        self.awareness_templates = self._init_awareness_templates()
        self.reframe_templates = self._init_reframe_templates()
        self.action_templates = self._init_action_templates()

    def process(self, user_input: str, analysis_data: Dict[str, Any]) -> Level3ProcessResult:
        """
        執行完整的 Level 3 四段式處理流程

        Args:
            user_input: 用戶輸入
            analysis_data: 從 level_detector 來的分析結果

        Returns:
            Level3ProcessResult: 完整的處理結果
        """
        # 步驟 1: 情緒承接
        empathy_result = self.step1_empathy(user_input, analysis_data)

        # 步驟 2: 狀態映照
        awareness_result = self.step2_awareness(user_input, analysis_data, empathy_result)

        # 步驟 3: 認知重構
        reframe_result = self.step3_reframe(user_input, analysis_data, awareness_result)

        # 步驟 4: 行動引導
        action_result = self.step4_action(user_input, analysis_data, reframe_result)

        # 整合總結
        summary = self._create_summary(empathy_result, awareness_result, reframe_result, action_result)

        return Level3ProcessResult(
            empathy=empathy_result,
            awareness=awareness_result,
            reframe=reframe_result,
            action=action_result,
            summary=summary,
            processing_flow=["empathy", "awareness", "reframe", "action"]
        )

    def step1_empathy(self, user_input: str, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        步驟 1: 情緒承接
        - 驗證感受的真實性
        - 表達理解與陪伴
        """
        keywords = analysis_data.get("keywords", [])
        emotion = analysis_data.get("emotion_detected", "")

        # 根據關鍵字選擇承接方式
        empathy_type = self._detect_empathy_type(keywords, emotion)
        template = random.choice(self.empathy_templates[empathy_type])

        return {
            "type": empathy_type,
            "message": template.format(emotion=emotion),
            "validation": "你的感受是真實且重要的",
            "presence": "我在這裡陪伴你",
            "tone": "溫暖接納"
        }

    def step2_awareness(self, user_input: str, analysis_data: Dict[str, Any], empathy_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        步驟 2: 狀態映照
        - 映照當下的內在狀態
        - 幫助覺察模式
        """
        keywords = analysis_data.get("keywords", [])

        # 檢測狀態模式
        pattern_type = self._detect_pattern_type(keywords, user_input)
        template = random.choice(self.awareness_templates[pattern_type])

        return {
            "pattern_type": pattern_type,
            "reflection": template,
            "current_state": "注意到你現在的狀態",
            "pattern_insight": self._generate_pattern_insight(pattern_type),
            "gentle_inquiry": "想要多分享一些你的感受嗎？"
        }

    def step3_reframe(self, user_input: str, analysis_data: Dict[str, Any], awareness_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        步驟 3: 認知重構
        - 提供不同角度的思考
        - 鬆動固化的想法
        """
        pattern_type = awareness_data["pattern_type"]

        # 根據模式類型選擇重構方式
        reframe_approach = self._select_reframe_approach(pattern_type)
        template = random.choice(self.reframe_templates[reframe_approach])

        return {
            "approach": reframe_approach,
            "new_perspective": template,
            "cognitive_shift": "也許我們可以從另一個角度來看",
            "possibility": self._generate_possibility(reframe_approach),
            "gentleness": "這些只是可能性，不需要急著接受"
        }

    def step4_action(self, user_input: str, analysis_data: Dict[str, Any], reframe_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        步驟 4: 行動引導
        - 提供溫和的行動方向
        - 強調小步驟和自我照顧
        """
        approach = reframe_data["approach"]

        # 生成適當的行動建議
        action_type = self._select_action_type(approach)
        template = random.choice(self.action_templates[action_type])

        return {
            "type": action_type,
            "guidance": template,
            "small_steps": self._generate_small_steps(action_type),
            "self_care": "記住照顧自己是最重要的",
            "support": "如果需要專業協助，尋求幫助是勇敢的選擇",
            "pacing": "可以慢慢來，不需要急"
        }

    def _create_summary(self, empathy: Dict, awareness: Dict, reframe: Dict, action: Dict) -> Dict[str, Any]:
        """創建整合總結"""
        return {
            "main_message": f"{empathy['message']} {reframe['new_perspective'][:30]}...",
            "key_insight": awareness['pattern_insight'],
            "gentle_direction": action['guidance'][:50] + "...",
            "overall_tone": "深度陪伴與溫和引導",
            "next_step": "繼續對話或尋求進一步支持"
        }

    # === 初始化模板 ===

    def _init_empathy_templates(self) -> Dict[str, List[str]]:
        return {
            "pain_validation": [
                "我感受到你現在很辛苦，這種痛苦是真實的",
                "你現在的感受我能理解，這確實很不容易",
                "這種痛苦的感覺是可以被理解的"
            ],
            "worthlessness_validation": [
                "聽到你這樣說自己，我的心也很痛",
                "你對自己這麼嚴苛，我想陪伴你",
                "這些自我否定的想法一定很折磨人"
            ],
            "crisis_validation": [
                "我聽見你的痛苦，你不是一個人",
                "現在感覺很絕望是可以理解的",
                "謝謝你願意分享這些，我會陪伴你"
            ]
        }

    def _init_awareness_templates(self) -> Dict[str, List[str]]:
        return {
            "self_criticism": [
                "注意到你對自己有很多嚴厲的評價",
                "覺察到內在有個很嚴苛的聲音",
                "看見你習慣用很重的標準來看自己"
            ],
            "hopelessness": [
                "感覺到你現在看不到出路",
                "注意到現在很難看見希望",
                "覺察到未來對你來說很模糊"
            ],
            "overwhelm": [
                "注意到你感覺被很多事情淹沒",
                "覺察到現在承受的東西很多很重",
                "看見你正在承載超出負荷的壓力"
            ]
        }

    def _init_reframe_templates(self) -> Dict[str, List[str]]:
        return {
            "compassion_shift": [
                "如果朋友遇到同樣的情況，你會怎麼對他說？",
                "也許可以用對待好朋友的方式來對待自己",
                "有沒有可能，你值得更溫柔的對待？"
            ],
            "perspective_expansion": [
                "這個困難也許是暫時的，即使現在看不到盡頭",
                "也許現在的感受，不等於永遠的真相",
                "困難的時刻，有時候也是成長的機會"
            ],
            "strength_recognition": [
                "能夠分享這些，本身就需要很大的勇氣",
                "撐到現在的你，其實很有力量",
                "願意尋求幫助，這本身就是智慧"
            ]
        }

    def _init_action_templates(self) -> Dict[str, List[str]]:
        return {
            "gentle_care": [
                "今天可以為自己做一件小小的好事",
                "也許可以從照顧基本需求開始",
                "給自己一些溫柔的時間和空間"
            ],
            "connection": [
                "考慮跟信任的人分享一些感受",
                "也許可以尋求專業的心理支持",
                "讓自己被理解和陪伴是重要的"
            ],
            "grounding": [
                "專注在當下這一刻，一次一個呼吸",
                "找一些能讓你感到安全的小事情",
                "建立一些簡單的日常節奏"
            ]
        }

    # === 檢測與選擇邏輯 ===

    def _detect_empathy_type(self, keywords: List[str], emotion: str) -> str:
        """根據關鍵字和情緒檢測承接類型"""
        if any(word in keywords for word in ["沒用", "廢物", "失敗", "worthless", "useless"]):
            return "worthlessness_validation"
        elif any(word in keywords for word in ["想死", "自殺", "結束", "suicide", "kill myself"]):
            return "crisis_validation"
        else:
            return "pain_validation"

    def _detect_pattern_type(self, keywords: List[str], user_input: str) -> str:
        """檢測狀態模式類型"""
        if any(word in keywords for word in ["沒用", "廢物", "失敗", "很爛"]):
            return "self_criticism"
        elif any(word in keywords for word in ["沒希望", "絕望", "hopeless"]):
            return "hopelessness"
        else:
            return "overwhelm"

    def _select_reframe_approach(self, pattern_type: str) -> str:
        """選擇重構方式"""
        approach_map = {
            "self_criticism": "compassion_shift",
            "hopelessness": "perspective_expansion",
            "overwhelm": "strength_recognition"
        }
        return approach_map.get(pattern_type, "compassion_shift")

    def _select_action_type(self, approach: str) -> str:
        """選擇行動類型"""
        action_map = {
            "compassion_shift": "gentle_care",
            "perspective_expansion": "grounding",
            "strength_recognition": "connection"
        }
        return action_map.get(approach, "gentle_care")

    def _generate_pattern_insight(self, pattern_type: str) -> str:
        """生成模式洞察"""
        insights = {
            "self_criticism": "內在批評的聲音並不等於真相",
            "hopelessness": "絕望感是暫時的，即使現在很真實",
            "overwhelm": "一次處理太多會讓人喘不過氣"
        }
        return insights.get(pattern_type, "每個人都值得理解和陪伴")

    def _generate_possibility(self, approach: str) -> str:
        """生成可能性思考"""
        possibilities = {
            "compassion_shift": "也許你值得更多的自我慈悲",
            "perspective_expansion": "困難可能是暫時的，改變是可能的",
            "strength_recognition": "你比自己想像的更有力量"
        }
        return possibilities.get(approach, "改變是可能的")

    def _generate_small_steps(self, action_type: str) -> List[str]:
        """生成小步驟建議"""
        steps = {
            "gentle_care": [
                "確保基本的吃飯和睡眠",
                "做一件讓你感到舒適的小事",
                "給自己一些不被打擾的時間"
            ],
            "connection": [
                "考慮向一個信任的人傳個訊息",
                "查詢心理諮商的資源",
                "加入支持性的社群或團體"
            ],
            "grounding": [
                "專注在五感的體驗",
                "做幾個深呼吸",
                "找一個安全舒適的地方待著"
            ]
        }
        return steps.get(action_type, ["一次只做一件小事"])