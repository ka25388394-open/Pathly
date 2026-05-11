#!/usr/bin/env python3
"""最終測試"""

import re

# 最終修正的模式
FINAL_PATTERNS = [
    {"pattern": r"我.*(很|有點|比較|還蠻|超|太).*(累|煩|痛|難受|不舒服|壓力|焦慮)", "weight": 1.5},
    {"pattern": r"(最近|這幾天|今天|現在).*(不|沒)(?!錯|壞)", "weight": 1.0},
    {"pattern": r"(感覺|覺得).*(不|有點|怪)", "weight": 1.0},
    {"pattern": r"不(太|怎麼|是很|大).*(想|好|行)", "weight": 1.0},
    {"pattern": r"(有點|一點|還蠻|比較).*(累|煩|焦慮|不安|難過)", "weight": 1.5},
    {"pattern": r"(睡|吃|頭).*不(好|了|行)", "weight": 1.0},
    {"pattern": r"(心情|狀態|精神).*(不|有點|還)", "weight": 1.0},
    {"pattern": r"(沒有|缺乏).*(動力|興趣|精神)", "weight": 1.0}
]

def final_test():
    """最終邊界測試"""

    # 關鍵測試案例
    test_cases = [
        # Level 1 (積極/中性)
        ("我很好", 1),
        ("我很開心", 1),
        ("我今天不錯", 1),  # 關鍵修正案例
        ("今天很棒", 1),

        # Level 2 (負面)
        ("我很累", 2),
        ("我今天很煩", 2),
        ("最近不太好", 2),
        ("今天沒精神", 2),
        ("感覺怪怪的", 2),
        ("不太想動", 2)
    ]

    print("Final Boundary Stability Test:")
    print("="*50)

    correct = 0
    for case, expected in test_cases:
        total_weight = 0
        matches = []

        for i, pattern_info in enumerate(FINAL_PATTERNS):
            if re.search(pattern_info["pattern"], case):
                matches.append(f"P{i+1}")
                total_weight += pattern_info["weight"]

        predicted_level = 2 if total_weight >= 1.0 else 1
        result = "PASS" if predicted_level == expected else "FAIL"

        if predicted_level == expected:
            correct += 1

        print(f"{result}: '{case}' -> L{predicted_level} (expected L{expected}), weight={total_weight:.1f}")

    accuracy = (correct / len(test_cases)) * 100
    print(f"\nFinal Accuracy: {correct}/{len(test_cases)} ({accuracy:.1f}%)")

    # 特別測試"不錯"修正
    print(f"\nSpecial test for '不錯' fix:")
    test_negative = "我今天不錯"
    pattern = r"(最近|這幾天|今天|現在).*(不|沒)(?!錯|壞)"
    match = re.search(pattern, test_negative)
    print(f"Pattern: {pattern}")
    print(f"Test case: '{test_negative}'")
    print(f"Result: {'MATCH' if match else 'NO MATCH'} (should be NO MATCH)")

if __name__ == "__main__":
    final_test()