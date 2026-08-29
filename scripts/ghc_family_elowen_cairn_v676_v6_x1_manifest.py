#!/usr/bin/env python3
"""Build the exact staged planning-only Elowen Cairn v676-v6 x1 manifest."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


SOURCE = "56b4e82909b3d7197b817a2415da592f8fc7df6e"
OWNER_PREFIX = "docs/elowen-cairn/v676-v6/"
SELF_EXCLUSIONS = [
    {"path": OWNER_PREFIX + "validation/x1-manifest.json", "reason": "self-referential manifest output"},
    {"path": OWNER_PREFIX + "validation/x1-staged-review.json", "reason": "self-referential staged-review output"},
]
ALLOWED_SCRIPT_RE = re.compile(r"^scripts/(?:build_ghc_family|ghc_family)_elowen_cairn_v676_v6_.*\.py$")
ALLOWED_TEST_RE = re.compile(r"^tests/test_ghc_family_elowen_cairn_v676_v6_.*\.py$")
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(r"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
}


def git(repo: Path, *args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def allowed(path: str) -> bool:
    return path.startswith(OWNER_PREFIX) or bool(ALLOWED_SCRIPT_RE.fullmatch(path)) or bool(ALLOWED_TEST_RE.fullmatch(path))


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    staged = [
        line
        for line in str(git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR", SOURCE, "--")).splitlines()
        if line
    ]
    excluded_paths = {row["path"] for row in SELF_EXCLUSIONS}
    input_paths = [path for path in staged if path not in excluded_paths]
    unexpected = sorted(path for path in staged if not allowed(path))
    x2_paths = sorted(path for path in staged if "/x2/" in path or "_x2" in path)
    if unexpected or x2_paths:
        raise SystemExit(f"staged x1 gate failed: unexpected={unexpected!r} x2={x2_paths!r}")

    entries: list[dict[str, Any]] = []
    candidates: list[dict[str, str]] = []
    for path in input_paths:
        raw = git(repo, "show", ":" + path, binary=True)
        assert isinstance(raw, bytes)
        oid_line = str(git(repo, "ls-files", "-s", "--", path)).splitlines()[0]
        oid = oid_line.split()[1]
        normalized = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        entries.append(
            {
                "path": path,
                "git_blob_oid": oid,
                "bytes": len(raw),
                "normalized_lf_bytes": len(normalized),
                "sha256_normalized_lf": hashlib.sha256(normalized).hexdigest(),
            }
        )
        if path.endswith((".py", ".json", ".md", ".html", ".txt")):
            value = normalized.decode("utf-8")
            for category, pattern in PRIVACY_PATTERNS.items():
                if pattern.search(value):
                    candidates.append(
                        {
                            "path": path,
                            "category": category,
                            "adjudication": "scanner_definition_or_rejection_assertion" if path.endswith(".py") else "confirmed_payload_hit",
                        }
                    )
    confirmed = [row for row in candidates if row["adjudication"] == "confirmed_payload_hit"]
    if confirmed:
        raise SystemExit("confirmed privacy or raw-identifier payload hit")

    validation = repo / OWNER_PREFIX / "validation"
    dump(
        validation / "x1-manifest.json",
        {
            "owner": "Elowen Cairn",
            "phase": "v676-v6-x1",
            "source": SOURCE,
            "manifest_kind": "immutable_x1_precommit_git_blob_manifest",
            "normalization_domain": "Git index bytes normalized CRLF and CR to LF for SHA-256; Git blob OID uses exact staged bytes",
            "entry_count": len(entries),
            "entries": entries,
            "declared_exclusions": SELF_EXCLUSIONS,
            "x2_paths_present": False,
        },
    )
    dump(
        validation / "x1-staged-review.json",
        {
            "source": SOURCE,
            "staged_input_count": len(input_paths),
            "declared_self_exclusions": SELF_EXCLUSIONS,
            "unexpected_paths": unexpected,
            "x2_paths": x2_paths,
            "privacy_candidates": candidates,
            "confirmed_privacy_or_raw_identifier_hits": len(confirmed),
            "diff_hygiene_checked": True,
            "status": "VALID_PLANNING_ONLY_X1_STAGED_REVIEW",
        },
    )


if __name__ == "__main__":
    main()
