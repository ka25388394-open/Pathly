"""TST Router - Phase 2D 最小實作"""

from typing import Optional


def determine_tst_marker(reset_signal: bool, message: str) -> Optional[str]:
    """
    Phase 2D TST marker 判斷。
    支援 Risk / Reset / Rest / Stay marker 判斷。
    優先順序：Risk > Reset > Rest > Stay

    Args:
        reset_signal: Phase 1 reset 訊號偵測結果
        message: 使用者當前輸入訊息

    Returns:
        Optional[str]: TST marker ("Risk" | "Reset" | "Rest" | "Stay" | None)
    """
    # Phase 2C: Risk marker 檢測 - 最高優先級
    if _detect_risk_signal(message):
        return "Risk"

    # Reset 優先判斷
    if reset_signal:
        return "Reset"

    # Rest marker 判斷 - 明確想停止處理的片語
    rest_phrases = [
        "先不要想了",
        "先不想了",
        "不想了",
        "先不想",
        "真的沒力了",
        "想休息",
        "今天夠了",
        "想停下來",
        "先這樣就好",
        "不想再繼續了",
        "腦袋關機了",
        "現在只想放空",
        "沒力氣整理",
        "不想處理了"
    ]

    # 檢查是否包含 Rest 片語
    if any(phrase in message for phrase in rest_phrases):
        return "Rest"

    # Phase 2D: Stay marker 檢測 - 表達困難且非技術語境
    if _detect_stay_signal(message):
        return "Stay"

    return None


def _detect_risk_signal(message: str) -> bool:
    """
    檢測明確安全風險訊號

    Args:
        message: 使用者輸入訊息

    Returns:
        bool: 是否包含明確風險片語
    """
    # 明確安全風險片語
    risk_phrases = [
        "我不想活了",
        "我想死",
        "我想自殺",
        "我想傷害自己",
        "我想消失",
        "我活不下去了",
        "我撐不下去了",
        "我真的撐不下去了",
        "我實在撐不下去了",
        "我快撐不下去了",
        "我完全撐不下去了",
        "我想結束生命",
        "我想結束這一切",
        "活著沒有意義",
        "i want to die",
        "i want to kill myself",
        "i want to hurt myself",
        "suicide",
        "kill myself"
    ]

    message_lower = message.lower().strip()

    # 檢測風險關鍵字
    return any(phrase in message_lower for phrase in risk_phrases)


def _detect_stay_signal(message: str) -> bool:
    """
    檢測 Stay 訊號 - 心理層面表達困難且非技術語境

    Args:
        message: 使用者輸入訊息

    Returns:
        bool: 是否為 Stay 狀態（表達困難且非技術語境）
    """
    # 技術語境排除詞
    tech_patterns = [
        "bug", "程式", "API", "後端", "前端", "代碼",
        "terminal", "PowerShell", "server", "localhost"
    ]

    # 如果包含技術語境詞，不判為 Stay
    if any(pattern in message for pattern in tech_patterns):
        return False

    # Stay 強觸發片語
    stay_patterns = [
        "說不上來",
        "不知道怎麼講",
        "不知道怎麼說",
        "說不清楚",
        "卡住了",
        "不知道自己怎麼了",
        "搞不清楚自己怎麼了",
        "說不出來",
        "不知道從哪裡說",
        "不知道從哪裡開始說",
        "不知道怎麼開始說",
        "不想整理",
        "我不想整理",
        "現在不想整理",
        "不想急著整理",
        "想先停在這裡",
        "我想先停在這裡",
        "先停在這裡就好"
    ]

    # 檢查是否包含 Stay 片語
    return any(pattern in message for pattern in stay_patterns)