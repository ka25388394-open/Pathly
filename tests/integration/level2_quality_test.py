#!/usr/bin/env python3
"""Level 2 回應品質測試"""

import requests
import re

def test_level2_quality():
    """測試 Level 2 回應品質"""

    test_cases = [
        "我今天很累",
        "我最近工作很累，也不知道怎麼調整",
        "我跟朋友有點卡住，不知道要不要說",
        "我想創作，但覺得自己不夠好",
        "我想變好，可是又怕自己做不到"
    ]

    print("Level 2 回應品質測試")
    print("=" * 80)

    results = []
    api_url = "http://localhost:8007/api/v1/ai/support"

    for i, message in enumerate(test_cases, 1):
        print(f"\n測試 {i}: {message}")
        print("-" * 60)

        try:
            payload = {"message": message}
            response = requests.post(api_url, json=payload, timeout=5)

            if response.status_code == 200:
                data = response.json()
                level = data["data"]["level"]

                if level != 2:
                    print(f"警告: 預期 Level 2, 實際 Level {level}")
                    continue

                # 提取回應內容
                response_data = data["data"]["response"]
                domain = response_data.get("domain", "未知")
                state = response_data.get("state", "未知")
                drive = response_data.get("drive", "未知")
                message_text = response_data.get("message", "")

                print(f"Domain: {domain}")
                print(f"State: {state}")
                print(f"Drive: {drive}")
                print(f"Message: {message_text}")

                # 評估回應品質
                evaluation = evaluate_level2_response(
                    message, domain, state, drive, message_text
                )

                results.append({
                    "input": message,
                    "domain": domain,
                    "state": state,
                    "drive": drive,
                    "message": message_text,
                    "evaluation": evaluation
                })

                print(f"\n評估結果:")
                for aspect, result in evaluation.items():
                    status = "✓" if result["pass"] else "✗"
                    print(f"{status} {aspect}: {result['comment']}")

            else:
                print(f"API 錯誤: {response.status_code}")

        except Exception as e:
            print(f"請求錯誤: {e}")

    # 生成測試報告
    generate_quality_report(results)

def evaluate_level2_response(input_text, domain, state, drive, message):
    """評估 Level 2 回應品質"""
    evaluation = {}

    # 1. Domain 合理性
    domain_eval = evaluate_domain(input_text, domain)
    evaluation["domain_合理性"] = domain_eval

    # 2. State 合理性
    state_eval = evaluate_state(input_text, state)
    evaluation["state_合理性"] = state_eval

    # 3. Drive 合理性
    drive_eval = evaluate_drive(input_text, drive)
    evaluation["drive_合理性"] = drive_eval

    # 4. 兩句話規則
    structure_eval = evaluate_message_structure(message)
    evaluation["兩句話結構"] = structure_eval

    # 5. 理解感受性
    empathy_eval = evaluate_empathy(input_text, message)
    evaluation["理解感受性"] = empathy_eval

    return evaluation

def evaluate_domain(input_text, domain):
    """評估 domain 分類合理性"""
    # 根據輸入文本判斷應該的 domain
    if "工作" in input_text:
        expected = "工作"
    elif "朋友" in input_text:
        expected = "關係"
    elif "創作" in input_text:
        expected = "創作"
    elif "變好" in input_text or "做不到" in input_text:
        expected = "挑戰"
    else:
        expected = "生活"  # 默認

    if domain == expected:
        return {"pass": True, "comment": f"正確識別為{domain}"}
    else:
        return {"pass": False, "comment": f"應為{expected}，實際{domain}"}

def evaluate_state(input_text, state):
    """評估 state 分類合理性"""
    # 根據輸入判斷合理的 state
    if "累" in input_text:
        reasonable_states = ["疲憊中", "痛苦中"]
    elif "卡住" in input_text or "不知道" in input_text:
        reasonable_states = ["拉扯中", "困惑中"]
    elif "怕" in input_text and "想" in input_text:
        reasonable_states = ["拉扯中", "混合中"]
    else:
        reasonable_states = ["拉扯中", "修復中", "成長中"]

    # 檢查是否在合理範圍內
    if any(rs in state for rs in reasonable_states) or state in reasonable_states:
        return {"pass": True, "comment": f"合理的狀態: {state}"}
    else:
        return {"pass": False, "comment": f"狀態{state}可能不合適"}

def evaluate_drive(input_text, drive):
    """評估 drive 分類合理性"""
    # 根據輸入判斷合理的 drive
    if "怕" in input_text or "不敢" in input_text:
        expected = "防衛型"
    elif "想" in input_text and "變好" in input_text:
        expected = "追尋型"
    elif "想" in input_text and "不知道" in input_text:
        expected = "混合型"
    else:
        expected = "混合型"  # 大多數情況

    if drive == expected:
        return {"pass": True, "comment": f"正確識別為{drive}"}
    else:
        return {"pass": False, "comment": f"可能更適合{expected}，實際{drive}"}

def evaluate_message_structure(message):
    """評估 message 是否符合兩句話結構"""
    sentences = re.split(r'[。！？]', message)
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) >= 2:
        # 檢查第一句是否為映照
        first_sentence = sentences[0]
        is_reflection = any(word in first_sentence for word in
                          ["感受", "理解", "聽起來", "看到", "感覺", "確實"])

        # 檢查第二句是否為選擇問句
        second_sentence = sentences[1] if len(sentences) > 1 else ""
        is_choice_question = any(word in second_sentence for word in
                               ["比較想", "還是", "先", "或是"])

        if is_reflection and is_choice_question:
            return {"pass": True, "comment": "符合映照+選擇問句結構"}
        elif is_reflection:
            return {"pass": True, "comment": "有映照，但問句可加強"}
        else:
            return {"pass": False, "comment": "缺少映照或選擇問句結構"}
    else:
        return {"pass": False, "comment": "不符合兩句話結構"}

def evaluate_empathy(input_text, message):
    """評估是否讓人感覺被理解"""
    # 檢查是否避免敷衍用詞
    dismissive_phrases = ["不錯呢", "很好", "挺好的", "沒問題"]
    has_dismissive = any(phrase in message for phrase in dismissive_phrases)

    # 檢查是否有理解性用詞
    empathetic_phrases = ["理解", "感受", "確實", "聽起來", "感覺", "陪伴", "一起"]
    has_empathy = any(phrase in message for phrase in empathetic_phrases)

    # 檢查是否回應了核心情感
    core_emotions = ["累", "困惑", "擔心", "害怕", "想要"]
    input_emotions = [emotion for emotion in core_emotions if emotion in input_text]
    addresses_emotion = any(emotion in message for emotion in input_emotions)

    if has_dismissive:
        return {"pass": False, "comment": "含有敷衍用詞，缺乏理解感"}
    elif has_empathy and addresses_emotion:
        return {"pass": True, "comment": "有理解感，回應了核心情感"}
    elif has_empathy:
        return {"pass": True, "comment": "有理解感，但可更貼近情感"}
    else:
        return {"pass": False, "comment": "缺乏理解感，偏向冷漠"}

def generate_quality_report(results):
    """生成品質測試報告"""
    print("\n\n" + "=" * 80)
    print("Level 2 回應品質測試報告")
    print("=" * 80)

    for i, result in enumerate(results, 1):
        evaluation = result["evaluation"]

        print(f"\n[{i}] {result['input']}")
        print(f"Domain: {result['domain']}")
        print(f"State: {result['state']}")
        print(f"Drive: {result['drive']}")
        print(f"Message: {result['message'][:60]}...")

        # 計算通過率
        pass_count = sum(1 for eval_result in evaluation.values() if eval_result["pass"])
        total_count = len(evaluation)

        print(f"品質評分: {pass_count}/{total_count}")

        # 列出需要改進的地方
        fails = [aspect for aspect, eval_result in evaluation.items()
                if not eval_result["pass"]]
        if fails:
            print(f"需改進: {', '.join(fails)}")

    print(f"\n測試完成: {len(results)} 個案例")

if __name__ == "__main__":
    test_level2_quality()