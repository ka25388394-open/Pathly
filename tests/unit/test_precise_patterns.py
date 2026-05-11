#!/usr/bin/env python3
"""測試更精確的模式"""

import re

# 更精確的模式
PRECISE_PATTERNS = [
    # 1. 主觀負面狀態表達（加入負面詞約束）
    {"pattern": r"我.*(很|有點|比較|還蠻|超|太).*(累|煩|痛|難受|不舒服|壓力|焦慮)", "weight": 1.5},
    # 2. 時間+狀態描述
    {"pattern": r"(最近|這幾天|今天|現在).*(不|沒)", "weight": 1.0},
    # 3. 感覺/覺得+狀態
    {"pattern": r"(感覺|覺得).*(不|有點|怪)", "weight": 1.0},
    # 4. 輕度否定表達
    {"pattern": r"不(太|怎麼|是很|大).*(想|好|行)", "weight": 1.0},
    # 5. 程度+情緒詞
    {"pattern": r"(有點|一點|還蠻|比較).*(累|煩|焦慮|不安|難過)", "weight": 1.5},
    # 6. 生理狀態描述
    {"pattern": r"(睡|吃|頭).*不(好|了|行)", "weight": 1.0},
    # 7. 心理狀態模糊表達
    {"pattern": r"(心情|狀態|精神).*(不|有點|還)", "weight": 1.0},
    # 8. 能力/意願下降
    {"pattern": r"(沒有|缺乏).*(動力|興趣|精神)", "weight": 1.0}
]

def test_precise_patterns():
    """測試更精確的模式"""

    # 應該是 Level 1（不匹配）的案例
    level_1_cases = [
        "我很好",          # 無負面詞
        "我很開心",        # 無負面詞
        "我今天不錯",      # 雖有"不"但非時間模式
        "今天很棒",        # 無負面詞
        "最近天氣很好"     # "最近"但非負面結尾
    ]

    # 應該是 Level 2（匹配）的案例
    level_2_cases = [
        "我很累",          # 主觀負面
        "我今天很煩",      # 主觀負面
        "最近不太好",      # 時間+否定
        "感覺怪怪的",      # 感覺+模糊
        "不太想動",        # 輕度否定
        "有點煩",          # 程度+情緒
        "睡不好",          # 生理+否定
        "心情不好",        # 心理+否定
        "沒有動力"         # 能力下降
    ]

    print("Precise Pattern Test:")
    print("="*50)

    # 測試 Level 1 案例
    print("Level 1 Cases (should NOT match):")
    level_1_correct = 0
    for case in level_1_cases:
        matches = []
        total_weight = 0
        for i, pattern_info in enumerate(PRECISE_PATTERNS):
            if re.search(pattern_info["pattern"], case):
                matches.append(f"P{i+1}")
                total_weight += pattern_info["weight"]

        result = "PASS" if total_weight == 0 else "FAIL"
        if total_weight == 0:
            level_1_correct += 1

        print(f"  {result}: '{case}' -> weight={total_weight:.1f}, patterns={matches}")

    print(f"\nLevel 1 Accuracy: {level_1_correct}/{len(level_1_cases)} ({level_1_correct/len(level_1_cases)*100:.1f}%)\n")

    # 測試 Level 2 案例
    print("Level 2 Cases (should match):")
    level_2_correct = 0
    for case in level_2_cases:
        matches = []
        total_weight = 0
        for i, pattern_info in enumerate(PRECISE_PATTERNS):
            if re.search(pattern_info["pattern"], case):
                matches.append(f"P{i+1}")
                total_weight += pattern_info["weight"]

        result = "PASS" if total_weight > 0 else "FAIL"
        if total_weight > 0:
            level_2_correct += 1

        print(f"  {result}: '{case}' -> weight={total_weight:.1f}, patterns={matches}")

    print(f"\nLevel 2 Accuracy: {level_2_correct}/{len(level_2_cases)} ({level_2_correct/len(level_2_cases)*100:.1f}%)")

    # 總體結果
    overall_accuracy = ((level_1_correct + level_2_correct) / (len(level_1_cases) + len(level_2_cases))) * 100
    print(f"\nOverall Pattern Accuracy: {overall_accuracy:.1f}%")

if __name__ == "__main__":
    test_precise_patterns()