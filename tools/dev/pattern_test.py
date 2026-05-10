#!/usr/bin/env python3
"""測試狀態模式集成效果"""

import requests

def test_pattern_integration():
    """測試狀態模式集成效果"""

    # 之前容易被錯分的邊界案例
    boundary_cases = [
        "我今天很累",        # 應該 Level 2（主觀狀態+程度）
        "最近不太好",        # 應該 Level 2（時間+否定）
        "感覺怪怪的",        # 應該 Level 2（感知+模糊狀態）
        "不太想動",          # 應該 Level 2（輕度否定）
        "有點煩",            # 應該 Level 2（程度+情緒）
        "睡不好",            # 應該 Level 2（生理+否定）
        "心情不好",          # 應該 Level 2（心理狀態）
        "沒有動力"           # 應該 Level 2（缺乏+積極詞）
    ]

    api_url = "http://localhost:8009/api/v1/ai/support"
    level_2_count = 0

    print("Pattern Integration Test Results:")
    print("="*50)

    for case in boundary_cases:
        try:
            response = requests.post(
                api_url,
                json={"message": case},
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                level = data["data"]["level"]
                patterns_score = data["data"]["analysis"].get("state_patterns_score", 0)

                if level == 2:
                    level_2_count += 1
                    status = "PASS"
                else:
                    status = "FAIL"

                print(f"{status}: '{case}' -> Level {level} (patterns: {patterns_score})")
            else:
                print(f"ERROR: '{case}' -> HTTP {response.status_code}")

        except Exception as e:
            print(f"ERROR: '{case}' -> Connection failed")

    print("-"*50)
    accuracy = (level_2_count / len(boundary_cases)) * 100
    print(f"Level 2 Detection Accuracy: {level_2_count}/{len(boundary_cases)} ({accuracy:.1f}%)")

    if accuracy >= 90:
        print("SUCCESS: Pattern integration working excellently!")
    elif accuracy >= 70:
        print("GOOD: Pattern integration working well")
    else:
        print("NEEDS WORK: Pattern integration needs adjustment")

if __name__ == "__main__":
    test_pattern_integration()