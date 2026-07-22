#!/usr/bin/env python3
"""Bootstrap Sable Rook's append-only v652-v1 Method Flow ledger."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import ghc_family_v652_v1_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
LEDGER = ROOT / "method-flow/method-flow-ledger.json"
RECORDS = ROOT / "method-flow/records"
RUNNER = Path.home() / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"


METHODS = [
    {
        "method_id": "V6521-M01",
        "title": "Discover sealed lifecycle paths before reading them",
        "failure_signature": "A read-only startup probe guesses a lifecycle path that does not exist.",
        "trigger_preconditions": ["A sealed predecessor packet uses phase-specific lifecycle directory names."],
        "candidate_workaround": "List the exact sealed phase root, then bind reads to discovered paths.",
        "recurrence_guard": "Never infer lifecycle filenames when an exact phase-root listing is cheap.",
        "rollback": "Retain the failed read-only probe and make no repository mutation.",
        "negative": "V6521-X1-N01",
        "fail_observed": "The guessed ordinary phase-truth path was absent.",
        "pass_observed": "The exact final phase-truth path was discovered and read without mutation.",
    },
    {
        "method_id": "V6521-M02",
        "title": "Separate workflow schema tokens from stronger live constraints",
        "failure_signature": "A sanitized workflow request overloads an enumerated policy field with a stronger phase-local token.",
        "trigger_preconditions": ["A live prohibition is stricter than the workflow runner's standard boundary vocabulary."],
        "candidate_workaround": "Use the required schema token and preserve the stronger live constraint in an additive explicit field.",
        "recurrence_guard": "Do not overload enumerated schema fields; express stricter live controls additively.",
        "rollback": "Retain the failed audit artifacts and perform no route or repository mutation.",
        "negative": "V6521-X1-N02",
        "fail_observed": "The first audit failed one messaging-boundary policy check and wrote only local planning evidence.",
        "pass_observed": "The corrected audit passed all twenty policy checks while preserving the no-action rule.",
    },
    {
        "method_id": "V6521-M03",
        "title": "Materialize foreach output before piping in Windows PowerShell 5.1",
        "failure_signature": "A statement-level foreach block is piped directly and fails at parse time.",
        "trigger_preconditions": ["A Windows PowerShell 5.1 wrapper serializes rows from a statement-level foreach loop."],
        "candidate_workaround": "Assign foreach results to an array and pipe only that array.",
        "recurrence_guard": "Never append a pipeline directly to statement-level foreach in Windows PowerShell 5.1.",
        "rollback": "Retain the parser failure; it changed no files, branches, or external state.",
        "negative": "V6521-X1-N03",
        "fail_observed": "The parser rejected an empty pipe element before novelty evidence was produced.",
        "pass_observed": "The array-materialized inventory returned exact novelty-search rows.",
    },
    {
        "method_id": "V6521-M04",
        "title": "Rewrite semantic collisions before x1 freezing",
        "failure_signature": "The exact frozen-chain novelty gate rejects one or more candidate mechanisms at its preregistered threshold.",
        "trigger_preconditions": ["A new proposal portfolio has exact predecessor titles and manual mechanism review available."],
        "candidate_workaround": "Replace collided mechanisms with genuinely different obligation surfaces and rerun the exact neighbour gate.",
        "recurrence_guard": "Never treat lexical renaming as semantic novelty; inspect the nearest mechanism and rewrite the proposal surface.",
        "rollback": "Retain the rejected candidate titles and freeze no proposal until the corrected portfolio passes.",
        "negative": "V6521-X1-N04",
        "fail_observed": "The first thirty-title gate rejected seven duplicated or overbroad mechanisms.",
        "pass_observed": "The corrected portfolio passed the exact lexical threshold with manual mechanism distinctions retained.",
    },
    {
        "method_id": "V6521-M05",
        "title": "Audit copied builders before first materialization",
        "failure_signature": "A mechanically adapted builder retains predecessor counts or semantic labels.",
        "trigger_preconditions": ["A successor builder was derived from a compatible predecessor implementation."],
        "candidate_workaround": "Compare every copied constant and domain noun against the current phase data before running the writer.",
        "recurrence_guard": "Run bounded count, source, and stale-label probes before the first artifact-writing invocation.",
        "rollback": "Retain the drift finding and generate no packet until the copied fields are corrected.",
        "negative": "V6521-X1-N05",
        "fail_observed": "Review found predecessor portfolio minima, source-manifest cardinalities, and stale domain nouns before generation.",
        "pass_observed": "The corrected import and stale-label probes returned current counts and Sable-owned surfaces only.",
    },
    {
        "method_id": "V6521-M06",
        "title": "Avoid PowerShell 7-only encoding tokens on Windows PowerShell 5.1",
        "failure_signature": "Set-Content rejects utf8NoBOM because the active shell exposes only its Windows PowerShell 5.1 encoding enumeration.",
        "trigger_preconditions": ["A mechanical source-copy operation runs under Windows PowerShell 5.1."],
        "candidate_workaround": "Preserve the harmless copied source and use apply_patch for the substantive UTF-8 rewrite.",
        "recurrence_guard": "Check the active PowerShell generation before selecting an encoding token; prefer apply_patch for source edits.",
        "rollback": "Retain the failed command output; no rewritten source, Git state, or external state was produced.",
        "negative": "V6521-X1-N06",
        "fail_observed": "Windows PowerShell rejected utf8NoBOM before the replacement pipeline wrote the destination.",
        "pass_observed": "Apply_patch rewrote the copied validator to current phase paths and count contracts.",
    },
]


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def run(*args: str) -> None:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    subprocess.run([sys.executable, str(RUNNER), *args], cwd=REPO, env=env, check=True)


def main() -> None:
    if not LEDGER.exists():
        run("init", "--ledger", str(LEDGER), "--phase", d.PHASE, "--owner", d.OWNER)
    for item in METHODS:
        method_id = item["method_id"]
        stem = method_id.lower()
        method_path = RECORDS / f"{stem}-method.json"
        fail_path = RECORDS / f"{stem}-fail.json"
        pass_path = RECORDS / f"{stem}-pass.json"
        method = {
            "method_id": method_id,
            "title": item["title"],
            "failure_signature": item["failure_signature"],
            "trigger_preconditions": item["trigger_preconditions"],
            "privacy_class": "sanitized_owner_local_workflow",
            "approval_class": "safe_now_read_only_or_owned_additive_recovery",
            "candidate_workaround": item["candidate_workaround"],
            "validation_witness_ids": [],
            "recurrence_guard": item["recurrence_guard"],
            "rollback": item["rollback"],
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["failure_retention", "sibling_lane_isolation", "privacy", "same_owner_only", "no_stage20_promotion"],
            "retained_negative_ids": [item["negative"]],
            "scope_boundary": "Bounded Sable-owned workflow recovery only; no external or independent-reproduction claim.",
        }
        failed = {
            "witness_id": f"{method_id}-WFAIL",
            "method_id": method_id,
            "procedure": "Retain the first exact failed startup invocation.",
            "scope": "Sable v652-v1 startup workflow",
            "expected": "The unsafe or incompatible method fails without external mutation.",
            "observed": item["fail_observed"],
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [item["negative"]],
            "boundary": "A failed startup witness has zero completion or validation credit.",
        }
        passed = {
            "witness_id": f"{method_id}-WPASS",
            "method_id": method_id,
            "procedure": "Apply only the bounded recovery after the failure is retained.",
            "scope": "Sable v652-v1 startup workflow",
            "expected": "The corrected bounded operation passes without crossing a protected gate.",
            "observed": item["pass_observed"],
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [item["negative"]],
            "boundary": "The passing recovery validates only the declared trigger and does not erase the failed witness.",
        }
        write_json(method_path, method)
        write_json(fail_path, failed)
        write_json(pass_path, passed)
        ledger = json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {"methods": []}
        if not any(row["method_id"] == method_id for row in ledger["methods"]):
            run("record", "--ledger", str(LEDGER), "--record-file", str(method_path))
            run("witness", "--ledger", str(LEDGER), "--witness-file", str(fail_path))
            run("witness", "--ledger", str(LEDGER), "--witness-file", str(pass_path))
            run("set-state", "--ledger", str(LEDGER), "--method-id", method_id, "--state", "preferred", "--note", "bounded recovery passed after retained failure")
    run("validate", "--ledger", str(LEDGER), "--receipt", str(ROOT / "method-flow/method-flow-validation.json"))
    run("summarize", "--ledger", str(LEDGER), "--json-output", str(ROOT / "method-flow/method-flow-summary.json"), "--markdown-output", str(ROOT / "method-flow/method-flow-summary.md"))


if __name__ == "__main__":
    main()
