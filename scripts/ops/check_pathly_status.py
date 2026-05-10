#!/usr/bin/env python3
"""Pathly 狀態一致性檢查"""

import os
import re
import requests
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def check_env_config():
    """檢查 .env 配置"""
    env_file = Path('.env')
    if not env_file.exists():
        return {"error": ".env 檔案不存在"}

    load_dotenv(env_file)
    return {
        "PROJECT_NAME": os.getenv('PROJECT_NAME'),
        "PORT": int(os.getenv('PORT', 8006)),
        "ENV": os.getenv('ENV')
    }

def check_frontend_config():
    """檢查前端 API 配置"""
    html_file = Path('pathly_simple_ui.html')
    if not html_file.exists():
        return {"error": "前端檔案不存在"}

    content = html_file.read_text(encoding='utf-8')

    # 搜尋 localhost:端口
    match = re.search(r'localhost:(\d+)', content)
    if match:
        return {"frontend_port": int(match.group(1))}
    else:
        return {"error": "找不到前端 API 端口設定"}

def check_running_services():
    """檢查運行中的服務"""
    services = {}
    ports_to_check = [5000, 8006, 8007, 8080]

    for port in ports_to_check:
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=1)
            if response.status_code == 200:
                data = response.json()
                services[port] = {
                    "status": "運行中",
                    "service": data.get("service", "unknown"),
                    "response_time": response.elapsed.total_seconds()
                }
        except:
            services[port] = {"status": "停止"}

    return services

def check_port_conflicts():
    """檢查端口占用情況"""
    try:
        result = subprocess.run(
            'netstat -ano | findstr :8006',
            shell=True, capture_output=True, text=True
        )

        if result.stdout:
            lines = result.stdout.strip().split('\n')
            processes = []
            for line in lines:
                if 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        processes.append(parts[-1])  # PID
            return {"port_8006_processes": processes}
        else:
            return {"port_8006_processes": []}
    except:
        return {"error": "無法檢查端口占用"}

def main():
    print("=" * 60)
    print("Pathly 狀態一致性檢查")
    print("=" * 60)

    # 檢查工作目錄
    if not Path('app/main.py').exists():
        print("❌ 錯誤：不在 Pathly 專案目錄")
        return

    # 1. 檢查 .env 配置
    print("\n1. .env 配置:")
    env_config = check_env_config()
    if "error" in env_config:
        print(f"   [ERROR] {env_config['error']}")
    else:
        print(f"   PROJECT_NAME: {env_config['PROJECT_NAME']}")
        print(f"   PORT: {env_config['PORT']}")
        print(f"   ENV: {env_config['ENV']}")

    # 2. 檢查前端配置
    print("\n2. 前端配置:")
    frontend_config = check_frontend_config()
    if "error" in frontend_config:
        print(f"   [ERROR] {frontend_config['error']}")
    else:
        print(f"   前端 API 端口: {frontend_config['frontend_port']}")

    # 3. 一致性檢查
    print("\n3. 一致性檢查:")
    if "error" not in env_config and "error" not in frontend_config:
        if env_config['PORT'] == frontend_config['frontend_port']:
            print("   [OK] 端口配置一致")
        else:
            print(f"   [FAIL] 端口不一致！ .env={env_config['PORT']}, 前端={frontend_config['frontend_port']}")

    # 4. 檢查運行中的服務
    print("\n4. 運行中的服務:")
    services = check_running_services()
    running_count = 0
    for port, info in services.items():
        if info['status'] == '運行中':
            running_count += 1
            print(f"   端口 {port}: [RUNNING] {info['service']} ({info['response_time']:.3f}s)")
        else:
            print(f"   端口 {port}: [STOP] 停止")

    # 5. 多重實例警告
    print(f"\n5. 實例數量檢查:")
    if running_count == 0:
        print("   [STOP] 無服務運行")
    elif running_count == 1:
        print("   [OK] 單一實例運行 (正常)")
    else:
        print(f"   [FAIL] 多重實例運行！({running_count} 個)")
        print("   建議執行: python cleanup_services.py")

    # 6. 端口占用詳情
    print("\n6. 端口占用:")
    port_info = check_port_conflicts()
    if "error" in port_info:
        print(f"   [ERROR] {port_info['error']}")
    else:
        processes = port_info['port_8006_processes']
        if not processes:
            print("   [FREE] 端口 8006 未被占用")
        elif len(processes) == 1:
            print(f"   [OK] 端口 8006 被 1 個進程占用 (PID: {processes[0]})")
        else:
            print(f"   [FAIL] 端口 8006 被 {len(processes)} 個進程占用！")
            print(f"   PIDs: {', '.join(processes)}")

    # 7. 總結建議
    print("\n總結:")
    if "error" not in env_config and "error" not in frontend_config:
        if env_config['PORT'] == frontend_config['frontend_port'] and running_count == 1:
            print("   [OK] 系統狀態正常，配置一致")
        else:
            print("   [ACTION] 發現問題，建議:")
            print("   1. python cleanup_services.py  # 清理多重實例")
            print("   2. 檢查 .env 和前端配置一致性")
            print("   3. python start_pathly.py      # 標準啟動")

if __name__ == "__main__":
    main()