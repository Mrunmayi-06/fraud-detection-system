@echo off
echo Starting GenAI Fraud Detection API...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if Ollama is running
echo Checking Ollama status...
curl -s http://localhost:11434/api/tags >nul 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: Ollama is not running!
    echo Please start Ollama in another terminal: ollama serve
    echo.
    pause
    exit /b 1
)

echo Ollama is running!
echo.
echo Starting Flask API on http://localhost:5000
echo Press CTRL+C to stop
echo.

python app.py
pause