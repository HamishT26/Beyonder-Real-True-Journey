#!/usr/bin/env python3
"""Exact Git-index review for Sable Rook v646-v3 evidence and final stages."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/sable-rook/v646-v3")
PHASE = ROOT / PHASE_REL
PRIVATE = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    "delegation_markup": re.compile(r"(?i)<" + r"\/?" + "codex_" + r"delegation>|<source_" + "thread_id>"),
    "private_uri": re.compile(r"(?i)\b(?:app|plugin|codex|vscode)://"),
    "private_local_path": re.compile(r"(?i)(?:\b[A-Z]:[\\/]+(?:Users|GHC-Archives)[\\/]+|/(?:home|users)/)"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,;]+"),
}
ALLOWED_SCRIPTS = {
    "scripts/build_ghc_family_v646_v3_evidence.py",
    "scripts/build_ghc_family_v646_v3_skills.py",
    "scripts/build_ghc_family_v646_v3_closeout.py",
    "scripts/ghc_family_external_negative_reconciler.py",
    "scripts/ghc_family_phase_local_test_quarantine.py",
    "scripts/ghc_family_exact_revision_credit.py",
    "scripts/ghc_family_manifest_fixed_point.py",
    "scripts/ghc_family_named_lane_locality_proof.py",
    "scripts/ghc_family_v646_v3_core_runner.py",
    "scripts/ghc_family_v646_v3_portfolio_runner.py",
    "scripts/ghc_family_v646_v3_runner_suite.py",
    "scripts/ghc_family_v646_v3_runtime.py",
    "scripts/ghc_family_v646_v3_scoped_tests.py",
    "scripts/ghc_family_v646_v3_skill_runner.py",
    "scripts/ghc_family_v646_v3_staged_review.py",
    "scripts/ghc_family_v646_v3_tools.py",
    "scripts/ghc_family_v646_v3_validation_runner.py",
    "scripts/ghc_family_v646_v3_validator.py",
    "tests/test_ghc_family_v646_v3.py",
}
BOUNDARY = "Exact staged-blob review is bounded same-owner evidence only; it is not complete privacy, exhaustive security, production certification, authority, or independent reproduction."


def git(*args: str, binary: bool = False, check: bool = True) -> str | bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, text=not binary, capture_output=True)
    if check and result.returncode:
        error = result.stderr if isinstance(result.stderr, str) else result.stderr.decode(errors="replace")
        raise RuntimeError(error.strip() or f"git {' '.join(args)} failed")
    return result.stdout


def scan(path: str, text: str) -> list[dict[str, Any]]:
    hits = []
    for kind, pattern in PRIVATE.items():
        for match in pattern.finditer(text):
            hits.append({"path": path, "class": kind, "offset": match.start()})
    return hits


def review(stage: str) -> tuple[dict[str, Any], dict[str, Any]]:
    paths = [row for row in str(git("diff", "--cached", "--name-only", "--diff-filter=ACMR")).splitlines() if row]
    prefix = PHASE_REL.as_posix() + "/"
    manifest_rel = (PHASE_REL / f"validation/{stage}-staged-manifest.json").as_posix()
    issues: list[str] = []
    privacy_hits: list[dict[str, Any]] = []
    json_count = 0
    entries = []
    for path in paths:
        if not (path.startswith(prefix) or path in ALLOWED_SCRIPTS):
            issues.append(f"unexpected staged path: {path}")
        blob = git("show", f":{path}", binary=True)
        assert isinstance(blob, bytes)
        if path.endswith(".json"):
            json_count += 1
            try:
                json.loads(blob.decode("utf-8"))
            except Exception as exc:
                issues.append(f"invalid staged JSON {path}: {exc}")
        try:
            privacy_hits.extend(scan(path, blob.decode("utf-8")))
        except UnicodeDecodeError:
            pass
        if path != manifest_rel:
            entries.append({"path": path, "sha256": hashlib.sha256(blob).hexdigest(), "bytes": len(blob)})

    lifecycle = {"closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"}
    lifecycle_paths = [path for path in paths if Path(path).name in lifecycle]
    if stage == "evidence" and lifecycle_paths:
        issues.append(f"final lifecycle files staged in evidence: {lifecycle_paths}")
    if stage == "final" and len(lifecycle_paths) != 3:
        issues.append(f"final lifecycle set incomplete: {lifecycle_paths}")
    if not paths:
        issues.append("staged surface is empty")
    diff_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, text=True, capture_output=True)
    if diff_check.returncode:
        issues.append("git diff --cached --check failed")
    if privacy_hits:
        issues.append("confirmed privacy or raw-identifier hits")

    payload = {
        "schema": f"ghc.family.v646-v3.{stage}-staged-review.v1",
        "stage": stage,
        "staged_file_count": len(paths),
        "staged_paths": paths,
        "json_parse_count": json_count,
        "privacy_pattern_classes": sorted(PRIVATE),
        "privacy_confirmed_hits": privacy_hits,
        "privacy_confirmed_hit_count": len(privacy_hits),
        "lifecycle_paths": lifecycle_paths,
        "diff_check": "pass" if diff_check.returncode == 0 else "fail",
        "issues": issues,
        "valid": not issues,
        "boundary": BOUNDARY,
    }
    manifest = {
        "schema": f"ghc.family.v646-v3.{stage}-staged-manifest.v1",
        "phase": "v646-gmut-thos-v3-x1-x2",
        "stage": stage,
        "hash_domain": "exact staged Git-index blobs excluding this self-referential manifest",
        "entry_count": len(entries),
        "entries": entries,
        "boundary": BOUNDARY,
    }
    return payload, manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("evidence", "final"), required=True)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload, manifest = review(args.stage)
    if args.write:
        target = PHASE / "validation"
        target.mkdir(parents=True, exist_ok=True)
        (target / f"{args.stage}-staged-review.json").write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        (target / f"{args.stage}-staged-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"stage": args.stage, "files": payload["staged_file_count"], "json": payload["json_parse_count"], "privacy_hits": payload["privacy_confirmed_hit_count"], "manifest_entries": manifest["entry_count"], "issues": len(payload["issues"]), "valid": payload["valid"]}))
    return 0 if payload["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
