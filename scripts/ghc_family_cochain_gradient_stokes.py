"""Bounded paired interface: cochain_gradient_stokes."""
from ghc_family_geometry_x2 import evaluate
from ghc_family_geometry_cli import main

if __name__ == "__main__":
    raise SystemExit(main(evaluate, ['coboundary_gradient', 'discrete_stokes']))
