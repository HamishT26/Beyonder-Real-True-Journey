"""Bounded family interface; record computations only."""
import sys
from ghc_family_model_core import cli

if __name__ == "__main__":
    sys.exit(cli({'markov_step', 'stationary_distribution', 'detailed_balance', 'stochastic_matrix'}))
