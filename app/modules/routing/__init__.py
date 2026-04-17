"""路由模組 - 整合的智能路由系統

提供統一的路由決策功能：
- 檢測用戶輸入的模式和信號
- 為不同處理模組評分
- 選擇最適合的處理路徑
"""

from __future__ import annotations

from .detector import IntegratedDetector, DetectionResult
from .scorer import IntegratedScorer, ModuleScore
from .engine import RoutingEngine

__all__ = [
    "IntegratedDetector",
    "DetectionResult",
    "IntegratedScorer",
    "ModuleScore",
    "RoutingEngine",
    "SmartRouter"
]


class SmartRouter:
    """智能路由器 - 整合檢測、評分和路由決策"""

    def __init__(self):
        self.detector = IntegratedDetector()
        self.scorer = IntegratedScorer()

    async def route(self, user_input: str, context: dict = None) -> dict:
        """路由用戶輸入到最適合的處理模組"""

        # 1. 檢測模式和信號
        detection_result = self.detector.detect(user_input, context)

        # 2. 為各模組評分
        module_scores = self.scorer.score_modules(detection_result, context)

        # 3. 選擇最佳模組
        best_module = self.scorer.select_best_module(module_scores)

        return {
            "selected_module": best_module.module_name,
            "confidence": best_module.confidence,
            "reasoning": best_module.reasoning,
            "score": best_module.score,
            "all_scores": [
                {
                    "module": score.module_name,
                    "score": score.score,
                    "reasoning": score.reasoning
                }
                for score in module_scores
            ],
            "detection_details": {
                "patterns": detection_result.detected_patterns,
                "signals": detection_result.detected_signals,
                "signal_strength": detection_result.signal_strength
            }
        }