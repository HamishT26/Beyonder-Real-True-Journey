"""Use only the three frozen package surfaces on public synthetic records."""
import copy,json,sys
from pathlib import Path
import jmespath,dpath,dictdiffer

def run():
    checks=[]
    def check(name,fn,expected):
        value=fn();checks.append({'name':name,'observed':value,'expected':expected,'pass':value==expected})
    def reject(name,fn,kind):
        try:fn();checks.append({'name':name,'rejected':False,'pass':False})
        except kind as exc:checks.append({'name':name,'rejected':True,'exception_type':type(exc).__name__,'pass':True,'negative_success_credit':0})
    rows=[{'state':'completed','value':2},{'state':'open_gap','value':None}]
    check('jmespath public completed projection',lambda:jmespath.search("[?state=='completed'].value",rows),[2])
    reject('jmespath malformed expression',lambda:jmespath.compile('[?'),jmespath.exceptions.ParseError)
    check('jmespath null dropping boundary',lambda:jmespath.search('[].value',rows),[2])
    check('dpath nested scalar selection',lambda:dpath.get({'a':{'v':4}},'a/v'),4)
    reject('dpath missing path',lambda:dpath.get({'a':1},'absent'),KeyError)
    original={'nested':{'value':1},'items':['a']};corrected={'nested':{'value':3},'items':['a','b']}
    delta=list(dictdiffer.diff(original,corrected,tolerance=0));restored=dictdiffer.revert(delta,corrected)
    check('dictdiffer patch roundtrip',lambda:dictdiffer.patch(delta,original),corrected)
    check('dictdiffer revert roundtrip',lambda:restored,original)
    reject('dictdiffer invalid change action',lambda:dictdiffer.patch([('not-an-operation','a',(1,2))],{'a':1}),KeyError)
    check('package inputs unchanged',lambda:original,{'nested':{'value':1},'items':['a']})
    out={'schema':'ghc.family.mira.package-smokes.v1','checks':checks,'pass':all(x['pass'] for x in checks),'same_owner_only':True,'independent_reproduction':False,
         'boundaries':['Query null omission is explicit; do not infer complete denominators.','Mutable helpers act only on copied synthetic records.','No cryptographic disclosure, production conformance, complete privacy or exhaustive security.']}
    target=Path(sys.argv[1])
    with target.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'checks':len(checks),'pass':out['pass']}))
    return 0 if out['pass'] else 1

if __name__=='__main__':raise SystemExit(run())
