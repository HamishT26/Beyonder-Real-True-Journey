"""Bounded family interface; record computations only."""
import sys
from ghc_family_model_core import cli

if __name__ == "__main__":
    sys.exit(cli({'absorption_probabilities', 'distribution_distance', 'hitting_times', 'coupling_bounds'}))
