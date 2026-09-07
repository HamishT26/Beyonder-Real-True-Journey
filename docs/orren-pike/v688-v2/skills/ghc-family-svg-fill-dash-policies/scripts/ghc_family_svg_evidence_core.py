"""Bounded SVG metadata profiles; no rendering, external fetch, or authority action."""
from __future__ import annotations
import json
import pathlib
import re
import sys
from fractions import Fraction

NUM=r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?'
ARITY={'M':2,'L':2,'H':1,'V':1,'C':6,'S':4,'Q':4,'T':2,'A':7,'Z':0}
FIELDS={
 'number_token':{'token'},'length_token':{'token'},'viewbox':{'values'},'aspect_ratio':{'value'},
 'point_pairs':{'text'},'command_arity':{'command','parameters'},
 'moveto':{'command','current','points','first'},'lineto':{'command','current','parameters'},
 'closepath':{'start','current'},'cubic_controls':{'command','current','previous_command','previous_control','parameters'},
 'quadratic_controls':{'command','current','previous_command','previous_control','parameters'},
 'arc_parameters':{'current','radii','rotation','flags','endpoint'},'subpath_partition':{'commands'},
 'path_length':{'token'},'fill_rule':{'rule'},'dash_array':{'values'},
 'stroke_style':{'linecap','linejoin','miterlimit'},'marker_orientation':{'value'},
 'local_href':{'href','available_ids'},'paint_order':{'value'}
}

class Refusal(ValueError):pass
def require(condition,error):
 if not condition:raise Refusal(error)
def text(value):
 require(type(value) is str,'TEXT_TYPE');require(len(value)<=4096,'TEXT_BOUND');return value
def number(value):
 text(value);require(re.fullmatch(NUM,value) is not None,'NUMBER_SYNTAX')
 exponent=re.search(r'[eE]([+-]?[0-9]+)$',value)
 require(len(value)<=48 and (exponent is None or len(exponent[1])<=3 and abs(int(exponent[1]))<=6),'NUMBER_BOUND')
 n=Fraction(value);require(abs(n)<=10**9 and n.denominator<=10**24,'NUMBER_BOUND');return n
def array(value,error='ARRAY_SHAPE',bound=64):
 require(type(value) is list and len(value)<=bound,error);return value
def point(value):
 require(type(value) is list and len(value)==2,'POINT_SHAPE');return [number(x) for x in value]
def strings(value):return [str(x) for x in value]
def add(a,b):return [x+y for x,y in zip(a,b)]
def reflect(current,control):return [2*x-y for x,y in zip(current,control)]
def command(c):
 require(type(c) is str and len(c)==1 and c.upper() in ARITY,'COMMAND_NAME');return c
def parameters(c,values):
 vals=[number(x) for x in array(values)];n=ARITY[c.upper()]
 require((not vals) if n==0 else bool(vals) and len(vals)%n==0,'COMMAND_ARITY')
 return [vals[i:i+n] for i in range(0,len(vals),n)] if n else []
def outcome(value=None,error=None):return {'accepted':error is None,'error':error,'value':value,'external_credit':False}

def evaluate(record):
 try:
  require(type(record) is dict,'DOCUMENT_SHAPE')
  op=record.get('operation');require(type(op) is str and op in FIELDS,'OPERATION')
  require(set(record)==FIELDS[op]|{'operation'},'FIELD_SET')
  p=record
  if op=='number_token':
   n=number(p['token']);v={'rational':str(n),'negative_zero':n==0 and p['token'].startswith('-')}
  elif op=='length_token':
   m=re.fullmatch('('+NUM+r')(px|cm|mm|in|pt|pc|em|ex|%)?',text(p['token']))
   require(m is not None,'LENGTH_SYNTAX');unit=m[2] or 'user'
   v={'amount':str(number(m[1])),'unit':unit,'context_required':unit in ['%','em','ex']}
  elif op=='viewbox':
   require(type(p['values']) is list and len(p['values'])==4,'VIEWBOX_ARITY')
   ns=[number(x) for x in p['values']];require(ns[2]>=0 and ns[3]>=0,'NEGATIVE_EXTENT')
   v={'minimum':strings(ns[:2]),'extent':strings(ns[2:]),'rendering_enabled':ns[2]>0 and ns[3]>0}
  elif op=='aspect_ratio':
   fields=text(p['value']).split();require(1<=len(fields)<=2,'ASPECT_SYNTAX')
   align=fields[0];mode=fields[1] if len(fields)==2 else 'meet'
   require(align=='none' or re.fullmatch(r'x(?:Min|Mid|Max)Y(?:Min|Mid|Max)',align) is not None,'ASPECT_SYNTAX')
   require(mode in ['meet','slice'],'ASPECT_SYNTAX');v={'align':align,'mode':None if align=='none' else mode}
  elif op=='point_pairs':
   s=text(p['text']);matches=list(re.finditer(NUM,s));require(len(matches)<=64,'POINT_BOUND')
   if not matches:require(not s.strip(),'POINT_SEPARATOR')
   pos=0;ns=[]
   for i,m in enumerate(matches):
    separator=s[pos:m.start()]
    require((not separator.strip()) if i==0 else re.fullmatch(r'(?:\s+|\s*,\s*)',separator) is not None,'POINT_SEPARATOR')
    ns.append(number(m[0]));pos=m.end()
   require(not s[pos:].strip(),'POINT_SEPARATOR');require(len(ns)%2==0,'POINT_PAIR_ARITY')
   v={'points':[strings(ns[i:i+2]) for i in range(0,len(ns),2)]}
  elif op=='command_arity':
   c=command(p['command']);groups=parameters(c,p['parameters'])
   v={'groups':[strings(x) for x in groups],'followup_command':None if c.upper()=='Z' else ('L' if c=='M' else 'l' if c=='m' else c)}
  elif op=='moveto':
   c=p['command'];require(c in ['M','m'],'MOVE_COMMAND');require(type(p['first']) is bool,'FIRST_TYPE')
   current=point(p['current']);pairs=array(p['points'],'MOVE_POINTS',32);require(bool(pairs),'MOVE_POINTS')
   pairs=[point(x) for x in pairs];ends=[]
   for i,pt in enumerate(pairs):
    current=pt if c=='M' or i==0 and p['first'] else add(current,pt);ends.append(strings(current))
   v={'subpath_start':ends[0],'current_point':ends[-1],'implicit_lines':ends[1:]}
  elif op=='lineto':
   c=p['command'];require(type(c) is str and c in ['L','l','H','h','V','v'],'LINE_COMMAND')
   current=point(p['current']);groups=parameters(c,p['parameters']);ends=[]
   for ns in groups:
    if c.upper()=='L':current=ns if c=='L' else add(current,ns)
    elif c.upper()=='H':current=[ns[0] if c=='H' else current[0]+ns[0],current[1]]
    else:current=[current[0],ns[0] if c=='V' else current[1]+ns[0]]
    ends.append(strings(current))
   v={'endpoints':ends,'current_point':strings(current)}
  elif op=='closepath':
   require(p['start'] is not None,'NO_SUBPATH');start=point(p['start']);current=point(p['current'])
   v={'endpoint':strings(start),'delta':strings([a-b for a,b in zip(start,current)]),'closed':True}
  elif op in ['cubic_controls','quadratic_controls']:
   cubic=op=='cubic_controls';cs=['C','c','S','s'] if cubic else ['Q','q','T','t'];c=p['command']
   require(c in cs,'CUBIC_COMMAND' if cubic else 'QUADRATIC_COMMAND');current=point(p['current']);groups=parameters(c,p['parameters']);require(len(groups)==1,'COMMAND_ARITY')
   ns=groups[0];pts=[ns[i:i+2] for i in range(0,len(ns),2)]
   if c.islower():pts=[add(current,pt) for pt in pts]
   smooth=c.upper() in ['S','T']
   if smooth:
    prior=p['previous_command'];require(prior is None or type(prior) is str and prior in 'MmLlHhVvCcSsQqTtAaZz','PREVIOUS_COMMAND')
    if prior in cs:
     require(p['previous_control'] is not None,'PREVIOUS_CONTROL');ctrl=reflect(current,point(p['previous_control']))
    else:ctrl=current
    pts=[ctrl]+pts
   v=({'control1':strings(pts[0]),'control2':strings(pts[1]),'endpoint':strings(pts[2])} if cubic else {'control':strings(pts[0]),'endpoint':strings(pts[1])})
  elif op=='arc_parameters':
   current=point(p['current']);radii=[abs(x) for x in point(p['radii'])];end=point(p['endpoint']);rotation=number(p['rotation']);flags=p['flags']
   require(type(flags) is list and len(flags)==2 and all(type(x) is int and x in [0,1] for x in flags),'ARC_FLAGS')
   kind='omitted' if current==end else 'line' if 0 in radii else 'arc'
   v={'radii':strings(radii),'rotation':str(rotation),'large_arc':flags[0]==1,'sweep':flags[1]==1,'endpoint':strings(end),'kind':kind}
  elif op=='subpath_partition':
   commands=array(p['commands']);v={'subpaths':[]}
   for i,c in enumerate(commands):
    command(c)
    if i==0:require(c.upper()=='M','INITIAL_MOVETO')
    prior=v['subpaths'][-1] if v['subpaths'] else None
    if c.upper()=='M':v['subpaths'].append({'commands':[c],'closed':False,'implicit_start':False})
    elif prior['closed']:
     require(c.upper()!='Z','REDUNDANT_CLOSE');v['subpaths'].append({'commands':[c],'closed':False,'implicit_start':True})
    else:prior['commands'].append(c);prior['closed']=c.upper()=='Z'
  elif op=='path_length':
   n=None if p['token'] is None else number(p['token']);require(n is None or n>=0,'NEGATIVE_PATH_LENGTH')
   v={'declared_length':None if n is None else str(n),'positive_scale_reference':n is not None and n>0}
  elif op=='fill_rule':
   rule=text(p['rule']);require(rule not in ['inherit','initial','unset'],'CASCADE_REQUIRED');require(rule in ['nonzero','evenodd'],'FILL_RULE');v={'rule':rule,'computed_fill':False}
  elif op=='dash_array':
   ns=[] if p['values']=='none' else [number(x) for x in array(p['values'])];require(all(x>=0 for x in ns),'NEGATIVE_DASH')
   if len(ns)%2:ns=ns+ns
   period=sum(ns,Fraction(0));v={'pattern':strings(ns),'period':str(period),'solid':period==0}
  elif op=='stroke_style':
   require(p['linecap'] in ['butt','round','square'],'LINECAP');require(p['linejoin'] in ['miter','miter-clip','round','bevel','arcs'],'LINEJOIN');n=number(p['miterlimit']);require(n>=1,'MITER_LIMIT')
   v={'linecap':p['linecap'],'linejoin':p['linejoin'],'miterlimit':str(n),'rendered':False}
  elif op=='marker_orientation':
   s=text(p['value'])
   if s in ['auto','auto-start-reverse']:v={'mode':s,'angle':None,'unit':None}
   else:
    m=re.fullmatch('('+NUM+r')(deg|rad|grad|turn)?',s);require(m is not None,'ORIENT_SYNTAX');v={'mode':'angle','angle':str(number(m[1])),'unit':m[2] or 'deg'}
  elif op=='local_href':
   href=text(p['href']);require(href.startswith('#'),'EXTERNAL_REFERENCE');frag=href[1:];require(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.-]*',frag) is not None,'FRAGMENT_SYNTAX')
   ids=array(p['available_ids']);require(all(type(x) is str and len(x)<=128 for x in ids),'TARGET_SHAPE');require(len(set(ids))==len(ids),'DUPLICATE_TARGET')
   v={'fragment':frag,'resolved':frag in ids,'external_fetch':False}
  else:
   s=text(p['value']);order=['fill','stroke','markers']
   if s!='normal':
    supplied=s.split();require(bool(supplied) and len(supplied)==len(set(supplied)) and all(x in order for x in supplied),'PAINT_ORDER');order=supplied+[x for x in order if x not in supplied]
   v={'order':order}
  return outcome(v)
 except Refusal as exc:return outcome(error=str(exc))

def strict_loads(raw):
 if isinstance(raw,bytes):
  require(len(raw)<=1024*1024,'DOCUMENT_BOUND');raw=raw.decode('utf-8')
 require(type(raw) is str and not raw.startswith('\ufeff'),'DOCUMENT_ENCODING')
 def pairs(seq):
  d={}
  for k,v in seq:
   require(k not in d,'DUPLICATE_KEY');d[k]=v
  return d
 def constant(value):raise Refusal('NONFINITE')
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=constant)

def main(allowed=None):
 try:
  require(len(sys.argv)==2,'ONE_INPUT_REQUIRED');p=pathlib.Path(sys.argv[1]);require(p.stat().st_size<=1024*1024,'DOCUMENT_BOUND');record=strict_loads(p.read_bytes())
  if allowed is not None:require(type(record) is dict and record.get('operation') in allowed,'OPERATION_SCOPE')
  result=evaluate(record)
 except (OSError,UnicodeError,json.JSONDecodeError,RecursionError):result=outcome(error='DOCUMENT_READ')
 except Refusal as exc:result=outcome(error=str(exc))
 print(json.dumps(result,sort_keys=True,ensure_ascii=True,allow_nan=False))
 return 0 if result['accepted'] else 2

if __name__=='__main__':raise SystemExit(main())
