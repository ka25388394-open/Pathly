#!/usr/bin/env python3
"""調試狀態模式匹配"""

import re

# 狀態描述語言模式（Level 2 專用）
STATE_PATTERNS = [
    {"pattern": r"我.*[很|有點|比較|還蠻|超|太]", "weight": 1.5},
    {"pattern": r"[最近|這幾天|今天|現在].*[不|沒]", "weight": 1.0},
    {"pattern": r"[感覺|覺得].*[不|有點|怪]", "weight": 1.0},
    {"pattern": r"不[太|怎麼|是很|大].*[想|好|行]", "weight": 1.0},
    {"pattern": r"[有點|一點|還蠻|比較].*[累|煩|焦慮|不安|難過]", "weight": 1.5},
    {"pattern": r"[睡|吃|頭].*不[好|了|行]", "weight": 1.0},
    {"pattern": r"[心情|狀態|精神].*[不|有點|還]", "weight": 1.0},
    {"pattern": r"[沒有|缺乏].*[動力|興趣|精神]", "weight": 1.0}
]

def test_pattern_matching():
    test_cases = [
        "我今天很累",
        "最近不太好",
        "感覺怪怪的",
        "不太想動",
        "有點煩",
        "睡不好",
        "心情不好",
        "沒有動力"
    ]

    print("Pattern Matching Debug:")
    print("="*40)

    for text in test_cases:
        total_weight = 0.0
        matched_patterns = []

        for i, pattern_info in enumerate(STATE_PATTERNS):
            pattern = pattern_info["pattern"]
            weight = pattern_info["weight"]

            if re.search(pattern, text):
                total_weight += weight
                matched_patterns.append(f"P{i+1}")

        print(f"'{text}': weight={total_weight:.1f}, patterns={matched_patterns}")

if __name__ == "__main__":
    test_pattern_matching()