"""Deterministic offline event calendars, state traces, queues, and replay."""
from __future__ import annotations
import argparse, heapq, json
from pathlib import Path

def integer(x):return type(x) is int
def schedule(data):
    events=data['events'];labels=[e[0] for e in events]
    if len(set(labels))!=len(labels):return {'error':'duplicate_event'}
    if any(not integer(e[1]) or e[1]<0 for e in events):return {'error':'invalid_tick'}
    if any(not integer(e[2]) for e in events):return {'error':'invalid_priority'}
    queue=[(tick,priority,i,label) for i,(label,tick,priority) in enumerate(events)]
    heapq.heapify(queue);result=[]
    while queue:
        tick,_,_,label=heapq.heappop(queue)
        if 'until' not in data or tick<data['until']:result.append(label)
    return result

TRANSITIONS={('planned','start'):'running',('planned','cancel'):'cancelled',('running','pause'):'paused',('running','finish'):'recorded',('running','cancel'):'cancelled',('paused','resume'):'running',('paused','cancel'):'cancelled'}
def transition(data):
    state='planned'
    for event in data['events']:
        key=(state,event)
        if key not in TRANSITIONS:return {'error':'invalid_transition'}
        state=TRANSITIONS[key]
    return state

def queue(data):
    jobs=data['jobs'];labels=[j[0] for j in jobs]
    if len(labels)!=len(set(labels)):return {'error':'duplicate_job'}
    if any(not integer(t) or t<0 for j in jobs for t in j[1:]):return {'error':'invalid_job'}
    result=[];free=0
    for _,(label,arrival,duration) in sorted(enumerate(jobs),key=lambda p:(p[1][1],p[0])):
        start=max(arrival,free);free=start+duration;result.append([label,start,free])
    return result

def replay(data):
    seen=dict(data.get('seen',{}));total=data.get('initial',0)
    if not integer(total):return {'error':'invalid_delta'}
    for label,delta in data['events']:
        if not integer(delta):return {'error':'invalid_delta'}
        if label in seen:
            if type(seen[label]) is not type(delta) or seen[label]!=delta:return {'error':'conflicting_replay'}
            continue
        seen[label]=delta;total+=delta
    return total

OPERATIONS={'schedule':schedule,'transition':transition,'queue':queue,'replay':replay}
def evaluate(operation,data):
    if operation not in OPERATIONS:return {'error':'unknown_operation'}
    try:return OPERATIONS[operation](data)
    except (KeyError,TypeError,ValueError,IndexError):return {'error':'malformed_input'}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--operation',required=True,choices=OPERATIONS);p.add_argument('--input',required=True);p.add_argument('--output');a=p.parse_args()
    value=evaluate(a.operation,json.loads(Path(a.input).read_text(encoding='utf8')))
    text=json.dumps(value,sort_keys=True,ensure_ascii=False)+'\n'
    if a.output:
        with Path(a.output).open('x',encoding='utf8',newline='\n') as f:f.write(text)
    else:print(text,end='')
if __name__=='__main__':main()
