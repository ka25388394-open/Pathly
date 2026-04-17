"""對話陪伴API端點"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.unified_ai_client import UnifiedAIClient


router = APIRouter(prefix="/dialogue", tags=["dialogue"])


class DialogueRequest(BaseModel):
    """對話請求"""
    user_input: str
    user_id: str = "anonymous"
    context: dict = {}


class DialogueResponse(BaseModel):
    """對話回應"""
    response: str
    level_used: str
    format_type: str
    allow_progression: bool
    next_suggestions: list[str]
    confidence_score: float
    success: bool = True


@router.post("/chat", response_model=DialogueResponse)
async def chat(request: DialogueRequest):
    """
    整合對話端點

    這是pathly的核心對話功能，整合了三層回應系統：
    - Level 1: 分層對話陪伴
    - Level 2: STL整理式回應
    - Level 3: TST四段式行動
    系統會根據使用者狀態智能選擇最適合的層級。
    """
    try:
        result = await integrated_dialogue_client.process_input(
            user_input=request.user_input,
            context=request.context
        )

        return DialogueResponse(
            response=result.response,
            level_used=result.level_used,
            format_type=result.format_type,
            allow_progression=result.allow_progression,
            next_suggestions=result.next_suggestions,
            confidence_score=result.confidence_score,
            success=True
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"對話處理失敗: {str(e)}"
        )


@router.get("/test")
async def test_dialogue_system():
    """測試對話系統的各種模式"""

    test_cases = {
        "grounding_test": "我真的很煩，整個人快炸掉了，什麼都不想碰",
        "clarification_test": "最近很多事情混在一起，有點說不清楚",
        "structuring_test": "我現在有三件事要處理，但時間不夠，怎麼排比較好",
        "reflection_test": "我發現我每次壓力大就會逃，然後最後更糟",
        "complex_test": "我知道我在逃，但我也覺得我需要休息，但又覺得自己是不是在找藉口"
    }

    try:
        results = await integrated_dialogue_client.test_all_levels(test_cases)
        return {
            "status": "success",
            "test_results": results,
            "total_tests": len(test_cases),
            "passed": len([r for r in results.values() if "error" not in r])
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"測試失敗: {str(e)}"
        )


@router.post("/analyze")
async def analyze_input(request: DialogueRequest):
    """
    分析使用者輸入（內部調試用）

    注意：這個端點會返回分析詳情，僅供開發調試使用，
    不應該在正式產品中對使用者顯示這些信息。
    """
    try:
        # 先進行分析但不生成回應
        result = await integrated_dialogue_client.process_input(
            user_input=request.user_input,
            context=request.context
        )

        # 獲取調試信息
        analytics = integrated_dialogue_client.analysis_engine.get_debug_info(result.analysis_result)

        return {
            "input": request.user_input,
            "analytics": analytics,
            "routing_decision": {
                "level_used": result.level_used,
                "format_type": result.format_type,
                "confidence_score": result.confidence_score,
                "routing_reason": result.routing_reason
            },
            "warning": "此為內部調試信息，不應顯示給使用者"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"分析失敗: {str(e)}"
        )