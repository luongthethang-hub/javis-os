import urllib.request
import json

tokens = {
    'claude': ('9215605178:AAFoOXqjWA3eVLc_PNUR2F2iH1ftoul-JIk', 'ThangleeClaude_bot'),
    'grok': ('9294574508:AAFIfDmkXiaJBMdBif2IjekPiojvUKoBMow', 'GrokThanglee_bot'),
    'perplexity': ('9186042684:AAHG-efZ1jVB8lyOLhXagl7Cl6p8mFKAfPw', 'PerplexcityThangLee_bot'),
    'dola': ('9160223359:AAGpgjOFB2R3ZPWq_Or-YrRm6MbEkIxJ3Co', 'DolaAI_ThangLee_bot')
}

for name, (token, username) in tokens.items():
    print(f"\n=== BOT: {name} (@{username}) ===")
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    req = urllib.request.urlopen(url, timeout=10)
    res = json.loads(req.read().decode('utf-8'))
    updates = res.get('result', [])
    print(f"Total pending: {len(updates)}")
    for u in updates:
        u_id = u.get('update_id')
        msg = u.get('message', {})
        txt = msg.get('text', '')
        chat = msg.get('chat', {})
        c_id = chat.get('id')
        c_type = chat.get('type')
        c_title = chat.get('title', c_type)
        sender = msg.get('from', {}).get('first_name', '')
        print(f"  [id={u_id}] {sender} in {c_title} ({c_id}): {txt}")
