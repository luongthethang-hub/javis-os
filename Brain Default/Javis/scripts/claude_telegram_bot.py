import os
import sys
import json
import time
import subprocess
import threading
import urllib.request
import urllib.parse
import urllib.error

CONFIG_PATH = r"C:\Users\Admin\JavisOS\brains\Brain Default\Javis\bridge\claude_bot_config.json"
LAUNCHER_SCRIPT = r"C:\Users\Admin\JavisOS\brains\Brain Default\Javis\scripts\handoff_desktop_launcher.ps1"
RESULT_FILE = r"C:\Users\Admin\JavisOS\brains\Brain Default\Javis\scripts\handoff-claude-last.txt"
TMP_DIR = r"C:\Users\Admin\JavisOS\brains\Brain Default\Javis\tmp"
OFFSET_FILE = os.path.join(TMP_DIR, "claude_bot_offset.txt")

os.makedirs(TMP_DIR, exist_ok=True)

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

BOT_TOKEN = config["bot_token"]
BOT_USERNAME = config.get("bot_username", "ThangleeClaude_bot").lower()
WAIT_SECONDS = config.get("wait_seconds", 240)
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

handoff_lock = threading.Lock()

def tg_request(endpoint, data=None, timeout=30):
    url = f"{API_BASE}/{endpoint}"
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"[HTTPError] {endpoint}: {e.code} - {err_msg}", flush=True)
        try:
            return json.loads(err_msg)
        except Exception:
            return {"ok": False, "description": err_msg}
    except Exception as e:
        print(f"[RequestError] {endpoint}: {e}", flush=True)
        return {"ok": False, "description": str(e)}

def send_chat_action(chat_id, action="typing"):
    return tg_request("sendChatAction", {"chat_id": chat_id, "action": action}, timeout=10)

def send_message(chat_id, text, reply_to_message_id=None):
    max_len = 4000
    chunks = [text[i:i+max_len] for i in range(0, len(text), max_len)]
    if not chunks:
        chunks = ["(Phản hồi rỗng từ Claude)"]

    for chunk in chunks:
        payload = {
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": "Markdown"
        }
        if reply_to_message_id:
            payload["reply_to_message_id"] = reply_to_message_id

        res = tg_request("sendMessage", payload, timeout=20)
        if not res.get("ok"):
            payload.pop("parse_mode", None)
            res = tg_request("sendMessage", payload, timeout=20)
        time.sleep(0.3)

def load_offset():
    if os.path.exists(OFFSET_FILE):
        try:
            with open(OFFSET_FILE, "r", encoding="utf-8") as f:
                return int(f.read().strip())
        except Exception:
            pass
    return 0

def save_offset(offset):
    try:
        with open(OFFSET_FILE, "w", encoding="utf-8") as f:
            f.write(str(offset))
    except Exception as e:
        print(f"Error saving offset: {e}", flush=True)

class TypingKeeper:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self.running = False

    def _run(self):
        while self.running:
            send_chat_action(self.chat_id, "typing")
            for _ in range(40):
                if not self.running:
                    break
                time.sleep(0.1)

def run_claude_handoff(prompt_text):
    prompt_file = os.path.join(TMP_DIR, f"claude_prompt_{int(time.time()*1000)}.txt")
    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(prompt_text)

    cmd = [
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-File", LAUNCHER_SCRIPT,
        "-App", "claude",
        "-PromptFile", prompt_file,
        "-WaitSeconds", str(WAIT_SECONDS)
    ]

    print(f"[Claude] Running handoff launcher for: {prompt_text[:60]}...", flush=True)
    start_t = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=WAIT_SECONDS + 90)
        print(f"[Claude] Launcher finished with code {proc.returncode} in {time.time()-start_t:.1f}s", flush=True)
    except subprocess.TimeoutExpired:
        print("[Claude] Handoff timeout expired!", flush=True)
        return "Lỗi: Quá thời gian phản hồi từ ứng dụng Claude Desktop (Timeout)."
    except Exception as e:
        print(f"[Claude] Subprocess error: {e}", flush=True)
        return f"Lỗi thực thi handoff: {e}"
    finally:
        if os.path.exists(prompt_file):
            try:
                os.remove(prompt_file)
            except Exception:
                pass

    if os.path.exists(RESULT_FILE):
        try:
            with open(RESULT_FILE, "r", encoding="utf-8") as f:
                res_content = f.read().strip()
            if res_content:
                return res_content
        except Exception as e:
            print(f"Error reading result file: {e}", flush=True)

    return "Không nhận được phản hồi từ Claude Desktop hoặc cửa sổ chưa sẵn sàng."

def handle_message(msg):
    chat = msg.get("chat", {})
    chat_id = chat.get("id")
    chat_type = chat.get("type", "private")
    text = msg.get("text", "").strip()
    msg_id = msg.get("message_id")
    from_user = msg.get("from", {})
    first_name = from_user.get("first_name", "User")

    if not text:
        return

    should_process = False
    clean_text = text

    if chat_type == "private":
        should_process = True
        if text.startswith("/start") or text.startswith("/help"):
            welcome = (
                f"Xin chào {first_name}! Tôi là **Claude** trong Liên minh AI của Thắng Lee.\n\n"
                "- Nhận lệnh trực tiếp từ bạn qua chat này.\n"
                "- Tự động đồng bộ với Second Brain của Javis.\n"
                "- Bạn có thể đặt câu hỏi hoặc giao việc kỹ thuật/phản biện tại đây."
            )
            send_message(chat_id, welcome, reply_to_message_id=msg_id)
            return
    else:
        tag_pattern = f"@{BOT_USERNAME}"
        reply_to = msg.get("reply_to_message", {})
        reply_from = reply_to.get("from", {})
        is_reply_to_bot = reply_from.get("username", "").lower() == BOT_USERNAME

        if tag_pattern in text.lower():
            should_process = True
            for part in text.split():
                if part.lower() == tag_pattern:
                    clean_text = clean_text.replace(part, "").strip()
        elif is_reply_to_bot:
            should_process = True
        elif text.startswith("/claude ") or text.startswith("/askclaude "):
            should_process = True
            clean_text = text.split(" ", 1)[1].strip()

    if not should_process or not clean_text:
        return

    print(f"\n[Telegram] Nhận tin nhắn từ {first_name} (chat {chat_id}): {clean_text[:80]}", flush=True)

    if not handoff_lock.acquire(blocking=False):
        send_message(chat_id, "Claude đang xử lý một tác vụ trước đó trên máy. Yêu cầu của bạn tạm thời chưa thể thực thi đồng thời, vui lòng đợi ít phút.", reply_to_message_id=msg_id)
        return

    keeper = TypingKeeper(chat_id)
    keeper.start()
    try:
        final_prompt = f"Yêu cầu từ {first_name} qua Telegram:\n{clean_text}\n\nHướng dẫn: Trả lời trực tiếp, chính xác, súc tích, giữ nguyên thuật ngữ kỹ thuật, định dạng Markdown rõ ràng, không dùng em dash."
        result = run_claude_handoff(final_prompt)
        send_message(chat_id, result, reply_to_message_id=msg_id)
    finally:
        keeper.stop()
        handoff_lock.release()

def main():
    print(f"=== CLAUDE TELEGRAM BOT BRIDGE STARTED (@{BOT_USERNAME}) ===", flush=True)
    offset = load_offset()
    print(f"Loaded offset: {offset}", flush=True)

    while True:
        try:
            updates = tg_request("getUpdates", {"offset": offset, "timeout": 20}, timeout=35)
            if updates.get("ok"):
                for u in updates.get("result", []):
                    u_id = u["update_id"]
                    offset = u_id + 1
                    save_offset(offset)
                    if "message" in u:
                        handle_message(u["message"])
            else:
                print(f"[getUpdates error]: {updates}", flush=True)
                time.sleep(3)
        except Exception as e:
            print(f"[Main loop exception]: {e}", flush=True)
            time.sleep(2)

if __name__ == "__main__":
    main()
