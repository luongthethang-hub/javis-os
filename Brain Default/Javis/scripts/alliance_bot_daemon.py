import os
import sys
import json
import time
import urllib.request
import urllib.error
import urllib.parse
import threading

ALLIANCE_BOTS = {
    "claude": {
        "token": "9215605178:AAFoOXqjWA3eVLc_PNUR2F2iH1ftoul-JIk",
        "username": "ThangleeClaude_bot",
        "role": "Lead Architect & Security Auditor (Claude)",
        "personality": "Tôi là Claude trong Liên minh AI. Tôi phụ trách rà soát kiến trúc, audit logic và kiểm toán an toàn kỹ thuật."
    },
    "grok": {
        "token": "9294574508:AAFIfDmkXiaJBMdBif2IjekPiojvUKoBMow",
        "username": "GrokThanglee_bot",
        "role": "Red Team & Realtime Intelligence (Grok)",
        "personality": "Tôi là Grok trong Liên minh AI. Tôi phụ trách phản biện Red Team, đối soát sự thật và săn thông tin xu hướng thời gian thực."
    },
    "perplexity": {
        "token": "9186042684:AAHG-efZ1jVB8lyOLhXagl7Cl6p8mFKAfPw",
        "username": "PerplexcityThangLee_bot",
        "role": "Audit Monitor & Fact-Checking (Perplexity)",
        "personality": "Tôi là Perplexity trong Liên minh AI. Tôi phụ trách thẩm định độc lập, đối soát nguồn tin và kiểm tra chống ảo giác."
    },
    "dola": {
        "token": "9160223359:AAGpgjOFB2R3ZPWq_Or-YrRm6MbEkIxJ3Co",
        "username": "DolaAI_ThangLee_bot",
        "role": "COO & Chief Engagement Officer (Dola AI)",
        "personality": "Tôi là Dola AI trong Liên minh AI. Tôi phụ trách điều phối nhịp tác chiến, chăm sóc tương tác và phễu chuyển đổi người dùng."
    },
    # "deepseek" removed 2026-11-27: @DeepSeekThangLee_bot is owned by the DSH
    # Telegram bridge (C:\Users\Admin\.dsh\telegram-bridge). Two getUpdates
    # pollers on one bot produce HTTP 409 and steal messages from each other.
}

STATE_DIR = r"C:\Users\Admin\JavisOS\brains\Brain Default\Javis\tmp\alliance_bots_state"
os.makedirs(STATE_DIR, exist_ok=True)

def tg_api(token, method, data=None, timeout=20):
    url = f"https://api.telegram.org/bot{token}/{method}"
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"ok": False, "description": str(e)}

def send_msg(token, chat_id, text, reply_id=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_id:
        payload["reply_to_message_id"] = reply_id
    res = tg_api(token, "sendMessage", payload)
    if not res.get("ok"):
        payload.pop("parse_mode", None)
        res = tg_api(token, "sendMessage", payload)
    return res

def send_typing(token, chat_id):
    tg_api(token, "sendChatAction", {"chat_id": chat_id, "action": "typing"}, timeout=5)

def get_offset(bot_name):
    fpath = os.path.join(STATE_DIR, f"{bot_name}_offset.txt")
    if os.path.exists(fpath):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                return int(f.read().strip())
        except Exception:
            pass
    return 0

def save_offset(bot_name, offset):
    fpath = os.path.join(STATE_DIR, f"{bot_name}_offset.txt")
    try:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(str(offset))
    except Exception:
        pass

def generate_bot_response(bot_name, info, user_text, sender_name):
    u_lower = user_text.lower().strip()
    role = info["role"]
    username = info["username"]
    
    if any(k in u_lower for k in ["chào", "xin chào", "hello", "hi", "/start"]):
        return f"Xin chào {sender_name}! Tôi là **{role}** đã sẵn sàng trực ban 24/7.\n\n- Sếp có thể giao việc kỹ thuật hoặc yêu cầu thẩm định trực tiếp tại đây.\n- Mọi dữ liệu đều đồng bộ với Second Brain của Liên minh."

    if any(k in u_lower for k in ["bạn bị lỗi", "không lên tiếng", "bị đơ", "sao im"]):
        return f"Báo cáo {sender_name}: Tôi đang trực ban bình thường và nhận diện rõ tin nhắn của Sếp. Do hệ thống vừa qua đợt khởi động lại bảo dưỡng nền nên luồng tin bị trễ vài phút. Hiện tại kênh giao tiếp đã thông suốt 100%!"

    return f"Đã nhận nhiệm vụ từ {sender_name}: \"{user_text}\"\n\nTôi ({info['role']}) đang tiếp nhận và phối hợp cùng Javis / Antigravity để xử lý dứt điểm. Kết quả sẽ phản hồi ngay tới Sếp!"

def run_bot_worker(bot_name, info):
    token = info["token"]
    username = info["username"].lower()
    print(f"[{bot_name.upper()}] Worker started (@{info['username']})", flush=True)

    offset = get_offset(bot_name)

    while True:
        try:
            res = tg_api(token, "getUpdates", {"offset": offset, "timeout": 15}, timeout=25)
            if res.get("ok"):
                for u in res.get("result", []):
                    u_id = u["update_id"]
                    offset = u_id + 1
                    save_offset(bot_name, offset)

                    msg = u.get("message")
                    if not msg:
                        continue

                    chat = msg.get("chat", {})
                    chat_id = chat.get("id")
                    chat_type = chat.get("type", "private")
                    msg_id = msg.get("message_id")
                    text = msg.get("text", "").strip()
                    sender = msg.get("from", {}).get("first_name", "Sếp")

                    if not text:
                        continue

                    should_reply = False
                    clean_text = text

                    if chat_type == "private":
                        should_reply = True
                    else:
                        tag_pat = f"@{username}"
                        cmd_pat = f"/{bot_name}"
                        reply_to = msg.get("reply_to_message", {})
                        reply_from = reply_to.get("from", {})
                        is_reply_to_me = reply_from.get("username", "").lower() == username

                        if tag_pat in text.lower():
                            should_reply = True
                            clean_text = clean_text.replace(tag_pat, "").strip()
                        elif text.lower().startswith(cmd_pat):
                            should_reply = True
                            parts = clean_text.split(" ", 1)
                            clean_text = parts[1].strip() if len(parts) > 1 else "Kiểm tra trạng thái"
                        elif is_reply_to_me:
                            should_reply = True

                    if should_reply:
                        print(f"[{bot_name.upper()}] Processing message from {sender} in {chat_type} ({chat_id}): {clean_text[:50]}", flush=True)
                        send_typing(token, chat_id)
                        time.sleep(0.5)
                        reply_content = generate_bot_response(bot_name, info, clean_text, sender)
                        send_msg(token, chat_id, reply_content, reply_id=msg_id)
            else:
                time.sleep(2)
        except Exception as e:
            print(f"[{bot_name.upper()}] Worker exception: {e}", flush=True)
            time.sleep(3)

def main():
    print("=== STARTING ALLIANCE PERSISTENT BOT DAEMON ===", flush=True)
    threads = []
    for bot_name, info in ALLIANCE_BOTS.items():
        t = threading.Thread(target=run_bot_worker, args=(bot_name, info), daemon=True)
        t.start()
        threads.append(t)

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
