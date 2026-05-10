#!/usr/bin/env python3
"""Pathly 本地開發啟動器"""

import os
import sys
import subprocess
import requests
from pathlib import Path
from dotenv import load_dotenv

def load_config():
    """載入配置"""
    env_file = Path('.env')
    if not env_file.exists():
        print("[ERROR] 找不到 .env 檔案")
        sys.exit(1)

    load_dotenv(env_file)

    config = {
        'PROJECT_NAME': os.getenv('PROJECT_NAME', 'pathly'),
        'ENV': os.getenv('ENV', 'development'),
        'BACKEND_PORT': int(os.getenv('BACKEND_PORT', 8007)),
        'FRONTEND_PORT': int(os.getenv('FRONTEND_PORT', 5500)),
    }

    return config

def check_directory():
    """檢查工作目錄"""
    if not Path('app/main.py').exists():
        print("[ERROR] 不在 Pathly 專案根目錄")
        print(f"當前目錄: {Path.cwd()}")
        sys.exit(1)

def check_port_available(port):
    """檢查端口是否可用，顯示詳細 PID 信息"""
    # 檢查端口占用情況
    try:
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        lines = result.stdout.split('\n')

        listening_pids = []
        for line in lines:
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    listening_pids.append(pid)

        if listening_pids:
            print(f"[WARNING] 端口 {port} 已被占用")
            print("發現以下 PID 在使用端口 8007:")
            for pid in listening_pids:
                print(f"  - PID {pid}")
            print("\n請先關閉這些進程:")
            print("方法 1: 手動關閉 uvicorn 視窗 (Ctrl+C)")
            print("方法 2: 手動執行 taskkill /PID <PID號碼> /F")
            print(f"方法 3: 執行 python cleanup_services.py")
            return False
        else:
            print(f"[OK] 端口 {port} 可用")
            return True

    except Exception as e:
        print(f"[WARNING] 無法檢查端口狀態: {e}")
        # 回到簡單檢查
        try:
            response = requests.get(f"http://127.0.0.1:{port}/health", timeout=1)
            print(f"[WARNING] 端口 {port} 已被使用")
            return False
        except requests.exceptions.ConnectionError:
            print(f"[OK] 端口 {port} 可用")
            return True

def start_server(config):
    """啟動服務器"""
    print("\n[INFO] 啟動 Pathly 後端服務...")
    print(f"[CMD] python -m uvicorn app.main:app --host 127.0.0.1 --port {config['BACKEND_PORT']} --reload")
    print()
    print("按 Ctrl+C 停止服務")
    print(f"前端請使用: http://127.0.0.1:{config['FRONTEND_PORT']}/pathly_simple_ui.html")
    print(f"API 基礎路徑: http://127.0.0.1:{config['BACKEND_PORT']}/api/v1")
    print(f"API 文檔: http://127.0.0.1:{config['BACKEND_PORT']}/docs")
    print()

    try:
        subprocess.run([
            sys.executable, '-m', 'uvicorn',
            'app.main:app',
            '--host', '127.0.0.1',
            '--port', str(config['BACKEND_PORT']),
            '--reload'
        ])
    except KeyboardInterrupt:
        print("\n[INFO] 服務已停止")

def main():
    print("=" * 40)
    print("      Pathly 本地開發啟動器")
    print("=" * 40)

    # 檢查目錄
    check_directory()

    # 載入配置
    print("\n[INFO] 載入配置...")
    config = load_config()

    # 顯示配置
    print(f"PROJECT_NAME: {config['PROJECT_NAME']}")
    print(f"ENV: {config['ENV']}")
    print(f"BACKEND_PORT: {config['BACKEND_PORT']}")
    print(f"FRONTEND_PORT: {config['FRONTEND_PORT']}")

    # 檢查端口
    print(f"\n[INFO] 檢查端口 {config['BACKEND_PORT']}...")
    if not check_port_available(config['BACKEND_PORT']):
        sys.exit(1)

    # 啟動服務
    start_server(config)

if __name__ == "__main__":
    main()