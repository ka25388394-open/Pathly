"""回應建構器 - core-pathly-main"""

import random
from typing import Dict, Any, Union, List
from app.core.ai_config import RESPONSE_TEMPLATES
from app.schemas.ai import ResponseContent, Level3Response
from app.services.ai.level3_processor import Level3Processor
from app.services.ai.level2_processor import Level2Processor
from app.services.ai.state_classifier import classify_basic_state


class ResponseBuilder:
    """AI 回應建構器"""

    def __init__(self):
        self.templates = RESPONSE_TEMPLATES
        self.level2_processor = Level2Processor()
        self.level3_processor = Level3Processor()

    def build_response(self, level: int, analysis: Dict[str, Any], user_input: str = "", turn_count: int = 0) -> Union[ResponseContent, Level3Response]:
        """
        根據等級和分析結果建構回應

        Args:
            level: 等級 (1-3)
            analysis: 分析結果
            user_input: 用戶輸入（Level 3 需要）
            turn_count: 對話輪次（Level 2 session 使用）

        Returns:
            ResponseContent 或 Level3Response
        """
        if level == 3:
            return self._build_level3_response(analysis, user_input)
        elif level == 2:
            return self._build_level2_response(analysis, user_input, turn_count)
        else:
            return self._build_standard_response(level, analysis)

    def _build_standard_response(self, level: int, analysis: Dict[str, Any]) -> ResponseContent:
        """建構標準回應（Level 1 & 2）"""
        template = self.templates[f"level_{level}"]

        # 隨機選擇訊息
        message = random.choice(template["messages"])

        # 獲取建議
        suggestions = template["suggestions"].copy()

        # 根據分析結果生成後續問題
        next_questions = self._generate_next_questions(level, analysis)

        return ResponseContent(
            message=message,
            suggestions=suggestions,
            next_questions=next_questions
        )

    def _build_level2_response(self, analysis: Dict[str, Any], user_input: str, turn_count: int = 0) -> ResponseContent:
        """建構 Level 2 回應（支援三句順流承接）"""

        # 基礎狀態分類
        state_result = classify_basic_state(user_input)

        # 根據 turn_count 選擇承接模板
        if turn_count <= 1:
            # 第一句：使用原本邏輯
            main_message = state_result["message"]
        elif turn_count == 2:
            # 第二句：承接模板
            main_message = self._get_second_turn_template(state_result["state"])
        else:  # turn_count >= 3
            # 第三句：STL-lite 語言鬆動模板
            main_message = self._get_third_turn_template(state_result["state"])

        # 簡化建議（不改原邏輯）
        suggestions = [
            "先從最有感覺的地方開始說",
            "不用擔心說得不夠完整",
            "我們可以慢慢來"
        ]

        # 簡化的後續問題
        next_questions = [
            "想多聊聊這個部分嗎？",
            "還有什麼想分享的？"
        ]

        return ResponseContent(
            message=main_message,
            suggestions=suggestions,
            next_questions=next_questions,
            domain=state_result["domain"],
            state=state_result["state"],
            drive=state_result["drive"]
        )

    def _generate_level2_questions(self, clarify_type: str) -> List[str]:
        """為 Level 2 生成適當的後續問題"""
        questions_map = {
            "emotional_clarify": [
                "哪種感受對你來說最明顯？",
                "想先從哪個情緒開始整理？"
            ],
            "situational_clarify": [
                "哪件事情對你來說比較急迫？",
                "想先談談哪個部分？"
            ],
            "decision_clarify": [
                "有哪些選擇是你已經想過的？",
                "什麼因素對你的決定最重要？"
            ]
        }
        return questions_map.get(clarify_type, [
            "想從哪個角度開始整理？",
            "什麼對你來說感覺最重要？"
        ])

    def _build_level3_response(self, analysis: Dict[str, Any], user_input: str) -> Level3Response:
        """建構 Level 3 回應（使用深度處理模組）"""

        # 使用 Level 3 深度處理器
        process_result = self.level3_processor.process(user_input, analysis)

        # 提取主要訊息
        main_message = process_result.summary["main_message"]

        # 整合建議（來自 action 步驟）
        suggestions = process_result.action["small_steps"]

        # 後續問題
        next_questions = [
            "你現在感覺最困難的是什麼？",
            "有什麼是我可以陪伴你的嗎？"
        ]

        # 結構化回應內容
        empathy = [
            process_result.empathy["message"],
            process_result.empathy["validation"]
        ]

        awareness = [
            process_result.awareness["reflection"],
            process_result.awareness["pattern_insight"]
        ]

        reframe = [
            process_result.reframe["new_perspective"],
            process_result.reframe["possibility"]
        ]

        action = [
            process_result.action["guidance"],
            process_result.action["self_care"]
        ]

        return Level3Response(
            message=main_message,
            suggestions=suggestions,
            next_questions=next_questions,
            empathy=empathy,
            awareness=awareness,
            reframe=reframe,
            action=action
        )

    def _generate_next_questions(self, level: int, analysis: Dict[str, Any]) -> list:
        """根據分析結果生成後續問題"""
        keywords = analysis.get("keywords", [])
        needs_help = analysis.get("needs_help", False)

        if level == 1:
            return [
                "今天有什麼特別的事情嗎？",
                "想聊聊你最近的心情嗎？"
            ]

        elif level == 2:
            questions = []

            # 根據關鍵字定制問題
            if any(kw in keywords for kw in ["累", "疲憊", "壓力"]):
                questions.extend([
                    "是工作上的壓力比較大嗎？",
                    "什麼事情讓你感到特別累？"
                ])

            if any(kw in keywords for kw in ["困惑", "迷茫", "不知道"]):
                questions.extend([
                    "能描述一下讓你困惑的情況嗎？",
                    "是在哪方面感到不確定？"
                ])

            if needs_help:
                questions.append("我可以怎麼幫助你？")

            # 如果沒有特定問題，使用預設問題
            if not questions:
                questions = [
                    "可以多告訴我一些嗎？",
                    "什麼讓你有這種感受？"
                ]

            return questions[:2]  # 最多返回 2 個問題

        else:  # level == 3
            return [
                "你現在感覺最困難的是什麼？",
                "有什麼是我可以陪伴你的嗎？"
            ]

    def _get_second_turn_template(self, state: str) -> str:
        """第二句承接模板 - 根據狀態選擇"""

        # A 情緒承接模板
        emotion_templates = [
            "這種累是今天特別明顯嗎？",
            "今天哪一段最讓你覺得撐著？"
        ]

        # B 混亂承接模板
        confusion_templates = [
            "沒關係，想到什麼說什麼就好。",
            "從哪一塊說起你比較自在？"
        ]

        # C 任務壓力模板
        task_templates = [
            "哪一件事現在壓得最重？",
            "要不要先從一個最卡的開始？"
        ]

        # D 自我觀察模板
        observation_templates = [
            "最近這種情況有變多嗎？",
            "你想先從剛剛那個發現說一點嗎？"
        ]

        # 根據 state 選擇模板
        if state in ["疲勞中", "壓力中"]:
            return random.choice(emotion_templates)
        elif state in ["混亂中", "迷茫中", "拉扯中"]:
            return random.choice(confusion_templates)
        elif state in ["工作", "任務"]:  # 工作相關
            return random.choice(task_templates)
        elif "模式" in str(state) or "反覆" in str(state):
            return random.choice(observation_templates)
        else:
            # Fallback to A 模式
            return random.choice(emotion_templates)

    def _get_third_turn_template(self, state: str) -> str:
        """第三句 STL-lite 語言鬆動模板"""

        # A 情緒承接 STL-lite
        emotion_stl = [
            "那種感覺比較像身體累，還是心也有點在撐？",
            "剛剛你說的那種累，比較像一直撐著，還是真的已經沒力了？"
        ]

        # B 混亂狀態 STL-lite
        confusion_stl = [
            "剛剛那些裡面，有沒有一件是最近一直在想的？",
            "如果只留一件在腦袋裡，會是哪一個？"
        ]

        # C 任務壓力 STL-lite
        task_stl = [
            "那件最卡的，是卡在開始，還是做到一半？",
            "比較難的是決定怎麼做，還是根本不想碰？"
        ]

        # D 自我觀察 STL-lite
        observation_stl = [
            "你剛剛說「每次」，是最近特別明顯，還是真的一直都這樣？",
            "那個狀態出現時，比較像卡住，還是一直重複？"
        ]

        # 根據 state 選擇 STL-lite 模板
        if state in ["疲勞中", "壓力中"]:
            return random.choice(emotion_stl)
        elif state in ["混亂中", "迷茫中", "拉扯中"]:
            return random.choice(confusion_stl)
        elif state in ["工作", "任務"]:
            return random.choice(task_stl)
        elif "模式" in str(state) or "反覆" in str(state):
            return random.choice(observation_stl)
        else:
            # Fallback to A 模式
            return random.choice(emotion_stl)