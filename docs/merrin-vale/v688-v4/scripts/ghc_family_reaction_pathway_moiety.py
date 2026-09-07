"""Bounded synthetic reaction dispatcher; no external execution."""
from ghc_family_reaction_core import cli
ALLOWED = ('limiting_pool', 'degree_of_reaction', 'pathway_sum', 'moiety_certificate')
if __name__ == "__main__":
    raise SystemExit(cli(ALLOWED))
