@echo off
cd /d "%~dp0"
title QR File Renamer v2025 - Portable
color 0B

:menu
cls
echo ==========================================
echo       QR FILE RENAMER v2025 - PORTABLE
echo       mrdj 2025 for Team Wilkerstat 3206
echo ==========================================
echo.
echo Select version to run:
echo.
echo [1] Universal Version (Auto-install deps)
echo [2] Stable Version (Enhanced detection)
echo [3] Simple Version (Basic GUI)
echo [4] Debug Version (Troubleshooting)
echo [5] Test GUI (Check if working)
echo.
echo [I] Install/Setup Dependencies
echo [H] Help and Instructions
echo [Q] Quit
echo.
set /p "choice=Enter your choice: "

if /i "%choice%"=="1" goto universal
if /i "%choice%"=="2" goto stable
if /i "%choice%"=="3" goto simple
if /i "%choice%"=="4" goto debug
if /i "%choice%"=="5" goto test
if /i "%choice%"=="I" goto install
if /i "%choice%"=="H" goto help
if /i "%choice%"=="Q" goto quit
goto menu

:universal
echo.
echo Starting Universal QR File Renamer...
echo This version auto-installs required dependencies.
echo.
python ws_rename_universal.py
pause
goto menu

:stable
echo.
echo Starting Stable QR File Renamer...
echo Enhanced detection with 280 combinations.
echo.
python ws_rename_stable.py
if errorlevel 1 (
    echo.
    echo ERROR: Missing dependencies!
    echo Run option [I] to install dependencies first.
    pause
)
goto menu

:simple
echo.
echo Starting Simple QR File Renamer...
echo Basic GUI version.
echo.
python ws_rename_simple.py
if errorlevel 1 (
    echo.
    echo ERROR: Missing dependencies!
    echo Run option [I] to install dependencies first.
    pause
)
goto menu

:debug
echo.
echo Starting Debug QR File Renamer...
echo For troubleshooting QR detection issues.
echo.
python ws_rename_debug.py
if errorlevel 1 (
    echo.
    echo ERROR: Missing dependencies!
    echo Run option [I] to install dependencies first.
    pause
)
goto menu

:test
echo.
echo Testing GUI functionality...
python test_gui.py
pause
goto menu

:install
cls
echo ==========================================
echo       INSTALLING DEPENDENCIES
echo ==========================================
echo.
echo Installing opencv-python and numpy...
python -m pip install opencv-python numpy
echo.
echo Installation complete!
pause
goto menu

:help
cls
echo ==========================================
echo              HELP & INSTRUCTIONS
echo ==========================================
echo.
echo VERSIONS AVAILABLE:
echo.
echo 1. UNIVERSAL VERSION (Recommended)
echo    - Auto-installs dependencies
echo    - Works in any Python environment
echo    - Enhanced QR detection (20 combinations)
echo    - Professional GUI with live logging
echo.
echo 2. STABLE VERSION (Advanced)
echo    - Requires manual dependency installation
echo    - 280 detection combinations
echo    - Highest accuracy (~90%%)
echo    - Threading for responsive UI
echo.
echo 3. SIMPLE VERSION (Basic)
echo    - Simple interface
echo    - Basic QR detection
echo    - Lightweight
echo.
echo 4. DEBUG VERSION (Troubleshooting)
echo    - Detailed logging
echo    - Analysis tools
echo    - Problem diagnosis
echo.
echo REQUIREMENTS:
echo - Python 3.7 or higher
echo - opencv-python library
echo - numpy library
echo.
echo SUPPORTED FILES:
echo - JPG, JPEG, PNG images
echo - QR codes with 14-digit numbers
echo - Batch processing of folders/subfolders
echo.
echo OUTPUT FORMAT:
echo - [14digits]_2025.ext
echo - Example: 12345678901234_2025.jpg
echo.
echo Created by mrdj 2025 for Team Wilkerstat 3206
echo ==========================================
echo.
pause
goto menu

:quit
echo.
echo Thank you for using QR File Renamer v2025!
echo Created by mrdj 2025 for Team Wilkerstat 3206
echo.
exit /b 0