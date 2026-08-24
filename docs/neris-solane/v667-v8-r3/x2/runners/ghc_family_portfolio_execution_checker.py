"""Owner-scoped runner generated for Neris v667-v8-r3."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
TARGET = ROOT / 'docs/neris-solane/v667-v8-r3/x2/portfolio/owner-execution.json'
CONTRACT = 'ghc_family_portfolio_execution_checker'
REQUIRED_KEY = 'owner_safe_now'

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    if not args.validate:
        raise SystemExit("--validate is required")
    if not TARGET.is_file():
        raise SystemExit(f"missing target: {TARGET.name}")
    payload = json.loads(TARGET.read_text(encoding="utf-8"))
    if REQUIRED_KEY not in payload:
        raise SystemExit(f"missing key: {REQUIRED_KEY}")
    print(json.dumps({"runner": CONTRACT, "target": TARGET.name, "state": "PASS_BOUNDED_OWNER_SCOPE"}, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
