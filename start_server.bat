@echo off
chcp 65001 >nul
echo ========================================
echo 标准搜索服务器启动脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查依赖...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo 安装FastAPI...
    pip install fastapi uvicorn
)

pip show playwright >nul 2>&1
if errorlevel 1 (
    echo 安装Playwright...
    pip install playwright
    playwright install chromium
)

echo.
echo ✅ 依赖检查完成
echo.

REM 启动服务器
echo 启动标准搜索服务器...
echo 服务器地址：http://localhost:8000
echo 按 Ctrl+C 停止服务器
echo.
python standard_search_server.py

pause
