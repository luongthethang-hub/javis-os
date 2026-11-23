import time
import subprocess
import os
import sys

SCRIPT_PATH = r"C:\Users\Admin\JavisOS\brains\Brain Default\Javis\scripts\alliance_bot_daemon.py"
PYTHON_EXE = sys.executable

def start_daemon():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Launching Alliance Bot Daemon...", flush=True)
    return subprocess.Popen([PYTHON_EXE, SCRIPT_PATH])

def main():
    print("=== ALLIANCE BOT WATCHDOG ACTIVATED ===", flush=True)
    proc = start_daemon()

    while True:
        time.sleep(5)
        ret = proc.poll()
        if ret is not None:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Alliance Bot Daemon exited with code {ret}. Auto-restarting in 2s...", flush=True)
            time.sleep(2)
            proc = start_daemon()

if __name__ == "__main__":
    main()
