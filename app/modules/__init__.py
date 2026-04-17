"""業務模組

包含pathly的核心業務邏輯模組：
- stl: STL狀態感知和語言轉化
- tst: TST任務導向轉化
- routing: 智能路由決策
- dialogue: 對話管理
"""

from __future__ import annotations

# 不在這裡直接導入具體類，避免循環依賴
# 各模組可以按需導入