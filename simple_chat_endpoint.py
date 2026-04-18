"""簡化的聊天端點 - 避免複雜依賴"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI()

class ChatRequest(BaseModel):
    user_input: str
    user_id: str = "anonymous"
    context: dict = {}

class ChatResponse(BaseModel):
    response: str
    success: bool = True

# 簡化的回應模板
RESPONSE_TEMPLATES = {
    "焦慮": [
        "我感受到你的緊張感。這種時候，記住你並不孤單，我們可以慢慢一起面對。",
        "焦慮的感覺確實不好受。要不要試著深呼吸幾次，讓自己放慢節奏？"
    ],
    "沮喪": [
        "我聽見了你的難過。這些感受都很真實，允許自己感受它們是可以的。",
        "低落的時候特別需要對自己溫柔。今天有什麼小小的事情讓你感到一點點好的嗎？"
    ],
    "困惑": [
        "困惑的時候不用急著找答案。我們可以慢慢梳理，一點一點來。",
        "不知道也沒關係，這本身就是一種誠實的狀態。想從哪裡開始說起呢？"
    ],
    "煩": [
        "聽起來你現在很煩躁。這種感覺我理解，有時候就是會有一堆事情湧上心頭。",
        "煩的時候很正常，不用壓抑。想說說是什麼讓你感到煩嗎？"
    ],
    "default": [
        "謝謝你願意和我分享。我在這裡陪你慢慢整理這些感受。",
        "我聽見了你想說的話。無論什麼感受，都是值得被理解的。",
        "這樣的心情我懂。要不要慢慢跟我說說現在的狀況？"
    ]
}

def detect_emotion(text: str) -> str:
    """簡單的情緒檢測"""
    if any(word in text for word in ["緊張", "焦慮", "擔心", "不安"]):
        return "焦慮"
    elif any(word in text for word in ["難過", "沮喪", "低落", "憂鬱"]):
        return "沮喪"
    elif any(word in text for word in ["困惑", "不知道", "混亂", "搞不清楚"]):
        return "困惑"
    elif any(word in text for word in ["煩", "煩躁", "火大", "生氣"]):
        return "煩"
    else:
        return "default"

@app.get("/health")
def health():
    return {"status": "ok", "service": "pathly-simple"}

@app.post("/api/v1/simple-chat", response_model=ChatResponse)
def simple_chat(request: ChatRequest):
    """簡化的聊天端點"""
    try:
        emotion = detect_emotion(request.user_input)
        templates = RESPONSE_TEMPLATES.get(emotion, RESPONSE_TEMPLATES["default"])
        response_text = random.choice(templates)

        # 簡單個人化
        if len(request.user_input) > 30:
            response_text += "\n\n想要繼續跟我說說嗎？"

        return ChatResponse(response=response_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"聊天處理失敗: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)