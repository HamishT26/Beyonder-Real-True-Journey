#!/usr/bin/env python3
"""Detailed and minimal validators for the bounded Tamar v645-v7 packet."""

from __future__ import annotations

import json
from collections import Counter
from typing import Any

from ghc_family_v645_v7_runtime import PHASE, TRUTH_BOUNDARY, parse_json_documents, privacy_scan, read_json


def _check(label: str, condition: bool, checks: list[dict[str, Any]]) -> None:
    checks.append({"label": label, "passed": bool(condition)})


def _exists(relative: str) -> bool:
    return (PHASE / relative).is_file()


def validate(mode: str = "detailed") -> dict[str, Any]:
    if mode not in {"detailed", "minimal"}:
        raise ValueError(mode)
    checks: list[dict[str, Any]] = []
    core = read_json("prototypes/runner-witnesses/ghc_family_v645_v7_core_runner.json")
    rows = core["rows"]
    _check("ten core proposals", len(rows) == 10, checks)
    _check("four outcome vocabulary", set(row["outcome"] for row in rows) == {"completed", "represented", "open_gap", "exact_gate"}, checks)
    _check("outcome distribution", Counter(row["outcome"] for row in rows) == Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}), checks)
    _check("bounded acceptance", core["all_bounded_acceptance_passed"], checks)
    _check("terminal abstention", core["stage20_verdict"] == "NOT_READY_FOR_STAGE_20", checks)
    _check("synthetic negatives", read_json("validation/synthetic-mutation-negative-register.json")["count"] == 70, checks)
    _check("Gaia zero rows", read_json("empirical/gaia-wide-binary-zero-row-receipt.json")["real_rows"] == 0, checks)
    _check("THOS zero people", read_json("thos/fixity-handover-proxy-vectors.json")["real_participants"] == 0, checks)
    _check("Freed ID zero keys", read_json("freed-id/batch-issuance-mutation-vectors.json")["real_keys"] == 0, checks)
    _check("CBR authority reserved", not read_json("cbr/community-archive-authority-reservation.json")["maori_authority_claimed"], checks)
    _check("same owner only", not read_json("prototypes/runner-witnesses/ghc_family_v645_v7_boundary_runner.json")["independent_reproduction"], checks)
    _check("JSON parses", parse_json_documents()["valid"], checks)
    _check("owner privacy scan", privacy_scan()["valid"], checks)
    if mode == "detailed":
        expected = [
            "method-flow/deadline-envelope-contract.json", "method-flow/probe-decomposition-vectors.json",
            "gmut/ward-anomaly-contract.json", "gmut/ward-anomaly-mutation-vectors.json",
            "empirical/gaia-wide-binary-study-contract.json", "empirical/gaia-wide-binary-zero-row-receipt.json",
            "thos/digital-preservation-ingest-protocol.json", "thos/fixity-handover-proxy-vectors.json",
            "freed-id/batch-issuance-profile.json", "freed-id/batch-issuance-mutation-vectors.json",
            "cbr/community-archive-authority-reservation.json", "cbr/embargo-takedown-consent-matrix.md",
            "security/python-import-cache-contract.json", "security/python-import-cache-mutation-vectors.json",
            "accessibility/modal-dialog-contract.json", "accessibility/modal-dialog-structural-audit.json",
            "thermo-psyche/maxwell-integrability-contract.json", "thermo-psyche/maxwell-relation-mutation-vectors.json",
            "stage20/holdout-contamination-contract.json", "stage20/adaptive-reuse-mutation-vectors.json",
        ]
        for relative in expected:
            _check(f"artifact {relative}", _exists(relative), checks)
        method = read_json("prototypes/runner-witnesses/ghc_family_v645_v7_method_flow_runner.json")
        _check("family Method Flow runner used", method["family_runner_used"], checks)
        _check("Method Flow failures retained", method["failed_witnesses"] == method["passing_witnesses"], checks)
        _check("Method Flow no erasure", method["failure_erasure_count"] == 0, checks)
        skills = read_json("prototypes/skill-runner-execution-ledger.json")
        _check("ten skills built", skills["count"] == 10, checks)
        _check("ten skills invoked", skills["all_built_validated_invoked"], checks)
        _check("skills phase local", not skills["installed_globally"], checks)
        _check("Python fixture disposable", read_json("security/python-import-cache-mutation-vectors.json")["temporary_root_removed"], checks)
        modal = read_json("accessibility/modal-dialog-structural-audit.json")
        _check("modal structural vectors", modal["valid"], checks)
        _check("manual accessibility reserved", modal["manual_keyboard_evaluation"] == "reserved" and modal["assistive_technology_evaluation"] == "reserved" and modal["affected_user_evaluation"] == "reserved", checks)
        _check("Maxwell category barrier", read_json("thermo-psyche/maxwell-relation-mutation-vectors.json")["valid"], checks)
        _check("holdout abstention", read_json("stage20/adaptive-reuse-mutation-vectors.json")["stage20_verdict"] == "NOT_READY_FOR_STAGE_20", checks)
        if _exists("x2-proposal-ledger.json"):
            ledger = read_json("x2-proposal-ledger.json")
            _check("x2 ten frozen executions", len(ledger["proposals"]) == 10, checks)
            _check("x2 IDs match x1", [row["proposal_id"] for row in ledger["proposals"]] == [f"V6457-P{i:02d}" for i in range(1, 11)], checks)
        if _exists("phase-truth.json"):
            truth = read_json("phase-truth.json")
            _check("phase truth terminal", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", checks)
            _check("phase truth no positive external claims", not any(truth["claims"].values()), checks)
        if _exists("retained-negative-register.json"):
            negatives = read_json("retained-negative-register.json")
            _check("inherited effective negatives", negatives["counts"]["inherited_effective"] == 2272, checks)
            _check("synthetic negatives retained", negatives["counts"]["preregistered_synthetic"] == 70, checks)
            _check("no negative erased", negatives["erased"] == 0, checks)
        if _exists("exact-open-gate-register.json"):
            gates = read_json("exact-open-gate-register.json")
            _check("open gaps remain", gates["counts"]["effective_open_gaps"] >= 9, checks)
            _check("exact gates remain", gates["counts"]["effective_exact_gates"] >= 10, checks)
            _check("no silent gate closure", gates["silently_closed"] == 0, checks)
        if _exists("deliverables/v645-v7-static-report.html"):
            html = (PHASE / "deliverables/v645-v7-static-report.html").read_text(encoding="utf-8")
            for marker in ('lang="en"', '<title>', 'href="#main"', '<main id="main"', '<caption>', '<details>', '<summary>'):
                _check(f"report marker {marker}", marker in html, checks)
            _check("report reserves human evaluation", "Manual keyboard, browser, assistive-technology, Maori-language, and affected-user evaluation remain reserved" in html, checks)
        if _exists("v645-v7-integrated-overview.md"):
            words = len((PHASE / "v645-v7-integrated-overview.md").read_text(encoding="utf-8").split())
            _check("overview three-page equivalent", 1500 <= words <= 6000, checks)
        for path in PHASE.rglob("*.md"):
            _check(f"word cap {path.relative_to(PHASE).as_posix()}", len(path.read_text(encoding="utf-8").split()) <= 6000, checks)
    passed = sum(row["passed"] for row in checks)
    return {
        "schema": f"ghc.family.v645-v7.validator.{mode}.v1",
        "mode": mode,
        "check_count": len(checks),
        "passed": passed,
        "failed": len(checks) - passed,
        "checks": checks,
        "result": "pass" if passed == len(checks) else "fail",
        "full_repository_suite": False,
        "full_repository_suite_owner": "Eiren Kestrel",
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": TRUTH_BOUNDARY,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["detailed", "minimal"], nargs="?", default="detailed")
    args = parser.parse_args()
    result = validate(args.mode)
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result["result"] == "pass" else 1)
