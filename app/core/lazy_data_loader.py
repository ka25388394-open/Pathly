"""懶載入資料載入器 - 避免啟動時載入大量靜態檔案"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional
from functools import lru_cache

from app.config import PROMPTS_DIR, TONE_CHARTER_PATH


class LazyDataLoader:
    """懶載入資料管理器"""

    def __init__(self):
        self._prompt_cache: Dict[str, str] = {}
        self._tone_charter: Optional[str] = None

    def get_prompt(self, prompt_name: str, use_cache: bool = True) -> str:
        """
        按需載入prompt檔案

        Args:
            prompt_name: prompt檔案名（不含.md）
            use_cache: 是否使用緩存
        """
        cache_key = f"prompt_{prompt_name}"

        # 檢查緩存
        if use_cache and cache_key in self._prompt_cache:
            return self._prompt_cache[cache_key]

        # 載入檔案
        prompt_path = PROMPTS_DIR / f"{prompt_name}.md"
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

        content = prompt_path.read_text(encoding="utf-8")

        # 緩存（如果啟用）
        if use_cache:
            self._prompt_cache[cache_key] = content

        return content

    def get_tone_charter(self, use_cache: bool = True) -> str:
        """
        按需載入語調憲章

        Args:
            use_cache: 是否使用緩存
        """
        if use_cache and self._tone_charter is not None:
            return self._tone_charter

        content = TONE_CHARTER_PATH.read_text(encoding="utf-8")

        if use_cache:
            self._tone_charter = content

        return content

    def clear_cache(self):
        """清除所有緩存（記憶體回收）"""
        self._prompt_cache.clear()
        self._tone_charter = None

    def get_cache_info(self) -> Dict[str, int]:
        """獲取緩存狀態"""
        return {
            "prompts_cached": len(self._prompt_cache),
            "tone_charter_cached": 1 if self._tone_charter else 0,
            "estimated_memory_kb": self._estimate_memory_usage()
        }

    def _estimate_memory_usage(self) -> int:
        """估算記憶體使用（KB）"""
        total_chars = 0

        # 計算prompt緩存
        for content in self._prompt_cache.values():
            total_chars += len(content)

        # 計算tone charter
        if self._tone_charter:
            total_chars += len(self._tone_charter)

        # 估算：1字符 ≈ 1字節，加上對象開銷
        return int(total_chars / 1024 * 1.2)  # 20%開銷


# 全局懶載入器實例
lazy_loader = LazyDataLoader()


# 便捷函數
def get_prompt_lazy(prompt_name: str) -> str:
    """便捷函數：按需載入prompt"""
    return lazy_loader.get_prompt(prompt_name, use_cache=True)


def get_tone_charter_lazy() -> str:
    """便捷函數：按需載入語調憲章"""
    return lazy_loader.get_tone_charter(use_cache=True)