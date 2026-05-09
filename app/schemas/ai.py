"""AI 分層系統資料模型 - core-pathly-main"""

from typing import List, Optional
from pydantic import BaseModel, Field


class SupportRequest(BaseModel):
    """AI 支援請求模型"""
    model_config = {"str_strip_whitespace": True}

    message: str = Field(..., min_length=1, max_length=2000, description="使用者輸入的訊息")
    session_id: Optional[str] = Field(None, description="會話 ID（可選）")


class AnalysisResult(BaseModel):
    """分析結果模型"""
    emotion_detected: str = Field(..., description="偵測到的情緒")
    keywords: List[str] = Field(default_factory=list, description="關鍵字列表")
    confidence: float = Field(..., ge=0.0, le=1.0, description="信心度 0-1")
    word_count: int = Field(..., ge=0, description="字數統計")
    needs_help: bool = Field(default=False, description="是否需要幫助")
    has_strong_negation: bool = Field(default=False, description="是否有強烈否定語句")


class ResponseContent(BaseModel):
    """回應內容模型"""
    message: str = Field(..., description="主要回應訊息")
    suggestions: List[str] = Field(default_factory=list, description="建議列表")
    next_questions: Optional[List[str]] = Field(default=None, description="後續問題（可選）")

    # Level 2 專用：人類狀態解析結果（可選）
    domain: Optional[str] = Field(None, description="生活領域（Level 2 專用）")
    state: Optional[str] = Field(None, description="當前狀態（Level 2 專用）")
    drive: Optional[str] = Field(None, description="內在驅動（Level 2 專用）")


class Level3Response(ResponseContent):
    """Level 3 專用回應模型（含結構化欄位）"""
    empathy: List[str] = Field(default_factory=list, description="同理心回應")
    awareness: List[str] = Field(default_factory=list, description="覺察回應")
    reframe: List[str] = Field(default_factory=list, description="重新框架")
    action: List[str] = Field(default_factory=list, description="行動建議")


class SupportResponse(BaseModel):
    """AI 支援回應模型"""
    success: bool = Field(default=True, description="請求是否成功")
    data: "SupportResponseData" = Field(..., description="回應資料")


class SupportResponseData(BaseModel):
    """回應資料內容"""
    level: int = Field(..., ge=1, le=3, description="判斷等級 1-3")
    analysis: AnalysisResult = Field(..., description="分析結果")
    response: ResponseContent = Field(..., description="回應內容")
    metadata: "ResponseMetadata" = Field(..., description="元資料")


class ResponseMetadata(BaseModel):
    """回應元資料"""
    model_config = {"protected_namespaces": ()}

    processing_time_ms: int = Field(..., ge=0, description="處理時間（毫秒）")
    model_used: str = Field(default="rule_based", description="使用的模型")
    session_id: Optional[str] = Field(None, description="會話 ID")
    timestamp: str = Field(..., description="時間戳")
    reset_signal: bool = Field(default=False, description="是否偵測到換話題訊號")
    reset_reason: Optional[str] = Field(None, description="觸發 reset 的原因關鍵詞")
    tst_marker: Optional[str] = Field(None, description="TST 路由標記")


class ErrorResponse(BaseModel):
    """錯誤回應模型"""
    success: bool = Field(default=False, description="請求是否成功")
    error: str = Field(..., description="錯誤訊息")
    code: str = Field(..., description="錯誤代碼")


# === Dev Mode Models ===

class DevRequest(BaseModel):
    """開發模式請求模型"""
    model_config = {"str_strip_whitespace": True}

    message: str = Field(..., min_length=1, max_length=1000, description="開發問題或需求")
    session_id: Optional[str] = Field(None, description="會話 ID（可選）")


class DevResponseData(BaseModel):
    """開發模式回應資料模型（遵循 SYSTEM_PROMPT 四段式結構）"""
    current_stage: str = Field(..., description="現在階段")
    problem_essence: str = Field(..., description="問題本質（一句話）")
    next_step: str = Field(..., description="最小下一步（只能一條）")
    claude_prompt: Optional[str] = Field(None, description="必要時的 Claude Prompt")
    processing_time_ms: int = Field(..., description="處理時間（毫秒）")
    session_id: str = Field(..., description="會話 ID")


class DevResponse(BaseModel):
    """開發模式回應模型"""
    success: bool = Field(default=True, description="請求是否成功")
    data: DevResponseData = Field(..., description="回應資料")