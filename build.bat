@echo off
echo Building Sinhala TTS Application...
echo ====================================

REM Check if virtual environment exists
if not exist "env\Scripts\activate.bat" (
    echo Virtual environment not found! Please ensure env folder exists.
    pause
    exit /b 1
)

REM Activate virtual environment
call env\Scripts\activate.bat

REM Install PyInstaller if not already installed
echo Installing PyInstaller...
pip install pyinstaller

REM Clean previous builds
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build

REM Build the executable
echo Building executable...
pyinstaller sinhala_tts.spec

REM Check if build was successful
if exist "dist\SinhalaTTS.exe" (
    echo.
    echo ====================================
    echo Build completed successfully!
    echo Executable location: dist\SinhalaTTS.exe
    echo ====================================
    echo.
    
    REM Copy additional files to dist folder
    if exist "README.md" copy "README.md" "dist\"
    if exist "LICENSE" copy "LICENSE" "dist\"
    
    echo Ready to create installer!
) else (
    echo.
    echo ====================================
    echo Build failed! Please check the errors above.
    echo ====================================
)

pause 