#!/usr/bin/env python3
"""Minimal standard-library verifier for bounded v642-v6 evidence integrity."""

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
    "retained-negative-register.json",
    "exact-open-gate-register.json",
    "phase-truth.json",
    "complete-incomplete-checklist.json",
    "threat-model.json",
    "reproduction/manifest.json",
    "reproduction/clean-snapshot-validation.json",
    "stage20/terminal-verdict.json",
    "tooling/executed-toolchain.json",
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def verify(phase: Path, allow_pending_snapshot: bool = False, require_report: bool = False) -> dict[str, Any]:
    checks: list[tuple[str, bool]] = []

    def check(name: str, value: Any) -> None:
        checks.append((name, bool(value)))

    for relative in CORE_PATHS:
        check(f"exists_{relative}", (phase / relative).is_file())
    report_path = phase / "deliverables/v642-v6-evidence-integrity-report.html"
    if require_report:
        check("report_exists", report_path.is_file())

    proposals = load(phase / "x1-proposals.json")
    ledger = load(phase / "x2-proposal-ledger.json")
    evidence = load(phase / "evidence/evidence-ledger.json")
    negatives = load(phase / "retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    truth = load(phase / "phase-truth.json")
    snapshot = load(phase / "reproduction/clean-snapshot-validation.json")
    terminal = load(phase / "stage20/terminal-verdict.json")
    manifest = load(phase / "reproduction/manifest.json")

    check("proposal_count", len(proposals["proposals"]) == 10)
    check("prior_count", proposals["prior_frozen_proposal_count"] == 120)
    check("outcome_vocabulary", set(proposals["outcome_classes"]) == set(EXPECTED))
    check("expected_distribution", proposals["expected_disposition_counts"] == EXPECTED)
    check("expectations_not_results", proposals["expected_counts_are_results"] is False)
    check("ledger_count", ledger["proposal_count"] == 10)
    check("ledger_distribution", ledger["observed_distribution"] == EXPECTED)
    check("ledger_expectations", ledger["all_expected_dispositions_matched"] is True)
    check("case_count", ledger["total_case_count"] == 80)
    check("case_matches", ledger["total_matched_count"] == 80)
    check("row_count", len(ledger["rows"]) == 10)
    for row in ledger["rows"]:
        check(f"row_{row['proposal_id']}_case_count", row["case_count"] == 8)
        check(f"row_{row['proposal_id']}_matched", row["matched_count"] == 8)
        check(f"row_{row['proposal_id']}_negatives", row["retained_negative_count"] == 7)
        vector = load(phase / row["artifacts"][1])
        check(f"row_{row['proposal_id']}_vector_match", vector["all_expected_results_matched"] is True)

    check("inherited_negatives", negatives["inherited_count"] == 147)
    check("x1_negatives", negatives["x1_operational_count"] == 8)
    check("synthetic_negatives", negatives["new_synthetic_count"] == 70)
    check("negative_total", negatives["negative_count"] == len(negatives["negatives"]))
    check("negative_retention", negatives["all_retained"] is True)
    check("negative_no_erasure", negatives["erasure_permitted"] is False)
    check("open_gates", gates["open_gap_count"] == 5 and len(gates["open_gaps"]) == 5)
    check("exact_gates", gates["exact_gate_count"] == 6 and len(gates["exact_gates"]) == 6)
    check("gates_visible", gates["all_visible"] is True)
    check("truth_negatives", truth["retained_negative_count"] == negatives["negative_count"])
    check("truth_messages", truth["outbound_message_count"] == 0)
    check("truth_tasks", truth["successor_task_count"] == 0)
    check("terminal", terminal["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    check("terminal_ready_false", terminal["stage20_ready"] is False)
    check("evidence_terminal", evidence["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    check("real_counts_zero", all(value == 0 for value in evidence["real_or_external_counts"].values()))
    check("protected_claims_false", all(value is False for value in evidence["protected_claims"].values()))
    check("truth_claims_false", all(value is False for value in truth["protected_claims"].values()))
    check("snapshot_state", snapshot["snapshot_state"] in {"pending", "verified"})
    check("snapshot_gate", snapshot["snapshot_state"] == "verified" or allow_pending_snapshot)
    check("snapshot_not_independent", snapshot["independent_team_reproduction"] is False)

    entries = manifest["entries"]
    check("manifest_count", manifest["entry_count"] == len(entries))
    check("manifest_paths_unique", len({row["path"] for row in entries}) == len(entries))
    for row in entries:
        path = phase / row["path"]
        check(f"manifest_exists_{row['path']}", path.is_file())
        check(f"manifest_hash_{row['path']}", path.is_file() and digest(path) == row["normalized_sha256"])
    check("manifest_same_owner", manifest["same_owner_repeatability_only"] is True)
    check("manifest_not_independent", manifest["independent_team_reproduction"] is False)

    json_files = sorted(phase.rglob("*.json"))
    parsed = 0
    for path in json_files:
        try:
            load(path)
            parsed += 1
        except Exception:
            pass
    check("all_json_parses", parsed == len(json_files))
    if require_report:
        report = report_path.read_text(encoding="utf-8") if report_path.exists() else ""
        for token in ["<main", "<h1", "<table", "skip-link", "focus-visible", "NOT_READY_FOR_STAGE_20"]:
            check(f"report_{token}", token.lower() in report.lower())
        check("report_manual_reservation", "manual and user accessibility evaluation remains reserved" in report.lower())
        check("report_no_script", "<script" not in report.lower())

    issues = [name for name, passed in checks if not passed]
    return {
        "schema": "ghc.family.v642-v6.evidence-integrity-minimal.v1",
        "checks_total": len(checks),
        "checks_passed": len(checks) - len(issues),
        "issue_count": len(issues),
        "issues": issues,
        "json_files_parsed": parsed,
        "snapshot_state": snapshot["snapshot_state"],
        "terminal_verdict": terminal["terminal_verdict"],
        "valid": not issues,
        "boundary": "Minimal verification is repository evidence only, not independent reproduction or external authority.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", required=True)
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--require-report", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    phase = Path(args.phase_dir).resolve()
    result = verify(phase, args.allow_pending_snapshot, args.require_report)
    if args.output:
        output = Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
