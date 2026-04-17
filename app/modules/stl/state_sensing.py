"""STL / State Sensing — 狀態感知模組。

從使用者原始輸入感知當下狀態：情緒強度、語氣張力、核心卡住點。
不分析原因、不給建議、不安慰，只是精準的狀態感知器。
"""

from __future__ import annotations

from app.schemas.stl import StateSensingOutput
from app.services.ai_client import call_with_tone_guard


async def run_state_sensing(raw_text: str) -> StateSensingOutput:
    """執行 STL 狀態感知：把原始輸入變成結構化狀態標籤。

    Args:
        raw_text: 使用者原始輸入文字

    Returns:
        StateSensingOutput: 狀態標籤、張力分數、情緒強度、穩定度、核心卡點、語氣訊號

    Raises:
        RuntimeError: Claude API 呼叫失敗
        ToneViolation: 輸出違反語氣憲法（tone_guard 會自動重試）
    """
    payload = {"raw_text": raw_text}

    return await call_with_tone_guard(
        task="state_sensing",
        payload=payload,
        schema=StateSensingOutput,
    )