#!/usr/bin/env python3
"""簡化編碼檢查"""

from pathlib import Path

def check_utf8_files():
    """檢查重要文件是否能以 UTF-8 正常讀取"""
    print("=== Pathly UTF-8 編碼檢查 ===\n")

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
            print(f"✅ {description}: UTF-8 讀取成功")

            # 檢查是否有中文內容
            chinese_chars = sum(1 for char in content if '\u4e00' <= char <= '\u9fff')
            if chinese_chars > 0:
                print(f"   發現 {chinese_chars} 個中文字符")

        except UnicodeDecodeError as e:
            print(f"❌ {description}: UTF-8 讀取失敗")
            print(f"   錯誤: {e}")
            all_good = False
        except FileNotFoundError:
            print(f"⚪ {description}: 文件不存在")

    print(f"\n=== 結果 ===")
    if all_good:
        print("✅ 所有文件都支持 UTF-8 編碼")
    else:
        print("❌ 發現編碼問題，需要修正")

    # 測試中文輸出
    print(f"\n=== 中文輸出測試 ===")
    test_text = "中文測試: 陪你慢慢整理內心的角落 🌟"
    print(test_text)

    # 測試從 .env 讀取
    try:
        from app.config import get_settings
        settings = get_settings()
        print(f"\n=== .env 讀取測試 ===")
        print(f"PROJECT_NAME: {settings.project_name}")
        print(f"ENV: {settings.env}")
        print("✅ .env 讀取正常")
    except Exception as e:
        print(f"❌ .env 讀取失敗: {e}")

if __name__ == "__main__":
    check_utf8_files()