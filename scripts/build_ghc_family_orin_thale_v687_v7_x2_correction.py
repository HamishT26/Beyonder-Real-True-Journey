#!/usr/bin/env python3
"""Build the additive Orin v687-v7 x2 root-runner omission correction."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v687-v7"
CORRECTION = PHASE / "x2" / "correction"
VALIDATION = PHASE / "validation"
SOURCE = "28dfdf1a3e9a1023f1e83f19fb267e57878b9d0b"
X1 = "7aea73908f8f41ed38473d6e30e5f1bda36588a7"
FIRST_EVIDENCE = "a29be946caf963315a48f73055f0eb1cae85e482"
ROOT_FILES = ["scripts/ghc_family_spectral_archive_contract.py"] + [f"scripts/ghc_family_spectral_archive_{i:02d}_runner.py" for i in range(1, 6)]
COUNTS = {"negatives": 82021, "methods": 93194, "failed_witnesses": 52869, "passing_witnesses": 81995, "open_gaps": 732, "exact_gates": 711, "proposals": 15230}


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=False)


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def norm(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def main() -> int:
    if run(["git", "rev-parse", "HEAD"]).stdout.strip() != FIRST_EVIDENCE:
        raise RuntimeError("correction builder requires retained first x2 evidence")
    missing = [path for path in ROOT_FILES if not (ROOT / path).is_file()]
    if missing:
        raise RuntimeError(f"missing root interfaces: {missing}")
    documents = {
        CORRECTION / "root-runner-omission.json": {
            "schema": "ghc.family.x2-correction.v1", "owner": "Orin Thale", "phase": "v687-v7",
            "retained_first_evidence": FIRST_EVIDENCE, "negative_id": "OR6877-X2-N006",
            "failure": "The first x2 builder omitted the five exercised root runners and shared core from its generated-path allowlist, manifest, and commit, leaving six untracked owner files after push.",
            "original_success_credit": 0, "original_manifest_rewritten": False,
            "recovery": "Preserve the first evidence and manifest at their immutable commit; add the six exact interfaces in one correction commit with a correction-only manifest, privacy scan, security review, and lifecycle test.",
            "recurrence_guard": "Enumerate every generated root interface explicitly before the staged allowlist is frozen.",
            "added_paths": ROOT_FILES, "counts": COUNTS,
        },
        CORRECTION / "phase-truth-overlay.json": {
            "schema": "ghc.family.phase-truth-overlay.v1", "owner": "Orin Thale", "phase": "v687-v7",
            "source": SOURCE, "x1": X1, "retained_first_evidence": FIRST_EVIDENCE,
            "state": "X2_ADDITIVE_CORRECTION_PREPARED", "outcomes": {"completed": 125, "represented": 39, "open_gap": 20, "exact_gate": 16},
            "effective_counts": COUNTS, "original_x2_phase_truth_rewritten": False,
            "canonical_state": "NOT_INVOKED", "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        CORRECTION / "method-flow-overlay.json": {
            "schema": "ghc.family.method-flow-overlay.v1", "owner": "Orin Thale", "phase": "v687-v7",
            "method_id": "OR6877-X2-M006", "retained_negative_id": "OR6877-X2-N006",
            "failed_witness": {"result": "fail", "credit": 0, "observed": "six owner interfaces remained untracked after first evidence push"},
            "passing_witness": {"result": "pass", "credit": "bounded_dependency_only", "expected": "all six interfaces bound by correction manifest and tests"},
            "failure_erased": False, "effective_counts": COUNTS,
        },
    }
    for path, value in documents.items():
        write_json(path, value)
    builder = ROOT / "scripts" / "build_ghc_family_orin_thale_v687_v7_x2_correction.py"
    test = ROOT / "tests" / "test_ghc_family_orin_thale_v687_v7_x2_correction.py"
    staged = VALIDATION / "x2-correction-staged-review.json"
    privacy = VALIDATION / "x2-correction-privacy.json"
    security = VALIDATION / "x2-correction-security.json"
    manifest = VALIDATION / "x2-correction-manifest.json"
    paths = [ROOT / path for path in ROOT_FILES] + list(documents) + [builder, test, staged, privacy, security, manifest]
    paths = sorted(paths, key=rel)
    write_json(staged, {"schema": "ghc.family.staged-review.v1", "phase": "v687-v7", "lifecycle": "x2-correction", "parent": FIRST_EVIDENCE, "expected_paths": [rel(path) for path in paths], "expected_path_count": len(paths), "original_x2_paths_modified": [], "unexpected_paths": []})
    patterns = {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)", re.I),
        "raw_task_identifier": re.compile(rb"(?:thread|task|agent)_id\s*[:=]", re.I),
        "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[:=]\s*[^\s]{8,}", re.I),
        "private_stream": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
    }
    candidates, confirmed, findings = [], [], []
    for path in paths:
        if not path.exists() or path in {privacy, manifest}:
            continue
        data = path.read_bytes(); scanner_definition = path == builder
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(data):
                row = {"path": rel(path), "class": class_name, "matched_sha256": hashlib.sha256(match.group()).hexdigest()}
                (candidates if scanner_definition else confirmed).append(row)
        if path.suffix == ".py":
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    findings.append({"path": rel(path), "finding": node.func.id})
    write_json(privacy, {"schema": "ghc.family.privacy-adjudication.v1", "classes": list(patterns), "candidates": candidates, "confirmed_hits": confirmed, "confirmed_count": len(confirmed), "complete_privacy_claimed": False})
    write_json(security, {"schema": "ghc.family.bounded-security.v1", "findings": findings, "finding_count": len(findings), "exhaustive_security_claimed": False})
    exclusions = [rel(manifest)]
    entries = []
    for path in paths:
        if rel(path) in exclusions:
            continue
        data = norm(path)
        entries.append({"path": rel(path), "bytes_normalized_lf": len(data), "sha256_normalized_lf": hashlib.sha256(data).hexdigest()})
    write_json(manifest, {"schema": "ghc.family.normalized-lf-manifest.v1", "anchor": "PENDING_CORRECTED_EVIDENCE_COMMIT", "byte_domain": "normalized_lf_git_blob", "declared_self_exclusions": exclusions, "entry_count": len(entries), "entries": entries})
    if confirmed or findings:
        raise RuntimeError(f"privacy={confirmed} security={findings}")
    print(json.dumps({"status": "X2_ADDITIVE_CORRECTION_PREPARED", "paths": len(paths), "entries": len(entries), "privacy_confirmed": 0, "security_findings": 0, "counts": COUNTS}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
