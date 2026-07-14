#!/usr/bin/env python3
"""Validate the bounded GHC Family v642-v7 constraint-evidence packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


EXPECTED_DISTRIBUTION = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
TRUTH_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
PRIVATE_PATTERNS = {
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "bearer_token": re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}"),
    "chatgpt_conversation_url": re.compile(r"https?://(?:chatgpt\.com|chat\.openai\.com)/(?:c|share)/[A-Za-z0-9-]+", re.I),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "openai_style_secret": re.compile(r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}"),
    "private_key_block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "raw_uuid_task_or_thread_id": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
    "windows_absolute_path": re.compile(r"(?i)(?:^|[\s\"'`(])(?:[A-Z]:\\|\\\\[^\s\\]+\\[^\s\\]+\\)"),
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


def validate(repo: Path, phase: Path, allow_pending_snapshot: bool = False) -> dict[str, Any]:
    checks: list[str] = []
    issues: list[str] = []

    def check(condition: bool, name: str, detail: str | None = None) -> None:
        checks.append(name)
        if not condition:
            issues.append(detail or name)

    required = [
        "x1-proposals.json",
        "x2-proposal-ledger.json",
        "evidence/evidence-ledger.json",
        "phase-truth.json",
        "retained-negative-register.json",
        "exact-open-gate-register.json",
        "threat-model.json",
        "complete-incomplete-checklist.json",
        "reproduction/manifest.json",
        "tooling/executed-toolchain.json",
        "deliverables/v642-v7-constraint-evidence-report.html",
        "v642-v7-integrated-overview.md",
    ]
    for relative in required:
        check((phase / relative).is_file(), f"required:{relative}")

    json_files = sorted(phase.rglob("*.json"))
    parsed: dict[Path, Any] = {}
    for path in json_files:
        try:
            parsed[path] = load(path)
            check(True, f"json:{path.relative_to(phase).as_posix()}")
        except Exception as exc:  # pragma: no cover - diagnostic
            check(False, f"json:{path.relative_to(phase).as_posix()}", str(exc))

    proposals = load(phase / "x1-proposals.json")
    proposal_rows = proposals["proposals"]
    check(proposals["proposal_count"] == 10 and len(proposal_rows) == 10, "proposal_count")
    check(proposals["prior_frozen_proposal_count"] == 130, "prior_frozen_count")
    check(proposals["outcome_classes"] == TRUTH_LABELS, "truth_vocabulary")
    check(proposals["expected_counts_are_results"] is False, "expected_counts_are_not_results")
    check(proposals["expected_disposition_counts"] == EXPECTED_DISTRIBUTION, "expected_distribution")
    check(len({row["proposal_id"] for row in proposal_rows}) == 10, "proposal_ids_unique")
    check(len({row["title"] for row in proposal_rows}) == 10, "proposal_titles_unique")
    required_fields = {
        "proposal_id", "title", "mission_surface", "hypothesis", "null_or_failure",
        "approval_class", "execution_lane", "authoritative_source_needs", "deliverables",
        "test_falsifier_or_gate", "rollback_or_recovery", "protected_gates",
        "expected_disposition", "novelty_against_prior_chain",
    }
    for row in proposal_rows:
        check(required_fields.issubset(row), f"proposal_fields:{row['proposal_id']}")
        check(len(row["deliverables"]) == 3, f"deliverable_count:{row['proposal_id']}")
        for relative in row["deliverables"]:
            check((phase / relative).is_file(), f"deliverable:{relative}")

    collision = load(phase / "provenance/prior-proposal-collision-audit.json")
    check(collision["prior_phase_counts"]["total"] == 130, "collision_prior_count")
    check(collision["candidate_count"] == 10, "collision_candidate_count")
    check(collision["exact_title_collisions"] == 0, "exact_title_collisions")
    check(collision["exact_proposal_id_collisions"] == 0, "exact_id_collisions")
    check(all(item["distinct"] is True for item in collision["checks"]), "semantic_delta_distinct")
    check(len(collision["x1_execution_negatives"]) == 4, "x1_negative_count")

    frozen = load(phase / "provenance/frozen-chain-proposal-index.json")
    inherited_index = repo / frozen["inherited_index"]
    check(frozen["inherited_record_count"] == 130, "frozen_inherited_count")
    check(frozen["new_record_count"] == 10 and frozen["effective_record_count"] == 140, "frozen_effective_count")
    check(inherited_index.is_file() and raw_digest(inherited_index) == frozen["inherited_index_sha256"], "frozen_inherited_hash")

    sources = load(phase / "sources/source-ledger.json")
    status_sum = sum(sources["effective_status_counts"].values())
    check(sources["effective_source_count"] == 69 and status_sum == 69, "source_count")
    check(sources["effective_status_counts"]["draft"] == 5, "draft_sources_visible")
    check(sources["effective_status_counts"]["watch"] == 1, "watch_source_visible")
    check(len(sources["added_sources"]) == 3, "added_source_count")

    ledger = load(phase / "x2-proposal-ledger.json")
    check(ledger["proposal_count"] == 10 and len(ledger["rows"]) == 10, "x2_proposal_count")
    check(ledger["observed_distribution"] == EXPECTED_DISTRIBUTION, "observed_distribution")
    check(ledger["all_expected_dispositions_matched"] is True, "expected_observed_match")
    check(ledger["total_case_count"] == 80 and ledger["total_matched_count"] == 80, "case_totals")
    check({row["observed_disposition"] for row in ledger["rows"]}.issubset(TRUTH_LABELS), "observed_truth_labels")
    for row in ledger["rows"]:
        check(row["case_count"] == 8 and row["matched_count"] == 8, f"cases:{row['proposal_id']}")
        check(row["retained_negative_count"] == 7, f"synthetic_negatives:{row['proposal_id']}")

    evidence = load(phase / "evidence/evidence-ledger.json")
    check(all(value == 0 for value in evidence["real_or_external_counts"].values()), "real_external_counts_zero")
    check(all(value is False for value in evidence["protected_claims"].values()), "protected_claims_false")
    check(evidence["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", "terminal_verdict")
    if allow_pending_snapshot:
        check(evidence["snapshot_state"] in {"pending", "verified"}, "snapshot_state_allowed")
    else:
        check(evidence["snapshot_state"] == "verified", "snapshot_state_verified")
        detached = phase / "reproduction/detached-evidence-validation.json"
        check(detached.is_file() and load(detached).get("valid") is True, "detached_evidence_valid")

    negatives = load(phase / "retained-negative-register.json")
    check(negatives["inherited_count"] == 233, "inherited_negatives_233")
    check(negatives["x1_operational_count"] == 4, "x1_negatives_4")
    check(negatives["new_synthetic_count"] == 70, "synthetic_negatives_70")
    check(negatives["transition_and_x2_operational_count"] >= 1, "transition_negative_retained")
    check(negatives["negative_count"] == len(negatives["negatives"]), "negative_count_matches")
    check(negatives["negative_count"] >= 308, "negative_count_floor")
    check(negatives["all_retained"] is True and negatives["erasure_permitted"] is False, "negative_retention")
    check(len({item["negative_id"] for item in negatives["negatives"]}) == negatives["negative_count"], "negative_ids_unique")

    gates = load(phase / "exact-open-gate-register.json")
    check(gates["open_gap_count"] == 5 and len(gates["open_gaps"]) == 5, "open_gaps_5")
    check(gates["exact_gate_count"] == 6 and len(gates["exact_gates"]) == 6, "exact_gates_6")
    check(gates["all_visible"] is True, "gates_visible")

    truth = load(phase / "phase-truth.json")
    check(truth["retained_negative_count"] == negatives["negative_count"], "truth_negative_count")
    check(truth["open_gap_count"] == 5 and truth["exact_gate_count"] == 6, "truth_gate_counts")
    check(truth["outbound_message_count"] == 0 and truth["successor_task_count"] == 0, "no_route_action")
    check(all(value is False for value in truth["protected_claims"].values()), "truth_protected_claims_false")
    check(truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", "truth_terminal_verdict")

    threat = load(phase / "threat-model.json")
    check(threat["threat_count"] >= 12 and len(threat["threats"]) == threat["threat_count"], "threat_count")
    check(threat["exhaustive_security"] is False and threat["independent_security_review"] is False, "security_boundary")
    check(threat["resource_ceilings"]["owned_generated_files"] == 15000, "owned_file_threshold")

    report_text = (phase / "deliverables/v642-v7-constraint-evidence-report.html").read_text(encoding="utf-8")
    for marker in ['<html lang="en">', 'href="#main"', '<main id="main"', '<caption>', ':focus-visible', 'NOT_READY_FOR_STAGE_20']:
        check(marker in report_text, f"report_marker:{marker}")
    check("complete WCAG" not in report_text, "report_no_complete_wcag_claim")
    overview_words = len((phase / "v642-v7-integrated-overview.md").read_text(encoding="utf-8").split())
    check(overview_words >= 1200, "overview_three_page_equivalent", f"overview has {overview_words} words")

    manifest = load(phase / "reproduction/manifest.json")
    check(manifest["entry_count"] == len(manifest["entries"]), "manifest_entry_count")
    check(manifest["same_owner_repeatability_only"] is True, "same_owner_only")
    check(manifest["independent_team_reproduction"] is False, "independent_reproduction_false")
    manifest_paths = [item["path"] for item in manifest["entries"]]
    check(len(manifest_paths) == len(set(manifest_paths)), "manifest_paths_unique")
    for item in manifest["entries"]:
        path = phase / item["path"]
        check(path.is_file(), f"manifest_exists:{item['path']}")
        if path.is_file():
            check(digest(path) == item["normalized_sha256"], f"manifest_hash:{item['path']}")
            check(normalized_size(path) == item["bytes"], f"manifest_size:{item['path']}")

    privacy_hits: list[dict[str, str]] = []
    scanned_files = 0
    for path in sorted(p for p in phase.rglob("*") if p.is_file()):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned_files += 1
        for name, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                privacy_hits.append({"file": path.relative_to(phase).as_posix(), "pattern": name})
    check(not privacy_hits, "privacy_zero_hits", json.dumps(privacy_hits, ensure_ascii=False))
    check(len([p for p in phase.rglob("*") if p.is_file()]) < 15000, "owned_files_below_threshold")

    return {
        "schema": "ghc.family.v642-v7.constraint-evidence-validation.v1",
        "phase": "v642-gmut-thos-v7-x1-x2",
        "owner": "Tamar Vey",
        "check_count": len(checks),
        "issue_count": len(issues),
        "checks": checks,
        "issues": issues,
        "json_files_parsed": len(parsed),
        "privacy_scan": {"files": scanned_files, "pattern_classes": len(PRIVATE_PATTERNS), "hits": len(privacy_hits)},
        "observed_distribution": ledger["observed_distribution"],
        "case_count": ledger["total_case_count"],
        "retained_negative_count": negatives["negative_count"],
        "manifest_entry_count": manifest["entry_count"],
        "overview_word_count": overview_words,
        "allow_pending_snapshot": allow_pending_snapshot,
        "valid": not issues,
        "boundary": "Validation covers bounded repository evidence and does not establish empirical, participant, production, legal, cultural, accessibility-complete, exhaustive-security, deployment, or independent-reproduction claims.",
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--phase-dir", required=True)
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    phase = (repo / args.phase_dir).resolve() if not Path(args.phase_dir).is_absolute() else Path(args.phase_dir).resolve()
    result = validate(repo, phase, args.allow_pending_snapshot)
    if args.output:
        output = (repo / args.output).resolve() if not Path(args.output).is_absolute() else Path(args.output).resolve()
        write_json(output, result)
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
