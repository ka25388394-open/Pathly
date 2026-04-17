"""SQLAlchemy engine / session 建立。"""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings

# 🚀 延後初始化：避免import時創建DB連線
_engine = None
_session_factory = None


def _get_engine():
    """懶載入資料庫引擎"""
    global _engine
    if _engine is None:
        _settings = get_settings()
        _engine_kwargs: dict = {}
        if _settings.is_sqlite:
            _engine_kwargs["connect_args"] = {"check_same_thread": False}
        _engine = create_engine(_settings.database_url, **_engine_kwargs)
    return _engine


def _get_session_factory():
    """懶載入session工廠"""
    global _session_factory
    if _session_factory is None:
        engine = _get_engine()
        _session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return _session_factory


# 向後相容的函數形式存取
def get_engine():
    return _get_engine()

def get_session_local():
    return _get_session_factory()

# 向後相容：模擬原來的全域變數
class _LazyEngine:
    def __getattr__(self, name):
        return getattr(_get_engine(), name)

class _LazySessionLocal:
    def __call__(self, *args, **kwargs):
        return _get_session_factory()(*args, **kwargs)

engine = _LazyEngine()
SessionLocal = _LazySessionLocal()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency — 每個 request 一個 session。"""
    # 延後到實際請求時才創建session
    session_factory = _get_session_factory()
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """開發階段用 — 依照 model 建立所有表。正式環境請改用 Alembic。"""
    # 匯入所有 model 確保 metadata 已註冊
    from app.db.models import (  # noqa: F401
        state_record,
        stl_analysis,
        tracking_log,
        tst_task,
        user,
    )
    from app.db.base import Base

    # 現在才真正創建DB引擎和表
    actual_engine = _get_engine()
    Base.metadata.create_all(bind=actual_engine)
