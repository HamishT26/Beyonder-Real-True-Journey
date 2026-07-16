#!/usr/bin/env python3
"""Apply retained post-evidence corrections to the v646-v2 lifecycle packet."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v646-v2"
EVIDENCE = "ad5ff9d4f135a0c61b73c597893dab81521ba5c4"
POST = [
    {
        "negative_id": "V6462-X2-N15",
        "surface": "first post-evidence broad scoped-test replay",
        "observed": "Sixty-five tests passed and two inherited v646-v1 precommit-validator tests failed because their original-phase commit cap does not apply after successor commits.",
        "credit": "none",
        "recovery": "Retain both failures and run an explicit successor selection that excludes only the two original-phase commit-cap assertions.",
        "method_id": "V6462-M22",
    },
    {
        "negative_id": "V6462-X2-N16",
        "surface": "canonical evidence scoped-test binding",
        "observed": "The first lifecycle builder rebound a precommit candidate receipt to the evidence head without an exact-head test invocation.",
        "credit": "none",
        "recovery": "Withdraw exact-evidence credit, label the receipt as precommit candidate evidence, and require the explicit successor selection at the exact final head.",
        "method_id": "V6462-M23",
    },
    {
        "negative_id": "V6462-X2-N17",
        "surface": "first explicit successor scoped-test runner",
        "observed": "Direct script execution discovered six loader failures because the repository root was absent from the import search path.",
        "credit": "none",
        "recovery": "Add the resolved repository root to the import path before loading the unchanged six-module selection.",
        "method_id": "V6462-M24",
    },
    {
        "negative_id": "V6462-X2-N18",
        "surface": "ten-second staged-state status probe",
        "observed": "The read-only status probe exceeded its ten-second command window before producing evidence.",
        "credit": "none",
        "recovery": "Retain the timeout, separate the status surfaces, disable login-shell startup, and use the measured sixty-second bounded window.",
        "method_id": "V6462-M25",
    },
    {
        "negative_id": "V6462-X2-N19",
        "surface": "ten-second process and staged-review metadata probe",
        "observed": "The second read-only probe also exceeded its ten-second command window before producing evidence.",
        "credit": "none",
        "recovery": "Retain the repeated timeout and rerun the decomposed metadata probe with login-shell startup disabled and a sixty-second bound.",
        "method_id": "V6462-M25",
    },
    {
        "negative_id": "V6462-X2-N20",
        "surface": "Windows ripgrep file-glob diagnostic",
        "observed": "A wildcard embedded in a Windows path was passed to ripgrep as a literal invalid path and the diagnostic exited without completing its intended search.",
        "credit": "none",
        "recovery": "Search the containing directory with an explicit ripgrep glob filter or enumerate explicit file paths before searching.",
        "method_id": "V6462-M26",
    },
    {
        "negative_id": "V6462-X2-N21",
        "surface": "PowerShell filesystem-provider bracket filter",
        "observed": "A bracket expression in Get-ChildItem -Filter returned no matches because the provider did not apply the assumed character-class semantics.",
        "credit": "none",
        "recovery": "Use an explicit broad filename prefix and then filter returned names, or enumerate the exact expected files.",
        "method_id": "V6462-M26",
    },
    {
        "negative_id": "V6462-X2-N22",
        "surface": "installed GHC Family Index runner lookup",
        "observed": "The first direct invocation assumed a nonexistent ghc_family_index.py filename and exited before producing an index.",
        "credit": "none",
        "recovery": "Resolve the installed skill package files first and invoke its actual build_ghc_family_index.py entrypoint.",
        "method_id": "V6462-M27",
    },
    {
        "negative_id": "V6462-X2-N23",
        "surface": "PowerShell staged-summary wrapper",
        "observed": "A native diff-check command was embedded with a statement separator inside a hashtable value expression, producing a parser error before any Git command ran.",
        "credit": "none",
        "recovery": "Run the native diff check first, store its exit code in a scalar, and construct the summary object afterward.",
        "method_id": "V6462-M28",
    },
]


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("lifecycle correction must run before the final commit")
    scoped = load("validation/final-precommit-successor-scoped-tests.json")
    if not scoped.get("valid") or scoped.get("passed") != 65 or scoped.get("excluded_count") != 2:
        raise SystemExit("explicit successor selection is not a passing 65-test receipt")

    x2 = load("validation/x2-operational-negatives.json")
    present = {row["negative_id"] for row in x2["rows"]}
    x2["rows"].extend(row for row in POST if row["negative_id"] not in present)
    x2["count"] = len(x2["rows"])
    write("validation/x2-operational-negatives.json", x2)

    negatives = load("retained-negative-register.json")
    present = {row["negative_id"] for row in negatives["x2_operational_rows"]}
    negatives["x2_operational_rows"].extend(row for row in POST if row["negative_id"] not in present)
    negatives["x2_operational"] = len(negatives["x2_operational_rows"])
    negatives["effective_total"] = negatives["inherited_effective"] + negatives["x1_operational"] + negatives["preregistered_synthetic_executed_and_rejected"] + negatives["x2_operational"]
    write("retained-negative-register.json", negatives)
    write(
        "validation/post-evidence-operational-negatives.json",
        {
            "schema": "ghc.family.v646-v2.post-evidence-operational-negatives.v1",
            "evidence_commit": EVIDENCE,
            "count": len(POST),
            "rows": POST,
            "all_received_zero_initial_credit": True,
            "effective_total_after_correction": negatives["effective_total"],
            "boundary": "Post-evidence failures are retained additively in the lifecycle commit and do not rewrite the immutable evidence commit.",
        },
    )

    method = load("method-flow/method-flow-summary.json")
    correction = load("validation/scoped-test-binding-correction.json")
    corrected_scoped = {
        "schema": "ghc.family.v646-v2.canonical-evidence-scoped-tests.correction.v2",
        "evidence_commit": EVIDENCE,
        "binding_status": "withdrawn_no_exact_head_invocation",
        "original_candidate_receipt": "validation/scoped-test-receipt.json",
        "original_candidate_passed": 67,
        "explicit_successor_precommit_receipt": "validation/final-precommit-successor-scoped-tests.json",
        "explicit_successor_precommit_passed": scoped["passed"],
        "excluded_phase_local_tests": scoped["excluded_phase_local_tests"],
        "exact_final_successor_selection_required": 65,
        "full_repository_suite_run": False,
        "valid_as_exact_evidence_receipt": False,
        "retained_negative_id": correction["retained_negative_id"],
        "boundary": correction["boundary"],
    }
    write("validation/canonical-evidence-scoped-tests.json", corrected_scoped)

    truth = load("phase-truth.json")
    truth["effective_retained_negatives"] = negatives["effective_total"]
    truth["method_flow"] = method["counts"]
    truth["canonical_scoped_tests"] = {
        "candidate_precommit_passed": 67,
        "exact_evidence_credit": "withdrawn",
        "explicit_successor_precommit_passed": 65,
        "exact_final_required": 65,
        "full_repository_suite_run": False,
    }
    truth["same_owner_repeatability"] = "pending exactly one named-lane exact-final replay"
    write("phase-truth.json", truth)

    checklist = load("complete-incomplete-checklist.json")
    checklist["completed"] = [row for row in checklist["completed"] if "scoped repository selection passed 67" not in row]
    for item in (
        "broad post-evidence selection retained at 65 passes and 2 phase-local failures",
        "explicit successor precommit selection passed 65 of 65",
        "precommit scoped receipt exact-evidence binding withdrawn",
    ):
        if item not in checklist["completed"]:
            checklist["completed"].append(item)
    checklist["pending"] = [
        "combined closeout and seal commit",
        "exact-final canonical validation including 65-test successor selection",
        "exactly one local-only named-lane replay",
        "single Sable Rook baton",
    ]
    write("complete-incomplete-checklist.json", checklist)

    closeout = load("closeout-receipt.json")
    closeout["effective_retained_negatives"] = negatives["effective_total"]
    closeout["post_evidence_operational_negatives"] = len(POST)
    closeout["scoped_tests"] = truth["canonical_scoped_tests"]
    closeout["method_flow"] = method["counts"]
    write("closeout-receipt.json", closeout)

    seal = load("seal-receipt.json")
    seal["candidate_checks_passed"] = [row for row in seal["candidate_checks_passed"] if "test" not in row.casefold()]
    seal["candidate_checks_passed"].insert(0, "65-test explicit successor precommit selection; exact-final replay still required")
    seal["exact_final_successor_scoped_tests_required"] = 65
    seal["post_evidence_operational_negatives"] = len(POST)
    write("seal-receipt.json", seal)

    final = load("final-validation-record.json")
    final["canonical_evidence_scoped_tests"] = "precommit_candidate_only_exact_head_credit_withdrawn"
    final["explicit_successor_precommit_tests"] = {"passed": 65, "excluded_phase_local": 2}
    final["exact_final_successor_scoped_tests_required"] = 65
    final["post_evidence_operational_negatives"] = len(POST)
    write("final-validation-record.json", final)

    wellbeing_path = PHASE / "wellbeing-check.md"
    lines = wellbeing_path.read_text(encoding="utf-8").splitlines()
    lines = [line for line in lines if not line.startswith("- The immutable evidence head passed 67 scoped tests")]
    lines = [
        "- 38 operational failures are retained across x1 and x2 at closeout; each failed witness received zero initial credit and every recovery stayed bounded."
        if "operational failures are retained across x1 and x2" in line
        else line
        for line in lines
    ]
    lines = [
        "- Method Flow closes with 28 methods, 38 retained failed witnesses, and 28 passing witnesses."
        if line.startswith("- Method Flow closes")
        else line
        for line in lines
    ]
    additions = [
        "- The earlier 67-test precommit candidate remains retained but has no exact-evidence binding; a post-evidence broad replay passed 65 and failed two inherited original-phase commit-cap assertions.",
        "- The explicit successor precommit selection passed 65 of 65 while listing both phase-local exclusions; exact-final canonical and named-lane invocations remain required.",
    ]
    for line in additions:
        if line not in lines:
            lines.append(line)
    wellbeing_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(json.dumps({"x2_operational": x2["count"], "effective_negatives": negatives["effective_total"], "successor_tests": scoped["passed"], "method_count": method["counts"]["methods"], "valid": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
