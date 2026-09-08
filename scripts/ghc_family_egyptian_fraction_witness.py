"""Bounded family interface; record computations only."""
import sys
from ghc_family_model_core import cli

if __name__ == "__main__":
    sys.exit(cli({'egyptian_fraction_verify', 'egyptian_fraction_search'}))
