#!/usr/bin/env python3
"""Validate and seal the Tamar Vey v645-v7 x1-only staged packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v645-v7"
PHASE_PREFIX = "docs/tamar-vey/v645-v7/"
RECEIPTS = {
    f"{PHASE_PREFIX}validation/x1-structural.json",
    f"{PHASE_PREFIX}validation/x1-privacy-scan.json",
    f"{PHASE_PREFIX}validation/x1-stale-label-review.json",
    f"{PHASE_PREFIX}validation/x1-exact-file-set.json",
    f"{PHASE_PREFIX}validation/x1-staged-review.json",
    f"{PHASE_PREFIX}validation/x1-scoped-check-receipt.json",
    f"{PHASE_PREFIX}reproduction/x1-content-seal.json",
}
SCRIPT_FILES = {
    "scripts/ghc_family_v645_v7_definitions.py",
    "scripts/build_ghc_family_v645_v7_preregistration.py",
    "scripts/ghc_family_v645_v7_x1_review.py",
    "tests/test_ghc_family_v645_v7_x1.py",
}
PRIVATE_PATTERNS = {
    "raw_uuid_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_route_or_callable": re.compile(r"(?:source_thread_id|clientThreadId|app://|codex://|private_callable_id)", re.I),
    "credential_or_secret_material": re.compile(r"(?:BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|api[_-]?key\s*[:=]|authorization:\s*bearer\s+[A-Za-z0-9._~-]{12,})", re.I),
    "private_absolute_local_path": re.compile(r"(?:[A-Za-z]:\\Users\\[^\\\s]+\\|D:\\GHC-Archives\\)", re.I),
    "private_session_artifact": re.compile(r"(?:session[_ -]?stream[_ -]?(?:path|id)|transcript[_ -]?(?:path|id)|screenshot[_ -]?(?:path|id))", re.I),
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def git(*args: str, binary: bool = False) -> str | bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=not binary)


def staged_paths() -> list[str]:
    return sorted(path for path in str(git("diff", "--cached", "--name-only", "--diff-filter=ACMR")).splitlines() if path)


def blob(path: str) -> bytes:
    return bytes(git("show", f":{path}", binary=True))


def phase_paths() -> list[str]:
    return sorted(path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file())


def privacy(paths: list[str], from_index: bool = False) -> dict[str, Any]:
    hits: list[dict[str, str]] = []
    scanned = 0
    for path in paths:
        if not path.startswith(PHASE_PREFIX):
            continue
        scanned += 1
        raw = blob(path) if from_index else (ROOT / path).read_bytes()
        text = raw.decode("utf-8")
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                hits.append({"path": path, "pattern_class": label})
    return {
        "schema": "ghc.family.v645-v7.privacy-scan.v1",
        "files_scanned": scanned,
        "pattern_classes": sorted(PRIVATE_PATTERNS),
        "hits": hits,
        "hit_count": len(hits),
        "valid": not hits,
        "boundary": "Five structural privacy classes are screened. Zero hits is not a privacy-complete claim.",
    }


def structural() -> dict[str, Any]:
    issues: list[str] = []
    required = [
        "identity-receipt.json", "x1-proposals.json", "x1-preregistration.md",
        "approval-packets/x1-approval-portfolio.json", "prototypes/x1-skill-runner-plan.json",
        "maintenance/x1-clean-refine-plan.json", "provenance/frozen-chain-proposal-index.json",
        "provenance/prior-proposal-collision-audit.json", "provenance/prior-portfolio-collision-audit.json",
        "sources/source-ledger.json", "sources/source-ledger.md", "environment/startup-receipt.json",
        "environment/version-receipt.json", "environment/sandbox-readonly-audit.json",
        "environment/rotation-guard.json", "focus/primary-focus-receipt.json",
        "method-flow/method-flow-state.json", "method-flow/runner-validation.json",
        "method-flow/method-flow-summary.json", "method-flow/method-flow-summary.md",
        "orchestration/phase-update.json", "orchestration/terminal-route-plan.json",
        "validation/x1-operational-negatives.json", "wellbeing-check.md",
        "tooling/ghc-family-index.json", "tooling/ghc-family-index.md",
    ]
    for item in required:
        if not (PHASE / item).is_file():
            issues.append(f"missing:{item}")

    proposals = load(PHASE / "x1-proposals.json")
    fields = {
        "proposal_id", "title", "mission_surface", "hypothesis", "null_or_failure", "approval_class",
        "execution_lane", "current_primary_or_official_source_needs", "concrete_artifacts",
        "test_falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
        "expected_disposition", "novelty_against_370_frozen_proposals",
    }
    rows = proposals.get("proposals", [])
    if len(rows) != 10 or len({row.get("title") for row in rows}) != 10:
        issues.append("proposal_count_or_title_uniqueness")
    if proposals.get("prior_frozen_proposal_count") != 370 or proposals.get("frozen_chain_count_after_x1") != 380:
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

    corpus = load(PHASE / "provenance/frozen-chain-proposal-index.json")
    if corpus.get("prior_file_count") != 37 or corpus.get("prior_proposal_count") != 370 or len(corpus.get("prior_proposals", [])) != 370:
        issues.append("prior_corpus_coverage")
    collision = load(PHASE / "provenance/prior-proposal-collision-audit.json")
    if collision.get("prior_frozen_proposal_count") != 370 or collision.get("exact_title_collision_count") != 0 or len(collision.get("comparisons", [])) != 10:
        issues.append("proposal_collision_audit")
    p_collision = load(PHASE / "provenance/prior-portfolio-collision-audit.json")
    if p_collision.get("exact_collision_count") != 0:
        issues.append("portfolio_collision")

    sources = load(PHASE / "sources/source-ledger.json")
    if len(sources.get("sources", [])) < 20 or any(row.get("status") not in {"current", "stable", "draft", "watch"} for row in sources.get("sources", [])):
        issues.append("source_status_or_count")
    if any(sources.get(field) != 0 for field in ("real_data_rows_ingested", "likelihood_evaluations", "real_participants", "real_keys_or_proofs")):
        issues.append("x1_external_evidence_leak")

    method = load(PHASE / "method-flow/method-flow-state.json")
    counts = method.get("counts", {})
    if method.get("schema") != "ghc.family.method-flow-state.v1" or counts.get("methods") != 9:
        issues.append("method_flow_method_count")
    if counts.get("states", {}).get("preferred") != 9 or counts.get("witness_results") != {"fail": 9, "pass": 9}:
        issues.append("method_flow_witnesses")
    if load(PHASE / "method-flow/runner-validation.json").get("valid") is not True:
        issues.append("method_flow_runner")

    negatives = load(PHASE / "validation/x1-operational-negatives.json")
    if negatives.get("baton_time_inherited") != 2271 or negatives.get("post_baton_inherited") != 1 or negatives.get("inherited_effective") != 2272:
        issues.append("inherited_negative_counts")
    if negatives.get("preregistered_synthetic") != 70 or negatives.get("new_operational_count") != 9 or negatives.get("effective_after_x1") != 2351:
        issues.append("x1_negative_counts")

    focus = load(PHASE / "focus/primary-focus-receipt.json")
    if focus.get("primary_trinity_pillar") != "Freed ID and CBR Heart" or "digital preservation" not in focus.get("bounded_human_practice", ""):
        issues.append("focus_or_practice")
    route = load(PHASE / "orchestration/terminal-route-plan.json")
    if route.get("current_state") != "PREPARED_NOT_SENT" or route.get("send_count") != 0 or route.get("target_title") != "Sylven Arc":
        issues.append("route_state")
    for forbidden in ("phase-truth.json", "x2-proposal-ledger.json", "closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"):
        if (PHASE / forbidden).exists():
            issues.append(f"x2_file:{forbidden}")

    json_count = 0
    for path in PHASE.rglob("*.json"):
        json_count += 1
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            issues.append(f"json:{path.relative_to(PHASE).as_posix()}")
    for path in PHASE.rglob("*"):
        if not path.is_file():
            continue
        raw = path.read_bytes()
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError:
            issues.append(f"utf8:{path.relative_to(PHASE).as_posix()}")
        if raw and not raw.endswith(b"\n"):
            issues.append(f"terminal_newline:{path.relative_to(PHASE).as_posix()}")
        if b"\r\n" in raw:
            issues.append(f"crlf:{path.relative_to(PHASE).as_posix()}")
    owner_file_count = len(phase_paths())
    if owner_file_count >= 15000:
        issues.append("owner_rotation_threshold")
    return {
        "schema": "ghc.family.v645-v7.x1-structural.v1", "phase": "v645-gmut-thos-v7-x1-x2",
        "proposal_count": len(rows), "expected_dispositions": dispositions, "json_document_count": json_count,
        "owner_generated_file_count": owner_file_count, "rotation_threshold": 15000,
        "issues": sorted(set(issues)), "issue_count": len(set(issues)), "valid": not issues,
        "boundary": "X1 structural validation proves only preregistration integrity; it grants no x2 outcome credit.",
    }


def allowed_staged(path: str) -> bool:
    return path.startswith(PHASE_PREFIX) or path in SCRIPT_FILES


def stale_review(paths: list[str], from_index: bool) -> dict[str, Any]:
    hits: list[dict[str, str]] = []
    patterns = {
        "sent_route": re.compile(r'"current_state"\s*:\s*"SENT"', re.I),
        "x2_started": re.compile(r'"x2_started"\s*:\s*true', re.I),
        "stage20_ready": re.compile(r'(?<!NOT_)READY_FOR_STAGE_20'),
        "independent_reproduction_claim": re.compile(r'"independent_reproduction"\s*:\s*true', re.I),
    }
    for path in paths:
        if not path.startswith(PHASE_PREFIX):
            continue
        text = (blob(path) if from_index else (ROOT / path).read_bytes()).decode("utf-8")
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"path": path, "class": label})
    return {"schema": "ghc.family.v645-v7.x1-stale-label-review.v1", "files_reviewed": len([p for p in paths if p.startswith(PHASE_PREFIX)]), "hits": hits, "valid": not hits, "boundary": "Source, standby, inheritance, and future-route names are allowed; ownership, execution, independence, and route states remain Tamar-scoped."}


def write_receipts() -> dict[str, Any]:
    staged = staged_paths()
    core = sorted(path for path in staged if path not in RECEIPTS)
    unexpected = [path for path in staged if not allowed_staged(path)]
    structural_receipt = structural()
    privacy_receipt = privacy(core, from_index=True)
    stale = stale_review(core, from_index=True)
    manifest = [{"path": path, "sha256": hashlib.sha256(blob(path)).hexdigest(), "bytes": len(blob(path))} for path in core]
    exact = {"schema": "ghc.family.v645-v7.x1-exact-file-set.v1", "phase": "v645-gmut-thos-v7-x1-x2", "manifest_domain": "canonical_git_index_blob", "self_excluding_receipts": sorted(RECEIPTS), "core_file_count": len(core), "files": manifest, "unexpected_staged": unexpected, "valid": not unexpected}
    staged_review = {"schema": "ghc.family.v645-v7.x1-staged-review.v1", "stage": "x1_only", "staged_core_file_count": len(core), "unexpected_staged": unexpected, "x2_implementation_files": [path for path in staged if path.startswith(PHASE_PREFIX) and ("/x2-" in path or path.endswith("phase-truth.json"))], "all_paths_owner_scoped_or_phase_tooling": not unexpected, "valid": not unexpected and structural_receipt["valid"] and privacy_receipt["valid"] and stale["valid"]}
    scoped = {"schema": "ghc.family.v645-v7.x1-scoped-check-receipt.v1", "scope": ["370-proposal frozen corpus", "v645-v6 inherited packet", "v645-v7 x1 packet", "v645-v7 definitions and x1 review"], "full_repository_suite_run": False, "full_repository_suite_owner": "Eiren Kestrel only", "checks": {"structural": structural_receipt["valid"], "privacy": privacy_receipt["valid"], "stale_labels": stale["valid"], "staged_paths": not unexpected, "proposal_count": structural_receipt["proposal_count"] == 10}, "valid": structural_receipt["valid"] and privacy_receipt["valid"] and stale["valid"] and not unexpected, "boundary": "This is a scoped x1 preregistration check, not x2 evidence, independent reproduction, or Stage 20 proof."}
    seal = {"schema": "ghc.family.v645-v7.x1-content-seal.v1", "hash_domain": "canonical_git_index_blob", "self_excluding": sorted(RECEIPTS), "entry_count": len(manifest), "entries": manifest, "aggregate_sha256": hashlib.sha256("\n".join(f"{row['sha256']}  {row['path']}" for row in manifest).encode()).hexdigest(), "boundary": "The content seal fixes the x1 core bytes only; it grants no x2 or external truth credit."}
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
    mismatches = [row["path"] for row in exact.get("files", []) if hashlib.sha256(blob(row["path"])).hexdigest() != row["sha256"]]
    live_structural = structural()
    live_privacy = privacy(staged, from_index=True)
    live_stale = stale_review(staged, from_index=True)
    result = {
        "schema": "ghc.family.v645-v7.x1-final-staged-check.v1", "staged_file_count": len(staged), "core_file_count": len(core),
        "receipt_file_count": len(RECEIPTS), "unexpected_staged": unexpected, "missing_receipts": missing_receipts,
        "core_set_matches": core == expected, "manifest_mismatches": mismatches, "structural_valid": live_structural["valid"],
        "privacy_valid": live_privacy["valid"], "stale_valid": live_stale["valid"],
    }
    result["valid"] = not unexpected and not missing_receipts and core == expected and not mismatches and live_structural["valid"] and live_privacy["valid"] and live_stale["valid"]
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check-staged", action="store_true")
    args = parser.parse_args()
    if args.write:
        result = write_receipts()
    elif args.check_staged:
        result = check_staged()
    else:
        result = {"structural": structural(), "privacy": privacy(phase_paths()), "stale": stale_review(phase_paths(), False)}
        result["valid"] = result["structural"]["valid"] and result["privacy"]["valid"] and result["stale"]["valid"]
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if (result.get("valid") if "valid" in result else all(item.get("valid", True) if isinstance(item, dict) else True for item in result.values())) else 1


if __name__ == "__main__":
    raise SystemExit(main())
