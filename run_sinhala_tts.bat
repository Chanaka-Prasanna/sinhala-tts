@echo off
echo Starting Sinhala TTS Application...
python sinhala_tts_app.py
if errorlevel 1 (
    echo.
    echo Error: Failed to start the application.
    echo Make sure Python is installed and run setup.py first.
    pause
) 