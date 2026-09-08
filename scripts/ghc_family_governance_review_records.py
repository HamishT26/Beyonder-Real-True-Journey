"""Bounded family interface; record computations only."""
import sys
from ghc_family_model_core import cli

if __name__ == "__main__":
    sys.exit(cli({'risk_register_projection', 'remedy_queue', 'review_coverage', 'consent_scope_check'}))
