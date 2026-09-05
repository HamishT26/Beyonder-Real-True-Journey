"""Explicit report projections and structural reservations for offline fixtures."""
import argparse,json
from pathlib import Path
def export(d):
    record=d['record'];allow=d['allow'];required=d['required']
    if len(allow)!=len(set(allow)):return {'error':'duplicate_allowlist'}
    if not set(required)<=set(allow):return {'error':'required_not_allowed'}
    if not set(required)<=set(record):return {'error':'missing_required'}
    return {k:record[k] for k in allow if k in record}
def table(d):
    h=d['headers'];rows=d['rows']
    return bool(h) and len(h)==len(set(h)) and all(type(x) is str and x.strip() for x in h) and all(len(row)==len(h) and all(type(x) is str and bool(x.strip()) for x in row) for row in rows)
def reservation(d):
    if not d['obligation'] or d['evidence'] is not None or d['authority'] is not None:return {'error':'unsupported_promotion'}
    if d['disposition'] not in ['represented','open_gap','exact_gate']:return {'error':'invalid_reservation'}
    return d['disposition']
OPERATIONS={'export':export,'table':table,'reservation':reservation}
def evaluate(operation,data):
    if operation not in OPERATIONS:return {'error':'unknown_operation'}
    try:return OPERATIONS[operation](data)
    except (KeyError,TypeError,ValueError,IndexError):return {'error':'malformed_input'}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--operation',required=True,choices=OPERATIONS);p.add_argument('--input',required=True);p.add_argument('--output');a=p.parse_args();text=json.dumps(evaluate(a.operation,json.loads(Path(a.input).read_text(encoding='utf8'))),ensure_ascii=False,sort_keys=True)+'\n'
    if a.output:
        with Path(a.output).open('x',encoding='utf8',newline='\n') as f:f.write(text)
    else:print(text,end='')
if __name__=='__main__':main()
