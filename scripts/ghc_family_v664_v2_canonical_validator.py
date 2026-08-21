#!/usr/bin/env python3
"""Run Neris v664-v2's one-shot exact-final owner-delta validation."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "df7e3ba4c43b8ed9de01e308c6b9163016e37ceb"
X1 = "4eaec9fa556426d94c800cb2a95c5709524e8203"
EVIDENCE = "d93b55252209b14cea58fdd4b0da1e95759c62fd"
BRANCH = "codex/GHC-Family/neris-solane-v664-v2-full-tools"
PHASE_PREFIX = "docs/neris-solane/v664-v2/"
X1_MANIFEST = f"{PHASE_PREFIX}x1/x1-content-manifest.json"
EVIDENCE_MANIFEST = f"{PHASE_PREFIX}validation/evidence-manifest.json"
FINAL_DELTA_MANIFEST = f"{PHASE_PREFIX}validation/final-delta-manifest.json"
FINAL_OWNER_MANIFEST = f"{PHASE_PREFIX}validation/final-owner-manifest.json"
FINAL_CANDIDATE = f"{PHASE_PREFIX}validation/final-stage-candidate.json"
FINAL_REVIEW = f"{PHASE_PREFIX}validation/final-staged-review.json"
BATON = f"{PHASE_PREFIX}handoffs/vesper-arlen-v664-v3-activation.md"
REPORT = f"{PHASE_PREFIX}deliverables/neris-v664-v2-marigram-evidence-report.html"
TEST_MODULES = [
    "tests/test_ghc_family_neris_v664_v2.py",
    "tests/test_ghc_family_neris_v664_v2_closeout.py",
]
OWNER_CODE = {
    "scripts/build_ghc_family_v664_v2_x1.py",
    "scripts/build_ghc_family_v664_v2_evidence.py",
    "scripts/build_ghc_family_v664_v2_closeout.py",
    "scripts/ghc_family_marigram_evidence.py",
    "scripts/ghc_family_v664_v2_canonical_validator.py",
    *TEST_MODULES,
}
TEXT_SUFFIXES = {".json", ".md", ".html", ".py", ".txt", ".tex", ".mjs", ".js", ".cjs"}
PRIVATE_PATTERNS = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    "private_absolute_path": re.compile(r"(?i)(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/(?:home|Users)/)"),
    "credential": re.compile(r"(?i)(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bAKIA[0-9A-Z]{16}\b|\"(?:password|api_key|access_token|resume_token)\"\s*:)") ,
    "private_route_identifier": re.compile(r"(?i)(?:codex" r"://|vscode" r"://|app" r"://connector_[0-9a-f]+)"),
    "transcript_or_session": re.compile(r"(?i)\"(?:raw_transcript|session_stream|private_app_state|browser_route)\"\s*:"),
}
SECURITY_PATTERNS = {
    "dynamic_eval": re.compile(r"(?m)^\s*(?:eval|exec)\s*\("),
    "unsafe_pickle_load": re.compile(r"\bpickle\.loads?\s*\("),
    "shell_true": re.compile(r"\bshell\s*=\s*True\b"),
    "destructive_git": re.compile(r"git\s+(?:reset\s+--hard|push\s+--force)"),
    "recursive_delete": re.compile(r"(?i)(?:rm\s+-" r"rf|Remove-" r"Item\b[^\n]*-Recurse)"),
}


class ValidationError(RuntimeError):
    """Raised for a malformed validation input rather than a failed check."""


def run_git(*args: str, check: bool = True, timeout: int = 120) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=check, timeout=timeout,
    )


def git_text(*args: str, check: bool = True, timeout: int = 120) -> str:
    result = run_git(*args, check=check, timeout=timeout)
    return result.stdout.decode("utf-8", "strict").strip()


def strict_json(raw: bytes, label: str) -> Any:
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in values:
            if key in output:
                raise ValidationError(f"duplicate JSON key {key!r} in {label}")
            output[key] = value
        return output

    return json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=pairs)


def blob(commit: str, path: str) -> bytes:
    return run_git("show", f"{commit}:{path}").stdout


def git_json(commit: str, path: str) -> dict[str, Any]:
    value = strict_json(blob(commit, path), path)
    if not isinstance(value, dict):
        raise ValidationError(f"JSON root is not an object: {path}")
    return value


def zpaths(*args: str) -> list[str]:
    raw = run_git(*args).stdout.decode("utf-8", "strict")
    return sorted(path for path in raw.split("\0") if path)


def owner_scope(path: str) -> bool:
    return path.startswith(PHASE_PREFIX) or path in OWNER_CODE


def replay_manifest(commit: str, manifest_path: str) -> dict[str, Any]:
    manifest = git_json(commit, manifest_path)
    mismatches: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in manifest.get("entries", []):
        path = row.get("path")
        if not isinstance(path, str) or path in seen:
            mismatches.append({"path": str(path), "reason": "missing or duplicate path"})
            continue
        seen.add(path)
        try:
            raw = blob(commit, path)
            object_id = git_text("rev-parse", f"{commit}:{path}")
        except (subprocess.CalledProcessError, UnicodeError):
            mismatches.append({"path": path, "reason": "blob unavailable"})
            continue
        if object_id != row.get("git_blob"):
            mismatches.append({"path": path, "reason": "Git blob identity differs"})
        if hashlib.sha256(raw).hexdigest() != row.get("sha256"):
            mismatches.append({"path": path, "reason": "SHA-256 differs"})
        if len(raw) != row.get("bytes"):
            mismatches.append({"path": path, "reason": "byte count differs"})
    return {
        "manifest": manifest_path,
        "declared": manifest.get("entry_count"),
        "replayed": len(seen),
        "mismatches": mismatches,
        "valid": manifest.get("valid") is True and manifest.get("entry_count") == len(seen) and not mismatches,
    }


def run_tests() -> dict[str, Any]:
    modules = []
    total = 0
    for relative in TEST_MODULES:
        result = subprocess.run(
            [sys.executable, str(ROOT / relative)], cwd=ROOT,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", check=False, timeout=300,
            env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"},
        )
        match = re.search(r"Ran (\d+) tests? in", result.stdout)
        count = int(match.group(1)) if match else 0
        total += count
        normalized = re.sub(r"Ran (\d+) tests? in [0-9.]+s", r"Ran \1 tests in <elapsed>", result.stdout)
        modules.append(
            {
                "module": relative,
                "returncode": result.returncode,
                "tests_run": count,
                "output_sha256": hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
                "valid": result.returncode == 0 and match is not None,
            }
        )
    return {"modules": modules, "tests_run": total, "valid": all(row["valid"] for row in modules)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    expected = args.expected_head.lower()
    if not re.fullmatch(r"[0-9a-f]{40}", expected):
        raise SystemExit("expected head must be a full lowercase SHA-1")
    output = Path(args.output).resolve()
    if output.is_relative_to(ROOT.resolve()) or output.suffix.lower() != ".json":
        raise SystemExit("output must be a new external JSON receipt outside the repository")
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise SystemExit("one-shot receipt path already exists; successful validation must not be replayed")

    issues: list[str] = []
    head = git_text("rev-parse", "HEAD")
    clean_before = not git_text("status", "--porcelain=v1", "--untracked-files=all")
    branch = git_text("branch", "--show-current")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    remote = run_git("ls-remote", "--exit-code", "origin", f"refs/heads/{BRANCH}", check=False, timeout=120)
    live_lines = remote.stdout.decode("utf-8", "strict").splitlines()
    live = live_lines[0].split()[0] if remote.returncode == 0 and len(live_lines) == 1 else ""
    ahead_behind = git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()

    if head != expected:
        issues.append("HEAD differs from the requested exact final")
    if branch != BRANCH:
        issues.append("current branch differs from the canonical Neris branch")
    if not clean_before:
        issues.append("worktree was not clean before validation")
    if not (head == upstream == tracking == live):
        issues.append("local, upstream, tracking, and fresh live heads differ")
    if ahead_behind != ["0", "0"]:
        issues.append("branch divergence is not 0/0")
    if git_text("rev-parse", "HEAD^") != EVIDENCE:
        issues.append("final is not the direct child of immutable evidence")
    for anchor in (SOURCE, X1, EVIDENCE):
        if run_git("merge-base", "--is-ancestor", anchor, head, check=False).returncode != 0:
            issues.append(f"required anchor is not ancestral: {anchor}")
    phase_commit_rows = git_text("rev-list", f"{SOURCE}..{head}").splitlines()
    merge_count = int(git_text("rev-list", "--count", "--merges", f"{SOURCE}..{head}"))
    parent_counts = [len(git_text("rev-list", "--parents", "-n", "1", commit).split()) - 1 for commit in phase_commit_rows]
    if len(phase_commit_rows) != 3 or merge_count != 0 or parent_counts != [1, 1, 1]:
        issues.append("phase history is not exactly three single-parent commits with zero merges")

    manifests = [
        replay_manifest(X1, X1_MANIFEST),
        replay_manifest(EVIDENCE, EVIDENCE_MANIFEST),
        replay_manifest(head, FINAL_DELTA_MANIFEST),
        replay_manifest(head, FINAL_OWNER_MANIFEST),
    ]
    if not all(row["valid"] for row in manifests):
        issues.append("one or more exact manifests failed replay")

    candidate = git_json(head, FINAL_CANDIDATE)
    final_delta = zpaths("diff", "--name-only", "-z", f"{EVIDENCE}..{head}")
    expected_delta = sorted(set(candidate["intended_allowlist"]) | {FINAL_REVIEW})
    if final_delta != expected_delta:
        issues.append("final commit delta differs from the committed allowlist plus review self-exclusion")
    owner_delta = zpaths("diff", "--name-only", "-z", f"{SOURCE}..{head}")
    out_of_scope = [path for path in owner_delta if not owner_scope(path)]
    if out_of_scope:
        issues.append("owner delta contains paths outside Neris scope")
    owner_manifest = git_json(head, FINAL_OWNER_MANIFEST)
    owner_manifest_paths = {row["path"] for row in owner_manifest["entries"]}
    owner_exclusions = set(owner_manifest["self_exclusions"])
    if owner_manifest_paths != set(owner_delta) - owner_exclusions:
        issues.append("final owner manifest coverage differs from the exact source-to-final owner delta")

    json_errors: list[dict[str, str]] = []
    privacy_hits: list[dict[str, str]] = []
    security_findings: list[dict[str, str]] = []
    json_count = 0
    text_count = 0
    changed_python = 0
    for path in owner_delta:
        raw = blob(head, path)
        suffix = Path(path).suffix.lower()
        if suffix == ".json":
            json_count += 1
            try:
                strict_json(raw, path)
            except (UnicodeError, json.JSONDecodeError, ValidationError) as exc:
                json_errors.append({"path": path, "error": str(exc)})
        if suffix not in TEXT_SUFFIXES:
            continue
        text_count += 1
        try:
            text = raw.decode("utf-8", "strict")
        except UnicodeError as exc:
            privacy_hits.append({"path": path, "class": "invalid_utf8", "detail": str(exc)})
            continue
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                privacy_hits.append({"path": path, "class": label})
        if suffix == ".py":
            changed_python += 1
            try:
                compile(text, path, "exec", dont_inherit=True)
            except SyntaxError as exc:
                security_findings.append({"path": path, "rule": "python_compile", "detail": str(exc)})
            for label, pattern in SECURITY_PATTERNS.items():
                if pattern.search(text):
                    security_findings.append({"path": path, "rule": label})
    if json_errors:
        issues.append("strict JSON parsing failed")
    if privacy_hits:
        issues.append("five-class privacy or raw-identifier scan found candidates")
    if security_findings:
        issues.append("changed-Python compile or bounded security review found issues")

    report = blob(head, REPORT).decode("utf-8", "strict")
    required_report_markers = ["<header", "<main", "<footer", "<table", "<caption", "Skip to evidence", "Reserved evaluation", "NOT_READY_FOR_STAGE_20"]
    report_structure = all(marker in report for marker in required_report_markers) and "<script" not in report.lower()
    if not report_structure:
        issues.append("static report structure or no-script boundary failed")
    baton_raw = blob(head, BATON)
    baton_text = baton_raw.decode("utf-8", "strict")
    baton_words = len(re.findall(r"\S+", baton_text))
    baton_ok = 10_000 <= baton_words <= 100_000
    if not baton_ok:
        issues.append("file-backed baton is outside the 10,000 to 100,000 word boundary")

    phase_truth = git_json(head, f"{PHASE_PREFIX}phase-truth-final.json")
    route = git_json(head, f"{PHASE_PREFIX}orchestration/terminal-route-state.json")
    truth_ok = (
        phase_truth.get("outcomes") == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
        and phase_truth.get("effective_negatives") == 24_333
        and phase_truth.get("effective_methods") == 8_747
        and phase_truth.get("effective_open_gaps") == 168
        and phase_truth.get("effective_exact_gates") == 166
        and phase_truth.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20"
    )
    route_ok = route.get("state") == "PREPARED_NOT_SENT" and route.get("message_sent") is False and route.get("successor_title") == "Vesper Arlen" and route.get("successor_phase") == "v664-v3"
    if not truth_ok:
        issues.append("final truth counts or verdict differ from the sealed contract")
    if not route_ok:
        issues.append("route is not accurately prepared and unsent")

    tests = run_tests()
    if not tests["valid"] or tests["tests_run"] != 63:
        issues.append("dependency-closed owner tests did not pass 63 of 63")
    skill_count = len([path for path in owner_delta if path.endswith("/SKILL.md") and f"{PHASE_PREFIX}skills/" in path])
    runner_count = len([path for path in owner_delta if path.startswith(f"{PHASE_PREFIX}runners/") and path.endswith(".json")])
    materialized_count = sum(
        1 for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts
    )
    file_budget_ok = len(owner_delta) < 2_000 and materialized_count < 2_000
    if skill_count != 10 or runner_count != 10:
        issues.append("skill or runner count differs from ten")
    if not file_budget_ok:
        issues.append("materialized or owner-delta file count reached the 2,000-file rotation boundary")

    clean_after = not git_text("status", "--porcelain=v1", "--untracked-files=all")
    if not clean_after:
        issues.append("worktree was not clean after validation")
    detailed = {
        "exact_head": head == expected,
        "canonical_branch": branch == BRANCH,
        "clean_before": clean_before,
        "four_way_equal": head == upstream == tracking == live,
        "zero_divergence": ahead_behind == ["0", "0"],
        "direct_evidence_parent": git_text("rev-parse", "HEAD^") == EVIDENCE,
        "source_x1_evidence_ancestry": all(run_git("merge-base", "--is-ancestor", anchor, head, check=False).returncode == 0 for anchor in (SOURCE, X1, EVIDENCE)),
        "three_single_parent_commits": len(phase_commit_rows) == 3 and parent_counts == [1, 1, 1],
        "zero_merges": merge_count == 0,
        "all_manifests": all(row["valid"] for row in manifests),
        "final_delta_allowlist": final_delta == expected_delta,
        "owner_scope": not out_of_scope,
        "owner_manifest_coverage": owner_manifest_paths == set(owner_delta) - owner_exclusions,
        "strict_json": not json_errors,
        "five_class_privacy": not privacy_hits,
        "changed_python_security": not security_findings,
        "static_report_structure": report_structure,
        "baton_word_boundary": baton_ok,
        "truth_counts": truth_ok,
        "route_prepared_not_sent": route_ok,
        "tests": tests["valid"] and tests["tests_run"] == 63,
        "ten_skills": skill_count == 10,
        "ten_runners": runner_count == 10,
        "file_budget": file_budget_ok,
        "clean_after": clean_after,
    }
    minimal_names = [
        "exact_head", "clean_before", "four_way_equal", "zero_divergence",
        "direct_evidence_parent", "three_single_parent_commits", "zero_merges",
        "all_manifests", "final_delta_allowlist", "owner_scope",
        "strict_json", "five_class_privacy", "changed_python_security",
        "truth_counts", "route_prepared_not_sent", "tests", "clean_after",
    ]
    minimal = {name: detailed[name] for name in minimal_names}
    valid = not issues and all(detailed.values()) and all(minimal.values())
    payload = {
        "schema": "ghc.family.neris.v664-v2.exact-final-canonical.v1",
        "expected_head": expected,
        "observed_head": head,
        "branch": branch,
        "invocation_count": 1,
        "successful_invocation_count": 1 if valid else 0,
        "post_success_replay": False,
        "local_upstream_tracking_live_equal": head == upstream == tracking == live,
        "ahead": int(ahead_behind[0]) if len(ahead_behind) == 2 else None,
        "behind": int(ahead_behind[1]) if len(ahead_behind) == 2 else None,
        "phase_commit_count": len(phase_commit_rows),
        "merge_count": merge_count,
        "parent_counts": parent_counts,
        "owner_delta_file_count": len(owner_delta),
        "materialized_file_count": materialized_count,
        "strict_json_parse_count": json_count,
        "privacy_scanned_text_file_count": text_count,
        "privacy_classes": sorted(PRIVATE_PATTERNS),
        "privacy_confirmed_hits": privacy_hits,
        "changed_python_count": changed_python,
        "security_findings": security_findings,
        "manifest_replays": manifests,
        "tests": tests,
        "baton_bytes": len(baton_raw),
        "baton_words": baton_words,
        "baton_sha256": hashlib.sha256(baton_raw).hexdigest(),
        "detailed_checks": detailed,
        "detailed_check_count": len(detailed),
        "detailed_checks_passed": sum(detailed.values()),
        "minimal_checks": minimal,
        "minimal_check_count": len(minimal),
        "minimal_checks_passed": sum(minimal.values()),
        "issues": issues,
        "clean_before": clean_before,
        "clean_after": clean_after,
        "same_owner_only": True,
        "independent_reproduction": False,
        "complete_repository_suite_run": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": valid,
        "boundary": "One exact-final owner-self-scoped canonical pass; not a full repository suite, independent reproduction, external audit, production certification, exhaustive security, privacy or accessibility completeness, professional validation, legal or cultural ratification, Māori authority, empirical confirmation, Theory-of-Everything proof, or Stage 20 authority.",
    }
    encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    try:
        with output.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(encoded)
    except FileExistsError:
        raise SystemExit("one-shot receipt path already exists; refusing replay")
    print(json.dumps({
        "valid": valid,
        "head": head,
        "tests": tests["tests_run"],
        "detailed": f"{sum(detailed.values())}/{len(detailed)}",
        "minimal": f"{sum(minimal.values())}/{len(minimal)}",
        "json": json_count,
        "privacy_files": text_count,
        "manifest_entries": sum(row["replayed"] for row in manifests),
        "baton_words": baton_words,
        "issues": issues,
    }, ensure_ascii=True, sort_keys=True))
    return 0 if valid else 2


if __name__ == "__main__":
    raise SystemExit(main())
