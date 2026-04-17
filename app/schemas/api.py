"""API request / response schemas。"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from app.schemas.response import UserFacingResponse


# ---------------------------------------------------------------------------
# /input
# ---------------------------------------------------------------------------
class InputRequest(BaseModel):
    raw_text: str = Field(min_length=1, max_length=5000)
    session_id: str | None = None
    user_id: str  # MVP 階段暫時手動傳，Phase 2 換成 JWT


class InputResponse(BaseModel):
    state_record_id: str
    session_id: str
    created_at: datetime


# ---------------------------------------------------------------------------
# /analyze
# ---------------------------------------------------------------------------
class AnalyzeRequest(BaseModel):
    state_record_id: str


class Scores(BaseModel):
    stability: int
    tension: int
    clarity: int
    readiness: int


class AnalyzeResponse(BaseModel):
    stl_analysis_id: str
    mode: Literal["A", "B", "C", "D"]
    scores: Scores
    state_label: str
    core_block: str
    root_issue: str
    clarified_sentence: str
    next_step: Literal["hold", "clarify", "transform", "action"]


# ---------------------------------------------------------------------------
# /transform
# ---------------------------------------------------------------------------
class TransformRequest(BaseModel):
    stl_analysis_id: str


class TransformResponse(BaseModel):
    tst_task_id: str
    awareness_text: str
    pattern_detected: str
    reframed_sentence: str
    new_perspective: str
    micro_action: str
    execution_context: str
    duration_minutes: int
    difficulty: int


# ---------------------------------------------------------------------------
# /task
# ---------------------------------------------------------------------------
class TaskActionRequest(BaseModel):
    tst_task_id: str
    action: Literal["start", "complete", "skip"]
    scheduled_at: datetime | None = None


class TaskActionResponse(BaseModel):
    tst_task_id: str
    status: str


# ---------------------------------------------------------------------------
# /track
# ---------------------------------------------------------------------------
class TrackRequest(BaseModel):
    tst_task_id: str
    event_type: Literal["started", "completed", "skipped", "reflected"]
    feedback_text: str | None = None
    felt_change: int | None = Field(default=None, ge=-5, le=5)


class TrackResponse(BaseModel):
    log_id: str
    next_hint: str | None = None
    pattern_progress: str | None = None


# ---------------------------------------------------------------------------
# /history
# ---------------------------------------------------------------------------
class HistoryItem(BaseModel):
    state_record_id: str
    created_at: datetime
    excerpt: str
    state_label: str | None = None
    mode: Literal["A", "B", "C", "D"] | None = None
    small_step: str | None = None
    task_status: Literal["pending", "started", "completed", "skipped"] | None = None


class HistoryResponse(BaseModel):
    items: list[HistoryItem]
    summary: str | None = None


# ---------------------------------------------------------------------------
# /process （合併端點，MVP 用）
# ---------------------------------------------------------------------------
class ProcessRequest(BaseModel):
    raw_text: str = Field(min_length=1, max_length=5000)
    user_id: str
    session_id: str | None = None


class ProcessResponse(BaseModel):
    session_id: str
    mode: Literal["A", "B", "C", "D"]
    response: UserFacingResponse
    meta: dict[str, Any] = Field(default_factory=dict)
