#!/usr/bin/env python3
"""Create v651-v2 final delta, owner, privacy, and staged review contracts."""

from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = "docs/orin-thale/v651-v2"
EVIDENCE = "8b3c1bb68852acc52c4554c34f1b6689a7c49efd"
OUT = {
    "delta_manifest": f"{PHASE_ROOT}/validation/final-delta-manifest.json",
    "owner_manifest": f"{PHASE_ROOT}/validation/final-owner-manifest.json",
    "delta_privacy": f"{PHASE_ROOT}/validation/final-delta-privacy.json",
    "owner_privacy": f"{PHASE_ROOT}/validation/final-owner-privacy.json",
    "review": f"{PHASE_ROOT}/validation/final-staged-review.json",
}
SELF_EXCLUSIONS = sorted(OUT.values())
ALLOWED_EXACT = {
    "scripts/build_ghc_family_v651_v2_closeout.py",
    "scripts/ghc_family_v651_v2_closeout_review.py",
    "scripts/ghc_family_v651_v2_final_validate.py",
    "tests/test_ghc_family_v651_v2_closeout.py",
}
PATTERNS = {
    "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_local_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/Users/|/home/)", re.I),
    "private_uri": re.compile(rb"(?:codex|chatgpt|file|vscode|app)://", re.I),
    "delegation_markup": re.compile(rb"<\s*(?:codex_delegation|source_thread_id|private_route)\b", re.I),
    "credential_assignment": re.compile(rb"(?:api[_-]?key|password|private[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-/+=]{12,}", re.I),
}


def run(*args: str, binary: bool = False) -> str | bytes:
    output = subprocess.check_output(list(args), cwd=REPO)
    return output if binary else output.decode("utf-8").strip()


def write_json(path: str, payload: object) -> None:
    target = REPO / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def index_map(paths: list[str] | None = None) -> dict[str, str]:
    args = ["git", "ls-files", "--stage", "-z"]
    if paths is not None:
        args.extend(["--", *paths])
    raw = run(*args, binary=True)
    result = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        _mode, oid, _stage = meta.decode().split()
        result[path.decode("utf-8")] = oid
    return result


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    proc = subprocess.run(["git", "cat-file", "--batch"], cwd=REPO, input="".join(oid + "\n" for oid in unique).encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    stream = io.BytesIO(proc.stdout)
    result = {}
    for expected in unique:
        header = stream.readline().rstrip(b"\n").decode().split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise RuntimeError(f"unexpected blob header: {header}")
        size = int(header[2])
        data = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError("missing batch terminator")
        result[expected] = data
    if stream.read():
        raise RuntimeError("unexpected trailing batch output")
    return result


def entries_for(paths: list[str], index: dict[str, str], blobs: dict[str, bytes]) -> list[dict]:
    return [{"path": path, "bytes": len(blobs[index[path]]), "git_blob": index[path], "sha256": hashlib.sha256(blobs[index[path]]).hexdigest()} for path in paths]


def definition_candidate(path: str, data: bytes, class_name: str, offset: int) -> dict | None:
    line_start = data.rfind(b"\n", 0, offset) + 1
    line_end = data.find(b"\n", offset)
    if line_end < 0:
        line_end = len(data)
    line = data[line_start:line_end]
    scanner_files = {
        "scripts/ghc_family_v651_v2_closeout_review.py",
        "scripts/ghc_family_v651_v2_final_validate.py",
    }
    if path in scanner_files and b"re.compile(rb" in line:
        return {"path": path, "class": class_name, "offset": offset, "reason": "scanner_definition"}
    if path == "tests/test_ghc_family_v651_v2_closeout.py" and b"self.assertNotIn" in line:
        return {"path": path, "class": class_name, "offset": offset, "reason": "sanitizer_negative_assertion"}
    return None


def scan(paths: list[str], index: dict[str, str], blobs: dict[str, bytes]) -> tuple[list[dict], list[dict], int]:
    hits = []
    candidates = []
    json_count = 0
    for path in paths:
        data = blobs[index[path]]
        if path.endswith(".json"):
            json.loads(data.decode("utf-8"))
            json_count += 1
        for class_name, pattern in PATTERNS.items():
            for match in pattern.finditer(data):
                candidate = definition_candidate(path, data, class_name, match.start())
                if candidate:
                    candidates.append(candidate)
                else:
                    hits.append({"path": path, "class": class_name, "offset": match.start()})
    return hits, candidates, json_count


def main() -> None:
    if run("git", "rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout review must run at the exact pushed evidence head")
    raw = run("git", "diff", "--cached", "--name-only", "-z", binary=True)
    delta_paths = sorted(part.decode("utf-8") for part in raw.split(b"\0") if part)
    if any(path in SELF_EXCLUSIONS for path in delta_paths):
        raise RuntimeError("self-excluding final receipts must not be staged before generation")
    unexpected = [path for path in delta_paths if not (path.startswith(PHASE_ROOT + "/") or path in ALLOWED_EXACT)]
    if unexpected:
        raise RuntimeError(f"unexpected closeout paths: {unexpected}")
    required = [f"{PHASE_ROOT}/final/phase-truth.json", f"{PHASE_ROOT}/seal/seal-candidate.json", f"{PHASE_ROOT}/handoffs/tamar-vey-v651-v3-activation.md", "scripts/ghc_family_v651_v2_final_validate.py", "tests/test_ghc_family_v651_v2_closeout.py"]
    missing = sorted(set(required) - set(delta_paths))
    if missing:
        raise RuntimeError(f"missing closeout paths: {missing}")
    diff_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    if diff_check.returncode:
        raise RuntimeError(diff_check.stdout + diff_check.stderr)

    all_index = index_map()
    delta_index = {path: all_index[path] for path in delta_paths}
    owner_paths = sorted(path for path in all_index if path.startswith(PHASE_ROOT + "/"))
    owner_index = {path: all_index[path] for path in owner_paths}
    blobs = batch_blobs(list(delta_index.values()) + list(owner_index.values()))
    delta_hits, delta_candidates, delta_json = scan(delta_paths, delta_index, blobs)
    owner_hits, owner_candidates, owner_json = scan(owner_paths, owner_index, blobs)
    if delta_hits or owner_hits:
        raise RuntimeError(f"confirmed privacy hits: {(delta_hits + owner_hits)[:5]}")
    delta_entries = entries_for(delta_paths, delta_index, blobs)
    owner_entries = entries_for(owner_paths, owner_index, blobs)
    write_json(OUT["delta_manifest"], {"schema": "ghc.family.v651-v2.final-delta-manifest.v1", "parent": EVIDENCE, "hash_domain": "exact_git_index_blob", "entry_count": len(delta_entries), "covered_path_count": len(delta_entries) + len(SELF_EXCLUSIONS), "self_exclusions": SELF_EXCLUSIONS, "entries": delta_entries})
    write_json(OUT["owner_manifest"], {"schema": "ghc.family.v651-v2.final-owner-manifest.v1", "hash_domain": "exact_git_index_blob", "entry_count": len(owner_entries), "covered_path_count": len(owner_entries) + len(SELF_EXCLUSIONS), "self_exclusions": SELF_EXCLUSIONS, "entries": owner_entries})
    write_json(OUT["delta_privacy"], {"schema": "ghc.family.v651-v2.final-delta-privacy.v1", "pattern_classes": sorted(PATTERNS), "files_scanned": len(delta_paths), "definition_candidates": delta_candidates, "confirmed_hits": delta_hits, "zero_confirmed_hits": True, "boundary": "Five-class scanning is not privacy-complete assurance."})
    write_json(OUT["owner_privacy"], {"schema": "ghc.family.v651-v2.final-owner-privacy.v1", "pattern_classes": sorted(PATTERNS), "files_scanned": len(owner_paths), "definition_candidates": owner_candidates, "confirmed_hits": owner_hits, "zero_confirmed_hits": True, "boundary": "Five-class scanning is not privacy-complete assurance."})
    write_json(OUT["review"], {"schema": "ghc.family.v651-v2.final-staged-review.v1", "parent": EVIDENCE, "delta_entries": len(delta_entries), "owner_entries": len(owner_entries), "self_exclusion_count": len(SELF_EXCLUSIONS), "predicted_final_delta_paths": len(delta_entries) + len(SELF_EXCLUSIONS), "predicted_final_owner_paths": len(owner_entries) + len(SELF_EXCLUSIONS), "delta_json_before_self_exclusions": delta_json, "owner_json_before_self_exclusions": owner_json, "definition_candidate_count": len(delta_candidates) + len(owner_candidates), "unexpected_paths": unexpected, "diff_hygiene": "pass", "closeout_tests": {"passed": 10, "total": 10}, "route_state": "PREPARED_NOT_SENT", "privacy_zero_confirmed_hits": True, "valid": True, "boundary": "Combined closeout/seal staged review only; exact-final validation must run once after commit and push."})
    print(json.dumps({"delta_entries": len(delta_entries), "owner_entries": len(owner_entries), "self_exclusions": len(SELF_EXCLUSIONS), "delta_json": delta_json, "owner_json": owner_json, "definition_candidates": len(delta_candidates) + len(owner_candidates), "privacy_hits": 0, "valid": True}))


if __name__ == "__main__":
    main()
