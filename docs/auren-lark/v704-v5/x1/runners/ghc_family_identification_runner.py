from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ALLOWED = ['discrimination_design_selection', 'identification_partition']

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile-id", required=True)
    parser.add_argument("--operation", required=True)
    args = parser.parse_args()
    if args.operation not in ALLOWED:
        print(json.dumps({"ok": False, "error": "operation_not_allowed"}))
        return 2
    root = Path(__file__).resolve().parents[1]
    records = json.loads((root / "core-results.json").read_text(encoding="utf-8"))["records"]
    match = next((row for row in records if row["profile_id"] == args.profile_id and row["operation"] == args.operation), None)
    if match is None:
        print(json.dumps({"ok": False, "error": "record_not_found"}))
        return 2
    print(json.dumps({"ok": True, "proposal_id": match["proposal_id"], "result": match["actual"]}, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())
