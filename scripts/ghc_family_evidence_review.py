"""Run explicit local consent_scope, appeal_cover requests."""
from ghc_family_capacity_core import cli
from ghc_family_inference_core import evaluate
if __name__ == '__main__':
    cli(['consent_scope', 'appeal_cover'], evaluate)
