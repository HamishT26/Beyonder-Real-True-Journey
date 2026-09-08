"""Bounded family interface; record computations only."""
import sys
from ghc_family_workflow_core import cli

if __name__ == "__main__":
    sys.exit(cli({'budget_check', 'context_window', 'quota_partition', 'source_selection'}))
