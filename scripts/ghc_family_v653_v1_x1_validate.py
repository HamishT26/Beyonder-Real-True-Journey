#!/usr/bin/env python3
"""Validate the exact staged Vesper v653-v1 x1-only packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/vesper-arlen/v653-v1/"
PHASE = REPO / PHASE_PREFIX
ALLOWED_EXACT = {
    "scripts/ghc_family_v653_v1_phase_data.py",
    "scripts/build_ghc_family_v653_v1_preregistration.py",
    "scripts/ghc_family_v653_v1_x1_validate.py",
    "tests/test_ghc_family_v653_v1_x1.py",
}
RECEIPTS = {
    f"{PHASE_PREFIX}validation/x1-staged-manifest.json",
    f"{PHASE_PREFIX}validation/x1-staged-privacy.json",
    f"{PHASE_PREFIX}validation/x1-staged-review.json",
}


def git(*args: str, text: bool = True):
    completed = subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
    )
    return completed.stdout


def staged_paths() -> list[str]:
    return sorted(
        row.replace("\\", "/")
        for row in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()
        if row.strip()
    )


def staged_bytes(path: str) -> bytes:
    return git("show", f":{path}", text=False)


def staged_blob(path: str) -> str:
    row = git("ls-files", "-s", "--", path).strip()
    if not row:
        raise RuntimeError(f"staged blob missing: {path}")
    return row.split()[1]


def staged_blob_map(paths: list[str]) -> dict[str, str]:
    rows = git("ls-files", "-s", "--", *paths).splitlines()
    mapping: dict[str, str] = {}
    for row in rows:
        metadata, path = row.split("\t", 1)
        _mode, object_id, stage = metadata.split()
        if stage == "0" and path in paths:
            mapping[path] = object_id
    missing = sorted(set(paths) - set(mapping))
    if missing:
        raise RuntimeError(f"staged blob map missing paths: {missing}")
    return mapping


def batch_blob_bytes(object_ids: list[str]) -> dict[str, bytes]:
    unique_ids = list(dict.fromkeys(object_ids))
    completed = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        check=True,
        input=("\n".join(unique_ids) + "\n").encode("ascii"),
        capture_output=True,
    )
    output = completed.stdout
    cursor = 0
    payloads: dict[str, bytes] = {}
    for requested_id in unique_ids:
        header_end = output.index(b"\n", cursor)
        header = output[cursor:header_end].decode("ascii")
        actual_id, object_type, size_text = header.split()
        if object_type != "blob":
            raise RuntimeError(f"expected blob for {requested_id}, found {object_type}")
        size = int(size_text)
        payload_start = header_end + 1
        payload_end = payload_start + size
        payloads[actual_id] = output[payload_start:payload_end]
        cursor = payload_end + 1
    return payloads


def write_json(relative: str, payload: Any) -> None:
    path = REPO / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def privacy_patterns() -> list[tuple[str, re.Pattern[str]]]:
    return [
        ("credential_assignment", re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{12,}")),
        ("raw_task_identifier", re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b")),
        ("private_absolute_path", re.compile(r"(?i)(?:[A-Z]:\\\\Users\\\\|D:\\\\GHC-Archives\\\\)")),
        ("private_route_scheme", re.compile(r"(?i)(?:thread|app|plugin)://")),
        ("private_callable_or_transcript_field", re.compile(r'(?i)"(?:call_id|callable_id|conversation|session_stream|resume_token)"\s*:')),
    ]


def compute() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    paths = staged_paths()
    if not paths:
        raise RuntimeError("no staged x1 files")
    out_of_scope = [
        path
        for path in paths
        if not path.startswith(PHASE_PREFIX) and path not in ALLOWED_EXACT
    ]
    x2_names = [
        path
        for path in paths
        if any(
            token in path
            for token in (
                "evidence-receipt",
                "closeout-receipt",
                "seal-receipt",
                "final-validation-record",
                "mutation-results",
            )
        )
    ]
    status = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    unstaged = [row for row in status if row and row[1] not in {" ", "?"}]
    manifest_paths = [path for path in paths if path not in RECEIPTS]
    object_ids = staged_blob_map(paths)
    payload_by_object = batch_blob_bytes(list(object_ids.values()))
    payloads = {
        path: payload_by_object[object_ids[path]]
        for path in paths
    }
    entries = [
        {
            "path": path,
            "git_blob": object_ids[path],
            "bytes": len(payloads[path]),
            "sha256": hashlib.sha256(payloads[path]).hexdigest(),
        }
        for path in manifest_paths
    ]
    patterns = privacy_patterns()
    hits = []
    scanned = 0
    for path in paths:
        payload = payloads[path]
        if b"\x00" in payload:
            continue
        scanned += 1
        text = payload.decode("utf-8", errors="replace")
        for pattern_class, pattern in patterns:
            if pattern.search(text):
                hits.append({"path": path, "pattern_class": pattern_class})
    json_paths = [path for path in paths if path.endswith(".json")]
    json_failures = []
    for path in json_paths:
        try:
            json.loads(payloads[path].decode("utf-8"))
        except Exception as exc:  # pragma: no cover - failure receipt
            json_failures.append({"path": path, "error_type": type(exc).__name__})
    phase_truth = json.loads(payloads[f"{PHASE_PREFIX}x1-phase-truth.json"].decode("utf-8"))
    proposals = json.loads(payloads[f"{PHASE_PREFIX}preregistration/proposals.json"].decode("utf-8"))
    mutations = json.loads(payloads[f"{PHASE_PREFIX}validation/preregistered-mutation-plan.json"].decode("utf-8"))
    review = {
        "schema": "ghc.family.v653-v1.x1-staged-review.v1",
        "valid": not out_of_scope and not x2_names and not unstaged and not hits and not json_failures,
        "staged_path_count": len(paths),
        "staged_name_sha256": hashlib.sha256("\n".join(paths).encode("utf-8")).hexdigest(),
        "out_of_scope_paths": out_of_scope,
        "x2_or_outcome_paths": x2_names,
        "unstaged_rows": unstaged,
        "proposal_count": proposals["proposal_count"],
        "mutation_plan_count": mutations["mutation_count"],
        "mutation_executed_count": mutations["executed_count"],
        "x2_outcomes_present": phase_truth["x2_outcomes_present"],
        "json_parse_count": len(json_paths),
        "json_failures": json_failures,
        "diff_hygiene_required_separately": True,
        "boundary": "Exact staged x1-only surface. No x2 execution or outcome is credited.",
    }
    manifest = {
        "schema": "ghc.family.v653-v1.x1-staged-manifest.v1",
        "hash_domain": "exact Git index",
        "entry_count": len(entries),
        "entries": entries,
        "lifecycle_self_exclusions": sorted(RECEIPTS),
        "boundary": "The three lifecycle receipts are excluded from their own manifest to avoid recursive hashes.",
    }
    privacy = {
        "schema": "ghc.family.v653-v1.x1-staged-privacy.v1",
        "pattern_class_count": len(patterns),
        "pattern_classes": [name for name, _pattern in patterns],
        "scanned_text_file_count": scanned,
        "confirmed_hit_count": len(hits),
        "confirmed_hits": hits,
        "boundary": "Concrete public-payload patterns only; prohibition prose is not itself a privacy hit.",
    }
    return manifest, privacy, review


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    manifest, privacy, review = compute()
    if args.write:
        write_json(f"{PHASE_PREFIX}validation/x1-staged-manifest.json", manifest)
        write_json(f"{PHASE_PREFIX}validation/x1-staged-privacy.json", privacy)
        write_json(f"{PHASE_PREFIX}validation/x1-staged-review.json", review)
    else:
        expected = {
            "manifest": json.loads((PHASE / "validation/x1-staged-manifest.json").read_text(encoding="utf-8")),
            "privacy": json.loads((PHASE / "validation/x1-staged-privacy.json").read_text(encoding="utf-8")),
            "review": json.loads((PHASE / "validation/x1-staged-review.json").read_text(encoding="utf-8")),
        }
        if expected != {"manifest": manifest, "privacy": privacy, "review": review}:
            raise RuntimeError("staged x1 receipts are stale")
    if not review["valid"] or privacy["confirmed_hit_count"] or review["mutation_executed_count"]:
        raise RuntimeError("x1 staged validation failed")
    print(
        json.dumps(
            {
                "valid": True,
                "staged_paths": review["staged_path_count"],
                "manifest_entries": manifest["entry_count"],
                "json_parses": review["json_parse_count"],
                "privacy_files": privacy["scanned_text_file_count"],
                "privacy_hits": privacy["confirmed_hit_count"],
                "x2": False,
            }
        )
    )


if __name__ == "__main__":
    main()
