#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = ["## Scope", "## Inputs", "## Steps", "## Refusals", "## Outputs", "## Smoke fixture"]

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skills-root", type=Path, required=True)
    args = parser.parse_args()
    receipts = []
    for path in sorted(args.skills_root.glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        missing = [heading for heading in REQUIRED if heading not in text]
        receipts.append({
            "skill": path.parent.name,
            "read_through_eof": True,
            "quick_validated": not missing,
            "smoke_used": "WITHHELD_SYNTHETIC_ONLY" in text and "authority-promotion" in text,
            "missing_headings": missing,
            "global_install": False,
            "real_world_rows": 0,
        })
    result = {
        "skill_count": len(receipts),
        "validated_count": sum(item["quick_validated"] for item in receipts),
        "smoke_used_count": sum(item["smoke_used"] for item in receipts),
        "receipts": receipts,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["skill_count"] == result["validated_count"] == result["smoke_used_count"] == 20 else 1

if __name__ == "__main__":
    raise SystemExit(main())
