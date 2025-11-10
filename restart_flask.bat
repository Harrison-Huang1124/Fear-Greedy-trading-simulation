@echo off
chcp 65001 >nul
echo ========================================
echo   重启 Flask 后端服务器
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python！
    echo 请先安装Python 3.7+
    pause
    exit /b 1
)

REM 查找并关闭占用5000端口的进程
echo [1/3] 检查端口5000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    echo [关闭] 发现进程 %%a 占用端口5000，正在关闭...
    taskkill /F /PID %%a >nul 2>&1
    timeout /t 1 /nobreak >nul
)

echo [2/3] 等待端口释放...
timeout /t 2 /nobreak >nul

echo [3/3] 启动Flask服务器...
echo.
echo Flask将在新窗口中运行
echo 请保持该窗口打开！
echo.
start "Flask Backend - 端口5000" cmd /k "cd /d %~dp0 && python app.py"

echo.
echo ========================================
echo   重启完成！
echo ========================================
echo.
echo Flask后端: http://localhost:5000
echo.
echo [提示]
echo 1. Flask在新窗口中运行
echo 2. 请保持Flask窗口打开
echo 3. 等待几秒后访问 http://localhost:5000/api/stocks 测试
echo.
echo 按任意键关闭此窗口...
pause >nul

