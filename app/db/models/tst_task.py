"""TSTTask — TST 轉化結果 + 任務追蹤。"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKey


class TSTTask(UUIDPrimaryKey, TimestampMixin, Base):
    __tablename__ = "tst_tasks"

    stl_analysis_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("stl_analysis.id"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )

    # --- Awareness ---
    awareness_text: Mapped[str] = mapped_column(Text)
    pattern_detected: Mapped[str | None] = mapped_column(String(100))
    historical_echo: Mapped[str | None] = mapped_column(Text)

    # --- Reframe ---
    original_sentence: Mapped[str | None] = mapped_column(Text)
    reframed_sentence: Mapped[str] = mapped_column(Text)
    new_perspective: Mapped[str | None] = mapped_column(Text)
    reframe_type: Mapped[str | None] = mapped_column(String(20))

    # --- Action ---
    micro_action: Mapped[str] = mapped_column(Text)
    execution_context: Mapped[str | None] = mapped_column(Text)
    duration_minutes: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(SmallInteger, default=1)
    success_criteria: Mapped[str | None] = mapped_column(Text)

    # --- 任務狀態機 ---
    status: Mapped[str] = mapped_column(String(20), default="pending")
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        Index("ix_tst_tasks_user_status_scheduled", "user_id", "status", "scheduled_at"),
    )
