@echo off
title Project Manager - core-pathly-main
color 0A

:menu
cls
echo ========================================
echo       Project Manager
echo       core-pathly-main (PORT 5000)
echo ========================================
echo.
echo 1. Start Pathly (with port check)
echo 2. Start Pathly (force)
echo 3. Check port 5000 status
echo 4. Stop all Python processes
echo 5. Open health check in browser
echo 6. Open API docs in browser
echo 7. Exit
echo.
set /p choice="Select option (1-7): "

if "%choice%"=="1" goto start_with_check
if "%choice%"=="2" goto start_force
if "%choice%"=="3" goto check_port
if "%choice%"=="4" goto stop_python
if "%choice%"=="5" goto open_health
if "%choice%"=="6" goto open_docs
if "%choice%"=="7" goto exit

echo Invalid option. Press any key to continue...
pause >nul
goto menu

:start_with_check
echo.
echo Starting with port check...
call check_port_before_start.bat
pause
goto menu

:start_force
echo.
echo Force starting core-pathly-main...
call start_pathly.bat
pause
goto menu

:check_port
echo.
echo Checking port 5000...
python check_port.py
echo.
pause
goto menu

:stop_python
echo.
echo Stopping all Python processes...
taskkill /f /im python.exe 2>nul
taskkill /f /im pythonw.exe 2>nul
echo Done. All Python processes stopped.
echo.
pause
goto menu

:open_health
echo.
echo Opening health check in browser...
start http://localhost:5000/health
goto menu

:open_docs
echo.
echo Opening API docs in browser...
start http://localhost:5000/docs
goto menu

:exit
echo.
echo Goodbye!
exit