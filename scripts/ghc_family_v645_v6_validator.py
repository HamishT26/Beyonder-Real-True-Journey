#!/usr/bin/env python3
"""Detailed and minimal validators for the bounded Orin v645-v6 packet."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v645_v6_runtime import PHASE, TRUTH_BOUNDARY, parse_json_documents, privacy_scan, read_json


def _exists(relative: str) -> bool:
    return (PHASE / relative).is_file()


def _check(label: str, condition: bool, checks: list[dict[str, Any]]) -> None:
    checks.append({"label": label, "passed": bool(condition)})


def validate(mode: str = "detailed") -> dict[str, Any]:
    if mode not in {"detailed", "minimal"}:
        raise ValueError(mode)
    checks: list[dict[str, Any]] = []
    core = read_json("prototypes/runner-witnesses/ghc_family_v645_v6_core_runner.json")
    rows = core["rows"]
    _check("ten core proposals", len(rows) == 10, checks)
    _check("four outcome vocabulary", set(row["outcome"] for row in rows) == {"completed", "represented", "open_gap", "exact_gate"}, checks)
    _check("outcome distribution", Counter(row["outcome"] for row in rows) == Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}), checks)
    _check("bounded acceptance", core["all_bounded_acceptance_passed"], checks)
    _check("terminal abstention", core["stage20_verdict"] == "NOT_READY_FOR_STAGE_20", checks)
    _check("synthetic negatives", read_json("validation/synthetic-mutation-negative-register.json")["count"] == 70, checks)
    _check("EHT zero rows", read_json("gmut/eht-shadow-zero-row-receipt.json")["real_rows"] == 0, checks)
    _check("EHT zero likelihoods", read_json("gmut/eht-shadow-zero-row-receipt.json")["likelihood_evaluations"] == 0, checks)
    _check("THOS zero people", read_json("thos/challenge-response-proxy-vectors.json")["real_participants"] == 0, checks)
    _check("Freed ID zero keys", read_json("freed-id/key-attestation-mutation-vectors.json")["real_keys"] == 0, checks)
    _check("CBR authority reserved", not read_json("cbr/fisheries-authority-reservation.json")["maori_authority_claimed"], checks)
    _check("same-owner only", not read_json("prototypes/runner-witnesses/ghc_family_v645_v6_boundary_runner.json")["independent_reproduction"], checks)
    _check("JSON parses", parse_json_documents()["valid"], checks)
    _check("owner privacy scan", privacy_scan()["valid"], checks)
    if mode == "detailed":
        expected_artifacts = [
            "method-flow/rollback-budget-contract.json", "method-flow/rollback-budget-vectors.json",
            "gmut/eikonal-transport-contract.json", "gmut/eikonal-mode-mutation-vectors.json",
            "gmut/eht-shadow-study-contract.json", "gmut/eht-shadow-zero-row-receipt.json",
            "thos/maritime-bridge-protocol.json", "thos/challenge-response-proxy-vectors.json",
            "freed-id/key-attestation-profile.json", "freed-id/key-attestation-mutation-vectors.json",
            "cbr/fisheries-authority-reservation.json", "cbr/observer-customary-harvest-matrix.md",
            "security/git-bundle-contract.json", "security/git-bundle-mutation-vectors.json",
            "accessibility/disclosure-contract.json", "accessibility/details-summary-audit.json",
            "thermo-psyche/clausius-contract.json", "thermo-psyche/cyclic-integral-mutation-vectors.json",
            "stage20/control-calibration-contract.json", "stage20/control-mutation-vectors.json",
        ]
        for relative in expected_artifacts:
            _check(f"artifact {relative}", _exists(relative), checks)
        portfolio = read_json("approval-packets/x2-execution-ledger.json")
        _check("20 safe-now executed", portfolio["safe_now_executed"] == 20, checks)
        _check("12 candidates executed", portfolio["candidates_executed"] == 12, checks)
        _check("10 exact preserved", portfolio["inherited_exact_preserved"] == 10, checks)
        _check("5 blocked preserved", portfolio["inherited_blocked_preserved"] == 5, checks)
        _check("no inherited packet executed", portfolio["inherited_packets_executed"] == 0, checks)
        skills = read_json("prototypes/skill-runner-execution-ledger.json")
        _check("12 skills built", skills["count"] == 12, checks)
        _check("12 skills invoked", skills["all_built_validated_invoked"], checks)
        _check("skills phase local", not skills["installed_globally"], checks)
        method = read_json("prototypes/runner-witnesses/ghc_family_v645_v6_method_flow_runner.json")
        _check("family Method Flow runner used", method["family_runner_used"], checks)
        _check("Method Flow failures retained", method["failed_witnesses"] == method["passing_witnesses"], checks)
        _check("Method Flow no erasure", method["failure_erasure_count"] == 0, checks)
        _check("Method Flow preferred has passes", method["preferred_methods"] == method["methods"], checks)
        bundle = read_json("security/git-bundle-mutation-vectors.json")
        _check("bundle lab disposable", bundle["disposable_lab"], checks)
        _check("bundle lab did not mutate canonical", not bundle["canonical_repository_mutated"], checks)
        _check("bundle lab did not mutate remote", not bundle["remote_mutated"], checks)
        _check("bundle expected failures observed", bundle["expected_results_passed"], checks)
        disclosure = read_json("accessibility/details-summary-audit.json")
        _check("disclosure vectors valid", disclosure["valid"], checks)
        _check("manual keyboard reserved", disclosure["manual_keyboard_evaluation"] == "reserved", checks)
        _check("assistive technology reserved", disclosure["assistive_technology_evaluation"] == "reserved", checks)
        _check("affected users reserved", disclosure["affected_user_evaluation"] == "reserved", checks)
        _check("Clausius vectors valid", read_json("thermo-psyche/cyclic-integral-mutation-vectors.json")["valid"], checks)
        _check("control calibration valid", read_json("stage20/control-mutation-vectors.json")["valid"], checks)
        for runner in ("core", "portfolio", "skill", "boundary", "method_flow"):
            _check(f"runner witness {runner}", _exists(f"prototypes/runner-witnesses/ghc_family_v645_v6_{runner}_runner.json"), checks)
        if _exists("phase-truth.json"):
            truth = read_json("phase-truth.json")
            _check("phase truth terminal", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", checks)
            _check("phase truth no deployment", not truth["claims"]["deployment_ready"], checks)
            _check("phase truth no independent reproduction", not truth["claims"]["independent_team_reproduction"], checks)
        if _exists("retained-negative-register.json"):
            negatives = read_json("retained-negative-register.json")
            _check("inherited effective negatives", negatives["counts"]["inherited_effective"] == 2172, checks)
            _check("synthetic negatives retained", negatives["counts"]["preregistered_synthetic"] == 70, checks)
            _check("no negative erasure", negatives["erased"] == 0, checks)
        if _exists("exact-open-gate-register.json"):
            gates = read_json("exact-open-gate-register.json")
            _check("open gaps remain", gates["counts"]["effective_open_gaps"] >= 8, checks)
            _check("exact gates remain", gates["counts"]["effective_exact_gates"] >= 9, checks)
            _check("no inherited gate silently closed", gates["silently_closed"] == 0, checks)
        if _exists("deliverables/v645-v6-static-report.html"):
            html = (PHASE / "deliverables/v645-v6-static-report.html").read_text(encoding="utf-8")
            for marker in ('lang="en"', '<title>', 'href="#main"', '<main id="main"', '<caption>', '<details>', '<summary>'):
                _check(f"report marker {marker}", marker in html, checks)
            _check("report reserves human evaluation", "Manual, assistive-technology, Māori-language, and affected-user evaluation remain reserved" in html, checks)
        for path in PHASE.rglob("*.md"):
            _check(f"word cap {path.relative_to(PHASE).as_posix()}", len(path.read_text(encoding="utf-8").split()) <= 6000, checks)
    passed = sum(row["passed"] for row in checks)
    return {
        "schema": f"ghc.family.v645-v6.validator.{mode}.v1",
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
