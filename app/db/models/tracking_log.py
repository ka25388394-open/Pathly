"""TrackingLog — 任務追蹤與使用者回饋。"""

from __future__ import annotations

from sqlalchemy import ForeignKey, SmallInteger, String, Text
from sqlalchemy import Column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKey


class TrackingLog(UUIDPrimaryKey, TimestampMixin, Base):
    __tablename__ = "tracking_logs"

    tst_task_id= Column(
        String(36), ForeignKey("tst_tasks.id"), nullable=False
    )
    user_id= Column(
        String(36), ForeignKey("users.id"), nullable=False
    )
    event_type= Column(String(20))  # started/completed/skipped/reflected
    feedback_text= Column(Text)
    felt_change= Column(SmallInteger)  # -5 ~ +5
    next_hint= Column(Text)
