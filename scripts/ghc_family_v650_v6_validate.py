#!/usr/bin/env python3
"""Family-current bounded v650-v6 runner: ghc_family_v650_v6_validate.py."""

from ghc_family_v650_v6_runner import wrapper_main

PROPOSAL_IDS = ['V6506-P01', 'V6506-P02', 'V6506-P03', 'V6506-P04', 'V6506-P05', 'V6506-P06', 'V6506-P07', 'V6506-P08', 'V6506-P09', 'V6506-P10', 'V6506-P11', 'V6506-P12', 'V6506-P13', 'V6506-P14', 'V6506-P15', 'V6506-P16', 'V6506-P17', 'V6506-P18', 'V6506-P19', 'V6506-P20']

if __name__ == "__main__":
    raise SystemExit(wrapper_main("ghc_family_v650_v6_validate.py", PROPOSAL_IDS))
