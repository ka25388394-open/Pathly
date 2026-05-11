#!/usr/bin/env python3
"""Level 2 邊界測試"""

import requests

def run_boundary_test():
    """執行邊界測試"""

    # 邊界測試案例：可能被誤判的 Level 2 句子
    test_cases = [
        ("有點累", "應該Level 2", "輕度疲憊情緒"),
        ("最近怪怪的", "應該Level 2", "模糊負面情感"),
        ("不太想動", "應該Level 2", "輕度抑鬱情緒"),
        ("有點煩", "應該Level 2", "輕度煩躁情緒"),
        ("感覺不對勁", "應該Level 2", "模糊不適感"),
        ("心情不好", "應該Level 2", "直接情緒表達"),
        ("有點焦慮", "應該Level 2", "輕度焦慮情緒"),
        ("睡不好", "應該Level 2", "生理狀態問題"),
        ("覺得怪怪的", "應該Level 2", "模糊負面感受"),
        ("有點不安", "應該Level 2", "輕度不安情緒")
    ]

    print("Level 2 邊界測試")
    print("=" * 80)
    print(f"{'測試句':<15} {'預期':<12} {'實際':<8} {'狀態':<8} {'特徵':<20}")
    print("-" * 80)

    api_url = "http://localhost:8007/api/v1/ai/support"
    results = []

    for sentence, expected_desc, feature in test_cases:
        try:
            payload = {"message": sentence}
            response = requests.post(api_url, json=payload, timeout=5)

            if response.status_code == 200:
                data = response.json()
                actual_level = data["data"]["level"]
                keywords = data["data"]["analysis"]["keywords"]

                # 判斷是否正確
                expected_level = 2  # 所有測試案例都應該是 Level 2
                is_correct = actual_level == expected_level

                status = "PASS" if is_correct else "FAIL"

                print(f"{sentence:<15} {'Level 2':<12} {'Level ' + str(actual_level):<8} {status:<8} {feature:<20}")

                results.append({
                    "sentence": sentence,
                    "expected": expected_level,
                    "actual": actual_level,
                    "correct": is_correct,
                    "keywords": keywords,
                    "feature": feature,
                    "char_count": len(sentence)
                })

            else:
                print(f"{sentence:<15} {'Level 2':<12} {'ERROR':<8} {'API':<8} {feature:<20}")

        except Exception as e:
            print(f"{sentence:<15} {'Level 2':<12} {'ERROR':<8} {'CONN':<8} {feature:<20}")

    # 分析結果
    analyze_boundary_results(results)

def analyze_boundary_results(results):
    """分析邊界測試結果"""
    print("\n" + "=" * 80)
    print("邊界測試分析")
    print("=" * 80)

    # 統計
    total = len(results)
    correct = sum(1 for r in results if r["correct"])
    failed = total - correct

    print(f"總測試案例: {total}")
    print(f"正確判斷: {correct}")
    print(f"誤判案例: {failed}")
    print(f"準確率: {correct/total*100:.1f}%")

    # 分析誤判案例
    failed_cases = [r for r in results if not r["correct"]]

    if failed_cases:
        print(f"\n誤判案例分析:")
        print("-" * 40)

        for case in failed_cases:
            print(f"'{case['sentence']}' -> Level {case['actual']} (應該Level {case['expected']})")
            print(f"  字數: {case['char_count']}")
            print(f"  關鍵字: {case['keywords']}")
            print(f"  特徵: {case['feature']}")

        # 找出共通特徵
        analyze_common_patterns(failed_cases)

        # 提供修正建議
        provide_fix_suggestions(failed_cases)

def analyze_common_patterns(failed_cases):
    """分析共通失敗模式"""
    print(f"\n共通失敗特徵:")
    print("-" * 30)

    # 字數分析
    char_counts = [case["char_count"] for case in failed_cases]
    avg_chars = sum(char_counts) / len(char_counts)
    print(f"1. 字數特徵:")
    print(f"   - 平均字數: {avg_chars:.1f}")
    print(f"   - 字數範圍: {min(char_counts)}-{max(char_counts)}")

    # 關鍵字分析
    all_keywords = []
    for case in failed_cases:
        all_keywords.extend(case["keywords"])

    print(f"2. 關鍵字特徵:")
    if all_keywords:
        keyword_freq = {}
        for kw in all_keywords:
            keyword_freq[kw] = keyword_freq.get(kw, 0) + 1
        print(f"   - 常見關鍵字: {list(keyword_freq.keys())}")
    else:
        print(f"   - 缺少Level 2關鍵字")

    # 語言模式分析
    sentences = [case["sentence"] for case in failed_cases]
    print(f"3. 語言模式:")

    # 檢查修飾詞
    modifiers = ["有點", "一點", "不太", "感覺", "覺得"]
    has_modifiers = [s for s in sentences if any(mod in s for mod in modifiers)]
    print(f"   - 含弱化修飾詞: {len(has_modifiers)}/{len(sentences)}")

    # 檢查情緒詞
    emotion_words = ["累", "煩", "焦慮", "不安", "不好"]
    has_emotions = [s for s in sentences if any(emo in s for emo in emotion_words)]
    print(f"   - 含情緒詞: {len(has_emotions)}/{len(sentences)}")

def provide_fix_suggestions(failed_cases):
    """提供修正建議"""
    print(f"\n最小修正建議:")
    print("-" * 30)

    # 分析失敗原因並提供對應建議
    print("1. 增加輕度情緒關鍵字權重:")
    light_emotions = ["有點累", "不太想", "怪怪的", "不對勁", "不好", "焦慮", "不安"]
    print(f"   建議在 LEVEL_KEYWORDS['level_2']['mild_stress'] 中添加:")
    print(f"   {light_emotions}")

    print(f"\n2. 調整短文本情緒判斷:")
    print(f"   當短文本(<=10字)包含任何 Level 2 關鍵字時，應直接歸類 Level 2")
    print(f"   修正位置: level_detector.py 中的短文本判斷邏輯")

    print(f"\n3. 降低模糊情緒門檻:")
    print(f"   含有修飾詞+情緒詞組合(如'有點累')的句子應額外加分")
    print(f"   建議: 檢測到修飾詞+情緒詞時，Level 2 分數 +0.5")

    print(f"\n4. 具體修改項目:")
    print(f"   - 在 ai_config.py 中增加輕度情緒關鍵字")
    print(f"   - 在 level_detector.py 中調整短文本+情緒的判斷邏輯")
    print(f"   - 增加修飾詞+情緒詞的組合檢測")

if __name__ == "__main__":
    run_boundary_test()