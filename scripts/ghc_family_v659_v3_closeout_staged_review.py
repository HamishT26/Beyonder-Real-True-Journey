#!/usr/bin/env python3
"""Review the exact staged Sable Rook v659-v3 closeout surface."""

from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/sable-rook/v659-v3/"
EVIDENCE = "04d167b799ba8b9de885e66ff8ee480bf5b219b2"
BASE_FINAL = "91d0ee0d7c4f37dbaa13f07d191f8af4b2464f73"
RECEIPT = PHASE_PREFIX + "validation/closeout-staged-review.json"
DELTA_MANIFEST = PHASE_PREFIX + "validation/final-delta-manifest.json"
OWNER_MANIFEST = PHASE_PREFIX + "final/final-owner-manifest.json"
SCANNER_DEFINITIONS = {
    "scripts/build_ghc_family_v659_v3_closeout.py",
    "scripts/ghc_family_v659_v3_closeout_staged_review.py",
    "scripts/ghc_family_v659_v3_final_validator.py",
}


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
    stream = io.BytesIO(result.stdout)
    blobs: dict[str, bytes] = {}
    for path in paths:
        header = stream.readline().decode("ascii").strip().split()
        if len(header) != 3 or header[1] != "blob":
            raise RuntimeError(f"unexpected indexed object type for {path}")
        size = int(header[2])
        blobs[path] = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError("invalid cat-file framing")
    if stream.read():
        raise RuntimeError("unexpected trailing batch data")
    return blobs


def normalized(payload: bytes) -> bytes:
    return payload.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def main() -> int:
    staged = [row for row in str(git("diff", "--cached", "--name-only")).splitlines() if row]
    statuses = [row.split("\t", 1) for row in str(git("diff", "--cached", "--name-status")).splitlines() if row]
    evidence_delta = {row for row in str(git("diff", "--name-only", EVIDENCE)).splitlines() if row}
    correction_delta = {row for row in str(git("diff", "--name-only", BASE_FINAL)).splitlines() if row}
    oid_map = index_oids()
    seeds = batch_blobs([DELTA_MANIFEST, OWNER_MANIFEST], oid_map)
    delta = json.loads(seeds[DELTA_MANIFEST].decode("utf-8"))
    owner = json.loads(seeds[OWNER_MANIFEST].decode("utf-8"))
    delta_entries = {row["path"]: row for row in delta["entries"]}
    delta_exclusions = set(delta["self_exclusions"])
    owner_entries = {row["path"]: row for row in owner["entries"]}
    owner_exclusions = set(owner["self_exclusions"])
    needed = sorted(set(staged) | set(delta_entries) | set(owner_entries))
    blobs = batch_blobs(needed, oid_map)

    issues: list[str] = []
    declared_final_surface = set(delta_entries) | delta_exclusions
    if evidence_delta != declared_final_surface:
        issues.append("delta_coverage")
    if correction_delta != set(staged):
        issues.append("correction_delta")
    if set(staged) - declared_final_surface:
        issues.append("outside_declared_final_surface")
    if any(status not in {"A", "M"} for status, _path in statuses):
        issues.append("destructive_or_unexpected_status")
    if RECEIPT not in delta_exclusions or RECEIPT not in owner_exclusions:
        issues.append("receipt_not_self_excluded")

    mismatches: list[dict[str, str]] = []
    for label, entries in (("delta", delta_entries), ("owner", owner_entries)):
        for path, row in entries.items():
            payload = normalized(blobs[path])
            if len(payload) != row["bytes"] or hashlib.sha256(payload).hexdigest() != row["sha256"]:
                mismatches.append({"manifest": label, "path": path})
    if mismatches:
        issues.append("manifest_mismatch")

    json_errors: list[dict[str, str]] = []
    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "credential_or_private_key": re.compile(r"(?<![A-Za-z0-9])(?:sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"),
        "delegation_markup": re.compile(r"<(?:codex_delegation|source_thread_id)>", re.I),
        "private_route_identifier": re.compile(r"(?:resume_token|private_callable|codex_(?:thread|task|agent)_id)\s*[:=]", re.I),
    }
    candidates: list[dict[str, str]] = []
    json_count = 0
    for path in staged:
        if path == RECEIPT:
            continue
        payload = blobs[path]
        if path.endswith(".json"):
            json_count += 1
            try:
                json.loads(payload.decode("utf-8"))
            except Exception as exc:
                json_errors.append({"path": path, "error": type(exc).__name__})
        text = payload.decode("utf-8", errors="replace")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": label})
    confirmed = [row for row in candidates if row["path"] not in SCANNER_DEFINITIONS]
    if json_errors:
        issues.append("json_parse")
    if confirmed:
        issues.append("confirmed_privacy_hit")

    valid = not issues
    receipt = {
        "schema": "ghc.family.v659-v3.closeout-staged-review.v1",
        "lifecycle": "closeout_precommit",
        "evidence_commit": EVIDENCE,
        "correction_base": BASE_FINAL,
        "staged_path_count": len(staged),
        "reviewed_content_count": len(staged) - 1,
        "receipt_self_exclusion": RECEIPT,
        "all_owner_closeout_updates": all(status in {"A", "M"} for status, _path in statuses),
        "staged_statuses": [{"status": status, "path": path} for status, path in statuses],
        "outside_declared_final_surface": sorted(set(staged) - declared_final_surface),
        "delta_manifest_entry_count": len(delta_entries),
        "delta_manifest_exclusion_count": len(delta_exclusions),
        "owner_manifest_entry_count": len(owner_entries),
        "owner_manifest_exclusion_count": len(owner_exclusions),
        "manifest_mismatches": mismatches,
        "json_parse_count": json_count,
        "json_errors": json_errors,
        "privacy_classes": list(patterns),
        "privacy_candidates": candidates,
        "privacy_confirmed_hits": confirmed,
        "issues": issues,
        "valid": valid,
        "boundary": "Exact closeout Git-index evidence only; not final-head, privacy-complete, exhaustive-security, independent-reproduction, production, professional, legal, cultural, Māori-authority, Theory-of-Everything, or Stage 20 credit.",
    }
    target = ROOT / RECEIPT
    target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "valid": valid, "staged": len(staged), "reviewed": len(staged) - 1,
        "json": json_count, "delta": len(delta_entries), "owner": len(owner_entries),
        "privacy_hits": len(confirmed),
    }, sort_keys=True))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
