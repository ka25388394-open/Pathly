"""GET /history — 使用者最近的整理紀錄。

給前端追蹤頁用：回看幾次狀態、最近的小行動、一句回顧摘要。
刻意不做統計/圖表聚合，保持「回看」氣質而非「績效儀表板」。
"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.models import StateRecord, STLAnalysis, TSTTask
from app.db.session import get_db
from app.schemas.api import HistoryItem, HistoryResponse

router = APIRouter(tags=["history"])


@router.get("/history", response_model=HistoryResponse)
def history(
    user_id: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
) -> HistoryResponse:
    if get_settings().mock_ai:
        return _mock_history()

    rows = (
        db.query(StateRecord, STLAnalysis, TSTTask)
        .outerjoin(STLAnalysis, STLAnalysis.state_record_id == StateRecord.id)
        .outerjoin(TSTTask, TSTTask.stl_analysis_id == STLAnalysis.id)
        .filter(StateRecord.user_id == user_id)
        .order_by(StateRecord.created_at.desc())
        .limit(limit)
        .all()
    )

    items: list[HistoryItem] = []
    for rec, analysis, task in rows:
        items.append(
            HistoryItem(
                state_record_id=rec.id,
                created_at=rec.created_at,
                excerpt=_excerpt(rec.raw_text),
                state_label=analysis.state_label if analysis else None,
                mode=analysis.decided_mode if analysis else None,
                small_step=(
                    task.micro_action
                    if task
                    else (analysis.response_small_step if analysis else None)
                ),
                task_status=task.status if task else None,
            )
        )

    return HistoryResponse(items=items, summary=_summarize(items))


def _excerpt(text: str, n: int = 60) -> str:
    text = text.strip().replace("\n", " ")
    return text if len(text) <= n else text[:n] + "…"


def _summarize(items: list[HistoryItem]) -> str | None:
    if not items:
        return None
    # 非 AI、非統計，單純一句「我們一起走過幾次」的回顧。
    return f"最近你整理過 {len(items)} 次，每一次都留下了一點東西。"


def _mock_history() -> HistoryResponse:
    now = datetime.now(timezone.utc)
    items = [
        HistoryItem(
            state_record_id="mock-rec-1",
            created_at=now - timedelta(hours=3),
            excerpt="今天又被同一件事卡住了，覺得自己好像在原地繞圈…",
            state_label="低壓卡住",
            mode="C",
            small_step="今晚睡前可以先寫三行今天有做到的小事，不用評價、不用長。",
            task_status="pending",
        ),
        HistoryItem(
            state_record_id="mock-rec-2",
            created_at=now - timedelta(days=1, hours=4),
            excerpt="不太知道自己是累還是沒動力，只是不想動。",
            state_label="無名感",
            mode="B",
            small_step="如果願意的話，可以先試試把剛剛的感覺換成一句話寫下來。",
            task_status="completed",
        ),
        HistoryItem(
            state_record_id="mock-rec-3",
            created_at=now - timedelta(days=3),
            excerpt="工作上的事一直懸在那邊，想完成又不想開始。",
            state_label="拖延",
            mode="C",
            small_step="只打開文件檔，看五分鐘，然後可以闔上。",
            task_status="skipped",
        ),
    ]
    return HistoryResponse(
        items=items,
        summary="最近你整理過幾次，每一次都有留下一點自己。",
    )
