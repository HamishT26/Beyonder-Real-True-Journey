"""Bounded synthetic CFG operations; JSON on stdin only."""
from ghc_family_cfg_core import cli

OPERATIONS = ('cfg_epsilon_variants', 'cfg_derive_step', 'cfg_derivation_validate', 'cfg_bounded_language')

if __name__ == '__main__':
    raise SystemExit(cli(OPERATIONS))
