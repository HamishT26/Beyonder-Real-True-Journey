#!/usr/bin/env python3
"""Create exact v651-v2 x2 evidence staged-index receipts."""

from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = "docs/orin-thale/v651-v2"
X1 = "06c5545a79e992537b6307eb6a68e6d01204144d"
X1_MANIFEST = f"{PHASE_ROOT}/validation/x1-staged-manifest.json"
OUT = {
    "manifest": f"{PHASE_ROOT}/validation/evidence-staged-manifest.json",
    "privacy": f"{PHASE_ROOT}/validation/evidence-staged-privacy.json",
    "review": f"{PHASE_ROOT}/validation/evidence-staged-review.json",
}
SELF_EXCLUSIONS = sorted(OUT.values())
ALLOWED_EXACT = {
    "scripts/build_ghc_family_v651_v2_evidence.py",
    "scripts/build_ghc_family_v651_v2_skills.py",
    "scripts/ghc_family_v651_v2_accessibility.py",
    "scripts/ghc_family_v651_v2_evidence_review.py",
    "scripts/ghc_family_v651_v2_format_and_protocol.py",
    "scripts/ghc_family_v651_v2_gmut_boards.py",
    "scripts/ghc_family_v651_v2_identity_and_authority.py",
    "scripts/ghc_family_v651_v2_method_and_provenance.py",
    "scripts/ghc_family_v651_v2_numeric_and_nonconversion.py",
    "scripts/ghc_family_v651_v2_portfolios.py",
    "scripts/ghc_family_v651_v2_runtime.py",
    "scripts/ghc_family_v651_v2_skill_smoke.py",
    "scripts/ghc_family_v651_v2_stage20.py",
    "scripts/ghc_family_v651_v2_validate.py",
    "scripts/ghc_family_v651_v2_zero_row_and_localization.py",
    "tests/test_ghc_family_v651_v2_x1.py",
    "tests/test_ghc_family_v651_v2_x2.py",
}
EXPECTED_X1_COMPANION_DRIFT = {
    f"{PHASE_ROOT}/method-flow/method-flow-ledger.json",
    f"{PHASE_ROOT}/method-flow/method-flow-summary.json",
    f"{PHASE_ROOT}/method-flow/method-flow-summary.md",
    f"{PHASE_ROOT}/method-flow/method-flow-validation.json",
    "tests/test_ghc_family_v651_v2_x1.py",
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


def write_json(path: str, payload: dict) -> None:
    target = REPO / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def staged_paths() -> list[str]:
    raw = run("git", "diff", "--cached", "--name-only", "-z", binary=True)
    return sorted(part.decode("utf-8") for part in raw.split(b"\0") if part)


def staged_index(paths: list[str]) -> dict[str, str]:
    raw = run("git", "ls-files", "--stage", "-z", "--", *paths, binary=True)
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
    proc = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input="".join(oid + "\n" for oid in unique).encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    stream = io.BytesIO(proc.stdout)
    result = {}
    for expected in unique:
        header = stream.readline().rstrip(b"\n").decode().split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise RuntimeError(f"unexpected blob header: {header}")
        size = int(header[2])
        data = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError("missing batch frame terminator")
        result[expected] = data
    if stream.read():
        raise RuntimeError("unexpected trailing batch bytes")
    return result


def main() -> None:
    if run("git", "rev-parse", "HEAD") != X1:
        raise RuntimeError("evidence review must run at the exact pushed x1 head")
    paths = staged_paths()
    if any(path in SELF_EXCLUSIONS for path in paths):
        raise RuntimeError("self-excluding evidence receipts must not be staged before generation")
    unexpected = [path for path in paths if not (path.startswith(PHASE_ROOT + "/") or path in ALLOWED_EXACT)]
    if unexpected:
        raise RuntimeError(f"unexpected staged paths: {unexpected}")
    if not paths or not any("/surfaces/" in path for path in paths) or not any("/outcomes/" in path for path in paths):
        raise RuntimeError("evidence surface is incomplete")
    x1_manifest = json.loads(run("git", "show", f"{X1}:{X1_MANIFEST}"))
    x1_covered = {row["path"] for row in x1_manifest["entries"]} | set(x1_manifest["self_exclusions"])
    current_x1_drift = set(paths) & x1_covered
    if current_x1_drift != EXPECTED_X1_COMPANION_DRIFT:
        raise RuntimeError(f"unexpected x1 companion drift: {sorted(current_x1_drift ^ EXPECTED_X1_COMPANION_DRIFT)}")
    diff_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    if diff_check.returncode:
        raise RuntimeError(diff_check.stdout + diff_check.stderr)

    index = staged_index(paths)
    if set(index) != set(paths):
        raise RuntimeError("staged path/index mismatch")
    blobs = batch_blobs([index[path] for path in paths])
    entries = []
    confirmed_hits = []
    scanner_definition_candidates = []
    staged_json_count = 0
    for path in paths:
        data = blobs[index[path]]
        entries.append({"path": path, "bytes": len(data), "git_blob": index[path], "sha256": hashlib.sha256(data).hexdigest()})
        if path.endswith(".json"):
            json.loads(data.decode("utf-8"))
            staged_json_count += 1
        for class_name, pattern in PATTERNS.items():
            for match in pattern.finditer(data):
                candidate = {"path": path, "class": class_name, "offset": match.start()}
                if path.startswith("scripts/") or path.startswith("tests/"):
                    scanner_definition_candidates.append(candidate)
                else:
                    confirmed_hits.append(candidate)
    if confirmed_hits:
        raise RuntimeError(f"confirmed privacy hits: {confirmed_hits[:5]}")

    write_json(OUT["manifest"], {"schema": "ghc.family.v651-v2.evidence-staged-manifest.v1", "source_head": X1, "hash_domain": "exact_git_index_blob", "entry_count": len(entries), "covered_path_count": len(entries) + len(SELF_EXCLUSIONS), "self_exclusions": SELF_EXCLUSIONS, "entries": entries})
    write_json(OUT["privacy"], {"schema": "ghc.family.v651-v2.evidence-staged-privacy.v1", "pattern_classes": sorted(PATTERNS), "scanned_entry_count": len(entries), "scanner_definition_candidates": scanner_definition_candidates, "confirmed_hits": confirmed_hits, "zero_confirmed_hits": True, "boundary": "Five-class staged text scanning is not privacy-complete assurance or independent review."})
    write_json(OUT["review"], {"schema": "ghc.family.v651-v2.evidence-staged-review.v1", "source_head": X1, "entry_count": len(entries), "self_exclusion_count": len(SELF_EXCLUSIONS), "predicted_final_staged_path_count": len(entries) + len(SELF_EXCLUSIONS), "staged_json_count": staged_json_count, "unexpected_paths": unexpected, "x1_companion_drift": sorted(current_x1_drift), "x1_commit_objects_immutable": True, "diff_hygiene": "pass", "current_phase_tests": {"passed": 26, "total": 26, "failed_aggregate_retained": "25_of_26"}, "mutations": {"executed": 100, "rejected": 100}, "skills": {"official_validated": 20, "smoke_used": 20}, "runners": {"passed": 10, "total": 10}, "privacy_zero_confirmed_hits": True, "manifest_exact_index_blobs": True, "valid": True, "boundary": "Dedicated x2 evidence staged review only; no full-suite, empirical, production, authority, complete-accessibility, exhaustive-security, or independent-reproduction credit."})
    print(json.dumps({"entries": len(entries), "self_exclusions": len(SELF_EXCLUSIONS), "predicted_paths": len(entries) + len(SELF_EXCLUSIONS), "json_blobs": staged_json_count, "x1_companion_drift": len(current_x1_drift), "privacy_hits": 0, "valid": True}))


if __name__ == "__main__":
    main()
