"""人類狀態分類器 - MVP 階段 1：基礎骨架"""

from typing import Dict, Any


def classify_basic_state(text: str) -> Dict[str, str]:
    """
    基礎狀態分類器 - 使用最簡單的 keyword 規則

    Args:
        text: 用戶輸入文本

    Returns:
        Dict 包含 domain, state, drive, message
    """
    text_lower = text.lower()

    # Domain 分類 - 生活領域
    domain = _classify_domain(text_lower)

    # State 分類 - 當前狀態
    state = _classify_state(text_lower)

    # Drive 分類 - 內在動力
    drive = _classify_drive(text_lower)

    # Message 生成 - 固定模板
    message = _generate_message(domain, state, drive)

    return {
        "domain": domain,
        "state": state,
        "drive": drive,
        "message": message
    }


def _classify_domain(text: str) -> str:
    """領域分類 - 官方枚舉"""

    # 關係
    if any(word in text for word in ["friend", "relationship", "朋友", "家人", "關係", "伴侶", "同事關係"]):
        return "關係"

    # 工作
    elif any(word in text for word in ["work", "job", "工作", "上班", "職場", "老闆", "專案"]):
        return "工作"

    # 創作
    elif any(word in text for word in ["創作", "寫作", "設計", "藝術", "表達", "創意"]):
        return "創作"

    # 挑戰
    elif any(word in text for word in ["挑戰", "困難", "obstacle", "challenge", "克服", "突破"]):
        return "挑戰"

    # 預設：生活
    else:
        return "生活"


def _classify_state(text: str) -> str:
    """狀態分類 - 官方枚舉"""

    # 痛苦中
    if any(word in text for word in ["痛苦", "很痛", "受傷", "崩潰", "痛", "hurt", "pain"]):
        return "痛苦中"

    # 疲勞中 - 新增分類專門處理疲勞短句
    elif any(word in text for word in ["空", "累", "好累", "疲倦", "疲憊", "tired", "exhausted", "精疲力盡", "空掉", "有點空掉", "整個人有點空掉", "不太想做", "什麼都不太想做", "有點空", "不太想動", "沒什麼力氣", "不想動", "整個人"]):
        return "疲勞中"

    # 拉扯中
    elif any(word in text for word in ["不知道", "困惑", "矛盾", "糾結", "confused", "torn", "拉扯"]):
        return "拉扯中"

    # 修復中
    elif any(word in text for word in ["修復", "療傷", "恢復", "調整", "healing", "recover"]):
        return "修復中"

    # 成長中
    elif any(word in text for word in ["成長", "進步", "學習", "提升", "變好", "growth", "improve"]):
        return "成長中"

    # 預設：穩定中
    else:
        return "穩定中"


def _classify_drive(text: str) -> str:
    """動力分類 - 官方枚舉"""

    # 防衛型
    if any(word in text for word in ["保護", "防禦", "害怕", "不想", "避免", "defend", "protect", "afraid"]):
        return "防衛型"

    # 追尋型
    elif any(word in text for word in ["想要", "追求", "尋找", "想變好", "want", "seek", "pursue"]):
        return "追尋型"

    # 預設：混合型
    else:
        return "混合型"


def _generate_message(domain: str, state: str, drive: str) -> str:
    """生成回應訊息 - 根據狀態調整語氣（第2階段：產品化）"""

    # 第一句：映照（根據 state 調整語氣）
    reflection = _generate_reflection(domain, state)

    # 第二句：選擇問句（根據 drive 調整方向）
    choice_question = _generate_choice_question(domain, state, drive)

    return f"{reflection} {choice_question}"


def _generate_reflection(domain: str, state: str) -> str:
    """第一句：映照用戶狀態（官方規格 - 根據 state 調整語氣）"""

    # 痛苦中 → 輕、慢、不推
    if state == "痛苦中":
        reflections = {
            "關係": "關係中的痛苦感覺很真實。",
            "工作": "工作帶來的痛苦感受到了。",
            "生活": "生活中的痛苦你正在承受著。",
            "創作": "創作路上的痛苦很不容易。",
            "挑戰": "面對挑戰時的痛苦是真實的。"
        }

    # 疲勞中 → 先承接疲勞感
    elif state == "疲勞中":
        reflections = {
            "關係": "聽起來你在關係中真的有點累。",
            "工作": "聽起來你工作上真的有點累。",
            "生活": "聽起來你今天真的有點累。",
            "創作": "聽起來你在創作上真的有點累。",
            "挑戰": "聽起來你面對挑戰時真的有點累。"
        }

    # 拉扯中 → 描述兩股力量
    elif state == "拉扯中":
        reflections = {
            "關係": "關係裡好像有兩股力量在拉扯。",
            "工作": "工作上有些事情讓你左右為難。",
            "生活": "生活中有些矛盾的感覺。",
            "創作": "創作時內心有些糾結。",
            "挑戰": "面對挑戰時心裡有些拉扯。"
        }

    # 修復中 → 幫他縮小一點
    elif state == "修復中":
        reflections = {
            "關係": "關係修復的路上有些在意的地方。",
            "工作": "工作調整中有些需要關注的。",
            "生活": "生活修復中有些重要的點。",
            "創作": "創作修復期有些想釐清的。",
            "挑戰": "挑戰修復中有些要處理的。"
        }

    # 穩定中 → 幫他縮小一點
    elif state == "穩定中":
        reflections = {
            "關係": "關係穩定中還有些想確認的。",
            "工作": "工作穩定下來有些想整理的。",
            "生活": "生活穩定中有些想調整的。",
            "創作": "創作穩定期有些想優化的。",
            "挑戰": "挑戰穩定後有些想改善的。"
        }

    # 成長中 → 微微往前帶
    elif state == "成長中":
        reflections = {
            "關係": "關係成長的路上有些新的可能。",
            "工作": "工作成長中看到一些機會。",
            "生活": "生活成長期有些期待的方向。",
            "創作": "創作成長中有些想嘗試的。",
            "挑戰": "挑戰成長期有些想探索的。"
        }

    # 預設
    else:
        reflections = {
            "關係": f"關係中感到{state}。",
            "工作": f"工作上感到{state}。",
            "生活": f"生活中感到{state}。",
            "創作": f"創作時感到{state}。",
            "挑戰": f"面對挑戰時感到{state}。"
        }

    return reflections.get(domain, f"在{domain}方面感到{state}。")


def _generate_choice_question(domain: str, state: str, drive: str) -> str:
    """第二句：選擇問句（官方規格 - 根據 state/drive 組合調整）"""

    # 疲勞中 → 先不急著整理原因，先分清楚類型
    if state == "疲勞中":
        questions = {
            "關係": "先不用急著整理原因，我們可以先分清楚：這比較像是關係讓你心累，還是身體也有點撐著？",
            "工作": "先不用急著整理原因，我們可以先分清楚：這比較像是工作讓你心累，還是身體也有點撐著？",
            "生活": "先不用急著整理原因，我們可以先分清楚：這比較像身體累，還是心裡也有點撐著？",
            "創作": "先不用急著整理原因，我們可以先分清楚：這比較像是創作讓你心累，還是身體也有點撐著？",
            "挑戰": "先不用急著整理原因，我們可以先分清楚：這比較像是心理上累，還是身體也有點撐著？"
        }
        return questions.get(domain, "先不用急著整理原因，我們可以先分清楚：這比較像身體累，還是心裡也有點撐著？")

    # 痛苦中 + 防衛型 → 輕、慢、不推（用「卡」的句型）
    elif state == "痛苦中" and drive == "防衛型":
        questions = {
            "關係": "你現在比較卡的是想保護自己，還是想修復關係？",
            "工作": "你現在比較卡的是想遠離工作壓力，還是想找到安全感？",
            "生活": "你現在比較卡的是想要休息，還是想要安全感？",
            "創作": "你現在比較卡的是害怕表達，還是想要保護作品？",
            "挑戰": "你現在比較卡的是想要避開，還是想要保護自己？"
        }

    # 拉扯中 + 混合型 → 描述兩股力量（用「想先」句型）
    elif state == "拉扯中" and drive == "混合型":
        questions = {
            "關係": "你比較想先理清自己的感受，還是先理清關係的方向？",
            "工作": "你比較想先穩定現狀，還是先嘗試改變？",
            "生活": "你比較想先處理眼前的，還是先想想未來的？",
            "創作": "你比較想先完成手上的，還是先探索新的？",
            "挑戰": "你比較想先退一步觀察，還是先往前試試？"
        }

    # 修復中 → 幫他縮小一點（用「想先」句型）
    elif state == "修復中":
        questions = {
            "關係": "你比較想先修復信任，還是先修復溝通？",
            "工作": "你比較想先調整工作方式，還是先調整工作心態？",
            "生活": "你比較想先調整作息，還是先調整心情？",
            "創作": "你比較想先修復創作動力，還是先修復創作技巧？",
            "挑戰": "你比較想先修復信心，還是先修復方法？"
        }

    # 穩定中 → 幫他縮小一點（用「想先」句型）
    elif state == "穩定中":
        questions = {
            "關係": "你比較想先鞏固現在的關係，還是先探索關係的可能？",
            "工作": "你比較想先深化工作技能，還是先拓展工作範圍？",
            "生活": "你比較想先維持現在的節奏，還是先加入新的元素？",
            "創作": "你比較想先精進現有技巧，還是先嘗試新風格？",
            "挑戰": "你比較想先穩固基礎，還是先挑戰更高目標？"
        }

    # 成長中 + 追尋型 → 微微往前帶（用「想先」句型）
    elif state == "成長中" and drive == "追尋型":
        questions = {
            "關係": "你比較想先深化關係品質，還是先拓展關係圈？",
            "工作": "你比較想先提升專業能力，還是先探索新領域？",
            "生活": "你比較想先優化生活品質，還是先嘗試新體驗？",
            "創作": "你比較想先突破創作技法，還是先探索創作主題？",
            "挑戰": "你比較想先征服當前挑戰，還是先尋找新挑戰？"
        }

    # 其他組合 → 通用選擇（用「想先」句型）
    else:
        questions = {
            "關係": "你比較想先聊聊關係的感受，還是先想想關係的方向？",
            "工作": "你比較想先聊聊工作的狀況，還是先想想工作的調整？",
            "生活": "你比較想先聊聊生活的感受，還是先想想生活的安排？",
            "創作": "你比較想先聊聊創作的感受，還是先想想創作的方向？",
            "挑戰": "你比較想先聊聊挑戰的感受，還是先想想應對的方法？"
        }

    return questions.get(domain, "你比較想先聊聊感受，還是先想想方向？")


# 測試函式（開發用）
def test_classifier():
    """簡單測試"""
    test_cases = [
        "我工作很累",
        "朋友關係讓我困惑",
        "學習上很迷茫",
        "想要變得更好"
    ]

    for case in test_cases:
        result = classify_basic_state(case)
        print(f"輸入: {case}")
        print(f"結果: {result}")
        print("---")


def test_official_states():
    """測試官方規格：5 組 state 的語氣效果"""
    print("=== 官方規格語氣測試 ===\n")

    official_scenarios = [
        # 5 組官方 state 測試
        ("關係", "痛苦中", "防衛型", "關係中感到痛苦想保護自己"),
        ("工作", "拉扯中", "混合型", "工作讓我左右為難"),
        ("生活", "修復中", "混合型", "生活在修復中"),
        ("創作", "穩定中", "追尋型", "創作穩定想提升"),
        ("挑戰", "成長中", "追尋型", "面對挑戰想成長")
    ]

    for domain, state, drive, scenario in official_scenarios:
        message = _generate_message(domain, state, drive)
        print(f"情境: {scenario}")
        print(f"分類: {domain}/{state}/{drive}")
        print(f"回應: {message}")
        print("---")


if __name__ == "__main__":
    test_classifier()