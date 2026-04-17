"""STL / Structure Mapping — 結構映照模組。

把使用者原始輸入拆成四層結構：事件/想法/情緒/行為，
建立因果關係，區分表面問題與根本議題。
"""

from __future__ import annotations

from app.schemas.stl import StateSensingOutput, StructureMappingOutput
from app.services.ai_client import call_with_tone_guard


async def run_structure_mapping(
    raw_text: str, state_sensing: StateSensingOutput
) -> StructureMappingOutput:
    """執行 STL 結構映照：把原始輸入拆解成四層結構圖。

    Args:
        raw_text: 使用者原始輸入文字
        state_sensing: 前一階段的狀態感知結果

    Returns:
        StructureMappingOutput: 問題地圖、表面問題、根本議題、階段位置

    Raises:
        RuntimeError: Claude API 呼叫失敗
        ToneViolation: 輸出違反語氣憲法
    """
    payload = {
        "raw_text": raw_text,
        "state_sensing": {
            "state_label": state_sensing.state_label,
            "tension_score": state_sensing.tension_score,
            "core_block": state_sensing.core_block,
        },
    }

    return await call_with_tone_guard(
        task="structure_mapping",
        payload=payload,
        schema=StructureMappingOutput,
    )