"""POST /task — 任務狀態機。"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import TSTTask
from app.db.session import get_db
from app.schemas.api import TaskActionRequest, TaskActionResponse

router = APIRouter(tags=["task"])

_ALLOWED_TRANSITIONS = {
    "start": ("pending", "doing"),
    "complete": ("doing", "done"),
    "skip": ("pending", "skipped"),
}


@router.post("/task", response_model=TaskActionResponse)
def update_task(
    req: TaskActionRequest, db: Session = Depends(get_db)
) -> TaskActionResponse:
    task = db.get(TSTTask, req.tst_task_id)
    if task is None:
        raise HTTPException(404, "tst_task not found")

    expected_from, target = _ALLOWED_TRANSITIONS[req.action]
    if task.status != expected_from:
        raise HTTPException(
            409,
            f"cannot {req.action} from status '{task.status}' "
            f"(expected '{expected_from}')",
        )

    task.status = target
    if req.action == "start" and req.scheduled_at is not None:
        task.scheduled_at = req.scheduled_at
    if req.action == "complete":
        task.completed_at = datetime.now(timezone.utc)

    db.commit()
    return TaskActionResponse(tst_task_id=task.id, status=task.status)
