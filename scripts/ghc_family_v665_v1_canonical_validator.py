#!/usr/bin/env python3
"""Run Orin v665-v1's singular exact-final owner-scoped canonical aggregate."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import traceback
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v665-v1"
PREFIX = "docs/orin-thale/v665-v1/"
SOURCE_FINAL = "3ec44a944aabe16f64335383885c39d9592bf849"
X1_HEAD = "1e9a49b0cc377ba2eafd90fb09e478c88f8f1f3b"
EVIDENCE_HEAD = "1104a4f2963c8782ddad8939e8b4aff50715cc42"
FIRST_FINAL = "92ec05c2cbcd6d3e6c1878b7dd7e6165491a44a9"
BRANCH = "codex/GHC-Family/orin-thale-v665-v1-full-tools"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
TEST_MODULES = [
    "tests.test_ghc_family_orin_v665_v1_x1",
    "tests.test_ghc_family_orin_v665_v1_x2",
    "tests.test_ghc_family_orin_v665_v1_closeout",
    "tests.test_ghc_family_orin_v665_v1_terminal_correction",
]


class CanonicalError(RuntimeError):
    """Raised when any exact-final canonical gate fails."""


def run(command: list[str], check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if check and result.returncode:
        raise CanonicalError(
            f"{' '.join(command)} failed ({result.returncode}): "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    return result


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return run(["git", *args], check=check)


def strict_json(raw: bytes | str, label: str) -> Any:
    text = raw.decode("utf-8") if isinstance(raw, bytes) else raw

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise CanonicalError(f"duplicate JSON key in {label}: {key}")
            value[key] = item
        return value

    try:
        return json.loads(text, object_pairs_hook=reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CanonicalError(f"strict JSON failed for {label}: {exc}") from exc


def load_json(path: Path) -> dict[str, Any]:
    value = strict_json(path.read_bytes(), str(path.relative_to(ROOT)))
    if not isinstance(value, dict):
        raise CanonicalError(f"JSON root is not an object: {path}")
    return value


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def changed_paths() -> list[str]:
    return sorted(git("diff", "--name-only", f"{SOURCE_FINAL}..HEAD").stdout.decode().splitlines())


def scan_text(path: str, raw: bytes) -> list[dict[str, str]]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return [{"path": path, "class": "non_utf8", "disposition": "confirmed_issue"}]
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)\b" + r"[0-9a-f]{8}" + r"(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"
        ),
        "private_absolute_local_path": re.compile(r"(?i)\b[a-z]:[\\/](?:users|ghc-archives)[\\/]"),
        "credential_or_secret_assignment": re.compile(
            r"(?i)(?:api[_-]?key|password|private[_-]?key|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"
        ),
        "private_route_value": re.compile(
            r"(?i)(?:resume[_ -]?value|raw[_ -]?route[_ -]?key)\s*[:=]\s*\S+"
        ),
        "transcript_or_session_payload": re.compile(
            r"(?i)(?:conversation[_ -]?export|session[_ -]?stream[_ -]?payload)\s*[:=]\s*\S+"
        ),
    }
    return [
        {
            "path": path,
            "class": name,
            "excerpt_sha256": sha256(match.group(0).encode("utf-8")),
            "disposition": "confirmed_issue",
        }
        for name, pattern in patterns.items()
        for match in pattern.finditer(text)
    ]


def replay_manifest(manifest: dict[str, Any], expected_paths: list[str]) -> dict[str, Any]:
    declared = sorted(entry["path"] for entry in manifest["entries"])
    exclusions = sorted(manifest["declared_self_exclusions"])
    covered = sorted(declared + exclusions)
    mismatches: list[str] = []
    for entry in manifest["entries"]:
        raw = git("show", f"HEAD:{entry['path']}").stdout
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            mismatches.append(entry["path"])
    return {
        "path_count": len(expected_paths),
        "entry_count": len(declared),
        "exclusion_count": len(exclusions),
        "path_set_equal": covered == expected_paths,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "valid": covered == expected_paths and not mismatches and manifest["coverage_valid"],
    }


def markdown_structure_issues(paths: list[str]) -> list[str]:
    """Apply front-matter rules to skills and report rules to other Markdown."""
    issues: list[str] = []
    for path in paths:
        text = git("show", f"HEAD:{path}").stdout.decode("utf-8")
        within_cap = len(re.findall(r"\S+", text)) <= 100_000
        if path.endswith("/SKILL.md"):
            valid = (
                text.startswith("---\nname: ghc-family-")
                and "\n---\n\n# ghc-family-" in text
                and "## Workflow" in text
                and "## Boundaries" in text
            )
        else:
            valid = text.startswith("# ") and TERMINAL_VERDICT in text
        if not valid or not within_cap:
            issues.append(path)
    return issues


def canonical_checks(expected_final: str) -> dict[str, Any]:
    before_status = git("status", "--porcelain=v1", "--untracked-files=all").stdout.decode()
    if before_status:
        raise CanonicalError("worktree is not clean before canonical validation")
    head = git("rev-parse", "HEAD").stdout.decode().strip()
    branch = git("branch", "--show-current").stdout.decode().strip()
    if head != expected_final:
        raise CanonicalError(f"exact head differs: {head} != {expected_final}")
    if branch != BRANCH:
        raise CanonicalError(f"branch differs: {branch}")

    test = run([sys.executable, "-m", "unittest", *TEST_MODULES, "-v"], check=False)
    test_output = test.stdout.decode("utf-8", "replace") + test.stderr.decode("utf-8", "replace")
    match = re.search(r"Ran (\d+) tests?", test_output)
    test_count = int(match.group(1)) if match else 0
    test_ok = test.returncode == 0 and test_count == 102 and "OK" in test_output

    paths = changed_paths()
    phase_json_paths = sorted(path for path in paths if path.startswith(PREFIX) and path.endswith(".json"))
    json_failures: list[str] = []
    for path in phase_json_paths:
        try:
            strict_json(git("show", f"HEAD:{path}").stdout, path)
        except CanonicalError:
            json_failures.append(path)

    markdown_paths = sorted(path for path in paths if path.startswith(PREFIX) and path.endswith(".md"))
    markdown_issues = markdown_structure_issues(markdown_paths)
    overview_words = len(
        re.findall(
            r"\S+",
            git("show", f"HEAD:{PREFIX}reports/final-integrated-overview.md").stdout.decode("utf-8"),
        )
    )

    html_paths = sorted(path for path in paths if path.startswith(PREFIX) and path.endswith(".html"))
    html_issues: list[str] = []
    for path in html_paths:
        text = git("show", f"HEAD:{path}").stdout.decode("utf-8")
        required = ("<html lang=", "<main", "<h1", "<h2", "<table", "<caption", TERMINAL_VERDICT)
        if not all(token in text for token in required) or "<script" in text.lower():
            html_issues.append(path)

    python_paths = sorted(path for path in paths if path.endswith(".py"))
    compile_issues: list[str] = []
    security_findings: list[dict[str, str]] = []
    dangerous_patterns = {
        "shell_true": re.compile(r"shell\s*=\s*True"),
        "os_system": re.compile(r"\bos\.system\s*\("),
        "unsafe_pickle": re.compile(r"\bpickle\.loads\s*\("),
        "unsafe_yaml": re.compile(r"\byaml\.load\s*\("),
    }
    for path in python_paths:
        raw = git("show", f"HEAD:{path}").stdout
        text = raw.decode("utf-8")
        try:
            compile(text, path, "exec")
        except SyntaxError:
            compile_issues.append(path)
        for name, pattern in dangerous_patterns.items():
            if pattern.search(text):
                security_findings.append({"path": path, "finding": name})

    privacy_hits: list[dict[str, str]] = []
    text_paths = [
        path
        for path in paths
        if Path(path).suffix.lower() in {".py", ".json", ".md", ".html", ".txt", ".tex", ".mjs", ".js"}
    ]
    for path in text_paths:
        privacy_hits.extend(scan_text(path, git("show", f"HEAD:{path}").stdout))

    owner_manifest = load_json(PHASE / "validation/correction-owner-manifest.json")
    delta_manifest = load_json(PHASE / "validation/correction-delta-manifest.json")
    owner_replay = replay_manifest(owner_manifest, paths)
    delta_paths = sorted(
        path
        for path in git("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").stdout.decode().splitlines()
        if path
    )
    delta_replay = replay_manifest(delta_manifest, delta_paths)

    source_ancestor = git("merge-base", "--is-ancestor", SOURCE_FINAL, "HEAD", check=False).returncode == 0
    x1_ancestor = git("merge-base", "--is-ancestor", X1_HEAD, "HEAD", check=False).returncode == 0
    evidence_ancestor = git("merge-base", "--is-ancestor", EVIDENCE_HEAD, "HEAD", check=False).returncode == 0
    parent = git("rev-parse", "HEAD^").stdout.decode().strip()
    parent_count = len(git("rev-list", "--parents", "-n", "1", "HEAD").stdout.decode().split()) - 1
    commit_count = int(git("rev-list", "--count", f"{SOURCE_FINAL}..HEAD").stdout.decode().strip())
    merge_count = int(git("rev-list", "--merges", "--count", f"{SOURCE_FINAL}..HEAD").stdout.decode().strip())

    truth = load_json(PHASE / "correction/phase-truth.json")
    route = load_json(PHASE / "orchestration/terminal-route-state-correction.json")
    stale_label_issues = []
    if truth.get("owner") != "Orin Thale" or truth.get("proposal_chain_after") != 4_030:
        stale_label_issues.append("phase_truth_owner_or_chain")
    if route.get("state") != "PREPARED_NOT_SENT" or route.get("send_count") != 0:
        stale_label_issues.append("route_state")
    outcome_unknown = sorted(set(truth["outcomes"]) - {"completed", "represented", "open_gap", "exact_gate"})

    diff_check = git("diff", "--check", f"{SOURCE_FINAL}..HEAD", check=False)
    diff_hygiene_ok = diff_check.returncode == 0
    file_count = sum(path.is_file() for path in PHASE.rglob("*"))

    fetch = git("fetch", "origin", BRANCH, check=False)
    upstream = git("rev-parse", "@{upstream}").stdout.decode().strip()
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}").stdout.decode().strip()
    live_rows = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").stdout.decode().split()
    live = live_rows[0] if live_rows else ""
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").stdout.decode().split()
    ahead, behind = (int(divergence[0]), int(divergence[1])) if len(divergence) == 2 else (-1, -1)
    after_status = git("status", "--porcelain=v1", "--untracked-files=all").stdout.decode()

    detailed = {
        "tests_102_of_102": test_ok,
        "strict_json": not json_failures,
        "markdown_structure": not markdown_issues,
        "overview_three_page_equivalent": overview_words >= 1_500,
        "html_structure": not html_issues,
        "python_compile": not compile_issues,
        "privacy_zero_confirmed_hits": not privacy_hits,
        "bounded_security_zero_findings": not security_findings,
        "owner_manifest": owner_replay["valid"],
        "delta_manifest": delta_replay["valid"],
        "stale_label_review": not stale_label_issues,
        "outcome_vocabulary": not outcome_unknown,
        "diff_hygiene": diff_hygiene_ok,
        "source_ancestry": source_ancestor,
        "x1_ancestry": x1_ancestor,
        "evidence_ancestry": evidence_ancestor,
        "final_direct_child_of_retained_first_final": parent == FIRST_FINAL,
        "four_phase_commits": commit_count == 4,
        "zero_merges": merge_count == 0,
        "one_final_parent": parent_count == 1,
        "exact_head": head == expected_final,
        "expected_branch": branch == BRANCH,
        "clean_before": not before_status,
        "fetch_succeeded": fetch.returncode == 0,
        "four_way_equal": head == upstream == tracking == live,
        "zero_divergence": ahead == 0 and behind == 0,
        "clean_after": not after_status,
        "file_ceiling": file_count < 2_000,
        "not_ready_for_stage20": truth["terminal_verdict"] == TERMINAL_VERDICT,
        "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0,
    }
    minimal = {
        "tests": test_ok,
        "json": not json_failures,
        "privacy": not privacy_hits,
        "security": not security_findings,
        "owner_manifest": owner_replay["valid"],
        "delta_manifest": delta_replay["valid"],
        "ancestry": source_ancestor and x1_ancestor and evidence_ancestor,
        "history": commit_count == 4 and merge_count == 0 and parent_count == 1,
        "head": head == expected_final,
        "clean": not before_status and not after_status,
        "remote": head == upstream == tracking == live and ahead == 0 and behind == 0,
        "truth": truth["terminal_verdict"] == TERMINAL_VERDICT,
        "route": route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0,
        "caps": file_count < 2_000 and overview_words >= 1_500,
        "no_full_suite": True,
    }
    all_passed = all(detailed.values()) and all(minimal.values())
    return {
        "schema": "ghc.family.orin.v665-v1.external-canonical-receipt.v1",
        "status": "passed" if all_passed else "failed",
        "expected_final": expected_final,
        "actual_final": head,
        "branch": branch,
        "test_selection": TEST_MODULES,
        "test_count": test_count,
        "test_return_code": test.returncode,
        "test_output_tail": test_output[-4_000:],
        "phase_json_count": len(phase_json_paths),
        "json_failure_count": len(json_failures),
        "markdown_count": len(markdown_paths),
        "markdown_issue_count": len(markdown_issues),
        "overview_word_count": overview_words,
        "html_count": len(html_paths),
        "html_issue_count": len(html_issues),
        "python_compile_count": len(python_paths),
        "python_compile_issue_count": len(compile_issues),
        "privacy_scanned_file_count": len(text_paths),
        "privacy_confirmed_hit_count": len(privacy_hits),
        "bounded_security_file_count": len(python_paths),
        "bounded_security_finding_count": len(security_findings),
        "owner_manifest": owner_replay,
        "delta_manifest": delta_replay,
        "lifecycle": {
            "source_final": SOURCE_FINAL,
            "x1_head": X1_HEAD,
            "evidence_head": EVIDENCE_HEAD,
            "retained_first_final": FIRST_FINAL,
            "final_head": head,
            "final_parent": parent,
            "phase_commit_count": commit_count,
            "merge_count": merge_count,
            "final_parent_count": parent_count,
            "ahead": ahead,
            "behind": behind,
            "local": head,
            "upstream": upstream,
            "tracking": tracking,
            "fresh_live": live,
        },
        "detailed_checks": detailed,
        "detailed_check_count": len(detailed),
        "detailed_pass_count": sum(detailed.values()),
        "minimal_checks": minimal,
        "minimal_check_count": len(minimal),
        "minimal_pass_count": sum(minimal.values()),
        "full_repository_suite": False,
        "same_owner_not_independent_reproduction": True,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": all_passed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--expected-final", required=True)
    args = parser.parse_args()
    receipt_path = Path(args.receipt)
    if receipt_path.exists():
        print(json.dumps({"valid": False, "error": "exclusive receipt already exists"}, sort_keys=True))
        return 2
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        receipt = canonical_checks(args.expected_final)
    except Exception as exc:  # retain exact failure rather than hide it
        receipt = {
            "schema": "ghc.family.orin.v665-v1.external-canonical-receipt.v1",
            "status": "failed",
            "expected_final": args.expected_final,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc(),
            "full_repository_suite": False,
            "valid": False,
        }
    with receipt_path.open("xb") as handle:
        handle.write(canonical_bytes(receipt))
    digest = sha256(receipt_path.read_bytes())
    print(
        json.dumps(
            {
                "valid": bool(receipt.get("valid")),
                "status": receipt.get("status"),
                "receipt_sha256": digest,
                "test_count": receipt.get("test_count", 0),
                "detailed": f"{receipt.get('detailed_pass_count', 0)}/{receipt.get('detailed_check_count', 0)}",
                "minimal": f"{receipt.get('minimal_pass_count', 0)}/{receipt.get('minimal_check_count', 0)}",
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0 if receipt.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
