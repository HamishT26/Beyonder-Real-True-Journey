#!/usr/bin/env python3
"""Review the exact staged Tamar v652-v3 closeout delta and owner union."""

from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tamar-vey/v652-v3"
SOURCE = "fa060eec3071694e1aff8eaf7d76d6c4b0f8075e"
X1 = "4e905d2b0637d4db78ac55273c8b52d5cf6c2117"
EVIDENCE = "22c4ca1e7d4473fcf5246867bb729b3748f34441"

EXCLUSIONS = {
    "docs/tamar-vey/v652-v3/validation/closeout-delta-manifest.json",
    "docs/tamar-vey/v652-v3/validation/final-owner-manifest.json",
    "docs/tamar-vey/v652-v3/validation/closeout-staged-privacy.json",
    "docs/tamar-vey/v652-v3/validation/closeout-staged-review.json",
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


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    proc = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input="".join(oid + "\n" for oid in unique).encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    stream = io.BytesIO(proc.stdout)
    result: dict[str, bytes] = {}
    for expected in unique:
        header = stream.readline().rstrip(b"\n").decode().split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise RuntimeError(f"unexpected blob header: {header}")
        size = int(header[2])
        data = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError("missing batch frame terminator")
        result[expected] = data
    return result


def index_map() -> dict[str, str]:
    raw = git("ls-files", "-s", "-z", binary=True)
    assert isinstance(raw, bytes)
    result: dict[str, str] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        _mode, oid, stage = meta.decode().split()
        if stage == "0":
            result[path.decode("utf-8")] = oid
    return result


def entry(path: str, index: dict[str, str], blobs: dict[str, bytes]) -> dict[str, object]:
    oid = index[path]
    data = blobs[oid]
    return {"path": path, "git_blob": oid, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def replay_manifest(commit: str, relative: str, expected_paths: set[str]) -> dict[str, object]:
    raw = git("show", f"{commit}:{relative}")
    manifest = json.loads(str(raw))
    declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    tree_raw = git("ls-tree", "-r", "-z", commit, binary=True)
    assert isinstance(tree_raw, bytes)
    tree: dict[str, str] = {}
    for record in tree_raw.split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        _mode, kind, oid = meta.decode().split()
        if kind == "blob":
            tree[path.decode("utf-8")] = oid
    blobs = batch_blobs([row["git_blob"] for row in manifest["entries"]])
    mismatches = []
    for row in manifest["entries"]:
        oid = tree.get(row["path"])
        data = blobs.get(row["git_blob"])
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
    index = index_map()
    staged_blobs = batch_blobs([index[path] for path in sorted(owner_paths) if path in index])
    delta_entries = [entry(path, index, staged_blobs) for path in sorted(delta_paths - EXCLUSIONS)]
    owner_entries = [entry(path, index, staged_blobs) for path in sorted(owner_paths - EXCLUSIONS)]

    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definition_paths = {
        "scripts/build_ghc_family_v652_v3_preregistration.py",
        "scripts/ghc_family_v652_v3_evidence_validate.py",
        "scripts/ghc_family_v652_v3_closeout_review.py",
        "scripts/ghc_family_v652_v3_final_validate.py",
        "docs/tamar-vey/v652-v3/validation/x1-staged-privacy.json",
        "docs/tamar-vey/v652-v3/validation/evidence-staged-privacy.json",
        "docs/tamar-vey/v652-v3/validation/closeout-staged-privacy.json",
    }
    candidates, confirmed, json_errors = [], [], []
    for path in sorted(owner_paths):
        data = staged_blobs[index[path]]
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
    x1 = replay_manifest(X1, "docs/tamar-vey/v652-v3/validation/x1-staged-manifest.json", x1_paths)
    evidence = replay_manifest(EVIDENCE, "docs/tamar-vey/v652-v3/validation/evidence-staged-manifest.json", evidence_paths)
    diff_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True)
    unstaged = str(git("diff", "--name-only")).splitlines()
    valid = not confirmed and not json_errors and not unstaged and diff_check.returncode == 0 and x1["valid"] and evidence["valid"]

    write("validation/closeout-delta-manifest.json", {"schema": "ghc.family.v652-v3.closeout-delta-manifest.v1", "hash_domain": "git_index_blob", "base_commit": EVIDENCE, "entries": delta_entries, "entry_count": len(delta_entries), "self_exclusions": sorted(EXCLUSIONS), "coverage_boundary": "Exact evidence-to-closeout staged delta except four declared self-referential review files."})
    write("validation/final-owner-manifest.json", {"schema": "ghc.family.v652-v3.final-owner-manifest.v1", "hash_domain": "git_index_blob", "source_commit": SOURCE, "entries": owner_entries, "entry_count": len(owner_entries), "self_exclusions": sorted(EXCLUSIONS), "coverage_boundary": "Exact source-to-final owner union at the staged closeout candidate except four declared self-referential review files."})
    write("validation/closeout-staged-privacy.json", {"schema": "ghc.family.v652-v3.closeout-privacy.v1", "scanned_file_count": len(owner_paths), "pattern_classes": sorted(patterns), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "boundary": "Five structural classes; zero confirmed hits is not complete privacy assurance."})
    write("validation/closeout-staged-review.json", {"schema": "ghc.family.v652-v3.closeout-staged-review.v1", "delta_path_count": len(delta_paths), "delta_manifest_entry_count": len(delta_entries), "owner_path_count": len(owner_paths), "owner_manifest_entry_count": len(owner_entries), "self_exclusion_count": len(EXCLUSIONS), "json_parsed_count": sum(path.endswith(".json") for path in owner_paths), "json_errors": json_errors, "privacy_confirmed_hits": len(confirmed), "x1_manifest_replay": x1, "evidence_manifest_replay": evidence, "unstaged_paths": unstaged, "diff_check_exit": diff_check.returncode, "valid": valid, "boundary": "Exact staged closeout review only; not final commit, canonical exact-head validation, independent reproduction, complete privacy, exhaustive security, accessibility conformance, authority, or Stage 20 readiness."})
    print(json.dumps({"delta_paths": len(delta_paths), "delta_entries": len(delta_entries), "owner_paths": len(owner_paths), "owner_entries": len(owner_entries), "json": sum(path.endswith('.json') for path in owner_paths), "privacy_hits": len(confirmed), "x1": x1["valid"], "evidence": evidence["valid"], "valid": valid}, sort_keys=True))
    raise SystemExit(0 if valid else 1)


if __name__ == "__main__":
    main()
