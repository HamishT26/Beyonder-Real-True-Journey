"""Finite x2 flow operations lower_feasible, min_cost."""
from scripts.ghc_family_flow_common import cli
from scripts.ghc_family_flow_x2 import evaluate

if __name__ == '__main__':
    raise SystemExit(cli(evaluate, ('lower_feasible', 'min_cost')))
