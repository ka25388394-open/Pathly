#!/usr/bin/env python3
"""測試整合三層對話系統"""

import asyncio
import json
from app.services.integrated_dialogue_client import integrated_dialogue_client

async def test_three_level_system():
    """測試三層對話系統"""

    print("🎯 測試 pathly 整合三層對話系統")
    print("=" * 60)

    # 測試案例設計來驗證不同路由路徑
    test_cases = {
        "高情緒強度_應走Level1": "我真的很煩，整個人快炸掉了，什麼都不想碰",
        "低清晰度_應走Level1": "最近很多事情混在一起，有點說不清楚",
        "結構需求_可能Level2或3": "我現在有三件事要處理，但時間不夠，怎麼排比較好",
        "自我觀察_可能Level2": "我發現我每次壓力大就會逃，然後最後更糟",
        "複雜矛盾_可能Level1或2": "我知道我在逃，但我也覺得我需要休息，但又覺得自己是不是在找藉口"
    }

    results = {}

    for test_name, input_text in test_cases.items():
        print(f"\n🧪 測試: {test_name}")
        print(f"輸入: {input_text}")
        print("-" * 40)

        try:
            result = await integrated_dialogue_client.process_input(input_text)

            print(f"✅ 成功路由到: {result.level_used}")
            print(f"📝 格式類型: {result.format_type}")
            print(f"🎯 信心分數: {result.confidence_score:.1f}")
            print(f"📋 路由原因: {result.routing_reason}")
            print(f"🔄 允許進階: {result.allow_progression}")

            # 顯示回應前100字符
            response_preview = result.response[:100] + "..." if len(result.response) > 100 else result.response
            print(f"💬 回應預覽: {response_preview}")

            if result.next_suggestions:
                print(f"💡 下一步建議: {', '.join(result.next_suggestions)}")

            results[test_name] = {
                "success": True,
                "level": result.level_used,
                "format": result.format_type,
                "confidence": result.confidence_score,
                "reason": result.routing_reason,
                "response_length": len(result.response)
            }

        except Exception as e:
            print(f"❌ 錯誤: {str(e)}")
            results[test_name] = {
                "success": False,
                "error": str(e)
            }

    print("\n" + "=" * 60)
    print("📊 測試總結")

    successful_tests = [name for name, result in results.items() if result.get("success")]
    failed_tests = [name for name, result in results.items() if not result.get("success")]

    print(f"✅ 成功: {len(successful_tests)}/{len(test_cases)}")
    print(f"❌ 失敗: {len(failed_tests)}")

    if successful_tests:
        print("\n🎯 路由分布:")
        level_counts = {}
        for name in successful_tests:
            level = results[name]["level"]
            level_counts[level] = level_counts.get(level, 0) + 1

        for level, count in level_counts.items():
            print(f"  {level}: {count} 次")

    if failed_tests:
        print(f"\n❌ 失敗的測試: {', '.join(failed_tests)}")

    return results

async def test_system_status():
    """測試系統狀態"""
    print("\n🔧 系統狀態檢查")
    print("-" * 40)

    try:
        status = integrated_dialogue_client.get_system_status()
        print("✅ 系統狀態正常")
        print(f"📋 系統名稱: {status['system_name']}")
        print(f"🔧 組件數量: {len(status['components'])}")
        print(f"📊 功能層級: {len(status['levels'])}")
        print(f"⚡ 特色功能: {len(status['features'])}")
        return True
    except Exception as e:
        print(f"❌ 系統狀態檢查失敗: {str(e)}")
        return False

async def main():
    """主測試函數"""
    print("🚀 pathly 整合對話系統 - 全面測試")
    print("=" * 60)

    # 1. 系統狀態檢查
    system_ok = await test_system_status()

    if not system_ok:
        print("❌ 系統狀態檢查失敗，跳過功能測試")
        return

    # 2. 三層對話系統測試
    results = await test_three_level_system()

    # 3. 輸出最終結果
    print(f"\n🏁 測試完成！")

    success_rate = len([r for r in results.values() if r.get("success")]) / len(results) * 100
    print(f"📈 成功率: {success_rate:.1f}%")

    if success_rate == 100:
        print("🎉 所有測試通過！整合系統運作正常！")
    elif success_rate >= 80:
        print("✅ 大部分測試通過，系統基本正常")
    else:
        print("⚠️ 有較多測試失敗，需要檢查系統")

if __name__ == "__main__":
    asyncio.run(main())