"""Finite x2 flow operations assignment, policy_gate."""
from scripts.ghc_family_flow_common import cli
from scripts.ghc_family_flow_x2 import evaluate

if __name__ == '__main__':
    raise SystemExit(cli(evaluate, ('assignment', 'policy_gate')))
