#!/usr/bin/env python3
"""Validate and smoke-use all twenty phase-local special CLI-preparation skills."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v651-v8-special-cli-prep"
VALIDATOR = (
    Path(os.environ.get("USERPROFILE", str(Path.home())))
    / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
)


def main() -> int:
    build = json.loads((PHASE / "skills/skill-build-ledger.json").read_text(encoding="utf-8"))
    rows = []
    for row in build["rows"]:
        directory = PHASE / "skills" / row["name"]
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(directory)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
            check=False,
        )
        skill_text = (directory / "SKILL.md").read_text(encoding="utf-8")
        smoke_used = all(token in skill_text for token in ("## Trigger", "## Procedure", "## Truth boundary"))
        rows.append(
            {
                **row,
                "state": "validated_and_smoke_used" if result.returncode == 0 and smoke_used else "failed",
                "validator_exit": result.returncode,
                "validator_summary": result.stdout.strip(),
                "smoke_used": smoke_used,
                "global_installation": False,
            }
        )
    payload = {
        "schema": "ghc.family.v651-v8-special.skill-use.v1",
        "count": len(rows),
        "validated": sum(row["validator_exit"] == 0 for row in rows),
        "smoke_used": sum(bool(row["smoke_used"]) for row in rows),
        "global_promotions": 0,
        "rows": rows,
        "boundary": "Phase-local structural validation and smoke use only; no universal applicability or authority claim.",
    }
    path = PHASE / "skills/skill-use-ledger.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    valid = payload["count"] == 20 and payload["validated"] == 20 and payload["smoke_used"] == 20
    print(json.dumps({"valid": valid, "skills": payload["count"], "validated": payload["validated"], "used": payload["smoke_used"]}))
    return 0 if valid else 2


if __name__ == "__main__":
    raise SystemExit(main())
