"""AI 分層聊天端點 - 最小版本"""

import time
import uuid
from fastapi import APIRouter
from app.schemas.ai_simple import ChatRequest, ChatResponse
from app.core.ai_simple import detect_level, RESPONSE_TEMPLATES

router = APIRouter()


@router.post("/ai-chat", response_model=ChatResponse)
async def ai_chat(request: ChatRequest):
    """
    AI 分層聊天端點

    根據用戶輸入判斷需要的支援等級（1-3），回傳對應回應
    """
    start_time = time.time()

    # 生成 session_id
    session_id = request.session_id or f"sess_{uuid.uuid4().hex[:8]}"

    # 檢測等級
    level, analysis_data = detect_level(request.message)

    # 獲取回應模板
    template = RESPONSE_TEMPLATES[level]

    # 建構回應
    response_data = {
        "message": template["message"],
        "suggestions": template["suggestions"]
    }

    # Level 3 額外欄位
    if level == 3:
        response_data.update({
            "empathy": template.get("empathy", []),
            "awareness": template.get("awareness", []),
            "reframe": template.get("reframe", []),
            "action": template.get("action", [])
        })

    # 計算處理時間
    processing_time = int((time.time() - start_time) * 1000)

    return ChatResponse(
        success=True,
        level=level,
        analysis=analysis_data,
        response=response_data,
        processing_time_ms=processing_time,
        session_id=session_id
    )


@router.get("/ai-chat/health")
async def ai_chat_health():
    """AI 聊天系統健康檢查"""
    # 簡單測試
    test_level, _ = detect_level("測試")

    return {
        "status": "healthy",
        "service": "ai_chat",
        "test_level": test_level,
        "version": "1.0-minimal"
    }