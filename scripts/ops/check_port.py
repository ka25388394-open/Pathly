#!/usr/bin/env python3
"""檢查 port 5000 是否被佔用"""

import socket
import sys
from pathlib import Path

# 添加專案路徑
sys.path.insert(0, str(Path(__file__).parent))

def check_port(port: int) -> bool:
    """檢查 port 是否可用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except OSError:
            return False

def main():
    from app.config import get_settings

    settings = get_settings()
    port = settings.port

    print(f"🔍 Checking port {port} for {settings.project_name}...")

    if check_port(port):
        print(f"✅ Port {port} is available")
        return 0
    else:
        print(f"❌ Port {port} is already in use!")
        print(f"   Please stop other services or change PORT in .env")
        return 1

if __name__ == "__main__":
    sys.exit(main())