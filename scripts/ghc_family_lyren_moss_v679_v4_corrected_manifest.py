#!/usr/bin/env python3
"""Manifest and stage-review the v679-v4 dependency correction."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "lyren-moss" / "v679-v4"
CORRECTION = PHASE / "correction1"
VALIDATION = PHASE / "validation"
INITIAL_FINAL = "20923e75fe7490f43ed585ee97dca596b9ca7adc"
SCRIPT_NAMES = {
    "scripts/ghc_family_lyren_moss_v679_v4_canonical.py",
    "scripts/build_ghc_family_lyren_moss_v679_v4_correction1.py",
    "scripts/ghc_family_lyren_moss_v679_v4_corrected_manifest.py",
}
TEST_NAMES = {"tests/test_ghc_family_lyren_moss_v679_v4_correction1.py"}
VALIDATION_NAMES = {
    "docs/lyren-moss/v679-v4/validation/correction1-build-receipt.json",
    "docs/lyren-moss/v679-v4/validation/correction1-test-receipt.json",
}
SELF_EXCLUSIONS = {
    "docs/lyren-moss/v679-v4/validation/corrected-final-manifest.json",
    "docs/lyren-moss/v679-v4/validation/corrected-content-seal.json",
    "docs/lyren-moss/v679-v4/validation/corrected-staged-review.json",
}


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True, encoding="utf-8").strip()


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def item(path: str) -> dict:
    data = normalize((ROOT / path).read_bytes())
    return {"path": path, "normalized_lf_bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def allowed(path: str) -> bool:
    return path.startswith("docs/lyren-moss/v679-v4/correction1/") or path in SCRIPT_NAMES or path in TEST_NAMES or path in VALIDATION_NAMES


def files() -> list[str]:
    paths = [path.relative_to(ROOT).as_posix() for path in CORRECTION.rglob("*") if path.is_file()]
    for relative in sorted(SCRIPT_NAMES | TEST_NAMES | VALIDATION_NAMES):
        if (ROOT / relative).is_file():
            paths.append(relative)
    return sorted(set(paths))


def manifest() -> dict:
    if run("git", "rev-parse", "HEAD") != INITIAL_FINAL:
        raise RuntimeError("corrected manifest must be built at the retained initial final")
    paths = files()
    if not paths or any(not allowed(path) for path in paths):
        raise RuntimeError("correction scope outside allowlist")
    value = {
        "schema": "ghc-family.lyren-moss.v679-v4.dependency-corrected-final-manifest.v1",
        "retained_initial_final": INITIAL_FINAL,
        "entry_count": len(paths),
        "entries": [item(path) for path in paths],
        "self_exclusions": sorted(SELF_EXCLUSIONS),
        "hash_domain": "normalized-LF file bytes designed to equal committed Git blob bytes",
    }
    (VALIDATION / "corrected-final-manifest.json").write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return value


def seal() -> dict:
    selected = [
        "docs/lyren-moss/v679-v4/correction1/preflight-failure.json",
        "docs/lyren-moss/v679-v4/correction1/correction-test-failure.json",
        "docs/lyren-moss/v679-v4/correction1/lifecycle.json",
        "docs/lyren-moss/v679-v4/correction1/terminal-overlay.json",
        "docs/lyren-moss/v679-v4/correction1/route-overlay.json",
        "docs/lyren-moss/v679-v4/correction1/correction-overview.md",
        "docs/lyren-moss/v679-v4/correction1/handoffs/ilyra-fen-v679-v5-dependency-corrected-activation-candidate.md",
        "docs/lyren-moss/v679-v4/correction1/activation-candidate-metadata.json",
        "docs/lyren-moss/v679-v4/validation/correction1-build-receipt.json",
        "docs/lyren-moss/v679-v4/validation/corrected-final-manifest.json",
    ]
    if any(not (ROOT / path).is_file() for path in selected):
        raise RuntimeError("correction seal source missing")
    value = {
        "schema": "ghc-family.lyren-moss.v679-v4.dependency-corrected-content-seal.v1",
        "retained_initial_final": INITIAL_FINAL,
        "entry_count": len(selected),
        "entries": [item(path) for path in selected],
        "route_state": "PREPARED_NOT_SENT",
    }
    (VALIDATION / "corrected-content-seal.json").write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return value


def batch_index(entries: list[dict]) -> list[str]:
    rows = {}
    for line in run("git", "ls-files", "-s").splitlines():
        if "\t" in line:
            metadata, path = line.split("\t", 1)
            fields = metadata.split()
            if len(fields) >= 3 and fields[2] == "0":
                rows[path] = fields[1]
    mismatches = []
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    assert process.stdin is not None and process.stdout is not None
    try:
        for entry in entries:
            oid = rows.get(entry["path"])
            if not oid:
                mismatches.append(entry["path"])
                continue
            process.stdin.write(oid.encode("ascii") + b"\n")
            process.stdin.flush()
            header = process.stdout.readline().decode("ascii").strip().split()
            if len(header) != 3 or header[1] != "blob":
                mismatches.append(entry["path"])
                continue
            data = normalize(process.stdout.read(int(header[2])))
            process.stdout.read(1)
            if hashlib.sha256(data).hexdigest() != entry["sha256"] or len(data) != entry["normalized_lf_bytes"]:
                mismatches.append(entry["path"])
    finally:
        process.stdin.close()
        process.wait(timeout=30)
    return mismatches


def review() -> dict:
    current_manifest = json.loads((VALIDATION / "corrected-final-manifest.json").read_text(encoding="utf-8"))
    current_seal = json.loads((VALIDATION / "corrected-content-seal.json").read_text(encoding="utf-8"))
    staged = [line for line in run("git", "diff", "--cached", "--name-only").splitlines() if line]
    deleted = [line for line in run("git", "diff", "--cached", "--name-only", "--diff-filter=D").splitlines() if line]
    expected = {entry["path"] for entry in current_manifest["entries"]} | {
        "docs/lyren-moss/v679-v4/validation/corrected-final-manifest.json",
        "docs/lyren-moss/v679-v4/validation/corrected-content-seal.json",
    }
    outside = sorted(path for path in staged if not allowed(path) and path not in SELF_EXCLUSIONS)
    missing = sorted(expected - set(staged))
    unexpected = sorted(set(staged) - expected - {"docs/lyren-moss/v679-v4/validation/corrected-staged-review.json"})
    mismatches = batch_index(current_manifest["entries"] + current_seal["entries"])
    value = {
        "schema": "ghc-family.lyren-moss.v679-v4.dependency-corrected-staged-review.v1",
        "retained_initial_final": run("git", "rev-parse", "HEAD"),
        "staged_file_count_before_self": len(staged),
        "manifest_entries": current_manifest["entry_count"],
        "seal_entries": current_seal["entry_count"],
        "deleted_paths": deleted,
        "outside_allowlist": outside,
        "missing_paths": missing,
        "unexpected_paths": unexpected,
        "index_mismatches": mismatches,
        "passed": run("git", "rev-parse", "HEAD") == INITIAL_FINAL and not (deleted or outside or missing or unexpected or mismatches),
    }
    (VALIDATION / "corrected-staged-review.json").write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("manifest", "seal", "review"))
    args = parser.parse_args()
    value = manifest() if args.mode == "manifest" else seal() if args.mode == "seal" else review()
    print(json.dumps({"entry_count": value.get("entry_count"), "passed": value.get("passed"), "route_state": value.get("route_state")}, sort_keys=True))


if __name__ == "__main__":
    main()
