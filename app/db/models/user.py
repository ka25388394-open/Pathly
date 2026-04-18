"""User — 使用者帳號。"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, String
from sqlalchemy import Column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKey


class User(UUIDPrimaryKey, TimestampMixin, Base):
    __tablename__ = "users"

    email= Column(String(255), unique=True, nullable=False)
    password_hash= Column(String(255), nullable=False)
    nickname= Column(String(50), nullable=True)
    last_active_at= Column(
        DateTime(timezone=True), nullable=True
    )
    preference= Column(JSON, default=dict)
