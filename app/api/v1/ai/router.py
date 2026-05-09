"""AI 路由器 - core-pathly-main"""

from fastapi import APIRouter
from .support import router as support_router
from .dev import router as dev_router

router = APIRouter()

# 註冊 AI support 路由（使用者模式）
router.include_router(
    support_router,
    tags=["AI Support"],
    responses={404: {"description": "Not found"}}
)

# 註冊 AI dev 路由（開發者模式）
router.include_router(
    dev_router,
    prefix="/dev",
    tags=["AI Dev Mode"],
    responses={404: {"description": "Not found"}}
)