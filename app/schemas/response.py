"""UserFacingResponse — 四段式使用者可見回應。

這是整個系統對使用者的最終輸出格式，嚴格對應 TONE_CHARTER 第四章。
所有欄位都經過 tone_guard 檢查，small_step 還要通過軟化詞檢查。
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.core.tone_guard import soft_step_field, tone_field


class UserFacingResponse(BaseModel):
    """四段式使用者可見回應（hold → organize → small_step → keep_choice）。"""

    hold: str = Field(max_length=80, description="先承接：一句話，不批判不解釋")
    organize: str = Field(description="再整理：溫和、不絕對")
    small_step: str = Field(description="再一小步：只給一個方向，含軟化詞")
    keep_choice: str = Field(description="留選擇權：保留主導權")

    _tone = tone_field("hold", "organize", "small_step", "keep_choice")
    _soft = soft_step_field("small_step")
