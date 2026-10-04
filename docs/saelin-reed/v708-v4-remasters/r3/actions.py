"""Exact finite Euler-Lagrange contracts; normalized toy mechanics only."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys
import time

VARS = ('q', 'r', 'l', 'v', 'w', 'u', 'a', 'b', 'c', 't', 'g', 'p', 's')
INDEX = {v: i for i, v in enumerate(VARS)}
ZERO = (0,) * len(VARS)
PAIRS = (('q', 'v', 'a'), ('r', 'w', 'b'), ('l', 'u', 'c'))


def clean(poly):
    return {k: v for k, v in poly.items() if v}


def P(terms):
    out = {}
    for name, coefficient in terms.items():
        exponents = list(ZERO)
        if name:
            for atom in name.split('*'):
                pieces = atom.split('^')
                if len(pieces) > 2 or pieces[0] not in INDEX:
                    raise ValueError('Invalid declared monomial')
                degree = int(pieces[1]) if len(pieces) == 2 else 1
                if not 0 <= degree <= 12:
                    raise ValueError('Degree outside finite profile')
                exponents[INDEX[pieces[0]]] += degree
        key = tuple(exponents)
        out[key] = out.get(key, F(0)) + F(coefficient)
    return clean(out)


def add(*polys):
    out = {}
    for poly in polys:
        for k, v in poly.items():
            out[k] = out.get(k, F(0)) + v
    return clean(out)


def scale(poly, factor):
    return clean({k: v * F(factor) for k, v in poly.items()})


def mul(left, right):
    if len(left) * len(right) > 10000:
        raise ValueError('Finite multiplication budget')
    out = {}
    for a, x in left.items():
        for b, y in right.items():
            key = tuple(i + j for i, j in zip(a, b))
            out[key] = out.get(key, F(0)) + x * y
    return clean(out)


def diff(poly, variable):
    i = INDEX[variable]
    out = {}
    for k, v in poly.items():
        if k[i]:
            target = list(k)
            target[i] -= 1
            out[tuple(target)] = v * k[i]
    return clean(out)


def dt(poly):
    pieces = [diff(poly, 't')]
    for q, v, a in PAIRS:
        pieces.extend((mul(P({v: 1}), diff(poly, q)),
                       mul(P({a: 1}), diff(poly, v))))
    return add(*pieces)


def residual(action, q, v, rayleigh):
    return add(dt(diff(action, v)), scale(diff(action, q), -1), diff(rayleigh, v))


def substitute(poly, values):
    out = {}
    for k, coefficient in poly.items():
        target = list(k)
        for variable, value in values.items():
            i = INDEX[variable]
            coefficient *= F(value) ** target[i]
            target[i] = 0
        key = tuple(target)
        out[key] = out.get(key, F(0)) + coefficient
    return clean(out)


def display(poly):
    out = {}
    for key, value in sorted(poly.items()):
        name = '*'.join(v if degree == 1 else f'{v}^{degree}'
                        for v, degree in zip(VARS, key) if degree) or '1'
        out[name] = str(value)
    return out


MODELS = [
    ('A01', 'Canonical oscillator', {'v^2': '1/2', 'q^2': '-1/2'},
     {'q': {'a': 1, 'q': 1}}, {}, 'Normalized positive kinetic and harmonic coefficients.'),
    ('A02', 'Mixed kinetic form', {'v^2': 1, 'v*w': 1, 'w^2': '3/2', 'q^2': '-1/2', 'r^2': -1},
     {'q': {'a': 2, 'b': 1, 'q': 1}, 'r': {'a': 1, 'b': 3, 'r': 2}}, {},
     'A symmetric positive kinetic matrix; coordinates remain coupled.'),
    ('A03', 'Coordinate-dependent mass', {'v^2': '1/2', 'q^2*v^2': '1/2', 'q^2': '-1/2'},
     {'q': {'a': 1, 'q^2*a': 1, 'q*v^2': 1, 'q': 1}}, {},
     'The derivative of the kinetic coefficient contributes a velocity-square term.'),
    ('A04', 'Quartic interaction', {'v^2': '1/2', 'w^2': '1/2', 'q^2*r^2': '-1/2', 'q^4': '-1/4', 'r^4': '-1/4'},
     {'q': {'a': 1, 'q*r^2': 1, 'q^3': 1}, 'r': {'b': 1, 'r*q^2': 1, 'r^3': 1}}, {},
     'Two coupled coordinates with a declared nonnegative quartic potential.'),
    ('A05', 'Time-dependent mass', {'t*v^2': '1/2', 'q^2': '-1/2'},
     {'q': {'t*a': 1, 'v': 1, 'q': 1}}, {}, 'Use t>0 for a nonsingular positive kinetic coefficient.'),
    ('A06', 'External forcing', {'v^2': '1/2', 'q^2': '-1/2', 't*q': 1},
     {'q': {'a': 1, 'q': 1, 't': -1}}, {}, 'A prescribed source; total closed-system energy is not claimed.'),
    ('A07', 'Gyroscopic coupling', {'v^2': '1/2', 'w^2': '1/2', 'q*w': '1/2', 'r*v': '-1/2'},
     {'q': {'a': 1, 'w': -1}, 'r': {'b': 1, 'v': 1}}, {}, 'Antisymmetric velocity coupling; not friction.'),
    ('A08', 'Total derivative', {'v^2': '1/2', 'q^2': '1/2', 't*q*v': 2},
     {'q': {'a': 1, 'q': 1}}, {}, 'Oscillator plus d(t*q^2)/dt; fixed endpoints are required.'),
    ('A09', 'Cyclic coordinate', {'v^2': '1/2', 'w^2': '1/2', 'q^2*w^2': '1/2'},
     {'q': {'a': 1, 'q*w^2': -1}, 'r': {'b': 1, 'q^2*b': 1, 'q*v*w': 2}}, {},
     'r is cyclic; its momentum is (1+q^2)*w, not simply w.'),
    ('A10', 'Translational pair symmetry', {'v^2': '1/2', 'w^2': '1/2', 'q^2': '-1/2', 'q*r': 1, 'r^2': '-1/2'},
     {'q': {'a': 1, 'q': 1, 'r': -1}, 'r': {'b': 1, 'r': 1, 'q': -1}}, {},
     'Potential depends on coordinate difference; the momentum sum is conserved on shell.'),
    ('A11', 'Anchored lattice gradient', {'v^2': '1/2', 'w^2': '1/2', 'q^2': -1, 'q*r': 1, 'r^2': -1},
     {'q': {'a': 1, 'q': 2, 'r': -1}, 'r': {'b': 1, 'r': 2, 'q': -1}}, {},
     'Two sites with zero endpoint values; unlike the free pair, translation is broken.'),
    ('A12', 'Holonomic multiplier', {'v^2': '1/2', 'w^2': '1/2', 'l*q^2': 1, 'l*r^2': 1, 'l': -1},
     {'q': {'a': 1, 'l*q': -2}, 'r': {'b': 1, 'l*r': -2}, 'l': {'': 1, 'q^2': -1, 'r^2': -1}}, {},
     'Constraint equation is required; this is a differential-algebraic model, not an unconstrained ODE.'),
    ('A13', 'Rayleigh dissipation', {'v^2': '1/2', 'w^2': '1/2', 'q^2': '-1/2', 'r^2': '-1/2'},
     {'q': {'a': 1, 'g*v': 1, 'q': 1}, 'r': {'b': 1, 'g*w': 1, 'r': 1}},
     {'g*v^2': '1/2', 'g*w^2': '1/2'}, 'g>=0; dissipative forces are added explicitly, not derived from the conservative action alone.'),
    ('A14', 'Linear coordinate pullback', {'v^2': 1, 'w^2': 1, 'q^2': -1, 'r^2': -1},
     {'q': {'a': 2, 'q': 2}, 'r': {'b': 2, 'r': 2}}, {},
     'x=q+r, y=q-r; an invertible, non-normalized change transforms both kinetic and potential terms.'),
    ('A15', 'Sum-only parameter observation', {'v^2': '1/2', 'p*q^2': '-1/2', 's*q^2': '-1/2'},
     {'q': {'a': 1, 'p*q': 1, 's*q': 1}}, {},
     'The residual identifies p+s under this model, not p and s separately.'),
]


def run():
    checks = []
    records = []

    def check(name, actual, expected, kind='positive'):
        checks.append({'name': name, 'kind': kind, 'passed': actual == expected,
                       'actual': actual, 'expected': expected})

    check('rational cancellation', display(add(P({'q': '1/3'}), P({'q': '-1/3'}))), {})
    check('monomial derivative', display(diff(P({'q^3*r': '2/3'}), 'q')), {'q^2*r': '2'})
    check('product expansion', display(mul(P({'q': 1, 'r': 1}), P({'q': 1, 'r': -1}))), display(P({'q^2': 1, 'r^2': -1})))
    check('total derivative clock', display(dt(P({'t*q': 1}))), display(P({'q': 1, 't*v': 1})))
    check('fixed parameters', display(dt(P({'g*p*s': 1}))), {})
    check('coefficient versus sample equality', P({'t^3': 1, 't': -1}) == {}, False, 'negative_control')

    for ident, name, action_terms, expected, rayleigh_terms, limitation in MODELS:
        before = len(checks)
        action, rayleigh = P(action_terms), P(rayleigh_terms)
        eq = {}
        energy = scale(action, -1)
        velocity_equations = {}
        dissipation = {}
        for q, v, _ in PAIRS:
            if q not in expected:
                continue
            eq[q] = residual(action, q, v, rayleigh)
            check(ident + ':' + q, display(eq[q]), display(P(expected[q])))
            energy = add(energy, mul(P({v: 1}), diff(action, v)))
            velocity_equations = add(velocity_equations, mul(P({v: 1}), eq[q]))
            dissipation = add(dissipation, mul(P({v: 1}), diff(rayleigh, v)))
        balance = add(dt(energy), diff(action, 't'), dissipation, scale(velocity_equations, -1))
        check(ident + ':energy identity', display(balance), {}, 'same_engine_consistency')
        first = next(iter(expected))
        corrupted = add(eq[first], P({'': 1}))
        check(ident + ':reject constant corruption', corrupted == P(expected[first]), False, 'negative_control')
        records.append({'id': ident, 'name': name, 'action': display(action),
                        'rayleigh': display(rayleigh), 'residuals': {q: display(e) for q, e in eq.items()},
                        'energy': display(energy), 'checks': len(checks) - before,
                        'limitation': limitation, 'empirical_credit': 0})

    by_id = {m[0]: m for m in MODELS}
    check('A08:explicit boundary derivative', display(add(P(by_id['A01'][2]), dt(P({'t*q^2': 1})))), display(P(by_id['A08'][2])))
    pair = by_id['A10']
    pair_l = P(pair[2])
    check('A10:momentum sum literal', display(add(residual(pair_l, 'q', 'v', {}), residual(pair_l, 'r', 'w', {}))), display(P({'a': 1, 'b': 1})))
    source_l = add(scale(mul(P({'v': 1, 'w': 1}), P({'v': 1, 'w': 1})), F(1, 2)),
                   scale(mul(P({'v': 1, 'w': -1}), P({'v': 1, 'w': -1})), F(1, 2)),
                   scale(mul(P({'q': 1, 'r': 1}), P({'q': 1, 'r': 1})), F(-1, 2)),
                   scale(mul(P({'q': 1, 'r': -1}), P({'q': 1, 'r': -1})), F(-1, 2)))
    check('A14:pullback algebra', display(source_l), display(P(by_id['A14'][2])))
    observed = residual(P(by_id['A15'][2]), 'q', 'v', {})
    check('A15:distinct parameter alias', display(substitute(observed, {'p': 1, 's': 2})), display(substitute(observed, {'p': 0, 's': 3})))
    check('A15:different sum detected', substitute(observed, {'p': 1, 's': 2}) == substitute(observed, {'p': 1, 's': 3}), False, 'negative_control')
    return {'schema': 'ghc.saelin.variational-x1.v1', 'models': records, 'checks': checks,
            'model_count': len(records), 'check_count': len(checks),
            'passed': sum(r['passed'] for r in checks), 'failed': sum(not r['passed'] for r in checks),
            'independent_executor': False, 'empirical_datasets': 0,
            'dimension_convention': 'normalized dimensionless toy mechanics',
            'physical_theories_established': 0, 'process_peak_rss': None}


def main():
    root = Path(__file__).resolve().parent
    output = root / 'x1-results.json'
    if output.exists():
        raise SystemExit('Receipt exists; inspect it instead of replaying this stage.')
    source = {p.name: {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
              for p in (root / 'PLAN.md', root / 'actions.py')}
    began = time.perf_counter()
    result = run()
    result['elapsed_seconds'] = time.perf_counter() - began
    result['sources'] = source
    result['python_version'] = sys.version.split()[0]
    with output.open('x', encoding='utf-8', newline='\n') as handle:
        json.dump(result, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write('\n')
    print(json.dumps({k: result[k] for k in ('model_count', 'check_count', 'passed', 'failed', 'elapsed_seconds', 'python_version')}))
    return bool(result['failed'])


if __name__ == '__main__':
    raise SystemExit(main())
