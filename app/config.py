"""應用設定 — 從環境變數載入。"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


# 路徑常數
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"
TONE_CHARTER_PATH = Path(__file__).resolve().parent / "core" / "TONE_CHARTER.md"


class Settings(BaseSettings):
    model_config = {
        "env_file": Path(__file__).resolve().parent.parent / ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }

    # App
    project_name: str = Field(default="Pathly", alias="PROJECT_NAME")
    port: int = Field(default=8000, alias="PORT")
    env: str = Field(default="development", alias="ENV")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_debug: bool = Field(default=True, alias="APP_DEBUG")
    app_host: str = "0.0.0.0"

    # Database
    database_url: str = Field(default="sqlite:///./pathly.db", alias="DATABASE_URL")

    # Google Gemini
    gemini_api_key: str = Field(default="", alias="GEMINI_API_KEY")
    gemini_model_deep: str = "gemini-2.5-flash"
    gemini_model_fast: str = "gemini-2.5-flash"

    # Tone Guard
    tone_reviewer_enabled: bool = False

    # Mock 模式：當 call_claude 還是 stub（Phase 1）時，讓 /process 回傳
    # 預先寫好的四段式範本，方便前端串接與氣質驗證。Phase 2 接 anthropic SDK 後可關掉。
    mock_ai: bool = Field(default=False, alias="MOCK_AI")

    # 端口配置
    backend_port: int = Field(default=8007, alias="BACKEND_PORT")
    frontend_port: int = Field(default=5500, alias="FRONTEND_PORT")

    @property
    def app_port(self) -> int:
        return self.port

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
