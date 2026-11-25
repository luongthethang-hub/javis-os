"""Bounded synthetic benchmark. Never logs credentials or sends vault content."""
import concurrent.futures
import datetime
import json
import pathlib
import random
import statistics
import time
import urllib.request
import urllib.error

ROOT = pathlib.Path(__file__).resolve().parent
MODELS = ['claude-sonnet-4-6', 'gpt-6-luna', 'gpt-5.6-sol', 'deepseek-v4.1-flash', 'gemini-flash-3.8-high', 'grok-4.7']
SEED = 25112026
rng = random.Random(SEED)
a, b = rng.randint(120, 300), rng.randint(11, 39)
rows = [{'id': i, 'status': rng.choice(['done', 'open']), 'amount': rng.randint(5, 90)} for i in range(8)]
expected_sum = sum(x['amount'] for x in rows if x['status'] == 'done')
ticket = rng.randint(1000, 9999)
CASES = [
 {'name': 'arithmetic', 'prompt': f'Return ONLY JSON {{"answer":integer}}. Calculate {a} * {b} + 17.', 'expected': {'answer': a*b+17}},
 {'name': 'data', 'prompt': 'Return ONLY JSON {"total":integer}. Sum amount only for status=done. Data: '+json.dumps(rows), 'expected': {'total': expected_sum}},
 {'name': 'code', 'prompt': 'Python 3: def f(xs):\n    total=0\n    for i in range(len(xs)-1): total+=xs[i]\n    return total\nReturn ONLY JSON {"bug":"off_by_one","result":integer,"fixed":integer}. Give actual result and intended sum for f([3,7,11,2]).', 'expected': {'bug':'off_by_one','result':21,'fixed':23}},
 {'name': 'grounding', 'prompt': 'Synthetic source: model X takes 2s on task A, model Y takes 3s on task A. There is NO price or task B data. Return ONLY JSON {"faster_on_A":"X" or "Y","cheaper":null or string,"best_on_B":null or string}. Do not invent missing facts.', 'expected': {'faster_on_A':'X','cheaper':None,'best_on_B':None}},
 {'name': 'tool', 'prompt': f'Call inspect_ticket exactly once with ticket={ticket}. Do not answer with prose. This is a simulated read-only tool; it will not be executed.', 'expected': {'ticket':ticket}},
]
TOOL = {'type':'function','function':{'name':'inspect_ticket','description':'Inspect a synthetic ticket, read only.', 'parameters':{'type':'object','properties':{'ticket':{'type':'integer'}},'required':['ticket'],'additionalProperties':False}}}

def parse_json(text):
    s=text.strip()
    if s.startswith('```'):
        s='\n'.join(s.splitlines()[1:-1])
    return json.loads(s)

def run(model, case, base, key):
    payload={'model':model,'messages':[{'role':'user','content':case['prompt']}], 'max_tokens':700,'stream':True,'stream_options':{'include_usage':True}}
    if case['name']=='tool':
        payload.update(tools=[TOOL],tool_choice={'type':'function','function':{'name':'inspect_ticket'}})
    req=urllib.request.Request(base+'/chat/completions', data=json.dumps(payload).encode(), headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','User-Agent':'LocalModelBenchmark/1.0'})
    start=time.perf_counter(); first=None; text=''; calls={}; usage={}; returned=None
    record={'model':model,'case':case['name'],'passed':False}
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            for line in response:
                if time.perf_counter()-start>90:
                    raise TimeoutError('total request deadline 90s')
                if not line.startswith(b'data:'): continue
                raw=line[5:].strip()
                if raw==b'[DONE]': break
                obj=json.loads(raw)
                returned=obj.get('model',returned)
                if obj.get('usage'): usage=obj['usage']
                for choice in obj.get('choices',[]):
                    delta=choice.get('delta',{})
                    content=delta.get('content') or ''
                    tc=delta.get('tool_calls') or []
                    if (content or tc) and first is None: first=time.perf_counter()-start
                    text+=content
                    for call in tc:
                        slot=calls.setdefault(call.get('index',0), {'name':'','arguments':''})
                        fun=call.get('function',{})
                        slot['name']+=fun.get('name') or ''
                        slot['arguments']+=fun.get('arguments') or ''
        if case['name']=='tool':
            record['passed']=len(calls)==1 and next(iter(calls.values()))['name']=='inspect_ticket' and parse_json(next(iter(calls.values()))['arguments'])==case['expected']
        else:
            record['passed']=parse_json(text)==case['expected']
        record.update(output=text,tool_calls=list(calls.values()),usage=usage,returned_model=returned)
    except urllib.error.HTTPError as exc:
        record['error']='HTTP '+str(exc.code)
    except Exception as exc:
        record['error']=type(exc).__name__+': '+str(exc).replace(key,'[REDACTED]')[:180]
        record['output']=text
    record.update(seconds=round(time.perf_counter()-start,3),ttft_seconds=round(first,3) if first is not None else None)
    return record

def main():
    settings=json.loads(pathlib.Path(r'C:\Users\Admin\JavisOS\server\settings.json').read_text(encoding='utf-8'))['model']
    base=settings['openai_compat_base'].rstrip('/'); key=settings['openai_compat_key']
    if key.startswith('enc:'):
        from cryptography.fernet import Fernet
        local_key=pathlib.Path(r'C:\Users\Admin\JavisOS\server\.secret_key').read_bytes().strip()
        key=Fernet(local_key).decrypt(key[4:].encode('ascii')).decode('utf-8')
    elif key.startswith('plain:'):
        key=key[6:]
    if base!='https://api.shopdonk.com/v1' or not key:
        raise RuntimeError('Unexpected endpoint or missing key; no calls sent')
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for n,case in enumerate(CASES,1):
            order=MODELS.copy(); rng.shuffle(order)
            futures=[pool.submit(run,m,case,base,key) for m in order]
            for f in concurrent.futures.as_completed(futures):
                r=f.result(); r['round']=n; results.append(r)
                print(json.dumps({k:r[k] for k in ('model','case','passed','seconds')},ensure_ascii=False),flush=True)
            (ROOT/'results.json').write_text(json.dumps({'seed':SEED,'cases':CASES,'results':results},ensure_ascii=False,indent=2),encoding='utf-8')
    summary=[]
    for m in MODELS:
        rr=[r for r in results if r['model']==m]
        times=[r['seconds'] for r in rr]
        tt=[r['ttft_seconds'] for r in rr if r['ttft_seconds'] is not None]
        summary.append({'model':m,'passed':sum(r['passed'] for r in rr),'tests':len(rr),'median_seconds':round(statistics.median(times),3),'max_seconds':max(times),'median_ttft_seconds':round(statistics.median(tt),3) if tt else None,'tool_passed':next(r['passed'] for r in rr if r['case']=='tool'),'prompt_tokens':sum(r.get('usage',{}).get('prompt_tokens',0) for r in rr),'completion_tokens':sum(r.get('usage',{}).get('completion_tokens',0) for r in rr)})
    (ROOT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
