"""POST /track — 任務追蹤與回饋。"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import TrackingLog, TSTTask
from app.db.session import get_db
from app.schemas.api import TrackRequest, TrackResponse

router = APIRouter(tags=["track"])


@router.post("/track", response_model=TrackResponse)
def track(req: TrackRequest, db: Session = Depends(get_db)) -> TrackResponse:
    task = db.get(TSTTask, req.tst_task_id)
    if task is None:
        raise HTTPException(404, "tst_task not found")

    log = TrackingLog(
        tst_task_id=task.id,
        user_id=task.user_id,
        event_type=req.event_type,
        feedback_text=req.feedback_text,
        felt_change=req.felt_change,
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    # Phase 2：根據歷史 tracking_logs 計算 pattern_progress 與 next_hint
    return TrackResponse(log_id=log.id, next_hint=None, pattern_progress=None)
