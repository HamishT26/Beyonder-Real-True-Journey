#!/usr/bin/env python3
"""Fail-closed lifecycle and stale-label review for Sylven v647-v4."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sylven-arc" / "v647-v4"


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def review(lifecycle: str) -> dict[str, Any]:
    issues: list[str] = []
    truth = load("phase-truth.json")
    orchestration = load("orchestration/x2-update.json")
    evidence = load("evidence-receipt.json")
    if truth.get("route_state") != "PREPARED_NOT_SENT":
        issues.append("phase truth route state is not PREPARED_NOT_SENT")
    if orchestration.get("route_state") != "PREPARED_NOT_SENT" or orchestration.get("send_count") != 0:
        issues.append("orchestration implies a sent route")
    if orchestration.get("successor_task_created"):
        issues.append("orchestration implies a successor task was created")
    lifecycle_paths = {
        "closeout-receipt.json": (PHASE / "closeout-receipt.json").exists(),
        "seal-receipt.json": (PHASE / "seal-receipt.json").exists(),
        "final-receipt.json": (PHASE / "final-receipt.json").exists(),
    }
    if lifecycle == "evidence":
        if evidence.get("evidence_commit") != "PENDING_UNTIL_COMMIT":
            issues.append("evidence candidate lacks the pending commit marker")
        if any(lifecycle_paths.values()):
            issues.append("closeout, seal, or final receipt appeared during evidence lifecycle")
    else:
        if evidence.get("evidence_commit") in {None, "PENDING_UNTIL_COMMIT"}:
            issues.append("final lifecycle retains a pending evidence commit")
        if not all(lifecycle_paths.values()):
            issues.append("final lifecycle is missing closeout, seal, or final receipt")
    return {
        "schema": f"ghc.family.v647-v4.lifecycle-review.{lifecycle}.v1",
        "lifecycle": lifecycle,
        "route_state": truth.get("route_state"),
        "send_count": orchestration.get("send_count"),
        "successor_task_created": orchestration.get("successor_task_created"),
        "lifecycle_receipts": lifecycle_paths,
        "issues": issues,
        "result": "pass" if not issues else "fail",
        "boundary": "Repository lifecycle review precedes any external baton and cannot prove delivery acknowledgement.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lifecycle", choices=["evidence", "final"], required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    result = review(args.lifecycle)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"lifecycle": args.lifecycle, "issues": len(result["issues"]), "result": result["result"]}, sort_keys=True))
    return 0 if result["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
