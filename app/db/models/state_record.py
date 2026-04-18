"""StateRecord — 使用者原始輸入記錄。"""

from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Index, String, Text

from app.db.base import Base, TimestampMixin, UUIDPrimaryKey


class StateRecord(UUIDPrimaryKey, TimestampMixin, Base):
    __tablename__ = "state_records"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    raw_text = Column(Text, nullable=False)
    input_channel = Column(String(20), default="web")
    session_id = Column(String(36), nullable=False)

    __table_args__ = (
        Index("ix_state_records_user_created", "user_id", "created_at"),
    )
