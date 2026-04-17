"""統一的AI客戶端

整合所有AI調用功能，替代散亂的多個客戶端文件：
- ai_client.py (基礎AI調用)
- dialogue_ai_client.py (對話專用)
- integrated_dialogue_client.py (整合對話)

提供統一的介面，支援不同的AI調用場景。
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional, Union, TypeVar

from pydantic import BaseModel, ValidationError

from app.config import get_settings
from app.core.tone_guard import assert_tone, scan_all
from app.core.lazy_data_loader import get_prompt_lazy, get_tone_charter_lazy
from ..modules.routing import SmartRouter
from ..modules.dialogue.response_modes import ResponseModeManager

T = TypeVar('T', bound=BaseModel)


class UnifiedAIClient:
    """統一的AI客戶端 - 處理所有AI調用需求"""

    def __init__(self):
        self.settings = get_settings()
        self.router = SmartRouter()
        self.response_manager = ResponseModeManager()

    async def process_input(
        self,
        user_input: str,
        input_type: str = "dialogue",
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        統一的輸入處理入口

        Args:
            user_input: 用戶輸入
            input_type: 輸入類型 ("dialogue", "stl", "tst", "auto")
            context: 上下文信息

        Returns:
            處理結果字典
        """
        if input_type == "auto":
            # 自動路由
            routing_result = await self.router.route(user_input, context)
            selected_module = routing_result["selected_module"]
        else:
            # 指定模組
            selected_module = input_type

        # 根據模組類型調用相應的處理方法
        if selected_module == "stl":
            return await self._process_stl_input(user_input, context)
        elif selected_module == "tst":
            return await self._process_tst_input(user_input, context)
        else:
            return await self._process_dialogue_input(user_input, context)

    async def _process_dialogue_input(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """處理對話輸入"""
        try:
            # 使用對話回應模式管理器
            response_mode = self.response_manager.determine_mode(user_input, context)

            # 構建AI回應
            if self.settings.mock_ai:
                response_text = self._generate_mock_dialogue_response(user_input, response_mode)
            else:
                response_text = await self._call_ai_for_dialogue(user_input, response_mode, context)

            return {
                "response": response_text,
                "mode": response_mode,
                "type": "dialogue",
                "success": True
            }

        except Exception as e:
            return {
                "response": "抱歉，處理過程中遇到了問題，讓我們換個方式聊聊？",
                "mode": "supportive",
                "type": "dialogue",
                "success": False,
                "error": str(e)
            }

    async def _process_stl_input(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """處理STL分析輸入"""
        try:
            # STL專用處理邏輯
            if self.settings.mock_ai:
                response_text = self._generate_mock_stl_response(user_input)
            else:
                response_text = await self._call_ai_for_stl(user_input, context)

            return {
                "response": response_text,
                "type": "stl_analysis",
                "success": True
            }

        except Exception as e:
            return {
                "response": "在分析過程中遇到了問題，我們可以先從簡單的分享開始。",
                "type": "stl_analysis",
                "success": False,
                "error": str(e)
            }

    async def _process_tst_input(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """處理TST任務輸入"""
        try:
            # TST專用處理邏輯
            if self.settings.mock_ai:
                response_text = self._generate_mock_tst_response(user_input)
            else:
                response_text = await self._call_ai_for_tst(user_input, context)

            return {
                "response": response_text,
                "type": "tst_task",
                "success": True
            }

        except Exception as e:
            return {
                "response": "在規劃過程中遇到了問題，讓我們一步步慢慢來。",
                "type": "tst_task",
                "success": False,
                "error": str(e)
            }

    def _generate_mock_dialogue_response(self, user_input: str, mode: str) -> str:
        """生成mock對話回應"""
        mock_responses = {
            "supportive": f"我聽到了你分享的「{user_input[:20]}...」，這些感受很真實。想再多聊聊嗎？",
            "exploratory": f"關於「{user_input[:20]}...」，我很好奇背後的想法。可以多說一些嗎？",
            "reflective": f"聽起來「{user_input[:20]}...」對你來說很重要。讓我們一起慢慢梳理。"
        }
        return mock_responses.get(mode, "謝謝你的分享，我在這裡陪你。")

    def _generate_mock_stl_response(self, user_input: str) -> str:
        """生成mock STL回應"""
        return f"""## 感受確認
我聽見你提到了{user_input[:30]}，這些感受都很真實。

## 情況梳理
讓我們慢慢把這個情況的各個面向理清楚。

## 語言轉化
也許我們可以用不同的角度來看這件事。

## 陪伴支持
無論如何，我會在這裡陪你慢慢整理。"""

    def _generate_mock_tst_response(self, user_input: str) -> str:
        """生成mock TST回應"""
        return f"""## 現況覺察
關於{user_input[:30]}，讓我們先看看現在的狀況。

## 重新框架
也許我們可以從另一個角度來理解這個狀況。

## 行動可能
一些小小的步驟可能會帶來改變。

## 溫柔前行
記住，改變可以很緩慢，很溫柔。"""

    async def _call_ai_for_dialogue(
        self,
        user_input: str,
        mode: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """實際的對話AI調用 (Phase 2實現)"""
        # TODO: 實現真實的AI調用
        raise NotImplementedError("Phase 2 實現真實AI調用")

    async def _call_ai_for_stl(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """實際的STL AI調用 (Phase 2實現)"""
        # TODO: 實現真實的AI調用
        raise NotImplementedError("Phase 2 實現真實AI調用")

    async def _call_ai_for_tst(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """實際的TST AI調用 (Phase 2實現)"""
        # TODO: 實現真實的AI調用
        raise NotImplementedError("Phase 2 實現真實AI調用")

    def build_prompt(
        self,
        prompt_name: str,
        variables: Dict[str, Any],
        include_tone_charter: bool = True
    ) -> str:
        """構建完整的prompt - 使用懶載入"""
        # 按需載入prompt模板
        template = get_prompt_lazy(prompt_name)

        # 變量替換
        for key, value in variables.items():
            template = template.replace(f"{{{key}}}", str(value))

        # 按需加入語調憲章
        if include_tone_charter:
            tone_charter = get_tone_charter_lazy()
            template = f"{tone_charter}\n\n{template}"

        return template