"""Fifteen distinct finite synthetic measurement models; exact arithmetic only.

No network, external records, randomness, installations or consequential actions.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
import copy
import hashlib
import json


def q(x):
    if type(x) not in (int, str, F):
        raise ValueError('exact integer or rational string required; booleans/floats refused')
    return F(x)


def vec(x):
    if not isinstance(x, list) or not 1 <= len(x) <= 16:
        raise ValueError('bounded nonempty vector required')
    return [q(v) for v in x]


def matrix(x):
    if not isinstance(x, list) or not 1 <= len(x) <= 8:
        raise ValueError('bounded matrix required')
    a = [vec(row) for row in x]
    if len({len(r) for r in a}) != 1:
        raise ValueError('ragged matrix')
    return a


def mean(x):
    return sum(x, F(0)) / len(x)


def det2(a):
    if len(a) != 2 or any(len(r) != 2 for r in a):
        raise ValueError('two by two matrix required')
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def rank(a):
    a = [row[:] for row in a]
    r = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][col]
        a[r] = [v / scale for v in a[r]]
        for i in range(len(a)):
            if i != r:
                scale = a[i][col]
                a[i] = [v - scale * w for v, w in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def mv(a, x):
    if any(len(row) != len(x) for row in a):
        raise ValueError('matrix-vector dimension mismatch')
    return [sum((v * w for v, w in zip(row, x)), F(0)) for row in a]


def affine(x, y):
    if len(x) != len(y) or len(x) < 2:
        raise ValueError('paired observations required')
    xx, yy = mean(x), mean(y)
    info = sum((v - xx) ** 2 for v in x)
    if info == 0:
        raise ValueError('slope not identified')
    slope = sum((v - xx) * (w - yy) for v, w in zip(x, y)) / info
    return yy - slope * xx, slope, info


def design(p):
    def info(v):
        x = vec(v)
        return [[F(len(x)), sum(x)], [sum(x), sum(v * v for v in x)]]
    a, b, c = [info(p[k]) for k in ('balanced', 'confounded', 'spread')]
    return dict(balanced_det=det2(a), confounded_det=det2(b), spread_det=det2(c),
                balanced_offdiag=a[0][1], balanced_rank=rank(a), confounded_rank=rank(b))


def identify(p):
    a, b = matrix(p['A']), matrix(p['augmented'])
    t1, t2 = vec(p['theta1']), vec(p['theta2'])
    y1, y2 = mv(a, t1), mv(a, t2)
    return dict(rank=rank(a), augmented_rank=rank(b), null_image=mv(a, vec(p['null'])),
                shared_observation=y1, augmented_det=det2(b),
                distinct_equivalent_parameters=t1 != t2 and y1 == y2)


def measurement(p):
    true, latent, error, bias = vec(p['true']), vec(p['latent']), vec(p['error']), q(p['bias'])
    if len(latent) != len(error):
        raise ValueError('predictor error length mismatch')
    reported = [v + bias for v in true]
    measured = [v + e for v, e in zip(latent, error)]
    intercept, slope, _ = affine(true, reported)
    return dict(mean_bias=mean([v - t for v, t in zip(reported, true)]),
                corrected=[v - bias for v in reported], latent_slope=affine(latent, latent)[1],
                measured_slope=affine(measured, latent)[1],
                response_intercept=intercept, response_slope=slope)


def missing(p):
    y, pi = vec(p['population']), vec(p['inclusion'])
    mask = p['mask']
    if len(mask) != len(y) or len(pi) != len(y) or not all(type(v) is bool for v in mask):
        raise ValueError('explicit Boolean observation mask and matching probabilities required')
    observed = [v for v, keep in zip(y, mask) if keep]
    if not observed or any(v <= 0 or v > 1 for v in pi):
        raise ValueError('observed values and positive inclusion probabilities required')
    observed_pattern_probability = F(1)
    for flag, prob in zip(mask, pi):
        observed_pattern_probability *= prob if flag else 1 - prob
    if observed_pattern_probability == 0:
        raise ValueError('observed mask has zero probability under declared inclusion design')
    lo, hi = p['missing_range']
    if type(lo) is not int or type(hi) is not int or not 0 <= hi - lo <= 5:
        raise ValueError('bounded integer completion grid required')
    unobserved = len(y) - len(observed)
    completions = [(sum(observed) + sum(c)) / len(y) for c in product(range(lo, hi + 1), repeat=unobserved)]
    expected = F(0)
    for flags in product((False, True), repeat=len(y)):
        mass = F(1)
        for flag, prob in zip(flags, pi):
            mass *= prob if flag else 1 - prob
        estimate = sum((value / prob for value, prob, flag in zip(y, pi, flags) if flag), F(0)) / len(y)
        expected += mass * estimate
    return dict(full_mean=mean(y), observed_mean=mean(observed), lower_mean=min(completions),
                upper_mean=max(completions), HT_expected=expected, completion_count=len(completions))


def nuisance(p):
    t, y, shift = vec(p['t']), vec(p['y']), q(p['shift'])
    a, slope, info = affine(t, y)
    forced = sum(v * w for v, w in zip(t, y)) / sum(v * v for v in t)
    return dict(profile_slope=slope, forced_zero_intercept_slope=forced, profile_intercept=a,
                shifted_slope=affine(t, [v + shift for v in y])[1],
                residual_sum=sum((v - a - slope * x for x, v in zip(t, y)), F(0)),
                centered_information=info)


def randomization(p):
    y, size, chosen = vec(p['values']), p['group_size'], p['observed_group']
    if type(size) is not int or not 0 < size < len(y) or len(y) > 8:
        raise ValueError('bounded nonempty groups required')
    if len(chosen) != size or len(set(chosen)) != size or any(type(i) is not int or not 0 <= i < len(y) for i in chosen):
        raise ValueError('invalid observed assignment')
    groups = list(combinations(range(len(y)), size))
    def difference(values, group):
        return mean([v for i, v in enumerate(values) if i in group]) - mean([v for i, v in enumerate(values) if i not in group])
    stats = [difference(y, g) for g in groups]
    observed = abs(difference(y, chosen))
    tails = sum(abs(v) >= observed for v in stats)
    constant = [F(0)] * len(y)
    constant_tail = sum(abs(difference(constant, g)) >= 0 for g in groups)
    return dict(assignments=len(groups), absolute_statistic=observed, tail_assignments=tails,
                two_sided_tail=F(tails, len(groups)), constant_data_tail=F(constant_tail, len(groups)),
                null_statistic_mean=mean(stats))


def intervals(p):
    a, b = vec(p['a']), vec(p['b'])
    if len(a) != 2 or len(b) != 2 or a[0] > a[1] or b[0] > b[1]:
        raise ValueError('ordered interval endpoints required')
    corners = sorted(x * y for x in a for y in b)
    same = [x - x for x in a]
    zero = [x * F(0) for x in a]
    return dict(product=[min(corners), max(corners)], sum=[a[0] + b[0], a[1] + b[1]],
                same_variable_difference=[min(same), max(same)],
                independent_difference=[a[0] - a[1], a[1] - a[0]],
                corner_products=corners, zero_product=[min(zero), max(zero)])


def sensitivity(p):
    point, h = vec(p['point']), q(p['step'])
    if len(point) != 2 or h <= 0:
        raise ValueError('two parameters and positive step required')
    def observable(x):
        return [x[0] + x[1], x[0] * x[1]]
    def jacobian(point, h):
        columns = []
        for i in range(2):
            plus, minus = point[:], point[:]
            plus[i] += h
            minus[i] -= h
            columns.append([(a - b) / (2 * h) for a, b in zip(observable(plus), observable(minus))])
        return [list(row) for row in zip(*columns)]
    j = jacobian(point, h)
    swapped = list(reversed(point))
    return dict(jacobian=j, determinant=det2(j), equal_point_determinant=det2(jacobian([point[0]] * 2, h)),
                step_invariance=j == jacobian(point, 2 * h), swapped_observation=observable(swapped),
                global_counterexample=swapped != point and observable(swapped) == observable(point))


def likelihood(p):
    n, k, p0, p1, prior = p['n'], p['k'], q(p['p0']), q(p['p1']), q(p['prior_odds'])
    if type(n) is not int or type(k) is not int or not 0 <= k <= n <= 16 or not 0 <= p0 <= 1 or not 0 <= p1 <= 1 or prior < 0:
        raise ValueError('invalid finite binomial contract')
    def mass(k, prob):
        return comb(n, k) * prob ** k * (1 - prob) ** (n - k)
    def ratio(a, b):
        return None if a == b == 0 else ('positive_over_zero' if b == 0 else a / b)
    l0, l1 = mass(k, p0), mass(k, p1)
    lr = ratio(l1, l0)
    if not isinstance(lr, F):
        raise ValueError('posterior calculation needs finite likelihood ratio')
    odds = prior * lr
    return dict(likelihood_ratio=lr, null_mass=l0, alternative_mass=l1,
                posterior_probability=odds / (1 + odds), zero_success_ratio=ratio(mass(0, p1), mass(0, p0)),
                both_impossible_ratio=ratio(mass(k, F(0)), mass(k, F(0))))


def brier(pred, labels):
    p, y = vec(pred), vec(labels)
    if len(p) != len(y) or any(not 0 <= v <= 1 for v in p) or any(v not in (0, 1) for v in y):
        raise ValueError('paired probabilities and binary labels required')
    return mean([(v - w) ** 2 for v, w in zip(p, y)])


def heldout(p):
    train, test = p['train_ids'], p['test_ids']
    if not train or not test or set(train) & set(test) or len(set(train)) != len(train) or len(set(test)) != len(test):
        raise ValueError('disjoint nonempty frozen split required')
    if len(train) != len(p['train_y']) or len(test) != len(p['test_y']):
        raise ValueError('split length mismatch')
    training = {name: brier(p[name + '_train'], p['train_y']) for name in ('A', 'B')}
    selected = min(training, key=lambda x: (training[x], x))
    testing = {name: brier(p[name + '_test'], p['test_y']) for name in ('A', 'B')}
    leaked = min(testing, key=lambda x: (testing[x], x))
    return dict(selected=selected, train_loss=training[selected], heldout_loss=testing[selected],
                B_heldout_loss=testing['B'], leaked_selection=leaked, heldout_used_for_selection=False)


def multiplicity(p):
    m, prob, alpha = p['m'], q(p['individual_tail']), q(p['family_alpha'])
    if type(m) is not int or not 1 <= m <= 8 or not 0 <= prob <= 1 or not 0 < alpha < 1:
        raise ValueError('bounded family and probabilities required')
    union = total = F(0)
    states = list(product((0, 1), repeat=m))
    for state in states:
        mass = prob ** sum(state) * (1 - prob) ** (m - sum(state))
        total += mass
        if any(state):
            union += mass
    correlated = sum((prob if common else F(0)) for common in (0, 1))
    return dict(independent_union=union, union_bound=min(F(1), m * prob),
                bonferroni_threshold=alpha / m, perfectly_correlated_union=correlated,
                enumerated_mass=total, outcomes=len(states))


def shift(p):
    source, target, risks = vec(p['p']), vec(p['q']), vec(p['risk'])
    if len(source) != len(target) or len(risks) != len(source) or sum(source) != 1 or sum(target) != 1:
        raise ValueError('matching probability mixtures required')
    if any(v < 0 for v in source + target) or any(not 0 <= v <= 1 for v in risks):
        raise ValueError('invalid mixture or bounded risk')
    if any(a == 0 and b > 0 for a, b in zip(source, target)):
        raise ValueError('target mass outside source support')
    weights = [b / a if a else F(0) for a, b in zip(source, target)]
    old = sum(a * r for a, r in zip(source, risks))
    new = sum(b * r for b, r in zip(target, risks))
    return dict(source_risk=old, target_risk=new, importance_weights=weights,
                reweighted_risk=sum(a * w * r for a, w, r in zip(source, weights, risks)),
                mean_importance_weight=sum(a * w for a, w in zip(source, weights)), risk_change=new - old)


def calibration(p):
    pred, y = vec(p['probabilities']), vec(p['labels'])
    loss = brier(pred, y)
    groups = {v: [label for value, label in zip(pred, y) if value == v] for v in set(pred)}
    base = mean(y)
    reliability = sum(F(len(labels), len(y)) * (prob - mean(labels)) ** 2 for prob, labels in groups.items())
    resolution = sum(F(len(labels), len(y)) * (mean(labels) - base) ** 2 for labels in groups.values())
    uncertainty = base * (1 - base)
    return dict(brier=loss, reliability=reliability, resolution=resolution, uncertainty=uncertainty,
                two_bin_brier=brier(p['two_bin_p'], p['two_bin_y']),
                decomposition_residual=loss - (uncertainty - resolution + reliability))


def canonical(value):
    def validate(x, depth=0):
        if depth > 16:
            raise ValueError('depth limit')
        if x is None or type(x) in (bool, int, str):
            return
        if type(x) is list:
            for v in x:
                validate(v, depth + 1)
            return
        if type(x) is dict and all(type(k) is str for k in x):
            for v in x.values():
                validate(v, depth + 1)
            return
        raise ValueError('restricted deterministic JSON domain; floating point refused')
    validate(value)
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')) + '\n').encode()


def reproducibility(p):
    original = copy.deepcopy(p)
    mapping, sequence = p['mapping'], p['sequence']
    encoded = canonical(mapping)
    text = p['known_text'].encode()
    digest = lambda b: hashlib.sha256(b).hexdigest()
    result = dict(known_sha256=digest(text),
                  object_reorder_equal=encoded == canonical(dict(reversed(list(mapping.items())))),
                  array_reorder_changes=canonical(sequence) != canonical(list(reversed(sequence))),
                  input_unchanged=p == original, source_revision_mismatch=digest(text) != digest(text + b'\n'),
                  canonical_text=encoded.decode())
    return result


def evidence(p):
    def classify(x, claim):
        if set(x) != {'synthetic', 'observed', 'authority', 'source_bound'} or any(type(v) is not bool for v in x.values()):
            raise ValueError('closed explicit Boolean evidence premises required')
        if not x['source_bound']:
            return 'open_gap'
        if claim == 'math':
            return 'completed' if x['synthetic'] else 'open_gap'
        if claim == 'empirical':
            return 'completed' if x['observed'] else 'open_gap'
        if claim == 'action':
            return 'completed' if x['authority'] else 'exact_gate'
        if claim == 'analogy':
            return 'represented'
        raise ValueError('unknown claim')
    result = dict(bounded_math=classify(p, 'math'), empirical=classify(p, 'empirical'),
                  real_action=classify(p, 'action'), analogy=classify(p, 'analogy'))
    try:
        classify(dict(p, observed='false'), 'empirical')
        refused = False
    except ValueError:
        refused = True
    result.update(string_boolean_refused=refused, unbound_source=classify(dict(p, source_bound=False), 'math'))
    return result


FUNCTIONS = [design, identify, measurement, missing, nuisance, randomization, intervals, sensitivity,
             likelihood, heldout, multiplicity, shift, calibration, reproducibility, evidence]


def mutant_value(index, p, actual):
    """Execute a deliberately wrong rule; this is not a corrected scientific model."""
    if index == 1: return len(matrix([[1, x] for x in p['confounded']])[0])
    if index == 2: return len(p['A'])
    if index == 3: return actual['latent_slope']
    if index == 4: return actual['observed_mean']
    if index == 5: return actual['forced_zero_intercept_slope']
    if index == 6:
        y = vec(p['values']);k = p['group_size'];threshold = actual['absolute_statistic']
        stats = [mean([v for i,v in enumerate(y) if i in g])-mean([v for i,v in enumerate(y) if i not in g]) for g in combinations(range(len(y)),k)]
        return F(sum(abs(s)>threshold for s in stats),len(stats))
    if index == 7:
        a,b=vec(p['a']),vec(p['b']);two=[a[0]*b[0],a[1]*b[1]];return [min(two),max(two)]
    if index == 8: return actual['jacobian'][0][0]*actual['jacobian'][1][1]
    if index == 9: return actual['likelihood_ratio']
    if index == 10: return actual['leaked_selection']
    if index == 11: return q(p['individual_tail'])
    if index == 12: return actual['source_risk']
    if index == 13: return actual['uncertainty']
    if index == 14: return canonical(sorted(p['sequence'])) != canonical(sorted(reversed(p['sequence'])))
    if index == 15: return 'completed' if bool('false') else 'open_gap'
    raise ValueError('unknown model')


def encode(value):
    if isinstance(value, F): return str(value)
    if isinstance(value, dict): return {k: encode(v) for k,v in value.items()}
    if isinstance(value, (list,tuple)): return [encode(v) for v in value]
    return value
