#!/usr/bin/env python3
"""Run the sole successful canonical scoped validation for v648-v6."""

from __future__ import annotations

import argparse
import io
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
PHASE = ROOT / "docs" / "orin-thale" / "v648-v6"
MODULES = [
    "tests.test_ghc_family_v648_v5_x1",
    "tests.test_ghc_family_v648_v5",
    "tests.test_ghc_family_v648_v5_closeout",
    "tests.test_ghc_family_v648_v6_x1",
    "tests.test_ghc_family_v648_v6",
    "tests.test_ghc_family_v648_v6_closeout",
]
X1 = "3f6a64d239bdde1c38fea166db5eff0f2f3e1d89"
SOURCE = "5725217126e85b849be63f932e5e79fb4e956698"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def phase_files() -> list[Path]:
    return sorted(path for path in PHASE.rglob("*") if path.is_file())


def privacy(files: list[Path]) -> tuple[int, list[dict[str, str]]]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {
        "validation/x1-staged-privacy.json",
        "validation/evidence-staged-privacy.json",
        "validation/final-staged-privacy.json",
    }
    hits = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        relative = path.relative_to(PHASE).as_posix()
        for pattern_class, pattern in patterns.items():
            if pattern.search(text) and relative not in definitions:
                hits.append({"path": relative, "pattern_class": pattern_class})
    return len(patterns), hits


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=PHASE / "validation/canonical-pass-result.json")
    parser.add_argument("--selection-only", action="store_true")
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromNames(MODULES)
    selected = suite.countTestCases()
    if selected != 67:
        raise RuntimeError(f"expected 67 selected tests, found {selected}")
    if args.selection_only:
        print(json.dumps({"selected_tests": selected, "modules": MODULES, "tests_executed": 0}, sort_keys=True))
        return
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    if not result.wasSuccessful():
        sys.stderr.write(stream.getvalue())
        raise RuntimeError(f"canonical scoped tests failed failures={len(result.failures)} errors={len(result.errors)}")
    files = phase_files()
    json_files = [path for path in files if path.suffix.casefold() == ".json"]
    for path in json_files:
        json.loads(path.read_text(encoding="utf-8"))
    pattern_count, hits = privacy(files)
    if hits:
        raise RuntimeError(f"canonical privacy hits: {hits}")
    outcomes = load("x2/core-outcome-ledger.json")
    negatives = load("x2/retained-negative-register.json")
    gates = load("x2/gate-register.json")
    skills = load("x2/skill-use-ledger-final.json")
    runners = load("x2/runner-use-ledger-final.json")
    checklist = load("complete-incomplete-checklist.json")
    plan = load("validation/final-validation-plan.json")
    x1_manifest = load("validation/x1-staged-manifest.json")
    evidence_manifest = load("validation/evidence-staged-manifest.json")
    detailed = [
        git("merge-base", "--is-ancestor", SOURCE, X1) == "",
        git("merge-base", "--is-ancestor", X1, git("rev-parse", "HEAD")) == "",
        git("rev-list", "--count", f"{SOURCE}..{X1}") == "1",
        git("rev-list", "--merges", f"{SOURCE}..{git('rev-parse','HEAD')}") == "",
        outcomes["proposal_count"] == 10,
        outcomes["distribution"] == {"completed":6,"represented":2,"open_gap":1,"exact_gate":1},
        outcomes["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        negatives["effective_at_evidence"] == 4473 and negatives["effective_current"] == 4482 and negatives["x2_operational"] == 22 and negatives["evidence_commit_declared_effective"] == 4471 and negatives["evidence_discrepancy_retained"] is True,
        negatives["negative_erased"] is False,
        gates["effective_open_gaps"] == 32,
        gates["effective_exact_gates"] == 33,
        gates["silently_closed"] == 0,
        skills["completed_count"] == 20,
        skills["pending_count"] == 0,
        runners["completed_count"] == 10,
        runners["pending_count"] == 0,
        load("approval-packets/x2-safe-now-results.json")["completed_count"] == 30,
        load("prototypes/x2-candidate-results.json")["completed_count"] == 20,
        load("maintenance/x2-clean-refine-results.json")["completed_count"] == 30,
        load("validation/x2-synthetic-mutation-results.json")["rejected_count"] == 70,
        load("approval-packets/inherited-held-packets.json")["executed_count"] == 0,
        load("stage20-terminal-board.json")["ready"] is False,
        load("closeout/closeout-candidate.json")["terminal_route"] == "PREPARED_NOT_SENT",
        load("orchestration/final-phase-state.json")["subagents"] == 0,
        load("orchestration/final-phase-state.json")["tasks_created"] == 0,
        load("orchestration/final-phase-state.json")["cross_platform_messages"] == 0,
        plan["full_repository_suite"] is False,
        plan["replay_budget"] == 0,
        len(x1_manifest["entries"]) + len(x1_manifest["self_exclusions"]) == 82,
        len(evidence_manifest["entries"]) + len(evidence_manifest["self_exclusions"]) > 100,
        "stage20" in checklist["incomplete"],
        all(len(path.read_text(encoding="utf-8").split()) <= 6000 for path in list(PHASE.rglob("*.md")) + list(PHASE.rglob("*.html"))),
    ]
    if len(detailed) != 32 or not all(detailed):
        raise RuntimeError(f"detailed validation failed: {[i+1 for i,value in enumerate(detailed) if not value]}")
    minimal = [
        selected == 67,
        result.testsRun == 67,
        len(result.failures) == 0,
        len(result.errors) == 0,
        len(json_files) > 100,
        pattern_count == 5,
        len(hits) == 0,
        outcomes["distribution"]["completed"] == 6,
        outcomes["distribution"]["represented"] == 2,
        outcomes["distribution"]["open_gap"] == 1,
        outcomes["distribution"]["exact_gate"] == 1,
        load("retained-negative-register-final.json")["negative_erased"] is False,
        load("exact-open-gate-register-final.json")["silently_closed"] == 0,
        len((PHASE / "integrated-overview.md").read_text(encoding="utf-8").split()) >= 1200,
        4000 <= len((PHASE / "handoffs/tamar-vey-v648-v7-activation.md").read_text(encoding="utf-8").split()) <= 6000,
        (PHASE / "accessible-report.html").is_file(),
        (PHASE / "threat-model.json").is_file(),
        (PHASE / "complete-incomplete-checklist.json").is_file(),
        plan["canonical_successful_pass_budget"] == 1,
        plan["successful_passes_used"] == 0,
    ]
    if len(minimal) != 20 or not all(minimal):
        raise RuntimeError(f"minimal validation failed: {[i+1 for i,value in enumerate(minimal) if not value]}")
    payload = {
        "schema":"ghc.family.v648-v6.canonical-pass.v1",
        "selected_modules":MODULES,
        "tests_selected":selected,
        "tests_run":result.testsRun,
        "tests_passed":result.testsRun,
        "detailed_checks":32,
        "detailed_passed":32,
        "minimal_checks":20,
        "minimal_passed":20,
        "phase_json_parses":len(json_files),
        "privacy_scanned_files":len(files),
        "privacy_pattern_classes":5,
        "privacy_confirmed_hits":0,
        "full_repository_suite":False,
        "successful_canonical_pass_number":1,
        "replay_used":False,
        "same_owner_only":True,
        "independent_reproduction":False,
        "terminal_verdict":"NOT_READY_FOR_STAGE_20",
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
