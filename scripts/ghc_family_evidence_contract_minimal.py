#!/usr/bin/env python3
"""Standard-library minimal verifier for the GHC Family v642-v8 packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


EXPECTED = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
CORE_PATHS = [
    "x1-proposals.json",
    "x2-proposal-ledger.json",
    "evidence/evidence-ledger.json",
    "phase-truth.json",
    "retained-negative-register.json",
    "exact-open-gate-register.json",
    "threat-model.json",
    "complete-incomplete-checklist.json",
    "reproduction/manifest.json",
    "reproduction/detached-evidence-validation.json",
    "deliverables/v642-v8-evidence-contract-report.html",
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def verify(phase: Path, allow_pending_snapshot: bool = False) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add(name: str, passed: bool, observed: Any = None) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed})

    add("core_paths", all((phase / relative).is_file() for relative in CORE_PATHS))
    parsed = 0
    try:
        for path in phase.rglob("*.json"):
            load(path)
            parsed += 1
        add("json_parse", True, parsed)
    except (OSError, json.JSONDecodeError) as exc:
        add("json_parse", False, str(exc))

    proposals = load(phase / "x1-proposals.json")
    ledger = load(phase / "x2-proposal-ledger.json")
    evidence = load(phase / "evidence/evidence-ledger.json")
    truth = load(phase / "phase-truth.json")
    negatives = load(phase / "retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    manifest = load(phase / "reproduction/manifest.json")
    detached = load(phase / "reproduction/detached-evidence-validation.json")

    add("proposal_count", proposals["proposal_count"] == 10 and len(proposals["proposals"]) == 10)
    add("frozen_prior_count", proposals["prior_frozen_proposal_count"] == 140)
    add("truth_labels", proposals["outcome_classes"] == ["completed", "represented", "open_gap", "exact_gate"])
    add("distribution", ledger["observed_distribution"] == EXPECTED, ledger["observed_distribution"])
    add("case_parity", ledger["case_count"] == 80 and ledger["synthetic_rejection_count"] == 70)
    add("real_counts_zero", all(value == 0 for value in evidence["real_external_counts"].values()))
    add("terminal_not_ready", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    add("protected_claims_false", all(value is False for value in truth["protected_claims"].values()))
    add("negative_floor", negatives["inherited_count"] == 312 and negatives["negative_count"] >= 393)
    add("negatives_retained", negatives["all_retained"] is True and negatives["erasure_permitted"] is False)
    add("gate_counts", gates["open_gap_count"] == 5 and gates["exact_gate_count"] == 6)
    add("no_route_action", truth["outbound_message_count"] == 0 and truth["successor_task_count"] == 0)
    add("no_subagents", truth["subagent_count"] == 0)
    add("same_owner_only", manifest["same_owner_repeatability_only"] is True and manifest["independent_team_reproduction"] is False)

    hashes_ok = manifest["entry_count"] == 60 and len(manifest["entries"]) == 60
    for item in manifest["entries"]:
        path = phase / item["path"]
        hashes_ok = hashes_ok and path.is_file() and digest(path) == item["normalized_sha256"]
    add("manifest_hashes", hashes_ok, manifest["entry_count"])

    report = (phase / "deliverables/v642-v8-evidence-contract-report.html").read_text(encoding="utf-8")
    add("report_structure", all(marker in report for marker in ['<html lang="en">', '<main id="main"', '<caption>', ':focus-visible']))
    add("report_boundary", "NOT_READY_FOR_STAGE_20" in report and "manual accessibility evaluation" in report and "affected-user evaluation" in report)

    if allow_pending_snapshot:
        snapshot_ok = detached["state"] in {"pending_exact_evidence_commit", "verified"}
    else:
        snapshot_ok = detached["state"] == "verified" and detached["snapshot_count"] >= 2
    add("snapshot_state", snapshot_ok, detached["state"])

    valid = all(row["passed"] for row in checks)
    return {
        "schema": "ghc.family.v642-v8.evidence-contract-minimal.v1",
        "phase": "v642-gmut-thos-v8-x1-x2",
        "owner": "Sylven Arc",
        "check_count": len(checks),
        "passed_count": sum(1 for row in checks if row["passed"]),
        "checks": checks,
        "json_files_parsed": parsed,
        "allow_pending_snapshot": allow_pending_snapshot,
        "valid": valid,
        "boundary": "Minimal verification covers repository structure only; it is not external scientific reproduction or authority.",
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(args.phase_dir.resolve(), args.allow_pending_snapshot)
    if args.output:
        write_json(args.output.resolve(), result)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
