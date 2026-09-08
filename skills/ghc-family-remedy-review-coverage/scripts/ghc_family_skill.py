"""Run only this skill's declared operation pair."""
import sys
from ghc_family_model_core import cli

if __name__ == "__main__":
    sys.exit(cli({'remedy_queue', 'review_coverage'}))
