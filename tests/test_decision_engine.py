"""Decision Engine 單元測試 — 四條路徑的邊界條件。

這是純規則層，任何改動都要先確保這組測試通過。
"""

from __future__ import annotations

import pytest

from app.services.decision_engine import (
    Scores,
    compute_readiness,
    compute_stability,
    decide_mode,
    next_step_for_mode,
)


class TestComputeStability:
    def test_low_tension_low_emotion(self):
        assert compute_stability(10, 10) == 90

    def test_high_tension_high_emotion(self):
        assert compute_stability(100, 100) == 0

    def test_mid(self):
        # 100 - 50*0.6 - 50*0.4 = 50
        assert compute_stability(50, 50) == 50

    def test_clamped(self):
        """公式理論最小是 0，不會變負數。"""
        assert compute_stability(100, 100) >= 0


class TestComputeReadiness:
    def test_preparing_action_high_clarity(self):
        # 80*0.5 + 80*0.3 + 90*0.2 = 40 + 24 + 18 = 82
        assert compute_readiness(80, 80, "準備行動") == 82

    def test_stuck_mid_clarity(self):
        # 50*0.5 + 50*0.3 + 50*0.2 = 25 + 15 + 10 = 50
        assert compute_readiness(50, 50, "卡住") == 50

    def test_unknown_stage_defaults_to_30(self):
        # 50*0.5 + 50*0.3 + 30*0.2 = 25 + 15 + 6 = 46
        assert compute_readiness(50, 50, "不存在的階段") == 46


class TestDecideMode:
    # ---- A：情緒高壓 ----
    def test_high_tension_returns_A(self):
        scores = Scores(stability=60, tension=85, clarity=80, readiness=80)
        assert decide_mode(scores) == "A"

    def test_very_low_stability_returns_A(self):
        scores = Scores(stability=20, tension=60, clarity=80, readiness=80)
        assert decide_mode(scores) == "A"

    def test_tension_exactly_80_is_A(self):
        """邊界：tension == 80 應該進 A。"""
        scores = Scores(stability=50, tension=80, clarity=80, readiness=80)
        assert decide_mode(scores) == "A"

    def test_stability_exactly_25_is_A(self):
        """邊界：stability == 25 應該進 A。"""
        scores = Scores(stability=25, tension=50, clarity=80, readiness=80)
        assert decide_mode(scores) == "A"

    # ---- B：語言不清 ----
    def test_low_clarity_returns_B(self):
        scores = Scores(stability=60, tension=40, clarity=30, readiness=60)
        assert decide_mode(scores) == "B"

    def test_clarity_49_returns_B(self):
        scores = Scores(stability=60, tension=40, clarity=49, readiness=60)
        assert decide_mode(scores) == "B"

    def test_clarity_50_does_not_return_B(self):
        """邊界：clarity == 50 不再是 B。"""
        scores = Scores(stability=60, tension=40, clarity=50, readiness=60)
        assert decide_mode(scores) != "B"

    # ---- D：就緒行動 ----
    def test_high_readiness_and_clarity_returns_D(self):
        scores = Scores(stability=70, tension=30, clarity=80, readiness=80)
        assert decide_mode(scores) == "D"

    def test_readiness_75_clarity_75_is_D(self):
        """邊界：兩個都剛好在門檻。"""
        scores = Scores(stability=70, tension=30, clarity=75, readiness=75)
        assert decide_mode(scores) == "D"

    def test_high_readiness_but_clarity_below_75_is_C(self):
        scores = Scores(stability=70, tension=30, clarity=70, readiness=80)
        assert decide_mode(scores) == "C"

    # ---- C：預設 ----
    def test_typical_middle_returns_C(self):
        scores = Scores(stability=55, tension=50, clarity=60, readiness=55)
        assert decide_mode(scores) == "C"


class TestNextStep:
    @pytest.mark.parametrize(
        "mode,expected",
        [
            ("A", "hold"),
            ("B", "clarify"),
            ("C", "transform"),
            ("D", "action"),
        ],
    )
    def test_next_step_mapping(self, mode, expected):
        assert next_step_for_mode(mode) == expected


class TestScoresValidation:
    def test_rejects_out_of_range(self):
        with pytest.raises(ValueError):
            Scores(stability=150, tension=50, clarity=50, readiness=50)

    def test_rejects_negative(self):
        with pytest.raises(ValueError):
            Scores(stability=50, tension=-1, clarity=50, readiness=50)
