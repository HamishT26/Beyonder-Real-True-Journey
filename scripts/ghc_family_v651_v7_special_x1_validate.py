#!/usr/bin/env python3
"""Validate the frozen x1-only Vesper v651-v7 special preparation packet."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/vesper-arlen/v651-v7-special-cli-prep"
RECEIPT = PHASE / "validation/x1-validation-receipt.json"


def main() -> int:
    issues: list[str] = []
    test = subprocess.run(
        [sys.executable, "-m", "unittest", "tests.test_ghc_family_v651_v7_special_x1"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if test.returncode:
        issues.append("x1 unit tests failed")

    json_files = sorted(PHASE.rglob("*.json"))
    parsed = 0
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
            parsed += 1
        except Exception as exc:  # pragma: no cover - diagnostic boundary
            issues.append(f"json parse failed: {path.relative_to(ROOT).as_posix()}: {type(exc).__name__}")

    patterns = {
        "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
        "private_absolute_path": re.compile(r"(?i)\b[A-Z]:[\\/]"),
        "private_uri": re.compile(r"(?i)\b(?:app|plugin|file|vscode)://"),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*[^\s,}\]]+"),
        "delegation_markup": re.compile(r"(?i)<\s*codex_delegation\b"),
    }
    scanned = 0
    hits: list[dict[str, str]] = []
    for path in sorted(p for p in PHASE.rglob("*") if p.is_file()):
        if path == RECEIPT or path.suffix.lower() not in {".json", ".md", ".txt", ".html", ".yaml", ".yml"}:
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        for name, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"path": path.relative_to(ROOT).as_posix(), "class": name})
    if hits:
        issues.append("privacy scan found confirmed candidates")

    proposals = json.loads((PHASE / "preregistration/proposals.json").read_text(encoding="utf-8"))
    if len(proposals["proposals"]) != 30 or proposals["frozen_rows_after_x1"] != 1120:
        issues.append("proposal freeze mismatch")
    novelty = json.loads((PHASE / "provenance/semantic-novelty-audit.json").read_text(encoding="utf-8"))
    if not novelty["valid"] or novelty["inherited_rows_checked"] != 1090:
        issues.append("novelty audit mismatch")
    raw = json.loads((PHASE / "workflow/raw-audit/workflow-plan-refinement.json").read_text(encoding="utf-8"))
    normalized = json.loads((PHASE / "workflow/normalized-audit/workflow-plan-refinement.json").read_text(encoding="utf-8"))
    if raw["valid"] or raw["counts"]["errors"] != 2:
        issues.append("raw route failure not retained")
    if not normalized["valid"] or normalized["counts"]["errors"]:
        issues.append("normalized candidate did not pass structurally")
    method = json.loads((PHASE / "method-flow/method-flow-summary.json").read_text(encoding="utf-8"))
    if method["counts"]["states"]["preferred"] != 5 or method["counts"]["witness_results"] != {"fail": 5, "pass": 5}:
        issues.append("method-flow counts mismatch")

    forbidden = [PHASE / "outcomes/core-outcomes.json", PHASE / "closeout/closeout-receipt.json", PHASE / "seal/seal-receipt.json"]
    if any(path.exists() for path in forbidden):
        issues.append("x2 or closeout artifact contaminated x1")

    manifest_path = PHASE / "validation/x1-owner-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_mismatches = []
    for row in manifest["entries"]:
        path = ROOT / row["path"]
        if not path.is_file():
            manifest_mismatches.append({"path": row["path"], "reason": "missing"})
            continue
        data = path.read_bytes()
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            manifest_mismatches.append({"path": row["path"], "reason": "content"})
    expected = {
        path.relative_to(ROOT).as_posix()
        for path in PHASE.rglob("*")
        if path.is_file() and path not in {manifest_path, RECEIPT}
    }
    listed = {row["path"] for row in manifest["entries"]}
    if expected != listed or manifest_mismatches:
        issues.append("x1 manifest parity mismatch")

    oversized = []
    for path in sorted(PHASE.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".txt", ".html"}:
            words = len(re.findall(r"\b\w+\b", path.read_text(encoding="utf-8", errors="replace")))
            if words > 100000:
                oversized.append(path.relative_to(ROOT).as_posix())
    materialized_files = sum(1 for path in ROOT.rglob("*") if path.is_file())
    if materialized_files >= 2000:
        issues.append("materialized worktree reached the 2,000-file ceiling")

    payload = {
        "schema": "ghc.family.v651-v7-special.x1-validation.v1",
        "tests": {"passed": test.returncode == 0, "module": "tests.test_ghc_family_v651_v7_special_x1", "test_count": 5},
        "json": {"parsed": parsed, "total": len(json_files)},
        "privacy": {"files_scanned": scanned, "classes": sorted(patterns), "confirmed_hits": hits},
        "manifest": {"entries": len(manifest["entries"]), "mismatches": manifest_mismatches, "path_domain_equal": expected == listed},
        "materialized_files": materialized_files,
        "oversized_documents": oversized,
        "issues": issues,
        "valid": not issues,
        "boundary": "This validates x1 planning and local workflow evidence only; it is not launch authority, independent reproduction, or Stage 20 evidence.",
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
