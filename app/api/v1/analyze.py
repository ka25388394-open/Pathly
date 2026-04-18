"""POST /analyze — STL 理解 + Decision Engine 判定。"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import StateRecord, STLAnalysis
from app.db.session import get_db
from app.schemas.api import AnalyzeRequest, AnalyzeResponse, Scores
from app.core.unified_ai_client import UnifiedAIClient
from app.services.stl_stubs import (
    run_full_stl, compute_stability, compute_readiness,
    decide_mode, EngineScores
)

router = APIRouter(tags=["analyze"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    req: AnalyzeRequest, db: Session = Depends(get_db)
) -> AnalyzeResponse:
    record = db.get(StateRecord, req.state_record_id)
    if record is None:
        raise HTTPException(404, "state_record not found")

    # 冪等：若已分析過，直接回傳既有結果
    existing = (
        db.query(STLAnalysis)
        .filter(STLAnalysis.state_record_id == record.id)
        .first()
    )
    if existing is not None:
        return _to_response(existing)

    stl = await run_full_stl(record.raw_text)

    sensing = stl.state_sensing
    mapping = stl.structure_mapping
    clarification = stl.language_clarification

    stability = compute_stability(sensing.tension_score, sensing.emotion_intensity)
    readiness = compute_readiness(
        clarification.clarity_score, stability, mapping.stage_position
    )
    scores = EngineScores(
        stability=stability,
        tension=sensing.tension_score,
        clarity=clarification.clarity_score,
        readiness=readiness,
    )
    mode = decide_mode(scores)

    analysis = STLAnalysis(
        state_record_id=record.id,
        state_label=sensing.state_label,
        tension_score=sensing.tension_score,
        emotion_intensity=sensing.emotion_intensity,
        stability_score=stability,
        core_block=sensing.core_block,
        problem_map=mapping.problem_map.model_dump(),
        surface_problem=mapping.surface_problem,
        root_issue=mapping.root_issue,
        stage_position=mapping.stage_position,
        clarified_sentence=clarification.clarified_sentence,
        core_statement=clarification.core_statement,
        transformation_input=clarification.transformation_input,
        clarity_score=clarification.clarity_score,
        readiness_score=readiness,
        decided_mode=mode,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return _to_response(analysis)


def _to_response(a: STLAnalysis) -> AnalyzeResponse:
    return AnalyzeResponse(
        stl_analysis_id=a.id,
        mode=a.decided_mode,  # type: ignore[arg-type]
        scores=Scores(
            stability=a.stability_score,
            tension=a.tension_score,
            clarity=a.clarity_score or 0,
            readiness=a.readiness_score,
        ),
        state_label=a.state_label,
        core_block=a.core_block,
        root_issue=a.root_issue or "",
        clarified_sentence=a.clarified_sentence or "",
        next_step=next_step_for_mode(a.decided_mode),  # type: ignore[arg-type]
    )
