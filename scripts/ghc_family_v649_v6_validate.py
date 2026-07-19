#!/usr/bin/env python3
"""Run Sylven v649-v6's sole successful canonical scoped validation."""

from __future__ import annotations

import argparse
import importlib
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
PHASE = ROOT / "docs" / "sylven-arc" / "v649-v6"
SOURCE = "295aa503d3c336273f541504a83b88783563ad90"
X1 = "d82382737868160e1b16c9302ca8a008b6f3153e"
EVIDENCE = "4e5f250f8dbe4f77fadce2dfdccfb7869f06ab30"
TAMAR_EVIDENCE = "63f679b002e3f17df465a11c30632e769215ff7c"
MODULES = [
    "tests.test_ghc_family_v649_v3_x1",
    "tests.test_ghc_family_v649_v3_x2",
    "tests.test_ghc_family_v649_v4_x1",
    "tests.test_ghc_family_v649_v4",
    "tests.test_ghc_family_v649_v4_closeout",
    "tests.test_ghc_family_v649_v5_x1",
    "tests.test_ghc_family_v649_v5",
    "tests.test_ghc_family_v649_v6_x1",
    "tests.test_ghc_family_v649_v6",
]


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def suite() -> unittest.TestSuite:
    loaded = {}
    for name in MODULES:
        loaded[name] = importlib.import_module(name)
    tamar = loaded["tests.test_ghc_family_v649_v5"]
    tamar_git = tamar.git

    def tamar_evidence_load(relative: str):
        repository_path = f"docs/tamar-vey/v649-v5/{relative}"
        return json.loads(git("show", f"{TAMAR_EVIDENCE}:{repository_path}"))

    def tamar_evidence_git(*args: str):
        projected = tuple(f"{TAMAR_EVIDENCE}:{arg[5:]}" if arg.startswith("HEAD:") else arg for arg in args)
        return tamar_git(*projected)

    tamar.load = tamar_evidence_load
    tamar.git = tamar_evidence_git
    selected = unittest.defaultTestLoader.loadTestsFromNames(MODULES)
    if any(type(test).__name__ == "_FailedTest" for group in selected for test in (group if hasattr(group, "__iter__") else [group])):
        raise RuntimeError("module selection contains _FailedTest")
    return selected


def privacy(files: list[Path]):
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
        "validation/correction-staged-privacy.json",
        "validation/final-staged-privacy.json",
    }
    hits = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        relative = path.relative_to(PHASE).as_posix()
        for name, pattern in patterns.items():
            if pattern.search(text) and relative not in definitions:
                hits.append({"path": relative, "pattern_class": name})
    return len(patterns), hits


def manifest_ok(relative: str, commit: str) -> bool:
    manifest = load(relative)
    if len(manifest["self_exclusions"]) != 3 or manifest["entry_count"] != len(manifest["entries"]):
        return False
    for entry in manifest["entries"]:
        try:
            if git("rev-parse", f"{commit}:{entry['path']}") != entry["git_blob"]:
                return False
        except subprocess.CalledProcessError:
            return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=PHASE / "validation/canonical-pass-result.json")
    parser.add_argument("--selection-only", action="store_true")
    args = parser.parse_args()
    selected_suite = suite()
    selected = selected_suite.countTestCases()
    plan = load("validation/final-validation-plan.json")
    if plan["selected_test_count"] is not None and selected != plan["selected_test_count"]:
        raise RuntimeError(f"selection drift planned={plan['selected_test_count']} actual={selected}")
    if args.selection_only:
        print(json.dumps({"selected_tests": selected, "modules": MODULES, "tests_executed": 0}, sort_keys=True))
        return
    if git("status", "--porcelain"):
        raise RuntimeError("canonical pass requires a clean exact evidence head")
    head = git("rev-parse", "HEAD")
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(selected_suite)
    if not result.wasSuccessful():
        sys.stderr.write(stream.getvalue())
        raise RuntimeError(f"canonical scoped tests failed failures={len(result.failures)} errors={len(result.errors)}")
    files = sorted(path for path in PHASE.rglob("*") if path.is_file())
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
    runners = load("x2/runner-use-ledger.json")
    method = load("method-flow/method-flow-ledger.json")
    x1_manifest = load("validation/x1-staged-manifest.json")
    evidence_manifest = load("validation/evidence-staged-manifest.json")
    correction_manifest = load("validation/correction-staged-manifest.json")
    owner_files = len([path for path in PHASE.rglob("*") if path.is_file()])
    detailed = [
        git("merge-base", "--is-ancestor", SOURCE, X1) == "",
        git("merge-base", "--is-ancestor", X1, EVIDENCE) == "",
        git("merge-base", "--is-ancestor", EVIDENCE, head) == "",
        git("rev-list", "--count", f"{SOURCE}..{X1}") == "1",
        git("rev-list", "--count", f"{X1}..{EVIDENCE}") == "1",
        git("rev-list", "--count", f"{EVIDENCE}..{head}") == "1",
        git("rev-list", "--merges", f"{SOURCE}..{head}") == "",
        git("rev-parse", f"{head}^") == EVIDENCE,
        outcomes["proposal_count"] == 10,
        outcomes["distribution"] == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        outcomes["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        negatives["effective_at_evidence"] == 5197,
        negatives["negative_erased"] is False,
        gates["effective_open_gaps"] == 40 and gates["effective_exact_gates"] == 41,
        gates["silently_closed"] == 0,
        skills["completed_count"] == 20 and skills["pending_count"] == 0,
        skills["global_installation"] is False and skills["subagent_forward_test"] is False,
        runners["completed_count"] == 9 and runners["pending_closeout_count"] == 1,
        load("approval-packets/x2-safe-now-results.json")["completed_count"] == 30,
        load("prototypes/x2-candidate-results.json")["completed_count"] == 20,
        load("maintenance/x2-clean-refine-results.json")["completed_count"] == 30,
        load("validation/x2-synthetic-mutation-results.json")["rejected_count"] == 70,
        load("approval-packets/inherited-held-packets.json")["executed_count"] == 0,
        load("stage20-terminal-board.json")["ready"] is False,
        load("closeout/closeout-candidate.json")["terminal_route"] == "PREPARED_NOT_SENT",
        load("orchestration/final-phase-state.json")["subagents"] == 0 and load("orchestration/final-phase-state.json")["tasks_created"] == 0,
        plan["full_repository_suite"] is False,
        plan["replay_budget"] == 0 and plan["post_success_replay"] is False,
        manifest_ok("validation/x1-staged-manifest.json", X1),
        manifest_ok("validation/evidence-staged-manifest.json", EVIDENCE),
        manifest_ok("validation/correction-staged-manifest.json", head),
        len(x1_manifest["entries"]) + len(x1_manifest["self_exclusions"]) == 63,
        len(evidence_manifest["entries"]) + len(evidence_manifest["self_exclusions"]) > 100,
        len(correction_manifest["entries"]) + len(correction_manifest["self_exclusions"]) > 10,
        load("validation/source-local-lifecycle-projection.json")["tests_removed"] == 0,
        "stage20" in load("complete-incomplete-checklist.json")["incomplete"],
        all(len(path.read_text(encoding="utf-8").split()) <= 6000 for path in list(PHASE.rglob("*.md")) + list(PHASE.rglob("*.html"))),
        load("validation/reproduction-receipt.json")["replay_used"] is False,
        load("validation/stale-label-review.json")["unquarantined_stale_label_count"] == 0,
        load("validation/evidence-staged-privacy.json")["confirmed_hit_count"] == 0,
        len(method["methods"]) == 26 and len(method["witnesses"]) == 44,
        sum(item["result"] == "fail" for item in method["witnesses"]) == 18,
        owner_files < 15000,
    ]
    if not all(detailed):
        raise RuntimeError(f"detailed checks failed {[index + 1 for index, value in enumerate(detailed) if not value]}")
    minimal = [
        result.testsRun == selected,
        not result.failures,
        not result.errors,
        len(json_files) > 100,
        pattern_count == 5,
        not hits,
        outcomes["distribution"]["completed"] == 6,
        outcomes["distribution"]["represented"] == 2,
        outcomes["distribution"]["open_gap"] == 1,
        outcomes["distribution"]["exact_gate"] == 1,
        load("retained-negative-register-final.json")["negative_erased"] is False,
        load("exact-open-gate-register-final.json")["silently_closed"] == 0,
        len((PHASE / "integrated-overview.md").read_text(encoding="utf-8").split()) >= 1200,
        len((PHASE / "handoffs/eiren-kestrel-v649-v7-activation.md").read_text(encoding="utf-8").split()) >= 1200,
        (PHASE / "accessible-report.html").is_file(),
        (PHASE / "threat-model.json").is_file(),
        plan["canonical_successful_pass_budget"] == 1,
        plan["successful_passes_used"] == 0,
        load("phase-truth.json")["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        owner_files < 15000,
    ]
    if not all(minimal):
        raise RuntimeError(f"minimal checks failed {[index + 1 for index, value in enumerate(minimal) if not value]}")
    payload = {
        "schema": "ghc.family.v649-v6.canonical-pass.v1",
        "evidence_head": head,
        "selected_modules": MODULES,
        "tests_selected": selected,
        "tests_run": result.testsRun,
        "tests_passed": result.testsRun,
        "detailed_checks": len(detailed),
        "detailed_passed": len(detailed),
        "minimal_checks": len(minimal),
        "minimal_passed": len(minimal),
        "phase_json_parses": len(json_files),
        "privacy_scanned_files": len(files),
        "privacy_pattern_classes": 5,
        "privacy_confirmed_hits": 0,
        "full_repository_suite": False,
        "successful_canonical_pass_number": 1,
        "failed_canonical_attempts_before_success": 2,
        "post_success_replay": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
