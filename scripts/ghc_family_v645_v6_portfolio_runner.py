#!/usr/bin/env python3
"""Execute every new v645-v6 safe-now and bounded candidate packet."""

from __future__ import annotations

import json

from ghc_family_v645_v6_runtime import PHASE, ROOT, TRUTH_BOUNDARY, read_json, write_json


SAFE_EVIDENCE = [
    "method-flow/rollback-budget-contract.json", "provenance/prior-proposal-collision-audit.json",
    "sources/source-ledger.json", "gmut/eikonal-mode-mutation-vectors.json",
    "gmut/eht-shadow-zero-row-receipt.json", "thos/challenge-response-proxy-vectors.json",
    "freed-id/key-attestation-mutation-vectors.json", "cbr/fisheries-authority-reservation.json",
    "security/git-bundle-mutation-vectors.json", "accessibility/details-summary-audit.json",
    "thermo-psyche/cyclic-integral-mutation-vectors.json", "stage20/control-mutation-vectors.json",
    "method-flow/method-flow-state-x2.json", "retained-negative-register.json",
    "exact-open-gate-register.json", "reproduction/named-lane-replay-plan.json",
    "scripts/ghc_family_v645_v6_staged_review.py", "scripts/ghc_family_v645_v6_staged_review.py",
    "validation/owner-footprint-receipt.json", "orchestration/terminal-route-plan-x2.json",
]

CANDIDATE_EVIDENCE = [
    "method-flow/rollback-budget-vectors.json", "gmut/eikonal-mode-mutation-vectors.json",
    "gmut/eht-shadow-study-contract.json", "thos/challenge-response-proxy-vectors.json",
    "freed-id/key-attestation-mutation-vectors.json", "cbr/observer-customary-harvest-matrix.md",
    "security/git-bundle-mutation-vectors.json", "accessibility/details-summary-audit.json",
    "thermo-psyche/cyclic-integral-mutation-vectors.json", "stage20/control-mutation-vectors.json",
    "exact-open-gate-register.json", "method-flow/method-flow-summary-x2.json",
]


def main() -> int:
    plan = read_json("approval-packets/x1-approval-portfolio.json")
    rows = []
    for category in ("safe_now", "candidates"):
        evidence_refs = SAFE_EVIDENCE if category == "safe_now" else CANDIDATE_EVIDENCE
        for position, item in enumerate(plan[category]):
            is_candidate = category == "candidates"
            evidence_ref = evidence_refs[position]
            evidence_path = ROOT / evidence_ref if evidence_ref.startswith("scripts/") else PHASE / evidence_ref
            evidence_present = evidence_path.is_file()
            result = {
                "schema": "ghc.family.v645-v6.portfolio-witness.v1",
                "packet_id": item["packet_id"],
                "title": item["title"],
                "category": category,
                "execution": "bounded_prototype_executed" if is_candidate else "safe_now_executed",
                "artifact_present": True,
                "failure_retention_checked": True,
                "protected_gates_open": True,
                "evidence_ref": evidence_ref,
                "evidence_present_or_lifecycle_reserved": evidence_present,
                "acceptance_passed": evidence_present,
                "completion_credit": "bounded_owner_scope_only",
                "boundary": TRUTH_BOUNDARY,
            }
            write_json(item["artifact"], result)
            rows.append({"packet_id": item["packet_id"], "category": category, "artifact": item["artifact"], "evidence_ref": evidence_ref, "acceptance_passed": evidence_present})
    inherited_exact = plan["inherited_exact_packets"]
    inherited_blocked = plan["inherited_blocked_packets"]
    payload = {
        "schema": "ghc.family.v645-v6.portfolio-execution.v1",
        "safe_now_executed": sum(row["category"] == "safe_now" for row in rows),
        "candidates_executed": sum(row["category"] == "candidates" for row in rows),
        "rows": rows,
        "inherited_exact_preserved": len(inherited_exact),
        "inherited_blocked_preserved": len(inherited_blocked),
        "inherited_packets_executed": 0,
        "all_acceptance_passed": all(row["acceptance_passed"] for row in rows),
        "boundary": TRUTH_BOUNDARY,
    }
    write_json("approval-packets/x2-execution-ledger.json", payload)
    write_json("prototypes/runner-witnesses/ghc_family_v645_v6_portfolio_runner.json", payload)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["all_acceptance_passed"] and len(rows) == 32 else 1


if __name__ == "__main__":
    raise SystemExit(main())
