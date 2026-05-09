"""Level 檢測器 - core-pathly-main"""

import re
from typing import Tuple, List, Dict
from app.core.ai_config import (
    LEVEL_KEYWORDS,
    HELP_SEEKING_PATTERNS,
    STRONG_NEGATION_PATTERNS,
    WORD_COUNT_THRESHOLDS,
    TECHNICAL_CONTEXT_KEYWORDS
)

# 狀態描述語言模式（Level 2 專用）
STATE_PATTERNS = [
    # 1. 主觀負面狀態表達（加入負面詞約束）
    {"pattern": r"我.*(很|有點|比較|還蠻|超|太).*(累|煩|痛|難受|不舒服|壓力|焦慮)", "weight": 1.5},
    # 2. 時間+負面狀態描述（排除積極表達）
    {"pattern": r"(最近|這幾天|今天|現在).*(不|沒)(?!錯|壞)", "weight": 1.0},
    # 3. 感覺/覺得+狀態
    {"pattern": r"(感覺|覺得).*(不|有點|怪)", "weight": 1.0},
    # 4. 輕度否定表達
    {"pattern": r"不(太|怎麼|是很|大).*(想|好|行)", "weight": 1.0},
    # 5. 程度+情緒詞
    {"pattern": r"(有點|一點|還蠻|比較).*(累|煩|焦慮|不安|難過)", "weight": 1.5},
    # 6. 生理狀態描述
    {"pattern": r"(睡|吃|頭).*不(好|了|行)", "weight": 1.0},
    # 7. 心理狀態模糊表達
    {"pattern": r"(心情|狀態|精神).*(不|有點|還)", "weight": 1.0},
    # 8. 能力/意願下降
    {"pattern": r"(沒有|缺乏).*(動力|興趣|精神)", "weight": 1.0}
]


class LevelDetector:
    """AI 分層等級檢測器"""

    def __init__(self):
        self.keywords = LEVEL_KEYWORDS
        self.help_patterns = HELP_SEEKING_PATTERNS
        self.negation_patterns = STRONG_NEGATION_PATTERNS
        self.thresholds = WORD_COUNT_THRESHOLDS
        self.technical_keywords = TECHNICAL_CONTEXT_KEYWORDS

    def detect_level(self, message: str) -> Tuple[int, Dict]:
        """
        檢測訊息的等級和相關資訊

        Args:
            message: 使用者輸入的訊息

        Returns:
            Tuple[int, Dict]: (等級, 分析資訊)
        """
        # 基本資訊提取
        word_count = len(message)
        keywords_found = self._extract_keywords(message)
        needs_help = self._detect_help_seeking(message)
        has_strong_negation = self._detect_strong_negation(message)
        state_patterns_score = self._detect_state_patterns(message)

        # 等級判斷
        level = self._calculate_level(
            message, word_count, keywords_found,
            needs_help, has_strong_negation, state_patterns_score
        )

        # 情緒檢測
        emotion = self._detect_emotion(level, keywords_found)

        # 信心度計算
        confidence = self._calculate_confidence(
            level, keywords_found, word_count, needs_help
        )

        analysis_info = {
            "emotion_detected": emotion,
            "keywords": keywords_found,
            "confidence": confidence,
            "word_count": word_count,
            "needs_help": needs_help,
            "has_strong_negation": has_strong_negation,
            "state_patterns_score": state_patterns_score
        }

        return level, analysis_info

    def _extract_keywords(self, message: str) -> List[str]:
        """提取訊息中的關鍵字"""
        message_lower = message.lower()
        found_keywords = []

        for level_name, categories in self.keywords.items():
            for category, words in categories.items():
                for word in words:
                    if word in message_lower:
                        found_keywords.append(word)

        return list(set(found_keywords))  # 去重

    def _detect_help_seeking(self, message: str) -> bool:
        """檢測是否有求助語氣"""
        message_lower = message.lower()

        for pattern in self.help_patterns:
            if pattern in message_lower:
                return True

        # 檢測問句
        if "?" in message or "？" in message:
            return True

        return False

    def _detect_strong_negation(self, message: str) -> bool:
        """檢測強烈否定語句"""
        message_lower = message.lower()

        for pattern in self.negation_patterns:
            if pattern in message_lower:
                return True

        return False

    def _detect_state_patterns(self, message: str) -> float:
        """檢測狀態描述語言模式（Level 2 專用）"""
        total_weight = 0.0

        for pattern_info in STATE_PATTERNS:
            pattern = pattern_info["pattern"]
            weight = pattern_info["weight"]

            if re.search(pattern, message):
                total_weight += weight

        return total_weight

    def _detect_technical_context(self, message: str) -> bool:
        """檢測是否為技術/任務語境，用於降低 Level 3 誤判"""
        message_lower = message.lower()

        # 檢查是否包含技術語境關鍵字
        for keyword in self.technical_keywords:
            if keyword in message_lower:
                return True

        return False

    def _calculate_level(self, message: str, word_count: int,
                        keywords: List[str], needs_help: bool,
                        has_strong_negation: bool, state_patterns_score: float) -> int:
        """計算等級"""

        # 獲取各級關鍵字
        level_1_keywords = []
        level_2_keywords = []
        level_3_keywords = []

        for category, words in self.keywords["level_1"].items():
            level_1_keywords.extend(words)
        for category, words in self.keywords["level_2"].items():
            level_2_keywords.extend(words)
        for category, words in self.keywords["level_3"].items():
            level_3_keywords.extend(words)

        # 計算各級分數
        level_1_count = sum(1 for kw in keywords if kw in level_1_keywords)
        level_2_count = sum(1 for kw in keywords if kw in level_2_keywords)
        level_3_count = sum(1 for kw in keywords if kw in level_3_keywords)

        # 檢查技術/任務語境（降低 Level 3 誤判）
        is_technical_context = self._detect_technical_context(message)

        # 檢查低自我價值關鍵字（直接提升至 Level 3，但技術語境除外）
        low_self_worth_keywords = self.keywords["level_3"]["low_self_worth"]
        has_low_self_worth = any(kw in keywords for kw in low_self_worth_keywords)

        if has_low_self_worth and not is_technical_context:
            return 3

        # Level 3 檢測（優先級最高，技術語境下降低權重）
        if is_technical_context:
            level_3_score = level_3_count * 1  # 技術語境下降低權重
        else:
            level_3_score = level_3_count * 2  # Level 3 關鍵字權重高

        # 強烈否定語句（技術語境下降低權重）
        if has_strong_negation:
            if is_technical_context:
                level_3_score += 1  # 技術語境下降低權重
            else:
                level_3_score += 2  # 非技術語境保持原權重

        # 長文本且有求助（降低門檻）
        if word_count > 50 and needs_help:
            level_3_score += 1

        # Level 3 門檻降低
        if level_3_score >= 2:
            return 3

        # Level 2 檢測
        level_2_score = level_2_count

        # 狀態描述語言模式（新增）
        level_2_score += state_patterns_score

        # 有求助且有負面情緒
        if needs_help and level_2_count > 0:
            level_2_score += 1

        # 短文本但有情緒關鍵字（新增）
        if word_count <= self.thresholds["short"] and level_2_count > 0:
            level_2_score += 0.5  # 短文本情緒表達加分

        # 中等長度文本
        if word_count > self.thresholds["short"]:
            level_2_score += 0.5

        # Level 2 門檻（情感表達優先）
        if level_2_score >= 1:
            return 2

        # 技術困難表達檢查：技術語境 + 困難詞 = 最低 Level 2（優先檢查）
        if is_technical_context:
            technical_difficulty_keywords = [
                "不懂", "不會", "不知道", "做不好", "失敗", "完全不", "根本不",
                "困難", "不熟", "不明白", "搞不懂", "不清楚", "不理解"
            ]
            message_lower = message.lower()
            has_difficulty = any(keyword in message_lower for keyword in technical_difficulty_keywords)

            if has_difficulty:
                return 2

        # Level 1 檢測（積極判斷）
        level_1_score = level_1_count

        # 短文本且無負面（但有狀態模式則不適用）
        if word_count <= self.thresholds["short"] and level_2_count == 0 and level_3_count == 0 and state_patterns_score == 0:
            level_1_score += 1

        # 有正面關鍵字
        if level_1_count > 0:
            return 1

        # 簡單問候或短文本（但有 Level 2+ 關鍵字或狀態模式則不適用）
        if word_count <= 15 and not needs_help and level_2_count == 0 and level_3_count == 0 and state_patterns_score == 0:
            return 1

        # 如果沒有明確指標，預設 Level 2（更安全的陪伴）
        return 2

    def _detect_emotion(self, level: int, keywords: List[str]) -> str:
        """根據等級和關鍵字檢測情緒"""
        if level == 3:
            if any(kw in keywords for kw in ["痛苦", "絕望", "崩潰"]):
                return "深度痛苦"
            elif any(kw in keywords for kw in ["自殺", "結束", "放棄"]):
                return "危機狀態"
            else:
                return "嚴重困擾"

        elif level == 2:
            if any(kw in keywords for kw in ["累", "疲憊", "壓力"]):
                return "輕微壓力"
            elif any(kw in keywords for kw in ["困惑", "迷茫", "不知道"]):
                return "困惑不安"
            else:
                return "輕度困擾"

        else:  # level == 1
            if any(kw in keywords for kw in ["開心", "高興", "不錯"]):
                return "積極正面"
            else:
                return "中性平和"

    def _calculate_confidence(self, level: int, keywords: List[str],
                            word_count: int, needs_help: bool) -> float:
        """計算信心度"""
        base_confidence = 0.5

        # 關鍵字匹配加成
        if keywords:
            base_confidence += min(0.3, len(keywords) * 0.1)

        # 字數合理性加成
        if level == 1 and word_count <= self.thresholds["short"]:
            base_confidence += 0.1
        elif level == 2 and self.thresholds["short"] < word_count <= self.thresholds["medium"]:
            base_confidence += 0.1
        elif level == 3 and word_count > self.thresholds["long"]:
            base_confidence += 0.1

        # 求助語氣加成
        if needs_help and level > 1:
            base_confidence += 0.1

        return min(1.0, base_confidence)