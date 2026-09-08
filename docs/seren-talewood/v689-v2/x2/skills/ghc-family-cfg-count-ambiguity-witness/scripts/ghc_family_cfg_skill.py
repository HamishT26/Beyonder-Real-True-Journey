"""Bounded synthetic CFG operations; JSON on stdin only."""
from ghc_family_cfg_core import cli

OPERATIONS = ('cfg_bounded_derivation_counts', 'cfg_ambiguity_witness')

if __name__ == '__main__':
    raise SystemExit(cli(OPERATIONS))
