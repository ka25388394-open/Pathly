"""測試對話陪伴系統整合"""

import asyncio
import sys
from pathlib import Path

# 添加 app 路徑
sys.path.append(str(Path(__file__).parent / "app"))

from services.dialogue_ai_client import dialogue_client


async def test_dialogue_modes():
    """測試各種對話模式"""

    print("=== pathly 對話陪伴系統測試 ===\n")

    test_cases = [
        {
            "name": "A模式測試 - 高情緒強度",
            "input": "我真的很煩，整個人快炸掉了，什麼都不想碰",
            "expected_mode": "A"
        },
        {
            "name": "B模式測試 - 混亂不清楚",
            "input": "最近很多事情混在一起，有點說不清楚",
            "expected_mode": "B"
        },
        {
            "name": "C模式測試 - 需要結構",
            "input": "我現在有三件事要處理，但時間不夠，怎麼排比較好",
            "expected_mode": "C"
        },
        {
            "name": "D模式測試 - 反思模式",
            "input": "我發現我每次壓力大就會逃，然後最後更糟",
            "expected_mode": "D"
        },
        {
            "name": "複雜混合測試",
            "input": "我知道我在逃，但我也覺得我需要休息，但又覺得自己是不是在找藉口",
            "expected_mode": "D"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"測試 {i}: {test_case['name']}")
        print(f"輸入: {test_case['input']}")
        print("-" * 50)

        try:
            result = await dialogue_client.process_dialogue_input(test_case['input'])

            print(f"使用模式: {result['mode_used']} - {result['mode_name']}")
            print(f"預期模式: {test_case['expected_mode']}")
            print(f"模式正確: {'OK' if result['mode_used'] == test_case['expected_mode'] else 'NG'}")
            print(f"\n回應:")
            print(f"{result['response']}")

            # 顯示調試信息
            debug = result['debug_info']
            print(f"\n[調試信息]")
            print(f"主要模式: {debug['dominant_pattern']}")
            print(f"清晰度: {debug['clarity_level']}, 強度: {debug['intensity_level']}")
            if debug.get('processing_notes'):
                print(f"處理注意: {', '.join(debug['processing_notes'])}")

        except Exception as e:
            print(f"[ERROR] 測試失敗: {str(e)}")

        print("\n" + "="*60 + "\n")


async def test_conversation_flow():
    """測試連續對話流程"""

    print("=== 連續對話測試 ===\n")

    conversation = [
        "我最近工作壓力很大",
        "就是每天都有很多事情要做，但又做不完",
        "我想整理一下，但不知道從哪開始",
        "好，我試試先列出最急的三件事"
    ]

    for i, message in enumerate(conversation, 1):
        print(f"輪次 {i}: {message}")

        try:
            result = await dialogue_client.process_dialogue_input(message)
            print(f"模式: {result['mode_used']} | 回應: {result['response']}")
        except Exception as e:
            print(f"[ERROR] 錯誤: {str(e)}")

        print()


async def test_edge_cases():
    """測試邊界案例"""

    print("=== 邊界案例測試 ===\n")

    edge_cases = [
        "好累",  # 極短輸入
        "我不知道該說什麼...",  # 猶豫
        "一切都很好，沒什麼問題",  # 表面平靜
        "你什麼都不懂，你只是個機器",  # 挑戰性輸入
    ]

    for case in edge_cases:
        print(f"測試: {case}")
        try:
            result = await dialogue_client.process_dialogue_input(case)
            print(f"模式: {result['mode_used']} | 回應: {result['response']}\n")
        except Exception as e:
            print(f"[ERROR] 錯誤: {str(e)}\n")


async def main():
    """主測試函數"""
    print(">> 開始測試 pathly 對話陪伴系統\n")

    # 基本模式測試
    await test_dialogue_modes()

    # 連續對話測試
    await test_conversation_flow()

    # 邊界案例測試
    await test_edge_cases()

    print(">> 所有測試完成")


if __name__ == "__main__":
    asyncio.run(main())