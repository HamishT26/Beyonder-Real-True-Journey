#!/usr/bin/env python3
"""Run Ilyra Fen v664-v5's one-shot exact-final owner-delta validation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "9bfb7cbc8fc438367207ce8d38070cf5d7fcb74b"
X1 = "cfbca99a371f97eecb959fb92be3469c0861ddf3"
EVIDENCE = "d407ae44696da7e59e8fb3af1dfaa2891a129c54"
BRANCH = "codex/GHC-Family/ilyra-fen-v664-v5-full-tools"
PHASE_PREFIX = "docs/ilyra-fen/v664-v5/"
X1_MANIFEST = f"{PHASE_PREFIX}x1/x1-content-manifest.json"
EVIDENCE_MANIFEST = f"{PHASE_PREFIX}validation/evidence-manifest.json"
FINAL_DELTA_MANIFEST = f"{PHASE_PREFIX}validation/final-delta-manifest.json"
FINAL_OWNER_MANIFEST = f"{PHASE_PREFIX}validation/final-owner-manifest.json"
FINAL_CANDIDATE = f"{PHASE_PREFIX}validation/final-stage-candidate.json"
FINAL_REVIEW = f"{PHASE_PREFIX}validation/final-staged-review.json"
BATON = f"{PHASE_PREFIX}handoffs/auren-lark-v664-v6-activation.md"
BATON_RECEIPT = f"{PHASE_PREFIX}handoffs/auren-lark-v664-v6-activation-receipt.json"
TEST_MODULES = [
    "tests/test_ghc_family_ilyra_v664_v5.py",
    "tests/test_ghc_family_ilyra_v664_v5_closeout.py",
]
OWNER_CODE = {
    "scripts/build_ghc_family_v664_v5_x1.py",
    "scripts/build_ghc_family_v664_v5_evidence.py",
    "scripts/build_ghc_family_v664_v5_closeout.py",
    "scripts/ghc_family_structural_monitoring_evidence.py",
    "scripts/ghc_family_v664_v5_canonical_validator.py",
    *TEST_MODULES,
}
TEXT_SUFFIXES = {".json", ".md", ".html", ".py", ".txt", ".tex", ".mjs", ".js", ".cjs"}
PRIVATE_PATTERNS = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    "private_absolute_path": re.compile(r"(?i)(?:[A-Z]:" + r"\\(?:Users|GHC-Archives)\\|/(?:home|Users)/)"),
    "credential": re.compile(r"(?i)(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bAKIA[0-9A-Z]{16}\b|\"(?:password|api" + r"_key|access_token|resume_token)\"\s*:)") ,
    "private_route_identifier": re.compile(r"(?i)(?:code" + r"x://|vscode" + r"://|app://connec" + r"tor_[0-9a-f]+)"),
    "transcript_or_session": re.compile(r"(?i)\"(?:raw_" + r"transcript|session_stream|private_app_state|browser_route)\"\s*:"),
}
SECURITY_PATTERNS = {
    "dynamic_eval": re.compile(r"\beval\s*\("),
    "dynamic_exec": re.compile(r"\bexec\s*\("),
    "shell_true": re.compile(r"\bshell\s*=\s*True\b"),
    "os_system": re.compile(r"\bos\.system\s*\("),
    "pickle_load": re.compile(r"\bpickle\.loads?\s*\("),
    "unsafe_yaml": re.compile(r"\byaml\.load\s*\("),
}


class ValidationError(RuntimeError):
    """Raised when a canonical input is malformed."""


def run_git(*args: str, check: bool = True, timeout: int = 180) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )


def git_text(*args: str, check: bool = True, timeout: int = 180) -> str:
    return run_git(*args, check=check, timeout=timeout).stdout.decode("utf-8", "strict").strip()


def zpaths(*args: str) -> list[str]:
    raw = run_git(*args).stdout.decode("utf-8", "strict")
    return sorted(path for path in raw.split("\0") if path)


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


def owner_scope(path: str) -> bool:
    return path.startswith(PHASE_PREFIX) or path in OWNER_CODE


def replay_manifest(commit: str, manifest_path: str) -> dict[str, Any]:
    manifest = git_json(commit, manifest_path)
    rows = manifest.get("entries", [])
    if not isinstance(rows, list):
        raise ValidationError(f"manifest entries are not a list: {manifest_path}")
    seen: set[str] = set()
    mismatches: list[dict[str, str]] = []
    for row in rows:
        if not isinstance(row, dict):
            mismatches.append({"path": "<non-object>", "reason": "entry is not an object"})
            continue
        path = row.get("path")
        if not isinstance(path, str) or path in seen:
            mismatches.append({"path": str(path), "reason": "missing or duplicate path"})
            continue
        seen.add(path)
        try:
            observed = git_text("rev-parse", f"{commit}:{path}")
        except (subprocess.CalledProcessError, UnicodeError):
            mismatches.append({"path": path, "reason": "Git blob unavailable"})
            continue
        if row.get("git_blob") != observed:
            mismatches.append({"path": path, "reason": "exact Git blob identity differs"})
    return {
        "manifest": manifest_path,
        "declared_entries": manifest.get("entry_count"),
        "replayed_entries": len(seen),
        "canonical_content_domain": "exact_git_blob",
        "mismatches": mismatches,
        "valid": manifest.get("valid") is True and manifest.get("entry_count") == len(seen) and not mismatches,
    }


def run_tests() -> dict[str, Any]:
    modules: list[dict[str, Any]] = []
    total = 0
    for relative in TEST_MODULES:
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / relative)],
            cwd=ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=300,
            env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"},
        )
        match = re.search(r"Ran (\d+) tests? in", result.stdout)
        count = int(match.group(1)) if match else 0
        total += count
        normalized = re.sub(r"Ran (\d+) tests? in [0-9.]+s", r"Ran \1 tests in <elapsed>", result.stdout)
        modules.append({
            "module": relative,
            "returncode": result.returncode,
            "test_count": count,
            "output_sha256": hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
            "valid": result.returncode == 0 and match is not None,
        })
    return {"modules": modules, "test_count": total, "valid": all(row["valid"] for row in modules)}


def safe_write_new(output: Path, payload: dict[str, Any]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.is_symlink() or output.exists():
        raise ValidationError("one-shot receipt path already exists or is linked; refusing replay")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    descriptor: int | None = None
    try:
        descriptor = os.open(output, flags, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            descriptor = None
            json.dump(payload, handle, ensure_ascii=False, allow_nan=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        if descriptor is not None:
            os.close(descriptor)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    expected = args.expected_head.lower()
    if not re.fullmatch(r"[0-9a-f]{40}", expected):
        raise SystemExit("expected head must be one full lowercase SHA-1")
    output = Path(args.output).resolve()
    if output.is_relative_to(ROOT.resolve()) or output.suffix.lower() != ".json":
        raise SystemExit("output must be a new external JSON receipt outside the repository")
    if output.exists() or output.is_symlink():
        raise SystemExit("one-shot receipt path already exists; refusing replay")

    issues: list[str] = []
    head = git_text("rev-parse", "HEAD")
    branch = git_text("branch", "--show-current")
    clean_before = not git_text("status", "--porcelain=v1", "--untracked-files=all")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    remote_result = run_git("ls-remote", "--exit-code", "origin", f"refs/heads/{BRANCH}", check=False)
    remote_lines = remote_result.stdout.decode("utf-8", "strict").splitlines()
    live = remote_lines[0].split()[0] if remote_result.returncode == 0 and len(remote_lines) == 1 else ""
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()

    if head != expected:
        issues.append("HEAD differs from requested exact final")
    if branch != BRANCH:
        issues.append("current branch differs from canonical Ilyra branch")
    if not clean_before:
        issues.append("worktree was not clean before validation")
    if not (head == upstream == tracking == live):
        issues.append("local, upstream, tracking, and fresh live heads differ")
    if divergence != ["0", "0"]:
        issues.append("typed branch divergence is not 0/0")
    direct_chain = (
        git_text("rev-parse", "HEAD^") == EVIDENCE
        and git_text("rev-parse", f"{EVIDENCE}^") == X1
        and git_text("rev-parse", f"{X1}^") == SOURCE
    )
    if not direct_chain:
        issues.append("source, x1, evidence, and final are not one direct chain")
    for anchor in (SOURCE, X1, EVIDENCE):
        if run_git("merge-base", "--is-ancestor", anchor, head, check=False).returncode != 0:
            issues.append(f"required anchor is not ancestral: {anchor}")
    phase_commits = git_text("rev-list", f"{SOURCE}..{head}").splitlines()
    merge_count = int(git_text("rev-list", "--count", "--merges", f"{SOURCE}..{head}"))
    parent_counts = [len(git_text("rev-list", "--parents", "-n", "1", commit).split()) - 1 for commit in phase_commits]
    history_ok = len(phase_commits) == 3 and merge_count == 0 and parent_counts == [1, 1, 1]
    if not history_ok:
        issues.append("phase history is not exactly three single-parent commits with zero merges")

    manifests = [
        replay_manifest(X1, X1_MANIFEST),
        replay_manifest(EVIDENCE, EVIDENCE_MANIFEST),
        replay_manifest(head, FINAL_DELTA_MANIFEST),
        replay_manifest(head, FINAL_OWNER_MANIFEST),
    ]
    if not all(row["valid"] for row in manifests):
        issues.append("one or more exact Git-blob manifests failed replay")
    candidate = git_json(head, FINAL_CANDIDATE)
    final_delta = zpaths("diff", "--name-only", "-z", f"{EVIDENCE}..{head}")
    expected_final_delta = sorted(set(candidate["intended_allowlist_without_review"]) | {FINAL_REVIEW})
    final_delta_ok = final_delta == expected_final_delta
    if not final_delta_ok:
        issues.append("final commit delta differs from committed allowlist plus review self-exclusion")
    owner_delta = zpaths("diff", "--name-only", "-z", f"{SOURCE}..{head}")
    out_of_scope = sorted(path for path in owner_delta if not owner_scope(path))
    if out_of_scope:
        issues.append("owner delta contains paths outside Ilyra scope")
    owner_manifest = git_json(head, FINAL_OWNER_MANIFEST)
    owner_manifest_paths = {row["path"] for row in owner_manifest["entries"]}
    owner_exclusions = set(owner_manifest["self_exclusions"])
    owner_manifest_ok = owner_manifest_paths == set(owner_delta) - owner_exclusions
    if not owner_manifest_ok:
        issues.append("final owner manifest coverage differs from exact source-to-final delta")

    json_errors: list[dict[str, str]] = []
    privacy_hits: list[dict[str, str]] = []
    security_findings: list[dict[str, str]] = []
    stale_labels: list[dict[str, str]] = []
    json_count = 0
    text_count = 0
    python_count = 0
    stale_pattern = re.compile(r"(?i)ilyra(?: fen)?\s+v(?!664-v5)\d{3}-v\d")
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
        if stale_pattern.search(text):
            stale_labels.append({"path": path, "class": "stale_ilyra_phase_label"})
        if suffix == ".py":
            python_count += 1
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
        issues.append("changed-Python compile or bounded pattern review found issues")
    if stale_labels:
        issues.append("stale Ilyra phase labels found")

    baton_raw = blob(head, BATON)
    baton_text = baton_raw.decode("utf-8", "strict")
    baton_words = len(re.findall(r"\S+", baton_text))
    baton_receipt = git_json(head, BATON_RECEIPT)
    baton_ok = (
        10_000 <= baton_words <= 100_000
        and baton_receipt.get("sha256") == hashlib.sha256(baton_raw).hexdigest()
        and baton_receipt.get("state") == "PREPARED_NOT_SENT"
        and baton_receipt.get("sent_by_ilyra_fen") is False
    )
    if not baton_ok:
        issues.append("file-backed activation baton integrity or unsent truth failed")
    truth = git_json(head, f"{PHASE_PREFIX}closeout/phase-truth-final.json")
    route = git_json(head, f"{PHASE_PREFIX}orchestration/terminal-route-state.json")
    truth_ok = (
        truth.get("outcomes") == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
        and truth.get("effective_negatives") == 24676
        and truth.get("effective_methods") == 8870
        and truth.get("effective_open_gaps") == 171
        and truth.get("effective_exact_gates") == 169
        and truth.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20"
    )
    route_ok = (
        route.get("state") == "PREPARED_NOT_SENT"
        and route.get("message_sent") is False
        and route.get("successor_title") == "Auren Lark"
        and route.get("successor_phase") == "v664-v6"
        and route.get("resend_allowed") is False
    )
    if not truth_ok:
        issues.append("final truth counts or verdict differ from the sealed contract")
    if not route_ok:
        issues.append("route is not accurately prepared and unsent")

    tests = run_tests()
    if not tests["valid"] or tests["test_count"] != 97:
        issues.append("dependency-closed owner tests did not pass 97 of 97")
    skill_count = len([path for path in owner_delta if path.startswith(f"{PHASE_PREFIX}skills/") and path.endswith("/SKILL.md")])
    runner_count = len([path for path in owner_delta if path.startswith(f"{PHASE_PREFIX}x2/runners/") and path.endswith(".json")])
    card_count = len([path for path in owner_delta if path.startswith(f"{PHASE_PREFIX}deck/cards/") and path.endswith(".json")])
    surface_contracts = len([path for path in owner_delta if path.startswith(f"{PHASE_PREFIX}x2/surfaces/") and path.endswith("/contract.json")])
    security_receipt = git_json(head, f"{PHASE_PREFIX}closeout/bounded-security-review.json")
    security_receipt_ok = (
        security_receipt.get("valid") is True
        and security_receipt.get("finding_count") == 0
        and security_receipt.get("candidate_count") == 0
        and security_receipt.get("python_compile_count") == 3
        and security_receipt.get("exhaustive_security") is False
    )
    if (skill_count, runner_count, card_count, surface_contracts) != (10, 10, 253, 20):
        issues.append("skill, runner, card, or surface counts differ from their frozen contract")
    if not security_receipt_ok:
        issues.append("sanitized retained security receipt failed")
    materialized_count = sum(
        1
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts
    )
    file_budget_ok = len(owner_delta) < 2000 and materialized_count < 2000
    if not file_budget_ok:
        issues.append("materialized or owner-delta file count reached the 2,000-file guard")
    clean_after = not git_text("status", "--porcelain=v1", "--untracked-files=all")
    if not clean_after:
        issues.append("worktree was not clean after validation")

    detailed = {
        "exact_head": head == expected,
        "canonical_branch": branch == BRANCH,
        "clean_before": clean_before,
        "four_way_equal": head == upstream == tracking == live,
        "zero_divergence": divergence == ["0", "0"],
        "direct_source_x1_evidence_final_chain": direct_chain,
        "three_single_parent_commits": len(phase_commits) == 3 and parent_counts == [1, 1, 1],
        "zero_merges": merge_count == 0,
        "all_manifests": all(row["valid"] for row in manifests),
        "final_delta_allowlist": final_delta_ok,
        "owner_scope": not out_of_scope,
        "owner_manifest_coverage": owner_manifest_ok,
        "strict_json": not json_errors,
        "five_class_privacy": not privacy_hits,
        "changed_python_review": not security_findings,
        "stale_label_hygiene": not stale_labels,
        "baton_prepared_unsent": baton_ok,
        "truth_counts": truth_ok,
        "route_prepared_not_sent": route_ok,
        "tests_97": tests["valid"] and tests["test_count"] == 97,
        "ten_skills": skill_count == 10,
        "ten_runners": runner_count == 10,
        "deck_253": card_count == 253,
        "surfaces_20": surface_contracts == 20,
        "security_receipt_retained_and_sanitized": security_receipt_ok,
        "file_budget": file_budget_ok,
        "clean_after": clean_after,
    }
    minimal_names = [
        "exact_head",
        "clean_before",
        "four_way_equal",
        "zero_divergence",
        "direct_source_x1_evidence_final_chain",
        "three_single_parent_commits",
        "zero_merges",
        "all_manifests",
        "final_delta_allowlist",
        "owner_scope",
        "strict_json",
        "five_class_privacy",
        "changed_python_review",
        "truth_counts",
        "route_prepared_not_sent",
        "tests_97",
        "clean_after",
    ]
    minimal = {name: detailed[name] for name in minimal_names}
    valid = not issues and all(detailed.values()) and all(minimal.values())
    payload = {
        "schema": "ghc.family.ilyra.v664-v5.exact-final-canonical.v1",
        "expected_head": expected,
        "observed_head": head,
        "branch": branch,
        "invocation_count": 1,
        "successful_invocation_count": 1 if valid else 0,
        "post_success_replay": False,
        "local_upstream_tracking_live_equal": head == upstream == tracking == live,
        "ahead": int(divergence[0]) if len(divergence) == 2 else None,
        "behind": int(divergence[1]) if len(divergence) == 2 else None,
        "phase_commit_count": len(phase_commits),
        "merge_count": merge_count,
        "parent_counts": parent_counts,
        "owner_delta_file_count": len(owner_delta),
        "materialized_file_count": materialized_count,
        "strict_json_parse_count": json_count,
        "privacy_scanned_text_file_count": text_count,
        "privacy_classes": sorted(PRIVATE_PATTERNS),
        "privacy_confirmed_hits": privacy_hits,
        "changed_python_count": python_count,
        "security_pattern_findings": security_findings,
        "stale_label_findings": stale_labels,
        "manifest_replays": manifests,
        "manifest_entries_replayed": sum(row["replayed_entries"] for row in manifests),
        "tests": tests,
        "baton_bytes": len(baton_raw),
        "baton_words": baton_words,
        "baton_sha256": hashlib.sha256(baton_raw).hexdigest(),
        "skill_count": skill_count,
        "runner_count": runner_count,
        "card_count": card_count,
        "surface_count": surface_contracts,
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
        "boundary": "One exact-final owner-self-scoped canonical pass; not a complete repository suite, independent reproduction, external audit, production certification, exhaustive security, privacy or accessibility completeness, professional validation, legal or cultural ratification, Māori authority, empirical confirmation, Theory-of-Everything proof, canon, personhood evidence, or Stage 20 authority.",
    }
    safe_write_new(output, payload)
    print(json.dumps({
        "valid": valid,
        "head": head,
        "tests": tests["test_count"],
        "detailed": f"{sum(detailed.values())}/{len(detailed)}",
        "minimal": f"{sum(minimal.values())}/{len(minimal)}",
        "json": json_count,
        "privacy_files": text_count,
        "manifest_entries": payload["manifest_entries_replayed"],
        "baton_words": baton_words,
        "issues": issues,
    }, ensure_ascii=True, sort_keys=True))
    return 0 if valid else 2


if __name__ == "__main__":
    raise SystemExit(main())
