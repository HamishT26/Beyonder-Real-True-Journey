#!/usr/bin/env python3
"""Build the second narrow v652-v2 terminal correction packet."""

from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/orin-thale/v652-v2"
CORRECTION1 = "19239aa3b00c8d7e32b329a2addae8391c8662a8"
CLOSEOUT = "0053eef587ebdc88d8bafbf09b2f214737abd539"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO).decode("utf-8").strip()


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = ROOT / relative; path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def replace_all(relative: str, replacements: list[tuple[str, str]], append: str = "") -> int:
    path = ROOT / relative; text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        if old not in text: raise RuntimeError(f"missing correction anchor in {relative}: {old[:100]}")
        text = text.replace(old, new)
    if append: text = text.rstrip() + "\n\n" + append.strip() + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")
    return len(re.findall(r"\b\w+\b", text, flags=re.UNICODE))


def main() -> None:
    if git("rev-parse", "HEAD") != CORRECTION1: raise SystemExit("second correction builder requires exact first-correction HEAD")
    truth = load("final/phase-truth.json")
    truth.update({"effective_negatives": 8212, "method_count": 37, "failed_witness_count": 39, "passing_witness_count": 35, "final_head_binding": "supplied_after_second_narrow_terminal_correction", "canonical_pass_run": False, "canonical_replay_run": False, "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": "Second corrected final repository truth candidate; two failed exact-head aggregates and eight precommit tooling or review faults have zero validation credit. Exact second-correction validation and acknowledged route delivery remain external lifecycle gates."})
    write_json("final/phase-truth.json", truth)
    negatives = load("final/retained-negative-register.json")
    additions = [
        {
            "negative_id": "V6522-X2-N17", "category": "lifecycle_test_and_scanner_definition_selection",
            "failed": "The first-correction aggregate passed 38 of 39 tests but included one inherited x1 no-x2-surface assertion and falsely classified three pattern literals in the correction review source as privacy payload hits.",
            "recovery": "Exclude only the named inherited lifecycle-local test, retain all other tests, and add the exact active correction scanner source to the definition set.",
            "passing": "The dependency preflight counted 39 raw and 38 eligible tests with one explicit exclusion and classified all three prior candidates as scanner definitions without running the suite.",
            "recurrence_guard": "Inventory lifecycle-local assertions and every active scanner definition before canonical aggregation."
        },
        {
            "negative_id": "V6522-X2-N18", "category": "truncated_index_mutation_response",
            "failed": "The narrow self-exclusion restage response exceeded the tool output budget and was truncated before attributable completion evidence returned.",
            "recovery": "Do not repeat the mutation; compare the exact manifest path set with the staged and unstaged index using bounded count-only output.",
            "passing": "The read-only comparison proved 21 declared and staged paths, zero missing, zero extra, zero unstaged, and all four self-exclusions staged.",
            "recurrence_guard": "Separate state-changing commands from bounded exact-index postflight and never retry an unattributed mutation blindly."
        },
        {
            "negative_id": "V6522-X2-N19", "category": "manifest_path_and_schema_assumption",
            "failed": "A read-only parity probe guessed a generic manifest directory and object-shaped self-exclusions, so the file was absent and the derived counts were unusable.",
            "recovery": "Discover the exact lifecycle filename, inspect its schema, and combine entry paths with string-valued self-exclusions before comparison.",
            "passing": "The corrected schema-aware comparison loaded the exact validation manifest and proved complete 21-path staged parity with zero unstaged paths.",
            "recurrence_guard": "Bind manifest location and exclusion shape from the exact staged artifact instead of inferring either."
        },
        {
            "negative_id": "V6522-X2-N20", "category": "atomic_builder_patch_anchor_mismatch",
            "failed": "A broad builder patch mixed desired transformed-document text with current source anchors and was rejected atomically before mutation.",
            "recovery": "Re-read the exact builder bytes and patch small current-byte hunks independently.",
            "passing": "Exact current source anchors were identified and the rejected patch was confirmed to have made no partial change.",
            "recurrence_guard": "Bind generated-builder edits to current source bytes, never only to intended target text."
        },
        {
            "negative_id": "V6522-X2-N21", "category": "compound_worktree_probe_timeout",
            "failed": "A compound staged, unstaged, and untracked count probe timed out while repeated line-ending warnings expanded its work and output.",
            "recovery": "Use one bounded porcelain-status read without untracked traversal.",
            "passing": "The single status read completed with 21 tracked rows, 21 staged paths, and 15 paths with newer unstaged regeneration changes.",
            "recurrence_guard": "Avoid compound working-tree diff enumeration after generated text rewrites."
        },
        {
            "negative_id": "V6522-X2-N22", "category": "powershell_search_quote_parser",
            "failed": "A mixed double-quoted ripgrep alternation containing JSON quotes was rejected by PowerShell before the search ran.",
            "recovery": "Use one fixed-string single-quoted search per exact builder anchor.",
            "passing": "The fixed-string search identified the exact truth, retained-negative, build-receipt, and print lines.",
            "recurrence_guard": "Do not compose quote-bearing regex alternations in PowerShell."
        },
        {
            "negative_id": "V6522-X2-N23", "category": "staged_review_wrapper_timeout",
            "failed": "The exact correction staged-review wrapper reached its 120-second supervision limit without attributable output.",
            "recovery": "Inspect the exact child lifecycle before any retry and reserve a measured wider window for a later complete review.",
            "passing": "No pass credit is assigned to the timed-out wrapper; its continuing child was tracked separately.",
            "recurrence_guard": "Budget immutable manifest replay from measured workload and never restart a still-running child."
        },
        {
            "negative_id": "V6522-X2-N24", "category": "wrapper_child_lifecycle_assumption",
            "failed": "The wrapper timeout was initially assumed to have ended the child, but one exact review process remained active.",
            "recovery": "Monitor the existing child to exit without restart and inspect its single attributable receipt.",
            "passing": "The process count fell from one to zero without restart and one complete receipt was attributable.",
            "recurrence_guard": "Treat wrapper status and child lifecycle as separate evidence."
        },
        {
            "negative_id": "V6522-X2-N25", "category": "method_flow_changed_during_staged_review",
            "failed": "The continuing review child completed after timeout-derived Method Flow evidence changed the ledger, so its receipt reported one unstaged path and was invalid.",
            "recovery": "Reconcile all known Method Flow evidence, freeze the ledger, restage the exact correction set, and run one final review without concurrent ledger mutation.",
            "passing": "The invalid receipt still preserved 222 JSON parses, zero privacy hits, six valid prior-manifest replays, and exactly one unstaged ledger path, but receives zero review credit.",
            "recurrence_guard": "Complete and freeze Method Flow before the final staged snapshot."
        }
    ]
    present = {item["negative_id"] for item in negatives["terminal_operational"]}
    negatives["terminal_operational"].extend(item for item in additions if item["negative_id"] not in present)
    negatives.update({"schema": "ghc.family.v652-v2.retained-negatives.second-corrected-final.v1", "terminal_operational_count": 10, "effective_at_final": 8212, "no_failure_erased": True})
    write_json("final/retained-negative-register.json", negatives)
    contract = load("final/final-validation-contract.json")
    contract.update({"expected_phase_commits": 5, "second_correction_parent": CORRECTION1, "raw_scoped_tests": 39, "expected_eligible_tests": 38, "explicit_lifecycle_exclusions": [{"file": "test_ghc_family_v652_v1_x1.py", "test": "test_document_caps_privacy_and_x1_only", "reason": "Inherited x1 lifecycle-local no-x2-surface assertion"}], "prior_failed_invocations": 2, "prior_failed_test_runs": [0, 39], "precommit_tooling_negative_ids": ["V6522-X2-N18", "V6522-X2-N19", "V6522-X2-N20", "V6522-X2-N21", "V6522-X2-N22", "V6522-X2-N23", "V6522-X2-N24", "V6522-X2-N25"], "successful_pass_limit": 1, "replay_after_success": False})
    write_json("final/final-validation-contract.json", contract)
    write_json("final/terminal-correction-2-receipt.json", {"schema": "ghc.family.v652-v2.terminal-correction-2.v1", "first_correction_head": CORRECTION1, "first_closeout_head": CLOSEOUT, "defect": "One inherited x1 self-state test was lifecycle-local and the final scanner omitted the active correction-review definition path.", "failed_invocation_credit": "zero", "failed_invocation_tests": {"passed": 38, "total": 39}, "failed_privacy_confirmed_hits": 3, "precommit_tooling_negative_ids": ["V6522-X2-N18", "V6522-X2-N19", "V6522-X2-N20", "V6522-X2-N21", "V6522-X2-N22", "V6522-X2-N23", "V6522-X2-N24", "V6522-X2-N25"], "recovery": "One exact lifecycle-test exclusion plus one exact scanner-definition addition, followed by schema-aware index attribution, child-lifecycle monitoring, and a frozen Method Flow snapshot after eight retained tooling or review faults.", "expected_corrected_phase_commits": 5, "expected_corrected_final_parent": CORRECTION1, "expected_raw_tests": 39, "expected_eligible_tests": 38, "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid_candidate": True})
    write_json("final/corrected-seal-2-candidate.json", {"schema": "ghc.family.v652-v2.corrected-seal-2-candidate.v1", "first_correction_head": CORRECTION1, "expected_corrected_final_parent": CORRECTION1, "exact_corrected_final_head": "bound_after_commit", "canonical_validation_state": "PENDING_SINGLE_SUCCESSFUL_PASS", "prior_failed_invocations": 2, "successful_passes": 0, "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid_candidate": True})

    baton_words = replace_all("handoffs/tamar-vey-v652-v3-activation.md", [
        ("- Second-corrected source-to-final history: exactly five Orin phase commits, zero merges, one parent for final, and complete source/x1/evidence/first-closeout/first-correction ancestry. Final must be the direct child of first correction `19239aa3b00c8d7e32b329a2addae8391c8662a8`.", "- Second-corrected source-to-final history: exactly five Orin phase commits, zero merges, one parent for final, and complete source/x1/evidence/first-closeout/first-correction ancestry. Final must be the direct child of first correction `19239aa3b00c8d7e32b329a2addae8391c8662a8`."),
        ("- Effective negatives at second-corrected final: 8,209. Seven terminal negatives retain both failed validator aggregates and five precommit tooling faults through the bounded status and fixed-string inspection recoveries; no failure was erased or netted out by recovery.", "- Effective negatives at second-corrected final: 8,212. Ten terminal negatives retain both failed validator aggregates and eight precommit tooling or review faults through the frozen-ledger staged-review boundary; no failure was erased or netted out by recovery."),
        ("- Method Flow at second-corrected final: 34 preferred methods, 36 retained failed witnesses, 34 bounded passing witnesses, and 70 witnesses total. Recovery erased no failure and earned no external authority or independent-reproduction credit.", "- Method Flow at second-corrected final: 37 methods, of which 35 are preferred and two remain candidates; 39 retained failed witnesses, 35 bounded passing witnesses, and 74 witnesses total. Recovery erased no failure and earned no external authority or independent-reproduction credit."),
        ("The 8,209 effective negatives comprise 8,022 inherited sealed and external activation negatives, 15 x1 operational negatives, 9 evidence-lifecycle operational negatives, six closeout diagnostic, precondition, partial-build, or document-contract negatives, two terminal validator aggregate negatives, five terminal postflight tooling negatives, and 150 executed rejected mutations.", "The 8,212 effective negatives comprise 8,022 inherited sealed and external activation negatives, 15 x1 operational negatives, 9 evidence-lifecycle operational negatives, six closeout diagnostic, precondition, partial-build, or document-contract negatives, two terminal validator aggregate negatives, eight terminal tooling or review negatives, and 150 executed rejected mutations."),
        ("Preserve all 8,209 inherited negatives", "Preserve all 8,212 inherited negatives"),
        ("The loader binds five exact files through importlib. The second preflight counted 39 raw tests and 38 eligible tests after excluding only the inherited v652-v1 x1 self-state assertion `test_document_caps_privacy_and_x1_only`; it also classified the active correction-review source as a scanner definition. Orin must run one dependency-justified successful canonical pass only at the second-corrected pushed final head", "The loader binds five exact files through importlib. The second preflight counted 39 raw tests and 38 eligible tests after excluding only the inherited v652-v1 x1 self-state assertion `test_document_caps_privacy_and_x1_only`; it also classified the active correction-review source as a scanner definition. Orin must run one dependency-justified successful canonical pass only at the second-corrected pushed final head"),
    ], append="""## Frozen-ledger staged-review boundary

Three further zero-credit negatives remain `V6522-X2-N23` through `V6522-X2-N25`. The 120-second review wrapper timed out while its child continued; the initial assumption that the child had ended was false; and the child eventually returned an invalid receipt because timeout-derived Method Flow evidence had changed the ledger after its staged snapshot. The receipt still preserved 222 JSON parses, zero privacy hits, six valid prior-manifest replays, and exactly one unstaged ledger path. Method Flow is now frozen at 37 methods and 74 witnesses before the final staged review; the two review-related methods remain candidates rather than receiving premature promotion.""")
    overview_words = replace_all("overview/final-integrated-overview.md", [("8,209 effective negatives", "8,212 effective negatives")], append="""## Frozen-ledger staged-review boundary

The first correction-two review wrapper timed out while its child continued. That child later produced an invalid receipt because timeout-derived Method Flow evidence had changed the ledger, leaving exactly one unstaged path. Its 222 JSON parses, zero privacy hits, and six valid inherited-manifest replays remain observations, but the review has zero credit. Method Flow is now frozen at 37 methods and 74 witnesses before the final staged review; two methods remain candidates rather than being promoted without a committed bounded witness.""")
    report = ROOT / "reports/final-static-report.html"; text = report.read_text(encoding="utf-8").replace("8,209 negatives", "8,212 negatives")
    text = text.replace("<h2>Route</h2>", "<h2>Frozen-ledger review boundary</h2><p>A review-wrapper timeout, a false child-exit assumption, and one invalid review with an unstaged Method Flow ledger remain zero-credit negatives. Method Flow is frozen at 37 methods and 74 witnesses before final staged review; two methods remain candidates.</p><h2>Route</h2>")
    report.write_text(text, encoding="utf-8", newline="\n")
    write_json("validation/terminal-correction-2-build-receipt.json", {"schema": "ghc.family.v652-v2.terminal-correction-2-build.v1", "built_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "first_correction_head": CORRECTION1, "effective_negatives": 8212, "methods": 37, "failed_witnesses": 39, "passing_witnesses": 35, "baton_words": baton_words, "overview_words": overview_words, "raw_tests": 39, "eligible_tests": 38, "dependency_preflight_tests_run": 0, "route_state": "PREPARED_NOT_SENT", "valid": 10000 <= baton_words <= 100000 and overview_words >= 1500})
    if not (10000 <= baton_words <= 100000 and overview_words >= 1500): raise SystemExit({"baton_words": baton_words, "overview_words": overview_words})
    print(json.dumps({"baton_words": baton_words, "overview_words": overview_words, "negatives": 8212, "methods": 37, "eligible_tests": 38, "route": "PREPARED_NOT_SENT", "valid": True}, sort_keys=True))


if __name__ == "__main__": main()
