"""POST /transform — TST 轉化層，產出 tst_task。"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.models import StateRecord, STLAnalysis, TSTTask
from app.db.session import get_db
from app.schemas.api import TransformRequest, TransformResponse
from app.schemas.stl import (
    LanguageClarificationOutput,
    ProblemMap,
    StateSensingOutput,
    STLResult,
    StructureMappingOutput,
)
from app.core.unified_ai_client import UnifiedAIClient

router = APIRouter(tags=["transform"])


@router.post("/transform", response_model=TransformResponse)
async def transform(
    req: TransformRequest, db: Session = Depends(get_db)
) -> TransformResponse:
    # Phase 1 mock：TST service 還是空的，給前端一份氣質正確的三段式範本。
    if get_settings().mock_ai:
        return TransformResponse(
            tst_task_id=f"mock-tst-{req.stl_analysis_id}",
            awareness_text=(
                "你注意到自己在做的事，和你想被看見的那一面，好像沒完全對上。"
            ),
            pattern_detected="把自我價值綁在今天的產出上",
            reframed_sentence=(
                "現在這種『做不到』的感覺，"
                "更像是『我正在學著把自己和產出分開來看』，而不是『我真的不行』。"
            ),
            new_perspective="分開自我與產出",
            micro_action="今晚睡前可以先寫三行今天有做到的小事，不用評價、不用長。",
            execution_context="睡前、只寫三行、不用形容詞",
            duration_minutes=5,
            difficulty=1,
        )

    analysis = db.get(STLAnalysis, req.stl_analysis_id)
    if analysis is None:
        raise HTTPException(404, "stl_analysis not found")

    record = db.get(StateRecord, analysis.state_record_id)
    if record is None:
        raise HTTPException(404, "state_record not found")

    # 冪等
    existing = (
        db.query(TSTTask).filter(TSTTask.stl_analysis_id == analysis.id).first()
    )
    if existing is not None:
        return _to_response(existing)

    stl_result = _hydrate_stl_result(analysis)
    tst = await run_full_tst(record.raw_text, stl_result)

    task = TSTTask(
        stl_analysis_id=analysis.id,
        user_id=record.user_id,
        awareness_text=tst.awareness.awareness_text,
        pattern_detected=tst.awareness.pattern_detected,
        historical_echo=tst.awareness.historical_echo,
        original_sentence=tst.reframe.original_sentence,
        reframed_sentence=tst.reframe.reframed_sentence,
        new_perspective=tst.reframe.new_perspective,
        reframe_type=tst.reframe.reframe_type,
        micro_action=tst.action.micro_action,
        execution_context=tst.action.execution_context,
        duration_minutes=tst.action.duration_minutes,
        difficulty=tst.action.difficulty,
        success_criteria=tst.action.success_criteria,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return _to_response(task)


def _hydrate_stl_result(a: STLAnalysis) -> STLResult:
    """從 STLAnalysis row 重建 STLResult 物件（給 TST 使用）。"""
    return STLResult(
        state_sensing=StateSensingOutput(
            state_label=a.state_label,  # type: ignore[arg-type]
            tension_score=a.tension_score,
            emotion_intensity=a.emotion_intensity,
            stability_score=a.stability_score,
            core_block=a.core_block,
            signals=[],
        ),
        structure_mapping=StructureMappingOutput(
            problem_map=ProblemMap(**(a.problem_map or {})),
            surface_problem=a.surface_problem or "",
            root_issue=a.root_issue or "",
            stage_position=a.stage_position or "卡住",  # type: ignore[arg-type]
        ),
        language_clarification=LanguageClarificationOutput(
            clarified_sentence=a.clarified_sentence or "",
            core_statement=a.core_statement or "",
            transformation_input=a.transformation_input or "",
            clarity_score=a.clarity_score or 0,
        ),
    )


def _to_response(t: TSTTask) -> TransformResponse:
    return TransformResponse(
        tst_task_id=t.id,
        awareness_text=t.awareness_text,
        pattern_detected=t.pattern_detected or "",
        reframed_sentence=t.reframed_sentence,
        new_perspective=t.new_perspective or "",
        micro_action=t.micro_action,
        execution_context=t.execution_context or "",
        duration_minutes=t.duration_minutes,
        difficulty=t.difficulty,
    )
