@echo off
setlocal
cd /d "%~dp0"
if not defined ENV_FOLDER set "ENV_FOLDER=.venv"
if not exist "%ENV_FOLDER%\Scripts\python.exe" (
    python -m venv "%ENV_FOLDER%"
    if errorlevel 1 exit /b 1
)
set "PYTHON=%ENV_FOLDER%\Scripts\python.exe"
"%PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 exit /b 1
"%PYTHON%" manage.py check
if errorlevel 1 exit /b 1
"%PYTHON%" manage.py migrate
if errorlevel 1 exit /b 1
set "ADDRESS=%~1"
if not defined ADDRESS set "ADDRESS=127.0.0.1:8000"
"%PYTHON%" manage.py runserver %ADDRESS%
