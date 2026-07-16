#!/usr/bin/env python3
"""Validate and seal the Tamar Vey v646-v5 x1-only staged packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v646-v5"
PREFIX = "docs/tamar-vey/v646-v5/"
RECEIPTS = {
    f"{PREFIX}validation/x1-structural.json",
    f"{PREFIX}validation/x1-privacy-scan.json",
    f"{PREFIX}validation/x1-stale-label-review.json",
    f"{PREFIX}validation/x1-exact-file-set.json",
    f"{PREFIX}validation/x1-staged-review.json",
    f"{PREFIX}validation/x1-scoped-check-receipt.json",
    f"{PREFIX}reproduction/x1-content-seal.json",
}
SCRIPT_FILES = {
    "scripts/ghc_family_v646_v5_definitions.py",
    "scripts/build_ghc_family_v646_v5_preregistration.py",
    "scripts/ghc_family_v646_v5_x1_review.py",
    "tests/test_ghc_family_v646_v5_x1.py",
}
PATTERNS = {
    "raw_uuid_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_route_or_callable": re.compile("(?:source_" + "thread_id|client" + "ThreadId|app" + "://|codex" + "://|private_" + "callable_id)", re.I),
    "credential_or_secret_material": re.compile("(?:BEGIN (?:RSA |EC |OPENSSH )?PRIVATE " + "KEY|api[_-]?" + "key\\s*[:=]|authorization:\\s*bearer\\s+[A-Za-z0-9._~-]{12,})", re.I),
    "private_absolute_local_path": re.compile("(?:[A-Za-z]:\\\\" + "Users\\\\[^\\\\\\s]+\\\\|D:\\\\GHC-" + "Archives\\\\)", re.I),
    "private_session_artifact": re.compile("(?:session[_ -]?" + "stream[_ -]?(?:path|id)|transcript[_ -]?(?:path|id)|screenshot[_ -]?(?:path|id))", re.I),
}


def git(*args: str, binary: bool = False):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=not binary, encoding=None if binary else "utf-8")


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: dict[str, Any]) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def phase_paths() -> list[str]:
    return sorted(path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file())


def content(path: str, from_index: bool) -> bytes:
    return git("show", f":{path}", binary=True) if from_index else (ROOT / path).read_bytes()


def structural() -> dict[str, Any]:
    proposals = load("x1-proposals.json")
    approvals = load("approval-packets/x1-approval-portfolio.json")
    skills = load("prototypes/x1-skill-runner-plan.json")
    clean = load("maintenance/x1-clean-refine-plan.json")
    sources = load("sources/source-ledger.json")
    method = load("method-flow/method-flow-state.json")
    required = {"proposal_id", "title", "mission_surface", "hypothesis", "null_or_failure", "approval_class", "execution_lane", "current_primary_or_official_source_needs", "concrete_artifacts", "test_falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
    rows = proposals["proposals"]
    distribution = {state: sum(row["expected_disposition"] == state for row in rows) for state in ("completed", "represented", "open_gap", "exact_gate")}
    checks = {
        "proposal_count": len(rows) == 10,
        "prior_count": proposals["prior_frozen_proposal_count"] == 430,
        "frozen_total": proposals["frozen_chain_count_after_x1"] == 440,
        "required_fields": all(required <= set(row) for row in rows),
        "four_outcomes_only": set(row["expected_disposition"] for row in rows) == {"completed", "represented", "open_gap", "exact_gate"},
        "distribution": distribution == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "x2_absent": proposals["x2_execution_present"] is False,
        "safe_count": len(approvals["safe_now"]) == 30,
        "candidate_count": len(approvals["candidates"]) == 20,
        "skills_count": len(skills["skills"]) == 20,
        "runners_count": len(skills["runners"]) == 10,
        "cleanup_count": len(clean["tasks"]) == 30,
        "source_statuses": all(row["status"] in {"current", "stable", "draft", "watch"} for row in sources["sources"]),
        "proposal_collisions_zero": load("provenance/prior-proposal-collision-audit.json")["exact_collision_count"] == 0,
        "portfolio_collisions_zero": load("provenance/prior-portfolio-collision-audit.json")["valid"],
        "method_failed_retained": method["counts"]["witness_results"]["fail"] == 4,
        "method_passed": method["counts"]["witness_results"]["pass"] == 4,
        "method_preferred": method["counts"]["states"]["preferred"] == 4,
        "route_unsent": load("orchestration/terminal-route-plan.json")["current_state"] == "PREPARED_NOT_SENT",
    }
    return {"schema": "ghc.family.v646-v5.x1-structural.v1", "checks": checks, "check_count": len(checks), "passed": sum(checks.values()), "proposal_count": len(rows), "distribution": distribution, "valid": all(checks.values()), "boundary": "X1 structure is preregistration evidence only and creates no x2 completion credit."}


def privacy(paths: list[str], from_index: bool) -> dict[str, Any]:
    hits = []
    decoded = 0
    for path in paths:
        data = content(path, from_index)
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            hits.append({"path": path, "pattern_class": "invalid_utf8"})
            continue
        decoded += 1
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                hits.append({"path": path, "pattern_class": label})
    return {"schema": "ghc.family.v646-v5.privacy-scan.v1", "files_scanned": len(paths), "utf8_decoded": decoded, "pattern_classes": sorted(PATTERNS), "pattern_class_count": len(PATTERNS), "hits": hits, "hit_count": len(hits), "valid": not hits, "boundary": "Five structural classes are screened. Zero hits is not privacy-complete assurance."}


def stale(paths: list[str], from_index: bool) -> dict[str, Any]:
    issues = []
    sent_literal = '"current_state": "' + 'SENT"'
    x2_literal = '"x2_execution_present": ' + 'true'
    stage20_literal = '"stage20_ready": ' + 'true'
    for path in paths:
        text = content(path, from_index).decode("utf-8")
        if sent_literal in text or x2_literal in text or stage20_literal in text:
            issues.append(path)
    return {"schema": "ghc.family.v646-v5.x1-stale-label-review.v1", "files_reviewed": len(paths), "issues": sorted(set(issues)), "terminal_route": "PREPARED_NOT_SENT", "x2_started": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": not issues}


def staged_review() -> dict[str, Any]:
    names = [row for row in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if row]
    statuses = [row.split("\t", 1) for row in git("diff", "--cached", "--name-status", "--diff-filter=ACMR").splitlines() if row]
    owner = sorted(path for path in names if path.startswith(PREFIX) or path in SCRIPT_FILES)
    core = sorted(path for path in owner if path not in RECEIPTS)
    unexpected = sorted(set(names) - set(owner))
    non_additive = [path for status, path in statuses if status != "A"]
    json_failures = []
    manifest = []
    for path in core:
        data = content(path, True)
        manifest.append({"path": path, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
        if path.endswith(".json"):
            try: json.loads(data.decode("utf-8"))
            except Exception: json_failures.append(path)
    structure = structural()
    private = privacy(core, True)
    labels = stale(core, True)
    write("validation/x1-structural.json", structure)
    write("validation/x1-privacy-scan.json", private)
    write("validation/x1-stale-label-review.json", labels)
    write("validation/x1-exact-file-set.json", {"schema": "ghc.family.v646-v5.x1-exact-file-set.v1", "core_file_count": len(core), "core_files": core, "receipt_files": sorted(RECEIPTS), "unexpected": unexpected, "non_additive": non_additive, "valid": not unexpected and not non_additive})
    valid = not unexpected and not non_additive and not json_failures and structure["valid"] and private["valid"] and labels["valid"]
    write("validation/x1-staged-review.json", {"schema": "ghc.family.v646-v5.x1-staged-review.v1", "stage": "x1_only", "staged_file_count": len(names), "core_file_count": len(core), "manifest_entry_count": len(manifest), "unexpected": unexpected, "non_additive": non_additive, "json_failures": json_failures, "x2_implementation_files": [path for path in names if "/x2-" in path or path.endswith("phase-truth.json")], "valid": valid})
    write("validation/x1-scoped-check-receipt.json", {"schema": "ghc.family.v646-v5.x1-scoped-check.v1", "scope": ["430 frozen core proposals", "v646-v4 inherited packet", "v646-v5 x1 packet", "expanded portfolio floors"], "full_repository_suite_run": False, "full_repository_suite_owner": "Eiren Kestrel", "checks": {"structural": structure["valid"], "privacy": private["valid"], "stale_labels": labels["valid"], "staged_paths": not unexpected and not non_additive, "json": not json_failures}, "valid": valid, "boundary": "Scoped x1 validation is not x2 evidence or independent reproduction."})
    write("reproduction/x1-content-seal.json", {"schema": "ghc.family.v646-v5.x1-content-seal.v1", "hash_domain": "exact staged Git blobs", "entry_count": len(manifest), "entries": manifest, "self_excluded_receipts": sorted(RECEIPTS), "x2_present": False, "valid": valid})
    return {"files": len(names), "core": len(core), "entries": len(manifest), "privacy": private["hit_count"], "valid": valid}


def staged_final() -> dict[str, Any]:
    names = [row for row in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if row]
    missing = sorted(RECEIPTS - set(names))
    review = load("validation/x1-staged-review.json")
    seal = load("reproduction/x1-content-seal.json")
    mismatches = []
    for row in seal["entries"]:
        data = content(row["path"], True)
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            mismatches.append(row["path"])
    valid = review["valid"] and not missing and not mismatches and privacy(names, True)["valid"] and stale(names, True)["valid"]
    return {"schema": "ghc.family.v646-v5.x1-final-staged.v1", "staged_file_count": len(names), "missing_receipts": missing, "manifest_mismatches": mismatches, "valid": valid}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["live", "write-receipts", "staged-final"])
    args = parser.parse_args()
    if args.mode == "live":
        result = {"structural": structural(), "privacy": privacy(phase_paths(), False), "stale": stale(phase_paths(), False)}
        result["valid"] = result["structural"]["valid"] and result["privacy"]["valid"] and result["stale"]["valid"]
    elif args.mode == "write-receipts":
        result = staged_review()
    else:
        result = staged_final()
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
