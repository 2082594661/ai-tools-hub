@echo off
REM 本地启动 AI工具箱 网站 (端口 9999)
start /min cmd /c "cd /d "%~dp0" && "C:\Users\龙潜\.workbuddy\binaries\python\versions\3.13.12\python.exe" -m http.server 9999 --bind 0.0.0.0"
timeout /t 2 >nul
echo.
echo   AI工具箱已启动
echo   浏览器打开: http://localhost:9999/
echo.
pause
