#!/usr/bin/env python3
"""Build exact normalized-LF Git-blob manifests for Liora v676-v4 final."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


SOURCE = "15a8eb4c7e6abc86f629af12ff29c9893e7723cb"
EVIDENCE = "c976479e91f94270f0e5cde975144865363bb618"
OWNER_PREFIX = "docs/liora-venn/v676-v4/"
FINAL_DELTA_PATH = OWNER_PREFIX + "validation/final-delta-manifest.json"
FINAL_OWNER_PATH = OWNER_PREFIX + "validation/final-owner-manifest.json"
FINAL_REVIEW_PATH = OWNER_PREFIX + "validation/final-staged-review.json"
SELF_EXCLUSIONS = [
    {"path": FINAL_DELTA_PATH, "reason": "self-referential final-delta manifest"},
    {"path": FINAL_OWNER_PATH, "reason": "self-referential final-owner manifest"},
    {"path": FINAL_REVIEW_PATH, "reason": "self-referential final staged review"},
]
ALLOWED_SCRIPT_RE = re.compile(r"^scripts/(?:build_ghc_family|ghc_family)_liora_venn_v676_v4_.*\.py$")
ALLOWED_TEST_RE = re.compile(r"^tests/test_ghc_family_liora_venn_v676_v4_.*\.py$")
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
        mode, oid, stage = left.split()
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
        stderr = self.proc.stderr.read().decode("utf-8", "replace") if self.proc.stderr else ""
        code = self.proc.wait()
        if code:
            raise RuntimeError(stderr)


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
    if git(repo, "rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("final manifests must be built at the immutable evidence head before final commit")
    staged = sorted(path for path in git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR", EVIDENCE, "--").splitlines() if path)
    exclusions = {row["path"] for row in SELF_EXCLUSIONS}
    staged_input = sorted(path for path in staged if path not in exclusions)
    unexpected = sorted(path for path in staged if not allowed(path))
    if unexpected:
        raise SystemExit(f"unexpected staged paths: {unexpected!r}")
    required_final_paths = {
        OWNER_PREFIX + "final/phase-truth.json",
        OWNER_PREFIX + "closeout/content-seal.json",
        OWNER_PREFIX + "handoffs/tamar-vey-v676-v5-activation-candidate.md",
        "scripts/build_ghc_family_liora_venn_v676_v4_final.py",
        "scripts/ghc_family_liora_venn_v676_v4_final_validator.py",
        "tests/test_ghc_family_liora_venn_v676_v4_final.py",
    }
    if not required_final_paths.issubset(staged_input):
        raise SystemExit(f"missing required final staged paths: {sorted(required_final_paths - set(staged_input))!r}")

    committed_owner = {
        path for path in git(repo, "diff", "--name-only", "--diff-filter=ACMR", SOURCE, EVIDENCE, "--").splitlines()
        if path and allowed(path)
    }
    owner_paths = sorted((committed_owner | set(staged)) - exclusions)
    index = index_map(repo)
    missing = sorted(path for path in owner_paths if path not in index)
    if missing:
        raise SystemExit(f"owner paths missing from index: {missing[:10]!r}")
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
                scanner_metadata = path.endswith(".py") or path.endswith("-staged-review.json") or path.endswith("privacy-adjudication.json")
                adjudication = "scanner_definition_or_adjudication_metadata" if scanner_metadata else "confirmed_payload_hit"
                candidates.append({"path": path, "category": category, "adjudication": adjudication})
    confirmed = [row for row in candidates if row["adjudication"] == "confirmed_payload_hit"]
    blobs.close()
    if confirmed:
        raise SystemExit(f"confirmed privacy or raw-identifier payload hits: {confirmed!r}")

    validation = repo / OWNER_PREFIX / "validation"
    common = {
        "owner": "Liora Venn",
        "phase": "v676-v4-final",
        "source": SOURCE,
        "evidence": EVIDENCE,
        "normalization_domain": "Git index bytes normalized CRLF and CR to LF for SHA-256; Git blob OID uses exact index bytes",
        "declared_exclusions": SELF_EXCLUSIONS,
    }
    dump(
        validation / "final-delta-manifest.json",
        {
            **common,
            "manifest_kind": "precommit_final_delta_git_blob_manifest",
            "range_start": EVIDENCE,
            "entry_count": len(delta_entries),
            "entries": delta_entries,
        },
    )
    dump(
        validation / "final-owner-manifest.json",
        {
            **common,
            "manifest_kind": "precommit_source_to_final_owner_git_blob_manifest",
            "range_start": SOURCE,
            "entry_count": len(owner_entries),
            "entries": owner_entries,
        },
    )
    dump(
        validation / "final-staged-review.json",
        {
            "source": SOURCE,
            "evidence": EVIDENCE,
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
            "status": "VALID_PRECOMMIT_FINAL_STAGED_REVIEW",
        },
    )


if __name__ == "__main__":
    main()
