"""Run only this skill's declared operation pair."""
import sys
from ghc_family_model_core import cli

if __name__ == "__main__":
    sys.exit(cli({'time_reversal', 'probability_current'}))
