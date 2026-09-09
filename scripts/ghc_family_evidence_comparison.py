"""Run explicit local record_projection, paired_gain requests."""
from ghc_family_capacity_core import cli
from ghc_family_inference_core import evaluate
if __name__ == '__main__':
    cli(['record_projection', 'paired_gain'], evaluate)
