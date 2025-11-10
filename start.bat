@echo off
echo 正在启动股票模拟交易系统...
echo.

REM 检查Python是否安装
py --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7或更高版本
    echo 请访问 https://www.python.org/downloads/ 下载并安装Python
    pause
    exit /b 1
)

REM 安装依赖
echo 正在安装依赖包...
py -m pip install -r requirements.txt

REM 启动应用
echo.
echo 启动应用...
echo 请在浏览器中访问: http://localhost:5000
echo 按 Ctrl+C 停止应用
echo.
py app.py

pause