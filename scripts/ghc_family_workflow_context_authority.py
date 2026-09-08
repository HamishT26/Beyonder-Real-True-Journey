"""Bounded family interface; record computations only."""
import sys
from ghc_family_workflow_core import cli

if __name__ == "__main__":
    sys.exit(cli({'card_selection', 'deck_parents', 'overlay_fold', 'evidence_gate'}))
