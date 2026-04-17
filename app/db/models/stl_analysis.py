"""STLAnalysis — STL 理解層的完整分析結果 + 判定引擎輸出。"""

from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, CHAR, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKey


class STLAnalysis(UUIDPrimaryKey, TimestampMixin, Base):
    __tablename__ = "stl_analysis"

    state_record_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("state_records.id"), nullable=False
    )

    # --- State Sensing ---
    state_label: Mapped[str] = mapped_column(String(20))
    tension_score: Mapped[int] = mapped_column(Integer)
    emotion_intensity: Mapped[int] = mapped_column(Integer)
    stability_score: Mapped[int] = mapped_column(Integer)
    core_block: Mapped[str] = mapped_column(Text)

    # --- Structure Mapping ---
    problem_map: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    surface_problem: Mapped[str | None] = mapped_column(Text)
    root_issue: Mapped[str | None] = mapped_column(Text)
    stage_position: Mapped[str | None] = mapped_column(String(20))

    # --- Language Clarification ---
    clarified_sentence: Mapped[str | None] = mapped_column(Text)
    core_statement: Mapped[str | None] = mapped_column(Text)
    transformation_input: Mapped[str | None] = mapped_column(Text)
    clarity_score: Mapped[int | None] = mapped_column(Integer)

    # --- Decision Engine ---
    readiness_score: Mapped[int] = mapped_column(Integer)
    decided_mode: Mapped[str] = mapped_column(CHAR(1))  # A/B/C/D

    # --- 四段式使用者可見回應 ---
    response_hold: Mapped[str | None] = mapped_column(Text)
    response_organize: Mapped[str | None] = mapped_column(Text)
    response_small_step: Mapped[str | None] = mapped_column(Text)
    response_keep_choice: Mapped[str | None] = mapped_column(Text)

    # --- Meta ---
    ai_model: Mapped[str | None] = mapped_column(String(50))
    cost_tokens: Mapped[int] = mapped_column(Integer, default=0)
    tone_violations: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
