"""STL/TST function stubs to prevent crashes during deployment."""

from typing import Any, Dict
from pydantic import BaseModel


class STLResult(BaseModel):
    """Stub STL analysis result."""
    state_sensing: Dict[str, Any] = {
        "tension_score": 0.5,
        "emotion_intensity": 0.5,
        "confidence": 0.8
    }
    structure_mapping: Dict[str, Any] = {
        "patterns": ["basic_structure"],
        "complexity": 0.5
    }
    language_clarification: Dict[str, Any] = {
        "clarity_score": 0.7,
        "suggestions": ["簡化表達"]
    }


class TSTResult(BaseModel):
    """Stub TST transformation result."""
    tasks: list = ["理解情況", "整理想法", "溫柔回應"]
    transformation_steps: list = ["感受確認", "情況梳理", "語言轉化", "溫柔陪伴"]


class EngineScores(BaseModel):
    """Decision engine scores."""
    stability: float = 0.7
    readiness: float = 0.6
    mode: str = "supportive"


async def run_full_stl(text: str) -> STLResult:
    """Stub STL analysis - prevents crash during deployment."""
    return STLResult()


async def run_full_tst(text: str, stl_result: STLResult) -> TSTResult:
    """Stub TST transformation - prevents crash during deployment."""
    return TSTResult()


def compute_stability(tension: float, intensity: float) -> float:
    """Compute stability score from tension and emotion intensity."""
    return max(0.0, min(1.0, 1.0 - (tension + intensity) / 2))


def compute_readiness(clarity: float, confidence: float, complexity: float = 0.5) -> float:
    """Compute readiness score from clarity and confidence."""
    return max(0.0, min(1.0, (clarity + confidence - complexity) / 2))


def decide_mode(stability: float, readiness: float) -> str:
    """Decide processing mode based on stability and readiness scores."""
    if stability >= 0.7 and readiness >= 0.7:
        return "analytical"
    elif stability >= 0.5:
        return "supportive"
    else:
        return "gentle"


def next_step_for_mode(mode: str, current_state: str = "initial") -> str:
    """Get next step recommendation for given mode."""
    steps = {
        "analytical": "深入分析情況結構",
        "supportive": "提供溫暖的情感支持",
        "gentle": "慢慢陪伴，不急於分析"
    }
    return steps.get(mode, "溫柔陪伴，慢慢來")