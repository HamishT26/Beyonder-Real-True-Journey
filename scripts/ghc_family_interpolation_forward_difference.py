from ghc_family_mesh_cli import main
from ghc_family_mesh_x1 import evaluate

if __name__ == "__main__":
    raise SystemExit(main(evaluate, {"linear_interpolate", "forward_difference"}))
