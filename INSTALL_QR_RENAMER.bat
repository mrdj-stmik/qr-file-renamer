@echo off
title QR File Renamer v2025 - Installer
color 0A

echo ==========================================
echo    QR FILE RENAMER v2025 - INSTALLER
echo    mrdj 2025 for Team Wilkerstat 3206
echo ==========================================
echo.

:: Check if Python is installed
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo.
    echo Please install Python from: https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

python --version
echo Python found! ✓
echo.

:: Install required packages
echo [2/4] Installing required packages...
echo Installing opencv-python and numpy...
python -m pip install opencv-python numpy --quiet
if errorlevel 1 (
    echo WARNING: Package installation had issues, but continuing...
) else (
    echo Packages installed successfully! ✓
)
echo.

:: Create desktop shortcut
echo [3/4] Creating desktop shortcut...
set "desktop=%USERPROFILE%\Desktop"
set "shortcut=%desktop%\QR File Renamer v2025.lnk"

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%shortcut%'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = '\"%~dp0ws_rename_universal.py\"'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'QR File Renamer v2025 - mrdj for Team Wilkerstat 3206'; $Shortcut.Save()"

if exist "%shortcut%" (
    echo Desktop shortcut created! ✓
) else (
    echo WARNING: Could not create desktop shortcut
)
echo.

:: Test run
echo [4/4] Testing installation...
echo Testing QR File Renamer...
timeout /t 2 >nul
python -c "import cv2, numpy, tkinter; print('All modules imported successfully! ✓')" 2>nul
if errorlevel 1 (
    echo WARNING: Some modules may not be available
    echo The program will try to auto-install them when running
) else (
    echo Installation test passed! ✓
)
echo.

echo ==========================================
echo    INSTALLATION COMPLETE!
echo ==========================================
echo.
echo You can now run QR File Renamer by:
echo   1) Double-clicking the desktop shortcut
echo   2) Running: python ws_rename_universal.py
echo   3) Using the batch file: run_qr_renamer.bat
echo.
echo Features:
echo   ✓ Auto-install missing dependencies
echo   ✓ Enhanced QR detection (20 combinations)
echo   ✓ Professional GUI with live logging
echo   ✓ Batch processing of folders/subfolders
echo   ✓ Support for JPG, PNG, JPEG files
echo.
echo Created by mrdj 2025 for Team Wilkerstat 3206
echo ==========================================
echo.
pause

:: Ask if user wants to run now
echo.
set /p "run=Do you want to run QR File Renamer now? (Y/N): "
if /i "%run%"=="Y" (
    echo.
    echo Starting QR File Renamer...
    python ws_rename_universal.py
)