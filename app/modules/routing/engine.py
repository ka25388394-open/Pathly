"""簡化的路由引擎 - 使用整合的檢測和評分組件"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Any

from .detector import IntegratedDetector, DetectionResult
from .scorer import IntegratedScorer, ModuleScore


@dataclass
class RoutingResult:
    """簡化的路由分析結果"""
    # 輸入基本信息
    input_text: str
    text_length: int

    # 檢測結果
    detected_patterns: List[str]
    signal_strength: float

    # 模組評分
    selected_module: str
    confidence: float
    reasoning: str

    # 所有模組分數
    module_scores: List[ModuleScore]


class RoutingEngine:
    """簡化的路由引擎"""

    def __init__(self):
        self.detector = IntegratedDetector()
        self.scorer = IntegratedScorer()

    def analyze_input(self, text: str, context: Optional[Dict[str, Any]] = None) -> RoutingResult:
        """
        分析輸入文本，選擇最佳處理模組

        Args:
            text: 使用者輸入文本
            context: 可選的上下文信息

        Returns:
            路由分析結果
        """
        # 1. 檢測模式和信號
        detection_result = self.detector.detect(text, context)

        # 2. 為各模組評分
        module_scores = self.scorer.score_modules(detection_result, context)

        # 3. 選擇最佳模組
        best_module = self.scorer.select_best_module(module_scores)

        return RoutingResult(
            input_text=text,
            text_length=len(text),
            detected_patterns=detection_result.detected_patterns,
            signal_strength=detection_result.signal_strength,
            selected_module=best_module.module_name,
            confidence=best_module.confidence,
            reasoning=best_module.reasoning,
            module_scores=module_scores
        )

    def get_routing_summary(self, result: RoutingResult) -> str:
        """獲取路由決策的簡要說明"""
        return (
            f"選擇 {result.selected_module} 模組 "
            f"(置信度: {result.confidence:.2f}) - {result.reasoning}"
        )