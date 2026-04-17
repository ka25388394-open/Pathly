"""Pydantic schemas — STL 理解層輸出。

欄位與 app/prompts/ 下的三支 STL prompt 一致。
使用者可見文字欄位全部套用 tone_guard。
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.core.tone_guard import tone_field

StateLabel = Literal[
    "混亂", "壓抑", "逃避", "焦慮", "低動力", "憤怒", "平靜", "清晰"
]
StagePosition = Literal["覺察前", "覺察中", "卡住", "準備轉化", "準備行動"]


class StateSensingOutput(BaseModel):
    state_label: StateLabel
    tension_score: int = Field(ge=0, le=100)
    emotion_intensity: int = Field(ge=0, le=100)
    stability_score: int = Field(ge=0, le=100)
    core_block: str = Field(max_length=60)
    signals: list[str] = Field(default_factory=list)

    _tone_core_block = tone_field("core_block")


class ProblemMap(BaseModel):
    event: str
    thought: str
    emotion: str
    behavior: str
    causal_chain: list[str] = Field(default_factory=list)


class StructureMappingOutput(BaseModel):
    problem_map: ProblemMap
    surface_problem: str
    root_issue: str
    stage_position: StagePosition

    _tone_root = tone_field("surface_problem", "root_issue")


class LanguageClarificationOutput(BaseModel):
    clarified_sentence: str
    core_statement: str
    transformation_input: str
    clarity_score: int = Field(ge=0, le=100)

    _tone = tone_field(
        "clarified_sentence", "core_statement", "transformation_input"
    )


class STLResult(BaseModel):
    """三個 STL 子模組的合併結果。"""

    state_sensing: StateSensingOutput
    structure_mapping: StructureMappingOutput
    language_clarification: LanguageClarificationOutput
