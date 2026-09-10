#!/usr/bin/env python3
"""Precommit validation for Vesper v689-v7-r2 final closeout."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader

X2 = "4cd2850ac7eb40b38f3b3e4b8046a5e8ae07aafa"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--canonical-latch", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    phase = root / "docs/vesper-arlen/v689-v7-r2"
    final = phase / "final"
    truth = load(final / "phase-truth.json")
    baton_index = load(final / "baton-module-index.json")
    flow = load(final / "method-flow-final.json")
    retained = load(final / "retained-negative-ledger.json")
    route = load(final / "terminal-route-candidate.json")
    manifest = load(final / "manifest.json")
    seal = load(final / "content-seal.json")
    assert truth["outcomes"] == {"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5}
    assert set(truth["outcomes"]) == ALLOWED_OUTCOMES
    assert truth["safe_tasks"] == truth["candidate_failed_subjects"] == truth["candidate_refusal_checks"] == truth["clean_fix_refine"] == 200
    assert truth["skills"] == 20 and truth["runners"] == 10 and truth["global_skills"] == truth["global_runners"] == 5
    assert truth["canonical_state"] == "NOT_INVOKED" and truth["delivery_state"] == "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"
    assert 10000 <= baton_index["baton_words"] <= 100000 and baton_index["module_count"] == 13
    assert len((final / "overview.md").read_text(encoding="utf-8").split()) >= 1800
    assert len(PdfReader(str(final / "overview.pdf")).pages) >= 3
    assert route["send_attempts"] == route["messages_sent"] == route["resends"] == 0
    assert route["exact_title"] == "Ilyan Reed" and route["recipient_phase"] == "v689-v8"
    assert retained["erased"] == 0 and retained["effective_negatives"] >= 500
    assert len(flow["methods"]) == 21 and len(flow["witnesses"]) == 644
    witness_ids = {row["witness_id"] for row in flow["witnesses"]}
    assert all(row["validation_witness_ids"] and set(row["validation_witness_ids"]) <= witness_ids for row in flow["methods"])
    assert not args.canonical_latch.exists()

    manifest_bad = []
    python_files = []
    for row in manifest["entries"]:
        path = root / row["path"]
        data = path.read_bytes().replace(b"\r\n", b"\n")
        if len(data) != row["bytes_normalized_lf"] or hashlib.sha256(data).hexdigest() != row["sha256_normalized_lf"]:
            manifest_bad.append(row["path"])
        if path.suffix == ".py":
            ast.parse(path.read_text(encoding="utf-8"))
            python_files.append(path)
    assert not manifest_bad
    seal_bad = []
    for row in seal["entries"]:
        path = root / row["path"]
        data = path.read_bytes().replace(b"\r\n", b"\n")
        if len(data) != row["bytes_normalized_lf"] or hashlib.sha256(data).hexdigest() != row["sha256_normalized_lf"]:
            seal_bad.append(row["path"])
    assert not seal_bad

    json_files = list(phase.rglob("*.json"))
    for path in json_files:
        load(path)
    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.IGNORECASE),
        "private_user_root": re.compile(r"[A-Z]:\\Users\\[^\\\s]+", re.IGNORECASE),
        "private_uri": re.compile(r"(?:plugin|app)://", re.IGNORECASE),
        "delegation_markup": re.compile(r"<codex_delegation>", re.IGNORECASE),
        "credential_assignment": re.compile(r"(?:api[_-]?key|secret|token)\s*[:=]\s*[\"'][^\"']+", re.IGNORECASE),
    }
    privacy_hits = []
    definition_candidates = []
    text_files = []
    for path in [root / row["path"] for row in seal["entries"]]:
        if path.suffix.lower() not in {".json", ".md", ".py", ".html", ".lock"}:
            continue
        text = path.read_text(encoding="utf-8")
        text_files.append(path)
        for name, pattern in patterns.items():
            if pattern.search(text):
                candidate = {"class": name, "path": path.relative_to(root).as_posix()}
                if path.suffix == ".py" and ("validate" in path.name or "canonical" in path.name):
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
    for preserved in ["docs/vesper-arlen/v689-v7-r2/plan", "docs/vesper-arlen/v689-v7-r2/x1", "docs/vesper-arlen/v689-v7-r2/x2"]:
        result = subprocess.run(["git", "-C", str(root), "diff", "--exit-code", X2, "--", preserved], capture_output=True, check=False)
        assert result.returncode == 0
    tracked = subprocess.run(["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard"], text=True, encoding="utf-8", capture_output=True, check=True).stdout.splitlines()
    assert len(tracked) < 2000
    print(json.dumps({"status": "VALID_FINAL_PRECOMMIT_OWNER_DELTA", "outcomes": truth["outcomes"], "baton_words": baton_index["baton_words"], "modules": 13, "overview_words": truth["overview_words"], "pdf_pages": len(PdfReader(str(final / "overview.pdf")).pages), "manifest_entries": manifest["entry_count"], "content_seal_entries": seal["entry_count"], "json_documents": len(json_files), "python_asts": len(python_files), "privacy_text_files": len(text_files), "privacy_definition_candidates": definition_candidates, "privacy_hits": 0, "security_findings": 0, "tracked_files": len(tracked), "planning_x1_x2_unchanged": True, "canonical_not_invoked": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
