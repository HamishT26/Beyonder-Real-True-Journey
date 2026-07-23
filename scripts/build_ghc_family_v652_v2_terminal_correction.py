#!/usr/bin/env python3
"""Build the narrow v652-v2 terminal validator correction packet."""

from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/orin-thale/v652-v2"
CLOSEOUT = "0053eef587ebdc88d8bafbf09b2f214737abd539"
EVIDENCE = "d185405470b9205a21d9b018bc0d3f7f44f49444"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO).decode("utf-8").strip()


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def replace_all(relative: str, replacements: list[tuple[str, str]], append: str = "") -> int:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        if old not in text:
            raise RuntimeError(f"missing correction anchor in {relative}: {old[:80]}")
        text = text.replace(old, new)
    if append:
        text = text.rstrip() + "\n\n" + append.strip() + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")
    return len(re.findall(r"\b\w+\b", text, flags=re.UNICODE))


def main() -> None:
    if git("rev-parse", "HEAD") != CLOSEOUT:
        raise SystemExit("terminal correction builder requires exact first closeout HEAD")

    truth = load("final/phase-truth.json")
    truth.update({
        "effective_negatives": 8203,
        "method_count": 28,
        "failed_witness_count": 30,
        "passing_witness_count": 28,
        "final_head_binding": "supplied_after_narrow_terminal_correction_commit",
        "canonical_pass_run": False,
        "canonical_replay_run": False,
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "Corrected final repository truth candidate; the first closeout-head invocation ran zero tests and has zero validation credit. Exact corrected-head validation and acknowledged route delivery remain external lifecycle gates."
    })
    write_json("final/phase-truth.json", truth)

    negatives = load("final/retained-negative-register.json")
    negatives.update({
        "schema": "ghc.family.v652-v2.retained-negatives.corrected-final.v1",
        "terminal_operational": [{
            "negative_id": "V6522-X2-N16",
            "category": "nonpackage_unittest_discovery",
            "failed": "The first exact-final invocation stopped before running any test because unittest discovery required the non-package tests directory to be importable.",
            "recovery": "Load the five exact test files with importlib file-module specs, count 39 tests without execution, and validate only the corrected pushed head.",
            "passing": "The dependency preflight loaded five exact modules, counted 39 tests, and consumed no successful canonical pass.",
            "recurrence_guard": "Use exact file-module loading for fixed selections when tests is not a package."
        }],
        "terminal_operational_count": 1,
        "effective_at_final": 8203,
        "no_failure_erased": True,
    })
    write_json("final/retained-negative-register.json", negatives)

    contract = load("final/final-validation-contract.json")
    contract.update({"expected_phase_commits": 4, "first_closeout_head": CLOSEOUT, "corrected_final_parent": CLOSEOUT, "exact_file_module_loader": True, "prior_failed_invocations": 1, "prior_tests_run": 0, "successful_pass_limit": 1, "replay_after_success": False})
    write_json("final/final-validation-contract.json", contract)
    write_json("final/terminal-correction-receipt.json", {
        "schema": "ghc.family.v652-v2.terminal-correction.v1", "first_closeout_head": CLOSEOUT, "evidence": EVIDENCE,
        "defect": "Non-package unittest discovery stopped the first exact-final invocation before any test ran.",
        "failed_invocation_credit": "zero", "failed_invocation_tests_run": 0,
        "recovery": "Exact file-module loading with a 39-test dependency-only count witness.",
        "expected_corrected_phase_commits": 4, "expected_corrected_final_parent": CLOSEOUT,
        "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid_candidate": True,
        "boundary": "Narrow validator transport correction only; no test-result or canonical validation credit until the corrected pushed head passes once."
    })
    write_json("final/corrected-seal-candidate.json", {"schema": "ghc.family.v652-v2.corrected-seal-candidate.v1", "first_closeout_head": CLOSEOUT, "expected_corrected_final_parent": CLOSEOUT, "exact_corrected_final_head": "bound_after_commit", "canonical_validation_state": "PENDING_SINGLE_SUCCESSFUL_PASS", "prior_failed_invocations": 1, "prior_tests_run": 0, "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid_candidate": True})

    baton_words = replace_all("handoffs/tamar-vey-v652-v3-activation.md", [
        ("- Expected source-to-final history: exactly three Orin phase commits, zero merges, one parent for final, and complete source/x1/evidence ancestry. Final must be the direct child of evidence.", "- Corrected source-to-final history: exactly four Orin phase commits, zero merges, one parent for final, and complete source/x1/evidence/first-closeout ancestry. Corrected final must be the direct child of first closeout `0053eef587ebdc88d8bafbf09b2f214737abd539`."),
        ("- Effective negatives at closeout: 8,202. No failure was erased or netted out by recovery.", "- Effective negatives at corrected final: 8,203. The added terminal negative is the zero-test non-package discovery failure; no failure was erased or netted out by recovery."),
        ("- Method Flow at closeout: 27 preferred methods, 29 retained failed witnesses, 27 bounded passing witnesses, and 56 witnesses total. Recovery erased no failure and earned no external authority or independent-reproduction credit.", "- Method Flow at corrected final: 28 preferred methods, 30 retained failed witnesses, 28 bounded passing witnesses, and 58 witnesses total. Recovery erased no failure and earned no external authority or independent-reproduction credit."),
        ("The 8,202 effective negatives comprise 8,022 inherited sealed and external activation negatives, 15 x1 operational negatives, 9 evidence-lifecycle operational negatives, six closeout diagnostic, precondition, partial-build, or document-contract negatives, and 150 executed rejected mutations.", "The 8,203 effective negatives comprise 8,022 inherited sealed and external activation negatives, 15 x1 operational negatives, 9 evidence-lifecycle operational negatives, six closeout diagnostic, precondition, partial-build, or document-contract negatives, one zero-test terminal validator discovery negative, and 150 executed rejected mutations."),
        ("Orin must run one dependency-justified successful canonical pass at the exact pushed final head, with no replay after success. A failed aggregate receives zero credit and becomes a retained negative.", "The first closeout-head invocation stopped before running any test because the tests directory is not a package; it has zero validation credit. The corrected loader binds the five exact files through importlib and counted 39 tests without executing them. Orin must run one dependency-justified successful canonical pass only at the corrected pushed final head, with no replay after success. Any failed aggregate receives zero credit and remains retained."),
        ("Preserve all 8,202 inherited negatives", "Preserve all 8,203 inherited negatives"),
    ], append="""## Narrow terminal correction truth

The first closeout head is `0053eef587ebdc88d8bafbf09b2f214737abd539`. Its exact-final validator invocation ran zero tests and stopped at module discovery because `tests` is not a package. That invocation receives zero validation credit, consumed no successful pass, changed no repository or route state, and remains `V6522-X2-N16`. The additive correction changes only the scoped loader and its truthful lifecycle surfaces: each of the five exact test files is loaded with an importlib file-module spec, the dependency preflight counts 39 tests without running them, and the single successful canonical pass remains reserved for the corrected pushed head. Tamar must preserve both the failed invocation and the corrected witness; neither is independent reproduction or full-suite evidence.""")
    overview_words = replace_all("overview/final-integrated-overview.md", [("8,202 effective negatives", "8,203 effective negatives")], append="""## Terminal correction

The first closeout-head validator invocation stopped before running any test because its discovery mechanism required the non-package tests directory to be importable. It has zero validation credit and remains retained as `V6522-X2-N16`. The narrow additive correction loads the five exact test files by file-module spec and counted 39 tests in a dependency-only preflight without executing the canonical suite. The single successful pass remains unused until the corrected head is committed, pushed, clean, and four-way remote-equal.""")
    report = ROOT / "reports/final-static-report.html"
    report_text = report.read_text(encoding="utf-8").replace("8,202 negatives", "8,203 negatives")
    report_text = report_text.replace("<h2>Route</h2>", "<h2>Terminal correction</h2><p>The first closeout-head validator ran zero tests because its discovery path required a package. The corrected exact-file loader preserves that failure and reserves the single successful pass for the corrected head.</p><h2>Route</h2>")
    report.write_text(report_text, encoding="utf-8", newline="\n")

    write_json("validation/terminal-correction-build-receipt.json", {"schema": "ghc.family.v652-v2.terminal-correction-build.v1", "built_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "first_closeout_head": CLOSEOUT, "effective_negatives": 8203, "methods": 28, "failed_witnesses": 30, "passing_witnesses": 28, "baton_words": baton_words, "overview_words": overview_words, "expected_tests": 39, "dependency_preflight_tests_run": 0, "route_state": "PREPARED_NOT_SENT", "valid": 10000 <= baton_words <= 100000 and overview_words >= 1500})
    if not (10000 <= baton_words <= 100000 and overview_words >= 1500):
        raise SystemExit({"baton_words": baton_words, "overview_words": overview_words})
    print(json.dumps({"baton_words": baton_words, "overview_words": overview_words, "negatives": 8203, "methods": 28, "expected_tests": 39, "route": "PREPARED_NOT_SENT", "valid": True}, sort_keys=True))


if __name__ == "__main__":
    main()
