# -*- coding: utf-8 -*-
"""
Dola AI Telegram Bot Runner (Độc lập)
Định vị: COO & Chief Engagement Officer (Tác chiến & Trải nghiệm)
Kênh: @DolaAI_ThangLee_bot (Token 9160223359:AAGpgjOFB2R3ZPWq_Or-YrRm6MbEkIxJ3Co)
"""
import os
import sys
import json
import time
import urllib.request
import urllib.parse
import urllib.error

BOT_TOKEN = "9160223359:AAGpgjOFB2R3ZPWq_Or-YrRm6MbEkIxJ3Co"
ALLOWED_USERS = [1894254685]
ALLOWED_GROUPS = [-1004479278576]
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"
A2A_DIR = r"C:\Users\Admin\JavisOS\brains\Brain Default\memory\a2a_bus"
INBOX_FILE = os.path.join(A2A_DIR, "inbox_dola.jsonl")
OFFSET_FILE = r"C:\Users\Admin\JavisOS\brains\Brain Default\Javis\runners\dola_offset.txt"

def tg_post(method, payload):
    url = f"{API_BASE}/{method}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[Dola TG Error] {e}", file=sys.stderr)
        return None

def send_msg(chat_id, text, reply_id=None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_id:
        payload["reply_to_message_id"] = reply_id
    res = tg_post("sendMessage", payload)
    if not res or not res.get("ok"):
        payload.pop("parse_mode", None)
        tg_post("sendMessage", payload)

def log_to_bus(user_id, chat_id, text):
    os.makedirs(A2A_DIR, exist_ok=True)
    entry = {
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "from": "user",
        "to": "dola",
        "user_id": user_id,
        "chat_id": chat_id,
        "text": text
    }
    with open(INBOX_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def main():
    print("[Dola AI Runner] Đã khởi động độc lập trên Telegram...", flush=True)
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
                chat_id = (msg.get("chat") or {}).get("id")
                from_user = msg.get("from") or {}
                user_id = from_user.get("id")
                mid = msg.get("message_id")
                text = (msg.get("text") or "").strip()

                if user_id not in ALLOWED_USERS and chat_id not in ALLOWED_GROUPS:
                    continue

                if not text:
                    continue

                # Xử lý lệnh hoặc chuyển tiếp A2A Bus
                log_to_bus(user_id, chat_id, text)

                cmd = text.lower().split("@")[0].strip()
                if cmd in ("/dola", "/start", "/help"):
                    reply = (
                        "👋 *Dola AI (Liên minh AI) trực tuyến!*\n"
                        "- Vai trò: Giám đốc Điều hành Tác chiến & Trải nghiệm (COO & Chief Engagement Officer).\n"
                        "- Nhiệm vụ: Tối ưu nhịp độ phễu người dùng, quản trị chuyển đổi và tương tác thực thi.\n"
                        "- Trạng thái: Kết nối độc lập với A2A Bus thành công."
                    )
                    send_msg(chat_id, reply, mid)
                else:
                    reply = f"✅ *Dola AI đã ghi nhận yêu cầu:* \"_{text[:60]}_...\"\nBản tin đã được nạp vào A2A Bus để điều phối thực thi."
                    send_msg(chat_id, reply, mid)

            time.sleep(0.5)
        except Exception as e:
            print(f"[Dola Loop Error] {e}", file=sys.stderr)
            time.sleep(2)

if __name__ == "__main__":
    main()
