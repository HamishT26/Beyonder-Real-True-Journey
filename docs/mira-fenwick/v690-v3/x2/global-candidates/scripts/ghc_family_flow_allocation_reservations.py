"""Bounded flow capability: ghc-family-flow-allocation-reservations."""
from scripts.ghc_family_flow_common import cli
from scripts.ghc_family_flow_x1 import evaluate as first, REQUIRED
from scripts.ghc_family_flow_x2 import evaluate as second

def evaluate(request):
    return first(request) if request.get('op') in REQUIRED else second(request)

if __name__ == '__main__':
    raise SystemExit(cli(evaluate, ('assignment', 'policy_gate', 'summary', 'reservation')))
