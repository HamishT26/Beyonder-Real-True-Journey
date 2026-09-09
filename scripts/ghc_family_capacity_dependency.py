"""Run explicit local critical_path, coverage requests."""
from ghc_family_capacity_core import cli
from ghc_family_capacity_core import evaluate
if __name__ == '__main__':
    cli(['critical_path', 'coverage'], evaluate)
