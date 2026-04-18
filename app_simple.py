"""
Pathly 超精簡版 - 避免所有版本問題
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="pathly - 簡化版")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MessageRequest(BaseModel):
    user_input: str
    context: dict = {}


class MessageResponse(BaseModel):
    response: str
    success: bool = True


@app.get("/")
def home():
    return {"message": "pathly 正在運行", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/dialogue")
def dialogue(request: MessageRequest):
    # 簡化的回應邏輯
    user_input = request.user_input

    # 模擬 pathly 的溫暖回應
    response = f"我聽到了你說的「{user_input[:20]}{'...' if len(user_input) > 20 else ''}」。\n\n讓我們慢慢一起整理這些感受。你想要先從哪個部分開始說起呢？"

    return MessageResponse(response=response)


@app.post("/api/v1/process")
def process_input(request: MessageRequest):
    user_input = request.user_input

    # 簡化的四段式回應
    response = f"""## 感受確認
我聽見了你分享的想法，這些都很真實。

## 情況梳理
關於「{user_input[:30]}」，讓我們慢慢把各個面向理清楚。

## 語言轉化
也許我們可以用不同的角度來看這件事情。

## 溫柔陪伴
無論如何，我會在這裡陪你一步步慢慢整理。"""

    return MessageResponse(response=response)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)