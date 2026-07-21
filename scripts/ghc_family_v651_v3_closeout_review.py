#!/usr/bin/env python3
"""Build exact staged-delta and owner-tree receipts for Tamar v651-v3 closeout."""

from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PHASE = "docs/tamar-vey/v651-v3"
EVIDENCE = "449f3a29402459a66838cbf1cc8a3b110c145162"
DELTA_MANIFEST = f"{PHASE}/validation/final-delta-manifest.json"
DELTA_PRIVACY = f"{PHASE}/validation/final-delta-privacy.json"
OWNER_MANIFEST = f"{PHASE}/validation/final-owner-manifest.json"
OWNER_PRIVACY = f"{PHASE}/validation/final-owner-privacy.json"
REVIEW = f"{PHASE}/validation/final-staged-review.json"
SELF_EXCLUSIONS = [DELTA_MANIFEST, DELTA_PRIVACY, OWNER_MANIFEST, OWNER_PRIVACY, REVIEW]

PATTERNS = {
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_local_path": re.compile(r"(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/Users/|/home/)", re.I),
    "private_uri": re.compile(r"(?:codex|chatgpt|file|vscode|app)://", re.I),
    "delegation_markup": re.compile(r"<\s*(?:codex_delegation|source_thread_id|private_route)\b", re.I),
    "credential_assignment": re.compile(r"(?:api[_-]?key|password|private[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-/+=]{12,}", re.I),
}
SCANNER_DEFINITIONS = {
    "scripts/ghc_family_v651_v3_closeout_review.py",
    "scripts/ghc_family_v651_v3_final_validate.py",
}


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=REPO, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def staged_paths() -> list[str]:
    raw = run("git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").stdout
    return sorted(item.decode("utf-8") for item in raw.split(b"\0") if item)


def index_rows() -> dict[str, tuple[str, str]]:
    raw = run("git", "ls-files", "-s", "-z").stdout
    rows: dict[str, tuple[str, str]] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        mode, oid, _stage = meta.decode("ascii").split()
        rows[path.decode("utf-8")] = (oid, mode)
    return rows


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    proc = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=REPO,
        input="".join(oid + "\n" for oid in unique).encode("ascii"),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
    )
    stream = io.BytesIO(proc.stdout)
    result: dict[str, bytes] = {}
    for expected in unique:
        header = stream.readline().rstrip(b"\n").decode("ascii").split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header: {header}")
        size = int(header[2])
        result[expected] = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError("missing cat-file terminator")
    if stream.read():
        raise RuntimeError("trailing cat-file output")
    return result


def entries(paths: list[str], rows: dict[str, tuple[str, str]], blobs: dict[str, bytes]) -> list[dict]:
    result = []
    for path in paths:
        oid, mode = rows[path]
        data = blobs[oid]
        result.append({"path": path, "mode": mode, "git_blob": oid, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return result


def scan(paths: list[str], rows: dict[str, tuple[str, str]], blobs: dict[str, bytes]) -> dict:
    candidates = []
    confirmed = []
    for path in paths:
        data = blobs[rows[path][0]]
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for class_name, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                line_number = text.count("\n", 0, match.start()) + 1
                source_line = text.splitlines()[line_number - 1].strip()
                sanitizer_assertion = (
                    path == "tests/test_ghc_family_v651_v3_closeout.py"
                    and class_name in {"private_uri", "delegation_markup"}
                    and source_line.startswith("self.assertNotIn(")
                )
                disposition = "scanner_definition" if path in SCANNER_DEFINITIONS else "sanitizer_negative_assertion" if sanitizer_assertion else "confirmed_payload"
                row = {"path": path, "class": class_name, "line": line_number, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload":
                    confirmed.append(row)
    return {"pattern_classes": list(PATTERNS), "scanned_count": len(paths), "candidate_count": len(candidates), "confirmed_hit_count": len(confirmed), "candidates": candidates, "confirmed_hits": confirmed, "complete_privacy_claim": False}


def write_json(relative: str, payload) -> None:
    path = REPO / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    head = run("git", "rev-parse", "HEAD").stdout.decode().strip()
    delta = staged_paths()
    allowed = (f"{PHASE}/", "scripts/build_ghc_family_v651_v3_", "scripts/ghc_family_v651_v3_", "tests/test_ghc_family_v651_v3_")
    forbidden = [path for path in delta if not path.startswith(allowed)]
    rows = index_rows()
    owner = sorted(path for path in rows if path.startswith(f"{PHASE}/"))
    delta_content = [path for path in delta if path not in SELF_EXCLUSIONS]
    owner_content = [path for path in owner if path not in SELF_EXCLUSIONS]
    missing = [path for path in delta_content + owner_content if path not in rows]
    if missing:
        raise RuntimeError(f"missing index paths: {missing[:5]}")
    blobs = batch_blobs([rows[path][0] for path in list(dict.fromkeys(delta_content + owner_content))])
    delta_entries = entries(delta_content, rows, blobs)
    owner_entries = entries(owner_content, rows, blobs)
    delta_scan = scan(delta_content, rows, blobs)
    owner_scan = scan(owner_content, rows, blobs)
    hygiene = run("git", "diff", "--cached", "--check", check=False)
    passed = bool(delta) and head == EVIDENCE and not forbidden and not delta_scan["confirmed_hits"] and not owner_scan["confirmed_hits"] and hygiene.returncode == 0
    write_json(DELTA_MANIFEST, {"schema": "ghc.family.v651-v3.final-delta-manifest.v1", "hash_domain": "git_index_blob", "entry_count": len(delta_entries), "entries": delta_entries, "self_exclusions": SELF_EXCLUSIONS})
    write_json(DELTA_PRIVACY, {"schema": "ghc.family.v651-v3.final-delta-privacy.v1", **delta_scan})
    write_json(OWNER_MANIFEST, {"schema": "ghc.family.v651-v3.final-owner-manifest.v1", "hash_domain": "git_index_blob", "entry_count": len(owner_entries), "entries": owner_entries, "self_exclusions": SELF_EXCLUSIONS})
    write_json(OWNER_PRIVACY, {"schema": "ghc.family.v651-v3.final-owner-privacy.v1", **owner_scan})
    write_json(REVIEW, {"schema": "ghc.family.v651-v3.final-staged-review.v1", "head_before_commit": head, "expected_parent": EVIDENCE, "staged_path_count": len(delta), "delta_manifest_entries": len(delta_entries), "owner_path_count": len(owner), "owner_manifest_entries": len(owner_entries), "self_exclusion_count": len(SELF_EXCLUSIONS), "forbidden_paths": forbidden, "delta_privacy_confirmed_hits": delta_scan["confirmed_hit_count"], "owner_privacy_confirmed_hits": owner_scan["confirmed_hit_count"], "diff_hygiene_issue_count": len(hygiene.stdout.decode("utf-8", errors="replace").splitlines()), "passed": passed})
    print(json.dumps({"staged": len(delta), "delta_entries": len(delta_entries), "owner": len(owner), "owner_entries": len(owner_entries), "confirmed_hits": delta_scan["confirmed_hit_count"] + owner_scan["confirmed_hit_count"], "passed": passed}, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
