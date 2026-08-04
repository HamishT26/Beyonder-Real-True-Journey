#!/usr/bin/env python3
"""Read-only scaffold audit for the additive Orin Thale v661-v3 x1 lane.

The substantive x1 files are deliberately authored in the Orin-owned worktree.
This helper confirms their presence and refuses to clone or rewrite Caelen's
sealed source. It performs no repository, task, network, or external mutation.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "scripts/ghc_family_v661_v3_data.py",
    "scripts/build_ghc_family_v661_v3_scaffold.py",
    "scripts/build_ghc_family_v661_v3_x1.py",
    "scripts/ghc_family_v661_v3_novelty_probe.py",
    "tests/test_ghc_family_v661_v3_x1.py",
)


def main() -> None:
    rows = [{"path": path, "exists": (ROOT / path).is_file()} for path in REQUIRED]
    receipt = {
        "schema": "ghc.family.v661-v3.read-only-scaffold-audit.v1",
        "owner": "Orin Thale",
        "phase": "v661-v3",
        "all_present": all(row["exists"] for row in rows),
        "files": rows,
        "source_mutated": False,
        "external_actions": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    if not receipt["all_present"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
