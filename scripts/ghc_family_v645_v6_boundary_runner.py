#!/usr/bin/env python3
"""Exercise the bounded truth and authority boundaries for Orin v645-v6."""

from __future__ import annotations

import json
from collections import Counter

from ghc_family_v645_v6_runtime import TRUTH_BOUNDARY, read_json, write_json


def main() -> int:
    core = read_json("prototypes/runner-witnesses/ghc_family_v645_v6_core_runner.json")
    checks = {
        "ten_core_rows": core["proposal_count"] == 10,
        "frozen_outcome_distribution": core["outcomes"] == {
            "completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1
        },
        "bounded_acceptance": core["all_bounded_acceptance_passed"],
        "eht_zero_real_rows": read_json("gmut/eht-shadow-zero-row-receipt.json")["real_rows"] == 0,
        "eht_zero_likelihoods": read_json("gmut/eht-shadow-zero-row-receipt.json")["likelihood_evaluations"] == 0,
        "thos_zero_people": all(
            read_json("thos/challenge-response-proxy-vectors.json")[key] == 0
            for key in ("real_participants", "real_operators", "real_arms")
        ),
        "freed_id_zero_real_keys": read_json("freed-id/key-attestation-mutation-vectors.json")["real_keys"] == 0,
        "freed_id_zero_live_interop": read_json("freed-id/key-attestation-mutation-vectors.json")["interoperability_events"] == 0,
        "cbr_no_case_or_authority_claim": not any(
            read_json("cbr/fisheries-authority-reservation.json")[key]
            for key in ("case_findings", "quota_decisions", "remedies_decided", "maori_authority_claimed", "legal_interpretation")
        ),
        "git_bundle_expected_results": read_json("security/git-bundle-mutation-vectors.json")["expected_results_passed"],
        "accessibility_structural_only": read_json("accessibility/details-summary-audit.json")["valid"]
            and read_json("accessibility/details-summary-audit.json")["manual_keyboard_evaluation"] == "reserved"
            and read_json("accessibility/details-summary-audit.json")["affected_user_evaluation"] == "reserved",
        "thermo_category_barrier": read_json("thermo-psyche/cyclic-integral-mutation-vectors.json")["valid"],
        "stage20_control_abstains": read_json("stage20/control-mutation-vectors.json")["stage20_verdict"] == "NOT_READY_FOR_STAGE_20",
        "synthetic_negative_count": read_json("validation/synthetic-mutation-negative-register.json")["count"] == 70,
    }
    outcomes = Counter(row["outcome"] for row in core["rows"])
    payload = {
        "schema": "ghc.family.v645-v6.boundary-runner.v1",
        "check_count": len(checks),
        "passed": sum(checks.values()),
        "checks": checks,
        "outcomes": dict(outcomes),
        "all_external_gates_preserved": True,
        "manual_accessibility_reserved": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "result": "pass" if all(checks.values()) else "fail",
        "boundary": TRUTH_BOUNDARY,
    }
    write_json("prototypes/runner-witnesses/ghc_family_v645_v6_boundary_runner.json", payload)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
