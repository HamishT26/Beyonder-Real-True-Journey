"""Finite interval topology on synthetic ticks using portion."""
import portion as P
from ghc_family_temporal_reports import Refusal, cli, exact_keys, finite_json, tick

FAMILIES = {'interval_membership', 'interval_intersection', 'interval_union', 'interval_difference'}


def atom(value):
    if type(value) is not list or len(value) != 4:
        raise Refusal('invalid_interval')
    lc, lo, hi, rc = value
    if type(lc) is not bool or type(rc) is not bool:
        raise Refusal('invalid_endpoint_closure')
    tick(lo)
    tick(hi)
    if lo > hi:
        raise Refusal('invalid_interval')
    maker = {(True, True): P.closed, (True, False): P.closedopen,
             (False, True): P.openclosed, (False, False): P.open}[(lc, rc)]
    return maker(lo, hi)


def interval_set(values):
    if type(values) is not list or len(values) > 64:
        raise Refusal('interval_budget')
    result = P.empty()
    for value in values:
        result = result | atom(value)
    return result


def run(family, data):
    try:
        finite_json(data)
        if type(family) is not str:
            raise Refusal('unknown_family')
        if family == 'interval_membership':
            exact_keys(data, ['interval', 'point'])
            return tick(data['point']) in atom(data['interval'])
        if family not in FAMILIES:
            raise Refusal('unknown_family')
        exact_keys(data, ['a', 'b'])
        a, b = interval_set(data['a']), interval_set(data['b'])
        if family == 'interval_intersection':
            value = a & b
        elif family == 'interval_union':
            value = a | b
        else:
            value = a - b
        return [list(row) for row in P.to_data(value)]
    except Refusal as exc:
        return {'error': str(exc)}


if __name__ == '__main__':
    raise SystemExit(cli(run, FAMILIES))
