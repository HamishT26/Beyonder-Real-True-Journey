"""Run explicit local beta_update, lr_path requests."""
from ghc_family_capacity_core import cli
from ghc_family_inference_core import evaluate
if __name__ == '__main__':
    cli(['beta_update', 'lr_path'], evaluate)
