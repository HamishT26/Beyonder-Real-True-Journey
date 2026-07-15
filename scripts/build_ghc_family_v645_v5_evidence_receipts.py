#!/usr/bin/env python3
"""Run scoped checks and build the Sable Rook v645-v5 evidence receipts."""

from __future__ import annotations

import io
import json
import subprocess
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs/sable-rook/v645-v5"
PHASE = "v645-gmut-thos-v5-x1-x2"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_v645_v5_validator import validate  # noqa: E402

MODULES = [
    "tests.test_ghc_family_v645_v3_x1", "tests.test_ghc_family_v645_v3",
    "tests.test_ghc_family_v645_v4_x1", "tests.test_ghc_family_v645_v4",
    "tests.test_ghc_family_v645_v5_x1", "tests.test_ghc_family_v645_v5",
]


def write(relative: str, payload: dict) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def run_tests() -> tuple[unittest.result.TestResult, float, str]:
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader
    for module in MODULES:
        suite.addTests(loader.loadTestsFromName(module))
    stream = io.StringIO()
    started = time.perf_counter()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return result, time.perf_counter() - started, stream.getvalue()


def main() -> int:
    result, seconds, output = run_tests()
    detailed = validate("detailed")
    minimal = validate("minimal")
    write("validation/evidence-candidate-detailed.json", detailed)
    write("validation/evidence-candidate-minimal.json", minimal)
    write("validation/scoped-repository-test-receipt.json", {
        "schema": "ghc.family.scoped-test-receipt.v2", "phase": PHASE,
        "scope": ["v645-v3 x1 and x2", "v645-v4 x1 and x2", "v645-v5 x1 and x2"],
        "modules": MODULES, "tests_run": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors),
        "seconds": round(seconds, 3), "result": "pass" if result.wasSuccessful() else "fail",
        "full_repository_suite": False, "full_repository_suite_owner": "Eiren Kestrel",
        "same_owner_only": True, "independent_reproduction": False,
        "runner_output_summary": output.strip().splitlines()[-1] if output.strip() else "",
    })
    truth = json.loads((PHASE_DIR / "phase-truth.json").read_text(encoding="utf-8"))
    stale = [key for key, value in truth["protected_claims"].items() if value is not False]
    write("validation/stale-label-review.json", {
        "schema": "ghc.family.stale-label-review.v2", "phase": PHASE,
        "terminal_verdict": truth["terminal_verdict"],
        "protected_false_fields": list(truth["protected_claims"]),
        "stale_or_promoted_fields": stale, "issue_count": len(stale),
        "result": "pass" if not stale and truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20" else "fail",
    })
    write("validation/evidence-receipt.json", {
        "schema": "ghc.family.evidence-receipt.v2", "phase": PHASE,
        "x1_commit": "2e330ab76f03c05ff556c484c22851d682b0ac7b",
        "scoped_tests": {"run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors)},
        "detailed": {"checks": detailed["check_count"], "result": detailed["result"]},
        "minimal": {"checks": minimal["check_count"], "result": minimal["result"]},
        "privacy": "pending exact staged Git-blob review",
        "manifest": "pending exact staged Git-blob review",
        "same_owner_only": True, "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })

    json_files = list(PHASE_DIR.rglob("*.json"))
    json_errors = []
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            json_errors.append(path.relative_to(PHASE_DIR).as_posix())
    markdown = list(PHASE_DIR.rglob("*.md"))
    word_counts = {path.relative_to(PHASE_DIR).as_posix(): len(path.read_text(encoding="utf-8").split()) for path in markdown}
    over = {path: count for path, count in word_counts.items() if count > 6000}
    overview_words = word_counts["v645-v5-integrated-overview.md"]
    diff_check = subprocess.run(["git", "diff", "--check"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    write("validation/json-document-diff-receipt.json", {
        "schema": "ghc.family.json-document-diff-receipt.v1", "phase": PHASE,
        "json_parses_before_staged_review": len(json_files), "json_errors": json_errors,
        "markdown_documents": len(markdown), "maximum_words": max(word_counts.values()),
        "over_6000_words": over, "overview_words": overview_words,
        "diff_hygiene": "pass" if diff_check.returncode == 0 else "fail",
        "diff_hygiene_output": diff_check.stdout.strip(),
        "result": "pass" if not json_errors and not over and overview_words >= 1500 and diff_check.returncode == 0 else "fail",
    })
    # Recount after all receipt files exist; rewriting these files does not change the count.
    final_json_count = len(list(PHASE_DIR.rglob("*.json")))
    evidence = json.loads((PHASE_DIR / "validation/evidence-receipt.json").read_text(encoding="utf-8"))
    evidence["json_parses_before_staged_review"] = final_json_count
    evidence["overview_words"] = overview_words
    evidence["diff_hygiene"] = "pass" if diff_check.returncode == 0 else "fail"
    write("validation/evidence-receipt.json", evidence)
    receipt = json.loads((PHASE_DIR / "validation/json-document-diff-receipt.json").read_text(encoding="utf-8"))
    receipt["json_parses_before_staged_review"] = final_json_count
    write("validation/json-document-diff-receipt.json", receipt)

    passed = result.wasSuccessful() and detailed["result"] == "pass" and minimal["result"] == "pass" and not stale and not json_errors and not over and overview_words >= 1500 and diff_check.returncode == 0
    print(json.dumps({"tests": result.testsRun, "detailed": detailed["check_count"], "minimal": minimal["check_count"], "json": final_json_count, "overview_words": overview_words, "result": "pass" if passed else "fail"}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
