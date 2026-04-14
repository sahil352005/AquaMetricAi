REM AquaMetric AI - Installation Script for Windows
REM This script automates the setup process

@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo 🚀 AquaMetric AI - Installation Script
echo ==========================================
echo.

REM Check Python version
echo [1/5] Checking Python version...
python --version
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
    echo Virtual environment created
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.

REM Create .env file
echo [5/5] Setting up configuration...
if exist .env (
    echo Environment file already exists
) else (
    copy .env.example .env
    echo Environment file created - update with your API key
)
echo.

echo ✅ Installation complete!
echo.
echo Next steps:
echo 1. Edit .env and add your OPENAI_API_KEY
echo 2. Run validation: python quickstart.py
echo 3. Start application: python app.py
echo 4. Open browser: http://localhost:5000
echo.

pause
