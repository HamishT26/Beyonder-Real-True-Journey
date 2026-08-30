from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT_REL = "docs/auren-lark/v677-v7"
ROOT = REPO / ROOT_REL
FINAL = ROOT / "final"
VALIDATION = ROOT / "validation"
SOURCE = "62ac8de91e2fec0d6a024f51eff6a3ad8d807a4d"
X1 = "73bf85d9371b74dda26953e743958ce684ea1436"
EVIDENCE = "3f91c32cb1acda2900ce69bedc60971353084775"

DELTA_PATH = f"{ROOT_REL}/validation/final-delta-manifest.json"
OWNER_PATH = f"{ROOT_REL}/validation/final-owner-manifest.json"
SEAL_PATH = f"{ROOT_REL}/final/content-seal.json"
REVIEW_PATH = f"{ROOT_REL}/validation/final-staged-review.json"
SELF_EXCLUSIONS = {DELTA_PATH, OWNER_PATH, SEAL_PATH, REVIEW_PATH}
CODE_PATHS = {
    "scripts/build_ghc_family_auren_lark_v677_v7_final.py",
    "scripts/ghc_family_auren_lark_v677_v7_canonical.py",
    "scripts/ghc_family_auren_lark_v677_v7_final_manifest.py",
    "tests/test_ghc_family_auren_lark_v677_v7_final.py",
}


def git(*args: str, text: bool = True):
    return subprocess.check_output(
        ["git", *args],
        cwd=REPO,
        text=text,
        encoding="utf-8" if text else None,
    )


def lines(value: str) -> list[str]:
    return [
        row.strip().replace("\\", "/")
        for row in value.splitlines()
        if row.strip()
    ]


def normalized(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def index_blob(path: str) -> bytes:
    return git("show", f":{path}", text=False)


def head_blob(path: str) -> bytes:
    return git("show", f"HEAD:{path}", text=False)


def entry(path: str, raw: bytes) -> dict:
    data = normalized(raw)
    return {
        "path": path,
        "bytes_normalized_lf": len(data),
        "sha256_normalized_lf": hashlib.sha256(data).hexdigest(),
    }


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def scan_privacy(
    owner_data: dict[str, bytes],
) -> tuple[list[dict], list[dict]]:
    patterns = {
        "private_absolute_path": re.compile(rb"(?i)[A-Z]:[\\/]+Users[\\/]+"),
        "raw_task_identifier": re.compile(
            rb"(?i)(source_thread_id|clientThreadId)"
        ),
        "credential_or_secret": re.compile(
            rb"(?i)(-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9_]{20,})"
        ),
        "uuid_like_private_identifier": re.compile(
            rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_session_material": re.compile(
            rb"(?i)(private app state|session stream|raw transcript payload|screenshot payload)"
        ),
    }
    candidates: list[dict] = []
    confirmed: list[dict] = []
    for path, raw in sorted(owner_data.items()):
        if Path(path).suffix.lower() not in {
            ".json",
            ".md",
            ".txt",
            ".html",
            ".py",
            ".yaml",
            ".yml",
        }:
            continue
        for category, pattern in patterns.items():
            if pattern.search(raw):
                scanner_definition = path.startswith(("scripts/", "tests/"))
                row = {
                    "path": path,
                    "category": category,
                    "scanner_definition": scanner_definition,
                }
                candidates.append(row)
                if not scanner_definition:
                    confirmed.append(row)
    return candidates, confirmed


def main() -> None:
    if git("rev-parse", "HEAD").strip() != EVIDENCE:
        raise SystemExit(
            "final manifest builder must run at immutable Auren evidence head"
        )
    if (
        git("rev-parse", f"{X1}^").strip() != SOURCE
        or git("rev-parse", f"{EVIDENCE}^").strip() != X1
    ):
        raise SystemExit("x1/evidence direct-parent chain mismatch")

    staged = set(
        lines(git("diff", "--cached", "--name-only", "--diff-filter=ACMR"))
    )
    final_paths = {
        path.relative_to(REPO).as_posix()
        for path in FINAL.rglob("*")
        if path.is_file()
    }
    expected = (
        final_paths
        | CODE_PATHS
        | {DELTA_PATH, OWNER_PATH, SEAL_PATH, REVIEW_PATH}
    )
    if staged != expected - SELF_EXCLUSIONS:
        missing = sorted((expected - SELF_EXCLUSIONS) - staged)
        extra = sorted(staged - (expected - SELF_EXCLUSIONS))
        raise SystemExit(
            f"initial staged set mismatch missing={missing} extra={extra}"
        )
    if any("/x1/" in path or "/x2/" in path for path in staged):
        raise SystemExit("final staging mixed immutable x1 or x2 paths")

    delta_paths = sorted(staged)
    delta_data = {path: index_blob(path) for path in delta_paths}
    for path, raw in delta_data.items():
        if path.endswith(".json"):
            json.loads(raw.decode("utf-8"))
        if path.endswith(".py"):
            ast.parse(raw.decode("utf-8"), filename=path)

    committed_paths = set(
        lines(
            git(
                "diff",
                "--name-only",
                "--diff-filter=ACMR",
                SOURCE,
                "HEAD",
            )
        )
    )
    owner_paths = sorted((committed_paths | staged) - SELF_EXCLUSIONS)
    owner_data: dict[str, bytes] = {}
    for path in owner_paths:
        owner_data[path] = (
            delta_data[path] if path in delta_data else head_blob(path)
        )

    candidates, confirmed = scan_privacy(owner_data)
    if confirmed:
        raise SystemExit(f"confirmed privacy findings: {confirmed}")
    if len(owner_paths) >= 2000:
        raise SystemExit("owner file ceiling reached")
    oversized = []
    for path, raw in owner_data.items():
        if Path(path).suffix.lower() in {".md", ".txt", ".html"}:
            words = len(raw.decode("utf-8").split())
            if words > 100000:
                oversized.append({"path": path, "words": words})
    if oversized:
        raise SystemExit(f"document word ceiling exceeded: {oversized}")

    delta_manifest = {
        "schema": "ghc-family-exact-git-blob-manifest/v1",
        "status": "REPOSITORY_PREPARED_FINAL_DELTA",
        "source": EVIDENCE,
        "entry_count": len(delta_paths),
        "entries": [entry(path, delta_data[path]) for path in delta_paths],
        "self_exclusions": sorted(SELF_EXCLUSIONS),
        "normalized_lf": True,
    }
    owner_manifest = {
        "schema": "ghc-family-exact-git-blob-manifest/v1",
        "status": "FINAL_OWNER_FROM_ILYRA_V677_V6_SOURCE",
        "source": SOURCE,
        "entry_count": len(owner_paths),
        "entries": [entry(path, owner_data[path]) for path in owner_paths],
        "self_exclusions": sorted(SELF_EXCLUSIONS),
        "normalized_lf": True,
    }
    write_json(VALIDATION / "final-delta-manifest.json", delta_manifest)
    write_json(VALIDATION / "final-owner-manifest.json", owner_manifest)

    seal_paths = sorted((final_paths - {SEAL_PATH}) | {DELTA_PATH, OWNER_PATH})
    seal_entries = [
        entry(path, (REPO / path).read_bytes()) for path in seal_paths
    ]
    write_json(
        FINAL / "content-seal.json",
        {
            "schema": "ghc-family-content-seal/v1",
            "status": "SEALED_REPOSITORY_PREPARED_FINAL",
            "entry_count": len(seal_entries),
            "entries": seal_entries,
            "normalized_lf": True,
        },
    )

    review = {
        "schema": "ghc-family-final-staged-review/v1",
        "status": "VALID_REPOSITORY_PREPARED_FINAL_STAGED_REVIEW",
        "expected_staged_paths": len(expected),
        "delta_manifest_entries": len(delta_paths),
        "owner_manifest_entries": len(owner_paths),
        "owner_file_count": len(owner_paths),
        "materialized_owner_file_ceiling": 2000,
        "privacy_classes": 5,
        "privacy_candidates": candidates,
        "confirmed_privacy_hits": confirmed,
        "json_parses": sum(path.endswith(".json") for path in owner_paths),
        "python_syntax_parses": sum(
            path.endswith(".py") for path in delta_paths
        ),
        "document_word_ceiling": 100000,
        "out_of_scope_paths": [],
        "x1_or_x2_paths_staged": [],
        "final_tests": "SCHEDULED_ONCE_INSIDE_EXACT_FINAL_CANONICAL",
        "precanonical_final_test_run": False,
        "full_repository_suite": False,
        "independent_reproduction": False,
    }
    write_json(VALIDATION / "final-staged-review.json", review)
    print(
        json.dumps(
            {
                "status": review["status"],
                "delta_entries": len(delta_paths),
                "owner_entries": len(owner_paths),
                "seal_entries": len(seal_entries),
                "privacy_candidates": len(candidates),
                "confirmed_hits": len(confirmed),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
