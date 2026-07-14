#!/usr/bin/env python3
"""Minimal standard-library verifier for the Eiren Kestrel v643-v7 packet."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


def load_engine(repo: Path):
    path = repo / "scripts/ghc_family_v643_v7_evidence.py"
    spec = importlib.util.spec_from_file_location("ghc_family_v643_v7_evidence_minimal", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def verify(phase: Path, allow_pending_snapshot: bool = False) -> dict[str, Any]:
    phase = phase.resolve()
    repo = phase.parents[2]
    engine = load_engine(repo)
    checks: list[dict[str, Any]] = []

    def add(label: str, passed: bool, detail: Any = None) -> None:
        checks.append({"label": label, "passed": bool(passed), "detail": detail})

    def read(relative: str) -> Any:
        return json.loads((phase / relative).read_text(encoding="utf-8"))

    required = [
        "x1-proposals.json",
        "x2-proposal-ledger.json",
        "phase-truth.json",
        "retained-negative-register.json",
        "exact-open-gate-register.json",
        "reproduction/x1-content-seal.json",
        "reproduction/manifest.json",
        "stage20/domain-veto-evidence-board.json",
        "validation/x2-privacy-scan.json",
        "deliverables/v643-v7-boundary-evidence-report.html",
        "deliverables/v643-v7-final-integrated-overview.md",
    ]
    add("required-files", all((phase / relative).is_file() for relative in required))
    if not checks[-1]["passed"]:
        issues = [row["label"] for row in checks if not row["passed"]]
        return _result(engine, checks, issues, allow_pending_snapshot)

    x1 = read("x1-proposals.json")
    x2 = read("x2-proposal-ledger.json")
    truth = read("phase-truth.json")
    negatives = read("retained-negative-register.json")
    gates = read("exact-open-gate-register.json")
    manifest = read("reproduction/manifest.json")
    x1_seal = read("reproduction/x1-content-seal.json")
    stage20 = read("stage20/domain-veto-evidence-board.json")
    privacy = read("validation/x2-privacy-scan.json")
    expected_negative_count = 904 + 4 + 70 + len(engine.X2_OPERATIONAL_NEGATIVES)

    add("phase-owner", x1.get("phase") == engine.PHASE and x1.get("owner") == engine.OWNER)
    add("source-binding", x2.get("source_commit") == engine.SOURCE_COMMIT and x2.get("source_seal") == engine.SOURCE_SEAL)
    add("x1-source-binding", x2.get("x1_commit") == engine.X1_COMMIT)
    add("ten-proposals", len(x1.get("proposals", [])) == 10)
    add("x1-before-x2", x2.get("x1_before_x2_preserved") is True)
    add("x1-content-seal", x1_seal.get("entry_count") == 26 and x1_seal.get("all_unchanged") is True)
    add("eighty-cases", x2.get("case_count") == 80)
    add("seventy-rejections", x2.get("synthetic_rejection_count") == 70)
    add("distribution", x2.get("distribution") == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
    add("fixture-expectations", all(row["matched_expectation"] for rows in engine.evaluate_catalog().values() for row in rows))
    add("negative-count", negatives.get("negative_count") == expected_negative_count)
    add("negative-row-count", len(negatives.get("negatives", [])) == expected_negative_count)
    add("inherited-negatives", negatives.get("inherited_count") == 904)
    add("x1-operational-negatives", negatives.get("x1_operational_count") == 4)
    add("x2-operational-negatives", negatives.get("x2_operational_count") == len(engine.X2_OPERATIONAL_NEGATIVES))
    add("negative-retention", negatives.get("all_retained") is True and negatives.get("erasure_permitted") is False)
    add("five-open-gaps", gates.get("open_gap_count") == 5)
    add("six-exact-gates", gates.get("exact_gate_count") == 6)
    add("terminal-verdict", truth.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20")
    add("primary-focus", truth.get("primary_focus") == "Freed ID/CBR Heart")
    add("all-pillars", truth.get("all_three_pillars_preserved") is True)
    add("route-unsent", truth.get("route_state") == "PREPARED_NOT_SENT" and truth.get("outbound_message_count") == 0)
    add("protected-claims-false", all(value is False for value in truth.get("protected_claims", {}).values()))
    add("independent-open", truth.get("independent_team_reproduction") is False)
    add("stage20-veto", stage20.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20" and stage20.get("compensation_across_domains_allowed") is False)
    add("privacy-zero", privacy.get("valid") is True and privacy.get("hit_count") == 0)
    add("manifest-count", manifest.get("entry_count") == len(manifest.get("entries", [])) and manifest.get("entry_count", 0) > 0)
    add(
        "manifest-parity",
        all(
            (repo / row["repo_path"]).is_file()
            and engine.normalized_sha256(repo / row["repo_path"]) == row["sha256_lf_normalized"]
            for row in manifest.get("entries", [])
        ),
    )
    add(
        "snapshot-state",
        manifest.get("snapshot_state") in {"pending", "verified"}
        if allow_pending_snapshot
        else manifest.get("snapshot_state") == "verified",
    )
    report = (phase / "deliverables/v643-v7-boundary-evidence-report.html").read_text(encoding="utf-8")
    add("report-static", '<html lang="en-NZ">' in report and "<script" not in report.casefold())
    add("report-boundaries", "Māori" in report and "NOT_READY_FOR_STAGE_20" in report)
    overview = (phase / "deliverables/v643-v7-final-integrated-overview.md").read_text(encoding="utf-8")
    add("overview-three-page-equivalent", len(overview.split()) >= 1500)

    issues = [row["label"] for row in checks if not row["passed"]]
    return _result(engine, checks, issues, allow_pending_snapshot)


def _result(engine: Any, checks: list[dict[str, Any]], issues: list[str], allow_pending_snapshot: bool) -> dict[str, Any]:
    return {
        "schema": "ghc.family.v643-v7.minimal-validation.v1",
        "phase": engine.PHASE,
        "owner": engine.OWNER,
        "valid": not issues,
        "check_count": len(checks),
        "passed_count": sum(row["passed"] for row in checks),
        "issue_count": len(issues),
        "issues": issues,
        "checks": checks,
        "allow_pending_snapshot": allow_pending_snapshot,
        "boundary": engine.BOUNDARY,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    repo = Path(__file__).resolve().parents[1]
    parser.add_argument("--phase", type=Path, default=repo / "docs/eiren-kestrel/v643-v7")
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
