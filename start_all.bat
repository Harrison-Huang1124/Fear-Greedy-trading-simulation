@echo off
chcp 65001 >nul
echo ========================================
echo   NeuroTrade FGI Dashboard 启动脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python！请先安装Python 3.7+
    pause
    exit /b 1
)

REM 检查Node.js是否安装
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Node.js！请先安装Node.js
    pause
    exit /b 1
)

echo [1/4] 检查依赖...
if not exist "node_modules" (
    echo [安装] 正在安装React依赖...
    call npm install
    if errorlevel 1 (
        echo [错误] npm install 失败！
        pause
        exit /b 1
    )
) else (
    echo [✓] React依赖已安装
)

echo.
echo [2/4] 启动Flask后端服务器...
echo [提示] Flask将在新窗口中运行，请保持该窗口打开
start "Flask Backend - 端口5000" cmd /k "cd /d %~dp0 && python app.py"

echo [等待] 等待Flask服务器启动...
timeout /t 5 /nobreak >nul

echo.
echo [3/4] 测试Flask API...
curl -s http://localhost:5000/api/stocks >nul 2>&1
if errorlevel 1 (
    echo [警告] Flask API可能尚未就绪，但将继续启动React...
) else (
    echo [✓] Flask API响应正常
)

echo.
echo [4/4] 启动React前端...
echo [提示] React将在新窗口中运行
start "React Frontend - 端口3000" cmd /k "cd /d %~dp0 && npm start"

echo.
echo ========================================
echo   启动完成！
echo ========================================
echo.
echo Flask后端: http://localhost:5000
echo React前端: http://localhost:3000
echo.
echo [重要提示]
echo 1. 请保持两个窗口都打开（Flask和React）
echo 2. 等待React编译完成（约30秒）
echo 3. 浏览器会自动打开，或手动访问 http://localhost:3000
echo 4. 如果看到Network Error，请检查Flask是否正常运行
echo.
echo 按任意键关闭此窗口（服务将继续运行）...
pause >nul

