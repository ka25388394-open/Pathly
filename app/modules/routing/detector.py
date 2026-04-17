"""整合的信號和模式檢測器

合併 pattern_detector 和 signal_detector 的功能
"""

from __future__ import annotations

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class DetectionResult:
    """檢測結果"""
    detected_patterns: List[str]
    signal_strength: float
    confidence: float
    detected_signals: Dict[str, float]


class IntegratedDetector:
    """整合的檢測器 - 合併模式和信號檢測"""

    def __init__(self):
        self.pattern_weights = {
            "emotional_expression": 0.8,
            "task_oriented": 0.7,
            "reflective_inquiry": 0.6,
            "action_planning": 0.9
        }

    def detect(self, text: str, context: Optional[Dict[str, Any]] = None) -> DetectionResult:
        """檢測文本中的模式和信號"""
        patterns = self._detect_patterns(text)
        signals = self._detect_signals(text, context)

        # 計算整體信號強度
        signal_strength = sum(signals.values()) / len(signals) if signals else 0.0
        confidence = min(signal_strength * 1.2, 1.0)  # 置信度上限為1.0

        return DetectionResult(
            detected_patterns=patterns,
            signal_strength=signal_strength,
            confidence=confidence,
            detected_signals=signals
        )

    def _detect_patterns(self, text: str) -> List[str]:
        """檢測文本模式"""
        patterns = []
        text_lower = text.lower()

        # 情感表達模式
        emotional_keywords = ["感覺", "覺得", "心情", "情緒", "難過", "開心", "焦慮"]
        if any(word in text for word in emotional_keywords):
            patterns.append("emotional_expression")

        # 任務導向模式
        task_keywords = ["想要", "計劃", "目標", "完成", "達成"]
        if any(word in text for word in task_keywords):
            patterns.append("task_oriented")

        # 反思探詢模式
        inquiry_keywords = ["為什麼", "怎麼", "如何", "是否", "可能"]
        if any(word in text for word in inquiry_keywords):
            patterns.append("reflective_inquiry")

        # 行動規劃模式
        action_keywords = ["下一步", "接下來", "開始", "嘗試", "改變"]
        if any(word in text for word in action_keywords):
            patterns.append("action_planning")

        return patterns

    def _detect_signals(self, text: str, context: Optional[Dict[str, Any]]) -> Dict[str, float]:
        """檢測各種信號強度"""
        signals = {}

        # 長度信號
        text_length = len(text)
        if text_length > 100:
            signals["lengthy_input"] = min(text_length / 500, 1.0)
        else:
            signals["brief_input"] = 1.0 - (text_length / 100)

        # 問號密度
        question_marks = text.count("？") + text.count("?")
        if question_marks > 0:
            signals["question_density"] = min(question_marks / 3, 1.0)

        # 情感強度
        strong_emotions = ["非常", "極度", "超級", "特別", "真的很"]
        emotion_count = sum(1 for word in strong_emotions if word in text)
        if emotion_count > 0:
            signals["emotional_intensity"] = min(emotion_count / 2, 1.0)

        # 上下文連續性
        if context and context.get("previous_interactions", 0) > 0:
            signals["context_continuity"] = min(context["previous_interactions"] / 5, 1.0)

        return signals