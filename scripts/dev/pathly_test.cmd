@echo off
echo ========================================
echo Pathly 核心體驗測試集（10 句）
echo 測試 API: /api/v1/ai/support
echo ========================================
echo.

REM ===== Level 1 測試 =====
echo [L1_01] 預期 Level:1, emotion_detected:輕微疲勞
echo 測試輸入: "今天工作還算順利，就是有點小累"
curl -X POST http://127.0.0.1:8007/api/v1/ai/support ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"今天工作還算順利，就是有點小累\"}"
echo.
echo ----------------------------------------

echo [L1_02] 預期 Level:1, emotion_detected:輕微迴避 [模糊短句]
echo 測試輸入: "沒事"
curl -X POST http://127.0.0.1:8007/api/v1/ai/support ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"沒事\"}"
echo.
echo ----------------------------------------

echo [L1_03] 預期 Level:1, emotion_detected:輕微需求
echo 測試輸入: "今天還不錯啦，想找人聊聊天"
curl -X POST http://127.0.0.1:8007/api/v1/ai/support ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"今天還不錯啦，想找人聊聊天\"}"
echo.
echo ----------------------------------------

REM ===== Level 2 測試 =====
echo [L2_01] 預期 Level:2, emotion_detected:中度疲勞 [必須包含句]
echo 測試輸入: "我今天真的有點累"
curl -X POST http://127.0.0.1:8007/api/v1/ai/support ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"我今天真的有點累\"}"
echo.
echo ----------------------------------------

echo [L2_02] 預期 Level:2, emotion_detected:中度疲勞 [模糊短句]
echo 測試輸入: "好累"
curl -X POST http://127.0.0.1:8007/api/v1/ai/support ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"好累\"}"
echo.
echo ----------------------------------------

echo [L2_03] 預期 Level:2, emotion_detected:中度放棄 [模糊短句]
echo 測試輸入: "算了"
curl -X POST http://127.0.0.1:8007/api/v1/ai/support ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"算了\"}"
echo.
echo ----------------------------------------

echo [L2_04] 預期 Level:2, emotion_detected:中度困惑
echo 測試輸入: "最近感覺有點迷茫，不太確定方向"
curl -X POST http://127.0.0.1:8007/api/v1/ai/support ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"最近感覺有點迷茫，不太確定方向\"}"
echo.
echo ----------------------------------------

REM ===== Level 3 測試 =====
echo [L3_01] 預期 Level:3, emotion_detected:重度自貶 [邊界案例]
echo 測試輸入: "我覺得自己完全沒有價值"
curl -X POST http://127.0.0.1:8007/api/v1/ai/support ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"我覺得自己完全沒有價值\"}"
echo.
echo ----------------------------------------

echo [L3_02] 預期 Level:3, emotion_detected:重度壓力
echo 測試輸入: "感覺整個人都要崩潰了"
curl -X POST http://127.0.0.1:8007/api/v1/ai/support ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"感覺整個人都要崩潰了\"}"
echo.
echo ----------------------------------------

echo [L3_03] 預期 Level:3, emotion_detected:重度無力 [容易誤判]
echo 測試輸入: "覺得做什麼都沒有意義"
curl -X POST http://127.0.0.1:8007/api/v1/ai/support ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"覺得做什麼都沒有意義\"}"
echo.
echo ----------------------------------------

echo.
echo ========================================
echo 測試完成！
echo 重點觀察：
echo - Level 判斷準確度
echo - emotion_detected 是否合理
echo - 回應是否符合四段式語氣憲法
echo - 是否出現禁止句型
echo ========================================