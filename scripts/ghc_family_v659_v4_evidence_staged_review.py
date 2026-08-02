#!/usr/bin/env python3
"""Review the exact staged Caelen Ash v659-v4 x2 evidence surface."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/caelen-ash/v659-v4/"
X1 = "8f1d7f05d3e79ede4b6579a68f1e0d901eba8669"
RECEIPT = PHASE_PREFIX + "validation/x2-evidence-staged-review.json"
MANIFEST = PHASE_PREFIX + "validation/x2-content-manifest.json"
SCANNER_FILE = "scripts/ghc_family_v659_v4_evidence_staged_review.py"


def git(*args: str, text: bool = True) -> str | bytes:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True,
        text=text, encoding="utf-8" if text else None,
    )
    return result.stdout.strip() if text else result.stdout


def index_oids() -> dict[str, str]:
    rows: dict[str, str] = {}
    raw = bytes(git("ls-files", "--stage", "-z", text=False))
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        _mode, oid, stage = metadata.decode("ascii").split()
        if stage == "0":
            rows[raw_path.decode("utf-8")] = oid
    return rows


def batch_blobs(paths: list[str], oid_map: dict[str, str]) -> dict[str, bytes]:
    missing = [path for path in paths if path not in oid_map]
    if missing:
        raise RuntimeError(f"index blob missing for {len(missing)} declared paths")
    request = "".join(f"{oid_map[path]}\n" for path in paths).encode("ascii")
    result = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=ROOT, check=True,
        input=request, capture_output=True,
    )
    output = result.stdout
    offset = 0
    blobs: dict[str, bytes] = {}
    for path in paths:
        header_end = output.index(b"\n", offset)
        header = output[offset:header_end].decode("ascii").split()
        if len(header) != 3 or header[1] != "blob":
            raise RuntimeError(f"unexpected indexed object type for {path}")
        size = int(header[2])
        start = header_end + 1
        blobs[path] = output[start : start + size]
        offset = start + size + 1
    return blobs


def main() -> None:
    staged = [line for line in str(git("diff", "--cached", "--name-only", "--diff-filter=ACMR")).splitlines() if line]
    statuses = [line.split("\t", 1) for line in str(git("diff", "--cached", "--name-status")).splitlines() if line]
    x1_paths = set(str(git("ls-tree", "-r", "--name-only", X1)).splitlines())
    oid_map = index_oids()
    manifest_blob = batch_blobs([MANIFEST], oid_map)[MANIFEST]
    manifest = json.loads(manifest_blob.decode("utf-8"))
    entries = {row["path"]: row for row in manifest["entries"]}
    exclusions = {PHASE_PREFIX + path for path in manifest["exclusions"]}
    needed = sorted(set(entries) | set(staged))
    blobs = batch_blobs(needed, oid_map)

    issues: list[str] = []
    expected_staged = sorted((set(entries) | exclusions) - x1_paths)
    if staged != expected_staged:
        issues.append("staged_allowlist")
    x1_overlap = sorted(set(staged) & x1_paths)
    if x1_overlap:
        issues.append("x1_overlap")
    non_additions = [{"status": status, "path": path} for status, path in statuses if status != "A"]
    if non_additions:
        issues.append("non_addition_set")
    if any(any(part in {"closeout", "seal", "final"} for part in Path(path).parts) for path in staged):
        issues.append("premature_lifecycle_path")

    manifest_mismatches: list[dict[str, str]] = []
    for path, row in entries.items():
        payload = blobs[path].replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if hashlib.sha256(payload).hexdigest() != row["sha256"] or len(payload) != row["bytes"]:
            manifest_mismatches.append({"path": path, "issue": "digest_or_length"})
    if manifest_mismatches:
        issues.append("manifest_mismatch")

    json_errors: list[dict[str, str]] = []
    json_count = 0
    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "credential_or_private_key": re.compile(r"(?<![A-Za-z0-9])(?:sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"),
        "delegation_markup": re.compile(r"<(?:codex_delegation|source_thread_id)>", re.I),
        "private_route_identifier": re.compile(r"(?:resume_token|private_callable|codex_(?:thread|task|agent)_id)\s*[:=]", re.I),
    }
    candidates: list[dict[str, str]] = []
    for path in staged:
        if path == RECEIPT:
            continue
        payload = blobs[path]
        if path.endswith(".json"):
            json_count += 1
            try:
                json.loads(payload.decode("utf-8"))
            except Exception as exc:  # pragma: no cover
                json_errors.append({"path": path, "error": type(exc).__name__})
        text = payload.decode("utf-8", errors="replace")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": label})
    confirmed = [row for row in candidates if row["path"] != SCANNER_FILE]
    if json_errors:
        issues.append("json_parse")
    if confirmed:
        issues.append("confirmed_privacy_hit")

    valid = not issues
    receipt = {
        "schema": "ghc.family.v659-v4.x2-evidence-staged-review.v1",
        "lifecycle": "x2_evidence_precommit",
        "x1_commit": X1,
        "staged_path_count": len(staged),
        "expected_staged_path_count": len(expected_staged),
        "allowlist_exact": staged == expected_staged,
        "reviewed_content_count": len(staged) - 1,
        "receipt_self_exclusion": RECEIPT,
        "manifest_entry_count": len(entries),
        "manifest_self_exclusion_count": len(exclusions),
        "manifest_mismatches": manifest_mismatches,
        "x1_overlap": x1_overlap,
        "non_additions": non_additions,
        "json_parse_count": json_count,
        "json_errors": json_errors,
        "privacy_classes": list(patterns),
        "privacy_candidates": candidates,
        "privacy_confirmed_hits": confirmed,
        "issues": issues,
        "valid": valid,
        "boundary": "Exact x2 Git-index evidence only; not final-head, privacy-complete, exhaustive-security, independent-reproduction, production, professional, legal, cultural, Māori-authority, Theory-of-Everything, or Stage 20 credit.",
    }
    target = ROOT / RECEIPT
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": valid, "staged": len(staged), "reviewed": len(staged) - 1, "json": json_count, "manifest": len(entries), "privacy_hits": len(confirmed)}, sort_keys=True))
    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
