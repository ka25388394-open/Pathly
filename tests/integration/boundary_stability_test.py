#!/usr/bin/env python3
"""Level 1/2 邊界穩定性測試"""

import requests
import re

# 測試當前錯誤的 regex
CURRENT_PATTERNS = [
    {"pattern": r"我.*[很|有點|比較|還蠻|超|太]", "weight": 1.5},
    {"pattern": r"[最近|這幾天|今天|現在].*[不|沒]", "weight": 1.0},
    {"pattern": r"[感覺|覺得].*[不|有點|怪]", "weight": 1.0},
    {"pattern": r"不[太|怎麼|是很|大].*[想|好|行]", "weight": 1.0},
    {"pattern": r"[有點|一點|還蠻|比較].*[累|煩|焦慮|不安|難過]", "weight": 1.5},
    {"pattern": r"[睡|吃|頭].*不[好|了|行]", "weight": 1.0},
    {"pattern": r"[心情|狀態|精神].*[不|有點|還]", "weight": 1.0},
    {"pattern": r"[沒有|缺乏].*[動力|興趣|精神]", "weight": 1.0}
]

def test_regex_patterns():
    """測試 regex 模式匹配"""
    print("Regex Pattern Testing:")
    print("="*50)

    test_cases = [
        ("我很好", "應該不匹配，但可能錯誤匹配"),
        ("我很累", "應該匹配"),
        ("今天很棒", "應該不匹配，但可能錯誤匹配")
    ]

    for text, expected in test_cases:
        matched = []
        for i, pattern_info in enumerate(CURRENT_PATTERNS):
            if re.search(pattern_info["pattern"], text):
                matched.append(f"P{i+1}")

        print(f"'{text}': {matched} - {expected}")
    print()

def boundary_stability_test():
    """邊界穩定性測試"""

    # 應該維持 Level 1 的句子（15句）
    level_1_cases = [
        "我很好",
        "我今天不錯",
        "我想聊聊天",
        "哈囉",
        "今天很棒",
        "最近天氣很好",
        "我很開心",
        "想分享一件事",
        "剛剛喝咖啡",
        "我覺得這個很好笑",
        "謝謝你",
        "不錯呢",
        "還好啊",
        "我在工作",
        "最近忙著學習"
    ]

    # 應該是 Level 2 的弱狀態句（10句）
    level_2_cases = [
        "我今天很累",
        "最近怪怪的",
        "有點煩",
        "不太想動",
        "沒什麼力氣",
        "心情不好",
        "睡不好",
        "沒有動力",
        "感覺卡住",
        "不知道怎麼調整"
    ]

    api_url = "http://localhost:8007/api/v1/ai/support"

    print("Boundary Stability Test Results:")
    print("="*70)
    print(f"{'Input':<20} {'Expected':<8} {'Actual':<6} {'Result':<6} {'Issue'}")
    print("-"*70)

    # 測試 Level 1 案例
    level_1_errors = []
    for case in level_1_cases:
        try:
            response = requests.post(api_url, json={"message": case}, timeout=5)
            if response.status_code == 200:
                actual_level = response.json()["data"]["level"]
                result = "PASS" if actual_level == 1 else "FAIL"
                issue = "Overclassified to L2" if actual_level == 2 else ""
                if actual_level != 1:
                    level_1_errors.append(case)
            else:
                actual_level = "ERR"
                result = "FAIL"
                issue = "API Error"
        except:
            actual_level = "ERR"
            result = "FAIL"
            issue = "Connection Error"

        print(f"{case:<20} {'L1':<8} {'L'+str(actual_level):<6} {result:<6} {issue}")

    # 測試 Level 2 案例
    level_2_errors = []
    for case in level_2_cases:
        try:
            response = requests.post(api_url, json={"message": case}, timeout=5)
            if response.status_code == 200:
                actual_level = response.json()["data"]["level"]
                result = "PASS" if actual_level == 2 else "FAIL"
                issue = "Underclassified to L1" if actual_level == 1 else ""
                if actual_level != 2:
                    level_2_errors.append(case)
            else:
                actual_level = "ERR"
                result = "FAIL"
                issue = "API Error"
        except:
            actual_level = "ERR"
            result = "FAIL"
            issue = "Connection Error"

        print(f"{case:<20} {'L2':<8} {'L'+str(actual_level):<6} {result:<6} {issue}")

    print("-"*70)

    # 統計結果
    l1_accuracy = ((len(level_1_cases) - len(level_1_errors)) / len(level_1_cases)) * 100
    l2_accuracy = ((len(level_2_cases) - len(level_2_errors)) / len(level_2_cases)) * 100

    print(f"Level 1 Accuracy: {len(level_1_cases)-len(level_1_errors)}/{len(level_1_cases)} ({l1_accuracy:.1f}%)")
    print(f"Level 2 Accuracy: {len(level_2_cases)-len(level_2_errors)}/{len(level_2_cases)} ({l2_accuracy:.1f}%)")

    if level_1_errors:
        print(f"\nLevel 1 誤判案例: {level_1_errors}")
    if level_2_errors:
        print(f"Level 2 誤判案例: {level_2_errors}")

    return level_1_errors, level_2_errors

if __name__ == "__main__":
    test_regex_patterns()
    boundary_stability_test()