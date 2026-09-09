"""Run explicit local ffd, context_batches requests."""
from ghc_family_capacity_core import cli
from ghc_family_capacity_core import evaluate
if __name__ == '__main__':
    cli(['ffd', 'context_batches'], evaluate)
