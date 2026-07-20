#!/usr/bin/env python3
"""Family-current bounded v650-v6 runner: ghc_family_v650_v6_portfolios.py."""

from ghc_family_v650_v6_runner import wrapper_main

PROPOSAL_IDS = ['V6506-P05', 'V6506-P06', 'V6506-P07', 'V6506-P08', 'V6506-P09', 'V6506-P10']

if __name__ == "__main__":
    raise SystemExit(wrapper_main("ghc_family_v650_v6_portfolios.py", PROPOSAL_IDS))
