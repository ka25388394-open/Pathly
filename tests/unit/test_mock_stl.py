#!/usr/bin/env python3
"""測試模擬STL成功情況下的路由"""

import asyncio
from dataclasses import dataclass
from app.services.integrated_analysis_engine import IntegratedAnalysisEngine, OutputLevel

# 模擬STL結果
@dataclass
class MockSTLResult:
    """模擬STL分析結果"""
    state_sensing: any = None
    structure_mapping: any = None
    language_clarification: any = None

@dataclass
class MockStateSensing:
    current_state: str
    core_block: str
    emotion_intensity: int

async def test_level_determination():
    """測試層級決定邏輯（不調用API）"""
    print("測試層級決定邏輯")
    print("=" * 50)

    engine = IntegratedAnalysisEngine()

    test_cases = [
        {
            "name": "高情緒應該Level1",
            "input": "我快崩潰了",
            "mock_intensity": "high",
            "mock_clarity": "medium",
            "mock_pattern": "H1"
        },
        {
            "name": "低清晰度應該Level1",
            "input": "不知道怎麼說",
            "mock_intensity": "medium",
            "mock_clarity": "low",
            "mock_pattern": "H1"
        },
        {
            "name": "中等狀態應該Level2",
            "input": "我想整理一下想法",
            "mock_intensity": "low",
            "mock_clarity": "high",
            "mock_pattern": "H2"
        },
        {
            "name": "準備行動應該Level3",
            "input": "請給我具體步驟",
            "mock_intensity": "low",
            "mock_clarity": "high",
            "mock_pattern": "H2"
        }
    ]

    for test_case in test_cases:
        print(f"\n測試: {test_case['name']}")
        print(f"輸入: {test_case['input']}")

        # 模擬基礎路由結果
        class MockBasicResult:
            def __init__(self, intensity, clarity, pattern):
                self.intensity_level = intensity
                self.clarity_level = clarity
                self.dominant_pattern = pattern
                self.needs_grounding = intensity == "high"
                self.processing_ready = intensity == "low" and clarity == "high"

        basic_result = MockBasicResult(
            test_case['mock_intensity'],
            test_case['mock_clarity'],
            test_case['mock_pattern']
        )

        # 測試層級決定
        context = {"continuous_dialogue": False}
        output_level, reason = engine._determine_output_level(basic_result, context)

        print(f"決定層級: {output_level.value}")
        print(f"決定原因: {reason}")

        # 驗證邏輯
        expected_level = None
        if test_case['mock_intensity'] == "high":
            expected_level = OutputLevel.LEVEL_1_DIALOGUE
        elif test_case['mock_clarity'] == "low":
            expected_level = OutputLevel.LEVEL_1_DIALOGUE
        elif (test_case['mock_intensity'] == "low" and
              test_case['mock_clarity'] == "high" and
              test_case['mock_pattern'] == "H2"):
            if "具體步驟" in test_case['input']:
                expected_level = OutputLevel.LEVEL_3_TST_ACTION
            else:
                expected_level = OutputLevel.LEVEL_2_STL_ORGANIZE
        else:
            expected_level = OutputLevel.LEVEL_2_STL_ORGANIZE

        is_correct = output_level == expected_level
        print(f"結果: {'正確' if is_correct else '需檢查'}")

async def main():
    print("測試層級決定邏輯（不調用API）")
    await test_level_determination()
    print("\n測試完成!")

if __name__ == "__main__":
    asyncio.run(main())