#!/usr/bin/env python3
"""Owner-scoped precommit validation for the Vesper v689-v7-r2 x1 delta."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path


PLANNING = "45650de06f1fb5a9d0bca7fc1a97cf2f8ed22bca"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    phase = root / "docs/vesper-arlen/v689-v7-r2"
    x1 = phase / "x1"
    results = load(x1 / "results.json")
    cleanup = load(x1 / "cleanup-receipt.json")
    skills = load(x1 / "skill-validation.json")
    runners = load(x1 / "runner-smokes.json")
    packages = load(x1 / "package-smoke-receipt.json")
    manifest = load(x1 / "manifest.json")
    assert len(results["safe_results"]) == 100
    assert len(results["candidate_results"]) == 100
    assert all(row["result"] == "pass" and row["input_unchanged"] for row in results["safe_results"])
    assert all(row["failed_subject"] and row["original_success_credit"] == 0 and row["refusal_check"] == "pass" for row in results["candidate_results"])
    assert cleanup["count"] == 100 and all(row["result"] == "pass" for row in cleanup["results"])
    assert skills["count"] == 10 and all(row["accepted"] for row in skills["quick_validate"])
    assert runners["count"] == 10 and all(row["positive"] and row["adverse_refusal"] for row in runners["smokes"])
    assert all(row["result"] == "pass" for row in packages["positive"])
    assert all(row["refusal_check"] == "pass" and row["original_success_credit"] == 0 for row in packages["adverse"])
    assert not (phase / "x2").exists()

    mismatches = []
    python_files = []
    for row in manifest["entries"]:
        path = root / row["path"]
        data = path.read_bytes().replace(b"\r\n", b"\n")
        if len(data) != row["bytes_normalized_lf"] or hashlib.sha256(data).hexdigest() != row["sha256_normalized_lf"]:
            mismatches.append(row["path"])
        if path.suffix == ".py":
            ast.parse(path.read_text(encoding="utf-8"))
            python_files.append(path)
    assert not mismatches

    json_files = list(phase.rglob("*.json"))
    for path in json_files:
        load(path)
    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_user_root": re.compile(r"[A-Z]:\\Users\\[^\\\s]+", re.I),
        "private_uri": re.compile(r"(?:plugin|app)://", re.I),
        "delegation_markup": re.compile(r"<codex_delegation>", re.I),
        "credential_assignment": re.compile(r"(?:api[_-]?key|secret|token)\s*[:=]\s*[\"'][^\"']+", re.I),
    }
    privacy_hits = []
    definition_candidates = []
    text_files = []
    for row in manifest["entries"]:
        path = root / row["path"]
        if path.suffix.lower() not in {".json", ".md", ".py", ".lock"}:
            continue
        text = path.read_text(encoding="utf-8")
        text_files.append(path)
        for name, pattern in patterns.items():
            if pattern.search(text):
                candidate = {"class": name, "path": row["path"]}
                if path.resolve() == Path(__file__).resolve():
                    definition_candidates.append(candidate)
                else:
                    privacy_hits.append(candidate)
    assert not privacy_hits
    dangerous = []
    for path in python_files:
        text = path.read_text(encoding="utf-8")
        for pattern in [r"\beval\s*\(", r"\bexec\s*\(", r"shell\s*=\s*True", r"pickle\.loads", r"yaml\.load\s*\("]:
            if re.search(pattern, text):
                dangerous.append({"path": path.relative_to(root).as_posix(), "pattern": pattern})
    assert not dangerous
    diff = subprocess.run(["git", "-C", str(root), "diff", "--exit-code", PLANNING, "--", "docs/vesper-arlen/v689-v7-r2/plan"], capture_output=True, check=False)
    assert diff.returncode == 0
    print(json.dumps({"status": "VALID_X1_PRECOMMIT_OWNER_DELTA", "safe": 100, "candidate_failed_subjects": 100, "candidate_refusal_checks": 100, "clean_fix_refine": 100, "skills": 10, "runner_operation_smokes": 10, "manifest_entries": manifest["entry_count"], "json_documents": len(json_files), "python_asts": len(python_files), "privacy_text_files": len(text_files), "privacy_definition_candidates": definition_candidates, "privacy_hits": 0, "security_findings": 0, "x2_absent": True, "planning_unchanged": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
