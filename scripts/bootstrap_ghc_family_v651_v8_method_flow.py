#!/usr/bin/env python3
"""Bootstrap Ilyra Fen's append-only v651-v8 Method Flow ledger."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/ilyra-fen/v651-v8"
LEDGER = ROOT / "method-flow/method-flow-ledger.json"
RECORDS = ROOT / "method-flow/records"
RUNNER = Path.home() / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"


METHODS = [
    {
        "method_id": "V6518-M01",
        "title": "Bind memory searches to the declared memory registry",
        "failure_signature": "A memory search starts from task metadata and cannot find the registry.",
        "trigger_preconditions": ["A phase needs prior GHC continuity and the memory root is declared separately from task metadata."],
        "candidate_workaround": "Search the exact declared memory registry path before opening any referenced rollout record.",
        "recurrence_guard": "Never infer the memory registry from the current task directory.",
        "rollback": "Retain the failed read-only search and make no repository or memory mutation.",
        "negative": "V6518-X1-N01",
        "fail_observed": "The inferred task-directory registry path was absent.",
        "pass_observed": "The declared memory-root registry was read and the relevant rollout pointer was resolved.",
    },
    {
        "method_id": "V6518-M02",
        "title": "Use ordinary non-force push after a verified fast-forward",
        "failure_signature": "A push wrapper requests an unsupported ff-only option after the local fast-forward already succeeded.",
        "trigger_preconditions": ["The owned branch is clean, its old head is ancestral to the verified source, and an explicit refspec is available."],
        "candidate_workaround": "Verify the intended head and divergence, then use an ordinary explicit-refspec push without force.",
        "recurrence_guard": "Apply ff-only to merge or pull, not push; ordinary push already rejects non-fast-forward updates by default.",
        "rollback": "If the explicit push fails, retain local history and stop without force or reset.",
        "negative": "V6518-X1-N02",
        "fail_observed": "The unsupported option stopped before any remote update.",
        "pass_observed": "The ordinary explicit-refspec push advanced only the Ilyra branch and four-way equality was restored.",
    },
    {
        "method_id": "V6518-M03",
        "title": "Pin UTF-8 before emitting inherited Unicode proposal titles",
        "failure_signature": "A bounded Python report reaches culturally correct Unicode text and the default Windows console encoding rejects it.",
        "trigger_preconditions": ["A Windows Python process may emit Māori or other non-ASCII repository text."],
        "candidate_workaround": "Set PYTHONUTF8 and PYTHONIOENCODING before process start and preserve source text unchanged.",
        "recurrence_guard": "Pin UTF-8 for every Unicode-emitting diagnostic; never transliterate source text to satisfy a console.",
        "rollback": "Retain the failed read-only probe and change no culturally authoritative wording.",
        "negative": "V6518-X1-N03",
        "fail_observed": "The default console codec stopped while printing an inherited Māori title.",
        "pass_observed": "The same bounded novelty read completed under explicit UTF-8 with the source text unchanged.",
    },
    {
        "method_id": "V6518-M04",
        "title": "Materialize foreach output before piping in Windows PowerShell 5.1",
        "failure_signature": "A statement-level foreach block is piped directly and fails at parse time.",
        "trigger_preconditions": ["A Windows PowerShell 5.1 wrapper needs to serialize rows produced by a statement-level foreach loop."],
        "candidate_workaround": "Assign the foreach results to an array and pipe only that array.",
        "recurrence_guard": "Never append a pipeline directly to statement-level foreach in Windows PowerShell 5.1.",
        "rollback": "Retain the parser failure; it changed no files, branches, or external state.",
        "negative": "V6518-X1-N04",
        "fail_observed": "The parser rejected an empty pipe element before inventory evidence was produced.",
        "pass_observed": "The array-materialized inventory returned exact line and byte counts for both selected skills.",
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
        run("init", "--ledger", str(LEDGER), "--phase", "v651-v8", "--owner", "Ilyra Fen")
    for item in METHODS:
        method_id = item["method_id"]
        method_path = RECORDS / f"{method_id.lower()}-method.json"
        fail_path = RECORDS / f"{method_id.lower()}-fail.json"
        pass_path = RECORDS / f"{method_id.lower()}-pass.json"
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
            "scope_boundary": "Bounded Ilyra-owned workflow recovery only; no external or independent-reproduction claim.",
        }
        fail = {
            "witness_id": f"{method_id}-WFAIL",
            "method_id": method_id,
            "procedure": "Retain the first exact failed startup invocation.",
            "scope": "Ilyra v651-v8 startup workflow",
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
            "scope": "Ilyra v651-v8 startup workflow",
            "expected": "The corrected bounded operation passes without crossing a protected gate.",
            "observed": item["pass_observed"],
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [item["negative"]],
            "boundary": "The passing recovery validates only the declared trigger and does not erase the failed witness.",
        }
        write_json(method_path, method)
        write_json(fail_path, fail)
        write_json(pass_path, passed)
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        if not any(row["method_id"] == method_id for row in ledger["methods"]):
            run("record", "--ledger", str(LEDGER), "--record-file", str(method_path))
            run("witness", "--ledger", str(LEDGER), "--witness-file", str(fail_path))
            run("witness", "--ledger", str(LEDGER), "--witness-file", str(pass_path))
            run("set-state", "--ledger", str(LEDGER), "--method-id", method_id, "--state", "preferred", "--note", "bounded recovery passed after retained failure")
    run("validate", "--ledger", str(LEDGER), "--receipt", str(ROOT / "method-flow/method-flow-validation.json"))
    run("summarize", "--ledger", str(LEDGER), "--json-output", str(ROOT / "method-flow/method-flow-summary.json"), "--markdown-output", str(ROOT / "method-flow/method-flow-summary.md"))


if __name__ == "__main__":
    main()
