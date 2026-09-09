"""Run explicit local token_cost, fair_quota requests."""
from ghc_family_capacity_core import cli
from ghc_family_capacity_core import evaluate
if __name__ == '__main__':
    cli(['token_cost', 'fair_quota'], evaluate)
