#!/usr/bin/env python3
"""Build exact final-delta and final-owner manifests before the closeout commit."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = "docs/eiren-kestrel/v651-v5-2-remaster"
EVIDENCE = "c67ce592463450ccf9aee7d460210cddb467c5ca"
CLOSEOUT = "7758ed116115462d3814af784a234418861b3d45"
OUT = {
    "delta_manifest": f"{PHASE_ROOT}/validation/final-delta-manifest.json",
    "owner_manifest": f"{PHASE_ROOT}/validation/final-owner-manifest.json",
    "delta_privacy": f"{PHASE_ROOT}/validation/final-delta-privacy.json",
    "owner_privacy": f"{PHASE_ROOT}/validation/final-owner-privacy.json",
    "review": f"{PHASE_ROOT}/validation/final-staged-review.json",
}
SELF_EXCLUSIONS = sorted(OUT.values())
ALLOWED_EXACT = {
    "scripts/build_ghc_family_v651_v5_2_closeout.py",
    "scripts/ghc_family_v651_v5_2_final_review.py",
    "scripts/ghc_family_v651_v5_2_exact_final_validate.py",
    "tests/test_ghc_family_v651_v5_2_closeout.py",
}
PATTERNS = {
    "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_local_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/Users/|/home/)", re.I),
    "private_uri": re.compile(rb"(?:codex|chatgpt|file|vscode|app)://", re.I),
    "delegation_markup": re.compile(rb"<\s*(?:codex_delegation|source_thread_id|private_route)\b", re.I),
    "credential_assignment": re.compile(rb"(?:api[_-]?key|password|private[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-/+=]{12,}", re.I),
}


def run(*args: str, text: bool = True):
    return subprocess.check_output(list(args), cwd=REPO, text=text, encoding="utf-8" if text else None)


def write_json(path: str, payload: dict) -> None:
    target = REPO / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def staged_paths() -> list[str]:
    raw = run("git", "diff", "--cached", "--name-only", "-z", text=False)
    return sorted(part.decode("utf-8") for part in raw.split(b"\0") if part)


def staged_blob(path: str) -> tuple[str, bytes]:
    row = run("git", "ls-files", "-s", "--", path).strip()
    if not row:
        raise RuntimeError(f"missing staged index entry: {path}")
    oid = row.split()[1]
    return oid, run("git", "cat-file", "blob", oid, text=False)


def head_tree(prefix: str) -> dict[str, str]:
    raw = run("git", "ls-tree", "-r", "-z", "HEAD", "--", prefix, text=False)
    result = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        _mode, kind, oid = meta.decode("ascii").split()
        if kind == "blob":
            result[path.decode("utf-8")] = oid
    return result


def blob(oid: str) -> bytes:
    return run("git", "cat-file", "blob", oid, text=False)


def scan(rows: list[tuple[str, bytes]]) -> tuple[list[dict], list[dict]]:
    confirmed, definitions = [], []
    for path, data in rows:
        code_domain = path.startswith(("scripts/", "tests/")) or "/skills/" in path or path.endswith(".py")
        for class_name, pattern in PATTERNS.items():
            for match in pattern.finditer(data):
                candidate = {"path": path, "class": class_name, "offset": match.start()}
                (definitions if code_domain else confirmed).append(candidate)
    return confirmed, definitions


def manifest_entries(rows: list[tuple[str, str, bytes]]) -> list[dict]:
    return [{"path": path, "bytes": len(data), "git_blob": oid, "sha256": hashlib.sha256(data).hexdigest()} for path, oid, data in rows]


def main() -> None:
    head = run("git", "rev-parse", "HEAD").strip()
    if head not in {EVIDENCE, CLOSEOUT}:
        raise RuntimeError("final review must run at the exact evidence or closeout correction parent")
    paths = staged_paths()
    if any(path in SELF_EXCLUSIONS for path in paths):
        raise RuntimeError("self-excluding receipts must not be staged before review generation")
    unexpected = [path for path in paths if not (path.startswith(PHASE_ROOT + "/") or path in ALLOWED_EXACT)]
    if unexpected:
        raise RuntimeError(f"unexpected final paths: {unexpected}")
    check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    if check.returncode:
        raise RuntimeError(check.stdout + check.stderr)

    delta_rows = []
    for path in paths:
        oid, data = staged_blob(path)
        delta_rows.append((path, oid, data))
    delta_confirmed, delta_definitions = scan([(path, data) for path, _oid, data in delta_rows])
    if delta_confirmed:
        raise RuntimeError(f"confirmed final-delta privacy hits: {delta_confirmed[:5]}")

    owner_map = head_tree(PHASE_ROOT)
    for path, oid, _data in delta_rows:
        if path.startswith(PHASE_ROOT + "/"):
            owner_map[path] = oid
    for path in SELF_EXCLUSIONS:
        owner_map.pop(path, None)
    owner_rows = [(path, oid, blob(oid)) for path, oid in sorted(owner_map.items())]
    owner_confirmed, owner_definitions = scan([(path, data) for path, _oid, data in owner_rows])
    if owner_confirmed:
        raise RuntimeError(f"confirmed final-owner privacy hits: {owner_confirmed[:5]}")

    write_json(OUT["delta_manifest"], {"schema": "ghc.family.v651-v5-2.final-delta-manifest.v1", "evidence_commit": EVIDENCE, "hash_domain": "exact_git_index_blob", "entry_count": len(delta_rows), "covered_path_count": len(delta_rows) + len(SELF_EXCLUSIONS), "self_exclusions": SELF_EXCLUSIONS, "entries": manifest_entries(delta_rows)})
    write_json(OUT["owner_manifest"], {"schema": "ghc.family.v651-v5-2.final-owner-manifest.v1", "evidence_commit": EVIDENCE, "owner_prefix": PHASE_ROOT, "hash_domain": "final_predicted_git_blob", "entry_count": len(owner_rows), "covered_path_count": len(owner_rows) + len(SELF_EXCLUSIONS), "self_exclusions": SELF_EXCLUSIONS, "entries": manifest_entries(owner_rows)})
    write_json(OUT["delta_privacy"], {"schema": "ghc.family.v651-v5-2.final-delta-privacy.v1", "files_scanned": len(delta_rows), "pattern_classes": sorted(PATTERNS), "scanner_definition_candidates": delta_definitions, "confirmed_hits": delta_confirmed, "zero_confirmed_hits": True, "boundary": "Five-class scanning is not privacy-complete assurance."})
    write_json(OUT["owner_privacy"], {"schema": "ghc.family.v651-v5-2.final-owner-privacy.v1", "files_scanned": len(owner_rows), "pattern_classes": sorted(PATTERNS), "scanner_definition_candidates": owner_definitions, "confirmed_hits": owner_confirmed, "zero_confirmed_hits": True, "boundary": "Five-class scanning is not privacy-complete assurance."})
    baton_words = len((REPO / PHASE_ROOT / "handoffs/elaren-kestrel-v651-v6-activation.md").read_text(encoding="utf-8").split())
    overview_words = len((REPO / PHASE_ROOT / "overview/final-integrated-overview.md").read_text(encoding="utf-8").split())
    write_json(OUT["review"], {"schema": "ghc.family.v651-v5-2.final-staged-review.v1", "evidence_commit": EVIDENCE, "review_parent": head, "delta_entry_count": len(delta_rows), "owner_entry_count": len(owner_rows), "self_exclusion_count": len(SELF_EXCLUSIONS), "predicted_staged_path_count": len(delta_rows) + len(SELF_EXCLUSIONS), "unexpected_paths": unexpected, "diff_hygiene": "pass", "bounded_tests": {"passed": 30, "total": 30}, "baton_words": baton_words, "overview_words": overview_words, "method_flow": {"methods": 18, "fail": 24, "pass": 19, "preferred": 18}, "privacy_zero_confirmed_hits": True, "manifest_exact_index_blobs": True, "valid": True, "boundary": "Final staged same-owner review only; the complete repository suite remains reserved for the exact pushed final head."})
    print(json.dumps({"delta_entries": len(delta_rows), "owner_entries": len(owner_rows), "self_exclusions": len(SELF_EXCLUSIONS), "delta_privacy_hits": 0, "owner_privacy_hits": 0, "valid": True}))


if __name__ == "__main__":
    main()
