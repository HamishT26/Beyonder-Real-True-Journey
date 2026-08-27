#!/usr/bin/env python3
"""Build exact staged manifests and reviews for Caelen Ash v672-v4."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/caelen-ash/v672-v4/"
X1_PROTECTED = {
    "scripts/build_ghc_family_caelen_ash_v672_v4.py",
    "tests/test_ghc_family_caelen_ash_v672_v4_x1.py",
}
REQUIRED_EVIDENCE_PATHS = {
    "docs/caelen-ash/v672-v4/x2/generation-state.json",
    "docs/caelen-ash/v672-v4/x2/method-flow/ledger.json",
    "docs/caelen-ash/v672-v4/x2/phase-truth.json",
    "docs/caelen-ash/v672-v4/x2/proposals/outcome-ledger.json",
    "docs/caelen-ash/v672-v4/x2/retained-negative-register.json",
    "scripts/ghc_family_caelen_v672_v4_build_x2.py",
    "scripts/ghc_family_caelen_v672_v4_weaving_guard.py",
    "scripts/ghc_family_caelen_v672_v4_manifest_guard.py",
    "scripts/ghc_family_caelen_v672_v4_privacy_guard.py",
    "scripts/ghc_family_caelen_v672_v4_record_x2_recovery.py",
    "scripts/ghc_family_caelen_v672_v4_record_stage_recovery.py",
    "scripts/ghc_family_caelen_v672_v4_record_archive_recovery.py",
    "scripts/ghc_family_caelen_v672_v4_stage_review.py",
    "scripts/ghc_family_caelen_v672_v4_warp_plan_guard.py",
    "scripts/ghc_family_caelen_v672_v4_material_provenance_guard.py",
    "scripts/ghc_family_caelen_v672_v4_loom_compatibility_guard.py",
    "scripts/ghc_family_caelen_v672_v4_threading_sequence_guard.py",
    "scripts/ghc_family_caelen_v672_v4_pattern_lineage_guard.py",
    "scripts/ghc_family_caelen_v672_v4_accessibility_structure_guard.py",
    "scripts/ghc_family_caelen_v672_v4_privacy_minimization_guard.py",
    "scripts/ghc_family_caelen_v672_v4_workload_handover_guard.py",
    "scripts/ghc_family_caelen_v672_v4_authority_boundary_guard.py",
    "scripts/ghc_family_caelen_v672_v4_weaving_packet_guard.py",
    "tests/test_ghc_family_caelen_ash_v672_v4_x2.py",
}
REQUIRED_FINAL_PATHS = {
    "docs/caelen-ash/v672-v4/closeout/closeout-receipt.json",
    "docs/caelen-ash/v672-v4/closeout/content-seal.json",
    "docs/caelen-ash/v672-v4/closeout/final-overview.md",
    "docs/caelen-ash/v672-v4/closeout/final-validation-candidate.json",
    "docs/caelen-ash/v672-v4/closeout/owner-manifest.json",
    "docs/caelen-ash/v672-v4/closeout/phase-index.json",
    "docs/caelen-ash/v672-v4/closeout/phase-truth.json",
    "docs/caelen-ash/v672-v4/closeout/stale-label-review.json",
    "docs/caelen-ash/v672-v4/closeout/wellbeing-check.json",
    "docs/caelen-ash/v672-v4/handoffs/terminal-route-hold.json",
    "scripts/ghc_family_caelen_v672_v4_build_closeout.py",
    "scripts/ghc_family_caelen_v672_v4_build_owner_manifest.py",
    "scripts/validate_ghc_family_caelen_ash_v672_v4_final.py",
    "tests/test_ghc_family_caelen_ash_v672_v4_final.py",
}
PATTERNS = {
    "raw_uuid_identifier": re.compile(rb"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"),
    "private_absolute_windows_path": re.compile(rb"\b[A-Za-z]:\\(?:Users|GHC-Archives|Windows)\\[^\r\n\"']+"),
    "credential_assignment": re.compile(rb"(?i)\b(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*[\"'][^\"']{8,}[\"']"),
    "private_application_route": re.compile(rb"\b(?:app|file|vscode)://[^\s\"']+"),
    "session_stream_marker": re.compile(rb"(?i)\b(?:session[_-]?stream|terminal[_-]?session)\s*[:=]\s*[\"'][^\"']+[\"']"),
}


def git(*args: str, text: bool = False):
    completed = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True,
        check=True,
        text=text,
        encoding="utf-8" if text else None,
    )
    return completed.stdout


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def allowed(path: str, lifecycle: str) -> bool:
    if path.startswith(PHASE_PREFIX):
        if lifecycle == "evidence":
            return path.startswith(PHASE_PREFIX + "x2/") or path.startswith(PHASE_PREFIX + "validation/")
        return path.startswith(PHASE_PREFIX + "closeout/") or path.startswith(PHASE_PREFIX + "validation/") or path.startswith(PHASE_PREFIX + "handoffs/")
    if path.startswith("scripts/ghc_family_caelen_v672_v4_") and path.endswith(".py"):
        return True
    if path.startswith("tests/test_ghc_family_caelen_ash_v672_v4_") and path.endswith(".py"):
        return path not in X1_PROTECTED
    if path == "scripts/validate_ghc_family_caelen_ash_v672_v4_final.py":
        return lifecycle == "final"
    return False


def build(lifecycle: str) -> None:
    manifest_relative = f"docs/caelen-ash/v672-v4/validation/{lifecycle}-staged-manifest.json"
    review_relative = f"docs/caelen-ash/v672-v4/validation/{lifecycle}-staged-review.json"
    self_exclusions = [manifest_relative, review_relative]
    paths = sorted(git("diff", "--cached", "--name-only", "--diff-filter=ACMR", text=True).splitlines())
    entries = []
    candidates = []
    json_issues = []
    json_count = 0
    markdown_counts = []
    for path in paths:
        if path in self_exclusions:
            continue
        blob = git("show", f":{path}")
        oid = git("rev-parse", f":{path}", text=True).strip()
        entries.append(
            {
                "path": path,
                "git_blob_oid": oid,
                "sha256": hashlib.sha256(blob).hexdigest(),
                "bytes": len(blob),
            }
        )
        if path.endswith(".json"):
            json_count += 1
            try:
                json.loads(blob.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                json_issues.append({"path": path, "error": str(exc)})
        if path.endswith(".md"):
            try:
                words = len(blob.decode("utf-8").split())
            except UnicodeDecodeError:
                words = -1
            markdown_counts.append({"path": path, "words": words})
        if b"\x00" not in blob:
            for class_name, pattern in PATTERNS.items():
                for match in pattern.finditer(blob):
                    candidates.append(
                        {
                            "path": path,
                            "class": class_name,
                            "offset": match.start(),
                            "disposition": "confirmed_payload_hit",
                        }
                    )
    diff_check = subprocess.run(
        ["git", "-C", str(ROOT), "diff", "--cached", "--check"],
        text=True,
        encoding="utf-8",
        capture_output=True,
    )
    x1_changes = [
        path
        for path in paths
        if path.startswith(PHASE_PREFIX + "x1/") or path in X1_PROTECTED
    ]
    out_of_scope = [path for path in paths if path not in self_exclusions and not allowed(path, lifecycle)]
    required_paths = REQUIRED_EVIDENCE_PATHS if lifecycle == "evidence" else REQUIRED_FINAL_PATHS
    missing_required = sorted(required_paths - set(paths))
    write_json(
        ROOT / manifest_relative,
        {
            "schema": f"ghc.family.caelen.v672-v4.{lifecycle}-staged-manifest.v1",
            "lifecycle": lifecycle,
            "entries": entries,
            "entry_count": len(entries),
            "self_exclusions": self_exclusions,
            "expected_surface_count": len(entries) + len(self_exclusions),
        },
    )
    write_json(
        ROOT / review_relative,
        {
            "schema": f"ghc.family.caelen.v672-v4.{lifecycle}-staged-review.v1",
            "lifecycle": lifecycle,
            "staged_paths": paths,
            "staged_path_count": len(paths),
            "manifest_entries": len(entries),
            "self_exclusions": self_exclusions,
            "x1_frozen_changes": x1_changes,
            "out_of_scope_paths": out_of_scope,
            "missing_required_paths": missing_required,
            "json_parse": {"documents": json_count, "issues": json_issues},
            "privacy_scan": {
                "classes": len(PATTERNS),
                "candidates": candidates,
                "confirmed_hits": len(candidates),
            },
            "markdown_word_counts": markdown_counts,
            "documents_over_100000_words": [row["path"] for row in markdown_counts if row["words"] > 100000],
            "diff_hygiene": {"exit_code": diff_check.returncode, "output": diff_check.stdout + diff_check.stderr},
            "valid": not (
                x1_changes or out_of_scope or missing_required or json_issues or candidates
                or any(row["words"] > 100000 for row in markdown_counts)
                or diff_check.returncode
            ),
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("lifecycle", choices=("evidence", "final"))
    args = parser.parse_args()
    build(args.lifecycle)


if __name__ == "__main__":
    main()
