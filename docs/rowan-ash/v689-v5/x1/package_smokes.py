"""Exercise the three pinned additions with fixed positive and adverse inputs."""
import importlib.metadata as metadata
import json
import os

os.environ['NUMEXPR_MAX_THREADS'] = '2'
os.environ['NUMEXPR_NUM_THREADS'] = '2'
os.environ['OMP_NUM_THREADS'] = '2'
import numpy as np
import symengine as se
import opt_einsum as oe
import numexpr as ne

rows = []
x = se.Symbol('x')
symbolic = str(se.expand((x + 1) ** 2 - x * x - 2 * x - 1))
rows.append({'package': 'symengine', 'kind': 'positive', 'observed': symbolic, 'expected': '0', 'passed': symbolic == '0'})
try:
    se.sympify('x + *')
except Exception as error:
    rows.append({'package': 'symengine', 'kind': 'adverse', 'observed_exception': type(error).__name__, 'passed': True, 'subject_success_credit': 0})
else:
    rows.append({'package': 'symengine', 'kind': 'adverse', 'passed': False, 'subject_success_credit': 0})
a = np.array([[1, 2], [3, 4]], dtype=np.int64)
b = np.array([[2, 0], [0, 3]], dtype=np.int64)
product = oe.contract('ij,jk->ik', a, b, optimize='greedy').tolist()
rows.append({'package': 'opt_einsum', 'kind': 'positive', 'observed': product, 'expected': [[2, 6], [6, 12]], 'passed': product == [[2, 6], [6, 12]]})
try:
    oe.contract('ij,jk->ik', np.ones((2, 3)), np.ones((4, 2)), optimize='greedy')
except ValueError as error:
    rows.append({'package': 'opt_einsum', 'kind': 'adverse', 'observed_exception': type(error).__name__, 'passed': True, 'subject_success_credit': 0})
else:
    rows.append({'package': 'opt_einsum', 'kind': 'adverse', 'passed': False, 'subject_success_credit': 0})
w = np.array([1, 2, 3, 4], dtype=np.int64)
g = np.array([1, -2, 3, 0], dtype=np.int64)
energy = ne.evaluate('w*g*g', local_dict={'w': w, 'g': g}, global_dict={}, optimization='moderate').tolist()
rows.append({'package': 'numexpr', 'kind': 'positive', 'observed': energy, 'expected': [1, 8, 27, 0], 'passed': energy == [1, 8, 27, 0]})
try:
    ne.evaluate('g +', local_dict={'g': g}, global_dict={})
except (SyntaxError, ValueError) as error:
    rows.append({'package': 'numexpr', 'kind': 'adverse', 'observed_exception': type(error).__name__, 'passed': True, 'subject_success_credit': 0})
else:
    rows.append({'package': 'numexpr', 'kind': 'adverse', 'passed': False, 'subject_success_credit': 0})
receipt = {'versions': {name: metadata.version(name) for name in ['symengine', 'opt_einsum', 'numexpr', 'numpy']},
           'smokes': rows, 'passed': sum(row['passed'] for row in rows), 'numexpr_threads': ne.get_num_threads(),
           'arbitrary_external_expressions': False, 'independent_reproduction': False,
           'scope': 'Fixed synthetic API checks, not a performance benchmark or exhaustive security audit.'}
print(json.dumps(receipt, indent=2, sort_keys=True, allow_nan=False))
raise SystemExit(0 if all(row['passed'] for row in rows) else 1)
