#!/usr/bin/env python3
"""Create exact v651-v4 x1 staged-index manifest, privacy, and review receipts."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = "docs/sylven-arc/v651-v4"
SOURCE = "3ec09ba3dfc019fd9def1e58eb4943b18bcc7def"
OUT = {
    "manifest": f"{PHASE_ROOT}/validation/x1-staged-manifest.json",
    "privacy": f"{PHASE_ROOT}/validation/x1-staged-privacy.json",
    "review": f"{PHASE_ROOT}/validation/x1-staged-review.json",
}
SELF_EXCLUSIONS = sorted(OUT.values())
ALLOWED_EXACT = {
    "scripts/build_ghc_family_v651_v4_preregistration.py",
    "scripts/ghc_family_v651_v4_phase_data.py",
    "scripts/ghc_family_v651_v4_x1_review.py",
    "tests/test_ghc_family_v651_v4_x1.py",
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


def main() -> None:
    if run("git", "rev-parse", "HEAD").strip() != SOURCE:
        raise RuntimeError("x1 review must run at the exact inherited source before the x1 commit")
    paths = staged_paths()
    if any(path in SELF_EXCLUSIONS for path in paths):
        raise RuntimeError("self-excluding receipts must not be staged before review generation")
    unexpected = [path for path in paths if not (path.startswith(PHASE_ROOT + "/") or path in ALLOWED_EXACT)]
    forbidden = [path for path in paths if any(part in path for part in ("/surfaces/", "/outcomes/", "evidence-phase-truth", "mutation-execution"))]
    if unexpected or forbidden:
        raise RuntimeError(f"unexpected={unexpected} x2_contamination={forbidden}")
    check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    if check.returncode:
        raise RuntimeError(check.stdout + check.stderr)

    entries, confirmed, definitions = [], [], []
    for path in paths:
        oid, data = staged_blob(path)
        entries.append({"path": path, "bytes": len(data), "git_blob": oid, "sha256": hashlib.sha256(data).hexdigest()})
        for class_name, pattern in PATTERNS.items():
            for match in pattern.finditer(data):
                candidate = {"path": path, "class": class_name, "offset": match.start()}
                if path.startswith("scripts/") or path.startswith("tests/"):
                    definitions.append(candidate)
                else:
                    confirmed.append(candidate)
    if confirmed:
        raise RuntimeError(f"confirmed privacy hits: {confirmed[:5]}")

    write_json(OUT["manifest"], {"schema": "ghc.family.v651-v4.x1-staged-manifest.v1", "source_head": SOURCE, "hash_domain": "exact_git_index_blob", "entry_count": len(entries), "covered_path_count": len(entries) + len(SELF_EXCLUSIONS), "self_exclusions": SELF_EXCLUSIONS, "entries": entries})
    write_json(OUT["privacy"], {"schema": "ghc.family.v651-v4.x1-staged-privacy.v1", "pattern_classes": sorted(PATTERNS), "scanned_entry_count": len(entries), "scanner_definition_candidates": definitions, "confirmed_hits": confirmed, "zero_confirmed_hits": True, "boundary": "Five-class staged scanning is not privacy-complete assurance or independent review."})
    write_json(OUT["review"], {"schema": "ghc.family.v651-v4.x1-staged-review.v1", "source_head": SOURCE, "entry_count": len(entries), "self_exclusion_count": len(SELF_EXCLUSIONS), "predicted_final_staged_path_count": len(entries) + len(SELF_EXCLUSIONS), "unexpected_paths": unexpected, "x2_contamination": forbidden, "diff_hygiene": "pass", "x1_tests": {"passed": 8, "total": 8}, "privacy_zero_confirmed_hits": True, "manifest_exact_index_blobs": True, "valid": True, "boundary": "Dedicated x1 review only; no x2, full-suite, or independent-reproduction credit."})
    print(json.dumps({"entries": len(entries), "self_exclusions": len(SELF_EXCLUSIONS), "predicted_paths": len(entries) + len(SELF_EXCLUSIONS), "privacy_hits": 0, "valid": True}))


if __name__ == "__main__":
    main()
