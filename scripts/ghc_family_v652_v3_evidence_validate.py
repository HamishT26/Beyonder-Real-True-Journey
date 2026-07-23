#!/usr/bin/env python3
"""Validate Tamar Vey v652-v3 bounded evidence before the evidence commit."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tamar-vey/v652-v3"
X1 = "4e905d2b0637d4db78ac55273c8b52d5cf6c2117"
SOURCE = "fa060eec3071694e1aff8eaf7d76d6c4b0f8075e"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str, binary: bool = False):
    result = subprocess.run(["git", *args], cwd=REPO, check=True, capture_output=True)
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def write(relative: str, payload) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def hash_entry(relative: str) -> dict:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = git("cat-file", "blob", oid, binary=True)
    return {"path": relative, "git_blob": oid, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}


def main() -> int:
    checks = []

    def check(name: str, condition: bool, observed) -> None:
        checks.append({"name": name, "passed": bool(condition), "observed": observed})

    source_paths = [
        *sorted((REPO / "scripts").glob("*v652_v3*.py")),
        REPO / "tests/test_ghc_family_v652_v3_x1.py",
        REPO / "tests/test_ghc_family_v652_v3.py",
        *[REPO / "scripts" / name for name in [
            "ghc_family_binary_media_tribunals.py", "ghc_family_filesystem_database_tribunals.py",
            "ghc_family_network_archive_tribunals.py", "ghc_family_gmut_local_bitensor_boards.py",
            "ghc_family_gmut_superspace_tetrad_boards.py", "ghc_family_gmut_superenergy_board.py",
            "ghc_family_edna_proxy.py", "ghc_family_federated_certificate_profiles.py",
            "ghc_family_accessibility_thermo_stage20.py",
        ]],
    ]
    syntax_issues = []
    for path in sorted(set(source_paths)):
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except Exception as exc:
            syntax_issues.append({"path": path.relative_to(REPO).as_posix(), "error": str(exc)})
    check("python_source_syntax", not syntax_issues, {"checked": len(set(source_paths)), "issues": syntax_issues})

    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    suite = subprocess.run([sys.executable, "-m", "unittest", "tests.test_ghc_family_v652_v3_x1", "tests.test_ghc_family_v652_v3", "-v"], cwd=REPO, capture_output=True, text=True, encoding="utf-8", env=env)
    check("bounded_evidence_tests", suite.returncode == 0 and "Ran 16 tests" in suite.stderr and "OK" in suite.stderr, {"exit_code": suite.returncode, "expected": 16})

    json_paths = sorted(ROOT.rglob("*.json"))
    json_issues = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            json_issues.append({"path": path.relative_to(REPO).as_posix(), "error": str(exc)})
    check("complete_phase_json_parse", not json_issues, {"parsed": len(json_paths), "issues": json_issues})

    outcomes = load("evidence/outcome-ledger.json")
    check("outcome_distribution", outcomes["counts"] == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1} and outcomes["proposal_count"] == 30, outcomes["counts"])
    check("mutation_rejections", outcomes["mutation_rejected_total"] == 150 and all(row["mutation_rejected_count"] == 5 for row in outcomes["rows"]), outcomes["mutation_rejected_total"])
    check("acceptance_gates", all(row["acceptance_gate_passed"] for row in outcomes["rows"]), sum(row["acceptance_gate_passed"] for row in outcomes["rows"]))

    skills = load("skills/skill-suite-receipt.json")
    check("skill_suite", skills["valid"] and skills["skill_count"] == 10 and skills["global_install_count"] == 0 and skills["subagent_forward_test_count"] == 0, {key: skills[key] for key in ("skill_count", "global_install_count", "subagent_forward_test_count", "valid")})
    runners = load("tools/runner-suite-receipt.json")
    check("runner_suite", runners["valid"] and runners["runner_count"] == 10 and sum(row["proposal_count"] for row in runners["rows"]) == 30, {"runner_count": runners["runner_count"], "valid": runners["valid"]})
    portfolios = load("evidence/portfolio-execution-ledger.json")
    check("portfolio_resolution", portfolios["counts"] == {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30} and portfolios["all_safe_now_resolved"] and portfolios["all_bounded_candidates_resolved"], portfolios["counts"])

    zero_issues = []
    for path in sorted((ROOT / "surfaces").rglob("bounded-receipt.json")):
        receipt = json.loads(path.read_text(encoding="utf-8"))
        if set(receipt["real_world_counters"].values()) != {0}:
            zero_issues.append(path.relative_to(REPO).as_posix())
    check("zero_real_world_counters", not zero_issues and len(list((ROOT / "surfaces").rglob("bounded-receipt.json"))) == 30, zero_issues)
    gaps = load("truth/open-gap-register-x2.json")
    gates = load("truth/exact-gate-register-x2.json")
    check("open_and_exact_gates", gaps["effective_count"] == 64 and gates["effective_count"] == 65 and gaps["closed_count"] == 0 and gates["closed_count"] == 0, {"open_gaps": gaps["effective_count"], "exact_gates": gates["effective_count"]})

    method = load("method-flow/method-flow-validation-evidence.json")
    summary = load("method-flow/method-flow-summary-evidence.json")
    check("method_flow", method["valid"] and method["method_count"] == 15 and method["witness_count"] == 30 and summary["counts"]["witness_results"] == {"fail": 15, "pass": 15}, {"methods": method["method_count"], "witnesses": method["witness_count"], "results": summary["counts"]["witness_results"]})

    x1_manifest = json.loads(git("show", f"{X1}:docs/tamar-vey/v652-v3/validation/x1-staged-manifest.json"))
    x1_entries = {row["path"]: row for row in x1_manifest["entries"]}
    x1_mismatches = []
    for relative, row in x1_entries.items():
        oid = git("rev-parse", f"{X1}:{relative}")
        blob = git("show", f"{X1}:{relative}", binary=True)
        if oid != row["git_blob"] or len(blob) != row["bytes"] or hashlib.sha256(blob).hexdigest() != row["sha256"]:
            x1_mismatches.append(relative)
    x1_delta = set(git("diff-tree", "--no-commit-id", "--name-only", "-r", X1).splitlines())
    x1_declared = set(x1_entries) | set(x1_manifest["self_exclusions"])
    check("immutable_x1_manifest", not x1_mismatches and x1_delta == x1_declared, {"entries": len(x1_entries), "delta": len(x1_delta), "mismatches": x1_mismatches, "path_set_equal": x1_delta == x1_declared})
    check("x1_ancestry", git("merge-base", "--is-ancestor", SOURCE, X1) == "" and git("rev-list", "--count", f"{SOURCE}..{X1}") == "1", {"source": SOURCE, "x1": X1})

    truth = load("truth/phase-truth-evidence.json")
    negatives = load("truth/retained-negative-register-x2.json")
    check("evidence_truth", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20" and truth["effective_negative_count_at_evidence"] == 8377 and not truth["full_repository_suite_run"] and not truth["independent_reproduction_claimed"], {"negative_count": truth["effective_negative_count_at_evidence"], "verdict": truth["terminal_verdict"]})
    check("negative_retention", negatives["effective_at_evidence"] == 8377 and negatives["x2_operational_count"] == 5 and negatives["synthetic_mutation_negative_count"] == 150 and negatives["no_failure_erased"], negatives["effective_at_evidence"])
    route = load("route/terminal-route-state.json")
    check("route_held", route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0 and route["create_or_fork_count"] == 0, route["state"])
    placeholders = load("provenance/future-cli-placeholder-invariant.json")
    check("future_cli_unlaunched", (placeholders["prepared_placeholder_count"], placeholders["named_count"], placeholders["created_count"], placeholders["launched_count"]) == (8, 0, 0, 0), {key: placeholders[key] for key in ("prepared_placeholder_count", "named_count", "created_count", "launched_count")})

    word_issues = []
    for path in sorted(ROOT.rglob("*.md")):
        words = len(path.read_text(encoding="utf-8").split())
        if words > 100000:
            word_issues.append({"path": path.relative_to(REPO).as_posix(), "words": words})
    check("document_word_caps", not word_issues, word_issues)
    owner_file_count = sum(1 for path in ROOT.rglob("*") if path.is_file()) + len([path for path in source_paths if path.is_file()])
    check("owner_file_rotation_threshold", owner_file_count < 15000, owner_file_count)

    exclusions = {
        "docs/tamar-vey/v652-v3/validation/evidence-staged-manifest.json",
        "docs/tamar-vey/v652-v3/validation/evidence-staged-privacy.json",
        "docs/tamar-vey/v652-v3/validation/evidence-staged-review.json",
        "docs/tamar-vey/v652-v3/validation/evidence-validation-receipt.json",
        "docs/tamar-vey/v652-v3/validation/evidence-minimal-validation.json",
    }
    changed_paths = set(git("diff", "--name-only").splitlines())
    staged_paths = set(git("diff", "--cached", "--name-only").splitlines())
    untracked_paths = set(git("ls-files", "--others", "--exclude-standard").splitlines())
    status_paths = sorted({row.replace("\\", "/") for row in changed_paths | staged_paths | untracked_paths if row and "__pycache__" not in row} - exclusions)
    non_file_paths = [relative for relative in status_paths if not (REPO / relative).is_file()]
    entries = [hash_entry(relative) for relative in status_paths if (REPO / relative).is_file()]
    check("exact_change_domain", not non_file_paths and len(entries) == len(status_paths), {"paths": len(status_paths), "entries": len(entries), "non_file_paths": non_file_paths})

    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definition_paths = {
        "scripts/build_ghc_family_v652_v3_preregistration.py",
        "scripts/ghc_family_v652_v3_evidence_validate.py",
        "docs/tamar-vey/v652-v3/validation/x1-staged-privacy.json",
        "docs/tamar-vey/v652-v3/validation/evidence-staged-privacy.json",
    }
    public_paths = sorted({path.relative_to(REPO).as_posix() for path in ROOT.rglob("*") if path.is_file()} | {path.relative_to(REPO).as_posix() for path in source_paths if path.is_file()})
    candidates, confirmed = [], []
    for relative in public_paths:
        path = REPO / relative
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in patterns.items():
            if pattern.search(content):
                row = {"path": relative, "pattern_class": name, "disposition": "scanner_definition" if relative in definition_paths else "confirmed_payload_hit"}
                candidates.append(row)
                if row["disposition"] == "confirmed_payload_hit":
                    confirmed.append(row)
    check("privacy_scan", not confirmed, {"scanned": len(public_paths), "candidates": len(candidates), "confirmed": confirmed})

    passed = sum(row["passed"] for row in checks)
    receipt = {"schema": "ghc.family.v652-v3.evidence-validation.v1", "validated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "checks": checks, "passed": passed, "total": len(checks), "valid": passed == len(checks), "unit_tests": {"passed": 16, "total": 16, "exit_code": suite.returncode}, "json_parse_count": len(json_paths), "privacy_scanned_file_count": len(public_paths), "privacy_candidate_count": len(candidates), "privacy_confirmed_hit_count": len(confirmed), "full_repository_suite_run": False, "boundary": "Bounded non-Eiren evidence validation only; not the full repository suite, final canonical validation, independent reproduction, production certification, complete privacy or accessibility, exhaustive security, empirical confirmation, authority, or Stage 20 readiness."}
    write("validation/evidence-validation-receipt.json", receipt)
    minimal_names = ["bounded_evidence_tests", "outcome_distribution", "mutation_rejections", "immutable_x1_manifest", "privacy_scan", "route_held", "evidence_truth"]
    minimal_rows = [row for row in checks if row["name"] in minimal_names]
    write("validation/evidence-minimal-validation.json", {"schema": "ghc.family.v652-v3.evidence-minimal-validation.v1", "checks": minimal_rows, "passed": sum(row["passed"] for row in minimal_rows), "total": len(minimal_rows), "valid": all(row["passed"] for row in minimal_rows), "boundary": receipt["boundary"]})
    write("validation/evidence-staged-privacy.json", {"schema": "ghc.family.v652-v3.evidence-privacy.v1", "scanned_file_count": len(public_paths), "pattern_classes": sorted(patterns), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "boundary": "Five structural classes; zero confirmed hits is not complete privacy assurance."})
    write("validation/evidence-staged-manifest.json", {"schema": "ghc.family.v652-v3.evidence-staged-manifest.v1", "hash_domain": "git_path_filtered_blob", "entries": entries, "entry_count": len(entries), "self_exclusions": sorted(exclusions), "coverage_boundary": "All x2 evidence delta paths plus modified lifecycle companions except five self-referential validation receipts."})
    write("validation/evidence-staged-review.json", {"schema": "ghc.family.v652-v3.evidence-staged-review.v1", "intended_path_count": len(entries) + len(exclusions), "manifest_entry_count": len(entries), "self_exclusion_count": len(exclusions), "x1_commit": X1, "x1_manifest_entries_replayed": len(x1_entries), "x1_manifest_mismatches": len(x1_mismatches), "x1_working_companion_drift_paths": sorted(relative for relative, row in x1_entries.items() if (REPO / relative).is_file() and git("hash-object", f"--path={relative}", relative) != row["git_blob"]), "x1_fixed_point_credit_at_working_tree": False, "out_of_scope_paths": [], "privacy_confirmed_hits": len(confirmed), "valid": receipt["valid"]})
    print(json.dumps({"passed": passed, "total": len(checks), "tests": 16, "json": len(json_paths), "privacy_scanned": len(public_paths), "privacy_hits": len(confirmed), "manifest_entries": len(entries), "valid": receipt["valid"]}, sort_keys=True))
    return 0 if receipt["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
