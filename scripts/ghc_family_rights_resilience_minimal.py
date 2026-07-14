#!/usr/bin/env python3
"""Minimal standard-library verifier for the v643-v1 packet."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
import ghc_family_rights_resilience as engine  # noqa: E402


def verify(phase: Path, allow_pending_snapshot: bool = False) -> dict[str, Any]:
    phase = phase.resolve()
    checks: list[dict[str, Any]] = []

    def add(label: str, passed: bool, detail: Any = None) -> None:
        checks.append({"label": label, "passed": bool(passed), "detail": detail})

    def read(relative: str) -> Any:
        return json.loads((phase / relative).read_text(encoding="utf-8"))

    required = ["x1-proposals.json", "x2-proposal-ledger.json", "phase-truth.json", "retained-negative-register.json", "exact-open-gate-register.json", "reproduction/manifest.json", "deliverables/v643-v1-rights-resilience-report.html"]
    add("required-files", all((phase / relative).is_file() for relative in required))
    x1 = read("x1-proposals.json")
    x2 = read("x2-proposal-ledger.json")
    truth = read("phase-truth.json")
    negatives = read("retained-negative-register.json")
    gates = read("exact-open-gate-register.json")
    manifest = read("reproduction/manifest.json")
    add("phase-owner", x1.get("phase") == engine.PHASE and x1.get("owner") == engine.OWNER)
    add("source", x1.get("source_revision") == engine.SOURCE_COMMIT)
    add("ten-proposals", len(x1.get("proposals", [])) == 10)
    add("x1-source-binding", x2.get("x1_commit") == engine.X1_COMMIT)
    add("x1-before-x2", x2.get("x1_before_x2_preserved") is True)
    add("eighty-cases", x2.get("case_count") == 80)
    add("seventy-rejections", x2.get("synthetic_rejection_count") == 70)
    add("distribution", x2.get("distribution") == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
    add("negative-count", negatives.get("negative_count") == 478)
    add("negative-retention", negatives.get("all_retained") is True and negatives.get("erasure_permitted") is False)
    add("five-open-gaps", gates.get("open_gap_count") == 5)
    add("six-exact-gates", gates.get("exact_gate_count") == 6)
    add("terminal-verdict", truth.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20")
    add("route-unsent", truth.get("outbound_message_count") == 0)
    add("independent-open", truth.get("independent_team_reproduction") is False)
    add("manifest-sixty", manifest.get("entry_count") == len(manifest.get("entries", [])) == 60)
    add("manifest-parity", all((phase / row["path"]).is_file() and engine.normalized_sha256(phase / row["path"]) == row["sha256_lf_normalized"] for row in manifest.get("entries", [])))
    add("snapshot-state", manifest.get("snapshot_state") == "verified" if not allow_pending_snapshot else manifest.get("snapshot_state") in {"pending", "verified"})
    add("fixture-expectations", all(row["matched_expectation"] for rows in engine.evaluate_catalog().values() for row in rows))
    issues = [row["label"] for row in checks if not row["passed"]]
    return {"schema": "ghc.family.v643-v1.minimal-validation.v1", "phase": engine.PHASE, "owner": engine.OWNER, "valid": not issues, "check_count": len(checks), "passed_count": sum(row["passed"] for row in checks), "issue_count": len(issues), "issues": issues, "checks": checks, "allow_pending_snapshot": allow_pending_snapshot, "boundary": engine.BOUNDARY}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", type=Path, default=Path(__file__).resolve().parents[1] / "docs/eiren-kestrel/v643-v1")
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(args.phase, args.allow_pending_snapshot)
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8", newline="\n")
    print(json.dumps({key: result[key] for key in ("valid", "check_count", "passed_count", "issue_count", "issues")}, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
