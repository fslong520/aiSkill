@echo off
REM News Skills 调度器启动脚本

cd /d "%~dp0"
echo ============================================
echo News Skills 定时调度器
echo ============================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)

REM 检查 schedule 库是否安装
python -c "import schedule" >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装 schedule 库...
    pip install schedule -q
)

REM 启动调度器
echo [启动] 调度器启动中...
echo.
python scheduler.py

pause
