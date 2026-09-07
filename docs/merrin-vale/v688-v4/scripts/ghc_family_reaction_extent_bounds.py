"""Bounded synthetic reaction dispatcher; no external execution."""
from ghc_family_reaction_core import cli
ALLOWED = ('element_residual', 'charge_residual', 'extent_update', 'extent_interval')
if __name__ == "__main__":
    raise SystemExit(cli(ALLOWED))
