"""FastAPI entry point。"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.config import get_settings
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Phase 1：啟動時建表。Phase 2 改用 Alembic migration。
    try:
        init_db()
    except Exception as e:
        # 資料庫初始化失敗不應阻止應用啟動
        # 健康檢查仍可運作，只是資料庫功能會失效
        print(f"Warning: Database initialization failed: {e}")
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="pathly — STL × TST 語言轉化與行動系統",
        version="0.1.0",
        debug=settings.app_debug,
        lifespan=lifespan,
    )

    # MVP 階段允許本地 Next.js dev server 與直接開啟的 HTML 檔案。Phase 2 上線前需收緊白名單。
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "null",  # 允許直接開啟的 HTML 檔案
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 先註冊輕量端點
    app.include_router(api_router)

    # 懶載入重型端點的中間件
    _heavy_endpoints_loaded = False

    @app.middleware("http")
    async def lazy_load_heavy_endpoints(request, call_next):
        nonlocal _heavy_endpoints_loaded

        # 檢查是否訪問重型端點
        path = request.url.path
        heavy_paths = ["/api/v1/analyze", "/api/v1/process", "/api/v1/transform",
                      "/api/v1/history", "/api/v1/task", "/api/v1/track"]

        if not _heavy_endpoints_loaded and any(path.startswith(hp) for hp in heavy_paths):
            # 首次訪問時載入重型端點
            from app.api.v1 import register_heavy_endpoints
            register_heavy_endpoints()
            _heavy_endpoints_loaded = True

        return await call_next(request)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "pathly"}

    return app


app = create_app()
