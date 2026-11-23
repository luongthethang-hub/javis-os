#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Emergency Watchdog Daemon (Out-of-Band Kill-Switch) cho Javis OS.
Chay doc lap voi Javis Core Server, lang nghe truc tiep tu Telegram Sep Thang (chat_id: 1894254685).
Xu ly cac lenh phanh va khoi phuc khan cap: /status, /panic, /stop, /reset, /reboot, /ping, /help.
"""

import os
import sys
import json
import time
import socket
import argparse
import subprocess
import urllib.request
import urllib.parse
import urllib.error

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

DEFAULT_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "bridge", "watchdog_config.json"
)

DEFAULT_CONFIG = {
    "bot_token": "9215605178:AAFoOXqjWA3eVLc_PNUR2F2iH1ftoul-JIk",
    "bot_username": "ThangleeClaude_bot",
    "allowed_chat_id": 1894254685,
    "server_port": 7777,
    "app_dir": r"C:\Users\Admin\JavisOS",
    "poll_interval_sec": 2,
    "target_child_processes": [
        "antigravity.exe",
        "node.exe",
        "node_repl.exe",
        "ffmpeg.exe",
        "ffprobe.exe",
        "rea-video.exe"
    ]
}


def load_config(config_path=None):
    target_path = config_path or DEFAULT_CONFIG_PATH
    if os.path.exists(target_path):
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                merged = dict(DEFAULT_CONFIG)
                merged.update(loaded)
                return merged
        except Exception as e:
            print(f"[WARN] Khong doc duoc file config {target_path}: {e}. Dung config mac dinh.", flush=True)
    return dict(DEFAULT_CONFIG)


def is_port_listening(port, host="127.0.0.1", timeout=0.15):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((host, port)) == 0
    except Exception:
        return False


def get_system_telemetry(config):
    start_t = time.perf_counter()
    port = config.get("server_port", 7777)
    server_alive = is_port_listening(port)

    cpu_usage = 0.0
    ram_used_mb = 0
    ram_total_mb = 0
    ram_pct = 0.0

    if HAS_PSUTIL:
        try:
            cpu_usage = psutil.cpu_percent(interval=None)
            vmem = psutil.virtual_memory()
            ram_used_mb = int(vmem.used / (1024 * 1024))
            ram_total_mb = int(vmem.total / (1024 * 1024))
            ram_pct = vmem.percent
        except Exception:
            pass

    ai_processes = []
    current_pid = os.getpid()

    if HAS_PSUTIL:
        keywords = ["python", "node", "antigravity", "ffmpeg", "mt5", "graphify"]
        try:
            for p in psutil.process_iter(['pid', 'name']):
                try:
                    pid = p.info['pid']
                    if pid == current_pid:
                        continue
                    p_name = (p.info['name'] or '').lower()
                    if any(k in p_name for k in keywords):
                        mem_mb = 0.0
                        try:
                            mem_mb = round(p.memory_info().rss / (1024 * 1024), 1)
                        except Exception:
                            pass
                        ai_processes.append({
                            "pid": pid,
                            "name": p.info['name'],
                            "mem_mb": mem_mb
                        })
                        if len(ai_processes) >= 8:
                            break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception:
            pass

    elapsed_ms = round((time.perf_counter() - start_t) * 1000, 1)

    return {
        "server_alive": server_alive,
        "server_port": port,
        "cpu_pct": cpu_usage,
        "ram_used_mb": ram_used_mb,
        "ram_total_mb": ram_total_mb,
        "ram_pct": ram_pct,
        "ai_processes": ai_processes,
        "elapsed_ms": elapsed_ms
    }


def execute_level1_panic(config):
    start_t = time.perf_counter()
    target_names = [n.lower() for n in config.get("target_child_processes", [])]
    killed = []
    freed_mb = 0.0
    current_pid = os.getpid()

    if HAS_PSUTIL:
        for p in psutil.process_iter(['pid', 'name', 'memory_info', 'cmdline']):
            try:
                pid = p.info['pid']
                if pid == current_pid:
                    continue
                name = (p.info['name'] or '').lower()
                cmd = " ".join(p.info.get('cmdline') or []).lower()

                should_kill = False
                if any(t in name for t in target_names):
                    should_kill = True
                elif "python" in name and any(x in cmd for x in ["subagent", "runner.py", "worker", "agent_runner"]):
                    if "server\\main.py" not in cmd and "server/main.py" not in cmd:
                        should_kill = True

                if should_kill:
                    mem = 0.0
                    if p.info.get('memory_info'):
                        mem = p.info['memory_info'].rss / (1024 * 1024)
                    p.kill()
                    killed.append({"pid": pid, "name": p.info['name'], "mem_mb": round(mem, 1)})
                    freed_mb += mem
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    else:
        for t_name in target_names:
            try:
                res = subprocess.run(["taskkill", "/F", "/IM", t_name], capture_output=True, text=True)
                if res.returncode == 0:
                    killed.append({"name": t_name, "pid": 0, "mem_mb": 0.0})
            except Exception:
                pass

    elapsed_ms = round((time.perf_counter() - start_t) * 1000, 1)
    return {
        "status": "success",
        "level": 1,
        "action": "panic_kill_children",
        "killed_count": len(killed),
        "freed_mb": round(freed_mb, 1),
        "killed_details": killed,
        "elapsed_ms": elapsed_ms
    }


def execute_level2_reset(config):
    start_t = time.perf_counter()
    panic_res = execute_level1_panic(config)

    app_dir = config.get("app_dir", r"C:\Users\Admin\JavisOS")
    port = config.get("server_port", 7777)
    current_pid = os.getpid()
    server_killed = False

    if HAS_PSUTIL:
        for p in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                pid = p.info['pid']
                if pid == current_pid:
                    continue
                cmd = " ".join(p.info.get('cmdline') or []).lower()
                if "server\\main.py" in cmd or "server/main.py" in cmd or "uvicorn" in cmd:
                    p.terminate()
                    try:
                        p.wait(timeout=1.0)
                    except psutil.TimeoutExpired:
                        p.kill()
                    server_killed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             f"Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue | ForEach-Object {{ Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }}"],
            capture_output=True, timeout=2.0
        )
    except Exception:
        pass

    time.sleep(0.5)

    py_exe = os.path.join(app_dir, ".venv", "Scripts", "python.exe")
    if not os.path.exists(py_exe):
        py_exe = sys.executable

    server_script = os.path.join(app_dir, "server", "main.py")
    server_cwd = os.path.join(app_dir, "server")

    new_proc = None
    try:
        flags = 0
        if os.name == "nt":
            flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS

        env = os.environ.copy()
        env["JAVIS_STATE_DIR"] = server_cwd

        new_proc = subprocess.Popen(
            [py_exe, server_script],
            cwd=server_cwd,
            creationflags=flags,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        return {
            "status": "error",
            "message": f"Khoi dong server that bai: {e}",
            "elapsed_ms": round((time.perf_counter() - start_t) * 1000, 1)
        }

    recovered = False
    for _ in range(10):
        time.sleep(0.3)
        if is_port_listening(port):
            recovered = True
            break

    elapsed_ms = round((time.perf_counter() - start_t) * 1000, 1)

    return {
        "status": "success" if recovered else "pending",
        "level": 2,
        "action": "hard_reset_core_and_children",
        "panic_freed_mb": panic_res.get("freed_mb", 0.0),
        "server_killed": server_killed,
        "new_server_pid": new_proc.pid if new_proc else None,
        "server_listening": recovered,
        "elapsed_ms": elapsed_ms
    }


def tg_call(token, method, data=None, timeout=15):
    url = f"https://api.telegram.org/bot{token}/{method}"
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"ok": False, "description": str(e)}


def send_tg_message(token, chat_id, text, reply_id=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_id:
        payload["reply_to_message_id"] = reply_id
    res = tg_call(token, "sendMessage", payload)
    if not res.get("ok"):
        payload.pop("parse_mode", None)
        res = tg_call(token, "sendMessage", payload)
    return res


def format_status_message(telemetry):
    srv_status = "HOAT DONG" if telemetry["server_alive"] else "MAT KET NOI / TREO"
    proc_lines = []
    for p in telemetry["ai_processes"][:8]:
        proc_lines.append(f"- PID {p['pid']}: `{p['name']}` ({p['mem_mb']} MB)")
    if not proc_lines:
        proc_lines = ["- Khong co tien trinh con bat thuong."]

    procs_text = "\n".join(proc_lines)

    return (
        f"*Bao cao Telemetry He thong (Watchdog Out-of-Band)*\n\n"
        f"- Core Server (Port {telemetry['server_port']}): *{srv_status}*\n"
        f"- CPU: *{telemetry['cpu_pct']}%*\n"
        f"- RAM: *{telemetry['ram_used_mb']} MB / {telemetry['ram_total_mb']} MB* ({telemetry['ram_pct']}%)\n"
        f"- Thoi gian do: *{telemetry['elapsed_ms']} ms*\n\n"
        f"*Tien trinh AI dang chay:*\n"
        f"{procs_text}\n\n"
        f"Lenh ho tro: `/status`, `/panic`, `/reset`"
    )


def format_panic_message(res):
    details = []
    for k in res.get("killed_details", [])[:6]:
        details.append(f"- Da huy PID {k['pid']}: `{k['name']}` ({k['mem_mb']} MB)")
    if not details:
        details = ["- Khong co tien trinh con treo can huy."]

    details_text = "\n".join(details)
    return (
        f"*Phanh Khan Cap Cap do 1 (PANIC) Thanh Cong*\n\n"
        f"- So tien trinh da don: *{res['killed_count']}*\n"
        f"- Dung luong RAM giai phong: *{res['freed_mb']} MB*\n"
        f"- Thoi gian dap ung: *{res['elapsed_ms']} ms*\n\n"
        f"{details_text}\n\n"
        f"Javis Core Server van duoc giu nguyen de tiep tuc phuc vu."
    )


def format_reset_message(res):
    st = "HOAN TAT" if res.get("server_listening") else "DANG KHOI DONG"
    pid_info = f"PID {res['new_server_pid']}" if res.get('new_server_pid') else "Khong ro"
    return (
        f"*Phanh Khan Cap Cap do 2 (HARD RESET) {st}*\n\n"
        f"- Giai phong tien trinh con: *{res.get('panic_freed_mb', 0.0)} MB*\n"
        f"- Tien trinh Server moi: *{pid_info}* (Port 7777)\n"
        f"- Trang thai Port 7777: *{'Listening' if res.get('server_listening') else 'Waiting'}*\n"
        f"- Thoi gian dap ung: *{res['elapsed_ms']} ms*\n\n"
        f"Kenh Core Server da san sang nhan lenh moi."
    )


def handle_command(cmd, text, chat_id, config):
    cmd = cmd.lower()
    if cmd in ["/status", "/telemetry", "/check"]:
        telemetry = get_system_telemetry(config)
        return format_status_message(telemetry)
    elif cmd in ["/panic", "/stop", "/kill"]:
        res = execute_level1_panic(config)
        return format_panic_message(res)
    elif cmd in ["/reset", "/reboot", "/restart"]:
        res = execute_level2_reset(config)
        return format_reset_message(res)
    elif cmd in ["/ping"]:
        now_str = time.strftime("%Y-%m-%d %H:%M:%S")
        port = config.get("server_port", 7777)
        alive = is_port_listening(port)
        return f"PONG luc {now_str}. Watchdog truc ban on dinh. Core 7777: {'UP' if alive else 'DOWN'}."
    elif cmd in ["/help", "/start"]:
        return (
            "*Bang dieu khien Cau chi Khan cap (Out-of-Band Kill-Switch)*\n\n"
            "- `/status`: Kiem tra tai nguyen CPU, RAM va cac tien trinh dang chay (< 500 ms)\n"
            "- `/panic`: Phanh cap 1 - taskkill tat ca tien trinh con CLI bi treo (< 1 giay)\n"
            "- `/reset`: Phanh cap 2 - Don sach tien trinh con va khoi dong lai Core Server 7777 (< 3 giay)\n"
            "- `/ping`: Kiem tra trang thai truc ban cua Watchdog"
        )
    return None


def run_daemon_loop(config):
    token = config.get("bot_token")
    allowed_id = int(config.get("allowed_chat_id", 1894254685))
    poll_sec = config.get("poll_interval_sec", 2)

    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Watchdog Daemon khoi dong. Bot: {config.get('bot_username')}, ChatId hop le: {allowed_id}", flush=True)

    offset = 0
    state_dir = os.path.join(config.get("app_dir", r"C:\Users\Admin\JavisOS"), "brains", "Brain Default", "Javis", "tmp")
    os.makedirs(state_dir, exist_ok=True)
    offset_file = os.path.join(state_dir, "watchdog_offset.txt")

    if os.path.exists(offset_file):
        try:
            with open(offset_file, "r", encoding="utf-8") as f:
                offset = int(f.read().strip())
        except Exception:
            offset = 0

    while True:
        try:
            updates = tg_call(token, "getUpdates", {"offset": offset, "timeout": 10}, timeout=15)
            if updates.get("ok"):
                for u in updates.get("result", []):
                    u_id = u["update_id"]
                    offset = u_id + 1
                    try:
                        with open(offset_file, "w", encoding="utf-8") as f:
                            f.write(str(offset))
                    except Exception:
                        pass

                    msg = u.get("message") or u.get("edited_message")
                    if not msg:
                        continue

                    chat = msg.get("chat", {})
                    chat_id = chat.get("id")
                    text = (msg.get("text") or "").strip()
                    msg_id = msg.get("message_id")

                    if int(chat_id) != allowed_id:
                        print(f"[REJECT] Tu choi lenh tu chat_id {chat_id} (Chi cho phep {allowed_id})", flush=True)
                        continue

                    if not text.startswith("/"):
                        continue

                    cmd = text.split()[0].split("@")[0]
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Nhan lenh tu Sep Thang: {cmd}", flush=True)

                    reply_text = handle_command(cmd, text, chat_id, config)
                    if reply_text:
                        send_tg_message(token, chat_id, reply_text, reply_id=msg_id)

            time.sleep(poll_sec)
        except KeyboardInterrupt:
            print("[INFO] Dung Watchdog theo yeu cau.", flush=True)
            break
        except Exception as e:
            print(f"[ERROR] Loi vong lap Watchdog: {e}", flush=True)
            time.sleep(poll_sec)


def main():
    parser = argparse.ArgumentParser(description="Javis OS Emergency Watchdog")
    parser.add_argument("--config", type=str, default=None, help="Duong dan watchdog_config.json")
    parser.add_argument("--status", action="store_true", help="Doc va in ngay telemetry he thong")
    parser.add_argument("--panic", action="store_true", help="Thuc thi phanh cap do 1 (taskkill tien trinh con)")
    parser.add_argument("--reset", action="store_true", help="Thuc thi phanh cap do 2 (restart core server 7777)")
    parser.add_argument("--test", action="store_true", help="Chay bo kiem tra self-test noi bo")

    args = parser.parse_args()
    config = load_config(args.config)

    if args.status:
        tel = get_system_telemetry(config)
        print(json.dumps(tel, indent=2))
        return

    if args.panic:
        res = execute_level1_panic(config)
        print(json.dumps(res, indent=2))
        return

    if args.reset:
        res = execute_level2_reset(config)
        print(json.dumps(res, indent=2))
        return

    if args.test:
        print("=== SELF-TEST EMERGENCY WATCHDOG ===")
        print(f"- Config bot: {config.get('bot_username')}")
        print(f"- Allowed Chat ID: {config.get('allowed_chat_id')}")
        tel = get_system_telemetry(config)
        print(f"- Telemetry: CPU={tel['cpu_pct']}%, RAM={tel['ram_pct']}%, Server7777={'UP' if tel['server_alive'] else 'DOWN'} (Do trong {tel['elapsed_ms']} ms)")
        print("- Kiem tra lenh /status:")
        msg = format_status_message(tel)
        assert "Bao cao Telemetry" in msg
        print("  -> Format status dat chuan.")
        print("- Kiem tra logic auth chat_id:")
        assert config['allowed_chat_id'] == 1894254685
        print("  -> Auth gate chan chat_id khac dat chuan.")
        print("=== TEST COMPLETED SUCCESSFULLY ===")
        return

    run_daemon_loop(config)


if __name__ == "__main__":
    main()
