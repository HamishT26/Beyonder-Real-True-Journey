"""Pure synthetic experiment-evidence contracts; no real decision or authority action."""
from __future__ import annotations

import argparse
import copy
import itertools
import json
import math
import pathlib
import re
from fractions import Fraction


class ContractError(ValueError): pass
def require(condition,code):
    if not condition: raise ContractError(code)
def integer(value,minimum=0,maximum=1000): require(type(value) is int and minimum<=value<=maximum,"E_INTEGER"); return value
def rational(value):
    require(type(value) in (int,str),"E_RATIONAL"); text=str(value); require(bool(re.fullmatch(r"[+-]?\d+(?:/\d+)?",text)) and len(text)<=80,"E_RATIONAL")
    try: result=Fraction(text)
    except (ValueError,ZeroDivisionError): raise ContractError("E_RATIONAL") from None
    require(max(abs(result.numerator),result.denominator)<=10**24,"E_LIMIT"); return result
def sequence(value,maximum=1000): require(type(value) is list and len(value)<=maximum,"E_SHAPE"); return value
def label(value): require(type(value) is str and 0<len(value.strip())<=120,"E_LABEL"); return value
def unique_labels(values):
    checked=[label(item) for item in sequence(values,50)]; require(len(checked)==len(set(checked)),"E_DUPLICATE"); return checked
def paired_effect(before,after):
    before=sequence(before,50); after=sequence(after,50); require(bool(before) and len(before)==len(after),"E_SHAPE")
    deltas=[rational(a)-rational(b) for b,a in zip(before,after)]
    return {"deltas":[str(item) for item in deltas],"mean_delta":str(sum(deltas,Fraction())/len(deltas)),"matching_verified_outside_model":False}
def sign_test(differences):
    rows=sequence(differences,60); require(bool(rows),"E_EMPTY"); parsed=[rational(item) for item in rows]; positives=sum(item>0 for item in parsed); negatives=sum(item<0 for item in parsed); ties=len(parsed)-positives-negatives; n=positives+negatives
    p_value=Fraction(1) if n==0 else min(Fraction(1),Fraction(2*sum(math.comb(n,i) for i in range(min(positives,negatives)+1)),2**n))
    return {"positive":positives,"negative":negatives,"ties":ties,"two_sided_p":str(p_value),"independence_verified":False}
def permutation_gap(values,group_a):
    values=sequence(values,10); require(2<=len(values)<=10,"E_SIZE"); parsed=[rational(item) for item in values]; group_a=sequence(group_a,9); require(0<len(group_a)<len(values),"E_SHAPE"); require(all(type(item) is int and 0<=item<len(values) for item in group_a),"E_INDEX"); require(len(group_a)==len(set(group_a)),"E_DUPLICATE")
    def gap(indices):
        chosen=set(indices); left=[value for i,value in enumerate(parsed) if i in chosen]; right=[value for i,value in enumerate(parsed) if i not in chosen]; return sum(left,Fraction())/len(left)-sum(right,Fraction())/len(right)
    observed=gap(group_a); groups=list(itertools.combinations(range(len(values)),len(group_a))); extreme=sum(abs(gap(group))>=abs(observed) for group in groups)
    return {"observed_gap":str(observed),"enumerated_assignments":len(groups),"two_sided_p":str(Fraction(extreme,len(groups))),"exchangeability_verified":False}
def bootstrap_grid(values,resamples):
    values=sequence(values,20); require(bool(values),"E_EMPTY"); parsed=[rational(item) for item in values]; resamples=sequence(resamples,100); require(bool(resamples),"E_EMPTY"); means=[]
    for row in resamples:
        row=sequence(row,len(values)); require(len(row)==len(values),"E_SHAPE"); require(all(type(item) is int and 0<=item<len(values) for item in row),"E_INDEX"); means.append(sum((parsed[item] for item in row),Fraction())/len(row))
    return {"means":[str(item) for item in means],"minimum":str(min(means)),"maximum":str(max(means)),"stochastic_claimed":False}
def binary_rows(value): value=sequence(value,100); require(all(type(item) is int and item in (0,1) for item in value),"E_BINARY"); return value
def confusion_profile(truth,prediction):
    truth=binary_rows(truth); prediction=binary_rows(prediction); require(bool(truth) and len(truth)==len(prediction),"E_SHAPE")
    tp=sum(t==p==1 for t,p in zip(truth,prediction)); tn=sum(t==p==0 for t,p in zip(truth,prediction)); fp=sum(t==0 and p==1 for t,p in zip(truth,prediction)); fn=sum(t==1 and p==0 for t,p in zip(truth,prediction))
    return {"tp":tp,"tn":tn,"fp":fp,"fn":fn,"sensitivity":None if tp+fn==0 else str(Fraction(tp,tp+fn)),"specificity":None if tn+fp==0 else str(Fraction(tn,tn+fp)),"real_classification":False}
def agreement_kappa(left,right,labels):
    labels=unique_labels(labels); require(len(labels)>=2,"E_SIZE"); left=sequence(left,100); right=sequence(right,100); require(bool(left) and len(left)==len(right),"E_SHAPE"); require(all(type(item) is str and item in labels for item in left+right),"E_LABEL"); n=len(left); observed=Fraction(sum(a==b for a,b in zip(left,right)),n); expected=sum(Fraction(left.count(item)*right.count(item),n*n) for item in labels); require(expected!=1,"E_DEGENERATE")
    return {"observed_agreement":str(observed),"expected_agreement":str(expected),"kappa":str((observed-expected)/(1-expected)),"reviewer_independence_verified":False}
def missingness_map(rows,columns):
    columns=unique_labels(columns); require(bool(columns),"E_EMPTY"); rows=sequence(rows,100); missing={column:0 for column in columns}; complete=0
    for row in rows:
        require(type(row) is dict and set(row)==set(columns),"E_FIELDS"); is_complete=True
        for column in columns:
            if row[column] is None: missing[column]+=1; is_complete=False
        complete+=is_complete
    return {"rows":len(rows),"missing_by_column":missing,"complete_rows":complete,"values_inferred":False}
def provenance_frontier(events):
    events=sequence(events,50); seen=set(); roots=[]; children={}; order=[]
    for event in events:
        require(type(event) is dict and set(event)=={"id","parents","digest"},"E_FIELDS"); event_id=label(event["id"]); require(event_id not in seen,"E_DUPLICATE"); parents=sequence(event["parents"],20); require(all(type(item) is str and item in seen for item in parents),"E_PARENT"); require(len(parents)==len(set(parents)),"E_DUPLICATE"); require(type(event["digest"]) is str and bool(re.fullmatch(r"[0-9a-f]{64}",event["digest"])),"E_DIGEST")
        if not parents: roots.append(event_id)
        children[event_id]=set()
        for parent in parents: children[parent].add(event_id)
        seen.add(event_id); order.append(event_id)
    return {"roots":roots,"frontier":[event_id for event_id in order if not children[event_id]],"topological_ids":order,"independent_review":False}
def release_scope(grant,now,purpose,artifact):
    require(type(grant) is dict and set(grant)=={"artifact","purposes","expires","revoked"},"E_FIELDS"); artifact=label(artifact); purpose=label(purpose); now=integer(now,0,10**9); grant_artifact=label(grant["artifact"]); purposes=unique_labels(grant["purposes"]); expires=integer(grant["expires"],0,10**9); require(type(grant["revoked"]) is bool,"E_BOOLEAN"); eligible=artifact==grant_artifact and purpose in purposes and now<expires and not grant["revoked"]
    return {"model_eligible":eligible,"real_consent_verified":False,"release_executed":False}
def authority_reservation(action,requested):
    action=label(action); allowed={"real_measurement_release","professional_calibration_decision","participant_enrollment","public_governance_decision","maori_authority_decision","stage20_promotion"}; require(action in allowed,"E_ACTION"); require(type(requested) is bool,"E_BOOLEAN")
    return {"action":action,"requested":requested,"executed":False,"disposition":"exact_gate"}
OPERATIONS={function.__name__:function for function in [paired_effect,sign_test,permutation_gap,bootstrap_grid,confusion_profile,agreement_kappa,missingness_map,provenance_frontier,release_scope,authority_reservation]}
PARAMETERS={name:function.__code__.co_varnames[:function.__code__.co_argcount] for name,function in OPERATIONS.items()}
def evaluate(request):
    original=copy.deepcopy(request)
    try:
        require(type(request) is dict,"E_FIELDS"); operation=request.get("op"); require(type(operation) is str and operation in OPERATIONS,"E_OP"); require(set(request)=={"op",*PARAMETERS[operation]},"E_FIELDS"); value=OPERATIONS[operation](**{field:copy.deepcopy(request[field]) for field in PARAMETERS[operation]}); require(request==original,"E_MUTATION"); return {"ok":True,"value":value,"error":None}
    except ContractError as exc: return {"ok":False,"value":None,"error":str(exc)}
def strict_json(text):
    def pairs(rows):
        result={}
        for key,value in rows:
            if key in result: raise ContractError("E_DUPLICATE_KEY")
            result[key]=value
        return result
    def constant(_): raise ContractError("E_NONFINITE")
    return json.loads(text,object_pairs_hook=pairs,parse_constant=constant)
def cli(allowed):
    parser=argparse.ArgumentParser(description="Bounded synthetic model; no real decision, task transport, or authority action."); parser.add_argument("--input",required=True); parser.add_argument("--output"); args=parser.parse_args(); raw=pathlib.Path(args.input).read_bytes(); require(len(raw)<=4_000_000,"E_LIMIT"); request=strict_json(raw.decode("utf-8-sig")); batch=request if type(request) is list else [request]; sequence(batch); result=[evaluate(item) if type(item) is dict and item.get("op") in allowed else {"ok":False,"value":None,"error":"E_OP"} for item in batch]; result=result if type(request) is list else result[0]; rendered=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+"\n"
    if args.output:
        with pathlib.Path(args.output).open("x",encoding="utf-8",newline="\n") as handle: handle.write(rendered)
    else: print(rendered,end="")
