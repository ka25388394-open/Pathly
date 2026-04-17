"""核心模組

提供應用的基礎設施和共享功能：
- unified_ai_client: 統一的AI調用客戶端
- tone_guard: 語調檢查和保護
"""

from __future__ import annotations

from .unified_ai_client import UnifiedAIClient
from .tone_guard import assert_tone, scan_all

__all__ = [
    "UnifiedAIClient",
    "assert_tone",
    "scan_all"
]