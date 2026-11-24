# -*- coding: utf-8 -*-
"""
Perplexity Telegram Bot Runner (Độc lập)
Định vị: Chief Intelligence Officer & Research Lead (Nghiên cứu & Dữ liệu chuyên sâu)
Kênh: @PerplexcityThangLee_bot (Token 9186042684:AAHG-efZ1jVB8lyOLhXagl7Cl6p8mFKAfPw)
"""
import os
import sys
import json
import time
import urllib.request
import urllib.parse
import urllib.error

BOT_TOKEN = "9186042684:AAHG-efZ1jVB8lyOLhXagl7Cl6p8mFKAfPw"
ALLOWED_USERS = [1894254685]
ALLOWED_GROUPS = [-1004479278576]
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"
A2A_DIR = r"C:\Users\Admin\JavisOS\brains\Brain Default\memory\a2a_bus"
INBOX_FILE = os.path.join(A2A_DIR, "inbox_perplexity.jsonl")
OFFSET_FILE = r"C:\Users\Admin\JavisOS\brains\Brain Default\Javis\runners\perplexity_offset.txt"

def tg_post(method, payload):
    url = f"{API_BASE}/{method}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[Perplexity TG Error] {e}", file=sys.stderr)
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
        "to": "perplexity",
        "user_id": user_id,
        "chat_id": chat_id,
        "text": text
    }
    with open(INBOX_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def main():
    print("[Perplexity Runner] Đã khởi động độc lập trên Telegram...", flush=True)
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

                log_to_bus(user_id, chat_id, text)

                cmd = text.lower().split("@")[0].strip()
                if cmd in ("/perplexity", "/start", "/help"):
                    reply = (
                        "🔍 *Perplexity (Liên minh AI) trực tuyến!*\n"
                        "- Vai trò: Giám đốc Thông tin & Nghiên cứu Chuyên sâu (CIO & Research Lead).\n"
                        "- Nhiệm vụ: Rà soát dữ liệu web thực tế, thẩm định chéo, cung cấp trích dẫn nguồn kiểm chứng.\n"
                        "- Trạng thái: Kết nối độc lập với A2A Bus thành công."
                    )
                    send_msg(chat_id, reply, mid)
                else:
                    reply = f"🔍 *Perplexity đã tiếp nhận đề tài nghiên cứu:* \"_{text[:60]}_...\"\nĐã chuyển dữ liệu vào A2A Bus để phân tích và trích xuất nguồn."
                    send_msg(chat_id, reply, mid)

            time.sleep(0.5)
        except Exception as e:
            print(f"[Perplexity Loop Error] {e}", file=sys.stderr)
            time.sleep(2)

if __name__ == "__main__":
    main()
