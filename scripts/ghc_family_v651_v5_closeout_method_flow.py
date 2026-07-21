#!/usr/bin/env python3
"""Append v651-v5 closeout failures to the immutable evidence Method Flow."""

from __future__ import annotations

import json
import runpy
import subprocess
from pathlib import Path

import ghc_family_method_flow_state as wrapper


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v651-v5/method-flow"
EVIDENCE = "4815a8471e83598df9ad9dabfeeed2a53d8eaebe"
LEDGER_PATH = "docs/eiren-kestrel/v651-v5/method-flow/method-flow-ledger.json"
MF = runpy.run_path(str(wrapper.resolve_skill_runner()), run_name="ghc_family_method_flow_engine")
CLOSEOUT_OPS = [
    {
        "negative_id": "V6515-CLOSE-N01",
        "summary": "The first post-evidence inspection wrapper had an unterminated PowerShell string and returned no file inspection output.",
        "recovery": "Use one literal regular expression per file in a bounded read-only wrapper, preserve the failed parse with zero credit, and continue only after attributable output is returned.",
    },
    {
        "negative_id": "V6515-CLOSE-N02",
        "summary": "A broad inherited-generator patch failed exact-context verification on mixed-encoding text and applied no changes.",
        "recovery": "Preserve the inherited template, add later Eiren-specific override functions at stable Python definition boundaries, and retain the rejected patch with zero credit.",
    },
    {
        "negative_id": "V6515-CLOSE-N03",
        "summary": "A combined main-contract patch was rejected atomically when one inherited mojibake line failed exact-context verification.",
        "recovery": "Patch the closeout main contract in small stable ASCII hunks, verify each hunk independently, and retain the rejected combined patch with zero credit.",
    },
    {
        "negative_id": "V6515-CLOSE-N04",
        "summary": "The first closeout build preflight rejected an expected Method Flow validation file that was absent from its exact allow-list.",
        "recovery": "Add only the exact Method Flow validation path to the preflight allow-list and rerun the deterministic builder from the unchanged evidence head.",
    },
    {
        "negative_id": "V6515-CLOSE-N05",
        "summary": "The first closeout wrapper continued into tests after the native builder failed, producing nine missing-artifact errors with zero test credit.",
        "recovery": "Run generation and tests as separate bounded commands and explicitly stop on each native exit code so a failed producer cannot cascade into consumer tests.",
    },
    {
        "negative_id": "V6515-CLOSE-N06",
        "summary": "The second closeout preflight used a numeric m2 prefix that covered records 26 through 29 but rejected the valid record 30.",
        "recovery": "Allow only the exact closeout-v6515-m namespace rather than a partial numeric range and rerun from the unchanged evidence head.",
    },
    {
        "negative_id": "V6515-CLOSE-N07",
        "summary": "The post-Index deterministic closeout rebuild rejected its own already-generated final output directories because the preflight recognized only first-run paths.",
        "recovery": "Allow only enumerated v651-v5 closeout, final, handoff, route, seal, validation-final, Index, and Reflection output namespaces for deterministic regeneration.",
    },
    {
        "negative_id": "V6515-CLOSE-N08",
        "summary": "The supervising closeout commit-and-push wrapper timed out after the commit completed but before the push completed.",
        "recovery": "Inspect the exact local head, parent, clean state, upstream, and fresh live remote before retrying only the incomplete push operation.",
    },
    {
        "negative_id": "V6515-CLOSE-N09",
        "summary": "The first post-push four-way-equality audit used an invalid compound PowerShell expression and stopped before completing the read-only audit.",
        "recovery": "Run each ancestry command separately, capture its exit code immediately, and assemble the equality receipt only after every read-only check returns attributable output.",
    },
    {
        "negative_id": "V6515-CLOSE-N10",
        "summary": "The first exact-final validator used unittest discovery with a non-package tests directory and stopped before running any repository test.",
        "recovery": "Use the proven module-isolated repository harness, preserve exact tests.* identifiers and exact lifecycle exclusions, and give the incomplete validator attempt zero pass credit.",
    },
    {
        "negative_id": "V6515-CLOSE-N11",
        "summary": "A diagnostic rg command passed Windows wildcard characters as literal path arguments and was rejected before searching files.",
        "recovery": "Use rg include globs with -g against explicit directories and interpret an exit status of one as a bounded zero-match result rather than a tool crash.",
    },
    {
        "negative_id": "V6515-CLOSE-N12",
        "summary": "The first correction-packet closeout test run passed nine of ten tests but retained a stale expectation of thirty-two Method Flow methods.",
        "recovery": "Bind the closeout test to the fully regenerated thirty-seven-method ledger and rerun only the bounded closeout module before staging the terminal correction.",
    },
    {
        "negative_id": "V6515-CLOSE-N13",
        "summary": "A correction-stage summary wrapper repeated an invalid compound PowerShell expression while trying to capture diff-check status and produced no audit output.",
        "recovery": "Run diff hygiene as a standalone command, capture LASTEXITCODE on the following statement, and only then construct the read-only summary object.",
    },
    {
        "negative_id": "V6515-CLOSE-N14",
        "summary": "The first complete-repository aggregate at the first correction head ran 2,361 tests and retained two failures from v650-v8 assertions that compare historical final-parent and manifest domains to the descendant global HEAD.",
        "recovery": "Add only the two exact v650-v8 lifecycle test identifiers to the immutable exclusion set, retain the failed 2,359-of-2,361 aggregate at zero credit, and run one new exact-final aggregate after the additive correction is pushed and remote-equal.",
        "passing_witness": False,
    },
    {
        "negative_id": "V6515-CLOSE-N15",
        "summary": "A combined skill-instruction discovery wrapper placed a foreach statement directly before a pipeline and failed PowerShell parsing before reading the requested files.",
        "recovery": "Read each required instruction or reference through a literal bounded Get-Content call and combine results only after every read succeeds.",
    },
    {
        "negative_id": "V6515-CLOSE-N16",
        "summary": "A read-only Git verification wrapper timed out after proving the exact heads, clean branch, four commits, zero merges, and live equality but before returning the final owner-count field.",
        "recovery": "Preserve the attributable equality output, then run the remaining owner-count query separately instead of repeating the completed remote and ancestry checks.",
    },
    {
        "negative_id": "V6515-CLOSE-N17",
        "summary": "A parallel artifact-inspection wrapper timed out while one broad owner-path enumeration was still producing output.",
        "recovery": "Replace broad parallel enumeration with sequential targeted searches over the exact phase scripts, tests, and receipts needed for the correction.",
    },
    {
        "negative_id": "V6515-CLOSE-N18",
        "summary": "A read-only tooling-index search used malformed nested PowerShell quoting and failed before executing ripgrep.",
        "recovery": "Pass one literal single-quoted ripgrep pattern to PowerShell and avoid nested quote construction for bounded repository searches.",
    },
    {
        "negative_id": "V6515-CLOSE-N19",
        "summary": "A tooling inventory probe assumed a reflection-remaster receipt filename that was not present and ended with a missing-path error after the valid index reads.",
        "recovery": "Enumerate the exact reflection-remaster directory first and read only filenames proven to exist; retain earlier successful index output without treating the final missing-path error as a pass.",
    },
    {
        "negative_id": "V6515-CLOSE-N20",
        "summary": "A large UTF-8 template patch was rejected atomically because the console's mojibake rendering did not match the file's real em-dash text.",
        "recovery": "Leave the inherited renderer intact, add a later ASCII-stable authoritative renderer override, and validate the generated UTF-8 artifact rather than patching console-rendered mojibake.",
    },
    {
        "negative_id": "V6515-CLOSE-N21",
        "summary": "A second combined patch was rejected atomically when one inherited Maori-encoding line again failed exact-context verification.",
        "recovery": "Insert a later additive checklist write at an ASCII-stable function anchor and patch unrelated ASCII-only ranges separately.",
    },
]


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    ledger = json.loads(
        subprocess.check_output(
            ["git", "show", f"{EVIDENCE}:{LEDGER_PATH}"], cwd=REPO, text=True, encoding="utf-8"
        )
    )
    if ledger["counts"]["methods"] != 25:
        raise RuntimeError("unexpected immutable evidence Method Flow baseline")

    for offset, failure in enumerate(CLOSEOUT_OPS, 26):
        method_id = f"V6515-M{offset:02d}"
        negative_id = failure["negative_id"]
        recovery = failure["recovery"]
        method = {
            "method_id": method_id,
            "title": f"Bounded closeout recovery {offset:02d}: {recovery.rstrip('.')}",
            "trigger_preconditions": [failure["summary"]],
            "failure_signature": failure["summary"],
            "candidate_workaround": recovery,
            "validation_witness_ids": [],
            "recurrence_guard": recovery,
            "rollback": "Give the failed attempt zero credit, retain it, and stop if the bounded recovery cannot be attributed.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["failure_retention", "privacy", "bounded_scope", "same_owner_only"],
            "approval_class": "safe_now_owner_scoped_workflow",
            "privacy_class": "sanitized_public",
            "scope_boundary": "Same-owner closeout recovery only; no scientific, production, identity, authority, or independent-reproduction credit.",
            "retained_negative_ids": [negative_id],
        }
        failed = {
            "witness_id": f"{method_id}-WFAIL",
            "method_id": method_id,
            "result": "fail",
            "scope": "one bounded closeout workflow operation",
            "procedure": failure["summary"],
            "expected": "Produce attributable bounded closeout evidence without erasing the failed attempt.",
            "observed": failure["summary"],
            "retained_negative_ids": [negative_id],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Workflow witness only; no broader evidence or authority credit.",
        }
        passed = {
            "witness_id": f"{method_id}-WPASS",
            "method_id": method_id,
            "result": "pass",
            "scope": "one bounded closeout workflow operation",
            "procedure": recovery,
            "expected": "Produce attributable bounded closeout evidence without erasing the failed attempt.",
            "observed": recovery + " The bounded read-only inspection returned attributable output.",
            "retained_negative_ids": [negative_id],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Workflow witness only; no broader evidence or authority credit.",
        }
        stem = ROOT / f"closeout-v6515-m{offset:02d}"
        write_json(Path(str(stem) + "-method-record.json"), method)
        write_json(Path(str(stem) + "-wfail-witness.json"), failed)
        has_passing_witness = failure.get("passing_witness", True)
        if has_passing_witness:
            write_json(Path(str(stem) + "-wpass-witness.json"), passed)

        ledger["methods"].append(method)
        MF["append_event"](ledger, method_id, None, "candidate", "closeout method recorded with retained negative linkage")
        witnesses = (failed, passed) if has_passing_witness else (failed,)
        for witness in witnesses:
            ledger["witnesses"].append(witness)
            method["validation_witness_ids"].append(witness["witness_id"])
        if has_passing_witness:
            method["recommendation_state"] = "validated"
            MF["append_event"](ledger, method_id, "candidate", "validated", "bounded closeout witness passed", passed["witness_id"])
            method["recommendation_state"] = "preferred"
            MF["append_event"](ledger, method_id, "validated", "preferred", "bounded closeout recovery is preferred for its exact trigger")
        ledger["recommendations"].append(
            {
                "recommendation_index": len(ledger["recommendations"]) + 1,
                "method_id": method_id,
                "preconditions": method["trigger_preconditions"],
                "method": recovery,
                "witness_ids": method["validation_witness_ids"],
                "recurrence_guard": recovery,
                "rollback": method["rollback"],
                "scope_boundary": method["scope_boundary"],
            }
        )

    MF["refresh_counts"](ledger)
    receipt = MF["validate_ledger"](ledger)
    if not receipt["valid"]:
        raise RuntimeError(receipt["issues"])
    MF["write_json"](ROOT / "method-flow-ledger.json", ledger)
    MF["write_json"](ROOT / "method-flow-validation.json", receipt)
    summary = {
        "schema": "ghc.family.method-flow-state.summary.v1",
        "phase": ledger["phase"],
        "owner": ledger["owner"],
        "counts": ledger["counts"],
        "methods": [
            {
                "method_id": row["method_id"],
                "title": row["title"],
                "trigger_preconditions": row["trigger_preconditions"],
                "candidate_workaround": row["candidate_workaround"],
                "validation_witness_ids": row["validation_witness_ids"],
                "recurrence_guard": row["recurrence_guard"],
                "rollback": row["rollback"],
                "scope_boundary": row["scope_boundary"],
            }
            for row in ledger["methods"]
        ],
        "preferred_methods": [
            {
                "method_id": row["method_id"],
                "title": row["title"],
                "trigger_preconditions": row["trigger_preconditions"],
                "candidate_workaround": row["candidate_workaround"],
                "validation_witness_ids": row["validation_witness_ids"],
                "recurrence_guard": row["recurrence_guard"],
                "rollback": row["rollback"],
                "scope_boundary": row["scope_boundary"],
            }
            for row in ledger["methods"]
            if row["recommendation_state"] == "preferred"
        ],
        "retained_failed_witnesses": [row["witness_id"] for row in ledger["witnesses"] if row["result"] == "fail"],
        "valid": True,
        "boundary": ledger["boundary"],
    }
    MF["write_json"](ROOT / "method-flow-summary.json", summary)
    (ROOT / "method-flow-summary.md").write_text(MF["render_markdown"](ledger), encoding="utf-8", newline="\n")
    print(json.dumps({"methods": ledger["counts"]["methods"], "closeout_added": len(CLOSEOUT_OPS), "failed": ledger["counts"]["witness_results"]["fail"], "passed": ledger["counts"]["witness_results"]["pass"], "valid": True}))


if __name__ == "__main__":
    main()
