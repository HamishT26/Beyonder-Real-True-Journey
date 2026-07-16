#!/usr/bin/env python3
"""Read-only exact-head and owner-manifest audit for Eiren v646-v7."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/eiren-kestrel/v646-v7/"
SOURCE = "327d0b8b6fca08d371d4dedd03e74a0bb7608c80"
X1 = "4604a34c48ba73f7d01f77e5a0bbf91a84145303"
EVIDENCE = "0ebc21bb089929a2d854ad6010174b82c6c00447"


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def blob(revision: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{revision}:{relative}"], cwd=ROOT)


def ancestor(left: str, right: str) -> bool:
    return subprocess.run(["git", "merge-base", "--is-ancestor", left, right], cwd=ROOT).returncode == 0


def privacy_scan(revision: str, paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_local_path": re.compile(rb"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Documents|AppData)[\\/]", re.I),
        "credential_material": re.compile(rb"(?<![A-Za-z0-9_-])(?:ghp_[A-Za-z0-9]{20,}|sk-(?:proj-|svcacct-)?[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|Bearer\s+[A-Za-z0-9._~-]{16,})", re.I),
        "private_callable_identifier": re.compile(rb"\b(?:mcp__|codex_app__|browser_[a-z0-9_]{6,})", re.I),
        "session_transcript_or_stream": re.compile(rb"(?:sessions[\\/][0-9]{4}[\\/]|rollout-[0-9]{4}|session[_ -]?stream|raw transcript)", re.I),
    }
    hits = []
    for relative in paths:
        raw = blob(revision, relative)
        for name, pattern in patterns.items():
            count = len(pattern.findall(raw))
            if count:
                hits.append({"path": relative, "class": name, "count": count})
    return {"files_scanned": len(paths), "pattern_classes": len(patterns), "confirmed_hits": hits, "confirmed_hit_count": sum(row["count"] for row in hits)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--mode", choices=["canonical", "named"], required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    clean_before = not git("status", "--porcelain=v1", "--untracked-files=all")
    head = git("rev-parse", "HEAD")
    branch = git("symbolic-ref", "--short", "HEAD", check=False)
    issues = []
    if head != args.expected_head:
        issues.append("exact head mismatch")
    if not branch:
        issues.append("detached head")
    if git("rev-parse", f"{head}^") != EVIDENCE:
        issues.append("final parent is not evidence commit")
    if not all((ancestor(SOURCE, X1), ancestor(X1, EVIDENCE), ancestor(EVIDENCE, head))):
        issues.append("anchor ancestry incomplete")
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..{head}"))
    merges = int(git("rev-list", "--merges", "--count", f"{SOURCE}..{head}"))
    parent_count = len(git("show", "-s", "--format=%P", head).split())
    if phase_commits != 3 or merges != 0 or parent_count != 1:
        issues.append("commit count, merge count, or final parent count invalid")

    manifest_path = PHASE_PREFIX + "validation/final-owner-manifest.json"
    manifest = json.loads(blob(head, manifest_path).decode("utf-8"))
    entries = manifest.get("entries", [])
    for entry in entries:
        if hashlib.sha256(blob(head, entry["path"])).hexdigest() != entry.get("sha256"):
            issues.append(f"manifest mismatch: {entry['path']}")
    phase_paths = sorted(line for line in git("ls-tree", "-r", "--name-only", head, PHASE_PREFIX).splitlines() if line)
    exclusions = set(manifest.get("declared_self_exclusions", []))
    if set(phase_paths) - {row["path"] for row in entries} != exclusions:
        issues.append("manifest coverage mismatch")
    json_parsed = 0
    for relative in phase_paths:
        if relative.endswith(".json"):
            try:
                json.loads(blob(head, relative).decode("utf-8"))
                json_parsed += 1
            except (UnicodeDecodeError, json.JSONDecodeError):
                issues.append(f"JSON parse failure: {relative}")
    privacy = privacy_scan(head, phase_paths)
    if privacy["confirmed_hit_count"]:
        issues.append("privacy or raw-identifier hit")

    upstream = git("rev-parse", "@{upstream}", check=False)
    live = ""
    remote_equal = None
    if args.mode == "canonical":
        tracking = git("rev-parse", "refs/remotes/origin/codex/GHC-Family/eiren-kestrel-v643-v1-full-tools", check=False)
        live_rows = git("ls-remote", "origin", "refs/heads/codex/GHC-Family/eiren-kestrel-v643-v1-full-tools", check=False).splitlines()
        live = live_rows[0].split("\t", 1)[0] if live_rows else ""
        remote_equal = head == upstream == tracking == live
        if not remote_equal:
            issues.append("canonical four-way equality failed")
    else:
        live_rows = git("ls-remote", "origin", f"refs/heads/{branch}", check=False).splitlines()
        if upstream or live_rows:
            issues.append("named lane has upstream or live remote ref")

    clean_after = not git("status", "--porcelain=v1", "--untracked-files=all")
    if not clean_before or not clean_after:
        issues.append("worktree not clean before and after")
    payload = {
        "schema": "ghc.family.v646-v7.exact-head-audit.v1", "mode": args.mode,
        "head": head, "expected_head": args.expected_head, "branch": branch,
        "clean_before": clean_before, "clean_after": clean_after,
        "source": SOURCE, "x1": X1, "evidence": EVIDENCE,
        "phase_commits": phase_commits, "merges": merges, "final_parent_count": parent_count,
        "manifest_entries": len(entries), "manifest_exclusions": sorted(exclusions),
        "phase_files": len(phase_paths), "json_parsed": json_parsed, "privacy": privacy,
        "upstream_present": bool(upstream), "live_remote_ref_present": bool(live) if args.mode == "canonical" else bool(live_rows),
        "remote_equal": remote_equal, "issue_count": len(issues), "issues": issues,
        "same_owner_only": True, "independent_reproduction": False,
        "result": "pass" if not issues else "fail",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"mode": args.mode, "head": head, "phase_commits": phase_commits, "merges": merges, "manifest": len(entries), "phase_files": len(phase_paths), "json": json_parsed, "privacy_hits": privacy["confirmed_hit_count"], "issues": len(issues), "result": payload["result"]}, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
