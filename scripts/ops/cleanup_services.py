#!/usr/bin/env python3
"""清理多重服務實例"""

import subprocess
import time
import requests

def kill_python_processes_on_ports():
    """終止占用特定端口的 Python 進程"""
    ports = [5000, 8006, 8007]

    for port in ports:
        try:
            # 使用 netstat 找到占用端口的進程 PID
            result = subprocess.run(
                f'netstat -ano | findstr :{port}',
                shell=True, capture_output=True, text=True
            )

            if result.stdout:
                lines = result.stdout.strip().split('\n')
                pids = set()

                for line in lines:
                    parts = line.split()
                    if len(parts) >= 5 and 'LISTENING' in line:
                        pid = parts[-1]
                        pids.add(pid)

                for pid in pids:
                    print(f"終止端口 {port} 的進程 PID {pid}")
                    subprocess.run(f'taskkill /F /PID {pid}', shell=True)
            else:
                print(f"端口 {port}: 無進程")

        except Exception as e:
            print(f"清理端口 {port} 時出錯: {e}")

def verify_cleanup():
    """驗證清理結果"""
    print("\n=== 清理驗證 ===")
    ports = [5000, 8006, 8007]

    for port in ports:
        try:
            resp = requests.get(f"http://localhost:{port}/health", timeout=1)
            print(f"端口 {port}: 仍在運行!")
        except:
            print(f"端口 {port}: 已清理 ✓")

def main():
    print("=== 開始清理多重 Pathly 實例 ===")
    kill_python_processes_on_ports()

    print("\n等待 3 秒...")
    time.sleep(3)

    verify_cleanup()

    print("\n=== 清理完成 ===")
    print("現在可以重新啟動單一實例:")
    print("python -m uvicorn app.main:app --host 0.0.0.0 --port 8006")

if __name__ == "__main__":
    main()