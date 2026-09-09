"""Run explicit local channel_joint, bayes_risk requests."""
from ghc_family_capacity_core import cli
from ghc_family_inference_core import evaluate
if __name__ == '__main__':
    cli(['channel_joint', 'bayes_risk'], evaluate)
