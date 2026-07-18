#!/usr/bin/env python3
"""Preflight and spend the one canonical scoped v648-v4 validation pass."""

from __future__ import annotations

import argparse
import io
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any

import ghc_family_v648_v4_definitions as d
from build_ghc_family_v648_v4_closeout import (
    EVIDENCE_COMMIT,
    PHASE,
    ROOT,
    SELECTION,
    SELF_EXCLUSIONS,
    X1_COMMIT,
)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def git(*args: str, check: bool = True) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if check and completed.returncode:
        raise RuntimeError(
            f"git command failed ({completed.returncode}): {args}: {completed.stderr.strip()}"
        )
    return completed.stdout.strip()


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def all_scan_paths() -> list[Path]:
    paths = {path for path in PHASE.rglob("*") if path.is_file()}
    extras = {
        ROOT / "scripts/build_ghc_family_v648_v4_preregistration.py",
        ROOT / "scripts/build_ghc_family_v648_v4_evidence.py",
        ROOT / "scripts/build_ghc_family_v648_v4_closeout.py",
        ROOT / "scripts/ghc_family_v648_v4_definitions.py",
        ROOT / "scripts/ghc_family_v648_v4_runtime.py",
        ROOT / "scripts/validate_ghc_family_v648_v4_final.py",
        ROOT / "tests/test_ghc_family_v648_v4_x1.py",
        ROOT / "tests/test_ghc_family_v648_v4.py",
        ROOT / "tests/test_ghc_family_v648_v4_closeout.py",
        *(ROOT / "scripts" / name for name in d.RUNNER_IDEAS),
    }
    paths.update(path for path in extras if path.is_file())
    return sorted(paths)


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_id": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_private_key": re.compile(
            r"(?i)(api[_-]?key|client_secret|private_key)\s*[:=]\s*[\"'][^\"']+|bearer\s+[A-Za-z0-9._-]{12,}"
        ),
        "private_callable_identifier": re.compile(r"(?i)(private_route|callable_identifier)\s*[:=]"),
        "private_session_or_route": re.compile(
            r"(?i)(session_stream|raw_transcript|conversation_export)\s*[:=]"
        ),
    }
    definitions = {
        "scripts/build_ghc_family_v648_v4_preregistration.py",
        "scripts/build_ghc_family_v648_v4_evidence.py",
        "scripts/build_ghc_family_v648_v4_closeout.py",
        "scripts/validate_ghc_family_v648_v4_final.py",
        "docs/ilyra-fen/v648-v4/validation/x1-staged-privacy.json",
        "docs/ilyra-fen/v648-v4/validation/evidence-staged-privacy.json",
        "docs/ilyra-fen/v648-v4/validation/final-staged-privacy.json",
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    scanned = 0
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        scanned += 1
        relative = path.relative_to(ROOT).as_posix()
        for pattern_class, pattern in patterns.items():
            if pattern.search(text):
                row = {
                    "path": relative,
                    "pattern_class": pattern_class,
                    "disposition": (
                        "scanner_definition"
                        if relative in definitions
                        else "confirmed_payload_hit"
                    ),
                }
                candidates.append(row)
                if relative not in definitions:
                    confirmed.append(row)
    return {
        "schema": "ghc.family.v648-v4.final-privacy.v1",
        "scanned_file_count": scanned,
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": "Five structural classes with exact scanner-definition disposition; zero confirmed hits is not complete privacy assurance.",
    }


def parse_phase_json() -> dict[str, Any]:
    files = sorted(PHASE.rglob("*.json"))
    issues = []
    for path in files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as error:  # pragma: no cover - retained in receipt if hit
            issues.append(
                {"path": path.relative_to(ROOT).as_posix(), "error": str(error)}
            )
    return {"count": len(files), "issues": issues}


def document_caps() -> dict[str, Any]:
    rows = []
    for path in sorted(list(PHASE.rglob("*.md")) + list(PHASE.rglob("*.html"))):
        rows.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "words": len(path.read_text(encoding="utf-8").split()),
            }
        )
    return {"rows": rows, "violations": [row for row in rows if row["words"] > 6000]}


def manifest_preflight() -> dict[str, Any]:
    manifest = load("validation/final-staged-manifest.json")
    cached = set(filter(None, git("diff", "--cached", "--name-only").splitlines()))
    unstaged = set(filter(None, git("diff", "--name-only").splitlines()))
    untracked = set(
        filter(None, git("ls-files", "--others", "--exclude-standard").splitlines())
    )
    mismatches = []
    for row in manifest["entries"]:
        observed = git("rev-parse", f":{row['path']}")
        if observed != row["git_blob"]:
            mismatches.append(
                {"path": row["path"], "expected": row["git_blob"], "observed": observed}
            )
    present_self = {
        path for path in SELF_EXCLUSIONS if git("ls-files", "--stage", "--", path)
    }
    covered_now = {row["path"] for row in manifest["entries"]} | present_self
    return {
        "cached_path_count": len(cached),
        "entry_count": len(manifest["entries"]),
        "declared_self_exclusion_count": len(SELF_EXCLUSIONS),
        "present_self_exclusions": sorted(present_self),
        "missing_reserved_self_exclusions": sorted(set(SELF_EXCLUSIONS) - present_self),
        "coverage_equal_for_present_surface": cached == covered_now,
        "only_cached": sorted(cached - covered_now),
        "only_manifest_or_present_self": sorted(covered_now - cached),
        "unstaged": sorted(unstaged),
        "untracked": sorted(untracked),
        "blob_mismatches": mismatches,
        "valid": (
            cached == covered_now and not unstaged and not untracked and not mismatches
        ),
    }


def evidence_manifest_check() -> dict[str, Any]:
    manifest = load("validation/evidence-staged-manifest.json")
    mismatches = []
    for row in manifest["entries"]:
        observed = git("rev-parse", f"{EVIDENCE_COMMIT}:{row['path']}")
        if observed != row["git_blob"]:
            mismatches.append(row["path"])
    return {"entries": len(manifest["entries"]), "mismatches": mismatches}


def module_preflight() -> dict[str, Any]:
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromNames(SELECTION)
    return {"count": suite.countTestCases(), "errors": list(loader.errors)}


def preflight() -> dict[str, Any]:
    manifest = manifest_preflight()
    parsed = parse_phase_json()
    privacy = privacy_scan(all_scan_paths())
    caps = document_caps()
    baton_words = len(
        (PHASE / "handoffs/sable-rook-v648-v5-activation.md")
        .read_text(encoding="utf-8")
        .split()
    )
    evidence_manifest = evidence_manifest_check()
    x1_receipt = load("validation/x1-immutability-receipt.json")
    modules = module_preflight()
    result = {
        "head": git("rev-parse", "HEAD"),
        "expected_head": EVIDENCE_COMMIT,
        "source_ancestral": subprocess.run(
            ["git", "merge-base", "--is-ancestor", d.SOURCE_COMMIT, "HEAD"],
            cwd=ROOT,
        ).returncode
        == 0,
        "x1_ancestral": subprocess.run(
            ["git", "merge-base", "--is-ancestor", X1_COMMIT, "HEAD"], cwd=ROOT
        ).returncode
        == 0,
        "phase_commits_before_final": int(
            git("rev-list", "--count", f"{d.SOURCE_COMMIT}..HEAD")
        ),
        "merge_commits_before_final": int(
            git("rev-list", "--count", "--merges", f"{d.SOURCE_COMMIT}..HEAD")
        ),
        "manifest": manifest,
        "json": parsed,
        "privacy": privacy,
        "document_cap_violations": caps["violations"],
        "baton_words": baton_words,
        "evidence_manifest": evidence_manifest,
        "x1_immutable": x1_receipt["passed"] and not x1_receipt["issues"],
        "module_selection": SELECTION,
        "test_cases_loaded_not_run": modules["count"],
        "module_loader_errors": modules["errors"],
        "full_suite": False,
        "replay": False,
    }
    result["valid"] = all(
        [
            result["head"] == EVIDENCE_COMMIT,
            result["source_ancestral"],
            result["x1_ancestral"],
            result["phase_commits_before_final"] == 2,
            result["merge_commits_before_final"] == 0,
            manifest["valid"],
            not parsed["issues"],
            privacy["confirmed_hit_count"] == 0,
            not caps["violations"],
            4000 <= baton_words <= 6000,
            not evidence_manifest["mismatches"],
            result["x1_immutable"],
            result["test_cases_loaded_not_run"] > 0,
            not result["module_loader_errors"],
        ]
    )
    return result


def check(name: str, passed: bool, observed: Any) -> dict[str, Any]:
    return {"name": name, "pass": bool(passed), "observed": observed}


def run_tests_once() -> dict[str, Any]:
    stream = io.StringIO()
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromNames(SELECTION)
    if loader.errors:
        raise RuntimeError(f"module loader errors: {loader.errors}")
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    output = stream.getvalue()
    return {
        "selection": SELECTION,
        "run_count": 1,
        "tests_run": result.testsRun,
        "failures": [str(case) for case, _ in result.failures],
        "errors": [str(case) for case, _ in result.errors],
        "skipped": len(result.skipped),
        "successful": result.wasSuccessful(),
        "sanitized_output_tail": "\n".join(output.splitlines()[-8:]),
    }


def run_validation() -> dict[str, Any]:
    canonical_path = PHASE / "validation/single-pass-canonical-validation.json"
    if canonical_path.exists():
        existing = json.loads(canonical_path.read_text(encoding="utf-8"))
        if existing.get("canonical_validation_runs", 0) >= 1:
            raise RuntimeError("canonical successful pass already consumed; replay refused")
    pre = preflight()
    if not pre["valid"]:
        raise RuntimeError(f"final preflight failed: {json.dumps(pre, sort_keys=True)}")

    tests = run_tests_once()
    if not tests["successful"]:
        raise RuntimeError(f"canonical aggregate failed: {json.dumps(tests, sort_keys=True)}")

    outcomes = load("x2-proposal-ledger.json")["outcomes"]
    negatives = load("retained-negative-register-x2.json")
    lifecycle = load("validation/lifecycle-operational-negatives.json")
    gates = load("exact-open-gate-register-x2.json")
    flow = load("method-flow/final-method-flow-ledger.json")
    safe = load("approval-packets/x2-safe-now-ledger.json")
    candidates = load("prototypes/x2-candidate-ledger.json")
    skills = load("tooling/x2-skill-ledger.json")
    runners = load("tooling/x2-runner-ledger.json")
    cleanup = load("maintenance/x2-clean-refine-ledger.json")
    synthetic = load("validation/preregistered-synthetic-negatives.json")
    fermi = load("empirical/fermi-4fgl-dr4-study-contract.json")["evidence"]
    thos = load("thos/community-radio-handover-contract.json")["evidence"]
    freed = load("freed-id/oauth-step-up-profile.json")["evidence"]
    cbr = load("cbr/community-radio-remedy-matrix.json")["evidence"]
    frozen = load("provenance/frozen-chain-proposal-index.json")
    baton_manifest = load("handoffs/sable-rook-v648-v5-activation-manifest.json")

    provisional = {
        "phase-truth-final.json": {
            "schema": "ghc.family.v648-v4.phase-truth.final.v1",
            "owner": d.OWNER,
            "phase": d.PHASE,
            "outcomes": outcomes,
            "retained_negatives": negatives["effective_total"] + lifecycle["count"],
            "open_gaps": gates["effective_open_gaps"],
            "exact_gates": gates["effective_exact_gates"],
            "canonical_successful_passes": 1,
            "full_repository_suite": False,
            "replay": False,
            "independent_reproduction": False,
            "terminal_route": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        "closeout-receipt.json": {
            "schema": "ghc.family.v648-v4.closeout.v1",
            "source_head": d.SOURCE_COMMIT,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "final_commit": "COMMIT_CONTAINING_THIS_RECEIPT",
            "phase_commit_plan": 3,
            "merge_commit_plan": 0,
            "canonical_validation_passed": True,
            "full_repository_suite": False,
            "replay": False,
            "terminal_route": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        "seal-receipt.json": {
            "schema": "ghc.family.v648-v4.seal.v1",
            "seal_candidate": "COMMIT_CONTAINING_THIS_RECEIPT",
            "source_x1_evidence_ancestry": True,
            "planned_phase_commits": 3,
            "planned_merges": 0,
            "canonical_validation_passed": True,
            "post_commit_identity_and_remote_equality": "REQUIRED_BEFORE_ROUTE",
            "same_owner_only": True,
            "independent_reproduction": False,
        },
        "final-validation-record.json": {
            "schema": "ghc.family.v648-v4.final-validation.candidate.v1",
            "canonical_validation_runs": 1,
            "canonical_validation_valid": True,
            "tests": tests["tests_run"],
            "full_repository_suite": False,
            "replay_runs": 0,
            "post_commit_checks_pending": [
                "exact final head",
                "three phase commits",
                "zero merges",
                "one final parent",
                "clean state",
                "four-way remote equality",
            ],
            "boundary": "Post-commit Git checks do not rerun tests or scans and earn no repeatability credit.",
        },
    }
    for relative, payload in provisional.items():
        write(relative, payload)
    write("validation/final-staged-privacy.json", {"schema": "pending"})
    write("validation/final-staged-review.json", {"schema": "pending"})
    write("validation/single-pass-canonical-validation.json", {"schema": "pending"})

    parsed = parse_phase_json()
    privacy = privacy_scan(all_scan_paths())
    caps = document_caps()
    owner_files = [path for path in PHASE.rglob("*") if path.is_file()]
    manifest = load("validation/final-staged-manifest.json")
    static_blob_mismatches = []
    for row in manifest["entries"]:
        observed = git("rev-parse", f":{row['path']}")
        if observed != row["git_blob"]:
            static_blob_mismatches.append(row["path"])

    detailed = [
        check("exact evidence head", pre["head"] == EVIDENCE_COMMIT, pre["head"]),
        check("source ancestry", pre["source_ancestral"], pre["source_ancestral"]),
        check("x1 ancestry", pre["x1_ancestral"], pre["x1_ancestral"]),
        check("pre-final phase commits", pre["phase_commits_before_final"] == 2, pre["phase_commits_before_final"]),
        check("zero merges", pre["merge_commits_before_final"] == 0, pre["merge_commits_before_final"]),
        check("six hundred proposal chain", frozen["count"] == 600, frozen["count"]),
        check("exact ten proposals", len(d.PROPOSALS) == 10, len(d.PROPOSALS)),
        check("outcome distribution", outcomes == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, outcomes),
        check("seventy mutations", synthetic["rejected_count"] == 70, synthetic["rejected_count"]),
        check("safe portfolio", safe["completed_count"] == 30, safe["completed_count"]),
        check("candidate portfolio", candidates["built_count"] == 20 and candidates["invoked_count"] == 20, [candidates["built_count"], candidates["invoked_count"]]),
        check("skill portfolio", skills["validated_count"] == 20 and skills["used_count"] == 20, [skills["validated_count"], skills["used_count"]]),
        check("runner portfolio", runners["passed_count"] == 10, runners["passed_count"]),
        check("cleanup portfolio", cleanup["completed_count"] == 30 and cleanup["destructive_action_count"] == 0, [cleanup["completed_count"], cleanup["destructive_action_count"]]),
        check("negative arithmetic", negatives["effective_total"] + lifecycle["count"] == 4296, negatives["effective_total"] + lifecycle["count"]),
        check("gate arithmetic", gates["effective_open_gaps"] == 30 and gates["effective_exact_gates"] == 31, [gates["effective_open_gaps"], gates["effective_exact_gates"]]),
        check("method flow", len(flow["methods"]) == 11 and len(flow["witnesses"]) == 22, [len(flow["methods"]), len(flow["witnesses"])]),
        check("Fermi zero row", fermi["real_rows"] == 0 and fermi["likelihood_evaluations"] == 0, [fermi["real_rows"], fermi["likelihood_evaluations"]]),
        check("THOS zero real broadcast", thos["real_broadcasts"] == 0, thos["real_broadcasts"]),
        check("Freed ID nonproduction", freed["production_identity"] is False, freed["production_identity"]),
        check("CBR authority reserved", not any([cbr["real_warning_decision"], cbr["privacy_remedy_decision"], cbr["legal_interpretation"], cbr["cultural_ratification"], cbr["maori_authority_decision"]]), cbr),
        check("x1 immutable", pre["x1_immutable"], pre["x1_immutable"]),
        check("evidence manifest", not pre["evidence_manifest"]["mismatches"], pre["evidence_manifest"]),
        check("static closeout manifest", not static_blob_mismatches, static_blob_mismatches),
        check("all phase JSON", not parsed["issues"], parsed),
        check("five class privacy", privacy["confirmed_hit_count"] == 0, privacy["confirmed_hits"]),
        check("document caps", not caps["violations"], caps["violations"]),
        check("durable baton", 4000 <= baton_manifest["word_count"] <= 6000, baton_manifest["word_count"]),
        check("authorized scoped tests", tests["successful"], tests),
        check("single pass no replay", tests["run_count"] == 1, [tests["run_count"], False, False]),
        check("owner file threshold", len(owner_files) < 15000, len(owner_files)),
        check("terminal abstention", True, "NOT_READY_FOR_STAGE_20"),
    ]
    required = [
        "deliverables/v648-v4-final-overview.md",
        "deliverables/v648-v4-static-report.html",
        "handoffs/sable-rook-v648-v5-activation.md",
        "handoffs/sable-rook-v648-v5-activation-manifest.json",
        "validation/final-staged-manifest.json",
        "validation/single-pass-selection.json",
        "tooling/final/ghc-family-index.json",
        "tooling/final/ghc-family-index.md",
        "x2-proposal-ledger.json",
        "retained-negative-register-x2.json",
        "exact-open-gate-register-x2.json",
        "method-flow/final-method-flow-ledger.json",
        "environment/version-receipt.json",
        "threat-model.json",
        "wellbeing-check-x2.json",
        "complete-incomplete-checklist-x2.json",
        "sources/source-ledger.json",
        "evidence-receipt.json",
        "validation/evidence-staged-manifest.json",
        "validation/x1-immutability-receipt.json",
    ]
    minimal = [
        check(relative, (PHASE / relative).is_file(), (PHASE / relative).is_file())
        for relative in required
    ]
    if not all(row["pass"] for row in detailed + minimal):
        raise RuntimeError("canonical detailed or minimal validation failed")

    write("validation/final-staged-privacy.json", privacy)
    write(
        "validation/final-staged-review.json",
        {
            "schema": "ghc.family.v648-v4.final-staged-review.v1",
            "static_entry_count": len(manifest["entries"]),
            "self_exclusion_count": len(SELF_EXCLUSIONS),
            "static_blob_mismatch_count": len(static_blob_mismatches),
            "expected_final_cached_path_count": len(manifest["entries"]) + len(SELF_EXCLUSIONS),
            "json_parse_count": parsed["count"],
            "json_issue_count": len(parsed["issues"]),
            "privacy_file_count": privacy["scanned_file_count"],
            "privacy_candidate_count": privacy["candidate_count"],
            "privacy_confirmed_hit_count": privacy["confirmed_hit_count"],
            "document_cap_violations": caps["violations"],
            "x1_immutable": pre["x1_immutable"],
            "evidence_manifest_mismatches": pre["evidence_manifest"]["mismatches"],
            "out_of_scope_paths": [],
            "passed": True,
        },
    )
    canonical = {
        "schema": "ghc.family.v648-v4.single-pass-canonical-validation.v1",
        "head": EVIDENCE_COMMIT,
        "canonical_validation_runs": 1,
        "full_repository_suite_run": False,
        "named_replay_runs": 0,
        "detached_replay_runs": 0,
        "repeatability_credit": 0,
        "independent_reproduction": False,
        "test_result": tests,
        "detailed_check_count": len(detailed),
        "detailed_checks_passed": sum(row["pass"] for row in detailed),
        "minimal_check_count": len(minimal),
        "minimal_checks_passed": sum(row["pass"] for row in minimal),
        "checks": detailed,
        "minimal_checks": minimal,
        "json_parse_count": parsed["count"],
        "privacy_file_count": privacy["scanned_file_count"],
        "privacy_pattern_classes": privacy["pattern_classes"],
        "privacy_confirmed_hits": privacy["confirmed_hits"],
        "final_static_manifest_entries": len(manifest["entries"]),
        "final_self_exclusions": len(SELF_EXCLUSIONS),
        "document_word_cap_violations": caps["violations"],
        "valid": True,
        "boundary": "One canonical same-owner scoped validation only; no full suite or replay and no independent, empirical, production, professional, legal, cultural, accessibility-complete, security-complete, or Stage 20 credit.",
    }
    write("validation/single-pass-canonical-validation.json", canonical)

    final_parsed = parse_phase_json()
    final_privacy = privacy_scan(all_scan_paths())
    if final_parsed["issues"] or final_privacy["confirmed_hit_count"]:
        raise RuntimeError("final result-receipt syntax or privacy check failed")
    canonical["json_parse_count"] = final_parsed["count"]
    canonical["privacy_file_count"] = final_privacy["scanned_file_count"]
    canonical["privacy_confirmed_hits"] = final_privacy["confirmed_hits"]
    write("validation/final-staged-privacy.json", final_privacy)
    write("validation/single-pass-canonical-validation.json", canonical)
    return canonical


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["preflight", "run"])
    args = parser.parse_args()
    payload = preflight() if args.mode == "preflight" else run_validation()
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if not payload.get("valid", True):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
