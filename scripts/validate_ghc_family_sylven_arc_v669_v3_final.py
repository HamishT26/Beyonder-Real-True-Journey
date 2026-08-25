"""One-shot exact-final validator for Sylven Arc v669-v3."""

from __future__ import annotations

import argparse
import ast
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SOURCE = "9c5b88ccde33130663859a3ffcb97188fa63efd7"
X1 = "a8ce92245d170fa64bc4a484a0a074a9848496de"
EVIDENCE = "d5b00198c28178c5a00e5eb9ca839e08d1194ff7"
BRANCH = "codex/GHC-Family/sylven-arc-v669-v3-full-tools"
OWNER_PREFIX = "docs/sylven-arc/v669-v3/"
OWNER_GLOBS = [
    "docs/sylven-arc/v669-v3/**",
    "scripts/*sylven_arc_v669_v3*.py",
    "scripts/ghc_family_ceramics_*.py",
    "tests/*sylven_arc_v669_v3*.py",
]


def git(repo: Path, *args: str, binary: bool = False, check: bool = True):
    return subprocess.run(
        ["git", *args], cwd=repo, check=check, capture_output=True, text=not binary
    )


def git_text(repo: Path, *args: str) -> str:
    return git(repo, *args).stdout.strip()


def blob(repo: Path, head: str, path: str) -> bytes:
    return git(repo, "show", f"{head}:{path}", binary=True).stdout


def load_blob_json(repo: Path, head: str, path: str) -> Any:
    return json.loads(blob(repo, head, path).decode("utf-8"))


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(tmp, path)


def exact_manifest(repo: Path, head: str, path: str, expected: set[str] | None = None) -> tuple[bool, dict[str, Any]]:
    manifest = load_blob_json(repo, head, path)
    mismatches = []
    seen = set()
    for entry in manifest["entries"]:
        data = blob(repo, head, entry["path"])
        seen.add(entry["path"])
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            mismatches.append(entry["path"])
    coverage = True if expected is None else seen == expected
    return not mismatches and coverage, {
        "path": path,
        "declared_entries": manifest["entry_count"],
        "replayed_entries": len(seen),
        "mismatches": mismatches,
        "coverage_exact": coverage,
        "self_exclusions": manifest["self_exclusions"],
    }


def privacy_scan(repo: Path, head: str, paths: list[str]) -> dict[str, Any]:
    patterns = {
        "private_absolute_path": re.compile(r"(?i)(?:[a-z]:\\users\\|[a-z]:\\ghc-archives\\)"),
        "raw_task_or_thread_identifier": re.compile(r"\b019[0-9a-f]{5,}(?:-[0-9a-f]{4,}){2,}\b", re.I),
        "credential_or_secret_assignment": re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*['\"][^'\"]+"),
        "transcript_or_session_stream": re.compile(r"(?i)(?:resume[_-]?value|session[_-]?stream)\s*[:=]\s*['\"][^'\"]+"),
        "private_callable_or_application_state": re.compile(r"(?i)(?:private[_-]?callable[_-]?id|private[_-]?app[_-]?state)\s*[:=]\s*['\"][^'\"]+"),
    }
    candidates = []
    scanned = 0
    for path in paths:
        if not path.startswith(OWNER_PREFIX) or Path(path).suffix.lower() not in {".json", ".md", ".html", ".txt"}:
            continue
        text = blob(repo, head, path).decode("utf-8")
        scanned += 1
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                candidates.append({"class": class_name, "path": path, "offset": match.start()})
    return {"classes": list(patterns), "files_scanned": scanned, "candidates": candidates, "confirmed_hits": len(candidates)}


def security_review(repo: Path, head: str, paths: list[str]) -> dict[str, Any]:
    findings = []
    py_paths = [path for path in paths if path.endswith(".py") and any(fnmatch.fnmatch(path, pattern) for pattern in OWNER_GLOBS)]
    for path in py_paths:
        tree = ast.parse(blob(repo, head, path).decode("utf-8"), filename=path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": path, "line": node.lineno, "kind": f"call_{node.func.id}"})
            if isinstance(node.func, ast.Attribute) and node.func.attr == "system" and isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                findings.append({"path": path, "line": node.lineno, "kind": "call_os_system"})
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append({"path": path, "line": node.lineno, "kind": "subprocess_shell_true"})
    return {"files_reviewed": len(py_paths), "findings": findings, "finding_count": len(findings)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    receipt_path = args.receipt.resolve()
    if receipt_path.exists():
        raise SystemExit("exclusive canonical receipt already exists; refusing replay")
    started = datetime.now(timezone.utc).isoformat()
    checks: dict[str, bool] = {}
    details: dict[str, Any] = {}
    try:
        head = git_text(repo, "rev-parse", "HEAD")
        checks["expected_head"] = head == args.expected_head
        checks["clean_before"] = git_text(repo, "status", "--porcelain") == ""
        upstream = git_text(repo, "rev-parse", "@{upstream}")
        tracking = git_text(repo, "rev-parse", f"refs/remotes/origin/{BRANCH}")
        live_line = git_text(repo, "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
        live = live_line.split("\t", 1)[0] if live_line else ""
        divergence = git_text(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
        checks.update(
            {
                "upstream_equal": upstream == head,
                "tracking_equal": tracking == head,
                "fresh_live_equal": live == head,
                "zero_divergence": divergence == ["0", "0"],
                "x1_parent_source": git_text(repo, "rev-parse", f"{X1}^") == SOURCE,
                "evidence_parent_x1": git_text(repo, "rev-parse", f"{EVIDENCE}^") == X1,
                "final_parent_evidence": git_text(repo, "rev-parse", "HEAD^") == EVIDENCE,
                "source_ancestor": git(repo, "merge-base", "--is-ancestor", SOURCE, head, check=False).returncode == 0,
                "x1_ancestor": git(repo, "merge-base", "--is-ancestor", X1, head, check=False).returncode == 0,
                "evidence_ancestor": git(repo, "merge-base", "--is-ancestor", EVIDENCE, head, check=False).returncode == 0,
                "three_phase_commits": git_text(repo, "rev-list", "--count", f"{SOURCE}..{head}") == "3",
                "zero_merges": git_text(repo, "rev-list", "--count", "--merges", f"{SOURCE}..{head}") == "0",
            }
        )
        phase_commits = git_text(repo, "rev-list", "--reverse", f"{SOURCE}..{head}").splitlines()
        parent_counts = [len(git_text(repo, "rev-list", "--parents", "-n", "1", commit).split()) - 1 for commit in phase_commits]
        checks["one_parent_per_phase_commit"] = parent_counts == [1, 1, 1]

        paths = git_text(repo, "ls-tree", "-r", "--name-only", head).splitlines()
        owner_paths = {path for path in paths if any(fnmatch.fnmatch(path, pattern) for pattern in OWNER_GLOBS)}
        owner_manifest_path = "docs/sylven-arc/v669-v3/validation/final-owner-git-blob-manifest.json"
        owner_manifest = load_blob_json(repo, head, owner_manifest_path)
        expected_owner = owner_paths - set(owner_manifest["self_exclusions"])
        owner_ok, owner_detail = exact_manifest(repo, head, owner_manifest_path, expected_owner)
        checks["final_owner_manifest_exact"] = owner_ok
        details["final_owner_manifest"] = owner_detail

        delta_manifest_path = "docs/sylven-arc/v669-v3/validation/final-delta-git-blob-manifest.json"
        delta_manifest = load_blob_json(repo, head, delta_manifest_path)
        delta_paths = set(git_text(repo, "diff", "--name-only", EVIDENCE, head).splitlines())
        expected_delta = delta_paths - set(delta_manifest["self_exclusions"])
        delta_ok, delta_detail = exact_manifest(repo, head, delta_manifest_path, expected_delta)
        checks["final_delta_manifest_exact"] = delta_ok
        details["final_delta_manifest"] = delta_detail

        json_paths = [path for path in paths if path.startswith(OWNER_PREFIX) and path.endswith(".json")]
        json_failures = []
        for path in json_paths:
            try:
                load_blob_json(repo, head, path)
            except Exception as exc:  # receipt contains class only, not private state
                json_failures.append({"path": path, "error_class": type(exc).__name__})
        checks["all_phase_json_parse"] = not json_failures
        details["json"] = {"parsed": len(json_paths) - len(json_failures), "total": len(json_paths), "failures": json_failures}

        privacy = privacy_scan(repo, head, paths)
        checks["five_class_privacy_zero_hits"] = privacy["confirmed_hits"] == 0 and len(privacy["classes"]) == 5
        details["privacy"] = privacy
        security = security_review(repo, head, paths)
        checks["bounded_python_security_zero_findings"] = security["finding_count"] == 0
        details["security"] = security

        truth = load_blob_json(repo, head, "docs/sylven-arc/v669-v3/closeout/phase-truth.json")
        checks["four_outcome_labels_exact"] = truth["outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
        checks["retained_counts_exact"] = all(
            truth[key] == value
            for key, value in {"effective_negatives": 30899, "methods": 17004, "failed_witnesses": 2720, "passing_witnesses": 3832, "open_gaps": 229, "exact_gates": 224}.items()
        )
        checks["terminal_nonpromotion"] = truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
        checks["zero_real_world_actions"] = all(truth[key] == 0 for key in ["real_people", "real_objects", "real_measurements", "network_calls", "external_actions", "authority_actions"])
        checks["full_suite_not_run"] = truth["full_repository_suite"] == "not_run_Eiren_only"

        baton_path = "docs/sylven-arc/v669-v3/handoffs/caelen-morrow-v669-v4-activation-candidate.md"
        baton_data = blob(repo, head, baton_path)
        baton_text = baton_data.decode("utf-8")
        integrity = load_blob_json(repo, head, "docs/sylven-arc/v669-v3/closeout/handoff-integrity.json")
        baton_words = len(re.findall(r"\S+", baton_text))
        checks["handoff_integrity_exact"] = integrity["bytes"] == len(baton_data) and integrity["sha256"] == hashlib.sha256(baton_data).hexdigest() and integrity["words"] == baton_words
        checks["handoff_word_cap"] = 10000 <= baton_words <= 100000
        checks["handoff_prepared_not_sent"] = "PREPARED_NOT_SENT" in baton_text and "SENT_BY_SYLVEN_ARC = true" not in baton_text

        report = blob(repo, head, "docs/sylven-arc/v669-v3/closeout/static-report.html").decode("utf-8")
        checks["static_report_structure"] = all(token in report for token in ['<html lang="en">', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', 'scope="row"'])
        checks["owner_file_cap"] = len(owner_paths) <= 2000
        doc_word_counts = {}
        for path in paths:
            if path.startswith(OWNER_PREFIX) and Path(path).suffix.lower() in {".md", ".txt", ".html"}:
                doc_word_counts[path] = len(re.findall(r"\S+", blob(repo, head, path).decode("utf-8")))
        checks["document_word_caps"] = all(count <= 100000 for count in doc_word_counts.values())
        details["caps"] = {"owner_files": len(owner_paths), "max_document_words": max(doc_word_counts.values(), default=0)}

        route = load_blob_json(repo, head, "docs/sylven-arc/v669-v3/closeout/route-state-final-candidate.json")
        checks["route_unsent_uncontacted"] = not route["sent"] and not route["acknowledged"] and not route["precontacted"] and not route["standby_contacted"]
        checks["prospective_successor_exact"] = route["prospective_successor"] == "Caelen Morrow" and route["prospective_phase"] == "v669-v4"

        test_proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "tests/test_ghc_family_sylven_arc_v669_v3_x2.py", "tests/test_ghc_family_sylven_arc_v669_v3_final.py"],
            cwd=repo,
            check=False,
            capture_output=True,
            text=True,
        )
        match = re.search(r"(\d+) passed", test_proc.stdout)
        tests_passed = int(match.group(1)) if match else 0
        checks["eligible_owner_tests"] = test_proc.returncode == 0 and tests_passed == 21
        details["tests"] = {"passed": tests_passed, "eligible": 21, "returncode": test_proc.returncode, "summary": test_proc.stdout.strip().splitlines()[-1] if test_proc.stdout.strip() else ""}

        after_head = git_text(repo, "rev-parse", "HEAD")
        after_clean = git_text(repo, "status", "--porcelain") == ""
        after_live_line = git_text(repo, "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
        after_live = after_live_line.split("\t", 1)[0] if after_live_line else ""
        checks["head_stable_after"] = after_head == head
        checks["clean_after"] = after_clean
        checks["fresh_live_equal_after"] = after_live == head

        minimal_keys = [
            "expected_head", "clean_before", "fresh_live_equal", "zero_divergence", "final_parent_evidence",
            "three_phase_commits", "zero_merges", "one_parent_per_phase_commit", "final_owner_manifest_exact",
            "all_phase_json_parse", "five_class_privacy_zero_hits", "eligible_owner_tests", "clean_after",
            "head_stable_after", "terminal_nonpromotion",
        ]
        success = all(checks.values())
        receipt = {
            "schema": "ghc.family.exact-final-canonical-receipt.v3",
            "owner": "Sylven Arc",
            "phase": "v669-v3",
            "started_utc": started,
            "completed_utc": datetime.now(timezone.utc).isoformat(),
            "exact_head": head,
            "exclusive_canonical_invocation": 1,
            "result": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if success else "FAILED_ZERO_AGGREGATE_CREDIT",
            "aggregate_success_credit": 1 if success else 0,
            "checks": checks,
            "detailed_checks": {"passed": sum(checks.values()), "total": len(checks)},
            "minimal_checks": {"passed": sum(checks[key] for key in minimal_keys), "total": len(minimal_keys), "keys": minimal_keys},
            "details": details,
            "full_repository_suite": "not_run_Eiren_only",
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "post_success_replay": False,
        }
        atomic_json(receipt_path, receipt)
        print(json.dumps({"result": receipt["result"], "head": head, "tests": details["tests"], "detailed": receipt["detailed_checks"], "minimal": receipt["minimal_checks"], "json": details["json"], "privacy": {"files": privacy["files_scanned"], "hits": privacy["confirmed_hits"]}, "manifests": {"owner": owner_detail["replayed_entries"], "delta": delta_detail["replayed_entries"]}}, sort_keys=True))
        raise SystemExit(0 if success else 1)
    except BaseException as exc:
        if isinstance(exc, SystemExit):
            raise
        failure = {
            "schema": "ghc.family.exact-final-canonical-receipt.v3",
            "owner": "Sylven Arc",
            "phase": "v669-v3",
            "started_utc": started,
            "completed_utc": datetime.now(timezone.utc).isoformat(),
            "exact_head": args.expected_head,
            "result": "FAILED_ZERO_AGGREGATE_CREDIT",
            "aggregate_success_credit": 0,
            "error_class": type(exc).__name__,
            "checks": checks,
            "details": details,
            "post_success_replay": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
        atomic_json(receipt_path, failure)
        raise


if __name__ == "__main__":
    main()
