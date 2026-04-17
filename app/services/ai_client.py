"""AI Client — 封裝 Claude 呼叫 + prompt 注入 + tone guard 重試。

Phase 1 stub：
- `build_prompt` 完整實作（讀 prompt 檔、注入 TONE_CHARTER、組 messages）
- `call_claude` 是可換掉的鉤子，預設拋 NotImplementedError
- `call_with_tone_guard` 實作完整的違規重試邏輯（給真實呼叫用）

Phase 2 才接上真的 anthropic SDK。
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

from app.config import PROMPTS_DIR, TONE_CHARTER_PATH, get_settings
from app.core.tone_guard import ToneViolation

T = TypeVar("T", bound=BaseModel)


@lru_cache(maxsize=1)
def load_tone_charter() -> str:
    """讀取憲法檔。cache 住避免每次呼叫都讀檔。"""
    return TONE_CHARTER_PATH.read_text(encoding="utf-8")


@lru_cache(maxsize=16)
def load_prompt_template(task_name: str) -> str:
    """讀取某一支 prompt 的模板檔。"""
    path = PROMPTS_DIR / f"{task_name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Prompt not found: {path}")
    return path.read_text(encoding="utf-8")


def build_prompt(task_name: str, user_payload: dict[str, Any]) -> list[dict[str, Any]]:
    """組出 Claude messages 格式（含 prompt cache 標記）。

    TONE_CHARTER 放在 system content 的 cache breakpoint 內，
    同一使用者後續呼叫 cache hit 可省 90% input token。
    """
    template = load_prompt_template(task_name)
    system_text = template.replace("{{TONE_CHARTER}}", load_tone_charter())

    return [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": system_text,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
        },
        {
            "role": "user",
            "content": json.dumps(user_payload, ensure_ascii=False),
        },
    ]


async def call_llm(
    messages: list[dict[str, Any]], *, model: str | None = None
) -> str:
    """實際呼叫 LLM API。現用 Google Gemini（便宜、穩定、品質好）。

    回傳值是 assistant 的純文字內容（預期為 JSON 字串）。
    """
    import google.generativeai as genai

    settings = get_settings()
    chosen_model = model or settings.gemini_model_fast  # Flash 版本，極便宜

    if not settings.gemini_api_key:
        raise ValueError(
            "GEMINI_API_KEY not set. Get one at: https://aistudio.google.com/app/apikey"
        )

    genai.configure(api_key=settings.gemini_api_key)

    try:
        # Convert messages to Gemini format
        prompt_parts = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            # Handle Claude's cache_control format if present
            if isinstance(content, list):
                text_content = ""
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_content += block.get("text", "")
                content = text_content

            if role == "system":
                prompt_parts.append(f"System Instructions:\n{content}\n")
            elif role == "user":
                prompt_parts.append(f"User Input:\n{content}\n")

        full_prompt = "\n".join(prompt_parts)

        model_instance = genai.GenerativeModel(
            model_name=chosen_model,
            generation_config=genai.GenerationConfig(
                temperature=0.2,
                max_output_tokens=2048,
                candidate_count=1,
            )
        )

        response = await model_instance.generate_content_async(full_prompt)

        if not response.text:
            raise ValueError("Empty response from Gemini")

        # Strip markdown code blocks if present
        result = response.text.strip()
        if result.startswith("```json") and result.endswith("```"):
            result = result[7:-3].strip()  # Remove ```json and ```
        elif result.startswith("```") and result.endswith("```"):
            result = result[3:-3].strip()  # Remove generic ```

        return result

    except Exception as e:
        # More specific error handling for common Gemini issues
        error_msg = str(e)
        if "API_KEY" in error_msg.upper():
            raise ValueError("Invalid Gemini API key. Get one at: https://aistudio.google.com/app/apikey") from e
        elif "QUOTA" in error_msg.upper() or "quota" in error_msg:
            raise RuntimeError("Gemini API quota exceeded. Check usage limits.") from e
        elif "SAFETY" in error_msg.upper():
            raise RuntimeError("Content blocked by Gemini safety filters. Try rephrasing.") from e
        else:
            raise RuntimeError(f"Gemini API error: {e}") from e


# 向後相容別名
call_claude = call_llm


async def call_with_tone_guard(
    task: str,
    payload: dict[str, Any],
    schema: type[T],
    *,
    max_retry: int = 2,
    model: str | None = None,
) -> T:
    """呼叫 Claude、解析 JSON、用 schema 驗證（含 tone_guard）。

    若觸發 ToneViolation：把違規訊息回注給 AI，要求依 TONE CHARTER 重寫，
    最多重試 `max_retry` 次。Pydantic 格式錯誤也同樣重試。
    """
    settings = get_settings()
    chosen_model = model or settings.gemini_model_deep
    current_payload = dict(payload)

    last_error: Exception | None = None
    for attempt in range(max_retry + 1):
        messages = build_prompt(task, current_payload)
        raw = await call_llm(messages, model=chosen_model)
        try:
            return schema.model_validate_json(raw)
        except (ToneViolation, ValidationError) as e:
            last_error = e
            if attempt == max_retry:
                break
            reason = str(e)
            current_payload = {
                **payload,
                "_retry_reason": (
                    f"上次輸出違反規格或 TONE CHARTER：{reason}. "
                    f"請依照 TONE CHARTER 重寫，特別是第三章禁止句型與四段式結構。"
                ),
            }

    assert last_error is not None
    raise last_error
