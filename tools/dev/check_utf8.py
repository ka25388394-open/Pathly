#!/usr/bin/env python3
"""UTF-8 編碼檢查（Windows 兼容版）"""

from pathlib import Path

def check_utf8_files():
    """檢查重要文件是否能以 UTF-8 正常讀取"""
    print("=== Pathly UTF-8 編碼檢查 ===")
    print()

    files_to_check = [
        ('.env', '配置文件'),
        ('pathly_simple_ui.html', '前端頁面'),
        ('app/main.py', 'FastAPI 主程序'),
        ('start_pathly.py', '啟動腳本')
    ]

    all_good = True

    for file_path, description in files_to_check:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"[OK] {description}: UTF-8 讀取成功")

            # 檢查是否有中文內容
            chinese_chars = sum(1 for char in content if '\u4e00' <= char <= '\u9fff')
            if chinese_chars > 0:
                print(f"     發現 {chinese_chars} 個中文字符")

        except UnicodeDecodeError as e:
            print(f"[FAIL] {description}: UTF-8 讀取失敗")
            print(f"       錯誤: {e}")
            all_good = False
        except FileNotFoundError:
            print(f"[SKIP] {description}: 文件不存在")

    print()
    print("=== 結果 ===")
    if all_good:
        print("[SUCCESS] 所有文件都支持 UTF-8 編碼")
    else:
        print("[ERROR] 發現編碼問題，需要修正")

    return all_good

if __name__ == "__main__":
    check_utf8_files()