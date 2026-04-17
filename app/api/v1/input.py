"""POST /input — 收使用者原始輸入，寫入 state_records。"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import StateRecord
from app.db.session import get_db
from app.schemas.api import InputRequest, InputResponse

router = APIRouter(tags=["input"])


@router.post("/input", response_model=InputResponse, status_code=201)
def create_input(req: InputRequest, db: Session = Depends(get_db)) -> InputResponse:
    session_id = req.session_id or str(uuid.uuid4())
    record = StateRecord(
        user_id=req.user_id,
        raw_text=req.raw_text,
        session_id=session_id,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return InputResponse(
        state_record_id=record.id,
        session_id=record.session_id,
        created_at=record.created_at,
    )
