#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical validator for Elowen v678-v5."""

from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


OWNER = "Elowen Cairn"
PHASE = "v678-v5"
BRANCH = "codex/GHC-Family/elowen-cairn-v678-v5-full-tools"
SOURCE = "0021481a0c9681c077bce277e6ac0f2fcb37dbcd"
X1 = "c938128b0e6307c4aaed8966340486b8c5315382"
EVIDENCE = "04095ca5d8ee6b37f47de2540afa0047f67ca61c"
OWNER_PREFIX = "docs/elowen-cairn/v678-v5/"
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
COUNTS = {
    "effective_negatives": 47001,
    "effective_methods": 44552,
    "retained_failed_witnesses": 18662,
    "bounded_passing_witnesses": 28975,
    "open_gaps": 407,
    "exact_gates": 398,
}
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(rb"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(rb"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(rb"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(rb"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
}
BOUNDARY = (
    "Bounded same-owner software and documentation evidence under shared infrastructure only; "
    "not a full-repository suite, independent reproduction, external audit, empirical validation, "
    "professional certification, production readiness, legal or cultural ratification, "
    "Māori-authority review, complete privacy or accessibility assurance, exhaustive security, "
    "proof, canon, or Stage 20 authority."
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalized(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def digest_json(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def write_json(path: Path, value: Any, *, exclusive: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if exclusive:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
    else:
        path.write_text(payload, encoding="utf-8", newline="\n")


def run(repo: Path, command: list[str], *, timeout: int = 900, check: bool = True, cwd: Path | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(command, cwd=cwd or repo, capture_output=True, check=check, timeout=timeout)


def git(repo: Path, *args: str) -> str:
    return run(repo, ["git", *args], timeout=300).stdout.decode("utf-8", "strict").strip()


def allowed(path: str) -> bool:
    return (
        path.startswith(OWNER_PREFIX)
        or re.fullmatch(r"scripts/(?:build_ghc_family|ghc_family|validate_ghc_family)_elowen_cairn_v678_v5_.*\.py", path) is not None
        or re.fullmatch(r"tests/test_ghc_family_elowen_cairn_v678_v5_.*\.py", path) is not None
    )


def changed(repo: Path, start: str, end: str) -> set[str]:
    return {
        path
        for path in git(repo, "diff", "--name-only", "--diff-filter=ACMR", start, end, "--").splitlines()
        if path and allowed(path)
    }


def tree_map(repo: Path, commit: str) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for line in git(repo, "ls-tree", "-r", commit).splitlines():
        if not line:
            continue
        left, path = line.split("\t", 1)
        mode, kind, oid = left.split()
        if kind == "blob":
            result[path] = (mode, oid)
    return result


def batch_blobs(repo: Path, oids: set[str]) -> dict[str, bytes]:
    if not oids:
        return {}
    proc = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=repo,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.stdin and proc.stdout
    result: dict[str, bytes] = {}
    for oid in sorted(oids):
        proc.stdin.write((oid + "\n").encode("ascii"))
        proc.stdin.flush()
        header = proc.stdout.readline().split()
        if len(header) < 3 or header[1] != b"blob":
            raise RuntimeError(f"non-blob object in batch: {oid}")
        raw = proc.stdout.read(int(header[2]))
        proc.stdout.read(1)
        result[oid] = raw
    proc.stdin.close()
    proc.stdin = None
    _stdout, stderr = proc.communicate(timeout=60)
    if proc.returncode:
        raise RuntimeError(stderr.decode("utf-8", "replace"))
    return result


def replay_manifest(
    repo: Path,
    head: str,
    manifest_path: Path,
    expected_paths: set[str],
    objects: dict[str, tuple[str, str]],
    blobs: dict[str, bytes],
) -> dict[str, Any]:
    value = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = value["entries"]
    exclusions = {row["path"] for row in value.get("declared_exclusions", [])}
    entry_paths = {row["path"] for row in entries}
    failures: list[str] = []
    if entry_paths & exclusions:
        failures.append("entry_exclusion_overlap")
    if entry_paths | exclusions != expected_paths:
        failures.append("path_set_mismatch")
    if value.get("entry_count") != len(entries):
        failures.append("entry_count_mismatch")
    for row in entries:
        path = row["path"]
        if path not in objects:
            failures.append(f"missing_path:{path}")
            continue
        oid = objects[path][1]
        if oid != row["git_blob_oid"]:
            failures.append(f"oid_mismatch:{path}")
            continue
        raw = blobs[oid]
        if hashlib.sha256(normalized(raw)).hexdigest() != row["sha256_normalized_lf"]:
            failures.append(f"hash_mismatch:{path}")
    return {
        "path": manifest_path.relative_to(repo).as_posix(),
        "tree": head,
        "entries": len(entries),
        "exclusions": len(exclusions),
        "failures": failures,
        "valid": not failures,
    }


def safe_extract_tar(raw: bytes, destination: Path) -> None:
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as archive:
        root = destination.resolve()
        for member in archive.getmembers():
            target = (destination / member.name).resolve()
            if root not in target.parents and target != root:
                raise RuntimeError("archive path escaped scratch root")
        archive.extractall(destination)


def pytest_at_tree(repo: Path, commit: str, test_path: str, scratch_root: Path) -> dict[str, Any]:
    scratch_root.mkdir(parents=True, exist_ok=True)
    temp = Path(tempfile.mkdtemp(prefix=f"ec6785-{commit[:8]}-", dir=scratch_root))
    try:
        archive = run(
            repo,
            ["git", "archive", "--format=tar", commit, OWNER_PREFIX.rstrip("/"), test_path],
            timeout=300,
        ).stdout
        safe_extract_tar(archive, temp)
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONPATH"] = str(temp)
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", test_path],
            cwd=temp,
            env=env,
            capture_output=True,
            timeout=900,
        )
        output = (result.stdout + result.stderr).decode("utf-8", "replace")
        match = re.search(r"(\d+) passed", output)
        return {
            "tree": commit,
            "test": test_path,
            "returncode": result.returncode,
            "passed": int(match.group(1)) if match else 0,
            "summary": output.strip().splitlines()[-1] if output.strip() else "no output",
        }
    finally:
        shutil.rmtree(temp)


def pytest_current(repo: Path, test_path: str) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", test_path],
        cwd=repo,
        env=env,
        capture_output=True,
        timeout=900,
    )
    output = (result.stdout + result.stderr).decode("utf-8", "replace")
    match = re.search(r"(\d+) passed", output)
    return {
        "tree": git(repo, "rev-parse", "HEAD"),
        "test": test_path,
        "returncode": result.returncode,
        "passed": int(match.group(1)) if match else 0,
        "summary": output.strip().splitlines()[-1] if output.strip() else "no output",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--latch", type=Path, required=True)
    parser.add_argument("--scratch-root", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    receipt = args.receipt.resolve()
    latch = args.latch.resolve()
    scratch_root = args.scratch_root.resolve()
    if receipt.exists() or latch.exists():
        raise SystemExit("exclusive canonical receipt or latch already exists; replay refused")
    write_json(
        latch,
        {"status": "RUNNING_EXCLUSIVE_OWNER_CANONICAL", "owner": OWNER, "phase": PHASE, "started_utc": utc_now()},
        exclusive=True,
    )

    payload: dict[str, Any] = {
        "owner": OWNER,
        "phase": PHASE,
        "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "invocation_count": 1,
        "success_count": 0,
        "replay_count": 0,
        "full_repository_suite_run": False,
        "boundary": BOUNDARY,
        "started_utc": utc_now(),
    }
    try:
        head = git(repo, "rev-parse", "HEAD")
        owner_root = repo / OWNER_PREFIX
        branch = git(repo, "branch", "--show-current")
        upstream = git(repo, "rev-parse", "@{upstream}")
        tracking = git(repo, "rev-parse", f"refs/remotes/origin/{BRANCH}")
        remote_line = git(repo, "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
        remote_fields = remote_line.split()
        fresh_remote = remote_fields[0] if len(remote_fields) == 2 else ""
        divergence_fields = git(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
        clean_before = git(repo, "status", "--porcelain=v1") == ""

        objects = tree_map(repo, head)
        owner_paths = changed(repo, SOURCE, head)
        x1_paths = changed(repo, SOURCE, X1)
        evidence_paths = changed(repo, X1, EVIDENCE)
        final_paths = changed(repo, EVIDENCE, head)
        all_oids = {objects[path][1] for path in owner_paths}
        blobs = batch_blobs(repo, all_oids)

        manifest_specs = [
            ("x1", owner_root / "validation" / "x1-manifest.json", x1_paths, tree_map(repo, X1), X1),
            ("evidence", owner_root / "validation" / "evidence-manifest.json", evidence_paths, tree_map(repo, EVIDENCE), EVIDENCE),
            ("final_delta", owner_root / "validation" / "final-delta-manifest.json", final_paths, objects, head),
            ("final_owner", owner_root / "validation" / "final-owner-manifest.json", owner_paths, objects, head),
        ]
        manifest_results = []
        for name, path, expected, mapping, tree in manifest_specs:
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest_oids = {row["git_blob_oid"] for row in manifest["entries"]}
            manifest_blobs = batch_blobs(repo, manifest_oids)
            result = replay_manifest(repo, tree, path, expected, mapping, manifest_blobs)
            result["name"] = name
            manifest_results.append(result)

        x1_tests = pytest_at_tree(repo, X1, "tests/test_ghc_family_elowen_cairn_v678_v5_x1.py", scratch_root)
        x2_tests = pytest_at_tree(repo, EVIDENCE, "tests/test_ghc_family_elowen_cairn_v678_v5_x2.py", scratch_root)
        final_tests = pytest_current(repo, "tests/test_ghc_family_elowen_cairn_v678_v5_final.py")
        tests = [x1_tests, x2_tests, final_tests]

        json_paths = sorted(path for path in owner_paths if path.endswith(".json"))
        json_failures = []
        for path in json_paths:
            try:
                json.loads(blobs[objects[path][1]].decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                json_failures.append({"path": path, "error": type(exc).__name__})

        document_paths = sorted(path for path in owner_paths if path.endswith((".md", ".html")))
        document_failures = []
        max_words = 0
        for path in document_paths:
            value = blobs[objects[path][1]].decode("utf-8")
            words = len(value.split())
            max_words = max(max_words, words)
            if words > 100_000:
                document_failures.append({"path": path, "reason": "word_ceiling"})
            if path.endswith(".md") and not value.lstrip().startswith("#"):
                document_failures.append({"path": path, "reason": "markdown_heading"})
            if path.endswith(".html") and not all(token in value.casefold() for token in ("<main", "<h1", "<title")):
                document_failures.append({"path": path, "reason": "html_structure"})

        privacy_candidates = []
        for path in sorted(owner_paths):
            if not path.endswith((".py", ".json", ".md", ".html", ".txt", ".yaml", ".yml")):
                continue
            raw = normalized(blobs[objects[path][1]])
            for category, pattern in PRIVACY_PATTERNS.items():
                if pattern.search(raw):
                    metadata = path.endswith(".py") or path.endswith("-staged-review.json") or path.endswith("privacy-adjudication.json")
                    privacy_candidates.append(
                        {
                            "path": path,
                            "category": category,
                            "adjudication": "scanner_definition_or_rejection_assertion" if metadata else "confirmed_payload_hit",
                        }
                    )
        confirmed_privacy = [row for row in privacy_candidates if row["adjudication"] == "confirmed_payload_hit"]

        python_paths = sorted(path for path in owner_paths if path.endswith(".py"))
        python_failures = []
        security_findings = []
        for path in python_paths:
            raw = blobs[objects[path][1]]
            try:
                source = raw.decode("utf-8")
                compile(source, path, "exec")
                tree = ast.parse(source, filename=path)
            except (UnicodeDecodeError, SyntaxError) as exc:
                python_failures.append({"path": path, "error": type(exc).__name__})
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security_findings.append({"path": path, "kind": node.func.id, "line": node.lineno})
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "system":
                    security_findings.append({"path": path, "kind": "system_call", "line": node.lineno})
                if isinstance(node, ast.Call) and any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    security_findings.append({"path": path, "kind": "shell_true", "line": node.lineno})

        truth = json.loads((owner_root / "final" / "phase-truth.json").read_text(encoding="utf-8"))
        flow = json.loads((owner_root / "final" / "method-flow-ledger.json").read_text(encoding="utf-8"))
        route = json.loads((owner_root / "orchestration" / "terminal-route-hold.json").read_text(encoding="utf-8"))
        staged_review = json.loads((owner_root / "validation" / "final-staged-review.json").read_text(encoding="utf-8"))
        seal = json.loads((owner_root / "closeout" / "content-seal.json").read_text(encoding="utf-8"))
        seal_failures = []
        for row in seal["entries"]:
            raw = blobs[objects[row["path"]][1]]
            if hashlib.sha256(normalized(raw)).hexdigest() != row["sha256_normalized_lf"]:
                seal_failures.append(row["path"])

        final_doc_paths = [path for path in final_paths if path.startswith(OWNER_PREFIX)]
        stale_terms = ("v676-v7", "typewriter", "7,630", "42,648", "540 exact normalized")
        stale_hits = []
        for path in sorted(final_doc_paths):
            if path == OWNER_PREFIX + "final/source-and-proposal-ledger.json":
                continue
            if not path.endswith((".json", ".md", ".html")):
                continue
            value = blobs[objects[path][1]].decode("utf-8", "replace")
            for term in stale_terms:
                if term.casefold() in value.casefold():
                    stale_hits.append({"path": path, "term": term})

        diff_check = run(repo, ["git", "diff", "--check", SOURCE, head], check=False).returncode == 0
        clean_after = git(repo, "status", "--porcelain=v1") == ""
        direct_history = (
            git(repo, "rev-parse", f"{X1}^") == SOURCE
            and git(repo, "rev-parse", f"{EVIDENCE}^") == X1
            and git(repo, "rev-parse", f"{head}^") == EVIDENCE
            and int(git(repo, "rev-list", "--count", f"{SOURCE}..{head}")) == 3
            and git(repo, "rev-list", "--merges", f"{SOURCE}..{head}") == ""
            and len(git(repo, "show", "-s", "--format=%P", head).split()) == 1
        )
        remote_equal = (
            head == upstream == tracking == fresh_remote
            and divergence_fields == ["0", "0"]
            and len(remote_fields) == 2
        )
        checks = {
            "exact_branch": branch == BRANCH,
            "direct_single_parent_zero_merge_history": direct_history,
            "clean_before": clean_before,
            "clean_after": clean_after,
            "typed_zero_divergence_and_fresh_four_way_equality": remote_equal,
            "all_lifecycle_manifests_exact": all(row["valid"] for row in manifest_results),
            "all_owner_tests_pass": all(row["returncode"] == 0 for row in tests),
            "test_partition_exact": [row["passed"] for row in tests] == [13, 10, 11],
            "all_phase_json_parse": not json_failures and len(json_paths) >= 630,
            "documents_structurally_bounded": not document_failures and len(document_paths) >= 25 and max_words <= 100_000,
            "privacy_candidates_adjudicated_zero_confirmed": not confirmed_privacy,
            "bounded_owner_python_compile_and_security": not python_failures and not security_findings,
            "phase_truth_exact": truth["declared_proposal_chain"] == 8570 and truth["core_outcomes"] == OUTCOMES and truth["current_overlay"] == COUNTS and truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
            "method_flow_exact": flow["phase_ledger_counts"] == {"methods": 810, "failed": 275, "passing": 535} and flow["current_overlay"] == COUNTS,
            "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT" and route["provisional_exact_title"] == "Sylven Arc" and route["provisional_phase"] == "v678-v6" and route["send_count"] == 0,
            "staged_review_exact": staged_review["status"] == "VALID_PRECOMMIT_FINAL_STAGED_REVIEW" and not staged_review["unexpected_paths"] and staged_review["confirmed_five_class_privacy_or_raw_identifier_hits"] == 0,
            "content_seal_exact": not seal_failures and len(seal["entries"]) == 9,
            "stale_label_review": not stale_hits,
            "diff_hygiene": diff_check,
            "owner_file_ceiling": len(owner_paths) < 2000,
            "full_repository_suite_not_run": True,
        }
        success = all(checks.values())
        payload.update(
            {
                "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if success else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
                "success_count": 1 if success else 0,
                "exact_final": head,
                "source": SOURCE,
                "x1": X1,
                "evidence": EVIDENCE,
                "checks": checks,
                "tests": tests,
                "test_count": sum(row["passed"] for row in tests),
                "manifest_results": manifest_results,
                "manifest_entry_count": sum(row["entries"] for row in manifest_results),
                "json_parse_count": len(json_paths),
                "json_failures": json_failures,
                "document_count": len(document_paths),
                "document_failures": document_failures,
                "maximum_document_words": max_words,
                "owner_file_count": len(owner_paths),
                "python_compile_count": len(python_paths),
                "python_failures": python_failures,
                "bounded_security_findings": security_findings,
                "privacy_scan_file_count": len([path for path in owner_paths if path.endswith((".py", ".json", ".md", ".html", ".txt", ".yaml", ".yml"))]),
                "privacy_candidates": privacy_candidates,
                "confirmed_privacy_or_raw_identifier_hits": confirmed_privacy,
                "stale_label_hits": stale_hits,
                "final_head_clean": clean_after,
                "divergence": divergence_fields,
                "four_way_equal": remote_equal,
                "completed_utc": utc_now(),
            }
        )
    except Exception as exc:  # retained in the exclusive failed receipt
        payload.update(
            {
                "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
                "success_count": 0,
                "error_type": type(exc).__name__,
                "error": str(exc).replace(str(repo), "<repository>"),
                "completed_utc": utc_now(),
            }
        )

    payload["canonical_payload_sha256"] = digest_json(payload)
    write_json(receipt, payload, exclusive=True)
    write_json(
        latch,
        {
            "status": payload["status"],
            "owner": OWNER,
            "phase": PHASE,
            "invocation_count": 1,
            "success_count": payload["success_count"],
            "replay_count": 0,
            "canonical_payload_sha256": payload["canonical_payload_sha256"],
            "receipt_sha256": hashlib.sha256(receipt.read_bytes()).hexdigest(),
            "completed_utc": utc_now(),
        },
    )
    print(json.dumps({key: payload.get(key) for key in ("status", "exact_final", "test_count", "json_parse_count", "manifest_entry_count", "success_count", "canonical_payload_sha256")}, sort_keys=True))
    return 0 if payload["success_count"] == 1 else 1


if __name__ == "__main__":
    raise SystemExit(main())
