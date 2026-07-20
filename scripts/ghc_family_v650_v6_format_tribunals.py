#!/usr/bin/env python3
"""Family-current bounded v650-v6 runner: ghc_family_v650_v6_format_tribunals.py."""

from ghc_family_v650_v6_runner import wrapper_main

PROPOSAL_IDS = ['V6506-P11', 'V6506-P12', 'V6506-P13', 'V6506-P18', 'V6506-P19']

if __name__ == "__main__":
    raise SystemExit(wrapper_main("ghc_family_v650_v6_format_tribunals.py", PROPOSAL_IDS))
