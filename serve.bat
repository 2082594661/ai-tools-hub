@echo off
REM 静默启动 AI工具箱 网站服务器 (端口 9999)
start /min "" "C:\Users\龙潜\.workbuddy\binaries\python\versions\3.13.12\python.exe" -m http.server 9999 --bind 0.0.0.0
timeout /t 1 >nul
echo 服务器已启动: http://localhost:9999/
