"""Bounded synthetic reaction dispatcher; no external execution."""
from ghc_family_reaction_core import cli
ALLOWED = ('flat_formula', 'grouped_formula')
if __name__ == "__main__":
    raise SystemExit(cli(ALLOWED))
