#!/usr/bin/env python3
"""Validate Elowen Cairn v654-v2 bounded x2 evidence before its commit."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v654_v2_x2_data as x2


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/elowen-cairn/v654-v2"
X1 = "8a8062a360dd6510d999cabe22cd38417f59def6"
EXPECTED = {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
SELF_EXCLUSIONS = {
    "docs/elowen-cairn/v654-v2/validation/evidence-manifest.json",
    "docs/elowen-cairn/v654-v2/validation/evidence-privacy.json",
    "docs/elowen-cairn/v654-v2/validation/evidence-staged-review.json",
    "docs/elowen-cairn/v654-v2/validation/evidence-validation-receipt.json",
    "docs/elowen-cairn/v654-v2/validation/evidence-minimal-validation.json",
}
ALLOWED_SCRIPT_PATHS = {
    "scripts/ghc_family_v654_v2_core.py",
    "scripts/ghc_family_v654_v2_x2_data.py",
    "scripts/build_ghc_family_v654_v2_x2_method_flow.py",
    "scripts/build_ghc_family_v654_v2_evidence.py",
    "scripts/ghc_family_v654_v2_evidence_validate.py",
    "scripts/ghc_family_letterpress_material_ledger.py",
    "scripts/ghc_family_press_state_boards.py",
    "scripts/ghc_family_print_worker_boundary_boards.py",
    "scripts/ghc_family_print_waste_release_refusal.py",
    "scripts/ghc_family_gmut_print_fields.py",
    "scripts/ghc_family_thos_letterpress_proxy.py",
    "scripts/ghc_family_freed_id_print_profiles.py",
    "scripts/ghc_family_accessible_print_audit.py",
    "scripts/ghc_family_v654_v2_detailed_validator.py",
    "scripts/ghc_family_v654_v2_bounded_suite.py",
    "tests/test_ghc_family_v654_v2.py",
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True, encoding="utf-8").strip()


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def status_paths() -> list[str]:
    rows = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
    ).splitlines()
    return sorted({row[3:].replace("\\", "/") for row in rows if len(row) > 3})


def hash_entry(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {"path": relative, "git_blob": oid, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(?:(?:api[_-]?key|client_secret|private_key)\s*[:=]\s*[\"']?[A-Za-z0-9._-]{8,}|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {
        "scripts/ghc_family_v654_v2_evidence_validate.py",
        "docs/elowen-cairn/v654-v2/validation/evidence-privacy.json",
    }
    candidates, confirmed = [], []
    scanned = 0
    for relative in paths:
        path = REPO / relative
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for pattern_class, pattern in patterns.items():
            if pattern.search(content):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": pattern_class, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {
        "schema": "ghc.family.v654-v2.evidence-privacy.v1",
        "scanned_file_count": scanned,
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": "Five structural classes with scanner-definition quarantine; zero confirmed hits is not complete privacy assurance.",
    }


def validate(require_staged: bool) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, observed: Any) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed})

    outcomes = load("evidence/outcome-ledger.json")
    portfolios = load("evidence/portfolio-execution-ledger.json")
    skills = load("skills/skill-suite-receipt.json")
    runners = load("tools/runner-suite-receipt.json")
    gaps = load("truth/open-gap-register-x2.json")
    gates = load("truth/exact-gate-register-x2.json")
    negatives = load("truth/retained-negative-register.json")
    truth = load("truth/phase-truth-evidence.json")
    method = load("method-flow/method-flow-ledger.json")
    successor = load("provenance/successor-authority-invariant.json")

    check("x1_head_before_evidence_commit", git("rev-parse", "HEAD") == X1, git("rev-parse", "HEAD"))
    check("outcome_distribution", outcomes["proposal_count"] == 30 and outcomes["counts"] == EXPECTED, outcomes["counts"])
    check("all_acceptance_gates", all(row["acceptance_gate_passed"] for row in outcomes["rows"]), len(outcomes["rows"]))
    check("mutation_rejections", outcomes["mutation_rejected_total"] == 150 and sum(row["mutation_rejected_count"] for row in outcomes["rows"]) == 150, outcomes["mutation_rejected_total"])
    surface_receipts = sorted((ROOT / "surfaces").rglob("bounded-receipt.json"))
    zero_issues = []
    for path in surface_receipts:
        receipt = json.loads(path.read_text(encoding="utf-8"))
        if set(receipt["real_world_counters"].values()) != {0}:
            zero_issues.append(path.relative_to(REPO).as_posix())
    check("zero_real_world_counters", len(surface_receipts) == 30 and not zero_issues, {"receipts": len(surface_receipts), "issues": zero_issues})
    check("skills", skills["skill_count"] == 10 and skills["valid"] and all(row["quick_validate_passed"] and row["smoke"]["valid"] and not row["smoke"]["global_installation"] for row in skills["rows"]), skills["skill_count"])
    check("runners", runners["runner_count"] == 10 and runners["valid"] and sum(row["proposal_count"] for row in runners["rows"]) == 30, runners["runner_count"])
    check("portfolios", portfolios["counts"] == {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30} and portfolios["all_safe_now_resolved"] and portfolios["all_bounded_candidates_resolved"], portfolios["counts"])
    check("open_gap", gaps["effective_count"] == 79 and gaps["closed_count"] == 0 and gaps["new_rows"][0]["real_rows"] == 0 and not gaps["new_rows"][0]["account_or_api_key_used"], gaps["effective_count"])
    check("exact_gate", gates["effective_count"] == 80 and gates["closed_count"] == 0 and gates["new_rows"][0]["authority_decisions"] == 0, gates["effective_count"])
    expected_negative_total = 10960 + len(x2.X2_OPERATIONAL_NEGATIVES)
    check("negative_retention", negatives["effective_at_evidence"] == expected_negative_total and negatives["x2_operational_count"] == len(x2.X2_OPERATIONAL_NEGATIVES) and negatives["synthetic_mutation_negative_count"] == 150 and negatives["no_failure_erased"], negatives["effective_at_evidence"])
    states = Counter(row["recommendation_state"] for row in method["methods"])
    witness = Counter(row["result"] for row in method["witnesses"])
    expected_methods = 17 + len(x2.X2_OPERATIONAL_NEGATIVES)
    check("method_flow", len(method["methods"]) == expected_methods and states == {"preferred": expected_methods} and witness == {"fail": expected_methods, "pass": expected_methods}, {"methods": len(method["methods"]), "states": dict(states), "witnesses": dict(witness)})
    check("truth", truth["outcome_counts"] == EXPECTED and truth["effective_negative_count_at_evidence"] == expected_negative_total and truth["real_row_count"] == 0 and truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20" and not truth["independent_reproduction_claimed"], truth["terminal_verdict"])
    check("successor_hold", successor["created_count"] == 0 and successor["forked_count"] == 0 and successor["delegated_count"] == 0 and successor["contacted_count"] == 0 and successor["state"] == "NO_SUCCESSOR_AUTHORIZED", successor["state"])

    x1_manifest = json.loads(git("show", f"{X1}:docs/elowen-cairn/v654-v2/validation/x1-staged-manifest.json"))
    x1_mismatch = []
    for row in x1_manifest["entries"]:
        observed = git("rev-parse", f"{X1}:{row['path']}")
        if observed != row["git_blob"]:
            x1_mismatch.append(row["path"])
    check("immutable_x1_manifest", not x1_mismatch, {"entries": len(x1_manifest["entries"]), "mismatches": x1_mismatch})

    json_paths = sorted(ROOT.rglob("*.json"))
    json_failures = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            json_failures.append({"path": path.relative_to(REPO).as_posix(), "error": type(exc).__name__})
    check("json_parse", not json_failures, {"count": len(json_paths), "failures": json_failures})

    paths = [path for path in status_paths() if path not in SELF_EXCLUSIONS and "__pycache__" not in path]
    out_of_scope = [
        path for path in paths
        if not path.startswith("docs/elowen-cairn/v654-v2/") and path not in ALLOWED_SCRIPT_PATHS
    ]
    check("working_scope", not out_of_scope, out_of_scope)
    privacy = privacy_scan(paths)
    check("privacy", privacy["confirmed_hit_count"] == 0, privacy["confirmed_hits"])
    entries = [hash_entry(path) for path in paths if (REPO / path).is_file()]
    write("validation/evidence-privacy.json", privacy)
    write("validation/evidence-manifest.json", {"schema": "ghc.family.v654-v2.evidence-manifest.v1", "hash_domain": "git_path_filtered_blob", "entries": entries, "entry_count": len(entries), "self_exclusions": sorted(SELF_EXCLUSIONS), "coverage_boundary": "Every current x2 evidence path plus modified lifecycle companion except five declared self-referential validation receipts."})

    staged_paths: list[str] = []
    staged_out: list[str] = []
    if require_staged:
        staged_paths = sorted(git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines())
        staged_out = [
            path for path in staged_paths
            if not path.startswith("docs/elowen-cairn/v654-v2/") and path not in ALLOWED_SCRIPT_PATHS
        ]
        check("exact_staged_scope", bool(staged_paths) and not staged_out, {"count": len(staged_paths), "out_of_scope": staged_out})
        check("staged_has_surfaces", sum("/surfaces/" in path for path in staged_paths) == 90, sum("/surfaces/" in path for path in staged_paths))

    passed = sum(row["passed"] for row in checks)
    receipt = {
        "schema": "ghc.family.v654-v2.evidence-validation.v1",
        "checks": checks,
        "passed": passed,
        "total": len(checks),
        "valid": passed == len(checks),
        "json_parse_count": len(json_paths),
        "privacy_scanned_file_count": privacy["scanned_file_count"],
        "privacy_confirmed_hit_count": privacy["confirmed_hit_count"],
        "manifest_entry_count": len(entries),
        "x1_manifest_entry_count": len(x1_manifest["entries"]),
        "require_staged": require_staged,
        "staged_path_count": len(staged_paths),
        "out_of_scope_staged_paths": staged_out,
        "full_repository_suite_run": False,
        "final_canonical_pass_run": False,
        "boundary": "Bounded non-Eiren evidence validation only; not the full repository suite, final canonical pass, independent reproduction, production certification, complete privacy or accessibility, authority, or Stage 20 readiness.",
    }
    write("validation/evidence-validation-receipt.json", receipt)
    write("validation/evidence-staged-review.json", {"schema": "ghc.family.v654-v2.evidence-staged-review.v1", "x1_commit": X1, "x1_manifest_entries_replayed": len(x1_manifest["entries"]), "manifest_entry_count": len(entries), "self_exclusion_count": len(SELF_EXCLUSIONS), "working_out_of_scope_paths": out_of_scope, "staged_path_count": len(staged_paths), "staged_out_of_scope_paths": staged_out, "privacy_confirmed_hits": privacy["confirmed_hit_count"], "valid": receipt["valid"]})
    write("validation/evidence-minimal-validation.json", {"schema": "ghc.family.v654-v2.evidence-minimal-validation.v1", "checks": [{"name": "outcomes", "passed": outcomes["counts"] == EXPECTED}, {"name": "mutations", "passed": outcomes["mutation_rejected_total"] == 150}, {"name": "zero_rows", "passed": truth["real_row_count"] == 0}, {"name": "successor_unauthorized", "passed": successor["created_count"] == 0 and successor["state"] == "NO_SUCCESSOR_AUTHORIZED"}, {"name": "privacy", "passed": privacy["confirmed_hit_count"] == 0}, {"name": "verdict", "passed": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"}], "valid": receipt["valid"], "boundary": receipt["boundary"]})
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-staged", action="store_true")
    args = parser.parse_args()
    receipt = validate(args.require_staged)
    print(json.dumps({"passed": receipt["passed"], "total": receipt["total"], "valid": receipt["valid"]}, sort_keys=True))
    raise SystemExit(0 if receipt["valid"] else 1)


if __name__ == "__main__":
    main()
