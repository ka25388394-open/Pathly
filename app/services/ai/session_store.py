"""最小可行 Session Memory Store - Level 2 三句承接專用"""

from __future__ import annotations

import time
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class SessionContext:
    """會話上下文 - 只保存最近3輪"""
    session_id: str
    messages: List[str] = field(default_factory=list)      # 最近3句
    levels: List[int] = field(default_factory=list)        # 最近3次level
    states: List[str] = field(default_factory=list)        # 最近3次state
    turn_count: int = 0                                     # 目前輪次
    last_updated: datetime = field(default_factory=datetime.now)

    def add_turn(self, message: str, level: int, state: str):
        """添加一輪對話，保持最近3輪"""
        # 添加到列表
        self.messages.append(message)
        self.levels.append(level)
        self.states.append(state)

        # 保持最近3輪，先進先出
        if len(self.messages) > 3:
            self.messages.pop(0)
            self.levels.pop(0)
            self.states.pop(0)

        self.turn_count = len(self.messages)
        self.last_updated = datetime.now()

    @property
    def previous_level(self) -> Optional[int]:
        """上一輪的level"""
        return self.levels[-1] if len(self.levels) > 0 else None

    @property
    def previous_state(self) -> Optional[str]:
        """上一輪的state"""
        return self.states[-1] if len(self.states) > 0 else None


class SessionStore:
    """In-Memory Session Store - MVP版本"""

    def __init__(self):
        self._sessions: Dict[str, SessionContext] = {}

    def get_or_create_session(self, session_id: str) -> SessionContext:
        """取得或建立會話上下文"""
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionContext(session_id=session_id)
        return self._sessions[session_id]

    def update_session(self, session_id: str, message: str, level: int, state: str):
        """更新會話狀態"""
        context = self.get_or_create_session(session_id)
        context.add_turn(message, level, state)

    def cleanup_expired_sessions(self, max_age_hours: int = 24):
        """清理過期會話 - 防止記憶體洩漏"""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        expired_sessions = [
            session_id for session_id, context in self._sessions.items()
            if context.last_updated < cutoff_time
        ]

        for session_id in expired_sessions:
            del self._sessions[session_id]

        return len(expired_sessions)

    def get_session_count(self) -> int:
        """取得目前會話數量 - 用於監控"""
        return len(self._sessions)


# Global instance - MVP使用單例
session_store = SessionStore()


def get_session_store() -> SessionStore:
    """取得全域 session store"""
    return session_store