@echo off
title Javis Out-of-Band Emergency Watchdog
cd /d "C:\Users\Admin\JavisOS\brains\Brain Default\Javis\scripts"
echo ========================================================
echo  JAVIS OS - OUT-OF-BAND EMERGENCY WATCHDOG DAEMON
echo  Lang nghe Telegram Sep Thang (ID: 1894254685)
echo  Lenh ho tro: /status, /panic, /reset, /ping
echo ========================================================
:loop
python.exe emergency_watchdog.py
echo [WARNING] Watchdog da thoat. Khoi dong lai sau 3 giay...
timeout /t 3 >nul
goto loop
