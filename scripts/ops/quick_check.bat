@echo off
echo 當前目錄: %cd%
echo.
echo 端口狀態:
for %%p in (8006 8007 5000) do (
    echo | set /p="端口 %%p: "
    curl -s http://localhost:%%p/health 2>nul && echo 運行中 || echo 停止
)
echo.
echo Python 進程數量:
tasklist | findstr python.exe | find /c "python.exe"