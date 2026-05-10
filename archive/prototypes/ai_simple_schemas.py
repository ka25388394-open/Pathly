"""AI 分層系統 - 簡單資料模型"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class ChatRequest(BaseModel):
    """聊天請求"""
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """聊天回應"""
    success: bool = True
    level: int
    analysis: Dict[str, Any]
    response: Dict[str, Any]
    processing_time_ms: int
    session_id: str