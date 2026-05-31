@echo off
echo ========================================
echo GenAI Fraud Detection System - Setup
echo ========================================
echo.

REM Create project structure
echo Creating project structure...
mkdir modules 2>nul
mkdir data 2>nul
mkdir tests 2>nul
mkdir frontend 2>nul
mkdir logs 2>nul

echo Done!
echo.

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install --upgrade pip
pip install flask flask-cors requests pandas numpy scikit-learn

echo.
echo Checking Ollama installation...
where ollama >nul 2>nul
if errorlevel 1 (
    echo ERROR: Ollama is not installed!
    echo Please install Ollama from: https://ollama.com/download
    pause
    exit /b 1
) else (
    echo Ollama is installed!
)

echo.
echo Pulling LLaMA 2 model (this may take a while)...
ollama pull llama2

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start Ollama: ollama serve
echo 2. Start API: run_api.bat
echo 3. Open frontend: frontend\index.html
echo.
pause