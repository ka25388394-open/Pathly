"""STLAnalysis — STL 理解層的完整分析結果 + 判定引擎輸出。"""

from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, CHAR, ForeignKey, Integer, String, Text
from sqlalchemy import Column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKey


class STLAnalysis(UUIDPrimaryKey, TimestampMixin, Base):
    __tablename__ = "stl_analysis"

    state_record_id= Column(
        String(36), ForeignKey("state_records.id"), nullable=False
    )

    # --- State Sensing ---
    state_label= Column(String(20))
    tension_score= Column(Integer)
    emotion_intensity= Column(Integer)
    stability_score= Column(Integer)
    core_block= Column(Text)

    # --- Structure Mapping ---
    problem_map= Column(JSON, default=dict)
    surface_problem= Column(Text)
    root_issue= Column(Text)
    stage_position= Column(String(20))

    # --- Language Clarification ---
    clarified_sentence= Column(Text)
    core_statement= Column(Text)
    transformation_input= Column(Text)
    clarity_score= Column(Integer)

    # --- Decision Engine ---
    readiness_score= Column(Integer)
    decided_mode= Column(CHAR(1))  # A/B/C/D

    # --- 四段式使用者可見回應 ---
    response_hold= Column(Text)
    response_organize= Column(Text)
    response_small_step= Column(Text)
    response_keep_choice= Column(Text)

    # --- Meta ---
    ai_model= Column(String(50))
    cost_tokens= Column(Integer, default=0)
    tone_violations= Column(JSON, default=list)
