@echo off
echo ====================================
echo     Pathly Health 檢查
echo ====================================
echo.

REM 讀取後端端口
for /f "tokens=2 delims==" %%a in ('findstr "BACKEND_PORT=" .env') do set BACKEND_PORT=%%a

echo [INFO] 檢查後端服務 (端口: %BACKEND_PORT%)
echo.

REM 1. 基礎健康檢查
echo 1. 基礎健康檢查:
curl -s http://localhost:%BACKEND_PORT%/health
if %errorlevel%==0 (
    echo [OK] 後端服務運行正常
) else (
    echo [FAIL] 後端服務無回應
    goto :end
)
echo.

REM 2. API 功能檢查
echo 2. API 功能檢查:
curl -s -X POST http://localhost:%BACKEND_PORT%/api/v1/ai/support ^
    -H "Content-Type: application/json" ^
    -d "{\"message\":\"健康檢查測試\"}"
if %errorlevel%==0 (
    echo [OK] API 功能正常
) else (
    echo [FAIL] API 功能異常
)
echo.

REM 3. CORS 檢查
echo 3. CORS 檢查:
curl -s -i -X OPTIONS http://localhost:%BACKEND_PORT%/api/v1/ai/support ^
    -H "Origin: http://localhost:5500" ^
    -H "Access-Control-Request-Method: POST" | findstr "200 OK"
if %errorlevel%==0 (
    echo [OK] CORS 配置正常
) else (
    echo [FAIL] CORS 配置異常
)
echo.

REM 4. 端口占用檢查
echo 4. 端口占用檢查:
netstat -ano | findstr :%BACKEND_PORT% | findstr LISTENING
if %errorlevel%==0 (
    echo [OK] 端口 %BACKEND_PORT% 正在監聽
) else (
    echo [FAIL] 端口 %BACKEND_PORT% 未被使用
)

:end
echo.
echo ====================================
echo 檢查完成
echo ====================================
pause