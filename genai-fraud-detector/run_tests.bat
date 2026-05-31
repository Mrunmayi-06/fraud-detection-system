@echo off
echo Running GenAI Fraud Detection Tests...
echo.

call venv\Scripts\activate.bat

python tests\test_cases.py

pause