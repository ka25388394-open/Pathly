"""AI Dev Mode API 端點 - core-pathly-main"""

import time
import uuid
from fastapi import APIRouter, HTTPException, status
from app.schemas.ai import (
    DevRequest,
    DevResponse,
    DevResponseData,
    ErrorResponse
)
from app.config import get_settings

router = APIRouter()


def _analyze_dev_request(message: str) -> dict:
    """分析開發請求，返回四段式回應內容（Mock 版本）"""
    message_lower = message.lower()

    # 簡單關鍵字匹配邏輯
    if any(word in message_lower for word in ["level", "判斷", "檢測"]):
        return {
            "current_stage": "Level 檢測邏輯需要調整",
            "problem_essence": "規則引擎與實際使用情況不匹配",
            "next_step": "檢查 app/services/ai/level_detector.py，添加詳細 debug 日誌",
            "claude_prompt": "幫我檢視這個 Python level detection 函數，重點看條件判斷邏輯是否有遺漏或過於嚴格的地方"
        }
    elif any(word in message_lower for word in ["api", "端點", "endpoint"]):
        return {
            "current_stage": "API 功能需要新增或調整",
            "problem_essence": "端點設計或路由配置問題",
            "next_step": "確認路由註冊，檢查 app/api/v1/__init__.py 的 include_router",
            "claude_prompt": None
        }
    elif any(word in message_lower for word in ["部署", "deploy", "railway"]):
        return {
            "current_stage": "部署環境配置問題",
            "problem_essence": "雲端平台配置與本地環境不一致",
            "next_step": "檢查 .env 和 Railway 環境變數是否同步",
            "claude_prompt": None
        }
    elif any(word in message_lower for word in ["前端", "ui", "介面"]):
        return {
            "current_stage": "前端整合問題",
            "problem_essence": "前後端通信或介面設計需要優化",
            "next_step": "確認 pathly_simple_ui.html 中的 API 路徑是否正確指向 8007 端口",
            "claude_prompt": None
        }
    else:
        # 通用回應
        return {
            "current_stage": "問題需要進一步分析",
            "problem_essence": "尚未明確定義具體技術問題",
            "next_step": "提供更多上下文信息，例如錯誤訊息、預期行為、當前行為",
            "claude_prompt": "幫我分析這個開發問題的技術背景和可能的解決方向"
        }


@router.post(
    "/",
    response_model=DevResponse,
    summary="AI 開發模式協助",
    description="為 Pathly 開發者提供技術問題分析和解決建議",
    responses={
        200: {"description": "成功分析開發問題"},
        400: {"description": "請求格式錯誤"},
        500: {"description": "服務器內部錯誤"}
    }
)
async def ai_dev(request: DevRequest):
    """
    AI 開發模式協助端點

    專為 Pathly 開發者設計的技術支援系統：
    - 產品決策分析
    - 系統架構建議
    - Debug 問題指引
    - 最小可行方案設計

    回應格式固定為：
    1. 現在階段
    2. 問題本質（一句話）
    3. 最小下一步（只能一條）
    4. 必要時提供 Claude Prompt
    """
    start_time = time.time()
    settings = get_settings()

    try:
        # 生成 session_id（如果沒有提供）
        session_id = request.session_id or f"dev_{uuid.uuid4().hex[:8]}"

        # 分析開發請求
        analysis_result = _analyze_dev_request(request.message)

        # 計算處理時間
        processing_time = int((time.time() - start_time) * 1000)

        # 建構回應資料
        response_data = DevResponseData(
            current_stage=analysis_result["current_stage"],
            problem_essence=analysis_result["problem_essence"],
            next_step=analysis_result["next_step"],
            claude_prompt=analysis_result["claude_prompt"],
            processing_time_ms=processing_time,
            session_id=session_id
        )

        return DevResponse(
            success=True,
            data=response_data
        )

    except Exception as e:
        # 錯誤處理
        error_detail = str(e) if settings.app_debug else "Internal server error"

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": error_detail,
                "code": "DEV_PROCESSING_ERROR"
            }
        )


@router.get(
    "/health",
    summary="AI Dev Mode 健康檢查",
    description="檢查 AI Dev Mode 服務是否正常運行"
)
async def dev_health():
    """AI Dev Mode 服務健康檢查"""
    try:
        # 簡單測試分析功能
        test_result = _analyze_dev_request("測試開發問題")

        return {
            "status": "healthy",
            "service": "ai_dev",
            "analyzer_working": True,
            "test_current_stage": test_result["current_stage"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "service": "ai_dev",
                "error": str(e)
            }
        )