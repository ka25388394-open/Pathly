"""STL / Language Clarification — 語言釐清模組。

把使用者模糊的感受翻譯成一句他自己也能認得的清晰句子。
不重寫人生，只是遞一個更清楚的鏡子。
"""

from __future__ import annotations

from app.schemas.stl import (
    LanguageClarificationOutput,
    StateSensingOutput,
    StructureMappingOutput,
)
from app.services.ai_client import call_with_tone_guard


async def run_language_clarification(
    raw_text: str,
    state_sensing: StateSensingOutput,
    structure_mapping: StructureMappingOutput,
) -> LanguageClarificationOutput:
    """執行 STL 語言釐清：把模糊感受翻譯成使用者能認得的清晰句子。

    Args:
        raw_text: 使用者原始輸入文字
        state_sensing: 狀態感知結果
        structure_mapping: 結構映照結果

    Returns:
        LanguageClarificationOutput: 釐清句子、核心陳述、轉化輸入、清晰度分數

    Raises:
        RuntimeError: Claude API 呼叫失敗
        ToneViolation: 輸出違反語氣憲法
    """
    payload = {
        "raw_text": raw_text,
        "state_sensing": {
            "state_label": state_sensing.state_label,
            "core_block": state_sensing.core_block,
        },
        "structure_mapping": {
            "root_issue": structure_mapping.root_issue,
            "surface_problem": structure_mapping.surface_problem,
        },
    }

    return await call_with_tone_guard(
        task="language_clarification",
        payload=payload,
        schema=LanguageClarificationOutput,
    )