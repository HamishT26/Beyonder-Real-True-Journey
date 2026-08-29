#!/usr/bin/env python3
"""Build exact normalized-LF Git-blob manifests for Elowen v676-v6 correction1."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "56b4e82909b3d7197b817a2415da592f8fc7df6e"
ORIGINAL_FINAL = "b37d777b2800372003451d95d3ad5b854ff77d7b"
OWNER_PREFIX = "docs/elowen-cairn/v676-v6/"
DELTA_PATH = OWNER_PREFIX + "validation/correction1-delta-manifest.json"
OWNER_PATH = OWNER_PREFIX + "validation/correction1-owner-manifest.json"
REVIEW_PATH = OWNER_PREFIX + "validation/correction1-staged-review.json"
SELF_EXCLUSIONS = [
    {"path": DELTA_PATH, "reason": "self-referential correction delta manifest"},
    {"path": OWNER_PATH, "reason": "self-referential correction owner manifest"},
    {"path": REVIEW_PATH, "reason": "self-referential correction staged review"},
]
SCRIPT_RE = re.compile(r"^scripts/(?:build_ghc_family|ghc_family|validate_ghc_family)_elowen_cairn_v676_v6_.*\.py$")
TEST_RE = re.compile(r"^tests/test_ghc_family_elowen_cairn_v676_v6_.*\.py$")
PRIVACY = {
    "private_absolute_path": re.compile(rb"(?i)[A-Z]:[\\/]+(?:Users|GHC-Archives)[\\/]+"),
    "raw_task_route": re.compile(rb"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(rb"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(rb"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def allowed(path: str) -> bool:
    return path.startswith(OWNER_PREFIX) or bool(SCRIPT_RE.fullmatch(path)) or bool(TEST_RE.fullmatch(path))


def normalized(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def index_map() -> dict[str, str]:
    result: dict[str, str] = {}
    for line in git("ls-files", "-s").splitlines():
        if line:
            left, path = line.split("\t", 1)
            _mode, oid, stage = left.split()
            if stage == "0":
                result[path] = oid
    return result


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    payload = b"".join(oid.encode("ascii") + b"\n" for oid in oids)
    proc = subprocess.run(["git", "cat-file", "--batch"], cwd=ROOT, input=payload, capture_output=True, check=True, timeout=300)
    stream = proc.stdout
    offset = 0
    result: dict[str, bytes] = {}
    for oid in oids:
        end = stream.find(b"\n", offset)
        if end < 0:
            raise RuntimeError("truncated batch header")
        header = stream[offset:end].split()
        offset = end + 1
        size = int(header[2])
        result[oid] = stream[offset : offset + size]
        offset += size + 1
    return result


def entry(path: str, oid: str, blobs: dict[str, bytes]) -> dict[str, Any]:
    raw = blobs[oid]
    norm = normalized(raw)
    return {"path": path, "git_blob_oid": oid, "bytes": len(raw), "normalized_lf_bytes": len(norm), "sha256_normalized_lf": hashlib.sha256(norm).hexdigest()}


def main() -> None:
    if git("rev-parse", "HEAD") != ORIGINAL_FINAL:
        raise SystemExit("correction manifests require the immutable original final as HEAD")
    staged = sorted(path for path in git("diff", "--cached", "--name-only", "--diff-filter=ACMR", ORIGINAL_FINAL, "--").splitlines() if path)
    exclusions = {row["path"] for row in SELF_EXCLUSIONS}
    inputs = sorted(path for path in staged if path not in exclusions)
    unexpected = sorted(path for path in staged if not allowed(path))
    if unexpected:
        raise SystemExit(f"unexpected staged correction paths: {unexpected!r}")
    required = {
        OWNER_PREFIX + "correction1/phase-truth.json",
        OWNER_PREFIX + "correction1/method-flow-overlay.json",
        "scripts/validate_ghc_family_elowen_cairn_v676_v6_final.py",
        "scripts/build_ghc_family_elowen_cairn_v676_v6_correction1.py",
        "tests/test_ghc_family_elowen_cairn_v676_v6_correction1.py",
    }
    if not required.issubset(inputs):
        raise SystemExit(f"missing correction inputs: {sorted(required - set(inputs))!r}")
    committed_owner = {path for path in git("diff", "--name-only", "--diff-filter=ACMR", SOURCE, ORIGINAL_FINAL, "--").splitlines() if path and allowed(path)}
    owner_paths = sorted((committed_owner | set(staged)) - exclusions)
    index = index_map()
    missing = sorted(path for path in owner_paths if path not in index)
    if missing:
        raise SystemExit(f"owner paths missing from index: {missing[:10]!r}")
    oids = list(dict.fromkeys(index[path] for path in owner_paths))
    blobs = batch_blobs(oids)
    delta_entries = [entry(path, index[path], blobs) for path in inputs]
    owner_entries = [entry(path, index[path], blobs) for path in owner_paths]
    candidates = []
    for path in owner_paths:
        if not path.endswith((".py", ".json", ".md", ".html", ".txt", ".yaml", ".yml")):
            continue
        raw = normalized(blobs[index[path]])
        for category, pattern in PRIVACY.items():
            if pattern.search(raw):
                scanner = path.endswith(".py") or path.endswith("-staged-review.json") or path.endswith("privacy-adjudication.json")
                candidates.append({"path": path, "category": category, "adjudication": "scanner_definition_or_adjudication_metadata" if scanner else "confirmed_payload_hit"})
    confirmed = [row for row in candidates if row["adjudication"] == "confirmed_payload_hit"]
    if confirmed:
        raise SystemExit(f"confirmed privacy hits: {confirmed!r}")
    validation = ROOT / OWNER_PREFIX / "validation"
    common = {"owner": "Elowen Cairn", "phase": "v676-v6-correction1", "source": SOURCE, "original_final": ORIGINAL_FINAL, "normalization_domain": "Git index bytes normalized CRLF and CR to LF for SHA-256; Git blob OID uses exact index bytes", "declared_exclusions": SELF_EXCLUSIONS}
    dump(validation / "correction1-delta-manifest.json", {**common, "manifest_kind": "precommit_correction_delta_git_blob_manifest", "range_start": ORIGINAL_FINAL, "entry_count": len(delta_entries), "entries": delta_entries})
    dump(validation / "correction1-owner-manifest.json", {**common, "manifest_kind": "precommit_source_to_corrected_final_owner_git_blob_manifest", "range_start": SOURCE, "entry_count": len(owner_entries), "entries": owner_entries})
    dump(validation / "correction1-staged-review.json", {"owner": "Elowen Cairn", "phase": "v676-v6-correction1", "staged_input_count": len(inputs), "owner_input_count": len(owner_paths), "declared_self_exclusions": SELF_EXCLUSIONS, "unexpected_paths": unexpected, "privacy_classes": sorted(PRIVACY), "privacy_candidates": candidates, "privacy_candidate_count": len(candidates), "confirmed_five_class_privacy_or_raw_identifier_hits": 0, "exact_staged_review": True, "status": "VALID_PRECOMMIT_CORRECTION1_STAGED_REVIEW"})


if __name__ == "__main__":
    main()
