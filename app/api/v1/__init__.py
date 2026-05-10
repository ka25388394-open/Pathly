"""API v1 router 匯總 - 分批載入優化。"""

from fastapi import APIRouter

# 🚀 立即載入：輕量、常用的端點
from app.api.v1 import dialogue, input as input_ep
from app.api.v1.ai import ai_router

# 📦 懶載入：重型、較少使用的端點
_heavy_endpoints = [
    "analyze", "process", "transform",
    "history", "task", "track"
]

api_router = APIRouter(prefix="/api/v1")

# 立即註冊輕量端點
api_router.include_router(input_ep.router)
api_router.include_router(dialogue.router)
api_router.include_router(ai_router, prefix="/ai")


def _load_heavy_endpoint(endpoint_name: str):
    """延後載入重型端點"""
    if endpoint_name == "analyze":
        from app.api.v1 import analyze
        return analyze.router
    elif endpoint_name == "process":
        from app.api.v1 import process
        return process.router
    elif endpoint_name == "transform":
        from app.api.v1 import transform
        return transform.router
    elif endpoint_name == "history":
        from app.api.v1 import history
        return history.router
    elif endpoint_name == "task":
        from app.api.v1 import task
        return task.router
    elif endpoint_name == "track":
        from app.api.v1 import track
        return track.router


def register_heavy_endpoints():
    """註冊重型端點（首次訪問時觸發）"""
    for endpoint_name in _heavy_endpoints:
        router = _load_heavy_endpoint(endpoint_name)
        api_router.include_router(router)
