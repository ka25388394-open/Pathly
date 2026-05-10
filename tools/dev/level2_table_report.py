#!/usr/bin/env python3
"""Level 2 回應品質表格報告"""

import requests

def generate_table_report():
    """生成表格格式的測試報告"""

    test_cases = [
        "我今天很累",
        "我最近工作很累，也不知道怎麼調整",
        "我跟朋友有點卡住，不知道要不要說",
        "我想創作，但覺得自己不夠好",
        "我想變好，可是又怕自己做不到"
    ]

    print("Level 2 回應品質測試表格")
    print("=" * 120)
    print(f"{'輸入':<20} {'Domain':<8} {'State':<8} {'Drive':<8} {'Message':<30} {'通過':<6} {'建議':<20}")
    print("-" * 120)

    api_url = "http://localhost:8008/api/v1/ai/support"

    for message in test_cases:
        try:
            payload = {"message": message}
            response = requests.post(api_url, json=payload, timeout=5)

            if response.status_code == 200:
                data = response.json()
                level = data["data"]["level"]

                if level != 2:
                    print(f"{message:<20} {'N/A':<8} {'N/A':<8} {'N/A':<8} {'判定為Level' + str(level):<30} {'FAIL':<6} {'需調整Level判斷':<20}")
                    continue

                response_data = data["data"]["response"]
                domain = response_data.get("domain", "未知")
                state = response_data.get("state", "未知")
                drive = response_data.get("drive", "未知")
                message_text = response_data.get("message", "")

                # 簡化評估
                issues = []

                # Domain 評估
                if "工作" in message and domain != "工作":
                    issues.append("Domain錯誤")
                elif "朋友" in message and domain != "關係":
                    issues.append("Domain錯誤")
                elif "創作" in message and domain != "創作":
                    issues.append("Domain錯誤")

                # Message 品質評估
                if "不錯呢" in message_text or "很好" in message_text:
                    issues.append("過於敷衍")

                # 兩句話結構
                sentences = message_text.split('。')
                if len([s for s in sentences if s.strip()]) < 2:
                    issues.append("結構不完整")

                # 選擇問句
                if "比較想" not in message_text and "還是" not in message_text:
                    issues.append("缺選擇問句")

                # 判斷通過狀態
                if len(issues) == 0:
                    status = "PASS"
                    suggestion = "良好"
                elif len(issues) <= 2:
                    status = "MINOR"
                    suggestion = "; ".join(issues[:2])
                else:
                    status = "FAIL"
                    suggestion = "; ".join(issues[:2]) + "..."

                # 縮短顯示
                short_message = message_text[:25] + "..." if len(message_text) > 25 else message_text

                print(f"{message:<20} {domain:<8} {state:<8} {drive:<8} {short_message:<30} {status:<6} {suggestion:<20}")

            else:
                print(f"{message:<20} {'ERROR':<8} {'ERROR':<8} {'ERROR':<8} {'API錯誤':<30} {'ERROR':<6} {'檢查API':<20}")

        except Exception as e:
            print(f"{message:<20} {'ERROR':<8} {'ERROR':<8} {'ERROR':<8} {'連接失敗':<30} {'ERROR':<6} {'檢查連接':<20}")

    print("-" * 120)
    print("\n狀態說明:")
    print("PASS: 品質良好")
    print("MINOR: 有小問題")
    print("FAIL: 需要修正")
    print("ERROR: 測試失敗")

if __name__ == "__main__":
    generate_table_report()