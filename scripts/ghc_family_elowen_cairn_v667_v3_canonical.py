#!/usr/bin/env python3
"""Exclusive exact-final canonical validator for Elowen Cairn v667-v3."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "elowen-cairn" / "v667-v3"
BRANCH = "codex/GHC-Family/elowen-cairn-v667-v3-full-tools"
SOURCE_SHA = "79389c8ffd79d78626d79e2109bf1b89bd1a9e67"
X1_SHA = "dc3a69fdbee3afe7f086b5ea9066c04b34b7995a"
EVIDENCE_SHA = "d2692f59aff891eb4b7d49c5fef8fd2b3c5914f9"


def run(*args: str) -> str:
    return subprocess.check_output(
        list(args), cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def git_blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)


def load_blob_json(commit: str, path: str) -> dict[str, Any]:
    return json.loads(git_blob(commit, path).decode("utf-8"))


def replay_manifest(commit: str, relative: str) -> dict[str, Any]:
    manifest = load_blob_json(commit, relative)
    failures = []
    for row in manifest["entries"]:
        blob = git_blob(commit, row["path"])
        if len(blob) != row["bytes"] or hashlib.sha256(blob).hexdigest() != row["sha256"]:
            failures.append(row["path"])
    return {
        "manifest": relative,
        "commit": commit,
        "entries": len(manifest["entries"]),
        "failures": failures,
        "valid": not failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exact-final", required=True)
    parser.add_argument("--receipt-dir", required=True)
    args = parser.parse_args()
    exact_final = args.exact_final
    receipt_dir = Path(args.receipt_dir)
    receipt_path = receipt_dir / f"exact-final-canonical-validation-{exact_final}.json"
    if receipt_path.exists():
        raise SystemExit("exclusive canonical receipt already exists; replay refused")
    receipt_dir.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, observed: Any = None) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed})

    local = run("git", "rev-parse", "HEAD")
    upstream = run("git", "rev-parse", "@{u}")
    tracking = run("git", "rev-parse", f"refs/remotes/origin/{BRANCH}")
    fresh_line = run("git", "ls-remote", "--heads", "origin", BRANCH)
    fresh = fresh_line.split()[0] if fresh_line else ""
    clean_before = not bool(run("git", "status", "--porcelain"))
    divergence = run("git", "rev-list", "--left-right", "--count", "HEAD...@{u}").split()
    check("exact_final_argument_matches_head", local == exact_final, local)
    check("local_matches_expected_final", local == exact_final, local)
    check("upstream_matches_final", upstream == exact_final, upstream)
    check("tracking_matches_final", tracking == exact_final, tracking)
    check("fresh_live_matches_final", fresh == exact_final, fresh)
    check("four_way_equality", len({local, upstream, tracking, fresh}) == 1)
    check("zero_divergence", divergence == ["0", "0"], divergence)
    check("clean_before", clean_before)
    check("x1_direct_parent", run("git", "rev-parse", f"{X1_SHA}^") == SOURCE_SHA)
    check("evidence_direct_parent", run("git", "rev-parse", f"{EVIDENCE_SHA}^") == X1_SHA)
    check("final_direct_parent", run("git", "rev-parse", f"{exact_final}^") == EVIDENCE_SHA)
    check("final_parent_count_one", len(run("git", "show", "-s", "--format=%P", exact_final).split()) == 1)
    check("three_phase_commits", int(run("git", "rev-list", "--count", f"{SOURCE_SHA}..{exact_final}")) == 3)
    check("zero_phase_merges", int(run("git", "rev-list", "--count", "--min-parents=2", f"{SOURCE_SHA}..{exact_final}")) == 0)

    test_files = [
        "tests/test_ghc_family_elowen_cairn_v667_v3_x1.py",
        "tests/test_ghc_family_elowen_cairn_v667_v3_x2.py",
        "tests/test_ghc_family_elowen_cairn_v667_v3_closeout.py",
    ]
    test_rows = []
    total_tests = 0
    for relative in test_files:
        completed = subprocess.run(
            [sys.executable, "-B", str(ROOT / relative)],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        output = completed.stdout + completed.stderr
        match = re.search(r"Ran (\d+) tests", output)
        count = int(match.group(1)) if match else 0
        total_tests += count
        test_rows.append(
            {"path": relative, "exit_code": completed.returncode, "tests": count, "output": output.strip()}
        )
        check(f"test_module_{Path(relative).stem}", completed.returncode == 0 and count > 0, count)

    phase_json = sorted(PHASE_ROOT.rglob("*.json"))
    json_failures = []
    for path in phase_json:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # retained in external receipt if it occurs
            json_failures.append({"path": str(path.relative_to(ROOT)), "error": type(exc).__name__})
    check("all_phase_json_parses", not json_failures, len(phase_json))

    x1_manifest = replay_manifest(
        X1_SHA, "docs/elowen-cairn/v667-v3/validation/x1-content-manifest.json"
    )
    evidence_manifest = replay_manifest(
        EVIDENCE_SHA,
        "docs/elowen-cairn/v667-v3/validation/evidence-content-manifest.json",
    )
    final_delta = replay_manifest(
        exact_final,
        "docs/elowen-cairn/v667-v3/validation/final-delta-manifest.json",
    )
    final_owner = replay_manifest(
        exact_final,
        "docs/elowen-cairn/v667-v3/validation/final-owner-manifest.json",
    )
    manifests = [x1_manifest, evidence_manifest, final_delta, final_owner]
    for row in manifests:
        check(f"manifest_{Path(row['manifest']).stem}", row["valid"], row["entries"])

    owner_paths = [
        path
        for path in run("git", "diff", "--name-only", SOURCE_SHA, exact_final).splitlines()
        if path
    ]
    privacy_patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_windows_path": re.compile(rb"\b[A-Za-z]:\\[^\r\n\"']+"),
        "credential_assignment": re.compile(rb"(?i)(api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*[\"'][^\"']+[\"']"),
        "private_callable_identifier": re.compile(rb"(?i)\b(source_thread_id|clientThreadId|resume_value|session_stream|private_callable)\b"),
        "transcript_or_private_app_state": re.compile(rb"(?i)\b(raw_transcript|private_app_state|terminal_session_stream|screenshot_payload)\b"),
    }
    privacy_hits = []
    privacy_definition_candidates = []
    scanner_definition_paths = {
        "scripts/build_ghc_family_elowen_cairn_v667_v3_closeout.py",
        "scripts/ghc_family_elowen_cairn_v667_v3_canonical.py",
        "tests/test_ghc_family_elowen_cairn_v667_v3_closeout.py",
    }
    python_paths = []
    security_findings = []
    dangerous = {
        "eval": re.compile(rb"\beval\s*\("),
        "exec": re.compile(rb"\bexec\s*\("),
        "shell_true": re.compile(rb"shell\s*=\s*True"),
        "os_system": re.compile(rb"os\.system\s*\("),
        "pickle_loads": re.compile(rb"pickle\.loads\s*\("),
        "yaml_unsafe_load": re.compile(rb"yaml\.load\s*\("),
    }
    for path in owner_paths:
        blob = git_blob(exact_final, path)
        if b"\x00" not in blob:
            for name, pattern in privacy_patterns.items():
                if pattern.search(blob):
                    target = (
                        privacy_definition_candidates
                        if path in scanner_definition_paths
                        else privacy_hits
                    )
                    target.append({"path": path, "class": name})
        if path.endswith(".py"):
            python_paths.append(path)
            compile(blob.decode("utf-8"), path, "exec")
            for name, pattern in dangerous.items():
                if pattern.search(blob):
                    security_findings.append({"path": path, "class": name})
    check("five_class_privacy_scan_zero_hits", not privacy_hits, len(owner_paths))
    check("bounded_python_security_zero_findings", not security_findings, len(python_paths))
    check("owner_file_ceiling", len(owner_paths) < 2000, len(owner_paths))

    truth = load_blob_json(exact_final, "docs/elowen-cairn/v667-v3/closeout/phase-truth.json")
    check("outcome_labels_exact", truth["core_outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
    check("effective_negatives_exact", truth["effective_negatives"] == 27333)
    check("effective_methods_exact", truth["effective_methods"] == 12795)
    check("effective_open_gaps_exact", truth["effective_open_gaps"] == 193)
    check("effective_exact_gates_exact", truth["effective_exact_gates"] == 191)
    check("stage20_verdict_exact", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    check("full_suite_not_run", truth["full_repository_suite_run"] is False)
    check("same_owner_boundary", truth["same_owner_evidence"] is True and truth["independent_reproduction"] is False)

    stale = load_blob_json(exact_final, "docs/elowen-cairn/v667-v3/closeout/stale-label-review.json")
    staged = load_blob_json(exact_final, "docs/elowen-cairn/v667-v3/validation/final-staged-review.json")
    privacy_receipt = load_blob_json(exact_final, "docs/elowen-cairn/v667-v3/validation/final-privacy-scan.json")
    security_receipt = load_blob_json(exact_final, "docs/elowen-cairn/v667-v3/validation/final-security-review.json")
    check("stale_label_review", stale["valid"] and not stale["stale_owner_or_phase_candidates"])
    check("final_staged_review", staged["valid"])
    check("committed_privacy_confirmed_zero", privacy_receipt["valid"] and privacy_receipt["confirmed_hit_count"] == 0)
    check("committed_security_finding_zero", security_receipt["valid"] and security_receipt["finding_count"] == 0)

    clean_after = not bool(run("git", "status", "--porcelain"))
    stable_after = run("git", "rev-parse", "HEAD") == exact_final
    check("clean_after", clean_after)
    check("exact_head_stable_after", stable_after)
    passed = all(row["passed"] for row in checks)
    payload = {
        "schema": "ghc-family-exclusive-exact-final-canonical-receipt-v4",
        "owner": "Elowen Cairn",
        "phase": "v667-v3",
        "started_at_utc": started,
        "finished_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "branch": BRANCH,
        "exact_final": exact_final,
        "invocation_count": 1,
        "successful_invocation_count": 1 if passed else 0,
        "post_success_replay": False,
        "full_repository_suite_run": False,
        "test_modules": test_rows,
        "tests_run": total_tests,
        "phase_json_parse_count": len(phase_json),
        "phase_json_failures": json_failures,
        "owner_file_count": len(owner_paths),
        "privacy_hits": privacy_hits,
        "privacy_scanner_definition_candidates": privacy_definition_candidates,
        "python_compile_count": len(python_paths),
        "security_findings": security_findings,
        "manifests": manifests,
        "detailed_checks": checks,
        "detailed_check_count": len(checks),
        "detailed_check_pass_count": sum(row["passed"] for row in checks),
        "minimal_checks": {
            "exact_head": local == exact_final,
            "clean_before": clean_before,
            "clean_after": clean_after,
            "zero_divergence": divergence == ["0", "0"],
            "four_way_equality": len({local, upstream, tracking, fresh}) == 1,
            "three_phase_commits": int(run("git", "rev-list", "--count", f"{SOURCE_SHA}..{exact_final}")) == 3,
            "zero_merges": int(run("git", "rev-list", "--count", "--min-parents=2", f"{SOURCE_SHA}..{exact_final}")) == 0,
            "one_final_parent": len(run("git", "show", "-s", "--format=%P", exact_final).split()) == 1,
            "x1_parent": run("git", "rev-parse", f"{X1_SHA}^") == SOURCE_SHA,
            "evidence_parent": run("git", "rev-parse", f"{EVIDENCE_SHA}^") == X1_SHA,
            "final_parent": run("git", "rev-parse", f"{exact_final}^") == EVIDENCE_SHA,
            "all_tests": all(row["exit_code"] == 0 for row in test_rows),
            "all_json": not json_failures,
            "privacy_zero": not privacy_hits,
            "security_zero": not security_findings,
        },
        "valid": passed,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "evidence_boundary": "same-owner bounded validation under shared infrastructure; not independent reproduction, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal/cultural/Māori authority, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI, consciousness/personhood, canon, or Stage 20 authority",
    }
    payload["canonical_payload_sha256"] = hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    receipt_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    file_hash = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
    print(
        json.dumps(
            {
                "receipt_file": receipt_path.name,
                "receipt_sha256": file_hash,
                "canonical_payload_sha256": payload["canonical_payload_sha256"],
                "valid": passed,
                "tests_run": total_tests,
                "detailed_checks": len(checks),
                "phase_json_parses": len(phase_json),
                "owner_files": len(owner_paths),
            },
            indent=2,
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
