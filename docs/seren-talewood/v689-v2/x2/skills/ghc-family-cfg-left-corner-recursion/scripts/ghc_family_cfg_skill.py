"""Bounded synthetic CFG operations; JSON on stdin only."""
from ghc_family_cfg_core import cli

OPERATIONS = ('cfg_left_corner', 'cfg_left_recursive')

if __name__ == '__main__':
    raise SystemExit(cli(OPERATIONS))
