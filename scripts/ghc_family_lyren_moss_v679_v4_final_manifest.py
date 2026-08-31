#!/usr/bin/env python3
"""Build and stage-review the Lyren Moss v679-v4 final delta and content seal."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "lyren-moss" / "v679-v4"
FINAL = PHASE / "final"
VALIDATION = PHASE / "validation"
EVIDENCE_HEAD = "b204dcbfbcb3d016ab18f4bebc5ef9dc56d9dee6"
SCRIPT_NAMES = {
    "scripts/build_ghc_family_lyren_moss_v679_v4_report.py",
    "scripts/build_ghc_family_lyren_moss_v679_v4_final.py",
    "scripts/ghc_family_lyren_moss_v679_v4_final_manifest.py",
    "scripts/ghc_family_lyren_moss_v679_v4_canonical.py",
}
TEST_NAMES = {"tests/test_ghc_family_lyren_moss_v679_v4_final.py"}
VALIDATION_NAMES = {
    "docs/lyren-moss/v679-v4/validation/final-build-receipt.json",
    "docs/lyren-moss/v679-v4/validation/final-scoped-validation-receipt.json",
}
SELF_EXCLUSIONS = {
    "docs/lyren-moss/v679-v4/validation/final-manifest.json",
    "docs/lyren-moss/v679-v4/validation/final-content-seal.json",
    "docs/lyren-moss/v679-v4/validation/final-staged-review.json",
}


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True, encoding="utf-8").strip()


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def allowed(path: str) -> bool:
    return path.startswith("docs/lyren-moss/v679-v4/final/") or path in SCRIPT_NAMES or path in TEST_NAMES or path in VALIDATION_NAMES


def final_files() -> list[str]:
    paths = [path.relative_to(ROOT).as_posix() for path in FINAL.rglob("*") if path.is_file()]
    for relative in sorted(SCRIPT_NAMES | TEST_NAMES | VALIDATION_NAMES):
        if (ROOT / relative).is_file():
            paths.append(relative)
    return sorted(set(paths))


def entry(path: str) -> dict:
    data = normalize((ROOT / path).read_bytes())
    return {"path": path, "normalized_lf_bytes": len(data), "sha256": sha(data)}


def build_manifest() -> dict:
    head = run("git", "rev-parse", "HEAD")
    if head != EVIDENCE_HEAD:
        raise RuntimeError(f"final manifest must be built at evidence head, got {head}")
    files = final_files()
    if not files or any(not allowed(path) for path in files):
        raise RuntimeError("final scope outside allowlist")
    manifest = {
        "schema": "ghc-family.lyren-moss.v679-v4.final-delta-manifest.v1",
        "owner": "Lyren Moss",
        "phase": "v679-v4",
        "evidence_head": EVIDENCE_HEAD,
        "entry_count": len(files),
        "entries": [entry(path) for path in files],
        "self_exclusions": sorted(SELF_EXCLUSIONS),
        "hash_domain": "normalized-LF file bytes designed to equal committed Git blob bytes",
    }
    VALIDATION.mkdir(parents=True, exist_ok=True)
    (VALIDATION / "final-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return manifest


def build_content_seal() -> dict:
    selected = [
        "docs/lyren-moss/v679-v4/final/lifecycle.json",
        "docs/lyren-moss/v679-v4/final/terminal-truth.json",
        "docs/lyren-moss/v679-v4/final/route-and-roster-overlay.json",
        "docs/lyren-moss/v679-v4/final/wellbeing-and-boundaries.json",
        "docs/lyren-moss/v679-v4/final/closeout-checklist.json",
        "docs/lyren-moss/v679-v4/final/final-operational-failures.json",
        "docs/lyren-moss/v679-v4/final/terminal-report.md",
        "docs/lyren-moss/v679-v4/final/terminal-report.html",
        "docs/lyren-moss/v679-v4/final/handoffs/ilyra-fen-v679-v5-activation-candidate.md",
        "docs/lyren-moss/v679-v4/final/activation-candidate-metadata.json",
        "docs/lyren-moss/v679-v4/validation/final-build-receipt.json",
        "docs/lyren-moss/v679-v4/validation/final-manifest.json",
    ]
    if any(not (ROOT / path).is_file() for path in selected):
        raise RuntimeError("content seal source missing")
    seal = {
        "schema": "ghc-family.lyren-moss.v679-v4.final-content-seal.v1",
        "evidence_head": EVIDENCE_HEAD,
        "entry_count": len(selected),
        "entries": [entry(path) for path in selected],
        "route_state": "PREPARED_NOT_SENT",
    }
    (VALIDATION / "final-content-seal.json").write_text(json.dumps(seal, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return seal


def batch_index_blobs(entries: list[dict]) -> list[str]:
    index_rows = {}
    for line in run("git", "ls-files", "-s").splitlines():
        if "\t" not in line:
            continue
        metadata, path = line.split("\t", 1)
        fields = metadata.split()
        if len(fields) >= 3 and fields[2] == "0":
            index_rows[path] = fields[1]
    mismatches = []
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    assert process.stdin is not None and process.stdout is not None
    try:
        for item in entries:
            object_id = index_rows.get(item["path"])
            if not object_id:
                mismatches.append(item["path"])
                continue
            process.stdin.write(object_id.encode("ascii") + b"\n")
            process.stdin.flush()
            header = process.stdout.readline().decode("ascii").strip().split()
            if len(header) != 3 or header[1] != "blob":
                mismatches.append(item["path"])
                continue
            data = normalize(process.stdout.read(int(header[2])))
            process.stdout.read(1)
            if sha(data) != item["sha256"] or len(data) != item["normalized_lf_bytes"]:
                mismatches.append(item["path"])
    finally:
        process.stdin.close()
        process.wait(timeout=30)
    return mismatches


def staged_review() -> dict:
    manifest = json.loads((VALIDATION / "final-manifest.json").read_text(encoding="utf-8"))
    seal = json.loads((VALIDATION / "final-content-seal.json").read_text(encoding="utf-8"))
    staged = [line for line in run("git", "diff", "--cached", "--name-only").splitlines() if line]
    deleted = [line for line in run("git", "diff", "--cached", "--name-only", "--diff-filter=D").splitlines() if line]
    expected = {item["path"] for item in manifest["entries"]} | {
        "docs/lyren-moss/v679-v4/validation/final-manifest.json",
        "docs/lyren-moss/v679-v4/validation/final-content-seal.json",
    }
    outside = sorted(path for path in staged if not allowed(path) and path not in SELF_EXCLUSIONS)
    missing = sorted(expected - set(staged))
    unexpected = sorted(set(staged) - expected - {"docs/lyren-moss/v679-v4/validation/final-staged-review.json"})
    mismatches = batch_index_blobs(manifest["entries"] + seal["entries"])
    result = {
        "schema": "ghc-family.lyren-moss.v679-v4.final-staged-review.v1",
        "evidence_head": run("git", "rev-parse", "HEAD"),
        "staged_file_count_before_self": len(staged),
        "final_manifest_entries": manifest["entry_count"],
        "content_seal_entries": seal["entry_count"],
        "deleted_paths": deleted,
        "outside_allowlist": outside,
        "missing_paths": missing,
        "unexpected_paths": unexpected,
        "index_manifest_or_seal_mismatches": mismatches,
        "passed": not (deleted or outside or missing or unexpected or mismatches) and run("git", "rev-parse", "HEAD") == EVIDENCE_HEAD,
    }
    (VALIDATION / "final-staged-review.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("manifest", "seal", "staged-review"))
    args = parser.parse_args()
    if args.mode == "manifest":
        value = build_manifest()
        output = {"entry_count": value["entry_count"], "evidence_head": value["evidence_head"]}
    elif args.mode == "seal":
        value = build_content_seal()
        output = {"entry_count": value["entry_count"], "route_state": value["route_state"]}
    else:
        output = staged_review()
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
