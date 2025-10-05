@echo off
echo ==========================================
echo    Universal QR File Renamer v2.0
echo    mrdj 2025 for Team Wilkerstat 3206
echo ==========================================
echo.
echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from https://python.org
    pause
    exit /b 1
)
echo.
echo Starting Universal QR File Renamer...
echo This version will auto-install required dependencies.
echo.
python ws_rename_universal.py
echo.
echo Application closed.
pause