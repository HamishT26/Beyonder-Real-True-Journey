#!/usr/bin/env python3
"""Review and manifest the exact staged Sable v655-v5 final delta."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/sable-rook/v655-v5/"
BASE = "ee10e567ce363e5a8bf710532c5a53d0a411defa"
REVIEW = PHASE_PREFIX + "validation/final-staged-review.json"
MANIFEST = PHASE_PREFIX + "validation/final-staged-manifest.json"
SELF_EXCLUSIONS = {REVIEW, MANIFEST}
ALLOWED_NONPHASE = {
    "scripts/build_ghc_family_v655_v5_closeout.py",
    "scripts/ghc_family_v655_v5_final_staged_review.py",
    "scripts/ghc_family_v655_v5_final_validate.py",
    "tests/test_ghc_family_v655_v5_closeout.py",
}
SCANNERS = {
    "scripts/ghc_family_v655_v5_final_staged_review.py",
    "scripts/ghc_family_v655_v5_final_validate.py",
}


def git(*args: str, text: bool = True) -> str | bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
    )
    return result.stdout.strip() if text else result.stdout


def index_bytes(path: str) -> bytes:
    return git("show", f":{path}", text=False)


def write(relative: str, payload: dict) -> None:
    path = REPO / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    if str(git("rev-parse", "HEAD")) != BASE:
        raise RuntimeError("final staged review requires the exact evidence head")
    paths = sorted(
        row
        for row in str(git("diff", "--cached", "--name-only")).splitlines()
        if row
    )
    status_rows = [
        row.split("\t", 1)
        for row in str(git("diff", "--cached", "--name-status")).splitlines()
        if row
    ]
    out_of_scope = sorted(
        path
        for path in paths
        if not path.startswith(PHASE_PREFIX) and path not in ALLOWED_NONPHASE
    )
    destructive = [
        {"status": status, "path": path}
        for status, path in status_rows
        if status.startswith(("D", "R", "C"))
    ]
    baseline_paths = set(str(git("ls-tree", "-r", "--name-only", BASE)).splitlines())
    baseline_changes = sorted(set(paths) & baseline_paths)
    required = {
        "scripts/build_ghc_family_v655_v5_closeout.py",
        "scripts/ghc_family_v655_v5_final_staged_review.py",
        "scripts/ghc_family_v655_v5_final_validate.py",
        "tests/test_ghc_family_v655_v5_closeout.py",
        PHASE_PREFIX + "closeout/closeout-receipt.json",
        PHASE_PREFIX + "seal/seal-receipt.json",
        PHASE_PREFIX + "lifecycle/final-record.json",
        PHASE_PREFIX + "validation/final-owner-manifest.json",
        PHASE_PREFIX + "handoffs/caelen-ash-v655-v6-activation.md",
    }
    missing_required = sorted(required - set(paths))
    patterns = {
        "raw_uuid": re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
            r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_path": re.compile(
            r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"
        ),
        "credential_or_secret": re.compile(
            r"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|"
            r"(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}|"
            r"(?<![A-Za-z0-9])AKIA[0-9A-Z]{16}|"
            r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"
        ),
        "private_route_value": re.compile(
            r"(?:source_thread_id|resume[_ -]?token|private_callable_identifier)"
            r"\s*[:=]\s*[\"'][^\"']+",
            re.I,
        ),
        "session_stream_payload": re.compile(
            r"(?:conversation[_ -]?transcript|session[_ -]?stream)"
            r"\s*[:=]\s*[\"'][^\"']+",
            re.I,
        ),
    }
    reviewed = [path for path in paths if path not in SELF_EXCLUSIONS]
    entries = []
    json_count = 0
    json_errors = []
    candidates = []
    for path in reviewed:
        content = index_bytes(path)
        entries.append(
            {
                "path": path,
                "git_blob": str(git("rev-parse", f":{path}")),
                "sha256": hashlib.sha256(content).hexdigest(),
                "bytes": len(content),
            }
        )
        if path.endswith(".json"):
            json_count += 1
            try:
                json.loads(content.decode("utf-8"))
            except Exception as exc:
                json_errors.append({"path": path, "error": type(exc).__name__})
        if Path(path).suffix.lower() in {
            ".py",
            ".json",
            ".md",
            ".txt",
            ".html",
            ".yaml",
            ".yml",
        }:
            text = content.decode("utf-8", errors="replace")
            for label, pattern in patterns.items():
                if pattern.search(text):
                    candidates.append({"path": path, "class": label})
    confirmed = [row for row in candidates if row["path"] not in SCANNERS]
    names_sha256 = hashlib.sha256(
        ("\n".join(paths) + "\n").encode("utf-8")
    ).hexdigest()
    manifest = {
        "schema": "ghc.family.v655-v5.final-staged-manifest.v1",
        "base_commit": BASE,
        "staged_path_count": len(paths),
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": sorted(SELF_EXCLUSIONS),
        "exact_staged_names_sha256": names_sha256,
        "boundary": "Raw Git-index manifest with two lifecycle self-exclusions.",
    }
    write(MANIFEST, manifest)
    valid = (
        bool(paths)
        and not out_of_scope
        and not destructive
        and not baseline_changes
        and not missing_required
        and not json_errors
        and not confirmed
        and len(entries) == len(paths) - len(set(paths) & SELF_EXCLUSIONS)
    )
    review = {
        "schema": "ghc.family.v655-v5.final-staged-review.v1",
        "base_commit": BASE,
        "staged_path_count": len(paths),
        "manifest_entry_count": len(entries),
        "exact_staged_names_sha256": names_sha256,
        "status_rows": [
            {"status": status, "path": path} for status, path in status_rows
        ],
        "out_of_scope_paths": out_of_scope,
        "destructive_paths": destructive,
        "baseline_changes": baseline_changes,
        "missing_required_paths": missing_required,
        "json_parse_count": json_count,
        "json_errors": json_errors,
        "privacy_pattern_classes": sorted(patterns),
        "privacy_candidates": candidates,
        "privacy_confirmed_hits": confirmed,
        "valid": valid,
        "boundary": (
            "Exact final candidate review only; it does not preclaim the "
            "containing commit, terminal validation, delivery, or external authority."
        ),
    }
    write(REVIEW, review)
    print(
        json.dumps(
            {
                "valid": valid,
                "staged": len(paths),
                "manifest": len(entries),
                "json": json_count,
                "privacy_hits": len(confirmed),
            },
            sort_keys=True,
        )
    )
    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
