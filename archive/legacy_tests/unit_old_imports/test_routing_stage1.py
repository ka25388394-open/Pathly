"""測試路由系統第一段 - 信號檢測到模式識別"""

import sys
import json
from pathlib import Path

# 添加 app 路徑
sys.path.append(str(Path(__file__).parent / "app"))

from services.routing.routing_engine import RoutingEngine


def test_routing_examples():
    """測試不同類型的輸入"""

    engine = RoutingEngine()

    # 測試案例
    test_cases = [
        {
            "name": "H1_衝動反應",
            "text": "我現在真的受不了了，忍不住想要立刻離開這個地方，很煩很煩"
        },
        {
            "name": "H2_過度控制",
            "text": "我一定要把這件事做好，不能出錯，每個步驟都要檢查，還不夠完整"
        },
        {
            "name": "H3_逃避模式",
            "text": "我知道應該要做，但想到就不想面對，一直拖著，卡住了不知道怎麼辦"
        },
        {
            "name": "H4_負面敘事",
            "text": "我總是這樣，每次都會搞砸，我是不是根本就不行，我怎麼又這樣了"
        },
        {
            "name": "H5_持續影響",
            "text": "那句話一直卡在心裡，那個眼神我會想很久，放不下那個語氣"
        },
        {
            "name": "H6_外歸因",
            "text": "都是因為別人的關係，外面的環境就是這樣，我也沒辦法改變什麼"
        },
        {
            "name": "混合低清晰度",
            "text": "就是很多東西混在一起，講不清楚，不知道從哪裡開始說..."
        }
    ]

    for test_case in test_cases:
        print(f"\n{'='*60}")
        print(f"測試案例: {test_case['name']}")
        print(f"輸入文本: {test_case['text']}")
        print(f"{'='*60}")

        # 執行分析
        result = engine.analyze_input(test_case['text'])

        # 顯示關鍵結果
        print(f"\n[分析結果]")
        print(f"  主要模式: {result.dominant_pattern}")
        if result.secondary_pattern:
            print(f"  次要模式: {result.secondary_pattern}")

        print(f"  清晰度: {result.clarity_level}")
        print(f"  強度: {result.intensity_level}")

        print(f"\n[模組分數]")
        for module, score in result.dominant_modules.items():
            print(f"  {module}: {score:.1f}")

        print(f"\n[路由建議]")
        routing = engine.get_routing_recommendation(result)
        print(f"  建議模式: {routing['selected_mode']}")
        print(f"  允許進階: {routing['allow_step_progression']}")
        print(f"  焦點提示: {routing['focus_hint']}")

        if routing['processing_notes']:
            print(f"  處理注意: {', '.join(routing['processing_notes'])}")

        print(f"\n[模式分數排名]")
        for i, pattern in enumerate(result.pattern_scores[:3]):
            print(f"  {i+1}. {pattern.pattern_id}: {pattern.score:.1f} ({pattern.confidence})")


def test_signal_detection():
    """測試信號檢測功能"""
    print(f"\n{'='*60}")
    print("信號檢測測試")
    print(f"{'='*60}")

    from services.routing.signal_detector import SignalDetector

    detector = SignalDetector()

    test_text = "我很煩，總是這樣，不知道怎麼辦，很多東西混在一起"

    signal_scores = detector.detect_signals(test_text)
    intensity, details = detector.get_signal_intensity(test_text)

    print(f"測試文本: {test_text}")
    print(f"\n信號分數:")
    print(f"  情緒信號: {signal_scores.emotion_signals}")
    print(f"  結構信號: {signal_scores.structure_signals}")
    print(f"  敘事信號: {signal_scores.narrative_signals}")
    print(f"  元認知信號: {signal_scores.metacognitive_signals}")
    print(f"  整合信號: {signal_scores.integration_signals}")

    print(f"\n整體強度: {intensity}")
    print(f"詳細分析: {details}")


if __name__ == "__main__":
    print(">> 路由系統第一段測試開始")

    # 測試信號檢測
    test_signal_detection()

    # 測試完整路由流程
    test_routing_examples()

    print(f"\n>> 測試完成")