#!/usr/bin/env python3
"""Detailed validator for the bounded Orin Thale v643-v4 packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
import ghc_family_boundary_evidence as engine  # noqa: E402


REQUIRED_PROPOSAL_FIELDS = {
    "proposal_id", "title", "mission_surface", "hypothesis", "null_or_failure",
    "approval_class", "execution_lane", "authoritative_source_needs", "deliverables",
    "test_falsifier_or_gate", "rollback_or_recovery", "protected_gates",
    "expected_disposition", "novelty_against_prior_chain",
}
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
FROZEN_LINE_ENDING_HASH_ALIASES = {
    (
        "docs/sable-rook/v643-v3/provenance/frozen-chain-proposal-index.json",
        "0078dbc08c7edd4adb398abfbf66ca9f04bbddda07c0e8fe328a7cf0c633b4ca",
        "2d91dcf5b4210a573168e26a2ceb3bfbf37d7d7dbf98dc2ef5331ffd4d0ccda2",
    )
}


def normalized(path: Path) -> bytes:
    return engine.normalized_bytes(path)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def frozen_hash_matches(path: Path, declared: str) -> bool:
    observed = hashlib.sha256(path.read_bytes()).hexdigest()
    if observed == declared:
        return True
    normalized_path = path.as_posix().lower()
    return any(
        normalized_path.endswith(suffix)
        and declared == legacy_declared
        and observed == legacy_observed
        for suffix, legacy_declared, legacy_observed in FROZEN_LINE_ENDING_HASH_ALIASES
    )


def is_ancestor(repo: Path, ancestor: str, descendant: str = "HEAD") -> bool:
    return subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=repo).returncode == 0


def validate(repo: Path, phase: Path | None = None, allow_pending_snapshot: bool = False) -> dict[str, Any]:
    repo = repo.resolve()
    phase = (phase or repo / "docs/orin-thale/v643-v4").resolve()
    checks: list[dict[str, Any]] = []
    issues: list[str] = []

    def check(label: str, condition: bool, detail: Any = None) -> None:
        passed = bool(condition)
        checks.append({"label": label, "passed": passed, "detail": detail})
        if not passed:
            issues.append(label if detail is None else f"{label}: {detail}")

    def read(relative: str) -> Any:
        target = phase / relative
        try:
            value = load(target)
            check(f"json:{relative}", True)
            return value
        except Exception as exc:  # pragma: no cover - diagnostic
            check(f"json:{relative}", False, str(exc))
            return {}

    required = [
        "x1-proposals.json", "x1-preregistration.md", "x2-proposal-ledger.json",
        "phase-truth.json", "complete-incomplete-checklist.json", "retained-negative-register.json",
        "exact-open-gate-register.json", "threat-model.json", "v643-v4-integrated-overview.md",
        "wellbeing-check.md", "evidence/evidence-ledger.json", "reproduction/manifest.json",
        "reproduction/independent-team-gap.json", "reproduction/evidence-snapshot-plan.json",
        "reproduction/x1-content-seal.json", "deliverables/v643-v4-boundary-evidence-report.html",
        "accessibility/static-report-receipt.json", "environment/x2-execution-receipt.json",
        "sources/source-ledger.json", "provenance/frozen-chain-proposal-index.json",
        "provenance/prior-proposal-collision-audit.json", "validation/x1-exact-file-set.json",
        "validation/x1-privacy-scan.json", "validation/x1-validation.json",
        "tooling/currency-review.json", "tooling/executed-toolchain.json",
        "stage20/domain-veto-evidence-board.json",
    ]
    for relative in required:
        check(f"required:{relative}", (phase / relative).is_file())

    json_files = sorted(phase.rglob("*.json"))
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
            check(f"all-json:{path.relative_to(phase).as_posix()}", True)
        except Exception as exc:  # pragma: no cover - diagnostic
            check(f"all-json:{path.relative_to(phase).as_posix()}", False, str(exc))

    x1 = read("x1-proposals.json")
    proposals = list(x1.get("proposals", []))
    check("phase-id", x1.get("phase") == engine.PHASE, x1.get("phase"))
    check("owner", x1.get("owner") == engine.OWNER, x1.get("owner"))
    check("source-commit", x1.get("source_revision") == engine.SOURCE_COMMIT, x1.get("source_revision"))
    check("source-seal", x1.get("source_seal_revision") == engine.SOURCE_SEAL)
    check("x1-ancestor", is_ancestor(repo, engine.X1_COMMIT))
    check("source-ancestor", is_ancestor(repo, engine.SOURCE_COMMIT))
    check("seal-ancestor", is_ancestor(repo, engine.SOURCE_SEAL))
    check("proposal-count", len(proposals) == 10)
    check("prior-frozen-count", x1.get("prior_frozen_proposal_count") == 180)
    check("truth-vocabulary", x1.get("outcome_classes") == list(engine.TRUTH_LABELS))
    check("expected-not-results", x1.get("expected_counts_are_results") is False)
    ids = [row.get("proposal_id") for row in proposals]
    titles = [row.get("title") for row in proposals]
    check("proposal-ids-unique", len(ids) == len(set(ids)) == 10)
    check("proposal-titles-unique", len(titles) == len(set(titles)) == 10)
    for proposal in proposals:
        pid = proposal.get("proposal_id", "missing")
        for field in sorted(REQUIRED_PROPOSAL_FIELDS):
            check(f"proposal-field:{pid}:{field}", proposal.get(field) not in (None, "", []))
        check(f"proposal-disposition:{pid}", proposal.get("expected_disposition") in engine.TRUTH_LABELS)
        check(f"proposal-deliverables:{pid}", len(proposal.get("deliverables", [])) == 3)
        check(f"proposal-sources:{pid}", len(proposal.get("authoritative_source_needs", [])) >= 1)
        check(f"proposal-gates:{pid}", len(proposal.get("protected_gates", [])) >= 3)
        for relative in proposal.get("deliverables", []):
            check(f"deliverable:{relative}", (phase / relative).is_file())
    expected = {label: sum(row.get("expected_disposition") == label for row in proposals) for label in engine.TRUTH_LABELS}
    check("expected-distribution", expected == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, expected)

    frozen = read("provenance/frozen-chain-proposal-index.json")
    check("frozen-inherited", frozen.get("inherited_record_count") == 180)
    check("frozen-new", frozen.get("new_record_count") == 10)
    check("frozen-effective", frozen.get("effective_record_count") == 190)
    check("frozen-no-duplicate-ids", frozen.get("exact_duplicate_ids") == [])
    check("frozen-no-duplicate-titles", frozen.get("exact_duplicate_titles") == [])
    inherited_index = repo / frozen.get("inherited_index", "missing")
    check("frozen-inherited-exists", inherited_index.is_file())
    if inherited_index.is_file():
        check("frozen-inherited-hash", frozen_hash_matches(inherited_index, frozen.get("inherited_index_sha256", "")))
    collision = read("provenance/prior-proposal-collision-audit.json")
    check("collision-prior", collision.get("prior_record_count") == 180)
    check("collision-new", collision.get("new_record_count") == 10)
    check("collision-max", collision.get("maximum_title_token_jaccard", 1) < collision.get("automatic_failure_threshold", 0))
    check("collision-semantic", collision.get("semantic_review_passed") is True)
    check("collision-x1-negatives", len(collision.get("x1_execution_negatives", [])) == 7)

    sources = read("sources/source-ledger.json")
    check("sources-effective", sources.get("effective_source_count") == 120)
    check("sources-added", sources.get("added_source_count") == 10)
    check("sources-status", sources.get("effective_status_counts") == {"current": 48, "stable": 63, "draft": 6, "watch": 3})
    check("sources-status-sum", sum(sources.get("effective_status_counts", {}).values()) == 120)

    x1_validation = read("validation/x1-validation.json")
    check("x1-validation-valid", x1_validation.get("valid") is True)
    check("x1-repository-suite", x1_validation.get("repository_tests") == {"passed": 372, "total": 372})
    check("x1-x2-absent", x1_validation.get("x2_implementation_files") == 0 and x1_validation.get("x2_outcome_files") == 0)
    x1_seal = read("reproduction/x1-content-seal.json")
    check("x1-seal-commit", x1_seal.get("x1_commit") == engine.X1_COMMIT)
    check("x1-seal-count", x1_seal.get("entry_count") == 27)
    check("x1-seal-unchanged", x1_seal.get("all_unchanged") is True and all(row.get("unchanged") for row in x1_seal.get("entries", [])))
    for row in x1_seal.get("entries", []):
        target = repo / row["repo_path"]
        check(f"x1-seal-exists:{row['repo_path']}", target.is_file())
        if target.is_file():
            check(f"x1-seal-working-hash:{row['repo_path']}", engine.normalized_sha256(target) == row["working_sha256_lf_normalized"])

    evaluations = engine.evaluate_catalog()
    check("fixture-groups", len(evaluations) == 10)
    check("fixture-cases", sum(len(rows) for rows in evaluations.values()) == 80)
    check("fixture-rejections", sum(not row["accepted"] for rows in evaluations.values() for row in rows) == 70)
    for pid, rows in evaluations.items():
        check(f"fixture-count:{pid}", len(rows) == 8)
        check(f"fixture-accepted:{pid}", sum(row["accepted"] for row in rows) == 1)
        for row in rows:
            check(f"fixture-match:{row['case_id']}", row["matched_expectation"], row["reasons"])

    x2 = read("x2-proposal-ledger.json")
    check("x2-x1-binding", x2.get("x1_commit") == engine.X1_COMMIT)
    check("x2-order", x2.get("x1_before_x2_preserved") is True)
    check("x2-counts", x2.get("proposal_count") == 10 and x2.get("case_count") == 80 and x2.get("synthetic_rejection_count") == 70)
    check("x2-distribution", x2.get("distribution") == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
    check("x2-row-count", len(x2.get("proposals", [])) == 10)
    for row in x2.get("proposals", []):
        check(f"x2-row-cases:{row['proposal_id']}", row.get("case_count") == 8 and row.get("accepted") == 1 and row.get("rejected") == 7)
        check(f"x2-no-external-claims:{row['proposal_id']}", row.get("external_claims_established") == [])

    evidence = read("evidence/evidence-ledger.json")
    zero_fields = ["empirical_rows", "real_participants", "real_arms", "real_raters", "real_keys_or_proofs", "legal_or_cultural_ratifications", "independent_team_returns", "different_architecture_returns"]
    for field in zero_fields:
        check(f"evidence-zero:{field}", evidence.get(field) == 0)

    negatives = read("retained-negative-register.json")
    inherited = load(repo / "docs/sable-rook/v643-v3/retained-negative-register.json")["negatives"]
    expected_negative_count = 637 + 70 + 7 + len(engine.X2_OPERATIONAL_NEGATIVES)
    check("negatives-inherited-count", negatives.get("inherited_count") == 637)
    check("negatives-first-637-exact", negatives.get("negatives", [])[:637] == inherited)
    check("negatives-synthetic-count", negatives.get("new_synthetic_count") == 70)
    check("negatives-x1-count", negatives.get("x1_operational_count") == 7)
    check("negatives-x2-count", negatives.get("x2_operational_count") == len(engine.X2_OPERATIONAL_NEGATIVES))
    check("negatives-total", negatives.get("negative_count") == len(negatives.get("negatives", [])) == expected_negative_count)
    check("negatives-unique", len({row.get("negative_id") for row in negatives.get("negatives", [])}) == expected_negative_count)
    check("negatives-retained", negatives.get("all_retained") is True and negatives.get("erasure_permitted") is False)
    for row in negatives.get("negatives", []):
        check(f"negative-retained:{row.get('negative_id')}", row.get("retained") is True)

    gates = read("exact-open-gate-register.json")
    check("open-gaps-five", gates.get("open_gap_count") == len(gates.get("open_gaps", [])) == 5)
    check("exact-gates-six", gates.get("exact_gate_count") == len(gates.get("exact_gates", [])) == 6)
    check("gates-visible", gates.get("all_visible") is True and gates.get("none_silently_closed") is True)
    gate_text = json.dumps(gates, ensure_ascii=False)
    check("maori-spelling-current", "Māori" in gate_text and "MÄori" not in gate_text)

    truth = read("phase-truth.json")
    check("truth-distribution", truth.get("distribution") == x2.get("distribution"))
    check("truth-negative-count", truth.get("retained_negative_count") == expected_negative_count)
    check("truth-gates", truth.get("open_gap_count") == 5 and truth.get("exact_gate_count") == 6)
    check("truth-focus", truth.get("primary_focus") == "GMUT Mind" and truth.get("all_three_pillars_preserved") is True)
    check("truth-protected-claims", all(value is False for value in truth.get("protected_claims", {}).values()))
    check("truth-verdict", truth.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20")
    check("truth-route", truth.get("route_state") == "PREPARED_NOT_SENT" and truth.get("outbound_message_count") == 0 and truth.get("successor_task_count") == 0 and truth.get("subagent_count") == 0)
    if allow_pending_snapshot:
        check("truth-snapshot-state-pending-allowed", truth.get("state") in {"EVIDENCE_CANDIDATE", "EVIDENCE_VERIFIED", "CLOSEOUT_CANDIDATE", "SEALED_CANDIDATE", "FINAL_HEAD_CANDIDATE"})
    else:
        check("truth-same-owner-verified", truth.get("same_owner_repeatability") is True)
        receipt = phase / "reproduction/evidence-snapshot-receipt.json"
        check("evidence-snapshot-receipt", receipt.is_file() and load(receipt).get("valid") is True if receipt.is_file() else False)
    check("truth-independent-false", truth.get("independent_team_reproduction") is False)

    checklist = read("complete-incomplete-checklist.json")
    check("checklist-complete-nonempty", len(checklist.get("complete", [])) >= 8)
    check("checklist-incomplete-visible", len(checklist.get("incomplete", [])) >= 8)
    check("checklist-stage20-incomplete", any("Stage 20" in item for item in checklist.get("incomplete", [])))
    threat = read("threat-model.json")
    check("threat-count", threat.get("threat_count") == len(threat.get("threats", [])) >= 14)
    check("threat-security-boundary", threat.get("exhaustive_security") is False and threat.get("independent_security_review") is False)
    check("rotation-scope", threat.get("resource_ceilings", {}).get("owner_generated_files") == 15000)

    report_path = phase / "deliverables/v643-v4-boundary-evidence-report.html"
    report = report_path.read_text(encoding="utf-8") if report_path.is_file() else ""
    for marker in ['<html lang="en-NZ">', 'href="#main"', '<main id="main">', '<caption>', ':focus-visible', 'NOT_READY_FOR_STAGE_20', 'Māori']:
        check(f"report-marker:{marker}", marker in report)
    forbidden_report_text = [
        ("maori-mojibake", "MÄori"),
        ("complete-wcag-claim", "complete WCAG conformance"),
        ("gmut-confirmation-claim", "GMUT is empirically confirmed"),
        ("thos-superiority-claim", "THOS is superior"),
        ("freed-id-production-claim", "production-ready Freed ID"),
    ]
    for label, forbidden in forbidden_report_text:
        check(f"report-forbidden:{label}", forbidden not in report)
    access = read("accessibility/static-report-receipt.json")
    check("access-static", access.get("static") is True and access.get("script_dependency") is False)
    check("access-manual-reserved", access.get("manual_accessibility_evaluation") is False and access.get("affected_user_evaluation") is False and access.get("complete_accessibility_conformance") is False)
    overview_words = len((phase / "v643-v4-integrated-overview.md").read_text(encoding="utf-8").split())
    check("overview-three-page-equivalent", overview_words >= 1200, overview_words)

    stage20 = read("stage20/domain-veto-evidence-board.json")
    check("stage20-vetoes", len(stage20.get("vetoes", [])) >= 6 and all(row.get("decision") == "veto" for row in stage20.get("vetoes", [])))
    check("stage20-no-compensation", stage20.get("compensation_across_domains_allowed") is False)
    check("stage20-verdict", stage20.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20")

    manifest = read("reproduction/manifest.json")
    entries = manifest.get("entries", [])
    check("manifest-count", manifest.get("entry_count") == len(entries) == 77, manifest.get("entry_count"))
    paths = [row.get("repo_path") for row in entries]
    check("manifest-unique", len(paths) == len(set(paths)))
    check("manifest-normalization", manifest.get("text_normalization") == "CRLF and CR normalized to LF before hashing")
    check("manifest-independent-false", manifest.get("independent_team_reproduction") is False)
    if allow_pending_snapshot:
        check("manifest-state", manifest.get("snapshot_state") in {"pending", "verified"})
    else:
        check("manifest-state", manifest.get("snapshot_state") == "verified")
    for row in entries:
        target = repo / row["repo_path"]
        check(f"manifest-exists:{row['repo_path']}", target.is_file())
        if target.is_file():
            data = normalized(target)
            check(f"manifest-hash:{row['repo_path']}", hashlib.sha256(data).hexdigest() == row["sha256_lf_normalized"])
            check(f"manifest-bytes:{row['repo_path']}", len(data) == row["bytes_lf_normalized"])

    retained_failure_receipts = {
        "validation/candidate-validation-summary.json",
        "validation/candidate-validation-rerun.json",
    }
    current_text_files = [
        path for path in phase.rglob("*")
        if path.is_file()
        and path.name != "retained-negative-register.json"
        and path.relative_to(phase).as_posix() not in retained_failure_receipts
    ]
    mojibake_hits = []
    for path in current_text_files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "MÄori" in text:
            mojibake_hits.append(path.relative_to(phase).as_posix())
    check("current-maori-mojibake-zero", not mojibake_hits, mojibake_hits)

    privacy_paths = [path for path in phase.rglob("*") if path.is_file()] + [
        repo / "scripts/ghc_family_boundary_evidence.py",
        repo / "scripts/ghc_family_boundary_evidence_validator.py",
        repo / "scripts/ghc_family_boundary_evidence_minimal.py",
        repo / "scripts/build_ghc_family_boundary_evidence_report.py",
        repo / "tests/test_ghc_family_v643_v4.py",
    ]
    privacy_hits = []
    scanned = 0
    for path in sorted(set(privacy_paths)):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for name, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                privacy_hits.append({"repo_path": path.relative_to(repo).as_posix(), "pattern": name})
    check("privacy-zero-hits", not privacy_hits, privacy_hits)
    check("owner-footprint-below-threshold", len([p for p in phase.rglob("*") if p.is_file()]) + 8 < 15000)

    return {
        "schema": "ghc.family.v643-v4.boundary-evidence-validation.v1",
        "phase": engine.PHASE,
        "owner": engine.OWNER,
        "valid": not issues,
        "check_count": len(checks),
        "passed_count": sum(row["passed"] for row in checks),
        "issue_count": len(issues),
        "issues": issues,
        "checks": checks,
        "json_files_parsed": len(json_files),
        "privacy_scan": {"files": scanned, "pattern_classes": len(PRIVATE_PATTERNS), "hits": len(privacy_hits)},
        "observed_distribution": x2.get("distribution"),
        "case_count": x2.get("case_count"),
        "retained_negative_count": negatives.get("negative_count"),
        "manifest_entry_count": manifest.get("entry_count"),
        "overview_word_count": overview_words,
        "allow_pending_snapshot": allow_pending_snapshot,
        "boundary": engine.BOUNDARY,
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def json_parse_receipt(phase: Path) -> dict[str, Any]:
    files = sorted(phase.rglob("*.json"))
    issues = []
    for path in files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - diagnostic
            issues.append({"path": path.relative_to(phase).as_posix(), "error": str(exc)})
    return {
        "schema": "ghc.family.v643-v4.json-parse-receipt.v1",
        "phase": engine.PHASE,
        "owner": engine.OWNER,
        "json_files_parsed": len(files),
        "issue_count": len(issues),
        "issues": issues,
        "valid": not issues,
        "boundary": "JSON syntax validity does not establish semantic truth or any protected external claim.",
    }


def staged_review(repo: Path, phase: Path) -> dict[str, Any]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=repo,
        check=True,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
    )
    names = sorted(line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip())
    x1_files = set(load(phase / "validation/x1-exact-file-set.json")["files"])
    x1_staged = sorted(x1_files.intersection(names))
    x2_external = {
        "scripts/ghc_family_boundary_evidence.py",
        "scripts/ghc_family_boundary_evidence_validator.py",
        "scripts/ghc_family_boundary_evidence_minimal.py",
        "scripts/build_ghc_family_boundary_evidence_report.py",
        "tests/test_ghc_family_v643_v4.py",
    }
    unexpected = [name for name in names if not name.startswith("docs/orin-thale/v643-v4/") and name not in x2_external]
    diff_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8")
    name_hash = hashlib.sha256(("\n".join(names) + "\n").encode("utf-8")).hexdigest()
    valid = bool(names) and not x1_staged and not unexpected and diff_check.returncode == 0
    return {
        "schema": "ghc.family.v643-v4.evidence-staged-review.v1",
        "phase": engine.PHASE,
        "owner": engine.OWNER,
        "file_count": len(names),
        "files": names,
        "sort_order": "Python Unicode code-point lexicographic order over repository-relative POSIX paths",
        "staged_name_list_sha256": name_hash,
        "x1_frozen_file_count_staged": len(x1_staged),
        "x1_frozen_files_staged": x1_staged,
        "unexpected_staged_file_count": len(unexpected),
        "unexpected_staged_files": unexpected,
        "diff_check_passed": diff_check.returncode == 0,
        "diff_check_output": diff_check.stdout.strip(),
        "owner_generated_file_threshold": 15000,
        "under_threshold": len(names) < 15000,
        "valid": valid,
        "boundary": "Exact staged-file review proves Git scope and x1 immutability for this commit, not scientific or institutional validity.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--phase", type=Path)
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-receipt-output", type=Path)
    parser.add_argument("--staged-review-output", type=Path)
    args = parser.parse_args()
    result = validate(args.repo, args.phase, args.allow_pending_snapshot)
    if args.output:
        write_json(args.output, result)
    if args.json_receipt_output:
        write_json(args.json_receipt_output, json_parse_receipt((args.phase or args.repo / "docs/orin-thale/v643-v4").resolve()))
    if args.staged_review_output:
        write_json(args.staged_review_output, staged_review(args.repo.resolve(), (args.phase or args.repo / "docs/orin-thale/v643-v4").resolve()))
    print(json.dumps({key: result[key] for key in ("valid", "check_count", "passed_count", "issue_count", "issues", "json_files_parsed", "privacy_scan", "manifest_entry_count")}, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
