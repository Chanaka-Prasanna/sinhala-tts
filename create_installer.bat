@echo off
title Sinhala TTS Installer Builder
color 0A

echo.
echo ==========================================
echo   Sinhala TTS - Complete Installer Build
echo ==========================================
echo.

REM Check for required files
echo [1/7] Checking required files...

if not exist "enhanced_sinhala_tts.py" (
    echo ERROR: enhanced_sinhala_tts.py not found!
    goto :error
)

if not exist "sinhala_text_to_phoneme.py" (
    echo ERROR: sinhala_text_to_phoneme.py not found!
    goto :error
)

if not exist "phonemes" (
    echo ERROR: phonemes directory not found!
    echo Please ensure phoneme audio files are in the phonemes folder.
    goto :error
)

echo ✓ All required files found.

REM Check virtual environment
echo.
echo [2/7] Setting up build environment...

if not exist "env\Scripts\activate.bat" (
    echo WARNING: Virtual environment not found!
    echo Using system Python installation...
    set "PYTHON_CMD=python"
) else (
    echo ✓ Virtual environment found, activating...
    call "env\Scripts\activate.bat"
    if errorlevel 1 (
        echo ERROR: Failed to activate virtual environment!
        goto :error
    )
    set "PYTHON_CMD=python"
    echo ✓ Virtual environment activated successfully.
)

REM Install PyInstaller
echo.
echo [3/7] Installing build dependencies...
echo Installing PyInstaller in virtual environment...
%PYTHON_CMD% -m pip install pyinstaller --upgrade
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller!
    echo Trying alternative installation method...
    pip install pyinstaller --upgrade
    if errorlevel 1 (
        echo ERROR: PyInstaller installation failed completely!
        goto :error
    )
)
echo ✓ PyInstaller installed successfully.

REM Clean previous builds
echo.
echo [4/7] Cleaning previous builds...
if exist "dist" (
    rmdir /s /q "dist"
    echo ✓ Cleaned dist directory
)
if exist "build" (
    rmdir /s /q "build"
    echo ✓ Cleaned build directory
)
if exist "installer_output" (
    rmdir /s /q "installer_output"
    echo ✓ Cleaned installer output directory
)

REM Create directory structure
mkdir "installer_output" 2>nul

REM Build executable
echo.
echo [5/7] Building executable...
echo This may take several minutes...

pyinstaller sinhala_tts.spec --noconfirm
if errorlevel 1 (
    echo ERROR: Failed to build executable!
    goto :error
)

if not exist "dist\SinhalaTTS.exe" (
    echo ERROR: Executable was not created successfully!
    goto :error
)

echo ✓ Executable built successfully!

REM Copy additional files
echo.
echo [6/7] Preparing installer files...

REM Copy phonemes if not already included
if not exist "dist\phonemes" (
    xcopy "phonemes" "dist\phonemes" /E /I /Q
    echo ✓ Copied phoneme files
)

REM Copy documentation
if exist "README.md" copy "README.md" "dist\" >nul
if exist "LICENSE.txt" copy "LICENSE.txt" "dist\" >nul

echo ✓ All files prepared for installer.

REM Check for Inno Setup
echo.
echo [7/7] Creating Windows installer...

REM Try common Inno Setup locations
set "INNO_SETUP="
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set "INNO_SETUP=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set "INNO_SETUP=C:\Program Files\Inno Setup 6\ISCC.exe"
) else if exist "C:\Program Files (x86)\Inno Setup 5\ISCC.exe" (
    set "INNO_SETUP=C:\Program Files (x86)\Inno Setup 5\ISCC.exe"
) else if exist "C:\Program Files\Inno Setup 5\ISCC.exe" (
    set "INNO_SETUP=C:\Program Files\Inno Setup 5\ISCC.exe"
)

if "%INNO_SETUP%"=="" (
    echo.
    echo WARNING: Inno Setup not found!
    echo Please install Inno Setup from: https://jrsoftware.org/isdl.php
    echo.
    echo After installing Inno Setup, you can create the installer manually by:
    echo 1. Opening installer.iss in Inno Setup
    echo 2. Clicking Build ^> Compile
    echo.
    echo Your executable is ready at: dist\SinhalaTTS.exe
    goto :success_no_installer
)

REM Create the installer
echo Using Inno Setup: %INNO_SETUP%
"%INNO_SETUP%" "installer.iss"
if errorlevel 1 (
    echo ERROR: Failed to create installer!
    goto :error
)

echo ✓ Installer created successfully!

REM Check if installer was created
if exist "installer_output\SinhalaTTS_Setup_v1.0.exe" (
    goto :success_with_installer
) else (
    echo WARNING: Installer file not found where expected.
    goto :success_no_installer
)

:success_with_installer
echo.
echo ==========================================
echo           BUILD COMPLETED SUCCESSFULLY!
echo ==========================================
echo.
echo Your installer is ready:
echo   Location: installer_output\SinhalaTTS_Setup_v1.0.exe
echo   Size: 
for %%I in ("installer_output\SinhalaTTS_Setup_v1.0.exe") do echo   %%~zI bytes
echo.
echo The installer includes:
echo   ✓ SinhalaTTS.exe (main application)
echo   ✓ All required dependencies
echo   ✓ Phoneme audio files
echo   ✓ Documentation files
echo   ✓ Uninstaller
echo.
echo You can now distribute this installer to others!
echo.
goto :end

:success_no_installer
echo.
echo ==========================================
echo         EXECUTABLE BUILD COMPLETED!
echo ==========================================
echo.
echo Your executable is ready:
echo   Location: dist\SinhalaTTS.exe
echo.
echo To create the installer:
echo   1. Install Inno Setup from: https://jrsoftware.org/isdl.php
echo   2. Run this script again
echo.
goto :end

:error
echo.
echo ==========================================
echo              BUILD FAILED!
echo ==========================================
echo.
echo Please check the error messages above and try again.
echo.
echo Common solutions:
echo   - Ensure Python is installed and in PATH
echo   - Check that all required files exist
echo   - Run as Administrator if needed
echo   - Install missing dependencies with pip
echo.
pause
exit /b 1

:end
echo Press any key to exit...
pause >nul
exit /b 0 