#!/usr/bin/env python3
"""狀態描述語言模式定義"""

import re

# Level 2 狀態描述模式
STATE_PATTERNS = [
    # 1. 主觀狀態表達
    {
        "pattern": r"我.*[很|有點|比較|還蠻|超|太]",
        "description": "我+程度修飾詞",
        "examples": ["我很累", "我有點煩", "我比較焦慮"],
        "weight": 1.5
    },

    # 2. 時間+狀態描述
    {
        "pattern": r"[最近|這幾天|今天|現在].*[不|沒]",
        "description": "時間詞+否定狀態",
        "examples": ["最近不太好", "這幾天沒精神", "今天不想動"],
        "weight": 1.0
    },

    # 3. 感覺/覺得+狀態
    {
        "pattern": r"[感覺|覺得].*[不|有點|怪]",
        "description": "感知詞+模糊狀態",
        "examples": ["感覺不對勁", "覺得怪怪的", "感覺有點累"],
        "weight": 1.0
    },

    # 4. 輕度否定表達
    {
        "pattern": r"不[太|怎麼|是很|大].*[想|好|行]",
        "description": "弱否定+動作/狀態",
        "examples": ["不太想動", "不怎麼好", "不是很開心"],
        "weight": 1.0
    },

    # 5. 程度+情緒詞
    {
        "pattern": r"[有點|一點|還蠻|比較].*[累|煩|焦慮|不安|難過]",
        "description": "程度詞+情緒詞",
        "examples": ["有點累", "一點煩", "比較焦慮"],
        "weight": 1.5
    },

    # 6. 生理狀態描述
    {
        "pattern": r"[睡|吃|頭].*不[好|了|行]",
        "description": "生理+否定",
        "examples": ["睡不好", "吃不下", "頭不舒服"],
        "weight": 1.0
    },

    # 7. 心理狀態模糊表達
    {
        "pattern": r"[心情|狀態|精神].*[不|有點|還]",
        "description": "心理詞+狀態修飾",
        "examples": ["心情不好", "狀態有點差", "精神還好"],
        "weight": 1.0
    },

    # 8. 能力/意願下降
    {
        "pattern": r"[沒有|缺乏].*[動力|興趣|精神]",
        "description": "缺乏+積極詞",
        "examples": ["沒有動力", "缺乏興趣", "沒精神"],
        "weight": 1.0
    }
]

def test_state_patterns():
    """測試狀態模式匹配"""

    # 測試案例
    test_cases = [
        # 應該匹配的（Level 2）
        ("我很累", True),
        ("最近不太好", True),
        ("感覺不對勁", True),
        ("不太想動", True),
        ("有點煩", True),
        ("睡不好", True),
        ("心情不好", True),
        ("沒有動力", True),

        # 不應該匹配的（Level 1）
        ("今天天氣很好", False),
        ("你好嗎", False),
        ("想聊聊天", False),
        ("不錯呢", False),
        ("謝謝你", False)
    ]

    print("狀態模式測試")
    print("=" * 40)

    for text, should_match in test_cases:
        matched_patterns = []
        total_weight = 0

        for pattern_info in STATE_PATTERNS:
            pattern = pattern_info["pattern"]
            weight = pattern_info["weight"]

            if re.search(pattern, text):
                matched_patterns.append(pattern_info["description"])
                total_weight += weight

        is_state = total_weight >= 1.0
        result = "✓" if (is_state == should_match) else "✗"

        print(f"{result} '{text}' -> 匹配: {is_state} (權重: {total_weight})")
        if matched_patterns:
            print(f"    模式: {', '.join(matched_patterns)}")

if __name__ == "__main__":
    test_state_patterns()