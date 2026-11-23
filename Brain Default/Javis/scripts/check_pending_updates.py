import urllib.request
import json

tokens = {
    'claude': '9215605178:AAFoOXqjWA3eVLc_PNUR2F2iH1ftoul-JIk',
    'grok': '9294574508:AAFIfDmkXiaJBMdBif2IjekPiojvUKoBMow',
    'perplexity': '9186042684:AAHG-efZ1jVB8lyOLhXagl7Cl6p8mFKAfPw',
    'dola': '9160223359:AAGpgjOFB2R3ZPWq_Or-YrRm6MbEkIxJ3Co'
}

for name, token in tokens.items():
    try:
        url = f'https://api.telegram.org/bot{token}/getUpdates?limit=5'
        req = urllib.request.urlopen(url, timeout=5)
        res = json.loads(req.read().decode('utf-8'))
        updates = res.get('result', [])
        print(f'{name}: {len(updates)} pending updates')
        for u in updates:
            msg = u.get('message', {})
            text = msg.get('text', '')
            chat = msg.get('chat', {})
            sender = msg.get('from', {}).get('first_name', '')
            chat_title = chat.get('title', chat.get('type', ''))
            print(f"   [{chat_title}] {sender}: {text[:60]}")
    except Exception as e:
        print(f'{name}: error {e}')
