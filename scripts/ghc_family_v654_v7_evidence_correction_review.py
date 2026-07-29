#!/usr/bin/env python3
"""Review the exact Elaren v654-v7 post-evidence correction delta."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/elaren-kestrel/v654-v7/"
X1 = "773528bda8b863218ba4aaed0ce134fcd48abb97"
EVIDENCE = "303e98c74c90c85330343f953784a79e0df5ac70"
MANIFEST = PHASE_PREFIX + "validation/evidence-candidate-manifest.json"
RECEIPT = PHASE_PREFIX + "validation/evidence-correction-staged-review.json"
ALLOWED_NONPHASE = {
    "scripts/build_ghc_family_v654_v7_evidence.py",
    "scripts/ghc_family_v654_v7_validate.py",
    "scripts/ghc_family_v654_v7_evidence_correction_review.py",
    "tests/test_ghc_family_v654_v7_validation.py",
}
SCANNER_PATHS = {
    "scripts/ghc_family_v654_v7_validate.py",
    "scripts/ghc_family_v654_v7_evidence_correction_review.py",
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


def staged_blob(path: str) -> bytes:
    return git("show", f":{path}", text=False)


def main() -> None:
    if str(git("rev-parse", "HEAD")) != EVIDENCE:
        raise RuntimeError("correction review requires the immutable evidence head")
    paths = [
        row
        for row in str(git("diff", "--cached", "--name-only")).splitlines()
        if row
    ]
    status_rows = [
        row.split("\t", 1)
        for row in str(git("diff", "--cached", "--name-status")).splitlines()
        if row
    ]
    allowed = [
        path
        for path in paths
        if path.startswith(PHASE_PREFIX) or path in ALLOWED_NONPHASE
    ]
    out_of_scope = sorted(set(paths) - set(allowed))
    destructive = [
        {"status": status, "path": path}
        for status, path in status_rows
        if status.startswith(("D", "R", "C"))
    ]
    x1_paths = set(str(git("ls-tree", "-r", "--name-only", X1)).splitlines())
    frozen_changes = sorted(set(paths) & x1_paths)
    required = {
        "scripts/build_ghc_family_v654_v7_evidence.py",
        "scripts/ghc_family_v654_v7_validate.py",
        "scripts/ghc_family_v654_v7_evidence_correction_review.py",
        "tests/test_ghc_family_v654_v7_validation.py",
        PHASE_PREFIX + "truth/retained-negative-register-x2.json",
        PHASE_PREFIX + "method-flow/method-flow-ledger-x2.json",
        PHASE_PREFIX + "validation/evidence-validation.json",
        PHASE_PREFIX + "validation/evidence-minimal-validation.json",
        MANIFEST,
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
    reviewed = [path for path in paths if path != RECEIPT]
    entries: list[dict[str, object]] = []
    json_count = 0
    json_errors: list[dict[str, str]] = []
    privacy_candidates: list[dict[str, str]] = []
    for path in reviewed:
        content = staged_blob(path)
        entries.append(
            {
                "path": path,
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
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
                    privacy_candidates.append({"path": path, "class": label})
    privacy_confirmed = [
        row for row in privacy_candidates if row["path"] not in SCANNER_PATHS
    ]

    manifest = json.loads(staged_blob(MANIFEST).decode("utf-8"))
    manifest_mismatches: list[dict[str, str]] = []
    for row in manifest["entries"]:
        try:
            actual = str(git("rev-parse", f":{row['path']}"))
        except subprocess.CalledProcessError:
            actual = "missing"
        if actual != row["git_blob"]:
            manifest_mismatches.append(
                {
                    "path": row["path"],
                    "expected": row["git_blob"],
                    "actual": actual,
                }
            )
    detailed = json.loads(
        staged_blob(PHASE_PREFIX + "validation/evidence-validation.json").decode(
            "utf-8"
        )
    )
    minimal = json.loads(
        staged_blob(
            PHASE_PREFIX + "validation/evidence-minimal-validation.json"
        ).decode("utf-8")
    )
    valid = (
        bool(paths)
        and not out_of_scope
        and not destructive
        and not frozen_changes
        and not missing_required
        and not json_errors
        and not privacy_confirmed
        and not manifest_mismatches
        and detailed.get("valid") is True
        and minimal.get("valid") is True
        and detailed.get("manifest_entry_count") == manifest.get("entry_count")
        and minimal.get("manifest_entry_count") == manifest.get("entry_count")
    )
    receipt = {
        "schema": "ghc.family.v654-v7.evidence-correction-staged-review.v1",
        "baseline_evidence_commit": EVIDENCE,
        "staged_path_count": len(paths),
        "reviewed_path_count": len(reviewed),
        "status_rows": [
            {"status": status, "path": path} for status, path in status_rows
        ],
        "reviewed_entries": entries,
        "out_of_scope_paths": out_of_scope,
        "destructive_paths": destructive,
        "x1_frozen_changes": frozen_changes,
        "missing_required_paths": missing_required,
        "json_parse_count": json_count,
        "json_errors": json_errors,
        "privacy_pattern_classes": sorted(patterns),
        "privacy_candidates": privacy_candidates,
        "privacy_confirmed_hits": privacy_confirmed,
        "manifest_entry_count": manifest["entry_count"],
        "manifest_mismatches": manifest_mismatches,
        "detailed_validation_valid": detailed.get("valid"),
        "minimal_validation_valid": minimal.get("valid"),
        "valid": valid,
        "boundary": (
            "Exact post-evidence correction delta only; no final-head, routing, "
            "independent-reproduction, production, professional, legal, cultural, "
            "Māori-authority, Theory-of-Everything, or Stage 20 credit."
        ),
    }
    target = REPO / RECEIPT
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "valid": valid,
                "staged": len(paths),
                "reviewed": len(reviewed),
                "json": json_count,
                "privacy_hits": len(privacy_confirmed),
                "manifest": manifest["entry_count"],
            },
            sort_keys=True,
        )
    )
    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
