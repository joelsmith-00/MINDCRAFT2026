@echo off
title LUMI Wake Word Listener
cd /d "%~dp0"
echo Starting LUMI Wake Word Listener...
echo Say "Hey Lumi" to activate!
echo.
".\venv\Scripts\python.exe" lumi_listener.py
pause
