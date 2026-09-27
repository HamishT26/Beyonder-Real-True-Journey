#!/usr/bin/env python3
"""Read-only exact-final metadata canonical for Mira Fenwick v707-v3.

This validator inspects committed Git blobs and saved receipts.  It never
re-executes the phase solver, x1/x2 tests, runners, skills, models, or hooks.
"""

from __future__ import annotations

import argparse
import ast
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


SOURCE = "d3582b4dcd084f80d7b3ea569a2d7f962eb98576"
BRANCH = "codex/GHC-Family/mira-fenwick-main-4"
PREFIX = "docs/mira-fenwick/v707-v3/"
MANIFEST = PREFIX + "final/manifest.json"
SEAL = PREFIX + "final/content-seal.json"


def git(repo: Path, *args: str, check: bool = True) -> str:
    completed = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=False)
    if check and completed.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {completed.stderr.strip()}")
    return completed.stdout.strip()


def git_blob(repo: Path, head: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{head}:{path}"], cwd=repo)


def git_json(repo: Path, head: str, path: str) -> Any:
    return json.loads(git_blob(repo, head, path).decode("utf-8"))


def replay_manifest(repo: Path, entries: list[dict[str, Any]]) -> tuple[dict[str, bytes], list[dict[str, Any]]]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=repo,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None
    contents: dict[str, bytes] = {}
    mismatches: list[dict[str, Any]] = []
    for entry in entries:
        process.stdin.write((entry["git_blob_sha1"] + "\n").encode("ascii"))
        process.stdin.flush()
        header = process.stdout.readline().decode("ascii").strip().split()
        if len(header) != 3 or header[1] != "blob":
            mismatches.append({"path": entry["path"], "kind": "header", "actual": header})
            continue
        actual_oid, _, size_text = header
        size = int(size_text)
        data = process.stdout.read(size)
        terminator = process.stdout.read(1)
        actual_sha = sha256(data).hexdigest()
        if actual_oid != entry["git_blob_sha1"] or size != entry["bytes"] or actual_sha != entry["sha256"] or terminator != b"\n":
            mismatches.append(
                {
                    "path": entry["path"],
                    "kind": "content",
                    "expected_oid": entry["git_blob_sha1"],
                    "actual_oid": actual_oid,
                    "expected_bytes": entry["bytes"],
                    "actual_bytes": size,
                    "expected_sha256": entry["sha256"],
                    "actual_sha256": actual_sha,
                }
            )
        contents[entry["path"]] = data
    process.stdin.close()
    process.wait()
    if process.returncode:
        stderr = process.stderr.read().decode("utf-8", "replace") if process.stderr else ""
        raise RuntimeError(f"git cat-file --batch failed: {stderr}")
    return contents, mismatches


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    args = parser.parse_args()
    repo = Path(git(Path.cwd(), "rev-parse", "--show-toplevel"))
    expected = args.expected_head
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, observed: Any) -> None:
        checks.append({"name": name, "passed": bool(condition), "observed": observed})

    clean_before = git(repo, "status", "--porcelain=v1")
    head = git(repo, "rev-parse", "HEAD")
    branch = git(repo, "branch", "--show-current")
    upstream_name = git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    upstream = git(repo, "rev-parse", "@{upstream}")
    tracking = git(repo, "rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git(repo, "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    ahead_behind = git(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    commits = git(repo, "rev-list", "--reverse", f"{SOURCE}..{head}").splitlines()
    merges = int(git(repo, "rev-list", "--count", "--merges", f"{SOURCE}..{head}"))
    source_ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE, head], cwd=repo, check=False).returncode == 0
    parents = [git(repo, "rev-parse", f"{commit}^") for commit in commits]

    check("clean-before", clean_before == "", clean_before)
    check("exact-head", head == expected, head)
    check("exact-branch", branch == BRANCH, branch)
    check("upstream-name", upstream_name == f"origin/{BRANCH}", upstream_name)
    check("local-upstream-equality", head == upstream, upstream)
    check("local-tracking-equality", head == tracking, tracking)
    check("fresh-live-equality", head == live, live)
    check("typed-zero-divergence", ahead_behind == ["0", "0"], ahead_behind)
    check("source-ancestor", source_ancestor, source_ancestor)
    check("four-owner-commits", len(commits) == 4, commits)
    check("zero-owner-merges", merges == 0, merges)
    check("direct-parent-chain", len(parents) == 4 and parents == [SOURCE, *commits[:3]], parents)

    manifest = git_json(repo, head, MANIFEST)
    seal = git_json(repo, head, SEAL)
    entries = manifest["entries"]
    check("manifest-declared-count", manifest["count"] == len(entries), {"declared": manifest["count"], "actual": len(entries)})
    check("content-seal-declared-count", seal["count"] == len(seal["entries"]), {"declared": seal["count"], "actual": len(seal["entries"])})
    check("manifest-seal-entry-equality", entries == seal["entries"], len(entries))
    check("manifest-seal-exclusion-equality", manifest["self_exclusions"] == seal["excluded"] == ["final/manifest.json", "final/content-seal.json"], manifest["self_exclusions"])
    check("owner-file-ceiling", len(entries) + 2 < 2000, len(entries) + 2)
    check("owner-prefix-only", all(entry["path"].startswith(PREFIX) for entry in entries), len(entries))

    contents, mismatches = replay_manifest(repo, entries)
    check("exact-git-blob-replay", not mismatches, {"replayed": len(contents), "mismatches": mismatches})

    json_count = 0
    markdown_count = 0
    python_count = 0
    python_security: list[dict[str, str]] = []
    privacy_hits: list[dict[str, str]] = []
    privacy_patterns = {
        "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "provider_secret": re.compile(r"\b(?:sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})\b"),
        "authorization_header": re.compile(r"\bBearer\s+[A-Za-z0-9._-]{20,}", re.IGNORECASE),
        "email_address": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        "phone_or_government_identifier": re.compile(r"\b(?:\+?\d[\d -]{8,}\d|\d{3}-\d{2}-\d{4})\b"),
    }
    for path, data in contents.items():
        suffix = Path(path).suffix.lower()
        if suffix == ".json":
            json.loads(data.decode("utf-8"))
            json_count += 1
        elif suffix == ".md":
            if not data.strip():
                raise RuntimeError(f"empty Markdown file: {path}")
            markdown_count += 1
        elif suffix == ".py":
            tree = ast.parse(data.decode("utf-8"), filename=path)
            python_count += 1
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    python_security.append({"path": path, "finding": node.func.id})
                if isinstance(node, ast.Call) and any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    python_security.append({"path": path, "finding": "shell=True"})
        if suffix in {".json", ".md", ".txt", ".html", ".py"}:
            text = data.decode("utf-8")
            for label, pattern in privacy_patterns.items():
                if pattern.search(text):
                    privacy_hits.append({"path": path, "class": label})
    check("strict-json-parses", json_count > 0, json_count)
    check("markdown-nonempty", markdown_count > 0, markdown_count)
    check("python-ast-parses", python_count > 0, python_count)
    check("bounded-python-security", not python_security, python_security)
    check("five-class-privacy", not privacy_hits, privacy_hits)

    phase_truth = json.loads(contents[PREFIX + "final/phase-truth.json"].decode("utf-8"))
    x1_tests = json.loads(contents[PREFIX + "x1/tests.json"].decode("utf-8"))
    x2_tests = json.loads(contents[PREFIX + "x2/tests.json"].decode("utf-8"))
    x1_skills = json.loads(contents[PREFIX + "x1/skill-validation.json"].decode("utf-8"))
    x2_skills = json.loads(contents[PREFIX + "x2/skill-validation.json"].decode("utf-8"))
    x1_runners = json.loads(contents[PREFIX + "x1/runner-receipts.json"].decode("utf-8"))
    x2_runners = json.loads(contents[PREFIX + "x2/runner-receipts.json"].decode("utf-8"))
    hooks = json.loads(contents[PREFIX + "x2/hook-receipts.json"].decode("utf-8"))
    baton_index = json.loads(contents[PREFIX + "final/baton-index.json"].decode("utf-8"))
    baton = contents[PREFIX + "final/baton.md"]
    outcomes = phase_truth["outcomes"]
    check("four-truth-labels", set(outcomes) == {"completed", "represented", "open_gap", "exact_gate"}, outcomes)
    check("outcome-counts", outcomes == {"completed": 255, "represented": 15, "open_gap": 15, "exact_gate": 15}, outcomes)
    check("terminal-verdict", phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", phase_truth["terminal_verdict"])
    check("route-prepared-not-sent", phase_truth["route_state"] == "PREPARED_NOT_SENT" and phase_truth["recipient_completion"] == "UNCLAIMED", {"route": phase_truth["route_state"], "recipient": phase_truth["recipient_completion"]})
    check("x1-saved-tests", x1_tests["count"] == x1_tests["passed"] == 20 and all(row["passed"] for row in x1_tests["records"]), {"count": x1_tests["count"], "passed": x1_tests["passed"]})
    check("x2-saved-tests", x2_tests["count"] == x2_tests["passed"] == 30 and all(row["passed"] for row in x2_tests["records"]), {"count": x2_tests["count"], "passed": x2_tests["passed"]})
    check("saved-skill-receipts", x1_skills["count"] == x2_skills["count"] == 10 and all(row["state"] == "pass" for row in x1_skills["records"] + x2_skills["records"]), 20)
    check("saved-runner-receipts", x1_runners["count"] == x2_runners["count"] == 5 and all(row["state"] == "pass" for row in x1_runners["records"] + x2_runners["records"]), 10)
    check("manual-uninstalled-hooks", hooks["count"] == 5 and hooks["installed"] is False and hooks["live_host_observations"] == 0, {"count": hooks["count"], "installed": hooks["installed"], "live": hooks["live_host_observations"]})
    check("baton-sha256", sha256(baton).hexdigest() == baton_index["sha256"], sha256(baton).hexdigest())
    check("baton-v19-length", baton_index["words"] >= 2000 and baton_index["words"] <= 100000, baton_index["words"])
    check("baton-literal-eof", baton.decode("utf-8").rstrip().endswith("LITERAL_EOF_MIRA_V707_V3"), baton_index["literal_eof"])

    clean_after = git(repo, "status", "--porcelain=v1")
    check("clean-after", clean_after == "", clean_after)
    passed = sum(1 for row in checks if row["passed"])
    failed = len(checks) - passed
    payload = {
        "state": "VALID_EXACT_FINAL_OWNER_SCOPED_METADATA_CANONICAL" if failed == 0 else "INVALID_EXACT_FINAL_OWNER_SCOPED_METADATA_CANONICAL",
        "head": head,
        "branch": branch,
        "checks": checks,
        "checks_summary": f"{passed}/{len(checks)}",
        "invocations": 1,
        "successes": 1 if failed == 0 else 0,
        "replays": 0,
        "manifest_entries": len(entries),
        "json_parses": json_count,
        "markdown_files": markdown_count,
        "python_ast_files": python_count,
        "complete_repository_suite": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": "Bounded same-owner exact-head metadata evidence under shared infrastructure; not the complete repository suite, an external audit, independent reproduction, production certification, exhaustive security, or complete privacy or accessibility assurance.",
    }
    payload["payload_sha256"] = sha256((json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")).hexdigest()
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
