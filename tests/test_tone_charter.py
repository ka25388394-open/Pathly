"""Golden set 測試 — TONE CHARTER v1.0 合規性驗證。

對應 app/core/TONE_CHARTER.md 第三章（禁止句型）與第四章（軟化詞規則）。

這份測試是整個系統的 regression suite：
- 未來修改 tone_guard.py 或 TONE_CHARTER.md 都要先跑這組
- 新增禁止句型時，對應的 BAD/GOOD sample 也要補上
- 使用者回饋「這句話讓我感到被批判」時，該句子應該被加進 BAD_SAMPLES

執行：
    pytest tests/test_tone_charter.py -v
"""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from app.core.tone_guard import (
    BANNED_PATTERNS,
    SOFT_WORDS,
    ToneViolation,
    assert_soft_step,
    assert_tone,
    find_banned,
    has_soft_word,
    scan_all,
    soft_step_field,
    tone_field,
)


# ---------------------------------------------------------------------------
# BAD SAMPLES — 每一條都必須被攔截
# ---------------------------------------------------------------------------
# 結構：(句子, 期望命中的規則名稱)
# 新增禁止句型時，請同步補一筆 BAD + 一筆 GOOD 對照。

BAD_SAMPLES: list[tuple[str, str]] = [
    # 3.1 批判與定義式
    ("你就是因為太害怕失敗才不敢開始", "judge_because"),
    ("很明顯你在逃避這個問題", "judge_obvious"),
    ("問題根本就是你沒有認真看待", "judge_root"),
    ("其實你不是累，你是在用忙碌逃避", "judge_redefine"),
    # 3.2 命令與強制式
    ("你應該要停止拖延", "cmd_should"),
    ("你現在必須做出決定", "cmd_must_now"),
    ("正確做法是面對它", "cmd_correct_way"),
    ("今天就去做這件事", "cmd_do_today"),
    ("你必須完成這份清單", "cmd_must_finish"),
    ("請立刻執行這個任務", "cmd_execute_now"),
    # 3.3 空泛安慰式
    ("沒事的。", "hollow_its_ok"),
    ("別擔心，你很棒。", "hollow_youre_great"),
    ("一切都會好起來的", "hollow_will_be_fine"),
    ("別想那麼多了", "hollow_dont_think"),
]


# ---------------------------------------------------------------------------
# GOOD SAMPLES — 符合憲法的句子，必須全部通過
# ---------------------------------------------------------------------------
# 包含：四段式各段的典型句、容易誤殺的邊界 case
GOOD_SAMPLES: list[str] = [
    # hold（承接）
    "這樣的卡住感，確實會讓人很難一下子整理清楚。",
    "當一件事同時牽動感受和判斷時，本來就不太容易立刻說明白。",
    "你現在不是沒有在想，而是想的東西可能疊在一起了。",
    # organize（整理）
    "聽起來像是你現在更接近的是一種想動又動不了的狀態。",
    "也許你現在更接近的，可能不是做不到，而是把自己的價值跟產出綁得很近。",
    "有一種可能是，你正在經歷一段還沒找到語言的時期。",
    "這不一定完全準確，但可能碰到一部分核心。",
    # small_step（一小步）
    "如果願意的話，今晚可以先寫三行今天做到的小事。",
    "你可以先只看這一小部分，不用一次處理全部。",
    "這一步不用做得漂亮，只要開始碰到就夠了。",
    "今天如果有空間，可以先試這一步。",
    # keep_choice（留選擇權）
    "不一定要今天就開始，先記住這個方向也可以。",
    "你不一定現在就要做決定。",
    "這裡先不用急著做結論。",
    # 邊界 case：包含「棒」字但不是「你很棒。」孤句
    "你很棒地把這件事整理出來了，我們可以從這裡繼續往下看。",
    # 邊界 case：句子中間有「應該」但不是「你應該要」
    "這裡應該還有別的可能性，我們先慢慢看。",
]


# ---------------------------------------------------------------------------
# Test: 禁止句型攔截
# ---------------------------------------------------------------------------
class TestBannedPatterns:
    @pytest.mark.parametrize("text,expected_rule", BAD_SAMPLES)
    def test_banned_sample_is_caught(self, text: str, expected_rule: str):
        """每一條 BAD_SAMPLE 都應該被 assert_tone 攔截，且命中正確的規則。"""
        with pytest.raises(ToneViolation) as exc_info:
            assert_tone(text, field_name="test")
        assert exc_info.value.info.rule == expected_rule, (
            f"句子「{text}」期望命中 {expected_rule}，"
            f"實際命中 {exc_info.value.info.rule}"
        )

    @pytest.mark.parametrize("text", GOOD_SAMPLES)
    def test_good_sample_passes(self, text: str):
        """每一條 GOOD_SAMPLE 都必須順利通過，不得誤殺。"""
        assert assert_tone(text, field_name="test") == text

    def test_empty_string_passes(self):
        """空字串不應觸發檢查。"""
        assert assert_tone("", field_name="test") == ""

    def test_find_banned_returns_none_for_clean_text(self):
        assert find_banned("這是一句完全乾淨的話。") is None

    def test_find_banned_returns_rule_and_match(self):
        result = find_banned("你應該要停下來")
        assert result is not None
        rule, matched = result
        assert rule == "cmd_should"
        assert "你應該要" in matched

    def test_violation_info_contains_full_context(self):
        text = "你就是因為怕失敗才這樣"
        with pytest.raises(ToneViolation) as exc_info:
            assert_tone(text, field_name="organize")
        info = exc_info.value.info
        assert info.field_name == "organize"
        assert info.rule == "judge_because"
        assert info.full_text == text
        assert "你就是因為" in info.matched_text


# ---------------------------------------------------------------------------
# Test: 涵蓋率 — 每一條 BANNED_PATTERNS 都至少有一筆 BAD_SAMPLE
# ---------------------------------------------------------------------------
class TestCoverage:
    def test_every_banned_rule_has_a_sample(self):
        """防止新增禁止句型時忘記寫測試。"""
        covered_rules = {rule for _, rule in BAD_SAMPLES}
        all_rules = set(BANNED_PATTERNS.keys())
        missing = all_rules - covered_rules
        assert not missing, (
            f"這些禁止句型規則沒有對應的 BAD_SAMPLE：{missing}。"
            f"請在 BAD_SAMPLES 補上測試句。"
        )


# ---------------------------------------------------------------------------
# Test: 軟化詞檢查（small_step 專用）
# ---------------------------------------------------------------------------
class TestSoftStep:
    @pytest.mark.parametrize(
        "text",
        [
            "如果願意的話，今晚寫三行就好。",
            "可以先只碰一點點。",
            "今天不用做完，記住方向就夠了。",
            "試試在睡前寫一行。",
            "也可以從最小的一步開始。",
        ],
    )
    def test_soft_step_passes_with_soft_word(self, text: str):
        assert assert_soft_step(text) == text

    @pytest.mark.parametrize(
        "text",
        [
            "今晚寫三行今天做到的事。",
            "睡前做一次深呼吸。",
            "把手邊的任務列出來。",
        ],
    )
    def test_soft_step_rejects_without_soft_word(self, text: str):
        with pytest.raises(ToneViolation) as exc_info:
            assert_soft_step(text)
        assert exc_info.value.info.rule == "missing_soft_word"

    def test_has_soft_word_positive(self):
        assert has_soft_word("如果你願意") is True

    def test_has_soft_word_negative(self):
        assert has_soft_word("你必須完成") is False

    def test_soft_words_list_non_empty(self):
        assert len(SOFT_WORDS) > 0


# ---------------------------------------------------------------------------
# Test: scan_all 非拋例外介面
# ---------------------------------------------------------------------------
class TestScanAll:
    def test_scan_all_empty_text(self):
        assert scan_all("") == []

    def test_scan_all_clean_text(self):
        assert scan_all("這是一句乾淨的話。") == []

    def test_scan_all_single_violation(self):
        result = scan_all("你應該要試試看")
        assert len(result) == 1
        assert result[0].rule == "cmd_should"

    def test_scan_all_multiple_violations(self):
        """同一段話命中多條規則時，應該全部回報。"""
        text = "你應該要停下來，因為你現在必須做決定。"
        result = scan_all(text)
        rules = {v.rule for v in result}
        assert "cmd_should" in rules
        assert "cmd_must_now" in rules


# ---------------------------------------------------------------------------
# Test: Pydantic validator 整合
# ---------------------------------------------------------------------------
class _SampleResponse(BaseModel):
    """模擬真實的四段式輸出 schema。"""

    hold: str
    organize: str
    small_step: str
    keep_choice: str

    _tone = tone_field("hold", "organize", "small_step", "keep_choice")
    _soft = soft_step_field("small_step")


class TestPydanticIntegration:
    def test_clean_response_passes(self):
        resp = _SampleResponse(
            hold="這樣的卡住感，確實會讓人很難一下子整理清楚。",
            organize="聽起來像是你現在更接近的是一種想動又動不了的狀態。",
            small_step="如果願意的話，今晚可以先寫三行今天做到的小事。",
            keep_choice="不一定要今天就開始，先記住這個方向也可以。",
        )
        assert resp.small_step.startswith("如果願意")

    def test_banned_in_organize_rejected(self):
        with pytest.raises(ValidationError) as exc_info:
            _SampleResponse(
                hold="這樣的卡住感確實不好說。",
                organize="你就是因為太害怕失敗才這樣。",
                small_step="如果願意的話，可以先寫一行。",
                keep_choice="不用今天完成。",
            )
        assert "judge_because" in str(exc_info.value) or "你就是因為" in str(
            exc_info.value
        )

    def test_banned_in_small_step_rejected(self):
        with pytest.raises(ValidationError):
            _SampleResponse(
                hold="這樣的卡住感確實不好說。",
                organize="聽起來像是你現在有點疊在一起了。",
                small_step="你必須完成這個任務。",
                keep_choice="不用今天就做。",
            )

    def test_small_step_missing_soft_word_rejected(self):
        """即使沒有禁止句型，small_step 缺軟化詞也要被擋。"""
        with pytest.raises(ValidationError) as exc_info:
            _SampleResponse(
                hold="這樣的卡住感確實不好說。",
                organize="聽起來像是你正在經歷一段不太好命名的時期。",
                small_step="今晚寫三行今天做到的事。",  # 缺軟化詞
                keep_choice="先記住這個方向也可以。",
            )
        assert "missing_soft_word" in str(exc_info.value) or "small_step" in str(
            exc_info.value
        )

    def test_banned_in_hold_rejected(self):
        with pytest.raises(ValidationError):
            _SampleResponse(
                hold="沒事的。",
                organize="聽起來像是你有些疊在一起了。",
                small_step="如果願意，可以先寫一行。",
                keep_choice="先記住也可以。",
            )
