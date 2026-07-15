#!/usr/bin/env python3
"""Validate and receipt the Orin Thale v645-v6 x1-only freeze."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v645-v6"
PHASE_PREFIX = "docs/orin-thale/v645-v6/"
RECEIPTS = {
    f"{PHASE_PREFIX}validation/x1-exact-file-set.json",
    f"{PHASE_PREFIX}validation/x1-privacy-scan.json",
    f"{PHASE_PREFIX}validation/x1-scoped-check-receipt.json",
    f"{PHASE_PREFIX}validation/x1-staged-review.json",
    f"{PHASE_PREFIX}validation/x1-stale-label-review.json",
    f"{PHASE_PREFIX}validation/x1-structural.json",
    f"{PHASE_PREFIX}reproduction/x1-content-seal.json",
}
SCRIPT_FILES = {
    "scripts/build_ghc_family_v645_v6_preregistration.py",
    "scripts/ghc_family_v645_v6_definitions.py",
    "scripts/ghc_family_v645_v6_x1_review.py",
    "tests/test_ghc_family_v645_v6_x1.py",
}
PRIVATE_PATTERNS = {
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_local_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
    "private_uri": re.compile(r"\b(?:app|plugin)://", re.I),
    "private_markup": re.compile(r"<(?:codex_delegation|source_thread_id)>", re.I),
    "private_callable": re.compile(r"\b(?:threadId|callable_id|session_stream)\b", re.I),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def git(*args: str, binary: bool = False) -> str | bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=not binary, encoding=None if binary else "utf-8")


def staged_paths() -> list[str]:
    return sorted(path for path in str(git("diff", "--cached", "--name-only", "--diff-filter=ACMR")).splitlines() if path)


def blob(path: str) -> bytes:
    return bytes(git("show", f":{path}", binary=True))


def phase_paths(include_receipts: bool = True) -> list[str]:
    paths = [path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file()]
    return sorted(path for path in paths if include_receipts or path not in RECEIPTS)


def privacy(paths: list[str], from_index: bool = False) -> dict[str, Any]:
    hits: list[dict[str, str]] = []
    for path in paths:
        if not path.startswith(PHASE_PREFIX):
            continue
        raw = blob(path) if from_index else (ROOT / path).read_bytes()
        text = raw.decode("utf-8")
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                hits.append({"path": path, "pattern_class": label})
    return {
        "schema": "ghc.family.v645-v6.privacy-scan.v1",
        "files_scanned": len([p for p in paths if p.startswith(PHASE_PREFIX)]),
        "pattern_classes": sorted(PRIVATE_PATTERNS),
        "hits": hits,
        "hit_count": len(hits),
        "valid": not hits,
        "boundary": "Five-plus structural privacy classes are screened; zero hits is not a privacy-complete claim.",
    }


def structural() -> dict[str, Any]:
    issues: list[str] = []
    required = [
        "identity-receipt.json",
        "x1-proposals.json",
        "x1-preregistration.md",
        "approval-packets/x1-approval-portfolio.json",
        "prototypes/x1-skill-runner-plan.json",
        "maintenance/x1-clean-refine-plan.json",
        "provenance/prior-proposal-collision-audit.json",
        "provenance/prior-portfolio-collision-audit.json",
        "provenance/rejected-candidate-register.json",
        "sources/source-ledger.json",
        "sources/source-ledger.md",
        "environment/startup-receipt.json",
        "environment/version-receipt.json",
        "environment/sandbox-readonly-audit.json",
        "environment/rotation-guard.json",
        "focus/primary-focus-receipt.json",
        "method-flow/method-flow-state.json",
        "method-flow/runner-validation.json",
        "orchestration/phase-update.json",
        "validation/x1-operational-negatives.json",
        "wellbeing-check.md",
        "tooling/ghc-family-index.json",
        "tooling/ghc-family-index.md",
    ]
    for item in required:
        if not (PHASE / item).is_file():
            issues.append(f"missing:{item}")

    proposals = load(PHASE / "x1-proposals.json")
    fields = {
        "proposal_id", "title", "mission_surface", "hypothesis", "null_or_failure", "approval_class",
        "execution_lane", "current_primary_or_official_source_needs", "concrete_artifacts",
        "test_falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
        "expected_disposition", "novelty_against_360_frozen_proposals",
    }
    rows = proposals.get("proposals", [])
    if len(rows) != 10:
        issues.append("proposal_count")
    if proposals.get("prior_frozen_proposal_count") != 360 or proposals.get("frozen_chain_count_after_x1") != 370:
        issues.append("frozen_chain_count")
    if proposals.get("x2_execution_present") is not False:
        issues.append("x2_present")
    for row in rows:
        if not fields.issubset(row):
            issues.append(f"proposal_fields:{row.get('proposal_id')}")
        if row.get("expected_disposition") not in {"completed", "represented", "open_gap", "exact_gate"}:
            issues.append(f"outcome_class:{row.get('proposal_id')}")
        for field in ("current_primary_or_official_source_needs", "concrete_artifacts", "protected_gates"):
            if not row.get(field):
                issues.append(f"empty:{row.get('proposal_id')}:{field}")
    dispositions = {state: sum(row.get("expected_disposition") == state for row in rows) for state in ("completed", "represented", "open_gap", "exact_gate")}
    if dispositions != {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}:
        issues.append("expected_distribution")
    if len({row.get("title") for row in rows}) != 10:
        issues.append("duplicate_proposal_title")

    collision = load(PHASE / "provenance/prior-proposal-collision-audit.json")
    if collision.get("prior_frozen_proposal_count") != 360 or collision.get("exact_title_collision_count") != 0 or len(collision.get("comparisons", [])) != 10:
        issues.append("proposal_collision_audit")
    portfolios = load(PHASE / "approval-packets/x1-approval-portfolio.json")
    counts = portfolios.get("counts")
    if counts != {"safe_now": 20, "candidates": 12, "inherited_exact": 10, "inherited_blocked": 5}:
        issues.append("portfolio_counts")
    if portfolios.get("completion_credit_before_x2") != 0:
        issues.append("portfolio_completion_credit")
    p_collision = load(PHASE / "provenance/prior-portfolio-collision-audit.json")
    if p_collision.get("exact_collision_count") != 0:
        issues.append("portfolio_collision")
    plans = load(PHASE / "prototypes/x1-skill-runner-plan.json")
    if len(plans.get("skills", [])) != 12 or len(plans.get("runners", [])) != 6:
        issues.append("skill_runner_counts")
    if not all(item.get("x2_state") == "preregistered_not_built_or_used" for item in [*plans.get("skills", []), *plans.get("runners", [])]):
        issues.append("skill_runner_x2_leak")
    clean = load(PHASE / "maintenance/x1-clean-refine-plan.json")
    if len(clean.get("tasks", [])) != 20 or clean.get("completion_credit_before_x2") != 0 or clean.get("destructive_task_count") != 0:
        issues.append("cleanup_plan")
    source = load(PHASE / "sources/source-ledger.json")
    if not source.get("sources") or any(row.get("status") not in {"current", "stable", "draft", "watch"} for row in source.get("sources", [])):
        issues.append("source_status")
    if source.get("real_data_rows_ingested") != 0 or source.get("likelihood_evaluations") != 0:
        issues.append("source_data_leak")
    method = load(PHASE / "method-flow/method-flow-state.json")
    if method.get("schema") != "ghc.family.method-flow-state.v1" or method.get("counts", {}).get("methods") != 6:
        issues.append("method_flow")
    if method.get("counts", {}).get("states", {}).get("preferred") != 6 or method.get("counts", {}).get("witness_results") != {"fail": 6, "pass": 6}:
        issues.append("method_flow_witnesses")
    negatives = load(PHASE / "validation/x1-operational-negatives.json")
    if negatives.get("inherited_effective") != 2172 or negatives.get("preregistered_synthetic") != 70 or negatives.get("new_operational_count") != 6 or negatives.get("effective_after_x1") != 2248:
        issues.append("negative_counts")
    focus = load(PHASE / "focus/primary-focus-receipt.json")
    if focus.get("primary_trinity_pillar") != "GMUT Mind" or "maritime" not in focus.get("bounded_human_practice", ""):
        issues.append("focus")
    route = load(PHASE / "orchestration/terminal-route-plan.json")
    if route.get("current_state") != "PREPARED_NOT_SENT" or route.get("send_count") != 0:
        issues.append("route_state")
    for forbidden in ("phase-truth.json", "x2-proposal-ledger.json", "closeout-receipt.json", "final-validation-record.json"):
        if (PHASE / forbidden).exists():
            issues.append(f"x2_file:{forbidden}")
    for path in PHASE.rglob("*.md"):
        if len(re.findall(r"\b\w+\b", path.read_text(encoding="utf-8"))) > 6000:
            issues.append(f"word_cap:{path.relative_to(PHASE).as_posix()}")
    for path in PHASE.rglob("*"):
        if path.is_file():
            raw = path.read_bytes()
            try:
                raw.decode("utf-8")
            except UnicodeDecodeError:
                issues.append(f"utf8:{path.relative_to(PHASE).as_posix()}")
            if raw and not raw.endswith(b"\n"):
                issues.append(f"terminal_newline:{path.relative_to(PHASE).as_posix()}")
            if b"\r\n" in raw:
                issues.append(f"crlf:{path.relative_to(PHASE).as_posix()}")
    return {
        "schema": "ghc.family.v645-v6.x1-structural.v1",
        "phase": "v645-gmut-thos-v6-x1-x2",
        "proposal_count": len(rows),
        "expected_dispositions": dispositions,
        "json_document_count": len(list(PHASE.rglob("*.json"))),
        "owner_generated_file_count": len(phase_paths()),
        "rotation_threshold": 15000,
        "issues": sorted(set(issues)),
        "issue_count": len(set(issues)),
        "valid": not issues,
        "boundary": "X1 structural validation proves only preregistration integrity; it grants no x2 outcome credit.",
    }


def allowed_staged(path: str) -> bool:
    return path.startswith(PHASE_PREFIX) or path in SCRIPT_FILES


def write_receipts() -> dict[str, Any]:
    staged = staged_paths()
    core = sorted(path for path in staged if path not in RECEIPTS)
    unexpected = [path for path in staged if not allowed_staged(path)]
    structural_receipt = structural()
    privacy_receipt = privacy(core, from_index=True)
    stale_hits: list[dict[str, str]] = []
    for path in core:
        if path.startswith(PHASE_PREFIX):
            text = blob(path).decode("utf-8")
            for label, pattern in {
                "wrong_phase_owner": re.compile(r"\b(?:Tamar Vey|Sylven Arc|Eiren Kestrel|Ilyra Fen|Sable Rook)\b.*\bowner\b", re.I),
                "sent_route": re.compile(r'"current_state"\s*:\s*"SENT"', re.I),
                "stage20_ready": re.compile(r'(?<!NOT_)READY_FOR_STAGE_20'),
            }.items():
                if pattern.search(text):
                    stale_hits.append({"path": path, "class": label})
    manifest = [{"path": path, "sha256": hashlib.sha256(blob(path)).hexdigest(), "bytes": len(blob(path))} for path in core]
    exact = {
        "schema": "ghc.family.v645-v6.x1-exact-file-set.v1",
        "phase": "v645-gmut-thos-v6-x1-x2",
        "manifest_domain": "canonical_git_index_blob",
        "self_excluding_receipts": sorted(RECEIPTS),
        "core_file_count": len(core),
        "files": manifest,
        "unexpected_staged": unexpected,
        "valid": not unexpected,
    }
    staged_review = {
        "schema": "ghc.family.v645-v6.x1-staged-review.v1",
        "stage": "x1_only",
        "staged_core_file_count": len(core),
        "unexpected_staged": unexpected,
        "x2_implementation_files": [path for path in staged if "/x2-" in path or path.endswith("phase-truth.json")],
        "all_paths_owner_scoped_or_phase_tooling": not unexpected,
        "valid": not unexpected and structural_receipt["valid"] and privacy_receipt["valid"],
    }
    stale = {
        "schema": "ghc.family.v645-v6.x1-stale-label-review.v1",
        "files_reviewed": len(core),
        "hits": stale_hits,
        "valid": not stale_hits,
        "boundary": "Named predecessor and standby sibling references are allowed only as source, standby, or inheritance evidence; ownership and route states remain Orin-scoped.",
    }
    scoped = {
        "schema": "ghc.family.v645-v6.x1-scoped-check-receipt.v1",
        "scope": ["v645-v5 inherited packet", "v645-v6 x1 packet", "v645-v6 definitions and x1 review"],
        "full_repository_suite_run": False,
        "full_repository_suite_owner": "Eiren Kestrel only",
        "checks": {"structural": structural_receipt["valid"], "privacy": privacy_receipt["valid"], "stale_labels": stale["valid"], "staged_paths": not unexpected, "proposal_count": structural_receipt["proposal_count"] == 10},
        "valid": structural_receipt["valid"] and privacy_receipt["valid"] and stale["valid"] and not unexpected,
        "boundary": "This is a scoped x1 preregistration check, not x2 evidence, independent reproduction, or Stage 20 proof.",
    }
    seal = {
        "schema": "ghc.family.v645-v6.x1-content-seal.v1",
        "hash_domain": "canonical_git_index_blob",
        "self_excluding": sorted(RECEIPTS),
        "entry_count": len(manifest),
        "entries": manifest,
        "aggregate_sha256": hashlib.sha256("\n".join(f"{row['sha256']}  {row['path']}" for row in manifest).encode()).hexdigest(),
        "boundary": "The content seal fixes the x1 core bytes only; it grants no x2 or external truth credit.",
    }
    write(PHASE / "validation/x1-structural.json", structural_receipt)
    write(PHASE / "validation/x1-privacy-scan.json", privacy_receipt)
    write(PHASE / "validation/x1-stale-label-review.json", stale)
    write(PHASE / "validation/x1-exact-file-set.json", exact)
    write(PHASE / "validation/x1-staged-review.json", staged_review)
    write(PHASE / "validation/x1-scoped-check-receipt.json", scoped)
    write(PHASE / "reproduction/x1-content-seal.json", seal)
    return {"structural": structural_receipt, "privacy": privacy_receipt, "stale": stale, "staged": staged_review, "scoped": scoped, "seal_entries": len(manifest)}


def check_staged() -> dict[str, Any]:
    staged = staged_paths()
    unexpected = [path for path in staged if not allowed_staged(path)]
    missing_receipts = sorted(RECEIPTS - set(staged))
    core = sorted(path for path in staged if path not in RECEIPTS)
    exact = load(PHASE / "validation/x1-exact-file-set.json")
    expected = [row["path"] for row in exact.get("files", [])]
    mismatches = []
    for row in exact.get("files", []):
        actual = hashlib.sha256(blob(row["path"])).hexdigest()
        if actual != row["sha256"]:
            mismatches.append(row["path"])
    live_structural = structural()
    live_privacy = privacy(staged, from_index=True)
    result = {
        "schema": "ghc.family.v645-v6.x1-final-staged-check.v1",
        "staged_file_count": len(staged),
        "core_file_count": len(core),
        "receipt_file_count": len(RECEIPTS),
        "unexpected_staged": unexpected,
        "missing_receipts": missing_receipts,
        "core_set_matches": core == expected,
        "manifest_mismatches": mismatches,
        "structural_valid": live_structural["valid"],
        "privacy_valid": live_privacy["valid"],
        "valid": not unexpected and not missing_receipts and core == expected and not mismatches and live_structural["valid"] and live_privacy["valid"],
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-receipts", action="store_true")
    parser.add_argument("--check-staged", action="store_true")
    args = parser.parse_args()
    result = write_receipts() if args.write_receipts else check_staged() if args.check_staged else structural()
    print(json.dumps(result, ensure_ascii=False))
    valid = result.get("valid") if isinstance(result, dict) else False
    if args.write_receipts:
        valid = all(item.get("valid", True) if isinstance(item, dict) else True for item in result.values())
    raise SystemExit(0 if valid else 1)


if __name__ == "__main__":
    main()
