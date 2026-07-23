#!/usr/bin/env python3
"""Review the exact staged v652-v2 closeout delta and final owner union."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/orin-thale/v652-v2"
SOURCE = "f168bcb798715d61d8b0a9ec2c6646a7af09ce29"
X1 = "3f5b49dc1a380452593c8080c3ae134e654c2079"
EVIDENCE = "d185405470b9205a21d9b018bc0d3f7f44f49444"

EXCLUSIONS = {
    "docs/orin-thale/v652-v2/validation/closeout-delta-manifest.json",
    "docs/orin-thale/v652-v2/validation/final-owner-manifest.json",
    "docs/orin-thale/v652-v2/validation/closeout-staged-privacy.json",
    "docs/orin-thale/v652-v2/validation/closeout-staged-review.json",
}


def git(*args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(["git", *args], cwd=REPO, check=True, capture_output=True)
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def write(relative: str, payload: object) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def index_blob(path: str) -> tuple[str, bytes]:
    oid = str(git("rev-parse", f":{path}"))
    data = git("show", f":{path}", binary=True)
    assert isinstance(data, bytes)
    return oid, data


def entry(path: str) -> dict[str, object]:
    oid, data = index_blob(path)
    return {"path": path, "git_blob": oid, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def replay_manifest(commit: str, relative: str, expected_paths: set[str]) -> dict[str, object]:
    raw = git("show", f"{commit}:{relative}")
    manifest = json.loads(str(raw))
    declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    mismatches = []
    for row in manifest["entries"]:
        oid = str(git("rev-parse", f"{commit}:{row['path']}"))
        data = git("show", f"{commit}:{row['path']}", binary=True)
        assert isinstance(data, bytes)
        if oid != row["git_blob"] or len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            mismatches.append(row["path"])
    return {"entry_count": len(manifest["entries"]), "self_exclusion_count": len(manifest["self_exclusions"]), "path_set_equal": declared == expected_paths, "mismatches": mismatches, "valid": declared == expected_paths and not mismatches}


def main() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("closeout staged review requires exact evidence HEAD")
    delta_paths = set(str(git("diff", "--cached", "--name-only", EVIDENCE)).splitlines())
    owner_paths = set(str(git("diff", "--cached", "--name-only", SOURCE)).splitlines())
    if not EXCLUSIONS.issubset(delta_paths):
        raise SystemExit({"missing_self_exclusions": sorted(EXCLUSIONS - delta_paths)})
    delta_entries = [entry(path) for path in sorted(delta_paths - EXCLUSIONS)]
    owner_entries = [entry(path) for path in sorted(owner_paths - EXCLUSIONS)]

    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definition_paths = {
        "scripts/build_ghc_family_v652_v2_preregistration.py",
        "scripts/ghc_family_v652_v2_x1_validate.py",
        "scripts/ghc_family_v652_v2_evidence_validate.py",
        "scripts/ghc_family_v652_v2_closeout_review.py",
        "scripts/ghc_family_v652_v2_final_validate.py",
        "docs/orin-thale/v652-v2/validation/x1-staged-privacy.json",
        "docs/orin-thale/v652-v2/validation/evidence-staged-privacy.json",
        "docs/orin-thale/v652-v2/validation/closeout-staged-privacy.json",
    }
    candidates, confirmed, json_errors = [], [], []
    for path in sorted(owner_paths):
        _oid, data = index_blob(path)
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if path.endswith(".json"):
            try:
                json.loads(text)
            except Exception as exc:  # noqa: BLE001
                json_errors.append({"path": path, "error": str(exc)})
        for name, pattern in patterns.items():
            if pattern.search(text):
                disposition = "scanner_definition" if path in definition_paths else "confirmed_payload_hit"
                row = {"path": path, "pattern_class": name, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)

    x1_paths = set(str(git("diff-tree", "--no-commit-id", "--name-only", "-r", X1)).splitlines())
    evidence_paths = set(str(git("diff-tree", "--no-commit-id", "--name-only", "-r", EVIDENCE)).splitlines())
    x1 = replay_manifest(X1, "docs/orin-thale/v652-v2/validation/x1-staged-manifest.json", x1_paths)
    evidence = replay_manifest(EVIDENCE, "docs/orin-thale/v652-v2/validation/evidence-staged-manifest.json", evidence_paths)
    diff_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True)
    unstaged = str(git("diff", "--name-only")).splitlines()
    valid = not confirmed and not json_errors and not unstaged and diff_check.returncode == 0 and x1["valid"] and evidence["valid"]

    write("validation/closeout-delta-manifest.json", {"schema": "ghc.family.v652-v2.closeout-delta-manifest.v1", "hash_domain": "git_index_blob", "base_commit": EVIDENCE, "entries": delta_entries, "entry_count": len(delta_entries), "self_exclusions": sorted(EXCLUSIONS), "coverage_boundary": "Exact evidence-to-closeout staged delta except four declared self-referential review files."})
    write("validation/final-owner-manifest.json", {"schema": "ghc.family.v652-v2.final-owner-manifest.v1", "hash_domain": "git_index_blob", "source_commit": SOURCE, "entries": owner_entries, "entry_count": len(owner_entries), "self_exclusions": sorted(EXCLUSIONS), "coverage_boundary": "Exact source-to-final owner union at the staged closeout candidate except four declared self-referential review files."})
    write("validation/closeout-staged-privacy.json", {"schema": "ghc.family.v652-v2.closeout-privacy.v1", "scanned_file_count": len(owner_paths), "pattern_classes": sorted(patterns), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "boundary": "Five structural classes; zero confirmed hits is not complete privacy assurance."})
    write("validation/closeout-staged-review.json", {"schema": "ghc.family.v652-v2.closeout-staged-review.v1", "delta_path_count": len(delta_paths), "delta_manifest_entry_count": len(delta_entries), "owner_path_count": len(owner_paths), "owner_manifest_entry_count": len(owner_entries), "self_exclusion_count": len(EXCLUSIONS), "json_parsed_count": sum(path.endswith(".json") for path in owner_paths), "json_errors": json_errors, "privacy_confirmed_hits": len(confirmed), "x1_manifest_replay": x1, "evidence_manifest_replay": evidence, "unstaged_paths": unstaged, "diff_check_exit": diff_check.returncode, "valid": valid, "boundary": "Exact staged closeout review only; not final commit, canonical exact-head validation, independent reproduction, complete privacy, exhaustive security, accessibility conformance, authority, or Stage 20 readiness."})
    print(json.dumps({"delta_paths": len(delta_paths), "delta_entries": len(delta_entries), "owner_paths": len(owner_paths), "owner_entries": len(owner_entries), "json": sum(path.endswith('.json') for path in owner_paths), "privacy_hits": len(confirmed), "x1": x1["valid"], "evidence": evidence["valid"], "valid": valid}, sort_keys=True))
    raise SystemExit(0 if valid else 1)


if __name__ == "__main__":
    main()
