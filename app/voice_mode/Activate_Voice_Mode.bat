@echo off
title LUMI Voice Interface
cd /d "%~dp0"
echo Starting LUMI in Voice Mode...
echo (Note: If GUI fails, it will continue in Terminal Voice Mode)
echo.
".\venv\Scripts\python.exe" main.py
pause
