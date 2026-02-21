@echo off
echo ========================================
echo Virtual Air Drums - Setup Script
echo ========================================
echo.

echo Step 1: Installing Python packages...
echo.
python -m pip install --upgrade pip
python -m pip install opencv-python mediapipe pygame numpy scipy

echo.
echo Step 2: Generating drum sounds...
echo.
python setup_sounds.py

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the application, use:
echo   run_drums.bat
echo.
echo Or manually run:
echo   python air_drums.py
echo.
pause
