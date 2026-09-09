"""Run explicit local fcfs, edd requests."""
from ghc_family_capacity_core import cli
from ghc_family_capacity_core import evaluate
if __name__ == '__main__':
    cli(['fcfs', 'edd'], evaluate)
