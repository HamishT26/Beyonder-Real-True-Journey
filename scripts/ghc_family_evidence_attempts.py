"""Run explicit local checkpoint, retry_budget requests."""
from ghc_family_capacity_core import cli
from ghc_family_inference_core import evaluate
if __name__ == '__main__':
    cli(['checkpoint', 'retry_budget'], evaluate)
