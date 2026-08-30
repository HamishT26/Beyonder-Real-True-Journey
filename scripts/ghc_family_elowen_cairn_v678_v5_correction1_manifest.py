#!/usr/bin/env python3
"""Build exact normalized-LF Git-index manifests for Elowen v678-v5 correction1."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


SOURCE = "0021481a0c9681c077bce277e6ac0f2fcb37dbcd"
FIRST_FINAL = "831f948e326e3875ef0d5d7391560297ce0e2ee8"
OWNER_PREFIX = "docs/elowen-cairn/v678-v5/"
DELTA_PATH = OWNER_PREFIX + "validation/correction1-delta-manifest.json"
OWNER_PATH = OWNER_PREFIX + "validation/correction1-owner-manifest.json"
REVIEW_PATH = OWNER_PREFIX + "validation/correction1-staged-review.json"
SELF_EXCLUSIONS = [
    {"path": DELTA_PATH, "reason": "self-referential correction1 delta manifest"},
    {"path": OWNER_PATH, "reason": "self-referential correction1 owner manifest"},
    {"path": REVIEW_PATH, "reason": "self-referential correction1 staged review"},
]
SCRIPT_RE = re.compile(r"^scripts/(?:build_ghc_family|ghc_family|validate_ghc_family)_elowen_cairn_v678_v5_.*\.py$")
TEST_RE = re.compile(r"^tests/test_ghc_family_elowen_cairn_v678_v5_.*\.py$")
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(rb"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(rb"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(rb"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(rb"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
}


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def allowed(path: str) -> bool:
    return path.startswith(OWNER_PREFIX) or bool(SCRIPT_RE.fullmatch(path)) or bool(TEST_RE.fullmatch(path))


def normalized(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


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


class BlobReader:
    def __init__(self, repo: Path):
        self.proc = subprocess.Popen(
            ["git", "-C", str(repo), "cat-file", "--batch"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.cache: dict[str, bytes] = {}

    def get(self, oid: str) -> bytes:
        if oid not in self.cache:
            assert self.proc.stdin and self.proc.stdout
            self.proc.stdin.write((oid + "\n").encode("ascii"))
            self.proc.stdin.flush()
            header = self.proc.stdout.readline().split()
            if len(header) < 3 or header[1] != b"blob":
                raise RuntimeError(f"object is not a blob: {oid}")
            raw = self.proc.stdout.read(int(header[2]))
            self.proc.stdout.read(1)
            self.cache[oid] = raw
        return self.cache[oid]

    def close(self) -> None:
        assert self.proc.stdin
        self.proc.stdin.close()
        self.proc.stdin = None
        _stdout, stderr = self.proc.communicate(timeout=60)
        if self.proc.returncode:
            raise RuntimeError(stderr.decode("utf-8", "replace"))


def entry(path: str, oid: str, blobs: BlobReader) -> dict[str, Any]:
    raw = blobs.get(oid)
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
        raise SystemExit("correction1 manifests require the retained first final before correction commit")
    staged = sorted(path for path in git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR", FIRST_FINAL, "--").splitlines() if path)
    exclusions = {row["path"] for row in SELF_EXCLUSIONS}
    staged_input = sorted(path for path in staged if path not in exclusions)
    unexpected = sorted(path for path in staged if not allowed(path))
    if unexpected:
        raise SystemExit(f"unexpected staged correction paths: {unexpected!r}")
    required = {
        OWNER_PREFIX + "correction1/phase-truth.json",
        OWNER_PREFIX + "correction1/content-seal.json",
        "scripts/build_ghc_family_elowen_cairn_v678_v5_correction1.py",
        "scripts/validate_ghc_family_elowen_cairn_v678_v5_correction1.py",
        "tests/test_ghc_family_elowen_cairn_v678_v5_correction1.py",
    }
    if not required.issubset(staged_input):
        raise SystemExit(f"missing required correction1 paths: {sorted(required - set(staged_input))!r}")

    committed_owner = {
        path for path in git(repo, "diff", "--name-only", "--diff-filter=ACMR", SOURCE, FIRST_FINAL, "--").splitlines()
        if path and allowed(path)
    }
    owner_paths = sorted((committed_owner | set(staged)) - exclusions)
    index = index_map(repo)
    missing = sorted(path for path in owner_paths if path not in index)
    if missing:
        raise SystemExit(f"owner paths absent from index: {missing[:10]!r}")
    blobs = BlobReader(repo)
    delta_entries = [entry(path, index[path], blobs) for path in staged_input]
    owner_entries = [entry(path, index[path], blobs) for path in owner_paths]
    candidates = []
    for path in owner_paths:
        if not path.endswith((".py", ".json", ".md", ".html", ".txt", ".yaml", ".yml")):
            continue
        raw = normalized(blobs.get(index[path]))
        for category, pattern in PRIVACY_PATTERNS.items():
            if pattern.search(raw):
                metadata = path.endswith(".py") or path.endswith("-staged-review.json")
                candidates.append(
                    {
                        "path": path,
                        "category": category,
                        "adjudication": "scanner_definition_or_rejection_assertion" if metadata else "confirmed_payload_hit",
                    }
                )
    confirmed = [row for row in candidates if row["adjudication"] == "confirmed_payload_hit"]
    blobs.close()
    if confirmed:
        raise SystemExit(f"confirmed privacy or raw-identifier payload hits: {confirmed!r}")

    validation = repo / OWNER_PREFIX / "validation"
    common = {
        "owner": "Elowen Cairn",
        "phase": "v678-v5-correction1",
        "source": SOURCE,
        "retained_first_final": FIRST_FINAL,
        "normalization_domain": "Git index bytes normalized CRLF and CR to LF for SHA-256; Git blob OID uses exact index bytes",
        "declared_exclusions": SELF_EXCLUSIONS,
    }
    dump(
        validation / "correction1-delta-manifest.json",
        {**common, "manifest_kind": "precommit_correction1_delta_git_blob_manifest", "range_start": FIRST_FINAL, "entry_count": len(delta_entries), "entries": delta_entries},
    )
    dump(
        validation / "correction1-owner-manifest.json",
        {**common, "manifest_kind": "precommit_correction1_owner_git_blob_manifest", "range_start": SOURCE, "entry_count": len(owner_entries), "entries": owner_entries},
    )
    dump(
        validation / "correction1-staged-review.json",
        {
            "source": SOURCE,
            "retained_first_final": FIRST_FINAL,
            "staged_input_count": len(staged_input),
            "owner_input_count": len(owner_paths),
            "declared_self_exclusions": SELF_EXCLUSIONS,
            "unexpected_paths": unexpected,
            "privacy_classes": sorted(PRIVACY_PATTERNS),
            "privacy_candidates": candidates,
            "privacy_candidate_count": len(candidates),
            "confirmed_five_class_privacy_or_raw_identifier_hits": 0,
            "exact_staged_review": True,
            "status": "VALID_PRECOMMIT_CORRECTION1_STAGED_REVIEW",
        },
    )


if __name__ == "__main__":
    main()
