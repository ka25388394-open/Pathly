@echo off
echo ====================================
echo      Pathly 本地開發啟動器
echo ====================================
echo.

REM 確保在專案根目錄
cd /d %~dp0

REM 檢查是否在正確目錄
if not exist "app\main.py" (
    echo [ERROR] 不在 Pathly 專案根目錄
    echo 請在 pathly 目錄中執行此腳本
    pause
    exit /b 1
)

REM 讀取並顯示配置
echo [INFO] 載入配置...
for /f "tokens=2 delims==" %%a in ('findstr "PROJECT_NAME=" .env') do set PROJECT_NAME=%%a
for /f "tokens=2 delims==" %%a in ('findstr "ENV=" .env') do set ENV=%%a
for /f "tokens=2 delims==" %%a in ('findstr "BACKEND_PORT=" .env') do set BACKEND_PORT=%%a
for /f "tokens=2 delims==" %%a in ('findstr "FRONTEND_PORT=" .env') do set FRONTEND_PORT=%%a

echo.
echo PROJECT_NAME: %PROJECT_NAME%
echo ENV: %ENV%
echo BACKEND_PORT: %BACKEND_PORT%
echo FRONTEND_PORT: %FRONTEND_PORT%
echo.

REM 檢查端口是否被占用
echo [INFO] 檢查端口 %BACKEND_PORT%...
curl -s http://localhost:%BACKEND_PORT%/health >nul 2>&1
if %errorlevel%==0 (
    echo [WARNING] 端口 %BACKEND_PORT% 已被使用
    echo 請先執行: python cleanup_services.py
    pause
    exit /b 1
) else (
    echo [OK] 端口 %BACKEND_PORT% 可用
)

echo.
echo [INFO] 啟動 Pathly 後端服務...
echo [CMD] python -m uvicorn app.main:app --host 0.0.0.0 --port %BACKEND_PORT%
echo.
echo 按 Ctrl+C 停止服務
echo 前端請使用: http://localhost:%FRONTEND_PORT%/pathly_simple_ui.html
echo API 基礎路徑: http://localhost:%BACKEND_PORT%/api/v1
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port %BACKEND_PORT%

pause