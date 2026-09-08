"""Bounded family interface; record computations only."""
import sys
from ghc_family_model_core import cli

if __name__ == "__main__":
    sys.exit(cli({'relative_entropy', 'time_reversal', 'entropy_production', 'entropy', 'probability_current', 'coarse_grain'}))
