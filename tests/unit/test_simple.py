#!/usr/bin/env python3
"""測試整合三層對話系統 - 簡化版"""

import asyncio
from app.services.integrated_dialogue_client import integrated_dialogue_client

async def test_routing():
    """測試路由邏輯"""
    print("測試 pathly 整合三層對話系統")
    print("=" * 50)

    test_cases = {
        "高情緒強度測試": "我真的很煩，整個人快炸掉了，什麼都不想碰",
        "低清晰度測試": "最近很多事情混在一起，有點說不清楚",
        "結構需求測試": "我現在有三件事要處理，但時間不夠，怎麼排比較好",
        "自我觀察測試": "我發現我每次壓力大就會逃，然後最後更糟",
        "複雜矛盾測試": "我知道我在逃，但我也覺得我需要休息，但又覺得自己是不是在找藉口"
    }

    results = {}

    for test_name, input_text in test_cases.items():
        print(f"\n測試: {test_name}")
        print(f"輸入: {input_text}")
        print("-" * 30)

        try:
            result = await integrated_dialogue_client.process_input(input_text)

            print(f"路由到: {result.level_used}")
            print(f"格式: {result.format_type}")
            print(f"信心分數: {result.confidence_score:.1f}")
            print(f"原因: {result.routing_reason}")

            # 顯示回應前100字符
            response_preview = result.response[:100] + "..." if len(result.response) > 100 else result.response
            print(f"回應: {response_preview}")

            results[test_name] = {
                "success": True,
                "level": result.level_used,
                "format": result.format_type,
                "confidence": result.confidence_score
            }

        except Exception as e:
            print(f"錯誤: {str(e)}")
            results[test_name] = {"success": False, "error": str(e)}

    print("\n" + "=" * 50)
    print("測試總結")

    successful = sum(1 for r in results.values() if r.get("success"))
    total = len(results)

    print(f"成功: {successful}/{total}")

    # 顯示路由分布
    if successful > 0:
        print("\n路由分布:")
        levels = {}
        for name, result in results.items():
            if result.get("success"):
                level = result["level"]
                levels[level] = levels.get(level, 0) + 1

        for level, count in levels.items():
            print(f"  {level}: {count} 次")

    return successful == total

async def main():
    print("啟動整合測試...")

    # 先檢查系統狀態
    try:
        status = integrated_dialogue_client.get_system_status()
        print(f"系統: {status['system_name']}")
        print(f"組件數: {len(status['components'])}")
    except Exception as e:
        print(f"系統狀態錯誤: {str(e)}")
        return

    # 執行路由測試
    success = await test_routing()

    if success:
        print("\n全部測試通過！整合系統正常運作。")
    else:
        print("\n部分測試失敗，需要檢查。")

if __name__ == "__main__":
    asyncio.run(main())