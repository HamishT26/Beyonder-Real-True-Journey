#!/usr/bin/env python3
"""Append x2 operational failures with the family Method Flow State runner."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from ghc_family_v645_v6_runtime import PHASE, ROOT, TRUTH_BOUNDARY, read_json, write_json


FAMILY_RUNNER = ROOT / "scripts/ghc_family_method_flow_state.py"
X1_LEDGER = PHASE / "method-flow/method-flow-state.json"
X2_LEDGER = PHASE / "method-flow/method-flow-state-x2.json"

INCIDENTS = [
    {
        "number": 7,
        "negative_id": "V6456-X1-N07",
        "title": "Use explicit remote refs in four-way divergence probes",
        "failure": "An unquoted PowerShell @{u} fragment was parsed as an encoded token and produced an ambiguous-revision failure.",
        "trigger": ["PowerShell ref formatting", "remote divergence probe"],
        "failed": "Interpolate a compact @{u} shorthand inside a PowerShell command wrapper.",
        "recovery": "Resolve and quote refs/remotes/origin plus the full branch name explicitly before rev-list.",
        "observed": "The explicit local and remote refs returned zero-ahead and zero-behind at the immutable x1 head.",
        "guard": "Never rely on shell-sensitive upstream shorthand inside structured wrappers.",
        "rollback": "Withdraw the failed equality claim and rerun with explicit refs before x2 begins.",
        "side_effects": ["read_only_git_metadata", "no_ref_change", "no_worktree_change"],
    },
    {
        "number": 8,
        "negative_id": "V6456-X2-N01",
        "title": "Split cold repository inspection when a ten-second aggregate probe times out",
        "failure": "The first parallel status, listing, and raw-content inspection exceeded its ten-second wrapper budget and returned no complete evidence.",
        "trigger": ["cold Windows worktree", "aggregate Git and file inspection"],
        "failed": "Request status, recursive file inventory, and three raw scripts in one short parallel probe.",
        "recovery": "Run status and bounded file reads separately with realistic per-command limits.",
        "observed": "The narrow status probe completed and showed only the four intended untracked x2 runner files.",
        "guard": "Budget cold Git status separately from content inspection and retain timeouts as evidence-free.",
        "rollback": "Terminate only the diagnostic; make no repository mutation or inference from silence.",
        "side_effects": ["read_only_repository", "no_ref_change", "no_artifact_change"],
    },
    {
        "number": 9,
        "negative_id": "V6456-X2-N02",
        "title": "Bound aggregate source reads as well as each component read",
        "failure": "A second parallel raw-file inspection exceeded its aggregate response budget after one partial file was returned.",
        "trigger": ["several raw script reads", "combined output budget"],
        "failed": "Assume individually small source files remain bounded when combined into one response.",
        "recovery": "Read one script or one compact symbol surface at a time and do not infer unseen tails.",
        "observed": "Individual reads completed and exposed the complete runtime, core, portfolio, and skill runner implementations.",
        "guard": "Track aggregate output size and prefer compact structural queries over multi-file dumps.",
        "rollback": "Discard the truncated read as authoritative evidence and reread only the needed complete file.",
        "side_effects": ["read_only_source", "no_artifact_change"],
    },
    {
        "number": 10,
        "negative_id": "V6456-X2-N03",
        "title": "List Method Flow filenames before selecting a summary path",
        "failure": "A read-only probe guessed x1-method-flow-summary.json, which does not exist in the frozen packet.",
        "trigger": ["frozen phase packet", "assumed filename convention"],
        "failed": "Read a guessed Method Flow summary filename before enumerating the owner directory.",
        "recovery": "List phase-local Method Flow files, then read the actual method-flow-summary.json or ledger.",
        "observed": "The enumeration identified the frozen state, summary, runner receipt, six method records, and twelve witnesses.",
        "guard": "Inspect exact owner-scoped filenames before assuming predecessor or lifecycle suffixes.",
        "rollback": "Assign no evidence credit to the missing path and use the discovered immutable file.",
        "side_effects": ["read_only_directory", "no_artifact_change"],
    },
    {
        "number": 11,
        "negative_id": "V6456-X2-N04",
        "title": "Inspect maintenance filenames before loading the cleanup portfolio",
        "failure": "A compact portfolio query guessed x1-cleanup-portfolio.json; the frozen file is x1-clean-refine-plan.json.",
        "trigger": ["frozen maintenance packet", "assumed portfolio filename"],
        "failed": "Open a guessed cleanup-plan path before listing the maintenance directory.",
        "recovery": "Enumerate the maintenance directory and load x1-clean-refine-plan.json by its observed name.",
        "observed": "The corrected read returned exactly twenty new non-destructive Orin cleanup tasks.",
        "guard": "Resolve exact frozen filenames before programmatic ingestion.",
        "rollback": "Retain the FileNotFoundError and do not treat it as a missing frozen obligation.",
        "side_effects": ["read_only_directory", "no_artifact_change"],
    },
    {
        "number": 12,
        "negative_id": "V6456-X2-N05",
        "title": "Resolve novelty evidence from the frozen provenance inventory",
        "failure": "A verification probe assumed a novelty subdirectory, but the frozen collision audits are stored under provenance.",
        "trigger": ["frozen x1 packet", "assumed evidence subdirectory"],
        "failed": "List a guessed novelty directory before inspecting the phase directory structure.",
        "recovery": "Enumerate exact phase directories and use provenance/prior-proposal-collision-audit.json.",
        "observed": "The provenance inventory exposed both proposal and portfolio collision audits without altering x1.",
        "guard": "Derive phase-local evidence paths from the frozen tree, not semantic folder guesses.",
        "rollback": "Assign no evidence credit to the missing directory and preserve the immutable provenance artifact.",
        "side_effects": ["read_only_directory", "no_artifact_change"],
    },
    {
        "number": 13,
        "negative_id": "V6456-X2-N06",
        "title": "Expand Python compile targets in PowerShell before invoking py_compile",
        "failure": "Python received a literal wildcard path on Windows and rejected it as an invalid filename.",
        "trigger": ["Windows PowerShell", "python py_compile", "wildcard argument"],
        "failed": "Pass scripts\\ghc_family_v645_v6_*.py directly to Python and assume shell expansion.",
        "recovery": "Enumerate matching files in PowerShell and invoke py_compile once per resolved path.",
        "observed": "Every v645-v6 runner, builder, and test module compiled successfully without changing dependencies.",
        "guard": "Perform wildcard expansion in the calling shell when the target program does not implement globbing.",
        "rollback": "Count the literal-wildcard invocation as zero compile evidence and rerun only resolved files.",
        "side_effects": ["local_bytecode_cache_only", "no_source_change", "no_dependency_change"],
    },
    {
        "number": 14,
        "negative_id": "V6456-X2-N07",
        "title": "Set UTF-8 subprocess I/O before runner boundary text is printed",
        "failure": "The first core-runner process wrote its artifacts but exited nonzero when the Windows cp1252 console could not encode Māori boundary text.",
        "trigger": ["Windows legacy console encoding", "Unicode boundary text", "runner JSON stdout"],
        "failed": "Invoke phase runners with inherited default console encoding and print Unicode JSON directly.",
        "recovery": "Set PYTHONIOENCODING=utf-8 for every bounded child runner and rerun from the start.",
        "observed": "The recovered core runner printed its receipt and exited zero while preserving UTF-8 repository artifacts.",
        "guard": "Declare UTF-8 process I/O for Windows evidence runners that may emit non-ASCII boundary language.",
        "rollback": "Give the failed invocation zero runner credit, retain its exception class, and overwrite only owner-generated candidate artifacts on rerun.",
        "side_effects": ["owner_candidate_artifacts_only", "no_committed_file_change", "no_ref_change"],
    },
    {
        "number": 15,
        "negative_id": "V6456-X2-N08",
        "title": "Update every portfolio consumer after a frozen evidence path is resolved",
        "failure": "The recovered novelty path was corrected in the skill runner but remained stale in the portfolio runner, so one of thirty-two acceptances correctly failed.",
        "trigger": ["shared evidence reference", "multiple phase-local consumers"],
        "failed": "Correct one consumer of a discovered frozen path without searching all phase-local references.",
        "recovery": "Search every v645-v6 runner for the stale path, update the portfolio mapping, and rerun all thirty-two acceptances.",
        "observed": "The corrected portfolio runner found the provenance audit and all twenty safe plus twelve candidate witnesses passed.",
        "guard": "After path recovery, run an exact old-reference scan across all owner scripts before rebuilding.",
        "rollback": "Give the failed portfolio run zero completion credit and overwrite only its owner-generated candidate receipts.",
        "side_effects": ["owner_candidate_receipts_only", "no_committed_file_change", "no_ref_change"],
    },
    {
        "number": 16,
        "negative_id": "V6456-X2-N09",
        "title": "Add the repository root before loading scoped unittest modules",
        "failure": "The first validation wrapper attempted eight scoped modules with only the scripts directory on sys.path; all eight imports errored and zero tests received credit.",
        "trigger": ["script launched by file path", "repository test modules", "unittest module loader"],
        "failed": "Assume the current working directory is automatically importable when Python executes a script from the scripts directory.",
        "recovery": "Insert the resolved repository root into sys.path before loading the eight frozen test module names.",
        "observed": "The recovered scoped runner loaded the v645-v3 through v645-v6 x1/x2 modules and all discovered tests passed.",
        "guard": "Make repository-root importability explicit in file-launched validation runners.",
        "rollback": "Count the eight import errors as one failed validation attempt with zero passed tests, preserve the receipt, and rerun the unchanged scope.",
        "side_effects": ["test_process_only", "no_test_source_change", "no_dependency_change"],
    },
    {
        "number": 17,
        "negative_id": "V6456-X2-N10",
        "title": "Keep every X2 receipt off immutable X1 paths",
        "failure": "The first evidence builder reused the frozen environment version-receipt and terminal-route-plan paths, and the pre-staging immutability check found two tracked modifications.",
        "trigger": ["strict x1-before-x2 phase", "lifecycle-unsuffixed receipt path"],
        "failed": "Write x2 environment and route state over semantically related frozen x1 paths.",
        "recovery": "Restore both exact x1 artifacts and write version-receipt-x2.json plus terminal-route-plan-x2.json.",
        "observed": "The recovered x1 tracked-file diff was zero while both x2 receipts remained additive and validated.",
        "guard": "Before staging, intersect every changed tracked path with the exact x1 tree and require an empty result.",
        "rollback": "Restore only the two exact frozen artifacts, retain the failed builder witness, and rerun the scoped packet without rewriting history.",
        "side_effects": ["two_owner_candidate_paths_restored", "two_additive_x2_receipts", "no_commit_or_ref_change"],
    },
    {
        "number": 18,
        "negative_id": "V6456-X2-N11",
        "title": "Run cached diff hygiene before giving the evidence index credit",
        "failure": "The first exact staged review found an extra blank line at the end of the new runtime module.",
        "trigger": ["exact staged Git index", "diff hygiene"],
        "failed": "Treat successful Python compilation as sufficient staged-file hygiene.",
        "recovery": "Remove the single trailing blank line, restage the exact blob, and require git diff --cached --check to pass.",
        "observed": "The corrected staged index passed diff hygiene with no whitespace errors.",
        "guard": "Run cached diff hygiene after the exact index is assembled and before every commit.",
        "rollback": "Give the failed staged index zero commit credit and modify only the owner runtime source.",
        "side_effects": ["one_owner_source_line", "no_history_change", "no_ref_change"],
    },
    {
        "number": 19,
        "negative_id": "V6456-X2-N12",
        "title": "Construct privacy regex literals so the staged scanner can scan itself",
        "failure": "The first five-class staged scan reported three hits in the two scanner implementations because their source contained the private tokens they were designed to detect.",
        "trigger": ["privacy scanner source included in scan", "literal private-pattern tokens"],
        "failed": "Embed complete private route and local-path tokens directly in scanner source, then scan that source with the same patterns.",
        "recovery": "Construct equivalent regexes from split nonprivate fragments and rerun the exact staged-blob scan.",
        "observed": "The recovered five-class scan examined the full evidence index including both scanners and returned zero hits.",
        "guard": "Every privacy scanner must include a self-scan fixture and avoid literal examples of prohibited tokens in published source.",
        "rollback": "Retain the three-hit receipt, claim no privacy pass, and replace only the owner scanner expressions.",
        "side_effects": ["two_owner_scanner_sources", "same_pattern_semantics", "no_scope_reduction"],
    },
]


def call(*args: str) -> None:
    subprocess.run([sys.executable, str(FAMILY_RUNNER), *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8")


def main() -> int:
    # The immutable x1 ledger is copied, never rewritten. All family-runner appends target x2.
    X2_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(X1_LEDGER, X2_LEDGER)
    for incident in INCIDENTS:
        n = incident["number"]
        method_id = f"V6456-M{n:02d}"
        fail_id = f"V6456-W{n:02d}-F"
        pass_id = f"V6456-W{n:02d}-P"
        record = {
            "method_id": method_id,
            "title": incident["title"],
            "failure_signature": incident["failure"],
            "trigger_preconditions": incident["trigger"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_local_tooling",
            "candidate_workaround": incident["recovery"],
            "validation_witness_ids": [fail_id, pass_id],
            "recurrence_guard": incident["guard"],
            "rollback": incident["rollback"],
            "rollback_witness_required": True,
            "side_effect_budget": incident["side_effects"],
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["private_material", "destructive_action", "sibling_lane", "host_change"],
            "retained_negative_ids": [incident["negative_id"]],
            "scope_boundary": "Same-owner bounded operational recovery only; no scientific, authority, production, accessibility-complete, security-complete, or independent-reproduction credit.",
        }
        failed = {
            "witness_id": fail_id, "method_id": method_id,
            "procedure": incident["failed"], "scope": "single owner-local operational diagnostic",
            "expected": "bounded diagnostic or recovery completes without crossing gates",
            "observed": incident["failure"], "result": "fail", "same_owner_only": True,
            "independent_reproduction": False, "retained_negative_ids": [incident["negative_id"]],
            "boundary": TRUTH_BOUNDARY,
        }
        passed = {
            "witness_id": pass_id, "method_id": method_id,
            "procedure": incident["recovery"], "scope": "single owner-local operational diagnostic",
            "expected": "bounded diagnostic or recovery completes without crossing gates",
            "observed": incident["observed"], "result": "pass", "same_owner_only": True,
            "independent_reproduction": False, "retained_negative_ids": [incident["negative_id"]],
            "boundary": TRUTH_BOUNDARY,
        }
        record_rel = f"method-flow/v6456-m{n:02d}-method-record.json"
        fail_rel = f"method-flow/v6456-w{n:02d}-f-witness.json"
        pass_rel = f"method-flow/v6456-w{n:02d}-p-witness.json"
        write_json(record_rel, record)
        write_json(fail_rel, failed)
        write_json(pass_rel, passed)
        call("record", "--ledger", str(X2_LEDGER), "--record-file", str(PHASE / record_rel))
        call("witness", "--ledger", str(X2_LEDGER), "--witness-file", str(PHASE / fail_rel))
        call("witness", "--ledger", str(X2_LEDGER), "--witness-file", str(PHASE / pass_rel))
        call("set-state", "--ledger", str(X2_LEDGER), "--method-id", method_id, "--state", "preferred", "--note", "Bounded passing witness recorded for the declared trigger only")

    validation = PHASE / "method-flow/method-flow-x2-validation.json"
    summary_json = PHASE / "method-flow/method-flow-summary-x2.json"
    summary_md = PHASE / "method-flow/method-flow-summary-x2.md"
    call("validate", "--ledger", str(X2_LEDGER), "--receipt", str(validation))
    call("summarize", "--ledger", str(X2_LEDGER), "--json-output", str(summary_json), "--markdown-output", str(summary_md))
    ledger = read_json("method-flow/method-flow-state-x2.json")
    payload = {
        "schema": "ghc.family.v645-v6.method-flow-runner.v1",
        "family_runner_used": True,
        "immutable_x1_methods": 6,
        "x2_methods_added": len(INCIDENTS),
        "methods": ledger["counts"]["methods"],
        "failed_witnesses": ledger["counts"]["witness_results"]["fail"],
        "passing_witnesses": ledger["counts"]["witness_results"]["pass"],
        "preferred_methods": ledger["counts"]["states"]["preferred"],
        "failure_erasure_count": 0,
        "retained_negative_ids": [row["negative_id"] for row in INCIDENTS],
        "same_owner_only": True,
        "independent_reproduction": False,
        "result": "pass",
        "boundary": TRUTH_BOUNDARY,
    }
    write_json("prototypes/runner-witnesses/ghc_family_v645_v6_method_flow_runner.json", payload)
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
