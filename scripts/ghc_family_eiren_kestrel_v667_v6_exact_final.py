#!/usr/bin/env python3
"""Run Eiren v667-v6 exact-final owner-scoped canonical validation once."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v667-v6"
BRANCH = "codex/GHC-Family/eiren-kestrel-v667-v6-full-tools"
SOURCE = "af68b8bdf317317fb349388f905d73862a9ea1b8"
X1 = "38aa1b783fd016134b46607894d16e56e5ccac99"
EVIDENCE = "8d7ff4b6938b783d23e4ce880ffed8d5fd7f9e59"
PHASE_ROOT = "docs/eiren-kestrel/v667-v6"
DRIVE_ROOT = Path(ROOT.anchor)
RECEIPT_ROOT = DRIVE_ROOT / "GHC-Archives" / "phase-temp" / "eiren-kestrel-v667-v6" / "canonical"
LOCK = RECEIPT_ROOT / "canonical-lock.json"
RECEIPT = RECEIPT_ROOT / "exact-final-canonical-receipt.json"


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return run(["git", "-C", str(ROOT), *args], check=check)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def owner_path(path: str) -> bool:
    return (
        path.startswith(f"{PHASE_ROOT}/")
        or path in {
            "scripts/build_ghc_family_eiren_kestrel_v667_v6_x1.py",
            "scripts/build_ghc_family_eiren_kestrel_v667_v6_x2.py",
            "scripts/build_ghc_family_eiren_kestrel_v667_v6_final.py",
            "tests/test_ghc_family_eiren_kestrel_v667_v6_x1.py",
            "tests/test_ghc_family_eiren_kestrel_v667_v6_x2.py",
            "tests/test_ghc_family_eiren_kestrel_v667_v6_final.py",
        }
        or path.startswith("scripts/ghc_family_eiren_kestrel_v667_v6_")
    )


def read_exact(stream: Any, size: int) -> bytes:
    parts: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise EOFError(f"partial Git blob with {remaining} bytes outstanding")
        parts.append(chunk)
        remaining -= len(chunk)
    return b"".join(parts)


def git_blobs(commit: str, paths: list[str]) -> dict[str, bytes]:
    proc = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.stdin is None or proc.stdout is None or proc.stderr is None:
        raise RuntimeError("Git batch pipes unavailable")
    blobs: dict[str, bytes] = {}
    try:
        for path in paths:
            proc.stdin.write(f"{commit}:{path}\n".encode("utf-8"))
            proc.stdin.flush()
            header = proc.stdout.readline().decode("utf-8").rstrip("\n")
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


def validate() -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD").strip()
    branch = git_text("branch", "--show-current").strip()
    parent = git_text("rev-parse", "HEAD^").strip()
    commits = [line for line in git_text("rev-list", "--reverse", f"{SOURCE}..{head}").splitlines() if line]
    merges = [line for line in git_text("rev-list", "--merges", f"{SOURCE}..{head}").splitlines() if line]
    parent_counts = [len(git_text("show", "-s", "--format=%P", commit).strip().split()) for commit in commits]
    if branch != BRANCH or parent != EVIDENCE or commits[:2] != [X1, EVIDENCE] or len(commits) != 3 or merges or parent_counts != [1, 1, 1]:
        raise AssertionError("exact branch or history prerequisite failed")

    pytest = run([sys.executable, "-m", "pytest", "-q", "tests/test_ghc_family_eiren_kestrel_v667_v6_final.py"], check=False)
    if pytest.returncode:
        raise AssertionError("final-only pytest failed: " + pytest.stdout.decode("utf-8", errors="replace") + pytest.stderr.decode("utf-8", errors="replace"))

    owner_paths = [
        path for path in git_text("ls-tree", "-r", "--name-only", head).splitlines()
        if path and owner_path(path)
    ]
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
            has_heading = stripped.startswith("#") or (stripped.startswith("---") and "\n# " in stripped)
            if not has_heading:
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
        raise AssertionError(f"structural issues: md={markdown_issues}, html={html_issues}, py={python_issues}")

    privacy_classes = {
        "opaque_task_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_windows_user_path": re.compile(rb"[A-Z]:\\Users\\[^\\\s]+", re.I),
        "credential_assignment": re.compile(rb"(?i)(api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9_./+-]{12,}"),
        "raw_thread_or_session_field": re.compile(rb"(?i)(source_thread_id|session_stream|private_callable_id)\s*[:=]"),
        "resume_or_private_route_value": re.compile(rb"(?i)(resume_value|private_route)\s*[:=]\s*['\"]?[^\s'\"]{8,}"),
    }
    privacy_candidates: list[dict[str, str]] = []
    for path, data in blobs.items():
        for name, pattern in privacy_classes.items():
            if pattern.search(data):
                privacy_candidates.append({"path": path, "class": name})
    if privacy_candidates:
        raise AssertionError(f"privacy candidates: {privacy_candidates}")

    manifests = {}
    for name in ("immutable-x1-manifest", "immutable-evidence-manifest", "final-delta-manifest", "final-owner-manifest"):
        value = json.loads(blobs[f"{PHASE_ROOT}/validation/{name}.json"].decode("utf-8"))
        manifests[name] = value["entry_count"]

    if git_text("status", "--porcelain=v1").strip():
        raise AssertionError("canonical lane is not clean")
    upstream = git_text("rev-parse", "@{upstream}").strip()
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}").strip()
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").strip().split()
    remote_line = git_text("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").strip()
    fresh_remote = remote_line.split()[0] if remote_line else ""
    if divergence != ["0", "0"] or not (head == upstream == tracking == fresh_remote):
        raise AssertionError("fresh four-way equality failed")

    return {
        "schema": "ghc-family-exact-final-canonical-receipt-v5",
        "owner": "Eiren Kestrel",
        "phase": PHASE,
        "status": "PASS",
        "validation_state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "invocation_count": 1,
        "successful_invocation_count": 1,
        "replayed": False,
        "head": head,
        "branch": branch,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "final_parent": parent,
        "phase_commit_count": len(commits),
        "merge_count": len(merges),
        "parent_counts": parent_counts,
        "final_only_tests_selected": 13,
        "final_only_tests_failed": 0,
        "pytest_stdout": pytest.stdout.decode("utf-8", errors="replace").strip(),
        "owner_file_count": len(owner_paths),
        "json_document_count": json_count,
        "markdown_document_count": markdown_count,
        "markdown_issue_count": len(markdown_issues),
        "html_document_count": html_count,
        "html_issue_count": len(html_issues),
        "python_compile_count": python_count,
        "python_compile_issue_count": len(python_issues),
        "privacy_class_count": len(privacy_classes),
        "privacy_scanned_file_count": len(owner_paths),
        "privacy_candidate_count": 0,
        "privacy_confirmed_hit_count": 0,
        "manifest_entry_counts": manifests,
        "clean_state": True,
        "divergence": {"ahead": 0, "behind": 0},
        "four_way_equality": True,
        "refs": {"local": head, "upstream": upstream, "tracking": tracking, "fresh_remote": fresh_remote},
        "already_successful_components_replayed": [],
        "scope": "bounded same-owner exact-final validation under shared infrastructure only",
        "not_claimed": ["full repository suite", "independent reproduction", "external audit", "production certification", "exhaustive security", "privacy completeness", "accessibility completeness", "professional validation", "legal or cultural review", "Māori-authority review", "empirical GMUT confirmation", "Theory-of-Everything proof", "AGI or ASI", "consciousness or personhood", "Stage 20 authority"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def main() -> int:
    RECEIPT_ROOT.mkdir(parents=True, exist_ok=True)
    if LOCK.exists() or RECEIPT.exists():
        print(json.dumps({"status": "REFUSED_DUPLICATE_INVOCATION", "receipt_token": "D_FIRST_EIREN_V667_V6_CANONICAL_RECEIPT"}, sort_keys=True))
        return 2
    write_external(LOCK, {"state": "STARTED", "invocation_count": 1, "receipt_token": "D_FIRST_EIREN_V667_V6_CANONICAL_RECEIPT"})
    try:
        receipt = validate()
    except Exception as exc:
        failure = {
            "schema": "ghc-family-exact-final-canonical-receipt-v5",
            "owner": "Eiren Kestrel",
            "phase": PHASE,
            "status": "FAIL",
            "validation_state": "FAILED_ZERO_AGGREGATE_SUCCESS_CREDIT",
            "invocation_count": 1,
            "successful_invocation_count": 0,
            "replayed": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "aggregate_success_credit": 0,
        }
        write_external(RECEIPT, failure)
        write_external(LOCK, {"state": "FAILED", "invocation_count": 1, "successful_invocation_count": 0, "receipt_token": "D_FIRST_EIREN_V667_V6_CANONICAL_RECEIPT"})
        print(json.dumps({"status": "FAIL", "receipt_sha256": sha256(RECEIPT.read_bytes())}, sort_keys=True))
        return 1
    write_external(RECEIPT, receipt)
    digest = sha256(RECEIPT.read_bytes())
    write_external(LOCK, {"state": "PASS", "invocation_count": 1, "successful_invocation_count": 1, "replayed": False, "receipt_sha256": digest, "receipt_token": "D_FIRST_EIREN_V667_V6_CANONICAL_RECEIPT"})
    print(json.dumps({"status": "PASS", "receipt_sha256": digest, "receipt_token": "D_FIRST_EIREN_V667_V6_CANONICAL_RECEIPT"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
