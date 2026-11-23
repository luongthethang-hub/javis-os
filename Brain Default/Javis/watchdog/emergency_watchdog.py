import os
import sys
import time
import json
import psutil
import subprocess
import urllib.request
import urllib.parse
import urllib.error

# Cấu hình Cầu chì khẩn cấp (Out-of-band Watchdog)
BOT_TOKEN = "9215605178:AAFoOXqjWA3eVLc_PNUR2F2iH1ftoul-JIk" # Dùng chung bot token hoặc bot chuyên trách
ALLOWED_USERS = [1894254685]  # Telegram user_id của Thắng Lee
ALLOWED_GROUPS = [-1004479278576] # Thắng Lee Group

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"
OFFSET_FILE = r"C:\Users\Admin\JavisOS\brains\Brain Default\Javis\watchdog\offset.txt"

def tg_post(method, payload):
    url = f"{API_BASE}/{method}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[Watchdog TG Error] {e}", file=sys.stderr)
        return None

def send_msg(chat_id, text):
    return tg_post("sendMessage", {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})

def get_sys_status():
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=0.5)
    
    ai_procs = []
    for p in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            name = p.info['name'].lower()
            if any(k in name for k in ['antigravity', 'python', 'node']):
                mem_mb = p.info['memory_info'].rss / (1024 * 1024)
                if mem_mb > 50:
                    ai_procs.append((p.info['name'], p.info['pid'], mem_mb))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
            
    ai_procs.sort(key=lambda x: x[2], reverse=True)
    top_str = "\n".join([f"- `{p[0]}` (PID {p[1]}): *{p[2]:.1f} MB*" for p in ai_procs[:5]])
    
    msg = (
        f"📊 *TRẠNG THÁI HỆ THỐNG HIỆN TẠI*\n"
        f"- CPU: *{cpu}%*\n"
        f"- RAM: *{mem.percent}%* (Trống: *{mem.available / (1024**3):.2f} GB*)\n"
        f"\n*Top tiến trình AI/Server chiếm RAM:*\n{top_str if top_str else '- Không có tiến trình lớn'}"
    )
    return msg

def emergency_stop():
    """Phanh khẩn cấp cấp độ 1: Giết toàn bộ sub-process CLI/Node/Worker treo, GIỮ LẠI Javis Server."""
    killed = []
    freed_mb = 0
    # Tìm tiến trình server chính cổng 7777 để chừa ra
    server_pid = None
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == 7777 and conn.status == 'LISTEN':
            server_pid = conn.pid
            break

    my_pid = os.getpid()

    for p in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            pid = p.info['pid']
            if pid in (server_pid, my_pid):
                continue
            name = p.info['name'].lower()
            # Chém Antigravity CLI, node_repl, python con sinh ra subtask
            if any(k in name for k in ['antigravity', 'node_repl']):
                rss = p.info['memory_info'].rss / (1024 * 1024)
                p.kill()
                killed.append(f"{p.info['name']} ({pid})")
                freed_mb += rss
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return f"⏹ *ĐÃ PHANH KHẨN CẤP (STOP)*\n- Đã tiêu diệt: *{len(killed)}* tiến trình treo ({', '.join(killed) if killed else 'Không có'})\n- Giải phóng xấp xỉ: *{freed_mb:.1f} MB* RAM.\n- Javis Core Server vẫn giữ kết nối an toàn."

def emergency_reset():
    """Phanh khẩn cấp & Tái khởi động cấp độ 2: Dọn sạch mọi thứ và khởi động lại Javis Core."""
    # 1. Chém sạch CLI treo
    for p in psutil.process_iter(['pid', 'name']):
        try:
            name = p.info['name'].lower()
            if any(k in name for k in ['antigravity', 'node_repl']):
                p.kill()
        except:
            pass

    # 2. Tìm server 7777 và kill
    server_killed = False
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == 7777 and conn.status == 'LISTEN':
            try:
                psutil.Process(conn.pid).kill()
                server_killed = True
            except:
                pass

    time.sleep(1)
    
    # 3. Kích hoạt server lại
    server_script = r"C:\Users\Admin\JavisOS\run_javis.bat"
    if os.path.exists(server_script):
        subprocess.Popen(["cmd.exe", "/c", server_script], cwd=r"C:\Users\Admin\JavisOS", creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        py_exe = sys.executable
        subprocess.Popen([py_exe, "server/main.py"], cwd=r"C:\Users\Admin\JavisOS", creationflags=subprocess.CREATE_NEW_CONSOLE)

    return "🔄 *ĐÃ HARD RESET TOÀN BỘ HỆ THỐNG*\n- Đã triệt tiêu toàn bộ tiến trình CLI treo và vòng lặp lỗi.\n- Đã khởi động lại Javis Core Server trên cổng 7777.\n- Hệ thống sẵn sàng nhận lệnh mới sau 3-5 giây."

def main():
    print("[Watchdog] Emergency Remote Service bắt đầu chạy...", flush=True)
    offset = 0
    if os.path.exists(OFFSET_FILE):
        try:
            with open(OFFSET_FILE, "r") as f:
                offset = int(f.read().strip())
        except:
            offset = 0

    while True:
        try:
            payload = {"timeout": 20, "allowed_updates": ["message"]}
            if offset > 0:
                payload["offset"] = offset

            resp = tg_post("getUpdates", payload)
            if not resp or not resp.get("ok"):
                time.sleep(2)
                continue

            for update in resp.get("result", []):
                uid = update.get("update_id", 0)
                if uid >= offset:
                    offset = uid + 1
                    with open(OFFSET_FILE, "w") as f:
                        f.write(str(offset))

                msg = update.get("message") or {}
                chat = msg.get("chat") or {}
                chat_id = chat.get("id")
                from_user = msg.get("from") or {}
                user_id = from_user.get("id")
                text = (msg.get("text") or "").strip()

                # Xác thực danh tính Layer 0: Chỉ Thắng Lee hoặc đúng nhóm của Sếp
                if user_id not in ALLOWED_USERS and chat_id not in ALLOWED_GROUPS:
                    continue

                cmd = text.lower().split("@")[0].strip()

                if cmd in ("/panic", "/emergency_stop", "/phanh"):
                    reply = emergency_stop()
                    send_msg(chat_id, reply)
                elif cmd in ("/hard_reset", "/reboot_all", "/reset_all"):
                    reply = emergency_reset()
                    send_msg(chat_id, reply)
                elif cmd in ("/stat", "/sysinfo", "/ram"):
                    reply = get_sys_status()
                    send_msg(chat_id, reply)

            time.sleep(0.5)
        except Exception as e:
            print(f"[Watchdog Loop Exception] {e}", file=sys.stderr)
            time.sleep(2)

if __name__ == "__main__":
    main()
