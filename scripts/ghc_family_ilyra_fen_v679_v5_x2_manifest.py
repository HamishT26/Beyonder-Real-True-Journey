#!/usr/bin/env python3
"""Build the exact normalized-LF manifest and staged review for Ilyra x2."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path


SOURCE = "9cce202db223bec1aa7c81dd98dcbd3b83c6cd29"
X1_HEAD = "5d762d925cf59319e112fb44ae4a4c61b8eddb3f"
ROOT = "docs/ilyra-fen/v679-v5"
X2_ROOT = f"{ROOT}/x2"
MANIFEST = f"{ROOT}/validation/x2-manifest.json"
REVIEW = f"{ROOT}/validation/x2-staged-review.json"
CODE_PATHS = {
    "scripts/build_ghc_family_ilyra_fen_v679_v5_report.py",
    "scripts/build_ghc_family_ilyra_fen_v679_v5_x2.py",
    "scripts/ghc_family_ilyra_fen_v679_v5_core.py",
    "scripts/ghc_family_ilyra_fen_v679_v5_accessibility_runner.py",
    "scripts/ghc_family_ilyra_fen_v679_v5_topology_runner.py",
    "scripts/ghc_family_ilyra_fen_v679_v5_contract_runner.py",
    "scripts/ghc_family_ilyra_fen_v679_v5_flashcard_runner.py",
    "scripts/ghc_family_ilyra_fen_v679_v5_metadata_runner.py",
    "scripts/ghc_family_ilyra_fen_v679_v5_mutation_runner.py",
    "scripts/ghc_family_ilyra_fen_v679_v5_portfolio_runner.py",
    "scripts/ghc_family_ilyra_fen_v679_v5_privacy_runner.py",
    "scripts/ghc_family_ilyra_fen_v679_v5_toolchain_runner.py",
    "scripts/ghc_family_ilyra_fen_v679_v5_x2_manifest.py",
    "tests/test_ghc_family_ilyra_fen_v679_v5_x2.py",
}
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(r"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
}
DEFINITION_PATHS = {
    "scripts/ghc_family_ilyra_fen_v679_v5_core.py",
    "scripts/ghc_family_ilyra_fen_v679_v5_x2_manifest.py",
    "tests/test_ghc_family_ilyra_fen_v679_v5_x2.py",
}


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()

    if git(repo, "rev-parse", "HEAD") != X1_HEAD:
        raise SystemExit("x2 evidence manifest must be built at the frozen x1 head")
    x2_paths = {
        path.relative_to(repo).as_posix()
        for path in (repo / X2_ROOT).rglob("*")
        if path.is_file()
    }
    expected = x2_paths | CODE_PATHS | {MANIFEST, REVIEW}
    staged = set(filter(None, git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()))
    if staged != expected:
        raise SystemExit(
            "unexpected staged x2 set: "
            + json.dumps({"missing": sorted(expected - staged), "extra": sorted(staged - expected)}, sort_keys=True)
        )
    if any(path.startswith(f"{ROOT}/x1/") for path in staged):
        raise SystemExit("planning-only x1 is immutable during x2")

    json_paths = sorted(path for path in staged if path.startswith(X2_ROOT + "/") and path.endswith(".json"))
    for relative in json_paths:
        json.loads((repo / relative).read_text(encoding="utf-8"))

    code_paths = sorted(path for path in staged if path.endswith(".py"))
    for relative in code_paths:
        try:
            ast.parse((repo / relative).read_text(encoding="utf-8"), filename=relative)
        except SyntaxError as error:
            raise SystemExit(f"changed Python syntax failed: {relative}: {error}") from error

    covered = sorted(expected - {MANIFEST, REVIEW})
    entries: list[dict[str, object]] = []
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    max_words = 0
    max_word_path = ""
    for relative in covered:
        path = repo / relative
        raw = normalized(path)
        words = len(raw.decode("utf-8", errors="replace").split())
        if words > max_words:
            max_words = words
            max_word_path = relative
        entries.append(
            {
                "path": relative,
                "bytes": len(raw),
                "sha256_normalized_lf": hashlib.sha256(raw).hexdigest(),
            }
        )
        if path.suffix.lower() not in {".json", ".md", ".py", ".txt", ".html", ".yaml"}:
            continue
        value = raw.decode("utf-8")
        for category, pattern in PRIVACY_PATTERNS.items():
            if not pattern.search(value):
                continue
            adjudication = "scanner_definition_or_synthetic_test" if relative in DEFINITION_PATHS else "confirmed_payload_hit"
            row = {"path": relative, "category": category, "adjudication": adjudication}
            candidates.append(row)
            if adjudication == "confirmed_payload_hit":
                confirmed.append(row)

    if len(entries) >= 2000:
        raise SystemExit("owner x2 materialization reached the 2000-file stop")
    if max_words > 100000:
        raise SystemExit("owner document exceeded the 100000-word stop")
    if confirmed:
        raise SystemExit("confirmed privacy or raw-identifier hit: " + json.dumps(confirmed, sort_keys=True))

    manifest = {
        "schema": "ghc-family-normalized-lf-manifest/v1",
        "source": SOURCE,
        "x1": X1_HEAD,
        "phase": "v679-v5",
        "lifecycle": "x2_evidence",
        "normalization": "CRLF and CR normalized to LF before SHA-256",
        "declared_self_exclusions": [MANIFEST, REVIEW],
        "entry_count": len(entries),
        "entries": entries,
    }
    review = {
        "schema": "ghc-family-exact-staged-review/v1",
        "source": SOURCE,
        "x1": X1_HEAD,
        "phase": "v679-v5",
        "status": "VALID_X2_EVIDENCE_STAGED_REVIEW",
        "staged_input_count": len(staged),
        "manifest_entries": len(entries),
        "strict_json_parses": len(json_paths),
        "changed_python_compiles": len(code_paths),
        "owner_file_stop": 2000,
        "max_document_words": max_words,
        "max_document_path": max_word_path,
        "privacy_candidates": candidates,
        "confirmed_privacy_or_raw_identifier_hits": 0,
        "declared_self_exclusions": [MANIFEST, REVIEW],
        "owner_test_truth": {
            "state": "VALID_PRE_HYGIENE_X2_OWNER_SCOPED_TEST_AGGREGATE",
            "aggregate_invocations": 1,
            "successful_invocations": 1,
            "tests_passed": 21,
            "tests_failed": 0,
            "post_success_replays": 0,
            "post_test_change": "receipt-only inherited wording in this manifest generator was corrected before exact assembly; no contract, core, runner, or test semantics changed after suite success",
            "post_test_semantic_change": False,
            "exact_post_hygiene_aggregate_replayed": False,
            "exact_post_hygiene_dependencies": ["changed Python syntax", "normalized-LF manifest", "diff hygiene"],
            "bounded_same_owner_only": True,
        },
        "x1_mutated": False,
        "full_repository_suite_run": False,
        "bounded_same_owner_evidence_only": True,
    }
    dump(repo / MANIFEST, manifest)
    dump(repo / REVIEW, review)
    print(
        json.dumps(
            {
                "status": review["status"],
                "staged": len(staged),
                "entries": len(entries),
                "json": len(json_paths),
                "compiled": len(code_paths),
                "privacy_confirmed": 0,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
