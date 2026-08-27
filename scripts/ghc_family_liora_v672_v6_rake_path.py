"""Family-current Liora v672-v6 rake_path runner."""

import sys
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from scripts.ghc_family_liora_v672_v6_core import cli


if __name__ == "__main__":
    raise SystemExit(cli("rake_path"))
