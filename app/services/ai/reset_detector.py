"""Reset Signal 檢測器 - Phase 1 最小實作"""

from typing import Tuple


def detect_reset_signal(message: str) -> Tuple[bool, str]:
    """
    檢測使用者訊息是否包含換話題的訊號

    Args:
        message: 使用者輸入的訊息

    Returns:
        Tuple[bool, str]: (是否有reset訊號, 觸發原因關鍵詞)
    """
    message = message.strip().lower()

    # Phase 1 最小關鍵詞檢測
    reset_keywords = [
        "換個話題", "換話題", "聊別的",
        "不說了", "算了",
        "另一個問題", "問別的", "別的事",
        "重新開始", "換個方向"
    ]

    for keyword in reset_keywords:
        if keyword in message:
            return True, keyword

    return False, ""