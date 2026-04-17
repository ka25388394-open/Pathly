"""pytest配置文件"""

import pytest
import sys
from pathlib import Path

# 添加項目根目錄到路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def mock_settings():
    """Mock應用設置"""
    class MockSettings:
        app_env = "test"
        app_debug = True
        database_url = "sqlite:///:memory:"
        mock_ai = True
        tone_reviewer_enabled = False

    return MockSettings()


@pytest.fixture
def sample_user_input():
    """示例用戶輸入"""
    return "我最近感覺很焦慮，不知道該怎麼辦"


@pytest.fixture
def sample_context():
    """示例上下文"""
    return {
        "user_id": "test_user",
        "previous_interactions": 2,
        "session_id": "test_session"
    }