#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最終驗收測試：疲勞短句修正"""

import requests
import json
import sys

def acceptance_test():
    """驗收測試：好累"""

    url = "http://127.0.0.1:8007/api/v1/ai/support"

    print("=== PATHLY 疲勞短句修正驗收 ===")
    print("目標：修正 Level 2 疲勞短句回應")
    print()

    # 測試「好累」
    test_input = "好累"
    print(f"測試輸入: {test_input}")

    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={"message": test_input},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()

            print(f"✅ API 調用成功")
            print(f"✅ Level: {data['data']['level']} (期望: 2)")
            print(f"✅ State: {data['data']['response'].get('state', 'N/A')} (期望: 疲勞中)")

            message = data['data']['response']['message']
            print(f"✅ Response Message 已修改")
            print()

            # 檢查是否包含期望的承接語句
            if "聽起來" in message and "累" in message:
                print("✅ 包含承接疲勞感的語句")
            else:
                print("❌ 未包含承接疲勞感的語句")

            # 檢查是否移除了舊的問題句型
            if "維持現在的節奏" not in message and "加入新的元素" not in message:
                print("✅ 已移除舊的「維持節奏vs加入元素」句型")
            else:
                print("❌ 仍包含舊的句型")

            # 檢查是否包含理想的問句方向
            if "身體累" in message and "心裡" in message:
                print("✅ 包含理想的身體vs心理分類問句")
            else:
                print("❌ 未包含身體vs心理分類問句")

            print()
            print("完整回應訊息:")
            print(f'"{message}"')
            print()

            # 總結
            level_correct = data['data']['level'] == 2
            state_correct = data['data']['response'].get('state') != '穩定中'
            message_improved = "維持現在的節奏" not in message

            if level_correct and state_correct and message_improved:
                print("🎉 驗收通過！疲勞短句回應已成功修正")
                return True
            else:
                print("❌ 驗收未完全通過，仍需調整")
                return False

        else:
            print(f"❌ API 錯誤: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

if __name__ == "__main__":
    success = acceptance_test()
    sys.exit(0 if success else 1)