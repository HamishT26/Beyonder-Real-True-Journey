#!/usr/bin/env python3
"""Validate the append-only Sylven v645-v8 Method Flow state."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys

from ghc_family_v645_v8_runtime import PHASE, ROOT, TRUTH_BOUNDARY, read_json, write_json


FAMILY_RUNNER = ROOT / "scripts/ghc_family_method_flow_state.py"
LEDGER = PHASE / "method-flow/method-flow-state.json"
X2_LEDGER = PHASE / "method-flow/method-flow-state-x2.json"

INCIDENTS = [
    {
        "number": 5,
        "negative_id": "V6458-X2-N01",
        "title": "Split an overbroad substantive patch after context verification failure",
        "failure": "The first substantive x2 patch included an unrelated runtime context that did not exist, so apply_patch rejected the entire edit and changed no file.",
        "failed": "Replace the core runner and alter an assumed runtime line in one context-sensitive patch.",
        "recovery": "Retain the rejected patch, verify that no file changed, and apply the core-runner replacement alone before reviewing runtime separately.",
        "observed": "The bounded core-runner replacement then applied without touching the unrelated runtime file.",
        "guard": "Do not combine independent context-sensitive edits unless every expected hunk was re-read from the current file.",
        "rollback": "Give the rejected patch zero implementation credit and preserve the source tree until the bounded replacement succeeds.",
    },
    {
        "number": 6,
        "negative_id": "V6458-X2-N02",
        "title": "Pass multi-alternative stale-term search patterns as quoted data",
        "failure": "A read-only multi-file stale-term scan embedded an apostrophe inside a single-quoted PowerShell pattern, so the shell parsed later alternatives as pipeline expressions and returned no review evidence.",
        "failed": "Interpolate a long alternation pattern containing an apostrophe into a single-quoted PowerShell argument.",
        "recovery": "Retain the parser failure, pass the unchanged alternation as a double-quoted data argument, and split the explicitly named files into bounded groups.",
        "observed": "The grouped searches then returned exact match or zero-match evidence without editing any file.",
        "guard": "Keep shell metacharacters and apostrophes inside a verified quoted data argument; a parser error receives zero scan credit.",
        "rollback": "Treat the failed scan as no evidence and make no stale-label claim until the quoted grouped searches finish.",
    },
    {
        "number": 7,
        "negative_id": "V6458-X2-N03",
        "title": "Separate verification commands after inline summary quoting failure",
        "failure": "A parallel verification wrapper embedded nested JSON-key quotes in an inline Python f-string, producing a syntax error and withholding the combined child result set.",
        "failed": "Run tests, validators, Git checks, and a nested-quoted inline JSON summary inside one parallel wrapper.",
        "recovery": "Retain the syntax error, give every unavailable child result zero credit, and rerun tests, validators, Git checks, and JSON or privacy summaries as separately bounded commands.",
        "observed": "Each separated verification command then returned its own result and exit status without nested shell or Python quote translation.",
        "guard": "Do not place nested quoted JSON indexing inside a shell-embedded f-string; result aggregation must not hide independently required evidence.",
        "rollback": "Discard the wrapper result set and do not advance the evidence commit until every separated command passes.",
    },
    {
        "number": 8,
        "negative_id": "V6458-X2-N04",
        "title": "Reject ancestry summaries built from a mistyped source revision",
        "failure": "A Git verification summary mistyped the source revision in its merge-count subcommand, emitted an ambiguous-revision fatal error, and then coerced missing output to zero.",
        "failed": "Aggregate several Git facts while manually repeating the source hash and allow a later JSON conversion to mask one failed child.",
        "recovery": "Retain the fatal error, withdraw the merge-count value, and rerun the merge count alone with the exact verified source revision and explicit exit-status check.",
        "observed": "The isolated command accepted the exact source revision and returned the evidenced zero-merge count.",
        "guard": "A summary is invalid if any child writes a Git fatal error; never coerce absent numeric output into evidence.",
        "rollback": "Give the failed summary no merge-count credit and do not commit evidence until the isolated ancestry command passes.",
    },
]


def call(*args: str) -> None:
    subprocess.run(
        [sys.executable, str(FAMILY_RUNNER), *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def main() -> int:
    shutil.copyfile(LEDGER, X2_LEDGER)
    for incident in INCIDENTS:
        number = incident["number"]
        method_id = f"V6458-M{number:02d}"
        fail_id = f"V6458-W{number:02d}-F"
        pass_id = f"V6458-W{number:02d}-P"
        record = {
            "method_id": method_id,
            "title": incident["title"],
            "failure_signature": incident["failure"],
            "trigger_preconditions": ["v645-v8 x2 evidence validation", "same-owner local tooling"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_local_tooling",
            "candidate_workaround": incident["recovery"],
            "validation_witness_ids": [fail_id, pass_id],
            "recurrence_guard": incident["guard"],
            "rollback": incident["rollback"],
            "rollback_witness_required": True,
            "side_effect_budget": ["owner_candidate_receipts_only", "no_ref_change", "no_remote_change"],
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["private_material", "destructive_action", "sibling_lane", "host_change"],
            "retained_negative_ids": [incident["negative_id"]],
            "scope_boundary": "Same-owner operational recovery only; no scientific, authority, production, accessibility-complete, security-complete, or independent-reproduction credit.",
        }
        failed = {"witness_id": fail_id, "method_id": method_id, "procedure": incident["failed"], "scope": "single owner-local evidence validation", "expected": "bounded validation completes without false credit", "observed": incident["failure"], "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [incident["negative_id"]], "boundary": TRUTH_BOUNDARY}
        passed = {"witness_id": pass_id, "method_id": method_id, "procedure": incident["recovery"], "scope": "single owner-local evidence validation", "expected": "bounded validation completes without false credit", "observed": incident["observed"], "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [incident["negative_id"]], "boundary": TRUTH_BOUNDARY}
        record_rel = f"method-flow/v6458-m{number:02d}-method-record.json"
        fail_rel = f"method-flow/v6458-w{number:02d}-f-witness.json"
        pass_rel = f"method-flow/v6458-w{number:02d}-p-witness.json"
        write_json(record_rel, record)
        write_json(fail_rel, failed)
        write_json(pass_rel, passed)
        call("record", "--ledger", str(X2_LEDGER), "--record-file", str(PHASE / record_rel))
        call("witness", "--ledger", str(X2_LEDGER), "--witness-file", str(PHASE / fail_rel))
        call("witness", "--ledger", str(X2_LEDGER), "--witness-file", str(PHASE / pass_rel))
        call("set-state", "--ledger", str(X2_LEDGER), "--method-id", method_id, "--state", "preferred", "--note", "Bounded passing witness recorded for the declared trigger only")
    call("validate", "--ledger", str(X2_LEDGER), "--receipt", str(PHASE / "method-flow/method-flow-x2-validation.json"))
    call(
        "summarize",
        "--ledger",
        str(X2_LEDGER),
        "--json-output",
        str(PHASE / "method-flow/method-flow-summary-x2.json"),
        "--markdown-output",
        str(PHASE / "method-flow/method-flow-summary-x2.md"),
    )
    ledger = read_json("method-flow/method-flow-state-x2.json")
    counts = ledger["counts"]
    payload = {
        "schema": "ghc.family.v645-v8.method-flow-runner.v1",
        "family_runner_used": True,
        "methods": counts["methods"],
        "failed_witnesses": counts["witness_results"]["fail"],
        "passing_witnesses": counts["witness_results"]["pass"],
        "preferred_methods": counts["states"]["preferred"],
        "operational_negatives_retained": counts["methods"],
        "failure_erasure_count": 0,
        "x2_operational_incidents_at_execution_build": len(INCIDENTS),
        "retained_negative_ids": [row["negative_id"] for row in INCIDENTS],
        "same_owner_only": True,
        "independent_reproduction": False,
        "result": "pass",
        "boundary": TRUTH_BOUNDARY,
    }
    write_json("prototypes/runner-witnesses/ghc_family_v645_v8_method_flow_runner.json", payload)
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
