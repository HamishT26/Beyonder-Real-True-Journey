#!/usr/bin/env python3
"""Run the one allowed successful canonical scoped pass for Sylven v648-v8."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sylven-arc" / "v648-v8"
SOURCE = "33c8f87a4037c81c3abca540b8c5db1d91328420"
X1 = "d86990f673aa82c45a5296ebba88c79a6dc3bde4"
EVIDENCE = "1e85a9e714ac2509095fac03aedf704b4892d8b3"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from ghc_family_v648_v8_staged_review import PRIVACY_PATTERNS, scanner_definition


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def ids(suite: unittest.TestSuite) -> list[str]:
    rows: list[str] = []
    for item in suite:
        rows.extend(ids(item) if isinstance(item, unittest.TestSuite) else [item.id()])
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = load("validation/final-validation-plan.json")
    if plan["successful_passes_used"] != 0 or plan["canonical_successful_pass_budget"] != 1:
        raise RuntimeError("canonical successful-pass budget is not available")
    selected = [name for name in ids(unittest.defaultTestLoader.loadTestsFromNames(plan["test_modules"])) if name not in set(plan["excluded_source_local_tests"])]
    if len(selected) != plan["selected_test_count"]:
        raise RuntimeError(f"expected {plan['selected_test_count']} selected tests, found {len(selected)}")
    run = subprocess.run([sys.executable, "-B", "-m", "unittest", *selected], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    combined = run.stdout + run.stderr
    if run.returncode:
        raise RuntimeError(combined[-6000:])
    match = re.search(r"Ran (\d+) tests", combined)
    test_count = int(match.group(1)) if match else -1
    files = sorted(path for path in PHASE.rglob("*") if path.is_file())
    json_files = [path for path in files if path.suffix.casefold() == ".json"]
    for path in json_files:
        json.loads(path.read_text(encoding="utf-8"))
    candidates: list[dict[str, str]] = []
    definitions: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for path in files:
        try:
            data = path.read_bytes()
            data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(ROOT).as_posix()
        for name, pattern in PRIVACY_PATTERNS.items():
            for found in pattern.finditer(data):
                line_start = data.rfind(b"\n", 0, found.start()) + 1
                line_end = data.find(b"\n", found.end())
                if line_end < 0:
                    line_end = len(data)
                row = {"path":rel,"pattern_class":name}
                candidates.append(row)
                if scanner_definition(rel, data[line_start:line_end]):
                    definitions.append(row)
                else:
                    confirmed.append(row)
    if confirmed:
        raise RuntimeError(f"privacy confirmed hits: {confirmed}")
    detailed = [
        git("rev-parse", "HEAD") == EVIDENCE,
        git("rev-parse", "HEAD^") == X1,
        git("rev-list", "--count", f"{SOURCE}..HEAD") == "2",
        git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD") == "0",
        git("rev-parse", "@{upstream}") == EVIDENCE,
        subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT).returncode == 0,
        load("x2/core-outcome-ledger.json")["distribution"] == {"completed":6,"represented":2,"open_gap":1,"exact_gate":1},
        load("x2/evidence-ledger.json")["real_rows"] == 0,
        load("x2/evidence-ledger.json")["real_participants_or_operators"] == 0,
        load("x2/evidence-ledger.json")["real_keys_tokens_or_services"] == 0,
        load("x2/evidence-ledger.json")["authority_decisions"] == 0,
        load("x2/evidence-ledger.json")["effect_estimates"] == 0,
        load("x2/evidence-ledger.json")["network_queries_or_downloads"] == 0,
        load("x2/portfolio-ledger.json")["safe_completed"] == 30,
        load("x2/portfolio-ledger.json")["candidates_completed"] == 20,
        load("x2/skill-use-ledger.json")["completed_count"] == 20,
        load("x2/runner-use-ledger.json")["completed_count"] == 10,
        load("x2/portfolio-ledger.json")["clean_refine_completed"] == 30,
        load("x2/portfolio-ledger.json")["inherited_completion_credit"] == 0,
        load("validation/x2-synthetic-mutation-results.json")["count"] == 70,
        load("validation/x2-synthetic-mutation-results.json")["rejected_count"] == 70,
        load("exact-open-gate-register-final.json")["effective_open_gaps"] == 34,
        load("exact-open-gate-register-final.json")["effective_exact_gates"] == 35,
        load("stage20-terminal-board.json")["ready"] is False,
        load("phase-truth-final-candidate.json")["terminal_route"] == "PREPARED_NOT_SENT",
        load("validation/final-staged-review.json")["passed"] is True,
        load("validation/final-staged-privacy.json")["confirmed_hit_count"] == 0,
        load("validation/final-staged-manifest.json")["entry_count"] > 0,
        load("closeout/closeout-build-receipt.json")["overview_three_page_equivalent"] is True,
        (PHASE / "accessible-report.html").is_file(),
        "stage20" in load("complete-incomplete-checklist.json")["incomplete"],
        load("orchestration/final-phase-state.json")["subagents"] == 0,
        load("orchestration/final-phase-state.json")["tasks_created"] == 0,
        plan["full_repository_suite"] is False,
        plan["replay_budget"] == 0,
        load("x2/evidence-ledger.json")["independent_reproduction"] is False,
        load("method-flow/method-flow-validation.json")["valid"] is True,
    ]
    minimal = [
        len(load("x1-proposals.json")["proposals"]) == 10,
        load("provenance/frozen-chain-proposal-index.json")["count"] == 640,
        load("x2/core-outcome-ledger.json")["count"] == 10,
        load("x2/skill-use-ledger.json")["skill_count"] == 20,
        load("x2/runner-use-ledger.json")["runner_count"] == 10,
        load("validation/x2-synthetic-mutation-results.json")["count"] == 70,
        len(PRIVACY_PATTERNS) == 5,
        len(confirmed) == 0,
        len(json_files) > 100,
        len(files) < 15000,
        load("phase-truth-final-candidate.json")["full_suite_used"] is False,
        load("phase-truth-final-candidate.json")["replay_used"] is False,
        load("stage20-terminal-board.json")["verdict"] == "NOT_READY_FOR_STAGE_20",
        load("exact-open-gate-register-final.json")["silently_closed"] == 0,
        load("wellbeing-closeout.json")["pause_right_preserved"] is True,
        load("closeout/closeout-candidate.json")["x1_commit"] == X1,
        load("validation/final-staged-review.json")["blob_capture_passed"] is True,
        load("validation/final-staged-review.json")["path_scope_passed"] is True,
        load("validation/final-staged-review.json")["diff_hygiene_passed"] is True,
        load("retained-negative-register-final.json")["negative_erased"] is False,
        load("retained-negative-register-final.json")["effective_total"] >= 4665,
        load("method-flow/method-flow-summary.json")["counts"]["witness_results"]["fail"] >= 14,
    ]
    if len(detailed) != plan["detailed_check_count"] or len(minimal) != plan["minimal_check_count"]:
        raise RuntimeError(f"validator count contract mismatch: {len(detailed)} detailed, {len(minimal)} minimal")
    if not all(detailed) or not all(minimal):
        raise RuntimeError(f"detailed={sum(detailed)}/{len(detailed)} minimal={sum(minimal)}/{len(minimal)}")
    payload = {"schema":"ghc.family.v648-v8.canonical-validation.external.v1","passed":True,"test_count":test_count,"detailed_passed":sum(detailed),"detailed_total":len(detailed),"minimal_passed":sum(minimal),"minimal_total":len(minimal),"json_parses":len(json_files),"privacy_scanned_files":len(files),"privacy_pattern_classes":len(PRIVACY_PATTERNS),"privacy_candidates":len(candidates),"privacy_scanner_definition_candidates":len(definitions),"privacy_confirmed_hits":0,"full_suite":False,"replay":False,"candidate_head":git("rev-parse", "HEAD"),"candidate_staged_tree":git("write-tree"),"same_owner_only":True,"independent_reproduction":False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
