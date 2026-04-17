"""TrackingLog — 任務追蹤與使用者回饋。"""

from __future__ import annotations

from sqlalchemy import ForeignKey, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKey


class TrackingLog(UUIDPrimaryKey, TimestampMixin, Base):
    __tablename__ = "tracking_logs"

    tst_task_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tst_tasks.id"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
    event_type: Mapped[str] = mapped_column(String(20))  # started/completed/skipped/reflected
    feedback_text: Mapped[str | None] = mapped_column(Text)
    felt_change: Mapped[int | None] = mapped_column(SmallInteger)  # -5 ~ +5
    next_hint: Mapped[str | None] = mapped_column(Text)
