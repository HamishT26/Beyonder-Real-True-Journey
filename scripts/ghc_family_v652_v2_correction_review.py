#!/usr/bin/env python3
"""Review the exact staged v652-v2 terminal correction and corrected owner union."""

from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/orin-thale/v652-v2"
SOURCE = "f168bcb798715d61d8b0a9ec2c6646a7af09ce29"
X1 = "3f5b49dc1a380452593c8080c3ae134e654c2079"
EVIDENCE = "d185405470b9205a21d9b018bc0d3f7f44f49444"
CLOSEOUT = "0053eef587ebdc88d8bafbf09b2f214737abd539"
EXCLUSIONS = {
    "docs/orin-thale/v652-v2/validation/correction-delta-manifest.json",
    "docs/orin-thale/v652-v2/validation/corrected-owner-manifest.json",
    "docs/orin-thale/v652-v2/validation/correction-staged-privacy.json",
    "docs/orin-thale/v652-v2/validation/correction-staged-review.json",
}


def git(*args: str, binary: bool = False):
    proc = subprocess.run(["git", *args], cwd=REPO, check=True, capture_output=True)
    return proc.stdout if binary else proc.stdout.decode("utf-8").strip()


def write(relative: str, payload: object) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def batch(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    proc = subprocess.run(["git", "cat-file", "--batch"], cwd=REPO, input="".join(oid + "\n" for oid in unique).encode(), capture_output=True, check=True)
    stream = io.BytesIO(proc.stdout)
    result = {}
    for expected in unique:
        header = stream.readline().rstrip(b"\n").decode().split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise RuntimeError(header)
        size = int(header[2]); result[expected] = stream.read(size)
        if stream.read(1) != b"\n": raise RuntimeError("missing frame terminator")
    if stream.read(): raise RuntimeError("trailing batch output")
    return result


def index_entry(path: str) -> dict[str, object]:
    oid = str(git("rev-parse", f":{path}")); data = git("show", f":{path}", binary=True)
    assert isinstance(data, bytes)
    return {"path": path, "git_blob": oid, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def replay(commit: str, manifest_path: str, expected: set[str]) -> dict[str, object]:
    manifest = json.loads(str(git("show", f"{commit}:{manifest_path}")))
    declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    blobs = batch([row["git_blob"] for row in manifest["entries"]])
    mismatches = []
    for row in manifest["entries"]:
        oid = str(git("rev-parse", f"{commit}:{row['path']}")); data = blobs[row["git_blob"]]
        if oid != row["git_blob"] or len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            mismatches.append(row["path"])
    return {"entry_count": len(manifest["entries"]), "self_exclusion_count": len(manifest["self_exclusions"]), "path_set_equal": declared == expected, "mismatches": mismatches, "valid": declared == expected and not mismatches}


def main() -> None:
    if git("rev-parse", "HEAD") != CLOSEOUT:
        raise SystemExit("correction review requires exact first closeout HEAD")
    delta_paths = set(str(git("diff", "--cached", "--name-only", CLOSEOUT)).splitlines())
    owner_paths = set(str(git("diff", "--cached", "--name-only", SOURCE)).splitlines())
    if not EXCLUSIONS.issubset(delta_paths):
        raise SystemExit({"missing_self_exclusions": sorted(EXCLUSIONS - delta_paths)})
    delta_entries = [index_entry(path) for path in sorted(delta_paths - EXCLUSIONS)]
    owner_entries = [index_entry(path) for path in sorted(owner_paths - EXCLUSIONS)]

    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definition_paths = {
        "scripts/build_ghc_family_v652_v2_preregistration.py", "scripts/ghc_family_v652_v2_x1_validate.py",
        "scripts/ghc_family_v652_v2_evidence_validate.py", "scripts/ghc_family_v652_v2_closeout_review.py",
        "scripts/ghc_family_v652_v2_correction_review.py", "scripts/ghc_family_v652_v2_final_validate.py",
        "docs/orin-thale/v652-v2/validation/x1-staged-privacy.json", "docs/orin-thale/v652-v2/validation/evidence-staged-privacy.json",
        "docs/orin-thale/v652-v2/validation/closeout-staged-privacy.json", "docs/orin-thale/v652-v2/validation/correction-staged-privacy.json",
    }
    candidates, confirmed, json_errors = [], [], []
    for path in sorted(owner_paths):
        data = git("show", f":{path}", binary=True); assert isinstance(data, bytes)
        try: text = data.decode("utf-8")
        except UnicodeDecodeError: continue
        if path.endswith(".json"):
            try: json.loads(text)
            except Exception as exc: json_errors.append({"path": path, "error": str(exc)})
        for name, pattern in patterns.items():
            if pattern.search(text):
                disposition = "scanner_definition" if path in definition_paths else "confirmed_payload_hit"
                row = {"path": path, "pattern_class": name, "disposition": disposition}; candidates.append(row)
                if disposition == "confirmed_payload_hit": confirmed.append(row)

    x1_paths = set(str(git("diff-tree", "--no-commit-id", "--name-only", "-r", X1)).splitlines())
    evidence_paths = set(str(git("diff-tree", "--no-commit-id", "--name-only", "-r", EVIDENCE)).splitlines())
    closeout_paths = set(str(git("diff-tree", "--no-commit-id", "--name-only", "-r", CLOSEOUT)).splitlines())
    closeout_owner = set(str(git("diff", "--name-only", f"{SOURCE}..{CLOSEOUT}")).splitlines())
    prior = {
        "x1": replay(X1, "docs/orin-thale/v652-v2/validation/x1-staged-manifest.json", x1_paths),
        "evidence": replay(EVIDENCE, "docs/orin-thale/v652-v2/validation/evidence-staged-manifest.json", evidence_paths),
        "closeout_delta": replay(CLOSEOUT, "docs/orin-thale/v652-v2/validation/closeout-delta-manifest.json", closeout_paths),
        "closeout_owner": replay(CLOSEOUT, "docs/orin-thale/v652-v2/validation/final-owner-manifest.json", closeout_owner),
    }
    unstaged = str(git("diff", "--name-only")).splitlines()
    diff_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True)
    valid = not confirmed and not json_errors and not unstaged and diff_check.returncode == 0 and all(row["valid"] for row in prior.values())
    write("validation/correction-delta-manifest.json", {"schema": "ghc.family.v652-v2.correction-delta-manifest.v1", "hash_domain": "git_index_blob", "base_commit": CLOSEOUT, "entries": delta_entries, "entry_count": len(delta_entries), "self_exclusions": sorted(EXCLUSIONS), "coverage_boundary": "Exact closeout-to-corrected-final staged delta except four declared self-referential review files."})
    write("validation/corrected-owner-manifest.json", {"schema": "ghc.family.v652-v2.corrected-owner-manifest.v1", "hash_domain": "git_index_blob", "source_commit": SOURCE, "entries": owner_entries, "entry_count": len(owner_entries), "self_exclusions": sorted(EXCLUSIONS), "coverage_boundary": "Exact source-to-corrected-final owner union at the staged correction candidate except four declared self-referential review files."})
    write("validation/correction-staged-privacy.json", {"schema": "ghc.family.v652-v2.correction-privacy.v1", "scanned_file_count": len(owner_paths), "pattern_classes": sorted(patterns), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "boundary": "Five structural classes; zero confirmed hits is not complete privacy assurance."})
    write("validation/correction-staged-review.json", {"schema": "ghc.family.v652-v2.correction-staged-review.v1", "delta_path_count": len(delta_paths), "delta_manifest_entry_count": len(delta_entries), "owner_path_count": len(owner_paths), "owner_manifest_entry_count": len(owner_entries), "self_exclusion_count": len(EXCLUSIONS), "json_parsed_count": sum(path.endswith('.json') for path in owner_paths), "json_errors": json_errors, "privacy_confirmed_hits": len(confirmed), "prior_manifest_replay": prior, "unstaged_paths": unstaged, "diff_check_exit": diff_check.returncode, "valid": valid, "boundary": "Exact staged correction review only; not final commit, canonical exact-head validation, independent reproduction, complete privacy, exhaustive security, accessibility conformance, authority, or Stage 20 readiness."})
    print(json.dumps({"delta_paths": len(delta_paths), "delta_entries": len(delta_entries), "owner_paths": len(owner_paths), "owner_entries": len(owner_entries), "json": sum(path.endswith('.json') for path in owner_paths), "privacy_hits": len(confirmed), "prior": all(row['valid'] for row in prior.values()), "valid": valid}, sort_keys=True))
    raise SystemExit(0 if valid else 1)


if __name__ == "__main__": main()
