#!/usr/bin/env python3
"""確認各端口對應的具體服務模組"""

import requests
import json

def check_service_identity(port):
    """檢查服務的具體身份"""
    try:
        # 檢查健康端點
        health_resp = requests.get(f"http://localhost:{port}/health", timeout=2)
        print(f"端口 {port}: {health_resp.text.strip()}")

        # 嘗試檢查 API 版本或其他識別信息
        try:
            api_resp = requests.post(f"http://localhost:{port}/api/v1/ai/support",
                                   json={"message": "test"}, timeout=2)
            if api_resp.status_code == 200:
                data = api_resp.json()
                model_used = data.get("data", {}).get("metadata", {}).get("model_used", "unknown")
                print(f"  └─ API 工作中，模型: {model_used}")
            else:
                print(f"  └─ API 回應碼: {api_resp.status_code}")
        except:
            print(f"  └─ 無 API 端點")

    except requests.exceptions.ConnectionError:
        print(f"端口 {port}: 無回應")
    except Exception as e:
        print(f"端口 {port}: 錯誤 - {str(e)[:50]}")

def main():
    print("=== 服務身份確認 ===")
    ports_to_check = [5000, 8006, 8007, 3000]

    for port in ports_to_check:
        check_service_identity(port)

    print("\n=== 當前工作目錄 ===")
    import os
    print(f"目錄: {os.getcwd()}")

    # 檢查是否在 pathly 目錄
    if "pathly" in os.getcwd():
        print("✅ 在 Pathly 專案目錄中")
    else:
        print("⚠️  不在 Pathly 專案目錄中")

if __name__ == "__main__":
    main()