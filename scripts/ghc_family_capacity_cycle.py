"""Run explicit local cycle_slice, mix_cost requests."""
from ghc_family_capacity_core import cli
from ghc_family_capacity_core import evaluate
if __name__ == '__main__':
    cli(['cycle_slice', 'mix_cost'], evaluate)
