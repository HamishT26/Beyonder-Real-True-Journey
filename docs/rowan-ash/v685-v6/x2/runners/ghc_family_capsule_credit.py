"""Owner-local capsule command interface; no task routing."""
from pathlib import Path
import importlib.util
import sys
root = Path(__file__).resolve().parents[5]
spec = importlib.util.spec_from_file_location("capsule", root / "scripts/ghc_family_evidence_capsule.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
if __name__ == "__main__":
    raise SystemExit(module.main(["check", "--group", 'credit', *sys.argv[1:]]))
