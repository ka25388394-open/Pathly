"""Pydantic schemas — TST 轉化層輸出。

對應 app/prompts/awareness.md / reframe.md / action.md。
使用者可見文字欄位套用 tone_guard；micro_action 額外套 soft_step_field。
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.core.tone_guard import soft_step_field, tone_field

ReframeType = Literal["事實重述", "責任重分", "時間拉遠", "身份分離"]


class AwarenessOutput(BaseModel):
    awareness_text: str
    pattern_detected: str
    historical_echo: str

    _tone = tone_field("awareness_text", "historical_echo")


class ReframeOutput(BaseModel):
    original_sentence: str
    reframed_sentence: str
    new_perspective: str
    reframe_type: ReframeType

    _tone = tone_field("reframed_sentence", "new_perspective")


class ActionOutput(BaseModel):
    micro_action: str
    execution_context: str
    duration_minutes: int = Field(ge=1, le=15)
    difficulty: int = Field(ge=1, le=3)
    success_criteria: str
    keep_choice: str

    _tone = tone_field(
        "micro_action", "execution_context", "success_criteria", "keep_choice"
    )
    _soft = soft_step_field("micro_action")


class TSTResult(BaseModel):
    awareness: AwarenessOutput
    reframe: ReframeOutput
    action: ActionOutput
