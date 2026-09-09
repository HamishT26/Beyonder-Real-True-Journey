"""Pure synthetic measurement-design contracts; no real measurement or authority action."""
from __future__ import annotations

import argparse
import copy
import itertools
import json
import pathlib
import re
from fractions import Fraction


class ContractError(ValueError): pass
def require(condition, code):
    if not condition: raise ContractError(code)
def integer(value, minimum=0, maximum=1000):
    require(type(value) is int and minimum <= value <= maximum, "E_INTEGER"); return value
def rational(value):
    require(type(value) in (int, str), "E_RATIONAL"); text=str(value)
    require(bool(re.fullmatch(r"[+-]?\d+(?:/\d+)?", text)) and len(text)<=80, "E_RATIONAL")
    try: result=Fraction(text)
    except (ValueError, ZeroDivisionError): raise ContractError("E_RATIONAL") from None
    require(max(abs(result.numerator), result.denominator)<=10**24, "E_LIMIT"); return result
def sequence(value, maximum=1000): require(type(value) is list and len(value)<=maximum, "E_SHAPE"); return value
def label(value): require(type(value) is str and 0<len(value.strip())<=120, "E_LABEL"); return value
def unique_labels(values):
    checked=[label(item) for item in sequence(values,50)]; require(len(checked)==len(set(checked)),"E_DUPLICATE"); return checked
def replicate_summary(values):
    rows=sequence(values,50); require(bool(rows),"E_EMPTY"); parsed=[rational(item) for item in rows]
    mean=sum(parsed,Fraction())/len(parsed); residuals=[item-mean for item in parsed]
    return {"count":len(parsed),"mean":str(mean),"residuals":[str(item) for item in residuals],"sum_squared_residuals":str(sum((item*item for item in residuals),Fraction())),"real_measurement":False}
def weighted_mean(values,weights):
    values=sequence(values,50); weights=sequence(weights,50); require(bool(values) and len(values)==len(weights),"E_SHAPE")
    parsed_values=[rational(item) for item in values]; parsed_weights=[rational(item) for item in weights]
    require(all(item>0 for item in parsed_weights),"E_POSITIVE"); total=sum(parsed_weights,Fraction())
    return {"mean":str(sum(v*w for v,w in zip(parsed_values,parsed_weights))/total),"total_weight":str(total),"weights_empirically_justified":False}
def affine_correction(indication,slope,intercept):
    indication=rational(indication); slope=rational(slope); intercept=rational(intercept); require(slope>0,"E_POSITIVE")
    return {"corrected":str((indication-intercept)/slope),"calibration_observed":False,"model":"indication=slope*value+intercept"}
def unit_scale(magnitude,numerator,denominator,from_unit,to_unit):
    magnitude=rational(magnitude); numerator=rational(numerator); denominator=rational(denominator)
    require(numerator>0 and denominator>0,"E_POSITIVE"); from_unit=label(from_unit); to_unit=label(to_unit)
    require(from_unit!=to_unit or numerator==denominator,"E_IDENTITY_FACTOR"); factor=numerator/denominator
    return {"magnitude":str(magnitude*factor),"factor":str(factor),"from_unit":from_unit,"to_unit":to_unit,"registry_verified":False}
def uncertainty_budget(components):
    rows=sequence(components,30); require(bool(rows),"E_EMPTY"); names=[]; variance=Fraction()
    for row in rows:
        require(type(row) is list and len(row)==3,"E_SHAPE"); name=label(row[0]); sensitivity=rational(row[1]); uncertainty=rational(row[2]); require(uncertainty>=0,"E_NONNEGATIVE")
        names.append(name); variance+=(sensitivity*uncertainty)**2
    require(len(names)==len(set(names)),"E_DUPLICATE")
    return {"component_count":len(rows),"combined_variance":str(variance),"correlations_assumed_zero":True,"real_measurement":False}
def expanded_uncertainty(variance,coverage_factor):
    variance=rational(variance); coverage_factor=rational(coverage_factor); require(variance>=0,"E_NONNEGATIVE"); require(coverage_factor>0,"E_POSITIVE")
    return {"expanded_uncertainty_squared":str(variance*coverage_factor**2),"coverage_factor":str(coverage_factor),"coverage_probability_verified":False}
def randomized_block(treatments,blocks,offset):
    treatments=unique_labels(treatments); require(bool(treatments),"E_EMPTY"); blocks=integer(blocks,1,20); offset=integer(offset,0,10**6); schedules=[]
    for block in range(blocks):
        start=(offset+block)%len(treatments); schedules.append({"block":block,"order":treatments[start:]+treatments[:start]})
    return {"blocks":schedules,"randomization_claimed":False,"balanced":True}
def latin_square(symbols,offset):
    symbols=unique_labels(symbols); require(1<=len(symbols)<=8,"E_SIZE"); offset=integer(offset,0,10**6); size=len(symbols)
    return {"size":size,"rows":[[symbols[(r+c+offset)%size] for c in range(size)] for r in range(size)],"randomization_claimed":False}
def factorial_design(factors):
    factors=unique_labels(factors); require(1<=len(factors)<=6,"E_SIZE"); rows=[list(values) for values in itertools.product([-1,1],repeat=len(factors))]
    return {"factors":factors,"run_count":len(rows),"rows":rows,"optimality_claimed":False}
def sample_registry(population_size,indices):
    population_size=integer(population_size,1,10000); indices=sequence(indices,1000)
    require(all(type(item) is int and 0<=item<population_size for item in indices),"E_INDEX"); require(len(indices)==len(set(indices)),"E_DUPLICATE")
    return {"indices":indices,"sample_size":len(indices),"coverage":str(Fraction(len(indices),population_size)),"complete_census":len(indices)==population_size}
OPERATIONS={function.__name__:function for function in [replicate_summary,weighted_mean,affine_correction,unit_scale,uncertainty_budget,expanded_uncertainty,randomized_block,latin_square,factorial_design,sample_registry]}
PARAMETERS={name:function.__code__.co_varnames[:function.__code__.co_argcount] for name,function in OPERATIONS.items()}
def evaluate(request):
    original=copy.deepcopy(request)
    try:
        require(type(request) is dict,"E_FIELDS"); operation=request.get("op"); require(type(operation) is str and operation in OPERATIONS,"E_OP")
        require(set(request)=={"op",*PARAMETERS[operation]},"E_FIELDS"); value=OPERATIONS[operation](**{field:copy.deepcopy(request[field]) for field in PARAMETERS[operation]}); require(request==original,"E_MUTATION")
        return {"ok":True,"value":value,"error":None}
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
    parser=argparse.ArgumentParser(description="Bounded synthetic model; no real measurement, task transport, or authority action."); parser.add_argument("--input",required=True); parser.add_argument("--output"); args=parser.parse_args()
    raw=pathlib.Path(args.input).read_bytes(); require(len(raw)<=4_000_000,"E_LIMIT"); request=strict_json(raw.decode("utf-8-sig")); batch=request if type(request) is list else [request]; sequence(batch)
    result=[evaluate(item) if type(item) is dict and item.get("op") in allowed else {"ok":False,"value":None,"error":"E_OP"} for item in batch]; result=result if type(request) is list else result[0]
    rendered=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+"\n"
    if args.output:
        with pathlib.Path(args.output).open("x",encoding="utf-8",newline="\n") as handle: handle.write(rendered)
    else: print(rendered,end="")
