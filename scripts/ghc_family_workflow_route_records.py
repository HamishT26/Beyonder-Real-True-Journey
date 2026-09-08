"""Bounded family interface; record computations only."""
import sys
from ghc_family_workflow_core import cli

if __name__ == "__main__":
    sys.exit(cli({'phase_advance', 'delivery_reduce', 'route_cursor', 'cycle_assignments'}))
