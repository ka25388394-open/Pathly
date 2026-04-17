"""整合的模組評分系統

合併 module_scorer 和 assessment 的功能
"""

from __future__ import annotations

from typing import Dict, Any, List
from dataclasses import dataclass
from .detector import DetectionResult


@dataclass
class ModuleScore:
    """模組評分結果"""
    module_name: str
    score: float
    reasoning: str
    confidence: float


class IntegratedScorer:
    """整合評分器 - 為不同模組評分"""

    def __init__(self):
        self.module_weights = {
            "stl": {
                "emotional_expression": 0.9,
                "reflective_inquiry": 0.8,
                "lengthy_input": 0.6
            },
            "tst": {
                "task_oriented": 0.9,
                "action_planning": 0.8,
                "brief_input": 0.5
            },
            "dialogue": {
                "question_density": 0.8,
                "context_continuity": 0.9,
                "emotional_intensity": 0.7
            }
        }

    def score_modules(
        self,
        detection_result: DetectionResult,
        context: Dict[str, Any] = None
    ) -> List[ModuleScore]:
        """為所有模組評分"""
        scores = []

        for module_name, weights in self.module_weights.items():
            score = self._calculate_module_score(module_name, detection_result, weights)
            reasoning = self._generate_reasoning(module_name, detection_result, score)

            scores.append(ModuleScore(
                module_name=module_name,
                score=score,
                reasoning=reasoning,
                confidence=detection_result.confidence
            ))

        return sorted(scores, key=lambda x: x.score, reverse=True)

    def _calculate_module_score(
        self,
        module_name: str,
        detection_result: DetectionResult,
        weights: Dict[str, float]
    ) -> float:
        """計算單個模組的評分"""
        total_score = 0.0
        total_weight = 0.0

        # 基於檢測到的模式評分
        for pattern in detection_result.detected_patterns:
            if pattern in weights:
                weight = weights[pattern]
                total_score += weight * 1.0  # 檢測到的模式得滿分
                total_weight += weight

        # 基於信號強度評分
        for signal, strength in detection_result.detected_signals.items():
            if signal in weights:
                weight = weights[signal]
                total_score += weight * strength
                total_weight += weight

        # 避免除零
        if total_weight == 0:
            return 0.0

        # 正規化分數
        base_score = total_score / total_weight

        # 應用置信度調整
        adjusted_score = base_score * detection_result.confidence

        return min(adjusted_score, 1.0)

    def _generate_reasoning(
        self,
        module_name: str,
        detection_result: DetectionResult,
        score: float
    ) -> str:
        """生成評分理由"""
        if score > 0.8:
            return f"{module_name} 高度匹配：檢測到多個相關模式"
        elif score > 0.5:
            return f"{module_name} 中等匹配：檢測到部分相關特徵"
        elif score > 0.2:
            return f"{module_name} 低度匹配：檢測到少量相關信號"
        else:
            return f"{module_name} 不匹配：未檢測到相關特徵"

    def select_best_module(
        self,
        scores: List[ModuleScore],
        min_threshold: float = 0.3
    ) -> ModuleScore:
        """選擇最佳模組"""
        if not scores:
            return ModuleScore("dialogue", 0.5, "預設對話模組", 0.5)

        best_score = scores[0]

        # 如果最高分數低於閾值，使用對話模組
        if best_score.score < min_threshold:
            return ModuleScore(
                "dialogue",
                0.5,
                "分數過低，使用預設對話模組",
                0.5
            )

        return best_score