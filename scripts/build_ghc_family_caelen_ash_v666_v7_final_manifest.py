#!/usr/bin/env python3
"""Build Caelen Ash v666-v7 final staged review and exact index manifests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
from datetime import datetime, timezone
from typing import Any, BinaryIO

from ghc_family_caelen_ash_v666_v7_runtime import PHASE_ROOT, PRIVACY_PATTERNS, ROOT, replay_manifest


SOURCE_SHA = "6226988b17b7d3a2399cf6d803aceb31b03fb99f"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
SELF_PATH = "scripts/build_ghc_family_caelen_ash_v666_v7_final_manifest.py"
REVIEW_PATH = "docs/caelen-ash/v666-v7/validation/final-staged-review.json"
DELTA_PATH = "docs/caelen-ash/v666-v7/validation/final-delta-manifest.json"
OWNER_PATH = "docs/caelen-ash/v666-v7/validation/final-owner-manifest.json"


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def load(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], stderr=subprocess.STDOUT
    ).decode("utf-8", errors="strict").strip()


def staged_rows() -> list[tuple[str, str]]:
    raw = git("diff", "--cached", "--name-status", "--no-renames")
    return [
        (line.split("\t", 1)[0], line.split("\t", 1)[1].replace("\\", "/"))
        for line in raw.splitlines()
        if line
    ]


def index_metadata() -> dict[str, tuple[str, str]]:
    raw = subprocess.check_output(
        [
            "git", "-C", str(ROOT), "ls-files", "--stage", "-z", "--",
            "docs/caelen-ash/v666-v7",
            "scripts/*caelen_ash_v666_v7*.py",
            "tests/*caelen_ash_v666_v7*.py",
        ]
    )
    result: dict[str, tuple[str, str]] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, raw_path = record.split(b"\t", 1)
        mode, oid, stage = meta.decode("ascii").split()
        path = raw_path.decode("utf-8").replace("\\", "/")
        if stage != "0":
            raise RuntimeError(f"unexpected index stage for {path}")
        result[path] = (mode, oid)
    return result


def read_exact(stream: BinaryIO, length: int) -> bytes:
    chunks: list[bytes] = []
    remaining = length
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise RuntimeError(f"short git batch read: {remaining} bytes remain")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def batch_index_blobs(paths: list[str], metadata: dict[str, tuple[str, str]]) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    process = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        if process.stdin is None or process.stdout is None:
            raise RuntimeError("git batch pipes unavailable")
        for path in paths:
            oid = metadata[path][1]
            process.stdin.write((oid + "\n").encode("ascii"))
            process.stdin.flush()
            header = process.stdout.readline().decode("ascii").strip().split()
            if len(header) != 3 or header[0] != oid or header[1] != "blob":
                raise RuntimeError(f"unexpected git batch header for {path}")
            blob = read_exact(process.stdout, int(header[2]))
            if read_exact(process.stdout, 1) != b"\n":
                raise RuntimeError(f"missing git batch terminator for {path}")
            result[path] = blob
    finally:
        if process.stdin is not None:
            process.stdin.close()
        return_code = process.wait(timeout=30)
        stderr = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
        if process.stdout is not None:
            process.stdout.close()
        if process.stderr is not None:
            process.stderr.close()
        if return_code:
            raise RuntimeError(stderr[:300])
    return result


def entries(paths: list[str], metadata: dict[str, tuple[str, str]], blobs: dict[str, bytes]) -> list[dict[str, Any]]:
    return [
        {
            "path": path,
            "git_mode": metadata[path][0],
            "git_blob_oid": metadata[path][1],
            "sha256": hashlib.sha256(blobs[path]).hexdigest(),
            "size_bytes": len(blobs[path]),
        }
        for path in paths
    ]


def main() -> None:
    evidence_sha = git("rev-parse", "HEAD")
    base_rows = [(s, p) for s, p in staged_rows() if p not in {REVIEW_PATH, DELTA_PATH, OWNER_PATH}]
    if not base_rows:
        raise RuntimeError("no staged final delta")
    base_paths = [path for _, path in base_rows]
    allowed = all(path.startswith("docs/caelen-ash/v666-v7/") or path == SELF_PATH for path in base_paths)
    metadata = index_metadata()
    blobs = batch_index_blobs(base_paths, metadata)
    parsed_json = 0
    candidates = []
    maximum_words = 0
    maximum_path = ""
    for path in base_paths:
        text = blobs[path].decode("utf-8")
        if "\r" in text:
            raise RuntimeError(f"non-LF staged text: {path}")
        words = len(re.findall(r"\S+", text))
        if words > maximum_words:
            maximum_words, maximum_path = words, path
        if path.endswith(".json"):
            json.loads(text)
            parsed_json += 1
        for class_name, pattern in PRIVACY_PATTERNS.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": class_name})
    checks = {
        "additive_only": all(status == "A" for status, _ in base_rows),
        "owner_allowlist": allowed,
        "document_word_cap": maximum_words <= 100000,
        "privacy_zero_confirmed_hits": not candidates,
        "evidence_manifest_replay": replay_manifest(PHASE_ROOT / "validation" / "evidence-content-manifest.json", evidence_sha)["valid"],
        "phase_truth_exact": load("closeout/phase-truth.json")["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "route_prepared_not_sent": load("handoffs/terminal-route-state.json")["prepared"] and not load("handoffs/terminal-route-state.json")["sent"],
        "terminal_verdict": load("closeout/phase-truth.json")["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
    }
    review = {
        "schema": "ghc.family.caelen-ash.v666-v7.final-staged-review.v1",
        "generated_at_utc": NOW,
        "reviewed_from": "exact_git_index_blobs",
        "reviewed_paths": base_paths,
        "reviewed_path_count": len(base_paths),
        "json_parsed": parsed_json,
        "maximum_document_words": maximum_words,
        "maximum_document_path": maximum_path,
        "privacy_scan_classes": list(PRIVACY_PATTERNS),
        "privacy_candidates": candidates,
        "privacy_confirmed_hits": len(candidates),
        "checks": checks,
        "self_exclusions": [REVIEW_PATH, DELTA_PATH, OWNER_PATH],
        "valid": all(checks.values()),
    }
    if not review["valid"]:
        raise RuntimeError(json.dumps(review, ensure_ascii=False, sort_keys=True))
    write_json("validation/final-staged-review.json", review)
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", REVIEW_PATH])

    delta_paths = [path for _, path in staged_rows() if path not in {DELTA_PATH, OWNER_PATH}]
    metadata = index_metadata()
    delta_blobs = batch_index_blobs(delta_paths, metadata)
    delta_entries = entries(delta_paths, metadata, delta_blobs)
    write_json(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.content-manifest.v1",
            "owner": "Caelen Ash",
            "phase": "final_delta",
            "generated_at_utc": NOW,
            "source_sha": evidence_sha,
            "hash_source": "exact_git_index_blobs",
            "entries": delta_entries,
            "entry_count": len(delta_entries),
            "deletion_count": 0,
            "additive_only": all(status == "A" for status, _ in base_rows),
            "self_exclusions": [DELTA_PATH, OWNER_PATH],
        },
    )
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", DELTA_PATH])

    metadata = index_metadata()
    owner_paths_index = sorted(path for path in metadata if path != OWNER_PATH)
    owner_blobs = batch_index_blobs(owner_paths_index, metadata)
    owner_entries = entries(owner_paths_index, metadata, owner_blobs)
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.owner-manifest.v1",
            "owner": "Caelen Ash",
            "phase": "v666-v7-final",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "expected_final_parent": evidence_sha,
            "hash_source": "exact_git_index_blobs_for_resulting_final_tree",
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "file_ceiling": 2000,
            "within_file_ceiling": len(owner_entries) + 1 < 2000,
            "self_exclusion": OWNER_PATH,
        },
    )
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", OWNER_PATH])
    print(json.dumps({"reviewed": len(base_paths), "delta_entries": len(delta_entries), "owner_entries": len(owner_entries), "valid": True}, sort_keys=True))


if __name__ == "__main__":
    main()
