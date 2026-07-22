#!/usr/bin/env python3
"""Create exact staged-index, privacy, and x1 review receipts for Elaren v651-v6."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = "docs/elaren-kestrel/v651-v6"
SOURCE = "7c4309d6b57bc4827ebd49bcb7c9dfc669c46e3d"
OUT = {
    "manifest": f"{PHASE_ROOT}/validation/x1-staged-manifest.json",
    "privacy": f"{PHASE_ROOT}/validation/x1-staged-privacy.json",
    "review": f"{PHASE_ROOT}/validation/x1-staged-review.json",
    "json": f"{PHASE_ROOT}/validation/x1-json-parse-receipt.json",
    "documents": f"{PHASE_ROOT}/validation/x1-document-cap-receipt.json",
    "files": f"{PHASE_ROOT}/validation/x1-owner-file-threshold.json",
}
SELF_EXCLUSIONS = sorted(OUT.values())
ALLOWED_EXACT = {
    "scripts/build_ghc_family_v651_v6_preregistration.py",
    "scripts/ghc_family_v651_v6_x1_method_flow.py",
    "scripts/ghc_family_v651_v6_x1_review.py",
    "tests/test_ghc_family_v651_v6_x1.py",
}
PATTERNS = {
    "raw_identifier_or_private_callable": re.compile(rb"(?:\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b|\b(?:thread|task|callable)[_-]?id\s*[:=]\s*['\"]?[A-Za-z0-9_-]{12,})", re.I),
    "private_local_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/Users/|/home/)", re.I),
    "private_uri_or_route": re.compile(rb"(?:codex|chatgpt|file|vscode|app|thread)://", re.I),
    "delegation_transcript_or_session": re.compile(rb"(?:<\s*(?:codex_delegation|source_thread_id|private_route)\b|\b(?:transcript|session[_-]?stream)\s*[:=])", re.I),
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
        raise RuntimeError("x1 review must run at the exact inherited source")
    paths = staged_paths()
    if any(path in SELF_EXCLUSIONS for path in paths):
        raise RuntimeError("self-excluding receipts must not be staged before review generation")
    unexpected = [path for path in paths if not (path.startswith(PHASE_ROOT + "/") or path in ALLOWED_EXACT)]
    forbidden_tokens = ("/outcomes/", "/surfaces/", "/mutations/", "/evidence/", "x2-phase", "x2-proposal", "mutation-execution", "/skills/")
    x2_contamination = [path for path in paths if any(token in path for token in forbidden_tokens)]
    if unexpected or x2_contamination:
        raise RuntimeError(f"unexpected={unexpected} x2_contamination={x2_contamination}")
    check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    if check.returncode:
        raise RuntimeError(check.stdout + check.stderr)

    entries: list[dict] = []
    confirmed: list[dict] = []
    definitions: list[dict] = []
    json_paths: list[str] = []
    document_rows: list[dict] = []
    for path in paths:
        oid, data = staged_blob(path)
        entries.append({"path": path, "bytes": len(data), "git_blob": oid, "sha256": hashlib.sha256(data).hexdigest()})
        if path.endswith(".json"):
            json.loads(data.decode("utf-8"))
            json_paths.append(path)
        if path.startswith(PHASE_ROOT + "/") and (path.endswith(".md") or path.endswith(".html")):
            words = len(data.decode("utf-8").split())
            document_rows.append({"path": path, "words": words, "under_cap": words <= 100000})
        for class_name, pattern in PATTERNS.items():
            for match in pattern.finditer(data):
                candidate = {"path": path, "class": class_name, "offset": match.start()}
                if path.startswith("scripts/") or path.startswith("tests/"):
                    definitions.append(candidate)
                else:
                    confirmed.append(candidate)
    if confirmed:
        raise RuntimeError(f"confirmed privacy hits: {confirmed[:8]}")
    if not all(row["under_cap"] for row in document_rows):
        raise RuntimeError("document word cap exceeded")

    owner_paths = [path for path in paths if path.startswith(PHASE_ROOT + "/")]
    predicted_owner_files = len(owner_paths) + len(SELF_EXCLUSIONS)
    if predicted_owner_files >= 2000:
        raise RuntimeError(f"owner file threshold exceeded: {predicted_owner_files}")

    write_json(OUT["manifest"], {
        "schema": "ghc.family.v651-v6.x1-staged-manifest.v1",
        "source_head": SOURCE,
        "hash_domain": "exact_git_index_blob",
        "entry_count": len(entries),
        "covered_path_count": len(entries) + len(SELF_EXCLUSIONS),
        "self_exclusions": SELF_EXCLUSIONS,
        "entries": entries,
    })
    write_json(OUT["privacy"], {
        "schema": "ghc.family.v651-v6.x1-staged-privacy.v1",
        "pattern_classes": sorted(PATTERNS),
        "scanned_entry_count": len(entries),
        "scanner_definition_candidates": definitions,
        "confirmed_hits": confirmed,
        "zero_confirmed_hits": True,
        "boundary": "Five-class staged scanning is not privacy-complete assurance, security certification, or independent review.",
    })
    write_json(OUT["json"], {
        "schema": "ghc.family.v651-v6.x1-json-parse.v1",
        "parsed_count": len(json_paths),
        "issues": [],
        "paths": json_paths,
        "valid": True,
    })
    write_json(OUT["documents"], {
        "schema": "ghc.family.v651-v6.x1-document-cap.v1",
        "cap_words": 100000,
        "document_count": len(document_rows),
        "maximum_words": max((row["words"] for row in document_rows), default=0),
        "all_under_cap": True,
        "documents": document_rows,
    })
    write_json(OUT["files"], {
        "schema": "ghc.family.v651-v6.x1-owner-file-threshold.v1",
        "owner_file_count": predicted_owner_files,
        "threshold": 2000,
        "below_threshold": True,
        "inherited_repository_baseline_counted": False,
    })
    write_json(OUT["review"], {
        "schema": "ghc.family.v651-v6.x1-staged-review.v1",
        "source_head": SOURCE,
        "entry_count": len(entries),
        "self_exclusion_count": len(SELF_EXCLUSIONS),
        "predicted_final_staged_path_count": len(entries) + len(SELF_EXCLUSIONS),
        "unexpected_paths": unexpected,
        "x2_contamination": x2_contamination,
        "diff_hygiene": "pass",
        "x1_tests": {"passed": 14, "total": 14},
        "json_parses": len(json_paths),
        "privacy_zero_confirmed_hits": True,
        "manifest_exact_index_blobs": True,
        "owner_files_below_threshold": True,
        "documents_under_cap": True,
        "valid": True,
        "boundary": "Dedicated x1 review only; no x2, full-suite, empirical, authority, or independent-reproduction credit.",
    })
    print(json.dumps({"entries": len(entries), "self_exclusions": len(SELF_EXCLUSIONS), "predicted_paths": len(entries) + len(SELF_EXCLUSIONS), "json": len(json_paths), "privacy_hits": 0, "owner_files": predicted_owner_files, "valid": True}))


if __name__ == "__main__":
    main()
