#!/usr/bin/env python3
"""Owner-scoped precommit validation for the Vesper v689-v7-r2 x2 delta."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

X1 = "b51e595c823a381ca88b7bfe69339cab8baf05d0"
IMAGE_SHA256 = "3995cfe63b709db0966832b3c95dbe6c18a68d2c06b04f5372b07f4e4b5ff570"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    phase = root / "docs/vesper-arlen/v689-v7-r2"
    x2 = phase / "x2"
    results = load(x2 / "results.json")
    cleanup = load(x2 / "cleanup-receipt.json")
    skills = load(x2 / "skill-validation.json")
    runners = load(x2 / "runner-smokes.json")
    comparisons = load(x2 / "package-comparisons.json")
    image = load(x2 / "image-receipt.json")
    deck = load(phase / "deck/deck-index.json")
    card_manifest = load(phase / "deck/card-manifest.json")
    flow = load(x2 / "method-flow.json")
    promotion = load(x2 / "global-promotion-receipt.json")
    manifest = load(x2 / "manifest.json")

    assert len(results["safe_results"]) == 100 and len(results["candidate_results"]) == 100
    assert Counter(row["outcome"] for row in results["safe_results"]) == {"completed": 80, "represented": 10, "open_gap": 5, "exact_gate": 5}
    assert all(row["result"] == "pass" and row["input_unchanged"] for row in results["safe_results"])
    assert all(row["failed_subject"] and row["original_success_credit"] == 0 and row["refusal_check"] == "pass" for row in results["candidate_results"])
    assert cleanup["count"] == 100 and all(row["result"] == "pass" for row in cleanup["results"])
    assert skills["owner_local_count"] == 10 and skills["merged_candidate_count"] == 5
    assert all(row["accepted"] for row in skills["owner_local"] + skills["merged_candidates"])
    assert runners["local_count"] == 10 and runners["merged_count"] == 5
    assert all(row["positive"] and row["adverse_refusal"] for row in runners["local_smokes"])
    assert all(row["result"] == "pass" for row in runners["merged_candidate_smokes"])
    assert comparisons["count"] == 30 and all(row["result"] == "pass" for row in comparisons["comparisons"])
    image_path = root / image["file"]
    assert image["sha256"] == IMAGE_SHA256 == hashlib.sha256(image_path.read_bytes()).hexdigest()
    assert image["role"] == "non_evidentiary_source_faithful_ledger_companion"
    assert promotion["skills_installed"] == 5 and promotion["runners_installed"] == 5
    assert promotion["overwrites"] == 0 and promotion["all_byte_parity"] and promotion["all_validated"] and promotion["all_smoked"]

    assert deck["counts"] == {"cards": 208, "tier1": 1, "tier2": 3, "tier3": 4, "tier4": 200}
    cards = [load(phase / "deck/cards" / f"{card_id}.json") for card_id in deck["card_ids"]]
    by_id = {row["card_id"]: row for row in cards}
    assert len(by_id) == 208
    for card in cards:
        if card["tier"] == 1:
            assert card["parent_ids"] == []
        else:
            assert len(card["parent_ids"]) == 1
            assert by_id[card["parent_ids"][0]]["tier"] == card["tier"] - 1
        assert card["outcome"] in {"completed", "represented", "open_gap", "exact_gate"}
    for row in card_manifest["entries"]:
        path = root / row["path"]
        data = path.read_bytes()
        assert len(data) == row["bytes"] and hashlib.sha256(data).hexdigest() == row["sha256"]

    assert len(flow["methods"]) == 20 and len(flow["witnesses"]) == 600
    witness_ids = {row["witness_id"] for row in flow["witnesses"]}
    assert all(set(row["validation_witness_ids"]) <= witness_ids and row["validation_witness_ids"] for row in flow["methods"])

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
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.IGNORECASE),
        "private_user_root": re.compile(r"[A-Z]:\\Users\\[^\\\s]+", re.IGNORECASE),
        "private_uri": re.compile(r"(?:plugin|app)://", re.IGNORECASE),
        "delegation_markup": re.compile(r"<codex_delegation>", re.IGNORECASE),
        "credential_assignment": re.compile(r"(?:api[_-]?key|secret|token)\s*[:=]\s*[\"'][^\"']+", re.IGNORECASE),
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
    for preserved in ["docs/vesper-arlen/v689-v7-r2/plan", "docs/vesper-arlen/v689-v7-r2/x1"]:
        diff = subprocess.run(["git", "-C", str(root), "diff", "--exit-code", X1, "--", preserved], capture_output=True, check=False)
        assert diff.returncode == 0
    print(json.dumps({"status": "VALID_X2_PRECOMMIT_OWNER_DELTA", "safe": 100, "candidate_failed_subjects": 100, "candidate_refusal_checks": 100, "clean_fix_refine": 100, "owner_local_skills": 10, "merged_skills": 5, "local_runner_operation_smokes": 10, "merged_runner_smokes": 5, "package_comparisons": 30, "deck_cards": 208, "manifest_entries": manifest["entry_count"], "json_documents": len(json_files), "python_asts": len(python_files), "privacy_text_files": len(text_files), "privacy_definition_candidates": definition_candidates, "privacy_hits": 0, "security_findings": 0, "x1_unchanged": True, "planning_unchanged": True, "global_promotions": 5}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
