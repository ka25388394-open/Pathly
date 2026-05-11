#!/usr/bin/env python3
"""Level 判斷回歸測試"""

import requests
import json

def run_regression_test():
    """執行回歸測試"""

    # 測試案例：(輸入, 預期 Level, 原因)
    test_cases = [
        ("今天還不錯，想聊聊天", 1, "積極正面，輕鬆聊天"),
        ("我今天很累", 2, "情感表達，需要陪伴"),
        ("我最近工作很累，也不知道怎麼調整", 2, "有困擾和求助，需要整理"),
        ("我覺得自己很沒用，真的快撐不下去了", 3, "低自我價值，深度痛苦"),
        ("哈囉", 1, "簡單問候")
    ]

    print("=" * 60)
    print("Pathly Level 判斷回歸測試")
    print("=" * 60)

    results = []
    api_url = "http://localhost:8007/api/v1/ai/support"

    for i, (message, expected_level, reason) in enumerate(test_cases, 1):
        print(f"\n測試案例 {i}:")
        print(f"輸入: {message}")
        print(f"預期: Level {expected_level} ({reason})")

        try:
            # 發送請求
            payload = {"message": message}
            response = requests.post(api_url, json=payload, timeout=5)

            if response.status_code == 200:
                data = response.json()
                actual_level = data["data"]["level"]
                response_msg = data["data"]["response"]["message"]
                keywords = data["data"]["analysis"]["keywords"]

                print(f"實際: Level {actual_level}")
                print(f"關鍵字: {keywords}")
                print(f"回應: {response_msg[:40]}...")

                # 判斷結果
                if actual_level == expected_level:
                    result = "[PASS]"
                    status = "pass"
                else:
                    result = "[FAIL]"
                    status = "fail"

                print(f"結果: {result}")

                results.append({
                    "case": i,
                    "message": message,
                    "expected": expected_level,
                    "actual": actual_level,
                    "status": status,
                    "keywords": keywords
                })

            else:
                print(f"[FAIL] API ERROR: {response.status_code}")
                print(f"Response: {response.text}")
                results.append({
                    "case": i,
                    "message": message,
                    "expected": expected_level,
                    "actual": None,
                    "status": "error"
                })

        except Exception as e:
            print(f"[FAIL] REQUEST ERROR: {e}")
            results.append({
                "case": i,
                "message": message,
                "expected": expected_level,
                "actual": None,
                "status": "error"
            })

    # 輸出總結
    print("\n" + "=" * 60)
    print("測試總結")
    print("=" * 60)

    pass_count = sum(1 for r in results if r["status"] == "pass")
    fail_count = sum(1 for r in results if r["status"] == "fail")
    error_count = sum(1 for r in results if r["status"] == "error")

    print(f"總測試案例: {len(results)}")
    print(f"通過: {pass_count}")
    print(f"失敗: {fail_count}")
    print(f"錯誤: {error_count}")

    # 分析失敗案例
    if fail_count > 0:
        print(f"\n失敗案例分析:")
        for result in results:
            if result["status"] == "fail":
                print(f"- 案例 {result['case']}: '{result['message']}'")
                print(f"  預期 Level {result['expected']}, 實際 Level {result['actual']}")
                print(f"  關鍵字: {result.get('keywords', [])}")

                # 提供修正建議
                suggestion = analyze_failure(result)
                print(f"  建議: {suggestion}")

    return results

def analyze_failure(result):
    """分析失敗原因並提供建議"""
    message = result["message"]
    expected = result["expected"]
    actual = result["actual"]
    keywords = result.get("keywords", [])

    if expected > actual:
        # 實際 Level 比預期低
        if expected == 2 and actual == 1:
            return "可能需要增加 Level 2 關鍵字權重或降低門檻"
        elif expected == 3 and actual < 3:
            return "可能需要增加 Level 3 關鍵字或調整低自我價值檢測"
    elif expected < actual:
        # 實際 Level 比預期高
        if expected == 1 and actual == 2:
            return "可能需要增加 Level 1 正面關鍵字權重"
        elif expected == 2 and actual == 3:
            return "可能 Level 3 門檻過低，需要調高"

    return "需要進一步分析關鍵字匹配邏輯"

if __name__ == "__main__":
    run_regression_test()