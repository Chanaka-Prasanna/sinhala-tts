@echo off
title Sinhala TTS - Quick Start Guide
color 0E

echo.
echo ========================================
echo      Sinhala TTS - Quick Start Guide
echo ========================================
echo.
echo This script will help you create a Windows installer
echo for your Sinhala Text-to-Speech application.
echo.

:menu
echo What would you like to do?
echo.
echo 1. Check prerequisites
echo 2. Build executable only
echo 3. Create complete installer (recommended)
echo 4. View installation guide
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto :check_prereq
if "%choice%"=="2" goto :build_exe
if "%choice%"=="3" goto :build_installer
if "%choice%"=="4" goto :view_guide
if "%choice%"=="5" goto :exit
goto :menu

:check_prereq
cls
echo ========================================
echo         Prerequisites Check
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.7+ first.
) else (
    python --version
    echo ✓ Python is installed
)
echo.

echo Checking virtual environment...
if exist "env\Scripts\activate.bat" (
    echo ✓ Virtual environment found
) else (
    echo ❌ Virtual environment not found at env\Scripts\activate.bat
)
echo.

echo Checking required files...
if exist "enhanced_sinhala_tts.py" (
    echo ✓ Main application file found
) else (
    echo ❌ enhanced_sinhala_tts.py not found
)

if exist "sinhala_text_to_phoneme.py" (
    echo ✓ Phoneme converter found
) else (
    echo ❌ sinhala_text_to_phoneme.py not found
)

if exist "phonemes" (
    echo ✓ Phonemes directory found
) else (
    echo ❌ phonemes directory not found
)
echo.

echo Checking Inno Setup installation...
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo ✓ Inno Setup 6 found (x86)
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    echo ✓ Inno Setup 6 found (x64)
) else if exist "C:\Program Files (x86)\Inno Setup 5\ISCC.exe" (
    echo ✓ Inno Setup 5 found (x86)
) else if exist "C:\Program Files\Inno Setup 5\ISCC.exe" (
    echo ✓ Inno Setup 5 found (x64)
) else (
    echo ❌ Inno Setup not found
    echo    Download from: https://jrsoftware.org/isdl.php
)
echo.

echo Prerequisites check complete!
echo.
pause
goto :menu

:build_exe
cls
echo ========================================
echo       Building Executable Only
echo ========================================
echo.
echo This will create SinhalaTTS.exe in the dist\ folder
echo without creating an installer.
echo.
set /p confirm="Continue? (y/n): "
if /i not "%confirm%"=="y" goto :menu

call build.bat
pause
goto :menu

:build_installer
cls
echo ========================================
echo      Creating Complete Installer
echo ========================================
echo.
echo This will:
echo - Build the executable
echo - Create a Windows installer
echo - Include all dependencies and files
echo.
echo Make sure you have:
echo - Inno Setup installed
echo - All phoneme files in phonemes\ folder
echo - Valid Python environment
echo.
set /p confirm="Continue? (y/n): "
if /i not "%confirm%"=="y" goto :menu

call create_installer.bat
pause
goto :menu

:view_guide
cls
echo ========================================
echo         Installation Guide
echo ========================================
echo.
echo Opening the installation guide...
if exist "INSTALLATION_GUIDE.md" (
    start notepad "INSTALLATION_GUIDE.md"
) else (
    echo INSTALLATION_GUIDE.md not found!
    echo Please ensure all files are in the correct location.
)
echo.
pause
goto :menu

:exit
echo.
echo Thank you for using Sinhala TTS installer builder!
echo.
echo Quick reminders:
echo - Test your installer on a clean Windows system
echo - Include all necessary phoneme files
echo - Consider code signing for professional distribution
echo.
pause
exit /b 0 