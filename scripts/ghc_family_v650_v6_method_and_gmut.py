#!/usr/bin/env python3
"""Family-current bounded v650-v6 runner: ghc_family_v650_v6_method_and_gmut.py."""

from ghc_family_v650_v6_runner import wrapper_main

PROPOSAL_IDS = ['V6506-P01', 'V6506-P02', 'V6506-P03', 'V6506-P04']

if __name__ == "__main__":
    raise SystemExit(wrapper_main("ghc_family_v650_v6_method_and_gmut.py", PROPOSAL_IDS))
