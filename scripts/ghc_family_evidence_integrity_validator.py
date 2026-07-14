#!/usr/bin/env python3
"""Validate a bounded GHC Family v642-v6 evidence-integrity packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_evidence_integrity as integrity


EXPECTED_DISTRIBUTION = {
    "completed": 6,
    "represented": 2,
    "open_gap": 1,
    "exact_gate": 1,
}
PRIVATE_PATTERNS = {
    "raw_uuid_task_or_thread_id": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "windows_absolute_path": re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:\\"),
    "chatgpt_conversation_url": re.compile(r"https?://(?:www\.)?chatgpt\.com/c/", re.I),
    "openai_style_secret": re.compile(r"(?<![A-Za-z0-9_])sk-[A-Za-z0-9_-]{20,}"),
    "github_token": re.compile(r"(?<![A-Za-z0-9_])gh[opsu]_[A-Za-z0-9]{20,}"),
    "private_key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _manifest_paths(phase: Path) -> list[Path]:
    excluded_names = {"closeout-receipt.json", "final-validation-record.json", "seal-receipt.json"}
    paths: list[Path] = []
    for path in sorted(phase.rglob("*")):
        if not path.is_file() or path == phase / "reproduction/manifest.json":
            continue
        relative = path.relative_to(phase).as_posix()
        if relative.startswith("validation/") or path.name in excluded_names:
            continue
        paths.append(path)
    return paths


def validate(
    repo: Path,
    phase: Path,
    allow_pending_snapshot: bool = False,
    require_report: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: Any, detail: str = "") -> None:
        checks.append({"name": name, "passed": bool(condition), "detail": detail})

    proposal_path = phase / "x1-proposals.json"
    check("x1_proposals_exists", proposal_path.exists())
    if not proposal_path.exists():
        return {"valid": False, "checks_total": len(checks), "checks_passed": 0, "issues": [checks[0]]}
    proposals_packet = load(proposal_path)
    proposals = proposals_packet["proposals"]
    check("phase_exact", proposals_packet.get("phase") == integrity.PHASE)
    check("owner_exact", proposals_packet.get("owner") == integrity.OWNER)
    check("proposal_count_exact", len(proposals) == 10)
    check("prior_frozen_count", proposals_packet.get("prior_frozen_proposal_count") == 120)
    check("truth_labels_exact", set(proposals_packet.get("outcome_classes", [])) == set(integrity.TRUTH_LABELS))
    check("expected_distribution_exact", proposals_packet.get("expected_disposition_counts") == EXPECTED_DISTRIBUTION)
    check("expected_not_results", proposals_packet.get("expected_counts_are_results") is False)

    required_fields = [
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
    ]
    for proposal in proposals:
        proposal_id = proposal.get("proposal_id", "missing")
        for field in required_fields:
            value = proposal.get(field)
            check(f"proposal_{proposal_id}_{field}", value not in (None, "", []))
        check(f"proposal_{proposal_id}_deliverable_count", len(proposal.get("deliverables", [])) == 3)
        check(f"proposal_{proposal_id}_outcome_allowed", proposal.get("expected_disposition") in integrity.TRUTH_LABELS)
    check("proposal_ids_unique", len({item["proposal_id"] for item in proposals}) == 10)
    check("proposal_titles_unique", len({item["title"] for item in proposals}) == 10)

    common_required = [
        "complete-incomplete-checklist.json",
        "evidence/evidence-ledger.json",
        "exact-open-gate-register.json",
        "phase-truth.json",
        "reproduction/manifest.json",
        "retained-negative-register.json",
        "threat-model.json",
        "tooling/executed-toolchain.json",
        "validation/execution-negative-log.json",
        "x2-proposal-ledger.json",
    ]
    required = common_required + [path for proposal in proposals for path in proposal["deliverables"]]
    if require_report:
        required.append("deliverables/v642-v6-evidence-integrity-report.html")
    for relative in required:
        check(f"required_{relative}", (phase / relative).is_file())

    json_files = sorted(phase.rglob("*.json"))
    json_errors: list[str] = []
    for path in json_files:
        try:
            load(path)
            check(f"json_parse_{path.relative_to(phase).as_posix()}", True)
        except Exception as exc:  # pragma: no cover - failure path is reported
            json_errors.append(f"{path.relative_to(phase).as_posix()}: {exc}")
            check(f"json_parse_{path.relative_to(phase).as_posix()}", False, str(exc))

    ledger = load(phase / "x2-proposal-ledger.json")
    check("ledger_proposal_count", ledger.get("proposal_count") == 10)
    check("ledger_distribution", ledger.get("observed_distribution") == EXPECTED_DISTRIBUTION)
    check("ledger_expectations_match", ledger.get("all_expected_dispositions_matched") is True)
    check("ledger_case_count", ledger.get("total_case_count") == 80)
    check("ledger_matched_count", ledger.get("total_matched_count") == 80)
    rows = ledger.get("rows", [])
    check("ledger_row_count", len(rows) == 10)
    proposal_by_id = {item["proposal_id"]: item for item in proposals}
    for row in rows:
        proposal_id = row.get("proposal_id", "missing")
        check(f"ledger_{proposal_id}_known", proposal_id in proposal_by_id)
        if proposal_id in proposal_by_id:
            proposal = proposal_by_id[proposal_id]
            check(f"ledger_{proposal_id}_expected", row.get("expected_disposition") == proposal["expected_disposition"])
            check(f"ledger_{proposal_id}_observed", row.get("observed_disposition") == integrity.OBSERVED[proposal_id])
            check(f"ledger_{proposal_id}_expectation", row.get("expectation_matched") is True)
            check(f"ledger_{proposal_id}_case_count", row.get("case_count") == 8)
            check(f"ledger_{proposal_id}_matched", row.get("matched_count") == 8)
            check(f"ledger_{proposal_id}_negative_count", row.get("retained_negative_count") == 7)
            check(f"ledger_{proposal_id}_artifact_set", row.get("artifacts") == proposal["deliverables"])
        vector = load(phase / row["artifacts"][1])
        cases = vector.get("cases", [])
        check(f"vector_{proposal_id}_case_count", len(cases) == 8)
        check(f"vector_{proposal_id}_all_matched", vector.get("all_expected_results_matched") is True)
        for case in cases:
            case_id = case.get("case_id", "missing")
            check(f"case_{case_id}_matched", case.get("matched") is True)
            if case.get("expected") == "reject":
                check(f"case_{case_id}_retained", case.get("retained_negative") is True)
                check(f"case_{case_id}_reasoned", bool(case.get("reasons")))
            else:
                check(f"case_{case_id}_canonical_not_negative", case.get("retained_negative") is False)

    evidence = load(phase / "evidence/evidence-ledger.json")
    for name, count in evidence.get("real_or_external_counts", {}).items():
        check(f"real_count_zero_{name}", count == 0)
    for claim in integrity.PROTECTED_CLAIMS:
        check(f"evidence_claim_false_{claim}", evidence.get("protected_claims", {}).get(claim) is False)
    check("evidence_terminal_not_ready", evidence.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20")

    negatives = load(phase / "retained-negative-register.json")
    expected_new = 8 + 70 + negatives.get("x2_operational_count", -1)
    check("negative_inherited_count", negatives.get("inherited_count") == 147)
    check("negative_x1_count", negatives.get("x1_operational_count") == 8)
    check("negative_synthetic_count", negatives.get("new_synthetic_count") == 70)
    check("negative_new_count", negatives.get("new_count") == expected_new)
    check("negative_total_count", negatives.get("negative_count") == 147 + expected_new)
    check("negative_list_count", len(negatives.get("negatives", [])) == negatives.get("negative_count"))
    check("negative_all_retained", negatives.get("all_retained") is True and all(item.get("retained") is True for item in negatives.get("negatives", [])))
    check("negative_erasure_forbidden", negatives.get("erasure_permitted") is False)
    inherited_path = repo / negatives["inherited_from"]
    check("negative_inherited_path", inherited_path.is_file())
    check("negative_inherited_digest", negatives.get("inherited_sha256") == digest(inherited_path))
    check("negative_ids_unique", len({item["negative_id"] for item in negatives["negatives"]}) == len(negatives["negatives"]))

    gates = load(phase / "exact-open-gate-register.json")
    check("open_gap_count", gates.get("open_gap_count") == 5 and len(gates.get("open_gaps", [])) == 5)
    check("exact_gate_count", gates.get("exact_gate_count") == 6 and len(gates.get("exact_gates", [])) == 6)
    check("gates_visible", gates.get("all_visible") is True)
    gate_text = json.dumps(gates, ensure_ascii=False).lower()
    for token in ["empirical", "legal", "cultural", "identity", "production", "deployment", "privacy", "proof", "canon", "destructive", "account", "api-key", "sibling merge", "māori"]:
        check(f"gate_token_{token}", token in gate_text)

    truth = load(phase / "phase-truth.json")
    check("truth_terminal", truth.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20")
    check("truth_messages_zero", truth.get("outbound_message_count") == 0)
    check("truth_tasks_zero", truth.get("successor_task_count") == 0)
    check("truth_open_gates", truth.get("open_gap_count") == 5)
    check("truth_exact_gates", truth.get("exact_gate_count") == 6)
    check("truth_negative_count", truth.get("retained_negative_count") == negatives.get("negative_count"))
    for claim in integrity.PROTECTED_CLAIMS:
        check(f"truth_claim_false_{claim}", truth.get("protected_claims", {}).get(claim) is False)

    terminal = load(phase / proposal_by_id["V6426-P10"]["deliverables"][2])
    check("terminal_verdict_exact", terminal.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20")
    check("terminal_ready_false", terminal.get("stage20_ready") is False)
    check("terminal_noncompensation", terminal.get("engineering_pass_cannot_compensate") is True)
    snapshot = load(phase / proposal_by_id["V6426-P08"]["deliverables"][2])
    snapshot_state = snapshot.get("snapshot_state")
    check("snapshot_state_allowed", snapshot_state in {"pending", "verified"})
    check("snapshot_state_gate", snapshot_state == "verified" or allow_pending_snapshot, snapshot_state or "missing")
    check("snapshot_not_independent", snapshot.get("independent_team_reproduction") is False)

    threat = load(phase / "threat-model.json")
    check("threat_count", threat.get("threat_count") == 12 and len(threat.get("threats", [])) == 12)
    check("threat_not_exhaustive", threat.get("exhaustive_security") is False)
    check("threat_no_independent_review", threat.get("independent_security_review") is False)

    manifest = load(phase / "reproduction/manifest.json")
    current_paths = _manifest_paths(phase)
    manifest_rows = manifest.get("entries", [])
    manifest_by_path = {item["path"]: item for item in manifest_rows}
    expected_relatives = {path.relative_to(phase).as_posix() for path in current_paths}
    check("manifest_entry_count", manifest.get("entry_count") == len(manifest_rows))
    check("manifest_path_set", set(manifest_by_path) == expected_relatives)
    check("manifest_paths_unique", len(manifest_by_path) == len(manifest_rows))
    for path in current_paths:
        relative = path.relative_to(phase).as_posix()
        row = manifest_by_path.get(relative, {})
        check(f"manifest_hash_{relative}", row.get("normalized_sha256") == digest(path))
        check(f"manifest_bytes_{relative}", row.get("bytes") == path.stat().st_size)
    check("manifest_same_owner", manifest.get("same_owner_repeatability_only") is True)
    check("manifest_not_independent", manifest.get("independent_team_reproduction") is False)

    toolchain = load(phase / "tooling/executed-toolchain.json")
    check("toolchain_standard_library", toolchain.get("standard_library_only") is True)
    check("toolchain_compatibility", toolchain.get("caller_compatibility_preserved") is True)
    check("toolchain_inherited_unchanged", toolchain.get("inherited_tools_modified") is False)
    for row in toolchain.get("family_current_tools", []):
        tool_path = repo / row["path"]
        check(f"tool_exists_{row['path']}", tool_path.is_file())
        check(f"tool_hash_{row['path']}", tool_path.is_file() and row.get("normalized_sha256") == digest(tool_path))

    privacy_hits: list[str] = []
    for path in sorted(item for item in phase.rglob("*") if item.is_file()):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                privacy_hits.append(f"{path.relative_to(phase).as_posix()}:{label}")
    check("privacy_zero_hits", not privacy_hits, ", ".join(privacy_hits))

    report_path = phase / "deliverables/v642-v6-evidence-integrity-report.html"
    if require_report:
        report = report_path.read_text(encoding="utf-8") if report_path.exists() else ""
        required_tokens = [
            "<!doctype html>",
            'lang="en"',
            "skip-link",
            "<main",
            "<h1",
            "<table",
            "focus-visible",
            "prefers-reduced-motion",
            "manual and user accessibility evaluation remains reserved",
            "NOT_READY_FOR_STAGE_20",
        ]
        for token in required_tokens:
            check(f"report_token_{token}", token.lower() in report.lower())
        check("report_no_script", "<script" not in report.lower())
        check("report_not_complete_accessibility_claim", "complete accessibility conformance achieved" not in report.lower())

    x1_commit = ledger.get("x1_commit")
    head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    ancestry = subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", x1_commit, head], check=False).returncode == 0
    check("x1_commit_format", bool(re.fullmatch(r"[0-9a-f]{40}", x1_commit or "")))
    check("x1_is_ancestor_of_head", ancestry)

    issues = [item for item in checks if not item["passed"]]
    return {
        "schema": "ghc.family.v642-v6.evidence-integrity-validation.v1",
        "phase": integrity.PHASE,
        "owner": integrity.OWNER,
        "checks_total": len(checks),
        "checks_passed": len(checks) - len(issues),
        "issue_count": len(issues),
        "issues": issues,
        "json_files_parsed": len(json_files) - len(json_errors),
        "proposal_count": len(proposals),
        "case_count": ledger.get("total_case_count"),
        "retained_negative_count": negatives.get("negative_count"),
        "manifest_entry_count": manifest.get("entry_count"),
        "snapshot_state": snapshot_state,
        "report_required": require_report,
        "terminal_verdict": terminal.get("terminal_verdict"),
        "valid": not issues,
        "boundary": "Validation establishes bounded repository consistency only; protected external claims and gates remain false or open.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--phase-dir", required=True)
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--require-report", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    phase_arg = Path(args.phase_dir)
    phase = phase_arg.resolve() if phase_arg.is_absolute() else (repo / phase_arg).resolve()
    result = validate(repo, phase, args.allow_pending_snapshot, args.require_report)
    if args.output:
        output = Path(args.output)
        output = output if output.is_absolute() else repo / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
