#!/usr/bin/env python3
"""Family-current bounded v650-v6 runner: ghc_family_v650_v6_accessibility.py."""

from ghc_family_v650_v6_runner import wrapper_main

PROPOSAL_IDS = ['V6506-P14', 'V6506-P15']

if __name__ == "__main__":
    raise SystemExit(wrapper_main("ghc_family_v650_v6_accessibility.py", PROPOSAL_IDS))
