"""POST /process — MVP 合併端點。

一次跑完 input → analyze → (transform)，回傳最終四段式使用者可見格式。
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.models import StateRecord, STLAnalysis, TSTTask
from app.db.session import get_db
from app.schemas.api import ProcessRequest, ProcessResponse
from app.schemas.response import UserFacingResponse
from app.core.unified_ai_client import UnifiedAIClient

router = APIRouter(tags=["process"])


@router.post("/process", response_model=ProcessResponse)
async def process(
    req: ProcessRequest, db: Session = Depends(get_db)
) -> ProcessResponse:
    session_id = req.session_id or str(uuid.uuid4())

    # Phase 1 mock 模式：call_claude 還是 stub 時，給前端一份氣質正確的四段式範本。
    # 還是會寫一筆 StateRecord 進 DB，讓追蹤路徑能跑通。
    if get_settings().mock_ai:
        record = StateRecord(
            user_id=req.user_id,
            raw_text=req.raw_text,
            session_id=session_id,
        )
        db.add(record)
        db.commit()
        return ProcessResponse(
            session_id=session_id,
            mode="C",
            response=UserFacingResponse(
                hold="這樣的一天，確實會讓人不太想面對自己。",
                organize=(
                    "聽起來你現在更接近的，可能不是「做不到」，"
                    "而是把自己的價值跟今天的產出綁得很近。"
                ),
                small_step="如果願意的話，今晚睡前可以先寫三行今天有做到的小事，不用評價、不用長。",
                keep_choice="這件事不一定要今天就開始，先記住這個方向也可以。",
            ),
            meta={
                "mock": True,
                "state_record_id": record.id,
                "stl_analysis_id": f"mock-stl-{record.id}",
                "tst_task_id": f"mock-tst-{record.id}",
            },
        )

    # 1. 存原始輸入
    record = StateRecord(
        user_id=req.user_id,
        raw_text=req.raw_text,
        session_id=session_id,
    )
    db.add(record)
    db.flush()

    # 2. STL 理解
    stl = await run_full_stl(req.raw_text)
    sensing = stl.state_sensing
    mapping = stl.structure_mapping
    clarification = stl.language_clarification

    # 3. Decision Engine
    stability = compute_stability(sensing.tension_score, sensing.emotion_intensity)
    readiness = compute_readiness(
        clarification.clarity_score, stability, mapping.stage_position
    )
    mode = decide_mode(
        Scores(
            stability=stability,
            tension=sensing.tension_score,
            clarity=clarification.clarity_score,
            readiness=readiness,
        )
    )

    # 4. 存 STL 分析
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
    db.flush()

    # 5. 若 mode 為 C/D，跑 TST
    tst_task_row: TSTTask | None = None
    if mode in ("C", "D"):
        tst = await run_full_tst(req.raw_text, stl)
        tst_task_row = TSTTask(
            stl_analysis_id=analysis.id,
            user_id=req.user_id,
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
        db.add(tst_task_row)
        db.flush()

        user_facing = UserFacingResponse(
            hold=tst.awareness.awareness_text[:80],
            organize=tst.reframe.reframed_sentence,
            small_step=tst.action.micro_action,
            keep_choice=tst.action.keep_choice,
        )
    else:
        # mode A/B：不進 TST，用 STL 結果組一個承接/釐清版本
        user_facing = _fallback_response(mode, stl)

    # 6. 存回四段式到 STLAnalysis
    analysis.response_hold = user_facing.hold
    analysis.response_organize = user_facing.organize
    analysis.response_small_step = user_facing.small_step
    analysis.response_keep_choice = user_facing.keep_choice

    db.commit()

    return ProcessResponse(
        session_id=session_id,
        mode=mode,
        response=user_facing,
        meta={
            "scores": {
                "stability": stability,
                "tension": sensing.tension_score,
                "clarity": clarification.clarity_score,
                "readiness": readiness,
            },
            "state_label": sensing.state_label,
            "stl_analysis_id": analysis.id,
            "tst_task_id": tst_task_row.id if tst_task_row else None,
        },
    )


def _fallback_response(mode: str, stl) -> UserFacingResponse:
    """mode A/B 時的簡易四段式組法。Phase 2 可以另寫一支 prompt 強化。"""
    sensing = stl.state_sensing
    clarification = stl.language_clarification

    if mode == "A":
        return UserFacingResponse(
            hold=f"這樣的{sensing.state_label}感，確實會讓人一下子很難整理。",
            organize="聽起來像是現在有些東西疊在一起了，不用急著分開它。",
            small_step="如果願意的話，可以先只做一次深呼吸，其他都先放著。",
            keep_choice="這裡先不用急著做結論。",
        )
    # B
    return UserFacingResponse(
        hold="現在這個感覺，還不太好直接說清楚。",
        organize=(
            clarification.clarified_sentence
            or "也許你現在更接近的，是一種還沒找到語言的狀態。"
        ),
        small_step="如果願意的話，可以先試試把剛剛的感覺換成一句話寫下來。",
        keep_choice="不一定要寫得精準，先記住這個方向也可以。",
    )
