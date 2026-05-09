"""AI Support API 端點 - core-pathly-main"""

import time
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from app.schemas.ai import (
    SupportRequest,
    SupportResponse,
    SupportResponseData,
    AnalysisResult,
    ResponseMetadata,
    ErrorResponse
)
from app.services.ai import LevelDetector, ResponseBuilder
from app.services.ai.session_store import get_session_store
from app.services.ai.reset_detector import detect_reset_signal
from app.services.ai.tst_router import determine_tst_marker
from app.config import get_settings

router = APIRouter()


@router.post(
    "/support",
    response_model=SupportResponse,
    summary="AI 分層心理支援",
    description="接收用戶輸入，進行分層分析並提供適當的心理支援回應",
    responses={
        200: {"description": "成功處理請求"},
        400: {"description": "請求格式錯誤"},
        500: {"description": "服務器內部錯誤"}
    }
)
async def ai_support(request: SupportRequest):
    """
    AI 分層心理支援端點

    根據用戶輸入的訊息，判斷需要的支援等級（1-3），
    並回傳對應的分析結果和適當的回應。

    - **Level 1**: 日常對話，輕鬆互動
    - **Level 2**: 輕度關懷，同理回應
    - **Level 3**: 深度陪伴，專業支援結構

    """
    start_time = time.time()
    settings = get_settings()

    try:
        # 生成 session_id（如果沒有提供）
        session_id = request.session_id or f"sess_{uuid.uuid4().hex[:8]}"

        # 取得 session context
        session_store = get_session_store()
        session_context = session_store.get_or_create_session(session_id)

        # 初始化檢測器和建構器
        detector = LevelDetector()
        builder = ResponseBuilder()


        # 檢測等級和分析
        level, analysis_info = detector.detect_level(request.message)

        # 檢測 reset 訊號
        reset_signal, reset_reason = detect_reset_signal(request.message)


        # 判斷 TST marker (Phase 2B)
        tst_marker = determine_tst_marker(reset_signal, request.message)


        # Level 2 continuity guard - 維持 Level 2 承接
        original_level = level
        if (session_context.previous_level == 2 and
            session_context.turn_count >= 1 and
            session_context.turn_count < 3 and
            level != 3):  # 不干擾真正的危機狀態
            level = 2

        # 建構回應 (Level 2 時傳遞本輪的 turn_count)
        if level == 2:
            # 修正時序：計算本輪應使用的 turn_count
            current_turn_count = min(session_context.turn_count + 1, 3)
            response_content = builder.build_response(level, analysis_info, request.message, turn_count=current_turn_count)
        else:
            response_content = builder.build_response(level, analysis_info, request.message)

        # 取得狀態用於更新 session
        state = getattr(response_content, 'state', 'unknown')
        if hasattr(response_content, 'response') and hasattr(response_content.response, 'state'):
            state = response_content.response.state

        # 保存本輪實際的 turn_count (用於 metadata 正確顯示)
        actual_turn_count = min(session_context.turn_count + 1, 3)

        # 更新 session context
        session_store.update_session(session_id, request.message, level, state)

        # 定期清理過期 session (每100次請求清理一次)
        if session_context.turn_count % 100 == 0:
            session_store.cleanup_expired_sessions()

        # 計算處理時間
        processing_time = int((time.time() - start_time) * 1000)

        # 建構分析結果
        analysis_result = AnalysisResult(**analysis_info)

        # 建構元資料 (添加 session 相關資訊和 reset 檢測結果)
        session_info = f"turn_{actual_turn_count}_prev_lvl_{session_context.previous_level or 'none'}"
        metadata = ResponseMetadata(
            processing_time_ms=processing_time,
            model_used=f"rule_based_session_enabled_{session_info}",
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            reset_signal=reset_signal,
            reset_reason=reset_reason if reset_signal else None,
            tst_marker=tst_marker
        )


        # 建構最終回應
        response_data = SupportResponseData(
            level=level,
            analysis=analysis_result,
            response=response_content,
            metadata=metadata
        )

        return SupportResponse(
            success=True,
            data=response_data
        )

    except Exception as e:
        # 錯誤處理
        settings = get_settings()
        error_detail = str(e) if settings.app_debug else "Internal server error"

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": error_detail,
                "code": "SUPPORT_PROCESSING_ERROR"
            }
        )


@router.get(
    "/support/health",
    summary="AI Support 健康檢查",
    description="檢查 AI Support 服務是否正常運行"
)
async def support_health():
    """AI Support 服務健康檢查"""
    try:
        # 簡單測試檢測器
        detector = LevelDetector()
        level, _ = detector.detect_level("測試訊息")

        return {
            "status": "healthy",
            "service": "ai_support",
            "detector_working": True,
            "test_level": level
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "service": "ai_support",
                "error": str(e)
            }
        )