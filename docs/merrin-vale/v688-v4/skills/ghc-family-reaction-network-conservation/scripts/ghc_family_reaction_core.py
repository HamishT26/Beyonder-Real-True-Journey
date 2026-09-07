"""Bounded exact symbolic reaction contracts. No physical or authority claims."""
from __future__ import annotations
import argparse
from fractions import Fraction
import functools
import json
import math
from pathlib import Path
import re

class Refusal(ValueError):
    pass

def need(condition, code):
    if not condition:
        raise Refusal(code)

def text(value):
    need(type(value) is str, 'TEXT_TYPE')
    need(len(value) <= 4096, 'TEXT_LIMIT')
    return value

def integer(value):
    need(type(value) is int, 'INTEGER_TYPE')
    need(abs(value) <= 10**9, 'INTEGER_LIMIT')
    return value

def rational(value):
    need(type(value) is str, 'RATIONAL_TYPE')
    need(len(value) <= 128 and re.fullmatch(r'[+-]?(?:\d+(?:/\d+)?|\d*\.\d+)', value), 'RATIONAL_VALUE')
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError):
        raise Refusal('RATIONAL_VALUE') from None

def fmt(value):
    return str(Fraction(value))

def mapping(value):
    need(type(value) is dict, 'MAP_TYPE')
    need(len(value) <= 1000, 'MAP_LIMIT')
    return value

def sequence(value, code='VECTOR_SHAPE', nonempty=True):
    need(type(value) is list and len(value) <= 1000 and (value or not nonempty), code)
    return value

def species(value):
    text(value)
    need(re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,63}', value), 'SPECIES_LABEL')
    return value

def side(value):
    result = {}
    for key, count in mapping(value).items():
        species(key)
        count = integer(count)
        need(count > 0, 'SIDE_COEFFICIENT')
        result[key] = count
    return result

def bool_flag(value):
    need(type(value) is bool, 'BOOLEAN_TYPE')
    return value

def formula_counts(value, grouped=False):
    value = text(value)
    need(bool(value) and len(value) <= 1000, 'FORMULA_SYNTAX')
    stack = [({}, '')]
    pos = 0
    while pos < len(value):
        char = value[pos]
        if char in '([' and grouped:
            need(len(stack) < 24, 'GROUP_DEPTH')
            stack.append(({}, char)); pos += 1
            continue
        if char in ')]' and grouped:
            need(len(stack) > 1 and stack[-1][1] == {')':'(',']':'['}[char], 'UNBALANCED_GROUP')
            counts, _ = stack.pop()
            need(bool(counts), 'EMPTY_GROUP')
            pos += 1
            match = re.match(r'\d+', value[pos:])
            multiplier = int(match.group()) if match else 1
            need(1 <= multiplier <= 10000, 'ATOM_COUNT')
            if match: pos += len(match.group())
            for key, amount in counts.items(): stack[-1][0][key] = stack[-1][0].get(key, 0) + amount * multiplier
            continue
        match = re.match(r'([A-Z][a-z]?)(\d*)', value[pos:])
        need(match is not None, 'FORMULA_SYNTAX')
        key, raw = match.groups(); count = int(raw) if raw else 1
        need(1 <= count <= 10000, 'ATOM_COUNT')
        stack[-1][0][key] = stack[-1][0].get(key, 0) + count
        pos += len(match.group())
    need(len(stack) == 1, 'UNBALANCED_GROUP')
    counts = dict(sorted(stack[0][0].items()))
    need(sum(counts.values()) <= 10**8, 'ATOM_TOTAL_LIMIT')
    return {'counts':counts, 'atom_total':sum(counts.values()), 'element_existence_verified':False}

def vectors(amounts, numbers):
    sequence(amounts); sequence(numbers)
    need(len(amounts) == len(numbers), 'VECTOR_SHAPE')
    amounts = [rational(v) for v in amounts]
    numbers = [integer(v) for v in numbers]
    need(all(v >= 0 for v in amounts), 'NEGATIVE_AMOUNT')
    return amounts, numbers

def matrix(value):
    sequence(value, 'MATRIX_SHAPE')
    rows = [sequence(row, 'MATRIX_SHAPE') for row in value]
    need(len({len(row) for row in rows}) == 1, 'MATRIX_SHAPE')
    need(len(rows) * len(rows[0]) <= 10000, 'MATRIX_LIMIT')
    return [[integer(v) for v in row] for row in rows]

FIELDS = {
    'flat_formula': {'formula'}, 'grouped_formula': {'formula'},
    'signed_numbers': {'reactants','products'}, 'primitive_numbers': {'numbers'},
    'element_residual': {'composition','numbers'}, 'charge_residual': {'charges','numbers'},
    'extent_update': {'initial_mol','numbers','extent_mol'}, 'extent_interval': {'initial_mol','numbers'},
    'limiting_pool': {'species','amounts_mol','numbers'}, 'degree_of_reaction': {'extent_mol','maximum_mol'},
    'pathway_sum': {'matrix','weights'}, 'moiety_certificate': {'matrix','weights'},
    'complex_registry': {'reactions'}, 'complex_incidence': {'node_count','edges'},
    'deficiency_record': {'complexes','linkage_classes','stoichiometric_rank'},
    'mass_action_monomial': {'law','coefficient','concentrations','orders'},
    'reaction_evidence': {'claim','available_roles','synthetic'}, 'arrow_semantics': {'arrow','observed'},
    'equation_comparison': {'left','right'},
    'accessible_equation': {'reactants','products','label','language','manual_evaluation'},
}
ORDER_FIELDS = {'reactant_order','product_order'}

def operation_value(data):
    mapping(data)
    op = text(data.get('operation'))
    need(op in FIELDS, 'OPERATION')
    fields = set(data) - {'operation'}
    need(fields == FIELDS[op] or (op == 'accessible_equation' and fields == FIELDS[op] | ORDER_FIELDS), 'FIELD_SET')
    if op in ('flat_formula','grouped_formula'):
        return formula_counts(data['formula'], op == 'grouped_formula')
    if op == 'signed_numbers':
        left, right = side(data['reactants']), side(data['products'])
        return {'signed':{k:right.get(k,0)-left.get(k,0) for k in sorted(left.keys() | right.keys())}}
    if op == 'primitive_numbers':
        values = [rational(v) for v in sequence(data['numbers'])]
        need(any(values), 'ZERO_EQUATION')
        multiple = math.lcm(*(v.denominator for v in values))
        integers = [int(v*multiple) for v in values]
        divisor = functools.reduce(math.gcd, (abs(v) for v in integers))
        return {'primitive':[v//divisor for v in integers]}
    if op == 'element_residual':
        composition = mapping(data['composition']); numbers = mapping(data['numbers']); elements = set()
        for label, atoms in composition.items():
            species(label); mapping(atoms)
            for symbol, count in atoms.items():
                species(symbol); need(integer(count) > 0, 'ATOM_COUNT'); elements.add(symbol)
        for label, value in numbers.items():
            need(label in composition, 'UNKNOWN_SPECIES'); integer(value)
        residual = {e:sum(n*composition[label].get(e,0) for label,n in numbers.items()) for e in sorted(elements)}
        return {'residual':residual,'balanced':all(v==0 for v in residual.values()),'physical_reaction_verified':False}
    if op == 'charge_residual':
        charges = mapping(data['charges']); numbers = mapping(data['numbers'])
        for label, value in charges.items(): species(label); integer(value)
        for label, value in numbers.items(): need(label in charges, 'UNKNOWN_SPECIES'); integer(value)
        result = sum(charges[k]*v for k,v in numbers.items())
        return {'charge_residual':result,'balanced':result==0,'electrochemistry_verified':False}
    if op in ('extent_update','extent_interval'):
        amounts, numbers = vectors(data['initial_mol'],data['numbers'])
        if op == 'extent_update':
            extent = rational(data['extent_mol']); result = [a+n*extent for a,n in zip(amounts,numbers)]
            need(all(v >= 0 for v in result), 'NEGATIVE_AMOUNT')
            return {'amounts_mol':[fmt(v) for v in result],'observed':False}
        lower = [-a/n for a,n in zip(amounts,numbers) if n>0]
        upper = [-a/n for a,n in zip(amounts,numbers) if n<0]
        return {'lower_mol':fmt(max(lower)) if lower else None,'upper_mol':fmt(min(upper)) if upper else None,'endpoints_included':True,'observed':False}
    if op == 'limiting_pool':
        names = [species(v) for v in sequence(data['species'])]
        need(len(set(names)) == len(names), 'DUPLICATE_SPECIES')
        amounts, numbers = vectors(data['amounts_mol'],data['numbers'])
        need(len(names) == len(amounts), 'VECTOR_SHAPE')
        caps = [(name,-amount/n) for name,amount,n in zip(names,amounts,numbers) if n<0]
        need(bool(caps), 'NO_CONSUMPTION'); bound = min(v for _,v in caps)
        return {'maximum_forward_extent_mol':fmt(bound),'limiting_species':[name for name,v in caps if v==bound],'observed':False}
    if op == 'degree_of_reaction':
        extent, maximum = rational(data['extent_mol']), rational(data['maximum_mol'])
        need(maximum > 0, 'MAXIMUM_EXTENT'); degree = extent/maximum
        need(0 <= degree <= 1, 'DEGREE_RANGE')
        return {'degree':fmt(degree),'observed':False}
    if op in ('pathway_sum','moiety_certificate'):
        mat = matrix(data['matrix']); weights = [rational(v) for v in sequence(data['weights'])]
        if op == 'pathway_sum':
            need(len(weights) == len(mat[0]), 'VECTOR_SHAPE')
            return {'net_numbers':[fmt(sum(a*b for a,b in zip(row,weights))) for row in mat],'kinetic_flux_observed':False}
        need(len(weights) == len(mat), 'VECTOR_SHAPE')
        residual = [sum(weights[i]*mat[i][j] for i in range(len(mat))) for j in range(len(mat[0]))]
        return {'column_residuals':[fmt(v) for v in residual],'conserved':not any(residual),'trivial':not any(weights),'physical_conservation_verified':False}
    if op == 'complex_registry':
        reactions = sequence(data['reactions'],'REACTION_SHAPE'); complexes = []; edges = []; keys = []
        for pair in reactions:
            sequence(pair,'REACTION_SHAPE'); need(len(pair)==2,'REACTION_SHAPE'); edge=[]
            for member in pair:
                value = dict(sorted(side(member).items())); key = tuple(value.items())
                if key not in keys: keys.append(key); complexes.append(value)
                edge.append(keys.index(key))
            edges.append(edge)
        return {'complexes':complexes,'edges':edges,'node_count':len(complexes)}
    if op == 'complex_incidence':
        n = integer(data['node_count']); need(1 <= n <= 1000,'NODE_COUNT')
        edges = sequence(data['edges'],'EDGE_SHAPE',False); need(n*len(edges)<=10000,'MATRIX_LIMIT')
        result = [[0]*len(edges) for _ in range(n)]
        for j,edge in enumerate(edges):
            sequence(edge,'EDGE_SHAPE'); need(len(edge)==2,'EDGE_SHAPE'); a,b = [integer(v) for v in edge]
            need(0<=a<n and 0<=b<n,'NODE_RANGE'); result[a][j]-=1; result[b][j]+=1
        return {'incidence':result,'column_sums':[sum(row[j] for row in result) for j in range(len(edges))]}
    if op == 'deficiency_record':
        n,l,s = [integer(data[k]) for k in ('complexes','linkage_classes','stoichiometric_rank')]
        need(n>=1,'NODE_COUNT'); need(1<=l<=n,'LINKAGE_RANGE'); need(s>=0,'RANK_RANGE'); need(n-l-s>=0,'NEGATIVE_DEFICIENCY')
        return {'deficiency':n-l-s,'network_verified':False,'dynamics_theorem_applied':False}
    if op == 'mass_action_monomial':
        need(text(data['law'])=='declared_mass_action','LAW_DECLARATION')
        coefficient = rational(data['coefficient']); need(coefficient>=0,'NEGATIVE_RATE_COEFFICIENT')
        concentrations = [rational(v) for v in sequence(data['concentrations'],nonempty=False)]
        orders = [integer(v) for v in sequence(data['orders'],nonempty=False)]
        need(len(concentrations)==len(orders),'VECTOR_SHAPE'); need(all(c>=0 for c in concentrations),'NEGATIVE_CONCENTRATION'); need(all(0<=v<=12 for v in orders),'ORDER_RANGE')
        value = coefficient * math.prod(c**n for c,n in zip(concentrations,orders))
        return {'formal_rate':fmt(value),'rate_units':'undeclared','measured_kinetics':False}
    if op == 'reaction_evidence':
        claim = text(data['claim'])
        requirements = {'stoichiometry':['entity_definition','balanced_equation'],'kinetics':['rate_law','parameter_estimates','time_series'],'thermodynamics':['standard_states','temperature','activity_model'],'deployment':['competent_release','safety_review']}
        need(claim in requirements,'CLAIM_CLASS'); need(bool_flag(data['synthetic']),'REAL_EVIDENCE_GATE')
        roles = [text(v) for v in sequence(data['available_roles'],nonempty=False)]
        need(len(roles)==len(set(roles)),'DUPLICATE_ROLE'); required = requirements[claim]
        return {'required_roles':required,'missing_roles':[v for v in required if v not in roles],'external_claim_supported':False}
    if op == 'arrow_semantics':
        arrow = text(data['arrow']); need(not bool_flag(data['observed']),'OBSERVATION_REQUIRED')
        meanings = {'=':'stoichiometric_relation','->':'net_forward','<->':'both_directions','<=>':'equilibrium_declaration','\u2192':'net_forward','\u21cc':'equilibrium_declaration'}
        need(arrow in meanings,'ARROW_PROFILE')
        return {'arrow':arrow,'meaning':meanings[arrow],'equilibrium_measured':False,'kinetics_measured':False}
    if op == 'equation_comparison':
        left = [rational(v) for v in sequence(data['left'])]; right = [rational(v) for v in sequence(data['right'])]
        need(len(left)==len(right),'VECTOR_SHAPE')
        if not any(left) and not any(right): relation,scale='both_zero',None
        elif not any(left) or not any(right): relation,scale='different',None
        else:
            index=next(i for i,v in enumerate(left) if v); factor=right[index]/left[index]
            if factor and all(b==a*factor for a,b in zip(left,right)): relation,scale=('same_orientation' if factor>0 else 'reverse_orientation'),fmt(factor)
            else: relation,scale='different',None
        return {'relation':relation,'scale':scale,'process_identity_verified':False}
    if op == 'accessible_equation':
        left,right = side(data['reactants']),side(data['products']); label=text(data['label']); language=text(data['language'])
        need(not bool_flag(data['manual_evaluation']),'MANUAL_EVALUATION_GATE'); need(language=='en','LANGUAGE_REVIEW_REQUIRED')
        orders=[]
        for name,member in [('reactant_order',left),('product_order',right)]:
            order = data.get(name,sorted(member))
            sequence(order,'ORDER_TYPE',False)
            need(all(type(v) is str for v in order) and len(order)==len(set(order)) and set(order)==set(member),'SPECIES_ORDER')
            orders.append(order)
        def spoken(member,order): return ' plus '.join(str(member[k])+' '+k for k in order) if member else 'empty set'
        return {'spoken':spoken(left,orders[0])+' yields '+spoken(right,orders[1]),'label_present':bool(label),'language':language,'accessibility_complete':False}
    raise Refusal('OPERATION')

def evaluate(data):
    try:
        return {'accepted':True,'error':None,'external_credit':False,'value':operation_value(data)}
    except Refusal as exc:
        return {'accepted':False,'error':str(exc),'external_credit':False,'value':None}

def strict_loads(raw):
    need(type(raw) is str and len(raw)<=1000000,'JSON_SIZE')
    def pairs(items):
        result={}
        for key,value in items:
            need(key not in result,'DUPLICATE_JSON_KEY'); result[key]=value
        return result
    def nonfinite(_): raise Refusal('NONFINITE_JSON')
    try:
        return json.loads(raw,object_pairs_hook=pairs,parse_constant=nonfinite)
    except (json.JSONDecodeError,RecursionError):
        raise Refusal('JSON_SYNTAX') from None

def typed_equal(left,right):
    if type(left) is not type(right): return False
    if type(left) is dict: return left.keys()==right.keys() and all(typed_equal(left[k],right[k]) for k in left)
    if type(left) is list: return len(left)==len(right) and all(typed_equal(a,b) for a,b in zip(left,right))
    return left==right

def cli(allowed):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--input',type=Path,required=True);parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    try:
        data=strict_loads(args.input.read_text(encoding='utf-8'))
        need(type(data) is dict and data.get('operation') in allowed,'RUNNER_OPERATION_SCOPE'); result=evaluate(data)
    except Refusal as exc: result={'accepted':False,'error':str(exc),'external_credit':False,'value':None}
    rendered=json.dumps(result,sort_keys=True,ensure_ascii=True,indent=2)+'\n'
    if args.output:
        with args.output.open('x',encoding='utf-8',newline='\n') as f: f.write(rendered)
    print(rendered,end='')
    return 0 if result['accepted'] else 2
