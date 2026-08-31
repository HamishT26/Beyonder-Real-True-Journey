#!/usr/bin/env python3
"""Build and review the immutable Lyren Moss v679-v4 x2 evidence manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "lyren-moss" / "v679-v4"
VALIDATION = PHASE / "validation"
X1_HEAD = "1fe28fafc308298e1043a9e2afbecf59c24c9866"
SCRIPT_NAMES = {
    "scripts/ghc_family_lyren_moss_v679_v4_core.py",
    "scripts/build_ghc_family_lyren_moss_v679_v4_x2.py",
    "scripts/ghc_family_lyren_moss_v679_v4_x2_manifest.py",
    "scripts/ghc_family_tabulating_card_contract_runner.py",
    "scripts/ghc_family_tabulating_card_column_runner.py",
    "scripts/ghc_family_tabulating_card_sequence_runner.py",
    "scripts/ghc_family_tabulating_card_correction_runner.py",
    "scripts/ghc_family_tabulating_card_provenance_runner.py",
    "scripts/ghc_family_tabulating_card_accessibility_runner.py",
    "scripts/ghc_family_tabulating_card_privacy_runner.py",
    "scripts/ghc_family_tabulating_card_mutation_runner.py",
    "scripts/ghc_family_tabulating_card_method_flow_runner.py",
    "scripts/ghc_family_tabulating_card_terminal_runner.py",
}
TEST_NAMES = {"tests/test_ghc_family_lyren_moss_v679_v4_x2.py"}
VALIDATION_NAMES = {
    "docs/lyren-moss/v679-v4/validation/x2-build-receipt.json",
    "docs/lyren-moss/v679-v4/validation/x2-test-composite.json",
    "docs/lyren-moss/v679-v4/validation/skill-creator-validation-receipt.json",
    "docs/lyren-moss/v679-v4/validation/runner-entrypoint-smoke-receipt.json",
    "docs/lyren-moss/v679-v4/validation/x2-compile-receipt.json",
}
SELF_EXCLUSIONS = {
    "docs/lyren-moss/v679-v4/validation/x2-manifest.json",
    "docs/lyren-moss/v679-v4/validation/x2-staged-review.json",
}


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True, encoding="utf-8").strip()


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def allowed(path: str) -> bool:
    return (
        path.startswith("docs/lyren-moss/v679-v4/x2/")
        or path in SCRIPT_NAMES
        or path in TEST_NAMES
        or path in VALIDATION_NAMES
    )


def owner_files() -> list[str]:
    paths: list[str] = []
    for path in (PHASE / "x2").rglob("*"):
        if path.is_file():
            paths.append(path.relative_to(ROOT).as_posix())
    for path in sorted(SCRIPT_NAMES | TEST_NAMES | VALIDATION_NAMES):
        if (ROOT / path).is_file():
            paths.append(path)
    return sorted(set(paths))


def build_manifest() -> dict:
    head = run("git", "rev-parse", "HEAD")
    if head != X1_HEAD:
        raise RuntimeError(f"x2 manifest must be built at frozen x1, got {head}")
    files = owner_files()
    if len(files) >= 2000:
        raise RuntimeError("owner file guard reached")
    if not files or any(not allowed(path) for path in files):
        raise RuntimeError("x2 owner scope is empty or outside the allowlist")
    entries = []
    for relative in files:
        data = normalize((ROOT / relative).read_bytes())
        entries.append({"path": relative, "normalized_lf_bytes": len(data), "sha256": sha(data)})
    manifest = {
        "schema": "ghc-family.lyren-moss.v679-v4.immutable-x2-manifest.v1",
        "owner": "Lyren Moss",
        "phase": "v679-v4",
        "x1_head": X1_HEAD,
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": sorted(SELF_EXCLUSIONS),
        "hash_domain": "normalized-LF file bytes designed to equal committed Git blob bytes",
        "file_guard": 2000,
    }
    VALIDATION.mkdir(parents=True, exist_ok=True)
    (VALIDATION / "x2-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return manifest


def staged_review() -> dict:
    staged = [line for line in run("git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT").splitlines() if line]
    deleted = [line for line in run("git", "diff", "--cached", "--name-only", "--diff-filter=D").splitlines() if line]
    outside = sorted(path for path in staged if not allowed(path) and path not in SELF_EXCLUSIONS)
    manifest = json.loads((VALIDATION / "x2-manifest.json").read_text(encoding="utf-8"))
    index_rows = {}
    for line in run("git", "ls-files", "-s").splitlines():
        if "\t" not in line:
            continue
        metadata, path = line.split("\t", 1)
        fields = metadata.split()
        if len(fields) >= 3 and fields[2] == "0":
            index_rows[path] = fields[1]
    index_mismatches = []
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None
    try:
        for entry in manifest["entries"]:
            object_id = index_rows.get(entry["path"])
            if not object_id:
                index_mismatches.append(entry["path"])
                continue
            process.stdin.write(object_id.encode("ascii") + b"\n")
            process.stdin.flush()
            header = process.stdout.readline().decode("ascii").strip().split()
            if len(header) != 3 or header[1] != "blob":
                index_mismatches.append(entry["path"])
                continue
            blob = process.stdout.read(int(header[2]))
            process.stdout.read(1)
            normalized = normalize(blob)
            if sha(normalized) != entry["sha256"] or len(normalized) != entry["normalized_lf_bytes"]:
                index_mismatches.append(entry["path"])
    finally:
        process.stdin.close()
        process.wait(timeout=30)
    expected = {entry["path"] for entry in manifest["entries"]} | {"docs/lyren-moss/v679-v4/validation/x2-manifest.json"}
    missing = sorted(expected - set(staged))
    unexpected = sorted(set(staged) - expected - {"docs/lyren-moss/v679-v4/validation/x2-staged-review.json"})
    result = {
        "schema": "ghc-family.lyren-moss.v679-v4.x2-staged-review.v1",
        "staged_file_count_before_self": len(staged),
        "manifest_entry_count": manifest["entry_count"],
        "deleted_paths": deleted,
        "outside_allowlist": outside,
        "missing_manifest_paths": missing,
        "unexpected_staged_paths": unexpected,
        "index_manifest_mismatches": index_mismatches,
        "x1_head": run("git", "rev-parse", "HEAD"),
        "passed": not (deleted or outside or missing or unexpected or index_mismatches),
    }
    (VALIDATION / "x2-staged-review.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("manifest", "staged-review"))
    args = parser.parse_args()
    value = build_manifest() if args.mode == "manifest" else staged_review()
    print(json.dumps(value if args.mode == "staged-review" else {"entry_count": value["entry_count"], "x1_head": value["x1_head"]}, sort_keys=True))


if __name__ == "__main__":
    main()
