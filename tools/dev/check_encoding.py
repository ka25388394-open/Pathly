#!/usr/bin/env python3
"""檢查文件編碼狀況"""

import chardet
from pathlib import Path

def check_file_encoding(file_path):
    """檢查單個文件編碼"""
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)

        print(f"文件: {file_path.name}")
        print(f"  編碼: {result['encoding']}")
        print(f"  信心度: {result['confidence']:.2%}")

        # 嘗試讀取內容
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"  UTF-8 讀取: ✅ 成功")
        except UnicodeDecodeError as e:
            print(f"  UTF-8 讀取: ❌ 失敗 - {e}")

        print()

    except Exception as e:
        print(f"檢查文件 {file_path} 時出錯: {e}")

def main():
    print("=== Pathly 文件編碼檢查 ===\n")

    # 檢查重要文件
    files_to_check = [
        Path('.env'),
        Path('pathly_simple_ui.html'),
        Path('app/main.py'),
        Path('app/config.py'),
        Path('start_pathly.py')
    ]

    for file_path in files_to_check:
        if file_path.exists():
            check_file_encoding(file_path)
        else:
            print(f"文件不存在: {file_path}\n")

    # 測試中文輸出
    print("=== 中文輸出測試 ===")
    print("中文測試: 你好世界 🌍")
    print("符號測試: ✅ ❌ 🎯")

if __name__ == "__main__":
    main()