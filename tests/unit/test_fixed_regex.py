#!/usr/bin/env python3
"""測試修正後的 regex"""

import re

# 修正後的模式（正確語法）
FIXED_PATTERNS = [
    {"pattern": r"我.*(很|有點|比較|還蠻|超|太)", "weight": 1.5},
    {"pattern": r"(最近|這幾天|今天|現在).*(不|沒)", "weight": 1.0},
    {"pattern": r"(感覺|覺得).*(不|有點|怪)", "weight": 1.0},
    {"pattern": r"不(太|怎麼|是很|大).*(想|好|行)", "weight": 1.0},
    {"pattern": r"(有點|一點|還蠻|比較).*(累|煩|焦慮|不安|難過)", "weight": 1.5},
    {"pattern": r"(睡|吃|頭).*不(好|了|行)", "weight": 1.0},
    {"pattern": r"(心情|狀態|精神).*(不|有點|還)", "weight": 1.0},
    {"pattern": r"(沒有|缺乏).*(動力|興趣|精神)", "weight": 1.0}
]

# 錯誤的模式（原始錯誤語法）
OLD_PATTERNS = [
    {"pattern": r"我.*[很|有點|比較|還蠻|超|太]", "weight": 1.5},
    {"pattern": r"[最近|這幾天|今天|現在].*[不|沒]", "weight": 1.0}
]

def test_regex_fix():
    """測試 regex 修正效果"""

    # Level 1 測試案例（應該不匹配）
    level_1_cases = [
        "我很好",
        "我很開心",
        "我今天不錯",
        "今天很棒",
        "最近天氣很好"
    ]

    # Level 2 測試案例（應該匹配）
    level_2_cases = [
        "我很累",
        "我今天很煩",
        "最近不太好",
        "今天沒精神"
    ]

    print("Regex Fix Test Results:")
    print("="*60)
    print(f"{'Case':<15} {'Old Pattern':<12} {'Fixed Pattern':<15} {'Expected'}")
    print("-"*60)

    # 測試 Level 1 案例（應該減少誤匹配）
    for case in level_1_cases:
        old_matches = sum(1 for p in OLD_PATTERNS if re.search(p["pattern"], case))
        fixed_matches = sum(1 for p in FIXED_PATTERNS if re.search(p["pattern"], case))
        expected = "No matches"

        old_result = f"{old_matches} matches" if old_matches > 0 else "No matches"
        fixed_result = f"{fixed_matches} matches" if fixed_matches > 0 else "No matches"

        print(f"{case:<15} {old_result:<12} {fixed_result:<15} {expected}")

    print()

    # 測試 Level 2 案例（應該保持匹配）
    for case in level_2_cases:
        old_matches = sum(1 for p in OLD_PATTERNS if re.search(p["pattern"], case))
        fixed_matches = sum(1 for p in FIXED_PATTERNS if re.search(p["pattern"], case))
        expected = "Should match"

        old_result = f"{old_matches} matches" if old_matches > 0 else "No matches"
        fixed_result = f"{fixed_matches} matches" if fixed_matches > 0 else "No matches"

        print(f"{case:<15} {old_result:<12} {fixed_result:<15} {expected}")

    # 詳細測試問題案例
    print("\nDetailed Pattern Analysis:")
    print("-"*40)

    test_case = "我很好"
    print(f"Testing: '{test_case}'")

    # 錯誤模式
    old_pattern = r"我.*[很|有點|比較|還蠻|超|太]"
    old_match = re.search(old_pattern, test_case)
    print(f"Old pattern: {old_pattern}")
    print(f"Old result: {'MATCH' if old_match else 'NO MATCH'}")
    if old_match:
        print(f"  Matched: '{old_match.group()}'")

    # 修正模式
    new_pattern = r"我.*(很|有點|比較|還蠻|超|太)"
    new_match = re.search(new_pattern, test_case)
    print(f"Fixed pattern: {new_pattern}")
    print(f"Fixed result: {'MATCH' if new_match else 'NO MATCH'}")
    if new_match:
        print(f"  Matched: '{new_match.group()}'")

if __name__ == "__main__":
    test_regex_fix()