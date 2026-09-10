"""Finite x2 flow operations min_cut, duality."""
from scripts.ghc_family_flow_common import cli
from scripts.ghc_family_flow_x2 import evaluate

if __name__ == '__main__':
    raise SystemExit(cli(evaluate, ('min_cut', 'duality')))
