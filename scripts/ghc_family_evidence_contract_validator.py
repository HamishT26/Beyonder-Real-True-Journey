#!/usr/bin/env python3
"""Validate the bounded GHC Family v642-v8 evidence-contract packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


PHASE_REL = Path("docs/sylven-arc/v642-v8")
EXPECTED_DISTRIBUTION = {
    "completed": 6,
    "represented": 2,
    "open_gap": 1,
    "exact_gate": 1,
}
TRUTH_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
PRIVATE_PATTERNS = {
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "bearer_token": re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}"),
    "conversation_url": re.compile(
        r"https?://(?:chatgpt\.com|chat\.openai\.com)/(?:c|share)/[A-Za-z0-9-]+",
        re.I,
    ),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "openai_style_secret": re.compile(r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}"),
    "private_key_block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "raw_uuid_task_or_thread_id": re.compile(
        r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-"
        r"[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"
    ),
    "windows_absolute_path": re.compile(
        r"(?i)(?:^|[\s\"'`(])(?:[A-Z]:\\|\\\\[^\s\\]+\\[^\s\\]+\\)"
    ),
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def digest(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path)).hexdigest()


def raw_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_size(path: Path) -> int:
    return len(normalized_bytes(path))


def validate(
    repo: Path,
    phase: Path | None = None,
    allow_pending_snapshot: bool = False,
) -> dict[str, Any]:
    """Return a detailed, deterministic validation receipt."""
    repo = repo.resolve()
    phase = (phase or (repo / PHASE_REL)).resolve()
    checks: list[str] = []
    issues: list[str] = []

    def check(condition: bool, name: str, detail: str | None = None) -> None:
        checks.append(name)
        if not condition:
            issues.append(detail or name)

    required = [
        "identity-receipt.json",
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
        "reproduction/independent-team-gap.json",
        "tooling/executed-toolchain.json",
        "accessibility/static-report-receipt.json",
        "deliverables/v642-v8-evidence-contract-report.html",
        "v642-v8-integrated-overview.md",
    ]
    for relative in required:
        check((phase / relative).is_file(), f"required:{relative}")

    json_files = sorted(phase.rglob("*.json"))
    parsed: dict[Path, Any] = {}
    for path in json_files:
        relative = path.relative_to(phase).as_posix()
        try:
            parsed[path] = load(path)
            check(True, f"json:{relative}")
        except Exception as exc:  # pragma: no cover - diagnostic path
            check(False, f"json:{relative}", f"{relative}: {exc}")

    proposals = load(phase / "x1-proposals.json")
    proposal_rows = proposals["proposals"]
    check(proposals["proposal_count"] == 10, "proposal_count_declared")
    check(len(proposal_rows) == 10, "proposal_count_observed")
    check(proposals["prior_frozen_proposal_count"] == 140, "prior_frozen_count_140")
    check(proposals["outcome_classes"] == TRUTH_LABELS, "truth_vocabulary")
    check(proposals["expected_counts_are_results"] is False, "expected_not_results")
    check(proposals["expected_disposition_counts"] == EXPECTED_DISTRIBUTION, "expected_distribution")
    check(len({row["proposal_id"] for row in proposal_rows}) == 10, "proposal_ids_unique")
    check(len({row["title"] for row in proposal_rows}) == 10, "proposal_titles_unique")
    required_fields = {
        "proposal_id",
        "title",
        "mission_surface",
        "hypothesis",
        "null_or_failure",
        "approval_class",
        "execution_lane",
        "authoritative_source_needs",
        "deliverables",
        "test_falsifier_or_gate",
        "rollback_or_recovery",
        "protected_gates",
        "expected_disposition",
        "novelty_against_prior_chain",
    }
    for row in proposal_rows:
        proposal_id = row["proposal_id"]
        check(required_fields.issubset(row), f"proposal_fields:{proposal_id}")
        check(len(row["deliverables"]) == 3, f"deliverable_count:{proposal_id}")
        check(row["expected_disposition"] in TRUTH_LABELS, f"expected_label:{proposal_id}")
        for relative in row["deliverables"]:
            check((phase / relative).is_file(), f"deliverable:{relative}")

    collision = load(phase / "provenance/prior-proposal-collision-audit.json")
    check(collision["prior_phase_counts"]["total"] == 140, "collision_prior_count")
    check(collision["candidate_count"] == 10, "collision_candidate_count")
    check(collision["exact_title_collisions"] == 0, "collision_titles_zero")
    check(collision["exact_proposal_id_collisions"] == 0, "collision_ids_zero")
    check(collision["semantic_delta_review_passed"] is True, "semantic_novelty_review")
    check(all(row["distinct"] is True for row in collision["checks"]), "semantic_novelty_rows")
    check(len(collision["x1_execution_negatives"]) == 11, "x1_negative_count_11")

    frozen = load(phase / "provenance/frozen-chain-proposal-index.json")
    inherited_index = repo / frozen["inherited_index"]
    check(frozen["inherited_record_count"] == 140, "frozen_inherited_count")
    check(frozen["new_record_count"] == 10, "frozen_new_count")
    check(frozen["effective_record_count"] == 150, "frozen_effective_count")
    check(inherited_index.is_file(), "frozen_inherited_exists")
    if inherited_index.is_file():
        check(raw_digest(inherited_index) == frozen["inherited_index_sha256"], "frozen_inherited_hash")

    sources = load(phase / "sources/source-ledger.json")
    check(sources["effective_source_count"] == sum(sources["effective_status_counts"].values()), "source_count")
    check(sources["effective_status_counts"]["draft"] == 5, "draft_sources_visible")
    check(sources["effective_status_counts"]["watch"] == 1, "watch_source_visible")
    check(sources["added_source_count"] == 7, "added_source_count_7")
    check(len(sources["added_sources"]) == 7, "added_sources_observed_7")

    ledger = load(phase / "x2-proposal-ledger.json")
    check(ledger["proposal_count"] == 10, "x2_proposal_count_declared")
    check(len(ledger["proposals"]) == 10, "x2_proposal_count_observed")
    check(ledger["observed_distribution"] == EXPECTED_DISTRIBUTION, "observed_distribution")
    check(ledger["expected_distribution"] == EXPECTED_DISTRIBUTION, "ledger_expected_distribution")
    check(ledger["expected_observed_match"] is True, "expected_observed_match")
    check(ledger["case_count"] == 80, "case_count_80")
    check(ledger["synthetic_rejection_count"] == 70, "synthetic_count_70")
    for row in ledger["proposals"]:
        check(row["observed_disposition"] in TRUTH_LABELS, f"observed_label:{row['proposal_id']}")
        check(row["expectation_matched"] is True, f"disposition_match:{row['proposal_id']}")
        check(row["case_count"] == 8, f"case_count:{row['proposal_id']}")
        check(row["accepted_case_count"] == 1, f"accepted_count:{row['proposal_id']}")
        check(row["rejected_case_count"] == 7, f"rejected_count:{row['proposal_id']}")

    evidence = load(phase / "evidence/evidence-ledger.json")
    check(evidence["entry_count"] == 30, "evidence_entry_count_30")
    check(len(evidence["entries"]) == 30, "evidence_entries_observed_30")
    check(evidence["case_count"] == 80, "evidence_case_count_80")
    check(evidence["synthetic_rejection_count"] == 70, "evidence_synthetic_count_70")
    check(all(value == 0 for value in evidence["real_external_counts"].values()), "real_external_counts_zero")
    for item in evidence["entries"]:
        artifact = phase / item["path"]
        check(artifact.is_file(), f"evidence_exists:{item['path']}")
        if artifact.is_file():
            check(digest(artifact) == item["normalized_sha256"], f"evidence_hash:{item['path']}")
            check(normalized_size(artifact) == item["bytes"], f"evidence_size:{item['path']}")

    for row in proposal_rows:
        vectors = load(phase / row["deliverables"][1])
        check(vectors["case_count"] == 8, f"vectors_count:{row['proposal_id']}")
        check(vectors["rejected_case_count"] == 7, f"vectors_rejected:{row['proposal_id']}")
        check(vectors["all_expected_outcomes_matched"] is True, f"vectors_match:{row['proposal_id']}")
        for case in vectors["cases"]:
            check(case["matched_expectation"] is True, f"fixture:{case['case_id']}")

    negatives = load(phase / "retained-negative-register.json")
    check(negatives["inherited_count"] == 312, "inherited_negatives_312")
    check(negatives["x1_operational_count"] == 11, "x1_negatives_11")
    check(negatives["new_synthetic_count"] == 70, "new_synthetic_70")
    check(negatives["transition_and_x2_operational_count"] >= 0, "x2_operational_nonnegative")
    check(negatives["negative_count"] == len(negatives["negatives"]), "negative_count_matches")
    check(negatives["negative_count"] >= 393, "negative_floor_393")
    check(negatives["all_retained"] is True, "all_negatives_retained")
    check(negatives["erasure_permitted"] is False, "negative_erasure_false")
    check(len({row["negative_id"] for row in negatives["negatives"]}) == negatives["negative_count"], "negative_ids_unique")
    for row in negatives["negatives"]:
        check(row.get("retained") is True, f"negative_retained:{row['negative_id']}")

    gates = load(phase / "exact-open-gate-register.json")
    check(gates["open_gap_count"] == 5, "open_gap_count_5")
    check(len(gates["open_gaps"]) == 5, "open_gap_rows_5")
    check(gates["exact_gate_count"] == 6, "exact_gate_count_6")
    check(len(gates["exact_gates"]) == 6, "exact_gate_rows_6")
    check(gates["all_visible"] is True, "gates_visible")

    truth = load(phase / "phase-truth.json")
    check(truth["retained_negative_count"] == negatives["negative_count"], "truth_negative_count")
    check(truth["open_gap_count"] == 5, "truth_open_gap_count")
    check(truth["exact_gate_count"] == 6, "truth_exact_gate_count")
    check(truth["outbound_message_count"] == 0, "outbound_zero")
    check(truth["successor_task_count"] == 0, "successor_zero")
    check(truth["subagent_count"] == 0, "subagents_zero")
    check(all(value is False for value in truth["protected_claims"].values()), "protected_claims_false")
    check(truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", "terminal_verdict")

    threat = load(phase / "threat-model.json")
    check(threat["threat_count"] >= 12, "threat_count")
    check(len(threat["threats"]) == threat["threat_count"], "threat_rows")
    check(threat["exhaustive_security"] is False, "exhaustive_security_false")
    check(threat["independent_security_review"] is False, "independent_security_false")
    ceiling = threat["resource_ceilings"]
    check(ceiling["owner_generated_files"] == 15000, "owned_file_threshold_15000")
    check(ceiling["inherited_repository_baseline_excluded"] is True, "inherited_baseline_excluded")
    owner_code = [
        repo / "scripts/ghc_family_evidence_contract.py",
        repo / "scripts/ghc_family_evidence_contract_validator.py",
        repo / "scripts/ghc_family_evidence_contract_minimal.py",
        repo / "scripts/build_ghc_family_evidence_contract_report.py",
        repo / "tests/test_ghc_family_v642_v8.py",
    ]
    owner_file_count = sum(1 for path in phase.rglob("*") if path.is_file()) + sum(path.is_file() for path in owner_code)
    check(owner_file_count < 15000, "owned_files_below_threshold", str(owner_file_count))

    detached = load(phase / "reproduction/detached-evidence-validation.json")
    independent = load(phase / "reproduction/independent-team-gap.json")
    check(detached["same_owner_repeatability_only"] is True, "detached_same_owner_only")
    check(detached["independent_team_reproduction"] is False, "detached_not_independent")
    check(independent["independent_team_count"] == 0, "independent_team_zero")
    check(independent["status"] == "open_gap", "independent_gap_open")
    if allow_pending_snapshot:
        check(detached["state"] in {"pending_exact_evidence_commit", "verified"}, "snapshot_state_allowed")
    else:
        check(detached["state"] == "verified", "snapshot_state_verified")
        check(detached["snapshot_count"] >= 2, "snapshot_count_two")
        if "snapshots" in detached:
            check(len(detached["snapshots"]) >= 2, "snapshot_rows_two")
            check(all(row.get("valid") is True for row in detached["snapshots"]), "snapshots_valid")

    report_path = phase / "deliverables/v642-v8-evidence-contract-report.html"
    report_text = report_path.read_text(encoding="utf-8")
    report_markers = [
        '<html lang="en">',
        'href="#main"',
        '<main id="main"',
        '<caption>',
        ':focus-visible',
        'NOT_READY_FOR_STAGE_20',
        'manual accessibility evaluation',
        'affected-user evaluation',
    ]
    for marker in report_markers:
        check(marker in report_text, f"report_marker:{marker}")
    check("complete accessibility conformance" not in report_text.lower(), "no_complete_accessibility_claim")
    overview_words = len((phase / "v642-v8-integrated-overview.md").read_text(encoding="utf-8").split())
    check(overview_words >= 1200, "overview_three_page_equivalent", str(overview_words))

    manifest = load(phase / "reproduction/manifest.json")
    check(manifest["entry_count"] == 60, "manifest_entry_count_60")
    check(len(manifest["entries"]) == 60, "manifest_rows_60")
    check(manifest["same_owner_repeatability_only"] is True, "manifest_same_owner_only")
    check(manifest["independent_team_reproduction"] is False, "manifest_not_independent")
    manifest_paths = [row["path"] for row in manifest["entries"]]
    check(len(set(manifest_paths)) == 60, "manifest_paths_unique")
    for row in manifest["entries"]:
        artifact = phase / row["path"]
        check(artifact.is_file(), f"manifest_exists:{row['path']}")
        if artifact.is_file():
            check(digest(artifact) == row["normalized_sha256"], f"manifest_hash:{row['path']}")
            check(normalized_size(artifact) == row["bytes"], f"manifest_size:{row['path']}")

    privacy_hits: list[dict[str, str]] = []
    scanned_files = 0
    for path in sorted(item for item in phase.rglob("*") if item.is_file()):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned_files += 1
        for name, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                privacy_hits.append({"file": path.relative_to(phase).as_posix(), "pattern": name})
    check(not privacy_hits, "privacy_zero_hits", json.dumps(privacy_hits, ensure_ascii=False))

    return {
        "schema": "ghc.family.v642-v8.evidence-contract-validation.v1",
        "phase": "v642-gmut-thos-v8-x1-x2",
        "owner": "Sylven Arc",
        "check_count": len(checks),
        "issue_count": len(issues),
        "checks": checks,
        "issues": issues,
        "json_files_parsed": len(parsed),
        "privacy_scan": {
            "files": scanned_files,
            "pattern_classes": len(PRIVATE_PATTERNS),
            "hits": len(privacy_hits),
        },
        "observed_distribution": ledger["observed_distribution"],
        "case_count": ledger["case_count"],
        "retained_negative_count": negatives["negative_count"],
        "manifest_entry_count": manifest["entry_count"],
        "overview_word_count": overview_words,
        "owner_generated_file_count": owner_file_count,
        "allow_pending_snapshot": allow_pending_snapshot,
        "valid": not issues,
        "boundary": "Validation covers bounded repository evidence only; protected empirical, participant, production, legal, cultural, accessibility-complete, exhaustive-security, deployment, proof/canon, identity, and independent-reproduction claims remain false or gated.",
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
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--phase-dir", type=Path)
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    phase = args.phase_dir.resolve() if args.phase_dir else repo / PHASE_REL
    result = validate(repo, phase, args.allow_pending_snapshot)
    if args.output:
        output = args.output if args.output.is_absolute() else repo / args.output
        write_json(output.resolve(), result)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
