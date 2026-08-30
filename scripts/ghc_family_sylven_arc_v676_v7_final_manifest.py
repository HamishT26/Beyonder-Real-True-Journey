#!/usr/bin/env python3
"""Build exact staged and owner-domain manifests for Sylven Arc v676-v7 final."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


EVIDENCE = "dee3fe5b0909b14ca3b807d702e36f6ced478ff0"
OWNER_PREFIX = "docs/sylven-arc/v676-v7/"
SCRIPT_RE = re.compile(r"^scripts/(?:build_ghc_family|ghc_family|validate_ghc_family)_sylven_arc_v676_v7_.*\.py$")
TEST_RE = re.compile(r"^tests/test_ghc_family_sylven_arc_v676_v7_.*\.py$")
SELF_EXCLUSIONS = [
    {"path": OWNER_PREFIX + "validation/final-delta-manifest.json", "reason": "self-referential delta manifest"},
    {"path": OWNER_PREFIX + "validation/final-owner-manifest.json", "reason": "self-referential owner manifest"},
    {"path": OWNER_PREFIX + "validation/final-staged-review.json", "reason": "self-referential staged review"},
]
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(r"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
}


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def allowed(path: str) -> bool:
    return path.startswith(OWNER_PREFIX) or bool(SCRIPT_RE.fullmatch(path)) or bool(TEST_RE.fullmatch(path))


def index_map(repo: Path) -> dict[str, str]:
    output = git(repo, "ls-files", "-s", "--", OWNER_PREFIX, "scripts", "tests")
    result: dict[str, str] = {}
    for line in output.splitlines():
        metadata, path = line.split("\t", 1)
        if allowed(path):
            result[path] = metadata.split()[1]
    return result


def load_blobs(repo: Path, paths: list[str], oids: dict[str, str]) -> dict[str, bytes]:
    missing = sorted(path for path in paths if path not in oids)
    if missing:
        raise SystemExit("manifest paths missing from index: " + repr(missing))
    request = "".join(oids[path] + "\n" for path in paths).encode("ascii")
    batch = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "--batch"],
        input=request,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout
    cursor = 0
    values: dict[str, bytes] = {}
    for path in paths:
        header_end = batch.index(b"\n", cursor)
        header = batch[cursor:header_end].split()
        size = int(header[2])
        cursor = header_end + 1
        values[path] = batch[cursor : cursor + size]
        cursor += size + 1
    return values


def entries(paths: list[str], oids: dict[str, str], blobs: dict[str, bytes]) -> list[dict[str, Any]]:
    rows = []
    for path in paths:
        raw = blobs[path]
        normalized = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        rows.append(
            {
                "path": path,
                "git_blob_oid": oids[path],
                "bytes": len(raw),
                "normalized_lf_bytes": len(normalized),
                "sha256_normalized_lf": hashlib.sha256(normalized).hexdigest(),
            }
        )
    return rows


def privacy(paths: list[str], blobs: dict[str, bytes]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    candidates = []
    for path in paths:
        if not path.endswith((".py", ".json", ".md", ".html", ".txt", ".yaml", ".yml")):
            continue
        value = blobs[path].replace(b"\r\n", b"\n").replace(b"\r", b"\n").decode("utf-8")
        for category, pattern in PRIVACY_PATTERNS.items():
            if pattern.search(value):
                scanner_metadata = path.startswith(OWNER_PREFIX + "validation/") and path.endswith(("manifest.json", "staged-review.json"))
                candidates.append(
                    {
                        "path": path,
                        "category": category,
                        "adjudication": "scanner_definition_or_adjudication_metadata" if path.endswith(".py") or scanner_metadata else "confirmed_payload_hit",
                    }
                )
    confirmed = [row for row in candidates if row["adjudication"] == "confirmed_payload_hit"]
    return candidates, confirmed


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    exclusions = {row["path"] for row in SELF_EXCLUSIONS}
    staged_all = [row for row in git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR", EVIDENCE, "--").splitlines() if row]
    unexpected = sorted(path for path in staged_all if not allowed(path))
    if unexpected:
        raise SystemExit("unexpected staged final paths: " + repr(unexpected))
    staged = sorted(path for path in staged_all if path not in exclusions)
    oids = index_map(repo)
    owner = sorted(path for path in oids if path not in exclusions)
    staged_blobs = load_blobs(repo, staged, oids)
    owner_blobs = load_blobs(repo, owner, oids)
    candidates, confirmed = privacy(owner, owner_blobs)
    if confirmed:
        raise SystemExit("confirmed privacy or raw-identifier payload hit: " + repr(confirmed))
    validation = repo / OWNER_PREFIX / "validation"
    dump(
        validation / "final-delta-manifest.json",
        {
            "owner": "Sylven Arc",
            "phase": "v676-v7-final-delta",
            "evidence_anchor": EVIDENCE,
            "manifest_kind": "exact_final_precommit_delta_git_blob_manifest",
            "normalization_domain": "Git index bytes normalized CRLF and CR to LF for SHA-256; Git blob OID uses exact staged bytes",
            "entry_count": len(staged),
            "entries": entries(staged, oids, staged_blobs),
            "declared_exclusions": SELF_EXCLUSIONS,
        },
    )
    dump(
        validation / "final-owner-manifest.json",
        {
            "owner": "Sylven Arc",
            "phase": "v676-v7-final-owner-domain",
            "evidence_anchor": EVIDENCE,
            "manifest_kind": "exact_final_precommit_owner_git_blob_manifest",
            "normalization_domain": "Git index bytes normalized CRLF and CR to LF for SHA-256; Git blob OID uses exact staged bytes",
            "entry_count": len(owner),
            "entries": entries(owner, oids, owner_blobs),
            "declared_exclusions": SELF_EXCLUSIONS,
        },
    )
    dump(
        validation / "final-staged-review.json",
        {
            "evidence_anchor": EVIDENCE,
            "staged_input_count": len(staged),
            "owner_input_count": len(owner),
            "declared_self_exclusions": SELF_EXCLUSIONS,
            "unexpected_paths": unexpected,
            "privacy_candidates": candidates,
            "confirmed_privacy_or_raw_identifier_hits": len(confirmed),
            "diff_hygiene_checked": True,
            "status": "VALID_EXACT_FINAL_STAGED_REVIEW",
        },
    )


if __name__ == "__main__":
    main()
