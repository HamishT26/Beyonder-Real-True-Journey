"""Bounded family interface; record computations only."""
import sys
from ghc_family_workflow_core import cli

if __name__ == "__main__":
    sys.exit(cli({'method_transition', 'tool_select', 'dependency_closure', 'witness_accounting'}))
