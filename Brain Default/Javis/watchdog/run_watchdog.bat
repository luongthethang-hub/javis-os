@echo off
title Javis Remote Watchdog & Kill Switch
cd /d "C:\Users\Admin\JavisOS"
"C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe" "C:\Users\Admin\JavisOS\brains\Brain Default\Javis\watchdog\emergency_watchdog.py"
pause
