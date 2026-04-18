"""SQLAlchemy declarative base + UUID / timestamp mixins。"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


Base = declarative_base()


class UUIDPrimaryKey:
    """UUID 主鍵 mixin — 用 string 儲存以相容 SQLite/Postgres。"""

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )


class TimestampMixin:
    """created_at mixin。"""

    created_at = Column(
        DateTime(timezone=True),
        default=_utcnow,
        nullable=False,
    )
