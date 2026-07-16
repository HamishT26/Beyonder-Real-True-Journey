#!/usr/bin/env python3
"""Check the bounded truth and authority limits for Sylven v645-v8."""

from __future__ import annotations

import json
from collections import Counter

from ghc_family_v645_v8_runtime import TRUTH_BOUNDARY, read_json, write_json


def main() -> int:
    core = read_json("prototypes/runner-witnesses/ghc_family_v645_v8_core_runner.json")
    euclid = read_json("empirical/euclid-q1-zero-row-receipt.json")
    thos = read_json("thos/rail-handover-proxy-vectors.json")
    freed = read_json("freed-id/bitstring-status-mutation-vectors.json")
    cbr = read_json("cbr/managed-retreat-authority-reservation.json")
    live = read_json("accessibility/live-region-structural-audit.json")
    checks = {
        "ten_core_rows": core["proposal_count"] == 10,
        "frozen_distribution": core["outcomes"] == {
            "completed": 6,
            "represented": 2,
            "open_gap": 1,
            "exact_gate": 1,
        },
        "bounded_acceptance": core["all_bounded_acceptance_passed"],
        "euclid_zero_rows": euclid["real_rows"] == 0 and euclid["downloads"] == 0 and euclid["inferred_shear_values"] == 0,
        "euclid_zero_likelihoods": euclid["likelihood_evaluations"] == 0 and euclid["constraints"] == 0,
        "thos_zero_people_and_operations": all(thos[key] == 0 for key in ("real_participants", "real_workers", "real_trains", "real_routes", "real_arms", "operational_instructions")),
        "freed_id_zero_real_events": all(freed[key] == 0 for key in ("real_keys", "real_proofs", "live_issuance", "live_resolution", "status_or_revocation_events", "interoperability_events")),
        "cbr_no_decision_or_authority": not any(cbr[key] for key in ("valuations", "relocation_decisions", "compensation_decisions", "tenancy_decisions", "remedies_decided", "legal_interpretation", "cultural_ratification", "maori_authority_claimed")),
        "sparse_lab_bounded": read_json("security/git-sparse-index-mutation-vectors.json")["expected_results_passed"],
        "accessibility_structural_only": live["valid"] and live["manual_keyboard_evaluation"] == "reserved" and live["affected_user_evaluation"] == "reserved" and not live["complete_wcag_claim"],
        "thermo_category_barrier": read_json("thermo-psyche/gibbs-duhem-mutation-vectors.json")["valid"],
        "stage20_abstains": read_json("stage20/entity-leakage-mutation-vectors.json")["stage20_verdict"] == "NOT_READY_FOR_STAGE_20",
        "synthetic_negative_count": read_json("validation/synthetic-mutation-negative-register.json")["count"] == 70,
    }
    outcomes = Counter(row["outcome"] for row in core["rows"])
    payload = {
        "schema": "ghc.family.v645-v8.boundary-runner.v1",
        "check_count": len(checks),
        "passed": sum(checks.values()),
        "checks": checks,
        "outcomes": dict(outcomes),
        "all_external_gates_preserved": True,
        "manual_accessibility_reserved": True,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "result": "pass" if all(checks.values()) else "fail",
        "boundary": TRUTH_BOUNDARY,
    }
    write_json("prototypes/runner-witnesses/ghc_family_v645_v8_boundary_runner.json", payload)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
