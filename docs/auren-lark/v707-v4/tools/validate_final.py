#!/usr/bin/env python3
"""Read-only exact-final metadata canonical for Auren Lark v707-v4.

This validator inspects committed Git blobs and saved receipts. It never
re-executes x1/x2 algorithms, tests, skills, runners, models, or hooks.
"""

from __future__ import annotations

import argparse
import ast
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
from typing import Any


SOURCE = "10a3c34c01f06a26ba771d9738fe90e5714b797c"
PLANNING = "d686188bbbdcb77b7609c246da59117a834f1b08"
X1 = "ab1df555f71c0ee8a646c2e5052d6c0fedd2fede"
X2 = "71d6f11b610084f6dd25386f43f1663eba23ecf2"
BRANCH = "codex/GHC-Family/auren-lark-main-4"
PREFIX = "docs/auren-lark/v707-v4/"


def git(repo: Path, *args: str, check: bool = True) -> str:
    completed = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=False)
    if check and completed.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {completed.stderr.strip()}")
    return completed.stdout.strip()


def git_blob(repo: Path, commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=repo)


def git_json(repo: Path, commit: str, path: str) -> Any:
    return json.loads(git_blob(repo, commit, path).decode("utf-8"))


def replay(entries: list[dict[str, Any]], repo: Path) -> tuple[int, list[dict[str, Any]]]:
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=repo, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert process.stdin is not None and process.stdout is not None
    mismatches = []
    replayed = 0
    for entry in entries:
        process.stdin.write((entry["git_blob_sha1"] + "\n").encode("ascii"))
        process.stdin.flush()
        header = process.stdout.readline().decode("ascii").strip().split()
        if len(header) != 3 or header[1] != "blob":
            mismatches.append({"path": entry["path"], "kind": "header"})
            continue
        oid, _, size_text = header
        size = int(size_text)
        data = process.stdout.read(size)
        terminator = process.stdout.read(1)
        if oid != entry["git_blob_sha1"] or size != entry["bytes"] or sha256(data).hexdigest() != entry["sha256"] or terminator != b"\n":
            mismatches.append({"path": entry["path"], "kind": "content"})
        replayed += 1
    process.stdin.close()
    process.wait()
    if process.returncode:
        stderr = process.stderr.read().decode("utf-8", "replace") if process.stderr else ""
        raise RuntimeError(f"git cat-file failed: {stderr}")
    return replayed, mismatches


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
    divergence = git(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    commits = git(repo, "rev-list", "--reverse", f"{SOURCE}..{head}").splitlines()
    parents = [git(repo, "rev-parse", f"{commit}^") for commit in commits]
    merges = int(git(repo, "rev-list", "--count", "--merges", f"{SOURCE}..{head}"))
    tracked = len(git(repo, "ls-tree", "-r", "--name-only", head).splitlines())
    check("clean-before", clean_before == "", clean_before)
    check("exact-head", head == expected, head)
    check("exact-branch", branch == BRANCH, branch)
    check("upstream-name", upstream_name == f"origin/{BRANCH}", upstream_name)
    check("local-upstream-equality", head == upstream, upstream)
    check("local-tracking-equality", head == tracking, tracking)
    check("fresh-live-equality", head == live, live)
    check("typed-zero-divergence", divergence == ["0", "0"], divergence)
    check("four-owner-commits", commits == [PLANNING, X1, X2, head], commits)
    check("zero-owner-merges", merges == 0, merges)
    check("direct-parent-chain", parents == [SOURCE, PLANNING, X1, X2], parents)
    check("file-ceiling", tracked < 2000, tracked)

    manifest_specs = [
        ("planning", PLANNING, PREFIX + "planning/manifest.json", 20),
        ("x1", X1, PREFIX + "x1/manifest.json", 28),
        ("x2", X2, PREFIX + "x2/manifest.json", 43),
        ("final", head, PREFIX + "final/manifest.json", None),
    ]
    final_entries: list[dict[str, Any]] = []
    manifest_counts = {}
    all_mismatches = []
    for label, commit, path, expected_count in manifest_specs:
        manifest = git_json(repo, commit, path)
        entries = manifest["entries"]
        replayed, mismatches = replay(entries, repo)
        manifest_counts[label] = replayed
        all_mismatches.extend({"stage": label, **row} for row in mismatches)
        check(f"{label}-manifest-count", manifest["count"] == len(entries) and (expected_count is None or len(entries) == expected_count), {"declared": manifest["count"], "actual": len(entries)})
        check(f"{label}-manifest-replay", replayed == len(entries) and not mismatches, {"replayed": replayed, "mismatches": mismatches})
        if label == "final":
            final_entries = entries
            final_manifest = manifest
    seal = git_json(repo, head, PREFIX + "final/content-seal.json")
    check("content-seal-count", seal["count"] == len(seal["entries"]), seal["count"])
    check("manifest-seal-equality", final_entries == seal["entries"], len(final_entries))
    check("manifest-seal-exclusions", final_manifest["self_exclusions"] == seal["excluded"] == ["final/manifest.json", "final/content-seal.json"], seal["excluded"])

    contents: dict[str, bytes] = {entry["path"]: git_blob(repo, head, entry["path"]) for entry in final_entries}
    json_count = 0
    markdown_count = 0
    python_count = 0
    security = []
    privacy = []
    patterns = {
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
                raise RuntimeError(f"empty Markdown: {path}")
            markdown_count += 1
        elif suffix == ".py":
            tree = ast.parse(data.decode("utf-8"), filename=path)
            python_count += 1
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security.append({"path": path, "finding": node.func.id})
                if isinstance(node, ast.Call) and any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    security.append({"path": path, "finding": "shell=True"})
        if suffix in {".json", ".md", ".txt", ".html", ".py"}:
            text = data.decode("utf-8")
            for label, pattern in patterns.items():
                if pattern.search(text):
                    privacy.append({"path": path, "class": label})
    check("strict-json-parses", json_count > 0, json_count)
    check("markdown-nonempty", markdown_count > 0, markdown_count)
    check("python-ast-parses", python_count > 0, python_count)
    check("bounded-python-security", not security, security)
    check("five-class-privacy", not privacy, privacy)

    phase_truth = json.loads(contents[PREFIX + "final/phase-truth.json"].decode("utf-8"))
    accounting = json.loads(contents[PREFIX + "final/accounting.json"].decode("utf-8"))
    proposals = json.loads(contents[PREFIX + "planning/proposals.json"].decode("utf-8"))
    inherited = json.loads(contents[PREFIX + "planning/inherited-zero-credit.json"].decode("utf-8"))
    x1_summary = json.loads(contents[PREFIX + "x1/session-summary.json"].decode("utf-8"))
    x2_summary = json.loads(contents[PREFIX + "x2/session-summary.json"].decode("utf-8"))
    x1_tests = json.loads(contents[PREFIX + "x1/tests.json"].decode("utf-8"))
    x2_tests = json.loads(contents[PREFIX + "x2/tests.json"].decode("utf-8"))
    hooks = json.loads(contents[PREFIX + "x2/hook-receipts.json"].decode("utf-8"))
    baton_index = json.loads(contents[PREFIX + "final/baton-index.json"].decode("utf-8"))
    baton = contents[PREFIX + "final/baton.md"]
    check("contracts", proposals["count"] == len(proposals["proposals"]) == 300, proposals["count"])
    check("inherited-zero-credit", inherited["count"] == len(inherited["records"]) == 300 and all(row["novelty_credit"] == row["completion_credit"] == 0 for row in inherited["records"]), inherited["count"])
    check("four-truth-labels", phase_truth["outcomes"] == {"completed": 255, "represented": 15, "open_gap": 15, "exact_gate": 15}, phase_truth["outcomes"])
    check("owner-accounting", phase_truth["owner_counts"] == {"methods": 33, "witnesses": 2867, "pass": 2249, "fail": 618, "negatives": 618, "open_gaps": 21, "exact_gates": 20}, phase_truth["owner_counts"])
    check("repository-accounting", phase_truth["repository_effective"] == {"methods": 6732, "witnesses": 307567, "pass": 236646, "fail": 70921, "negatives": 79754, "open_gaps": 2457, "exact_gates": 2799}, phase_truth["repository_effective"])
    check("arithmetic", accounting["pass_plus_fail_equals_witnesses"] is True, accounting["pass_plus_fail_equals_witnesses"])
    check("terminal-verdict", phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", phase_truth["terminal_verdict"])
    check("route-prepared", phase_truth["canonical_state"] == "NOT_YET_INVOKED" and phase_truth["route_state"] == "PREPARED_NOT_SENT" and phase_truth["recipient_completion"] == "UNCLAIMED", {"canonical": phase_truth["canonical_state"], "route": phase_truth["route_state"], "recipient": phase_truth["recipient_completion"]})
    check("x1-saved", x1_summary["state"] == "VALID_X1_OWNER_SCOPED" and x1_tests["count"] == x1_tests["passed"] == 20, {"state": x1_summary["state"], "tests": x1_tests["passed"]})
    check("x2-saved", x2_summary["state"] == "VALID_X2_OWNER_SCOPED" and x2_tests["count"] == x2_tests["passed"] == 30, {"state": x2_summary["state"], "tests": x2_tests["passed"]})
    check("hooks-uninstalled", hooks["hook_count"] == 10 and hooks["installed"] is False and hooks["live_host_observations"] == 0, {"count": hooks["hook_count"], "installed": hooks["installed"], "live": hooks["live_host_observations"]})
    check("baton-sha256", sha256(baton).hexdigest() == baton_index["sha256"], sha256(baton).hexdigest())
    check("baton-length", 2000 <= baton_index["words"] <= 100000, baton_index["words"])
    check("baton-eof", baton.decode("utf-8").rstrip().endswith("LITERAL_EOF_AUREN_V707_V4"), baton_index["literal_eof"])
    clean_after = git(repo, "status", "--porcelain=v1")
    check("clean-after", clean_after == "", clean_after)
    passed = sum(row["passed"] for row in checks)
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
        "manifest_replays": manifest_counts,
        "final_manifest_entries": len(final_entries),
        "json_parses": json_count,
        "markdown_files": markdown_count,
        "python_ast_files": python_count,
        "tracked_files": tracked,
        "complete_repository_suite": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": "Bounded same-owner exact-head metadata evidence under shared infrastructure; not the complete repository suite, an external audit, independent reproduction, production certification, exhaustive security, complete privacy or accessibility assurance, empirical confirmation, authority, personhood evidence, Theory-of-Everything proof, canon, or Stage 20 authority.",
    }
    payload["payload_sha256"] = sha256((json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")).hexdigest()
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
