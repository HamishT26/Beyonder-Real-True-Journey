from ghc_family_mesh_cli import main
from ghc_family_mesh_x2 import evaluate

if __name__ == "__main__":
    raise SystemExit(main(evaluate, {"provenance_binding", "claim_reservation"}))
