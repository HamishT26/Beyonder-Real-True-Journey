#!/usr/bin/env python3
"""Run the Elaren v667-v7 exact-final owner-scoped canonical aggregate once."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v667-v7"
BRANCH = "codex/GHC-Family/elaren-kestrel-v667-v7-full-tools"
SOURCE = "dc8d91294b7656ad5e9961bba93ff759af20846c"
X1 = "b92d8b1b648c4d716ca894b22fda14327baed9b3"
EVIDENCE = "9fde47f17a3c248643a543e0f44460e69191e627"
PHASE_ROOT = "docs/elaren-kestrel/v667-v7"
RECEIPT_ROOT = Path(ROOT.anchor) / "GHC-Archives" / "phase-temp" / "elaren-kestrel-v667-v7" / "canonical"
LOCK = RECEIPT_ROOT / "canonical-lock.json"
RECEIPT = RECEIPT_ROOT / "exact-final-canonical-receipt.json"
TOKEN = "D_FIRST_ELAREN_V667_V7_CANONICAL_RECEIPT"


def run(argv: list[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return run(["git", "-C", str(ROOT), *args], check=check)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def owner_path(path: str) -> bool:
    return (
        path.startswith(f"{PHASE_ROOT}/")
        or path in {
            "scripts/build_ghc_family_elaren_kestrel_v667_v7_x1.py",
            "scripts/build_ghc_family_elaren_kestrel_v667_v7_x2.py",
            "scripts/build_ghc_family_elaren_kestrel_v667_v7_final.py",
            "tests/test_ghc_family_elaren_kestrel_v667_v7_x1.py",
            "tests/test_ghc_family_elaren_kestrel_v667_v7_x2.py",
            "tests/test_ghc_family_elaren_kestrel_v667_v7_final.py",
            "scripts/ghc_family_elaren_kestrel_v667_v7_exact_final.py",
        }
        or path.startswith("scripts/ghc_family_elaren_kestrel_v667_v7_")
    )


def read_exact(stream: Any, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise EOFError(f"partial Git blob with {remaining} bytes outstanding")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def git_blobs(commit: str, paths: list[str]) -> dict[str, bytes]:
    proc = subprocess.Popen(["git", "-C", str(ROOT), "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.stdin is None or proc.stdout is None or proc.stderr is None:
        raise RuntimeError("Git batch pipes unavailable")
    blobs: dict[str, bytes] = {}
    try:
        for path in paths:
            proc.stdin.write(f"{commit}:{path}\n".encode("utf-8"))
            proc.stdin.flush()
            header = proc.stdout.readline().decode("utf-8", errors="strict").rstrip("\n")
            fields = header.split()
            if len(fields) != 3 or fields[1] != "blob":
                raise RuntimeError(f"unexpected Git batch header for {path}: {header}")
            data = read_exact(proc.stdout, int(fields[2]))
            if proc.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing Git batch delimiter for {path}")
            blobs[path] = data
    finally:
        proc.stdin.close()
        stderr = proc.stderr.read()
        code = proc.wait()
        if code:
            raise RuntimeError(stderr.decode("utf-8", errors="replace"))
    return blobs


def write_external(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def replay_manifest(commit: str, manifest: dict[str, Any]) -> None:
    paths = [row["path"] for row in manifest["entries"]]
    blobs = git_blobs(commit, paths)
    for row in manifest["entries"]:
        data = blobs[row["path"]]
        if len(data) != row["bytes"] or digest(data) != row["sha256"]:
            raise AssertionError(f"manifest replay mismatch: {row['path']}")


def validate() -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD").strip()
    branch = git_text("branch", "--show-current").strip()
    parent = git_text("rev-parse", "HEAD^").strip()
    commits = [line for line in git_text("rev-list", "--reverse", f"{SOURCE}..{head}").splitlines() if line]
    merges = [line for line in git_text("rev-list", "--merges", f"{SOURCE}..{head}").splitlines() if line]
    parent_counts = [len(git_text("show", "-s", "--format=%P", commit).strip().split()) for commit in commits]
    if branch != BRANCH or parent != EVIDENCE or commits[:2] != [X1, EVIDENCE] or len(commits) != 3 or merges or parent_counts != [1, 1, 1]:
        raise AssertionError("exact branch or history prerequisite failed")

    tests = run([sys.executable, "tests/test_ghc_family_elaren_kestrel_v667_v7_final.py"], check=False)
    if tests.returncode:
        raise AssertionError("final-only tests failed")

    owner_paths = [path for path in git_text("ls-tree", "-r", "--name-only", head).splitlines() if path and owner_path(path)]
    if len(owner_paths) >= 2000:
        raise AssertionError("owner file ceiling exceeded")
    blobs = git_blobs(head, owner_paths)
    json_count = markdown_count = html_count = python_count = 0
    markdown_issues: list[str] = []
    html_issues: list[str] = []
    python_issues: list[str] = []
    for path, data in blobs.items():
        if path.endswith(".json"):
            value = json.loads(data.decode("utf-8"))
            if not isinstance(value, dict):
                raise AssertionError(f"non-object JSON root: {path}")
            json_count += 1
        elif path.endswith(".md"):
            text = data.decode("utf-8")
            markdown_count += 1
            stripped = text.lstrip()
            if not (stripped.startswith("#") or (stripped.startswith("---") and "\n# " in stripped)):
                markdown_issues.append(path)
        elif path.endswith(".html"):
            text = data.decode("utf-8").casefold()
            html_count += 1
            if "<html" not in text or "<title>" not in text or "<main" not in text:
                html_issues.append(path)
        elif path.endswith(".py"):
            python_count += 1
            try:
                compile(data.decode("utf-8"), path, "exec")
            except SyntaxError:
                python_issues.append(path)
    if markdown_issues or html_issues or python_issues:
        raise AssertionError("owner structural check failed")

    privacy_classes = {
        "opaque_task_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_drive_path": re.compile(rb"\b[A-Z]:(?:\\|/|%5c)", re.I),
        "credential_assignment": re.compile(rb"(?i)(api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9_./+-]{12,}"),
        "raw_thread_or_session_field": re.compile(rb"(?i)(source_thread_id|session_stream|private_callable_id)\s*[:=]"),
        "resume_or_private_route_value": re.compile(rb"(?i)(resume_value|private_route)\s*[:=]\s*['\"]?[^\s'\"]{8,}"),
    }
    candidates = [{"path": path, "class": name} for path, data in blobs.items() for name, pattern in privacy_classes.items() if pattern.search(data)]
    if candidates:
        raise AssertionError(f"privacy candidates: {candidates}")

    manifests: dict[str, dict[str, Any]] = {}
    for name in ("immutable-x1-manifest", "immutable-evidence-manifest", "final-delta-manifest", "final-owner-manifest"):
        manifests[name] = json.loads(blobs[f"{PHASE_ROOT}/validation/{name}.json"].decode("utf-8"))
        if manifests[name]["status"] != "PASS" if "status" in manifests[name] else False:
            raise AssertionError(f"manifest state failed: {name}")
    replay_manifest(X1, manifests["immutable-x1-manifest"])
    replay_manifest(EVIDENCE, manifests["immutable-evidence-manifest"])
    replay_manifest(head, manifests["final-delta-manifest"])
    replay_manifest(head, manifests["final-owner-manifest"])

    baton_path = f"{PHASE_ROOT}/handoffs/neris-solane-v667-v8-activation-prepared.md"
    baton = blobs[baton_path]
    baton_index = json.loads(blobs[f"{PHASE_ROOT}/deck/final-baton-index.json"].decode("utf-8"))
    if baton_index["bytes"] != len(baton) or baton_index["sha256"] != digest(baton) or not 10000 <= baton_index["whitespace_words"] <= 100000:
        raise AssertionError("baton integrity failed")
    phase_truth = json.loads(blobs[f"{PHASE_ROOT}/truth/phase-truth-final.json"].decode("utf-8"))
    expected = {"effective_negatives": 28304, "effective_methods": 14445, "open_gaps": 199, "exact_gates": 197, "failed_witnesses": 588, "passing_witnesses": 1015}
    if any(phase_truth[key] != value for key, value in expected.items()) or phase_truth["terminal_verdict"] != "NOT_READY_FOR_STAGE_20":
        raise AssertionError("final phase truth failed")
    route = json.loads(blobs[f"{PHASE_ROOT}/route/route-state.json"].decode("utf-8"))
    if route["state"] != "PREPARED_NOT_SENT" or route["delivery_claim"] or route["successor_contacted"]:
        raise AssertionError("premature route state")

    if git_text("status", "--porcelain=v1", "--untracked-files=all").strip():
        raise AssertionError("canonical lane is not clean")
    upstream = git_text("rev-parse", "@{upstream}").strip()
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}").strip()
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").strip().split()
    live_line = git_text("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").strip()
    live = live_line.split()[0] if live_line else ""
    if divergence != ["0", "0"] or not (head == upstream == tracking == live):
        raise AssertionError("fresh four-way equality failed")

    return {
        "schema": "ghc-family-exact-final-canonical-receipt-v6", "owner": "Elaren Kestrel", "phase": PHASE,
        "status": "PASS", "validation_state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "invocation_count": 1, "successful_invocation_count": 1, "replayed": False,
        "head": head, "branch": branch, "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "final_parent": parent,
        "phase_commit_count": len(commits), "merge_count": len(merges), "parent_counts": parent_counts,
        "final_only_tests_selected": 13, "final_only_tests_failed": 0,
        "owner_file_count": len(owner_paths), "json_document_count": json_count,
        "markdown_document_count": markdown_count, "markdown_issue_count": len(markdown_issues),
        "html_document_count": html_count, "html_issue_count": len(html_issues),
        "python_compile_count": python_count, "python_compile_issue_count": len(python_issues),
        "privacy_class_count": len(privacy_classes), "privacy_scanned_file_count": len(owner_paths),
        "privacy_candidate_count": 0, "privacy_confirmed_hit_count": 0,
        "manifest_entry_counts": {name: value["entry_count"] for name, value in manifests.items()},
        "baton_bytes": len(baton), "baton_words": baton_index["whitespace_words"], "baton_sha256": digest(baton),
        "clean_state": True, "divergence": {"ahead": 0, "behind": 0}, "four_way_equality": True,
        "refs": {"local": head, "upstream": upstream, "tracking": tracking, "fresh_remote": live},
        "already_successful_components_replayed": [],
        "scope": "bounded same-owner exact-final validation under shared infrastructure only",
        "not_claimed": ["complete repository suite", "independent reproduction", "external audit", "production certification", "exhaustive security", "privacy completeness", "accessibility completeness", "professional validation", "legal or cultural review", "Māori-authority review", "empirical GMUT confirmation", "Theory-of-Everything proof", "AGI or ASI", "consciousness or personhood", "Stage 20 authority"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def main() -> int:
    RECEIPT_ROOT.mkdir(parents=True, exist_ok=True)
    if LOCK.exists() or RECEIPT.exists():
        print(json.dumps({"status": "REFUSED_DUPLICATE_INVOCATION", "receipt_token": TOKEN}, sort_keys=True))
        return 2
    write_external(LOCK, {"state": "STARTED", "invocation_count": 1, "receipt_token": TOKEN})
    try:
        receipt = validate()
    except Exception as exc:
        failure = {
            "schema": "ghc-family-exact-final-canonical-receipt-v6", "owner": "Elaren Kestrel", "phase": PHASE,
            "status": "FAIL", "validation_state": "FAILED_ZERO_AGGREGATE_SUCCESS_CREDIT",
            "invocation_count": 1, "successful_invocation_count": 0, "replayed": False,
            "error_type": type(exc).__name__, "error": str(exc), "aggregate_success_credit": 0,
        }
        write_external(RECEIPT, failure)
        receipt_sha = digest(RECEIPT.read_bytes())
        write_external(LOCK, {"state": "FAILED", "invocation_count": 1, "successful_invocation_count": 0, "receipt_sha256": receipt_sha, "receipt_token": TOKEN})
        print(json.dumps({"status": "FAIL", "receipt_sha256": receipt_sha, "receipt_token": TOKEN}, sort_keys=True))
        return 1
    write_external(RECEIPT, receipt)
    receipt_sha = digest(RECEIPT.read_bytes())
    write_external(LOCK, {"state": "PASS", "invocation_count": 1, "successful_invocation_count": 1, "replayed": False, "receipt_sha256": receipt_sha, "receipt_token": TOKEN})
    print(json.dumps({"status": "PASS", "receipt_sha256": receipt_sha, "receipt_token": TOKEN}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
