#!/usr/bin/env python3
"""Validate the bounded Eiren Kestrel v644-v5 x1/x2 packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


PHASE_REL = Path("docs/eiren-kestrel/v644-v5")
X1_COMMIT = "8a4323e25aeff7a3b9abce898b460cf125e5db83"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}
EXPECTED_DISTRIBUTION = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
PRIVATE_ROUTE_FIELD = "source" + "_" + "thread" + "_" + "id"


PRIVATE_PATTERNS = {
    "raw_uuid": re.compile(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        re.IGNORECASE,
    ),
    "delegation_markup": re.compile(
        r"<(?:codex_delegation|" + re.escape(PRIVATE_ROUTE_FIELD) + r")>",
        re.IGNORECASE,
    ),
    "private_local_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.IGNORECASE),
    "private_uri": re.compile(r"\b(?:app|plugin)://", re.IGNORECASE),
    "credential_assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"
    ),
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def index_blob(repo: Path, relative_path: str) -> bytes:
    return subprocess.check_output(
        ["git", "-C", str(repo), "show", f":{relative_path}"],
    )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def build_manifest(repo: Path, phase: Path) -> dict[str, Any]:
    exclusions = {
        "reproduction/evidence-manifest.json",
        "reproduction/final-manifest.json",
    }
    entries = []
    for path in sorted(p for p in phase.rglob("*") if p.is_file()):
        rel = path.relative_to(phase).as_posix()
        if rel in exclusions or rel.startswith("validation/"):
            continue
        rel_repo = path.relative_to(repo).as_posix()
        blob = index_blob(repo, rel_repo)
        entries.append({"path": rel, "sha256": hashlib.sha256(blob).hexdigest(), "bytes": len(blob)})
    return {
        "schema": "ghc.family.v644-v5.evidence-manifest.v2",
        "phase": "v644-gmut-thos-v5-x1-x2",
        "hash_domain": "git_index_blob_bytes",
        "working_tree_line_endings_ignored": True,
        "entry_count": len(entries),
        "entries": entries,
        "same_owner_repeatability_only": True,
        "independent_team_reproduction": False,
        "boundary": "This byte manifest supports local repeatability and change detection, not independent scientific reproduction.",
    }


def validate(
    repo: Path,
    phase: Path,
    allow_pending_lean: bool,
    expected_head: str | None,
) -> dict[str, Any]:
    checks: list[str] = []
    issues: list[str] = []

    def check(condition: bool, name: str, detail: str | None = None) -> None:
        checks.append(name)
        if not condition:
            issues.append(detail or name)

    required = [
        "x1-proposals.json",
        "x2-proposal-ledger.json",
        "phase-truth.json",
        "retained-negative-register.json",
        "exact-open-gate-register.json",
        "threat-model.json",
        "complete-incomplete-checklist.json",
        "evidence/evidence-ledger.json",
        "reproduction/evidence-manifest.json",
        "tooling/executed-toolchain.json",
        "tooling/ghc-family-method-flow-state-skill-receipt.json",
        "method-flow/method-flow-state.json",
        "method-flow/workaround-validation-ledger.json",
        "method-flow/recurrence-prevention-recommendations.md",
        "deliverables/v644-v5-boundary-evidence-report.html",
        "deliverables/v644-v5-final-integrated-overview.md",
        "repository/lean-companion-validation.json",
        "stage20/terminal-evidence-board.json",
    ]
    for rel in required:
        check((phase / rel).is_file(), f"required:{rel}")

    parsed: dict[Path, Any] = {}
    json_issues: list[str] = []
    for path in sorted(phase.rglob("*.json")):
        try:
            parsed[path] = load(path)
            check(True, f"json:{path.relative_to(phase).as_posix()}")
        except Exception as exc:
            json_issues.append(f"{path.relative_to(phase).as_posix()}:{type(exc).__name__}")
            check(False, f"json:{path.relative_to(phase).as_posix()}")

    proposals = load(phase / "x1-proposals.json")
    ledger = load(phase / "x2-proposal-ledger.json")
    check(proposals["proposal_count"] == 10, "x1_proposal_count")
    check(proposals["prior_frozen_proposal_count"] == 270, "prior_proposal_count")
    check(ledger["proposal_count"] == 10 and len(ledger["rows"]) == 10, "x2_proposal_count")
    check(set(row["observed_disposition"] for row in ledger["rows"]).issubset(ALLOWED), "allowed_outcomes")
    check(ledger["observed_distribution"] == EXPECTED_DISTRIBUTION, "observed_distribution")
    check(ledger["all_expected_dispositions_matched"] is True, "expected_observed_match")
    check(ledger["total_case_count"] == 70, "case_count_70")
    check(ledger["total_matched_count"] == 70, "case_match_70")
    for row in ledger["rows"]:
        check(row["case_count"] == 7 and row["matched_count"] == 7, f"cases:{row['proposal_id']}")
        for rel in row["deliverables"]:
            check((phase / rel).is_file(), f"deliverable:{rel}")

    negatives = load(phase / "retained-negative-register.json")
    check(negatives["inherited_count"] == 1399, "inherited_negatives")
    check(negatives["x1_operational_count"] == 9, "x1_negative_count")
    check(negatives["new_synthetic_count"] == 70, "synthetic_negative_count")
    check(negatives["x2_operational_count"] == 10, "x2_negative_count")
    check(negatives["negative_count"] == 1488, "effective_negative_count")
    check(len(negatives["negatives"]) == negatives["negative_count"], "negative_array_count")
    check(negatives["duplicate_negative_ids"] == [], "negative_ids_unique")
    check(negatives["all_retained"] is True and negatives["erasure_permitted"] is False, "negative_retention")

    gates = load(phase / "exact-open-gate-register.json")
    check(gates["open_gap_count"] == 5 and len(gates["open_gaps"]) == 5, "open_gaps_5")
    check(gates["exact_gate_count"] == 6 and len(gates["exact_gates"]) == 6, "exact_gates_6")
    check(gates["all_visible"] is True and gates["none_silently_closed"] is True, "gates_visible")

    method = load(phase / "method-flow/method-flow-state.json")
    method_validation = load(phase / "method-flow/workaround-validation-ledger.json")
    check(method["schema"] == "ghc.family.method-flow-state.v1", "method_schema")
    method_count = method["counts"]["methods"]
    check(method_count >= 8, "method_count_minimum_8")
    preferred = method["counts"]["states"]["preferred"]
    candidate = method["counts"]["states"]["candidate"]
    if allow_pending_lean:
        check(
            preferred + candidate == method_count and candidate == 1,
            "method_pending_lean",
        )
    else:
        check(preferred == method_count and candidate == 0, "method_all_preferred")
    check(method["counts"]["witness_results"]["fail"] >= 1, "failed_witness_retained")
    check(method_validation["validation"]["valid"] is True, "method_validation")
    if not allow_pending_lean:
        check(method_validation["pending_methods"] == [], "no_pending_methods")

    lean = load(phase / "repository/lean-companion-validation.json")
    if allow_pending_lean:
        check(lean.get("observed_disposition") == "completed" or lean.get("valid") is True, "lean_placeholder_or_valid")
    else:
        check(lean.get("valid") is True, "lean_valid")
        check(lean.get("selected_file_count", 15000) < 15000, "lean_under_limit")
        check(lean.get("tracked_file_count") == lean.get("selected_file_count"), "lean_tracked_parity")
        check(lean.get("canonical_repository_replaced") is False, "canonical_not_replaced")
        check(lean.get("public_remote_configured") is False, "no_public_remote")
        check(lean.get("targeted_test_passed") is True, "lean_targeted_test")
        check(lean.get("independent_reproduction") is False, "lean_not_independent")

    evidence = load(phase / "evidence/evidence-ledger.json")
    check(all(value == 0 for value in evidence["real_or_external_counts"].values()), "real_external_counts_zero")
    check(all(value is False for value in evidence["protected_claims"].values()), "protected_claims_false")
    check(evidence["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", "evidence_terminal")

    truth = load(phase / "phase-truth.json")
    check(truth["retained_negative_count"] == negatives["negative_count"], "truth_negative_count")
    check(truth["open_gap_count"] == 5 and truth["exact_gate_count"] == 6, "truth_gate_counts")
    check(truth["outbound_message_count"] == 0 and truth["successor_task_count"] == 0, "no_route_action")
    check(all(value is False for value in truth["protected_claims"].values()), "truth_protected_false")
    check(truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", "truth_terminal")

    report = (phase / "deliverables/v644-v5-boundary-evidence-report.html").read_text(encoding="utf-8")
    for marker in [
        '<html lang="en">',
        'href="#main"',
        '<main id="main"',
        ":focus-visible",
        "<caption>",
        "NOT_READY_FOR_STAGE_20",
    ]:
        check(marker in report, f"report_marker:{marker}")
    check("complete WCAG conformance" not in report, "report_no_complete_claim")
    overview_words = len((phase / "deliverables/v644-v5-final-integrated-overview.md").read_text(encoding="utf-8").split())
    check(overview_words >= 1200, "overview_three_page_equivalent", f"overview words={overview_words}")

    manifest = load(phase / "reproduction/evidence-manifest.json")
    check(manifest["entry_count"] == len(manifest["entries"]), "manifest_count")
    manifest_paths = [row["path"] for row in manifest["entries"]]
    check(len(manifest_paths) == len(set(manifest_paths)), "manifest_paths_unique")
    for row in manifest["entries"]:
        path = phase / row["path"]
        check(path.is_file(), f"manifest_exists:{row['path']}")
        if path.is_file():
            rel_repo = path.relative_to(repo).as_posix()
            try:
                blob = index_blob(repo, rel_repo)
            except subprocess.CalledProcessError:
                blob = b""
            check(hashlib.sha256(blob).hexdigest() == row["sha256"], f"manifest_hash:{row['path']}")
            check(len(blob) == row["bytes"], f"manifest_size:{row['path']}")
    check(manifest["same_owner_repeatability_only"] is True, "manifest_same_owner")
    check(manifest["independent_team_reproduction"] is False, "manifest_not_independent")

    privacy_hits: list[dict[str, str]] = []
    scanned = 0
    for path in sorted(p for p in phase.rglob("*") if p.is_file()):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                privacy_hits.append({"file": path.relative_to(phase).as_posix(), "pattern_class": label})
    check(not privacy_hits, "privacy_zero_hits", json.dumps(privacy_hits))
    check(len([p for p in phase.rglob("*") if p.is_file()]) < 15000, "owner_files_under_limit")

    head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True, encoding="utf-8").strip()
    ancestry = subprocess.run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", X1_COMMIT, head],
        check=False,
    ).returncode == 0
    check(ancestry, "x1_ancestral")
    if expected_head:
        check(head == expected_head, "exact_expected_head", f"expected {expected_head}, found {head}")

    return {
        "schema": "ghc.family.v644-v5.validation.v1",
        "phase": "v644-gmut-thos-v5-x1-x2",
        "owner": "Eiren Kestrel",
        "allow_pending_lean": allow_pending_lean,
        "head": head,
        "expected_head": expected_head,
        "check_count": len(checks),
        "issue_count": len(issues),
        "checks": checks,
        "issues": issues,
        "json_files_parsed": len(parsed),
        "json_parse_issues": json_issues,
        "privacy_scan": {
            "files_scanned": scanned,
            "pattern_classes": len(PRIVATE_PATTERNS),
            "hits": privacy_hits,
        },
        "observed_distribution": ledger["observed_distribution"],
        "mutation_case_count": ledger["total_case_count"],
        "retained_negative_count": negatives["negative_count"],
        "open_gap_count": gates["open_gap_count"],
        "exact_gate_count": gates["exact_gate_count"],
        "manifest_entry_count": manifest["entry_count"],
        "overview_word_count": overview_words,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": not issues,
        "boundary": "Validation covers bounded repository evidence only; it does not establish empirical, participant, production, legal, cultural, accessibility-complete, exhaustive-security, deployment, or independent-reproduction claims.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--phase-dir", type=Path, default=PHASE_REL)
    parser.add_argument("--allow-pending-lean", action="store_true")
    parser.add_argument("--refresh-manifest", action="store_true")
    parser.add_argument("--expected-head")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    phase = (repo / args.phase_dir).resolve() if not args.phase_dir.is_absolute() else args.phase_dir.resolve()
    if args.refresh_manifest:
        write_json(phase / "reproduction/evidence-manifest.json", build_manifest(repo, phase))
    result = validate(repo, phase, args.allow_pending_lean, args.expected_head)
    if args.output:
        output = (repo / args.output).resolve() if not args.output.is_absolute() else args.output.resolve()
        write_json(output, result)
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
