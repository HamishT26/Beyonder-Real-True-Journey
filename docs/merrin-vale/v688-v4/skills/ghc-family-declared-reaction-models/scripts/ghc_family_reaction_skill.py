"""Bounded synthetic reaction dispatcher; no external execution."""
from ghc_family_reaction_core import cli
ALLOWED = ('deficiency_record', 'mass_action_monomial')
if __name__ == "__main__":
    raise SystemExit(cli(ALLOWED))
