"""Execute the separately recorded interpretation plan without reading its answers."""
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path

os.environ['NUMEXPR_MAX_THREADS'] = '2'
os.environ['NUMEXPR_NUM_THREADS'] = '2'
os.environ['OMP_NUM_THREADS'] = '2'
import numpy as np
import numexpr as ne
import opt_einsum as oe
import symengine as se

base = Path(__file__).resolve().parents[1]
symbolic = []
for n in range(2, 7):
    variables = [se.Symbol('f' + str(i)) for i in range(n)]
    energy = sum((i + 1) * (variables[i + 1] - variables[i]) ** 2 for i in range(n - 1))
    residuals = []
    for j in range(n):
        weighted_difference = 0
        if j:
            weighted_difference += j * (variables[j] - variables[j - 1])
        if j + 1 < n:
            weighted_difference += (j + 1) * (variables[j] - variables[j + 1])
        residuals.append(str(se.expand(se.diff(energy, variables[j]) - 2 * weighted_difference)))
    symbolic.append({'vertices': n, 'residuals': residuals, 'passed': all(r == '0' for r in residuals)})

proposals = json.loads((base / 'plan/new-proposals.json').read_bytes())['proposals']
arrays = []
for row in (p for p in proposals if p['operation'] == 'energy_identity'):
    payload = row['request']['payload']
    vertices, edges = payload['vertices'], payload['edges']
    weights = np.array(payload['weights'], dtype=np.int64)
    potential = np.array(payload['potential'], dtype=np.int64)
    indices = {vertex: i for i, vertex in enumerate(vertices)}
    incidence = np.zeros((len(edges), len(vertices)), dtype=np.int64)
    for i, (a, b) in enumerate(edges):
        incidence[i, indices[a]] = -1
        incidence[i, indices[b]] = 1
    matrix = incidence.T @ np.diag(weights) @ incidence
    contracted = int(oe.contract('i,ij,j->', potential, matrix, potential, optimize='greedy'))
    source = np.array([payload['potential'][indices[a]] for a, b in edges], dtype=np.int64)
    target = np.array([payload['potential'][indices[b]] for a, b in edges], dtype=np.int64)
    terms = ne.evaluate('weights*(target-source)*(target-source)', local_dict={'weights': weights, 'target': target, 'source': source}, global_dict={}, optimization='moderate')
    elementwise = sum(int(value) for value in terms)
    expected = row['expected']['value']['edge_energy']
    assert abs(expected) < 2 ** 53
    arrays.append({'proposal_id': row['proposal_id'], 'opt_einsum': contracted, 'numexpr': elementwise, 'frozen_expected': expected, 'passed': contracted == elementwise == expected})

steps = []
for dt in [Fraction(1, 4), Fraction(1, 2), Fraction(3, 2)]:
    initial = [Fraction(0), Fraction(1)]
    derivative = [initial[0] - initial[1], initial[1] - initial[0]]
    updated = [a - dt * b for a, b in zip(initial, derivative)]
    energy = (updated[1] - updated[0]) ** 2 / 2
    steps.append({'step': str(dt), 'updated_potential': [str(x) for x in updated], 'energy_after': str(energy), 'energy_before': '1/2', 'decreases_or_equal': energy <= Fraction(1, 2)})
negative_energy = Fraction(-1, 2) * (1 - 0) ** 2
disconnected_potential = [2, 2, 9]
disconnected_energy = Fraction(1, 2) * (disconnected_potential[1] - disconnected_potential[0]) ** 2
curve = [{'step': str(Fraction(i, 20)), 'energy_ratio': str((1 - 2 * Fraction(i, 20)) ** 2)} for i in range(31)]
receipt = {'symbolic_derivative_checks': symbolic, 'array_energy_comparisons': arrays,
           'negative_weight_counterexample': {'energy': str(negative_energy), 'inside_evaluator_profile': False},
           'explicit_euler_steps': steps, 'euler_energy_ratio_curve': curve,
           'disconnected_counterexample': {'potential': disconnected_potential, 'energy': str(disconnected_energy), 'globally_constant': len(set(disconnected_potential)) == 1},
           'interpretation_plan_sha256': hashlib.sha256((base / 'x2/research-plan.json').read_bytes()).hexdigest(),
           'new_proposal_credit': 0, 'independent_reproduction': False,
           'boundary': 'Existing finite mathematical identities and explicit model counterexamples; no measured physical system or new thermodynamic law.'}
print(json.dumps(receipt, indent=2, sort_keys=True))
raise SystemExit(0 if all(r['passed'] for r in symbolic + arrays) and negative_energy == Fraction(-1, 2) and disconnected_energy == 0 and steps[-1]['energy_after'] == '2' else 1)
