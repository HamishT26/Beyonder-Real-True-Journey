"""Bounded family interface; record computations only."""
import sys
from ghc_family_workflow_core import cli

if __name__ == "__main__":
    sys.exit(cli({'manifest_diff', 'file_budget', 'staged_allowlist', 'path_scope'}))
