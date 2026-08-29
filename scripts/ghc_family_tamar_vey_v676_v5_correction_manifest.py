#!/usr/bin/env python3
"""Build additive correction manifests from the staged Tamar v676-v5 index."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


SOURCE = "ce97f35c2351c8daef6f48b4dc1c60928e1fc1be"
FIRST_FINAL = "58a5fa6edeafaf2c1e3048036e131f857d7996d3"
OWNER_PREFIX = "docs/tamar-vey/v676-v5/"
DELTA_PATH = OWNER_PREFIX + "validation/correction-delta-manifest.json"
OWNER_PATH = OWNER_PREFIX + "validation/correction-owner-manifest.json"
REVIEW_PATH = OWNER_PREFIX + "validation/correction-staged-review.json"
SELF_EXCLUSIONS = [
    {"path": DELTA_PATH, "reason": "self-referential correction-delta manifest"},
    {"path": OWNER_PATH, "reason": "self-referential correction-owner manifest"},
    {"path": REVIEW_PATH, "reason": "self-referential correction staged review"},
]
PRIVACY_EXCLUSIONS = {
    DELTA_PATH,
    OWNER_PATH,
    REVIEW_PATH,
    OWNER_PREFIX + "validation/final-delta-manifest.json",
    OWNER_PREFIX + "validation/final-owner-manifest.json",
    OWNER_PREFIX + "validation/final-staged-review.json",
}
ALLOWED_SCRIPT_RE = re.compile(r"^scripts/(?:build_ghc_family|ghc_family)_tamar_vey_v676_v5_.*\.py$")
ALLOWED_TEST_RE = re.compile(r"^tests/test_ghc_family_tamar_vey_v676_v5_.*\.py$")
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(rb"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(rb"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(rb"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(rb"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
}


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def allowed(path: str) -> bool:
    return path.startswith(OWNER_PREFIX) or bool(ALLOWED_SCRIPT_RE.fullmatch(path)) or bool(ALLOWED_TEST_RE.fullmatch(path))


def normalized(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def index_map(repo: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in git(repo, "ls-files", "-s").splitlines():
        if not line:
            continue
        left, path = line.split("\t", 1)
        _mode, oid, stage = left.split()
        if stage == "0":
            result[path] = oid
    return result


def blob(repo: Path, oid: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), "cat-file", "blob", oid])


def entry(repo: Path, path: str, oid: str) -> dict[str, Any]:
    raw = blob(repo, oid)
    norm = normalized(raw)
    return {
        "path": path,
        "git_blob_oid": oid,
        "bytes": len(raw),
        "normalized_lf_bytes": len(norm),
        "sha256_normalized_lf": hashlib.sha256(norm).hexdigest(),
    }


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    if git(repo, "rev-parse", "HEAD") != FIRST_FINAL:
        raise SystemExit("correction manifests must be built at the retained first final before the correction commit")
    staged = sorted(path for path in git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR", FIRST_FINAL, "--").splitlines() if path)
    exclusions = {row["path"] for row in SELF_EXCLUSIONS}
    staged_input = sorted(path for path in staged if path not in exclusions)
    unexpected = sorted(path for path in staged if not allowed(path))
    if unexpected:
        raise SystemExit(f"unexpected staged correction paths: {unexpected!r}")
    required = {
        OWNER_PREFIX + "correction/correction-receipt.json",
        OWNER_PREFIX + "correction/phase-truth.json",
        OWNER_PREFIX + "correction/method-flow-overlay.json",
        OWNER_PREFIX + "correction/content-seal.json",
        OWNER_PREFIX + "handoffs/elowen-cairn-v676-v6-activation-candidate-corrected.md",
        OWNER_PREFIX + "orchestration/terminal-route-hold-corrected.json",
        "scripts/ghc_family_tamar_vey_v676_v5_final_validator.py",
        "tests/test_ghc_family_tamar_vey_v676_v5_correction.py",
    }
    if not required.issubset(staged_input):
        raise SystemExit(f"missing required correction paths: {sorted(required - set(staged_input))!r}")
    owner_committed = {
        path for path in git(repo, "diff", "--name-only", "--diff-filter=ACMR", SOURCE, FIRST_FINAL, "--").splitlines()
        if path and allowed(path)
    }
    owner_paths = sorted((owner_committed | set(staged)) - exclusions)
    index = index_map(repo)
    missing = sorted(path for path in owner_paths if path not in index)
    if missing:
        raise SystemExit(f"owner paths missing from index: {missing[:10]!r}")
    delta_entries = [entry(repo, path, index[path]) for path in staged_input]
    owner_entries = [entry(repo, path, index[path]) for path in owner_paths]
    candidates = []
    for path in owner_paths:
        if path in PRIVACY_EXCLUSIONS or not path.endswith((".py", ".json", ".md", ".html", ".txt", ".yaml", ".yml")):
            continue
        raw = normalized(blob(repo, index[path]))
        for category, pattern in PRIVACY_PATTERNS.items():
            if pattern.search(raw):
                scanner_metadata = path.endswith(".py") or path.endswith("-staged-review.json") or path.endswith("privacy-adjudication.json")
                candidates.append({
                    "path": path,
                    "category": category,
                    "adjudication": "scanner_definition_or_adjudication_metadata" if scanner_metadata else "confirmed_payload_hit",
                })
    confirmed = [row for row in candidates if row["adjudication"] == "confirmed_payload_hit"]
    if confirmed:
        raise SystemExit(f"confirmed privacy or raw-identifier correction hits: {confirmed!r}")
    validation = repo / OWNER_PREFIX / "validation"
    common = {
        "owner": "Tamar Vey",
        "phase": "v676-v5-additive-correction",
        "source": SOURCE,
        "first_final": FIRST_FINAL,
        "normalization_domain": "Git index bytes normalized CRLF and CR to LF for SHA-256; Git blob OID uses exact index bytes",
        "declared_exclusions": SELF_EXCLUSIONS,
    }
    dump(validation / "correction-delta-manifest.json", {
        **common,
        "manifest_kind": "precommit_additive_correction_delta_git_blob_manifest",
        "range_start": FIRST_FINAL,
        "entry_count": len(delta_entries),
        "entries": delta_entries,
    })
    dump(validation / "correction-owner-manifest.json", {
        **common,
        "manifest_kind": "precommit_source_to_corrected_final_owner_git_blob_manifest",
        "range_start": SOURCE,
        "entry_count": len(owner_entries),
        "entries": owner_entries,
    })
    dump(validation / "correction-staged-review.json", {
        "source": SOURCE,
        "first_final": FIRST_FINAL,
        "staged_input_count": len(staged_input),
        "owner_input_count": len(owner_paths),
        "declared_self_exclusions": SELF_EXCLUSIONS,
        "unexpected_paths": unexpected,
        "privacy_classes": sorted(PRIVACY_PATTERNS),
        "privacy_candidates": candidates,
        "privacy_candidate_count": len(candidates),
        "confirmed_five_class_privacy_or_raw_identifier_hits": 0,
        "exact_staged_review": True,
        "diff_hygiene_required": True,
        "status": "VALID_PRECOMMIT_ADDITIVE_CORRECTION_STAGED_REVIEW",
    })
    print(json.dumps({
        "status": "VALID_PRECOMMIT_ADDITIVE_CORRECTION_MANIFESTS",
        "delta_entries": len(delta_entries),
        "owner_entries": len(owner_entries),
        "privacy_candidates": len(candidates),
        "confirmed_hits": 0,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
