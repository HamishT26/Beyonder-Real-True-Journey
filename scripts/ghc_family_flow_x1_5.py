"""Finite x1 flow operations augment_once, max_value."""
from scripts.ghc_family_flow_common import cli
from scripts.ghc_family_flow_x1 import evaluate

if __name__ == '__main__':
    raise SystemExit(cli(evaluate, ('augment_once', 'max_value')))
