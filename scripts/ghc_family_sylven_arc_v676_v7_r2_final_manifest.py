#!/usr/bin/env python3
"""Build exact final-delta/owner manifests, staged review, and content seal."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


SOURCE = "e66201e9efd19cb3fc98baf672ea4df440758616"
X1_HEAD = "82c5a8a45af8abcb17df5c793853be6fdc97c8ee"
EVIDENCE_HEAD = "b22eebdc9743f49d758b10e0f3577f21049f8143"
ROOT = "docs/sylven-arc/v676-v7-r2"
FINAL_ROOT = f"{ROOT}/final"
DELTA_MANIFEST = f"{ROOT}/validation/final-delta-manifest.json"
OWNER_MANIFEST = f"{ROOT}/validation/final-owner-manifest.json"
STAGED_REVIEW = f"{ROOT}/validation/final-staged-review.json"
CONTENT_SEAL = f"{FINAL_ROOT}/content-seal.json"
SELF_EXCLUSIONS = {DELTA_MANIFEST, OWNER_MANIFEST, STAGED_REVIEW, CONTENT_SEAL}
CODE_PATHS = {
    "scripts/build_ghc_family_sylven_arc_v676_v7_r2_final.py",
    "scripts/ghc_family_sylven_arc_v676_v7_r2_canonical.py",
    "scripts/ghc_family_sylven_arc_v676_v7_r2_final_manifest.py",
    "tests/test_ghc_family_sylven_arc_v676_v7_r2_final.py",
}
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(r"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
}


def git(repo: Path, *args: str, binary: bool = False):
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
        encoding=None if binary else "utf-8",
    )
    return result.stdout if binary else result.stdout.strip()


def normalize(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def working_bytes(repo: Path, relative: str) -> bytes:
    return (repo / relative).read_bytes()


def head_bytes(repo: Path, relative: str) -> bytes:
    return git(repo, "show", f"HEAD:{relative}", binary=True)


def entry(relative: str, raw: bytes) -> dict[str, object]:
    return {
        "path": relative,
        "bytes": len(raw),
        "sha256_normalized_lf": hashlib.sha256(normalize(raw)).hexdigest(),
    }


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def definition_or_fixture(relative: str) -> bool:
    return (
        relative.startswith("tests/")
        or relative.endswith("staged-review.json")
        or relative.endswith("_manifest.py")
        or relative.endswith("_canonical.py")
        or relative.endswith("_core.py")
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    if git(repo, "rev-parse", "HEAD") != EVIDENCE_HEAD:
        raise SystemExit("final manifest must be built at immutable x2 evidence head")

    final_paths = {
        path.relative_to(repo).as_posix()
        for path in (repo / FINAL_ROOT).rglob("*")
        if path.is_file()
    }
    expected_staged = final_paths | CODE_PATHS | {DELTA_MANIFEST, OWNER_MANIFEST, STAGED_REVIEW}
    staged = set(filter(None, git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()))
    if staged != expected_staged:
        raise SystemExit(
            "unexpected final staged set: "
            + json.dumps(
                {"missing": sorted(expected_staged - staged), "extra": sorted(staged - expected_staged)}, sort_keys=True
            )
        )
    if any(f"{ROOT}/x1/" in path or f"{ROOT}/x2/" in path for path in staged):
        raise SystemExit("immutable x1/x2 paths cannot be staged at final")

    final_json = sorted(path for path in staged if path.startswith(FINAL_ROOT + "/") and path.endswith(".json"))
    for relative in final_json:
        json.loads((repo / relative).read_text(encoding="utf-8"))

    changed_python = sorted(path for path in staged if path.endswith(".py"))
    result = subprocess.run(
        ["python", "-m", "py_compile", *(str(repo / path) for path in changed_python)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        raise SystemExit("final changed-Python compile failed: " + result.stderr)

    delta_paths = sorted(staged - SELF_EXCLUSIONS)
    delta_entries = [entry(relative, working_bytes(repo, relative)) for relative in delta_paths]
    dump(
        repo / DELTA_MANIFEST,
        {
            "schema": "ghc-family-normalized-lf-manifest/v1",
            "phase": "v676-v7-r2",
            "lifecycle": "final_delta",
            "source": SOURCE,
            "x1": X1_HEAD,
            "evidence": EVIDENCE_HEAD,
            "normalization": "CRLF and CR normalized to LF before SHA-256",
            "declared_self_exclusions": sorted(SELF_EXCLUSIONS),
            "entry_count": len(delta_entries),
            "entries": delta_entries,
        },
    )

    committed_owner = set(
        filter(None, git(repo, "diff", "--name-only", "--diff-filter=ACMR", SOURCE, "HEAD").splitlines())
    )
    owner_paths = sorted((committed_owner | staged) - SELF_EXCLUSIONS)
    owner_entries = []
    candidates = []
    confirmed = []
    max_words = 0
    max_word_path = ""
    for relative in owner_paths:
        raw = working_bytes(repo, relative) if relative in staged else head_bytes(repo, relative)
        owner_entries.append(entry(relative, raw))
        words = len(normalize(raw).decode("utf-8", errors="replace").split())
        if words > max_words:
            max_words = words
            max_word_path = relative
        suffix = Path(relative).suffix.lower()
        if suffix not in {".json", ".md", ".py", ".txt", ".html", ".yaml"}:
            continue
        text = normalize(raw).decode("utf-8")
        for category, pattern in PRIVACY_PATTERNS.items():
            if not pattern.search(text):
                continue
            adjudication = "scanner_definition_or_synthetic_test" if definition_or_fixture(relative) else "confirmed_payload_hit"
            row = {"path": relative, "category": category, "adjudication": adjudication}
            candidates.append(row)
            if adjudication == "confirmed_payload_hit":
                confirmed.append(row)
    if len(owner_entries) >= 2000:
        raise SystemExit("final owner scope reached 2000-file stop")
    if max_words > 100000:
        raise SystemExit("final owner document exceeded 100000-word stop")
    if confirmed:
        raise SystemExit("confirmed final privacy/raw-identifier hit: " + json.dumps(confirmed, sort_keys=True))

    dump(
        repo / OWNER_MANIFEST,
        {
            "schema": "ghc-family-normalized-lf-manifest/v1",
            "phase": "v676-v7-r2",
            "lifecycle": "final_owner_from_immutable_first_final",
            "source": SOURCE,
            "x1": X1_HEAD,
            "evidence": EVIDENCE_HEAD,
            "normalization": "CRLF and CR normalized to LF before SHA-256",
            "declared_self_exclusions": sorted(SELF_EXCLUSIONS),
            "entry_count": len(owner_entries),
            "entries": owner_entries,
        },
    )

    seal_paths = sorted(
        {
            path.relative_to(repo).as_posix()
            for path in (repo / FINAL_ROOT).rglob("*")
            if path.is_file()
        }
        - {CONTENT_SEAL}
        | {DELTA_MANIFEST, OWNER_MANIFEST}
    )
    seal_entries = [entry(relative, working_bytes(repo, relative)) for relative in seal_paths]
    dump(
        repo / CONTENT_SEAL,
        {
            "schema": "ghc-family-content-seal/v1",
            "status": "SEALED_REPOSITORY_PREPARED_FINAL",
            "phase": "v676-v7-r2",
            "source": SOURCE,
            "x1": X1_HEAD,
            "evidence": EVIDENCE_HEAD,
            "normalization": "CRLF and CR normalized to LF before SHA-256",
            "declared_self_exclusions": [CONTENT_SEAL, STAGED_REVIEW],
            "entry_count": len(seal_entries),
            "entries": seal_entries,
        },
    )

    staged_review = {
        "schema": "ghc-family-final-staged-review/v1",
        "status": "VALID_REPOSITORY_PREPARED_FINAL_STAGED_REVIEW",
        "phase": "v676-v7-r2",
        "source": SOURCE,
        "x1": X1_HEAD,
        "evidence": EVIDENCE_HEAD,
        "staged_input_count": len(staged),
        "final_delta_entries": len(delta_entries),
        "final_owner_entries": len(owner_entries),
        "content_seal_entries": len(seal_entries),
        "strict_final_json_parses": len(final_json),
        "changed_python_compiles": len(changed_python),
        "max_document_words": max_words,
        "max_document_path": max_word_path,
        "privacy_candidates": candidates,
        "confirmed_privacy_or_raw_identifier_hits": 0,
        "final_owner_tests": "scheduled_once_inside_exact-final canonical invocation; not run precommit",
        "full_repository_suite_run": False,
        "bounded_same_owner_evidence_only": True,
        "declared_self_exclusions": sorted(SELF_EXCLUSIONS),
    }
    dump(repo / STAGED_REVIEW, staged_review)
    print(
        json.dumps(
            {
                "status": staged_review["status"],
                "staged": len(staged),
                "delta": len(delta_entries),
                "owner": len(owner_entries),
                "seal": len(seal_entries),
                "json": len(final_json),
                "compiled": len(changed_python),
                "privacy_confirmed": 0,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
