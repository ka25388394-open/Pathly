"""TSTTask — TST 轉化結果 + 任務追蹤。"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, SmallInteger, String, Text
from sqlalchemy import Column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKey


class TSTTask(UUIDPrimaryKey, TimestampMixin, Base):
    __tablename__ = "tst_tasks"

    stl_analysis_id= Column(
        String(36), ForeignKey("stl_analysis.id"), nullable=False
    )
    user_id= Column(
        String(36), ForeignKey("users.id"), nullable=False
    )

    # --- Awareness ---
    awareness_text= Column(Text)
    pattern_detected= Column(String(100))
    historical_echo= Column(Text)

    # --- Reframe ---
    original_sentence= Column(Text)
    reframed_sentence= Column(Text)
    new_perspective= Column(Text)
    reframe_type= Column(String(20))

    # --- Action ---
    micro_action= Column(Text)
    execution_context= Column(Text)
    duration_minutes= Column(Integer)
    difficulty= Column(SmallInteger, default=1)
    success_criteria= Column(Text)

    # --- 任務狀態機 ---
    status= Column(String(20), default="pending")
    scheduled_at= Column(DateTime(timezone=True))
    completed_at= Column(DateTime(timezone=True))

    __table_args__ = (
        Index("ix_tst_tasks_user_status_scheduled", "user_id", "status", "scheduled_at"),
    )
