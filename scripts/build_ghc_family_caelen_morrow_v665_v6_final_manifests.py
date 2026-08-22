#!/usr/bin/env python3
"""Build exact staged review and final manifests for Caelen v665-v6.

Run only while HEAD is the immutable evidence commit and every intended final
path except the generated review/manifests is already staged as an addition.
The script reviews Git index blobs, then stages its three generated artifacts.
It does not commit, push, contact another task, or invoke canonical validation.
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/caelen-morrow/v665-v6/"
EVIDENCE = "5904cd361cf276ce6c05b2829c581837640a564f"
X1 = "9be19f91371da0d2bcdd23de421fed202c5641fa"
REVIEW_PATH = PHASE_PREFIX + "validation/final-staged-review.json"
OWNER_MANIFEST_PATH = PHASE_PREFIX + "validation/final-owner-manifest.json"
DELTA_MANIFEST_PATH = PHASE_PREFIX + "validation/final-delta-manifest.json"
GENERATED_PATHS = {REVIEW_PATH, OWNER_MANIFEST_PATH, DELTA_MANIFEST_PATH}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def git_bytes(*args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], stderr=subprocess.STDOUT)


def git_text(*args: str) -> str:
    return git_bytes(*args).decode("utf-8").strip()


def write_json(path: str, payload: dict[str, Any]) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def stage(path: str) -> None:
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--", path])


def index_blob(path: str) -> bytes:
    return git_bytes("show", f":{path}")


def index_metadata(path: str) -> tuple[str, str]:
    line = git_text("ls-files", "-s", "--", path)
    if not line:
        raise RuntimeError(f"path is absent from index: {path}")
    prefix, indexed_path = line.split("\t", 1)
    mode, oid, stage_number = prefix.split()
    if indexed_path != path or stage_number != "0":
        raise RuntimeError(f"unexpected index entry for {path}")
    return mode, oid


def entry(path: str, *, status: str = "A") -> dict[str, Any]:
    blob = index_blob(path)
    mode, oid = index_metadata(path)
    return {
        "path": path,
        "status": status,
        "git_mode": mode,
        "git_blob_oid": oid,
        "size_bytes": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
    }


def staged_statuses() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in git_text("diff", "--cached", "--name-status", "HEAD").splitlines():
        if not line:
            continue
        status, path = line.split("\t", 1)
        rows.append((status, path))
    return rows


def owner_path(path: str) -> bool:
    return path.startswith(PHASE_PREFIX) or bool(
        re.fullmatch(r"(?:scripts|tests)/[^/]*v665_v6[^/]*\.py", path)
    )


def owner_paths_from_index() -> list[str]:
    return sorted(path for path in git_text("ls-files").splitlines() if owner_path(path))


def privacy_patterns() -> dict[str, re.Pattern[str]]:
    return {
        "raw_task_or_thread_identifier": re.compile(
            "(" + "source_" + "thread_id|" + "thread" + "Id|" + "task" + "Id)", re.I
        ),
        "private_absolute_path": re.compile(r"[A-Z]:\\(?:Users|GHC-Archives)\\", re.I),
        "credential_or_token_value": re.compile(
            r"(Bearer\s+[A-Za-z0-9._~-]+|api[_-]?key\s*[:=]\s*[\"']?[A-Za-z0-9])",
            re.I,
        ),
        "session_identifier_value": re.compile(
            r"session[_ -]?(?:id|stream)\s*[:=]\s*[\"']?[A-Za-z0-9]", re.I
        ),
        "private_callable_identifier_value": re.compile(
            r"(?:callable|tool)[_ -]?id\s*[:=]\s*[\"']?[A-Za-z0-9]", re.I
        ),
    }


def security_findings(path: str, text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    tree = ast.parse(text, filename=path)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            name = node.func.attr
        else:
            name = ""
        if name in {"eval", "exec", "system", "popen"}:
            findings.append({"path": path, "line": node.lineno, "class": name})
        if name in {"run", "Popen", "call", "check_call", "check_output"}:
            for keyword in node.keywords:
                if (
                    keyword.arg == "shell"
                    and isinstance(keyword.value, ast.Constant)
                    and keyword.value.value is True
                ):
                    findings.append(
                        {"path": path, "line": node.lineno, "class": "subprocess_shell_true"}
                    )
    return findings


def replay_commit_manifest(ref: str, path: str) -> dict[str, Any]:
    manifest = json.loads(git_bytes("show", f"{ref}:{path}").decode("utf-8"))
    failures: list[str] = []
    for row in manifest["entries"]:
        blob = git_bytes("show", f"{ref}:{row['path']}")
        if len(blob) != row["size_bytes"] or hashlib.sha256(blob).hexdigest() != row["sha256"]:
            failures.append(row["path"])
    return {"path": path, "entries": len(manifest["entries"]), "failures": failures}


def replay_index_manifest(path: str) -> list[str]:
    manifest = json.loads((ROOT / path).read_text(encoding="utf-8"))
    failures: list[str] = []
    for row in manifest["entries"]:
        blob = index_blob(row["path"])
        if len(blob) != row["size_bytes"] or hashlib.sha256(blob).hexdigest() != row["sha256"]:
            failures.append(row["path"])
    return failures


def main() -> None:
    if git_text("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("final manifests must be built at the immutable evidence commit")

    statuses = staged_statuses()
    if not statuses:
        raise RuntimeError("no intended final paths are staged")
    if any(status != "A" for status, _ in statuses):
        raise RuntimeError("the final delta must contain additions only")
    staged_paths = [path for _, path in statuses]
    if any(not owner_path(path) for path in staged_paths):
        raise RuntimeError("a staged path is outside the Caelen v665-v6 owner scope")
    if git_text("diff", "--name-only"):
        raise RuntimeError("unstaged tracked changes remain")
    if git_text("ls-files", "--others", "--exclude-standard"):
        raise RuntimeError("unstaged untracked paths remain")

    patterns = privacy_patterns()
    json_failures: list[str] = []
    compile_failures: list[str] = []
    security: list[dict[str, Any]] = []
    privacy_hits: list[dict[str, str]] = []
    non_utf8: list[str] = []
    crlf_paths: list[str] = []
    word_cap_failures: list[str] = []
    reviewed_entries: list[dict[str, Any]] = []
    json_count = 0
    python_count = 0
    max_words = 0
    max_word_path = ""

    reviewed_paths = [path for path in staged_paths if path not in GENERATED_PATHS]
    for path in reviewed_paths:
        blob = index_blob(path)
        reviewed_entries.append(entry(path))
        if b"\r\n" in blob:
            crlf_paths.append(path)
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            non_utf8.append(path)
            continue
        if path.endswith(".json"):
            json_count += 1
            try:
                json.loads(text)
            except Exception:
                json_failures.append(path)
        if path.endswith(".py"):
            python_count += 1
            try:
                compile(text, path, "exec")
                security.extend(security_findings(path, text))
            except Exception:
                compile_failures.append(path)
        words = len(re.findall(r"\S+", text))
        if words > max_words:
            max_words, max_word_path = words, path
        if words > 100_000:
            word_cap_failures.append(path)
        for class_name, pattern in patterns.items():
            if pattern.search(text):
                privacy_hits.append({"class": class_name, "path": path})

    route = json.loads(index_blob(PHASE_PREFIX + "orchestration/route-state-final-candidate.json"))
    baton_blob = index_blob(route["prepared_baton"])
    baton_words = len(re.findall(r"\S+", baton_blob.decode("utf-8")))
    baton_integrity = (
        10_000 <= baton_words <= 100_000
        and baton_words == route["prepared_baton_words"]
        and hashlib.sha256(baton_blob).hexdigest() == route["prepared_baton_sha256"]
    )
    x1_replay = replay_commit_manifest(
        X1, PHASE_PREFIX + "validation/x1-content-manifest.json"
    )
    evidence_replay = replay_commit_manifest(
        EVIDENCE, PHASE_PREFIX + "validation/evidence-content-manifest.json"
    )
    checks = {
        "staged_paths_nonempty": bool(reviewed_paths),
        "additive_only": all(status == "A" for status, _ in statuses),
        "owner_scope_only": all(owner_path(path) for path in staged_paths),
        "utf8_only": not non_utf8,
        "lf_only": not crlf_paths,
        "all_staged_json_parse": not json_failures,
        "staged_python_compile": not compile_failures,
        "bounded_python_security_zero": not security,
        "five_class_privacy_zero": not privacy_hits,
        "document_word_caps": not word_cap_failures,
        "final_file_cap": len(owner_paths_from_index()) + len(GENERATED_PATHS) <= 2000,
        "baton_integrity_and_word_cap": baton_integrity,
        "x1_manifest_replay": not x1_replay["failures"] and x1_replay["entries"] == 18,
        "evidence_manifest_replay": not evidence_replay["failures"] and evidence_replay["entries"] == 115,
        "immutable_evidence_head": git_text("rev-parse", "HEAD") == EVIDENCE,
        "working_tree_fully_staged": not git_text("diff", "--name-only")
        and not git_text("ls-files", "--others", "--exclude-standard"),
    }
    review = {
        "schema": "ghc.family.caelen-morrow.v665-v6.final-staged-review.v1",
        "owner": "Caelen Morrow",
        "phase": "v665-v6",
        "generated_at_utc": now(),
        "basis_head": EVIDENCE,
        "reviewed_paths": reviewed_paths,
        "reviewed_entries": reviewed_entries,
        "reviewed_path_count": len(reviewed_paths),
        "json_count": json_count,
        "python_count": python_count,
        "privacy_scan_classes": list(patterns),
        "privacy_candidate_hits": privacy_hits,
        "privacy_confirmed_hits": len(privacy_hits),
        "security_findings": security,
        "maximum_document_words": max_words,
        "maximum_document_path": max_word_path,
        "baton_words": baton_words,
        "baton_sha256": hashlib.sha256(baton_blob).hexdigest(),
        "x1_manifest_replay": x1_replay,
        "evidence_manifest_replay": evidence_replay,
        "checks": checks,
        "valid": all(checks.values()),
        "canonical_aggregate_invoked": False,
        "same_owner": True,
        "independent_reproduction": False,
    }
    if not review["valid"]:
        raise RuntimeError("final staged review failed: " + json.dumps(checks, sort_keys=True))
    write_json(REVIEW_PATH, review)
    stage(REVIEW_PATH)

    owner_exclusions = [OWNER_MANIFEST_PATH, DELTA_MANIFEST_PATH]
    owner_paths = [
        path for path in owner_paths_from_index() if path not in set(owner_exclusions)
    ]
    owner_manifest = {
        "schema": "ghc.family.caelen-morrow.v665-v6.content-manifest.v1",
        "owner": "Caelen Morrow",
        "phase_label": "v665-v6",
        "phase": "final_owner",
        "generated_at_utc": now(),
        "hash_source": "actual_git_index_blobs",
        "source_sha": "cacbeb47741b9e86a6a980f85f6f9658a0837f7c",
        "evidence_sha": EVIDENCE,
        "entries": [entry(path) for path in owner_paths],
        "entry_count": len(owner_paths),
        "deletion_count": 0,
        "additive_final_delta": True,
        "self_exclusions": owner_exclusions,
    }
    write_json(OWNER_MANIFEST_PATH, owner_manifest)
    stage(OWNER_MANIFEST_PATH)

    delta_paths = [path for _, path in staged_statuses() if path != DELTA_MANIFEST_PATH]
    delta_manifest = {
        "schema": "ghc.family.caelen-morrow.v665-v6.content-manifest.v1",
        "owner": "Caelen Morrow",
        "phase_label": "v665-v6",
        "phase": "final_delta",
        "generated_at_utc": now(),
        "hash_source": "actual_git_index_blobs",
        "parent_sha": EVIDENCE,
        "entries": [entry(path) for path in delta_paths],
        "entry_count": len(delta_paths),
        "deletion_count": 0,
        "additive_only": True,
        "self_exclusions": [DELTA_MANIFEST_PATH],
    }
    write_json(DELTA_MANIFEST_PATH, delta_manifest)
    stage(DELTA_MANIFEST_PATH)

    owner_failures = replay_index_manifest(OWNER_MANIFEST_PATH)
    delta_failures = replay_index_manifest(DELTA_MANIFEST_PATH)
    final_statuses = staged_statuses()
    if owner_failures or delta_failures:
        raise RuntimeError("generated final manifest replay failed")
    if any(status != "A" for status, _ in final_statuses):
        raise RuntimeError("generated final delta is not additive")
    if git_text("diff", "--name-only") or git_text("ls-files", "--others", "--exclude-standard"):
        raise RuntimeError("generated final paths are not fully staged")

    print(
        json.dumps(
            {
                "status": "PASS",
                "reviewed_paths": len(reviewed_paths),
                "final_delta_entries": len(delta_paths),
                "final_owner_entries": len(owner_paths),
                "final_staged_paths": len(final_statuses),
                "json": json_count,
                "python": python_count,
                "privacy_confirmed_hits": len(privacy_hits),
                "canonical_invoked": False,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
