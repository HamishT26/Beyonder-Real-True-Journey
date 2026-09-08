"""Run only this skill's declared operation pair."""
import sys
from ghc_family_workflow_core import cli

if __name__ == "__main__":
    sys.exit(cli({'manifest_diff', 'staged_allowlist'}))
