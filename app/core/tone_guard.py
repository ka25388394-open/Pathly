"""Tone Guard — 語言風格憲法的硬底線攔截層。

對應 TONE_CHARTER.md 第三章（絕對禁止句型）與第四章（四段式軟化詞要求）。
這一層是 regex 硬規則，不依賴 AI 判斷；AI 會飄，regex 不會。

使用方式：

    from pydantic import BaseModel
    from app.core.tone_guard import tone_field, soft_step_field

    class UserFacingResponse(BaseModel):
        hold: str
        organize: str
        small_step: str
        keep_choice: str

        _tone = tone_field("hold", "organize", "small_step", "keep_choice")
        _soft = soft_step_field("small_step")
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from pydantic import validator

# ---------------------------------------------------------------------------
# 第三章 — 絕對禁止句型
# ---------------------------------------------------------------------------
# 每一條 regex 對應 TONE_CHARTER.md 第三章列出的句型。
# 中文沒有詞邊界，所以用前後字元排除 + 子字串匹配的方式。
# 注意：這裡刻意寬鬆一點（寧可誤殺重試，也不要讓違規輸出到使用者眼前）。

BANNED_PATTERNS: dict[str, str] = {
    # 3.1 批判與定義式
    "judge_because": r"你就是因為",
    "judge_obvious": r"很明顯你在",
    "judge_root": r"問題根本就是",
    "judge_redefine": r"其實你不是.{0,15}你是",
    # 3.2 命令與強制式
    "cmd_should": r"你應該要",
    "cmd_must_now": r"你現在必須",
    "cmd_correct_way": r"正確做法是",
    "cmd_do_today": r"今天就去做",
    "cmd_must_finish": r"你必須完成",
    "cmd_execute_now": r"請立刻執行",
    # 3.3 空泛安慰式
    #   —「沒事的」「你很棒」「一切都會好起來」「別想那麼多」
    #   這類通常單獨成句，所以用句末/標點邊界判斷，避免誤殺
    #   例如「你很棒地把這件事整理出來」不該被擋。
    "hollow_its_ok": r"(?:^|[，。！？\s])沒事的(?:[。！？\s]|$)",
    "hollow_youre_great": r"(?:^|[，。！？\s])你很棒(?:[。！？\s]|$)",
    "hollow_will_be_fine": r"一切都會好起來",
    "hollow_dont_think": r"別想那麼多",
}

# 編譯為單一 regex 以加速掃描，同時保留命名群組以便報告具體違規條目
_BANNED_RE = re.compile(
    "|".join(f"(?P<{name}>{pat})" for name, pat in BANNED_PATTERNS.items())
)


# ---------------------------------------------------------------------------
# 第四章 — small_step 軟化詞要求
# ---------------------------------------------------------------------------
# 任務引導句必須至少包含一個軟化詞，避免滑向說教/強迫。
SOFT_WORDS: tuple[str, ...] = (
    "如果",
    "可以先",
    "願意",
    "試試",
    "不用",
    "也可以",
    "有空間",
    "先記住",
    "先只",
)

_SOFT_RE = re.compile("|".join(re.escape(w) for w in SOFT_WORDS))


# ---------------------------------------------------------------------------
# 例外
# ---------------------------------------------------------------------------
@dataclass
class ToneViolationInfo:
    """一次違規的具體資訊，用於重試 prompt 與日後統計。"""

    field_name: str
    rule: str  # 對應 BANNED_PATTERNS 的 key，或 "missing_soft_word"
    matched_text: str
    full_text: str


class ToneViolation(ValueError):
    """禁止句型或軟化詞缺失時拋出。

    attribute `info` 提供結構化細節，給 call_with_tone_guard 做重試決策用。
    """

    def __init__(self, info: ToneViolationInfo):
        self.info = info
        super().__init__(
            f"[{info.field_name}] 違反 TONE CHARTER ({info.rule}): "
            f"命中「{info.matched_text}」"
        )


# ---------------------------------------------------------------------------
# 核心檢查函式
# ---------------------------------------------------------------------------
def find_banned(text: str) -> tuple[str, str] | None:
    """回傳 (rule_name, matched_text)，無違規則回 None。"""
    if not text:
        return None
    m = _BANNED_RE.search(text)
    if not m:
        return None
    return m.lastgroup or "unknown", m.group(0)


def has_soft_word(text: str) -> bool:
    """判斷文字是否包含至少一個軟化詞。"""
    return bool(text and _SOFT_RE.search(text))


def assert_tone(text: str, field_name: str = "") -> str:
    """檢查禁止句型。違規拋 ToneViolation，通過則原樣回傳。"""
    hit = find_banned(text)
    if hit is None:
        return text
    rule, matched = hit
    raise ToneViolation(
        ToneViolationInfo(
            field_name=field_name,
            rule=rule,
            matched_text=matched,
            full_text=text,
        )
    )


def assert_soft_step(text: str, field_name: str = "small_step") -> str:
    """檢查 small_step 欄位是否包含軟化詞。"""
    if not has_soft_word(text):
        raise ToneViolation(
            ToneViolationInfo(
                field_name=field_name,
                rule="missing_soft_word",
                matched_text="",
                full_text=text,
            )
        )
    return text


def scan_all(text: str) -> list[ToneViolationInfo]:
    """非拋例外版本：回傳所有違規條目（用於離線審查 / 報表）。"""
    violations: list[ToneViolationInfo] = []
    if not text:
        return violations
    for m in _BANNED_RE.finditer(text):
        violations.append(
            ToneViolationInfo(
                field_name="",
                rule=m.lastgroup or "unknown",
                matched_text=m.group(0),
                full_text=text,
            )
        )
    return violations


# ---------------------------------------------------------------------------
# Pydantic validator 工廠
# ---------------------------------------------------------------------------
def tone_field(*fields: str):
    """Pydantic v1 validator 工廠：對指定欄位套用禁止句型檢查。

    用法：

        class Foo(BaseModel):
            text: str
            _tone = tone_field("text")
    """

    def _validator(cls, v, **kwargs):  # type: ignore[no-untyped-def]
        field_name = kwargs.get('field', {}).name if 'field' in kwargs else ''
        return assert_tone(v, field_name)

    return validator(*fields, allow_reuse=True)(_validator)


def soft_step_field(*fields: str):
    """Pydantic v1 validator 工廠：對指定欄位套用軟化詞檢查。

    專用於 small_step / micro_action 這類行動引導欄位。
    """

    def _validator(cls, v, **kwargs):  # type: ignore[no-untyped-def]
        field_name = kwargs.get('field', {}).name if 'field' in kwargs else ''
        return assert_soft_step(v, field_name)

    return validator(*fields, allow_reuse=True)(_validator)


# ---------------------------------------------------------------------------
# 對外公開介面
# ---------------------------------------------------------------------------
__all__: Iterable[str] = (
    "BANNED_PATTERNS",
    "SOFT_WORDS",
    "ToneViolation",
    "ToneViolationInfo",
    "find_banned",
    "has_soft_word",
    "assert_tone",
    "assert_soft_step",
    "scan_all",
    "tone_field",
    "soft_step_field",
)
