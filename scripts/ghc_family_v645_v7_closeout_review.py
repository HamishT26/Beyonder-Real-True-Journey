#!/usr/bin/env python3
"""Review closeout staged blobs and full owner-manifest parity."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREFIX = "docs/tamar-vey/v645-v7/"
SELF = {
    f"{PREFIX}validation/closeout-staged-manifest.json",
    f"{PREFIX}validation/closeout-staged-review.json",
}
ALLOWED_MODIFIED = {"scripts/build_ghc_family_v645_v7_closeout.py"}
PATTERNS = {
    "raw_uuid_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_route_or_callable": re.compile("(?:source_" + "thread_id|client" + "ThreadId|app" + "://|codex" + "://|private_" + "callable_id)", re.I),
    "credential_or_secret_material": re.compile("(?:BEGIN (?:RSA |EC |OPENSSH )?PRIVATE " + "KEY|api[_-]?" + "key\\s*[:=]|authorization:\\s*bearer\\s+[A-Za-z0-9._~-]{12,})", re.I),
    "private_absolute_local_path": re.compile("(?:[A-Za-z]:\\\\" + "Users\\\\[^\\\\\\s]+\\\\|D:\\\\GHC-" + "Archives\\\\)", re.I),
    "private_session_artifact": re.compile("(?:session[_ -]?" + "stream[_ -]?(?:path|id)|transcript[_ -]?(?:path|id)|screenshot[_ -]?(?:path|id))", re.I),
}


def command(*args: str, binary: bool = False):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=not binary, encoding=None if binary else "utf-8")


def staged_blob(path: str) -> bytes:
    return command("show", f":{path}", binary=True)


def committed_or_staged_blob(path: str) -> bytes:
    try:
        return staged_blob(path)
    except subprocess.CalledProcessError:
        return command("show", f"HEAD:{path}", binary=True)


def write(relative: str, payload: dict) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    status_rows = [row.split("\t", 1) for row in command("diff", "--cached", "--name-status", "--diff-filter=ACMR").splitlines() if row]
    names = [path for _, path in status_rows]
    owner = sorted(path for path in names if path.startswith(PREFIX) or re.fullmatch(r"(?:scripts|tests)/[^/]*v645_v7[^/]*\.py", path))
    entries = []
    confirmed = []
    json_failures = []
    for path in owner:
        if path in SELF:
            continue
        data = staged_blob(path)
        entries.append({"path": path, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            confirmed.append({"path": path, "pattern_class": "invalid_utf8"})
            continue
        if path.endswith(".json"):
            try:
                json.loads(text)
            except json.JSONDecodeError:
                json_failures.append(path)
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                confirmed.append({"path": path, "pattern_class": label})
    unexpected = sorted(set(names) - set(owner))
    disallowed_modified = sorted(path for status, path in status_rows if status != "A" and path not in ALLOWED_MODIFIED)
    exact = json.loads((ROOT / f"{PREFIX}validation/exact-owner-manifest.json").read_text(encoding="utf-8"))
    mismatches = []
    for row in exact["entries"]:
        data = committed_or_staged_blob(row["path"])
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            mismatches.append(row["path"])
    manifest = {"schema": "ghc.family.v645-v7.closeout-staged-manifest.v1", "domain": "exact staged closeout Git blobs", "entry_count": len(entries), "entries": entries, "self_excluded": sorted(SELF), "valid": True}
    review = {
        "schema": "ghc.family.v645-v7.closeout-staged-review.v1",
        "staged_file_count": len(names),
        "owner_staged_file_count": len(owner),
        "manifest_entry_count": len(entries),
        "unexpected_paths": unexpected,
        "allowed_modified_closeout_tools": sorted(ALLOWED_MODIFIED & set(names)),
        "disallowed_modified_paths": disallowed_modified,
        "json_failures": json_failures,
        "privacy_pattern_class_count": len(PATTERNS),
        "privacy_confirmed_hit_count": len(confirmed),
        "privacy_confirmed_hits": confirmed,
        "exact_owner_manifest_entry_count": exact["entry_count"],
        "exact_owner_manifest_mismatches": mismatches,
        "valid": not unexpected and not disallowed_modified and not json_failures and not confirmed and not mismatches,
        "boundary": "Exact staged and manifest parity checks do not establish privacy, security, or independent-reproduction completeness.",
    }
    write(f"{PREFIX}validation/closeout-staged-manifest.json", manifest)
    write(f"{PREFIX}validation/closeout-staged-review.json", review)
    print(json.dumps({"staged": len(names), "entries": len(entries), "full_manifest": exact["entry_count"], "mismatches": len(mismatches), "privacy": len(confirmed), "valid": review["valid"]}, ensure_ascii=False))
    return 0 if review["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
