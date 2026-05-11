#!/usr/bin/env python3
"""詳細路由診斷測試"""

import asyncio
from app.services.integrated_dialogue_client import integrated_dialogue_client

async def test_routing_details():
    """詳細測試路由邏輯"""
    print("詳細路由診斷測試")
    print("=" * 60)

    # 設計測試來觸發不同層級
    test_cases = [
        {
            "name": "極高情緒_應該Level1",
            "input": "我真的很煩，整個人快炸掉了，什麼都不想碰",
            "expected_level": "Level 1"
        },
        {
            "name": "低清晰度_應該Level1",
            "input": "最近很多事情混在一起，有點說不清楚",
            "expected_level": "Level 1"
        },
        {
            "name": "高清晰度低情緒_應該Level2或3",
            "input": "我需要整理一下我的工作計劃，有三個專案要排序，時間管理是我的挑戰",
            "expected_level": "Level 2/3"
        },
        {
            "name": "具體行動需求_應該Level3",
            "input": "我已經分析過了，現在需要具體的步驟來解決這個工作流程問題",
            "expected_level": "Level 3"
        },
        {
            "name": "冷靜且結構化_應該Level2或3",
            "input": "我想要系統性地檢視我在人際關係中的模式，這對我的生活品質有重要影響",
            "expected_level": "Level 2/3"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"輸入: {test_case['input']}")
        print(f"預期層級: {test_case['expected_level']}")
        print("-" * 50)

        try:
            result = await integrated_dialogue_client.process_input(test_case['input'])

            # 獲取詳細分析
            debug_info = integrated_dialogue_client.analysis_engine.get_debug_info(result.analysis_result)

            print(f"實際路由: {result.level_used}")
            print(f"格式類型: {result.format_type}")
            print(f"信心分數: {result.confidence_score:.1f}")
            print(f"路由原因: {result.routing_reason}")
            print(f"允許進階: {result.allow_progression}")

            print("\n詳細分析:")
            basic_routing = debug_info['basic_routing']
            print(f"  主要模式: {basic_routing['dominant_pattern']}")
            print(f"  清晰度: {basic_routing['clarity_level']}")
            print(f"  情緒強度: {basic_routing['intensity_level']}")
            print(f"  需要定錨: {basic_routing['needs_grounding']}")
            print(f"  需要釐清: {basic_routing['needs_clarification']}")

            if 'stl_analysis' in debug_info:
                print("  STL分析: 已執行")
            else:
                print("  STL分析: 未執行")

        except Exception as e:
            print(f"錯誤: {str(e)}")

    print("\n" + "=" * 60)

async def test_forced_levels():
    """測試強制不同層級"""
    print("\n強制層級測試")
    print("=" * 60)

    # 測試更極端的案例來嘗試觸發Level 2和3
    extreme_cases = [
        {
            "name": "超低情緒超高清晰度",
            "input": "我需要制定一個明確的計劃來改善我的時間管理能力，具體來說是早上六點到八點的晨間例行公事",
        },
        {
            "name": "純結構性問題",
            "input": "請幫我分析如何優化我的工作流程，我已經確定了問題點在於任務切換太頻繁",
        },
        {
            "name": "準備好行動的狀態",
            "input": "我已經思考清楚了，現在需要具體的執行步驟，請給我一個可操作的建議",
        }
    ]

    for test_case in extreme_cases:
        print(f"\n測試: {test_case['name']}")
        print(f"輸入: {test_case['input']}")
        print("-" * 30)

        try:
            # 添加模擬上下文來提示是連續對話
            context = {
                "continuous_dialogue": False,
                "interaction_count": 1
            }

            result = await integrated_dialogue_client.process_input(
                test_case['input'], context
            )

            print(f"路由結果: {result.level_used}")
            print(f"路由原因: {result.routing_reason}")

            # 檢查基礎路由分析
            basic = result.analysis_result.basic_routing
            print(f"基礎分析: 清晰度={basic.clarity_level}, 強度={basic.intensity_level}")

        except Exception as e:
            print(f"錯誤: {str(e)}")

async def main():
    print("啟動詳細路由診斷...")

    await test_routing_details()
    await test_forced_levels()

    print("\n診斷完成！")

if __name__ == "__main__":
    asyncio.run(main())