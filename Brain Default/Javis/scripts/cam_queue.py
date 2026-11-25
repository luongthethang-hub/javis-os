"""Local trusted-worker pull queue. Python 3.12, standard library only."""
import argparse
import json
import re
import secrets
import sqlite3
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[1] / 'cam-queue.sqlite3'


def run(db, op, args):
    c = sqlite3.connect(db, timeout=10)
    try:
        with c:
            c.execute('BEGIN IMMEDIATE')
            c.execute('CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY, packet TEXT NOT NULL, state TEXT NOT NULL, owner TEXT, ticket TEXT, result TEXT)')
            if op == 'status':
                return dict(c.execute('SELECT state,count(*) FROM jobs GROUP BY state'))
            if op == 'put':
                raw = Path(args[0]).read_bytes()
                if len(raw) > 3000:
                    raise ValueError('Queue profile: maximum 3000 UTF-8 bytes')
                p = json.loads(raw.decode('utf-8-sig'))
                def strings(v):
                    return isinstance(v, list) and all(isinstance(x, str) and x.strip() for x in v)
                if not (p['schema'] == 'taskpacket/v1' and p['risk_tier'] == 'LOW' and p['autonomy_level'] == 'A3' and all(isinstance(p[k], str) and p[k].strip() for k in ('task_id','trace_id','goal')) and all(strings(p[k]) for k in ('constraints','inputs','checklist','eligible_workers')) and p['constraints'] and 3 <= len(p['checklist']) <= 5 and p['eligible_workers'] and set(p['eligible_workers']) <= {'javis','deepseek-lead','antigravity'} and p['max_retries'] == 2 and p['escalate_to_l1_on_fail'] is True):
                    raise ValueError('Invalid taskpacket/v1 or ineligible risk tier')
                for ref in p['inputs']:
                    if not re.fullmatch(r'.+#sha256=[0-9a-f]{64}', ref):
                        raise ValueError('Expected versioned source reference')
                packet = json.dumps(p, sort_keys=True)
                old = c.execute('SELECT packet FROM jobs WHERE id=?',(p['task_id'],)).fetchone()
                if old and old[0] != packet:
                    raise ValueError('Conflicting task_id')
                if not old:
                    c.execute("INSERT INTO jobs(id,packet,state) VALUES(?,?,'ready')",(p['task_id'],packet))
                return 'existing' if old else 'queued'
            if op == 'claim':
                worker, = args
                if c.execute("SELECT 1 FROM jobs WHERE state='running' AND owner=?",(worker,)).fetchone():
                    return None
                row = c.execute("SELECT id, packet FROM jobs WHERE state='ready' AND EXISTS (SELECT 1 FROM json_each(packet,'$.eligible_workers') WHERE value=?) ORDER BY rowid LIMIT 1",(worker,)).fetchone()
                if not row:
                    return None
                token = secrets.token_hex(24)
                c.execute("UPDATE jobs SET state='running',owner=?,ticket=? WHERE id=?",(worker,token,row[0]))
                return {'packet':json.loads(row[1]),'ticket':token}
            task, ticket, evidence = args
            if not evidence.strip():
                raise ValueError('Evidence reference or failure reason required')
            state = 'review' if op == 'submit' else 'escalated'
            if not c.execute("UPDATE jobs SET state=?,result=?,ticket=NULL WHERE state='running' AND id=? AND ticket=?",(state,evidence,task,ticket)).rowcount:
                raise ValueError('No matching active claim')
            return state
    finally:
        c.close()


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--db', default=str(DEFAULT))
    cli.add_argument('op', choices=['status','put','claim','submit','fail'])
    cli.add_argument('args', nargs='*')
    a = cli.parse_args()
    try:
        print(json.dumps(run(a.db,a.op,a.args), ensure_ascii=True))
    except (KeyError, TypeError, ValueError, sqlite3.Error, OSError) as exc:
        cli.exit(1, f'{exc}\n')
