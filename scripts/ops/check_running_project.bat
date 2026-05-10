@echo off
echo ===== 專案運行狀態檢查 =====
echo.

echo 1. 檢查所有 Python 進程:
tasklist | findstr python.exe

echo.
echo 2. 檢查端口占用:
netstat -ano | findstr :8006
netstat -ano | findstr :8007
netstat -ano | findstr :5000
netstat -ano | findstr :3000

echo.
echo 3. 檢查目前目錄:
echo 當前目錄: %cd%
echo.

echo 4. 快速健康檢查:
curl -s http://localhost:8006/health 2>nul
if %errorlevel%==0 (
    echo [8006] 服務運行中
    curl -s http://localhost:8006/health
) else (
    echo [8006] 服務未運行
)

curl -s http://localhost:8007/health 2>nul
if %errorlevel%==0 (
    echo [8007] 服務運行中
    curl -s http://localhost:8007/health
) else (
    echo [8007] 服務未運行
)

echo.
echo ===== 檢查完成 =====