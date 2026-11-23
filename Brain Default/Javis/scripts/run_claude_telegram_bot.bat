@echo off
title Claude Telegram Bot Bridge
cd /d "C:\Users\Admin\JavisOS\brains\Brain Default\Javis\scripts"
:loop
python.exe claude_telegram_bot.py
echo [WARNING] Bot script exited. Restarting in 5 seconds...
timeout /t 5 >nul
goto loop
