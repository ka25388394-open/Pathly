"""AI 分層系統 - 最小配置版本"""

# 簡單的關鍵字配置
LEVEL_KEYWORDS = {
    "level_1": ["嗨", "你好", "哈囉", "謝謝", "不錯", "開心"],
    "level_2": ["累", "疲憊", "壓力", "困難", "煩惱", "不知道", "困惑"],
    "level_3": ["痛苦", "絕望", "崩潰", "受不了", "沒意義", "很痛苦"]
}

# 求助關鍵字
HELP_KEYWORDS = ["幫我", "怎麼辦", "該怎麼", "不知道該", "求救"]

# 回應模板
RESPONSE_TEMPLATES = {
    1: {
        "message": "很高興和你聊天！有什麼想分享的嗎？",
        "suggestions": ["可以分享今天的心情", "聊聊最近的想法"]
    },
    2: {
        "message": "聽起來你最近遇到了一些挑戰，想多聊聊嗎？",
        "suggestions": ["試著描述具體情況", "分享你的真實感受"]
    },
    3: {
        "message": "我感受到你現在很辛苦，讓我陪伴你度過這個困難時刻。",
        "suggestions": ["慢慢分享你的感受", "我會陪伴你"],
        "empathy": ["我能感受到你的痛苦"],
        "awareness": ["注意到你正在經歷困難"],
        "reframe": ["這個困難是暫時的"],
        "action": ["我們可以慢慢談談"]
    }
}

def detect_level(message: str) -> tuple:
    """簡單的 level 檢測邏輯"""
    message_lower = message.lower()
    word_count = len(message)
    keywords_found = []

    # 檢測關鍵字
    for level, keywords in LEVEL_KEYWORDS.items():
        for keyword in keywords:
            if keyword in message_lower:
                keywords_found.append(keyword)
                if level == "level_3":
                    return 3, {"keywords": keywords_found, "word_count": word_count}
                elif level == "level_2":
                    # 繼續檢查是否有 level_3
                    pass

    # 檢測求助語氣
    needs_help = any(help_word in message_lower for help_word in HELP_KEYWORDS)

    # 判斷邏輯
    if any(kw in [k for k in LEVEL_KEYWORDS["level_3"]] for kw in keywords_found):
        return 3, {"keywords": keywords_found, "word_count": word_count, "needs_help": needs_help}
    elif any(kw in [k for k in LEVEL_KEYWORDS["level_2"]] for kw in keywords_found) or (needs_help and word_count > 20):
        return 2, {"keywords": keywords_found, "word_count": word_count, "needs_help": needs_help}
    else:
        return 1, {"keywords": keywords_found, "word_count": word_count, "needs_help": needs_help}