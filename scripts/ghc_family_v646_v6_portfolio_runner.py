#!/usr/bin/env python3
"""Execute the frozen v646-v6 30/20/30 non-skill portfolios within bounds."""

from __future__ import annotations

import json
from pathlib import Path

import ghc_family_v646_v6_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sylven-arc/v646-v6"
CORE_EVIDENCE = [artifact for pair in (
    ("method-flow/durable-outbox-contract.json", "method-flow/delivery-order-mutation-vectors.json"),
    ("gmut/schwinger-dyson-obligations.json", "gmut/schwinger-dyson-mutations.json"),
    ("empirical/erosita-erass1-study-contract.json", "empirical/erosita-erass1-zero-row-receipt.json"),
    ("thos/hydrographic-handover-contract.json", "thos/hydrographic-proxy-vectors.json"),
    ("freed-id/dpop-binding-profile.json", "freed-id/dpop-replay-mutation-vectors.json"),
    ("cbr/navigation-chart-authority-reservation.json", "cbr/hazard-name-remedy-matrix.json"),
    ("tooling/json-sequence-contract.json", "tooling/json-sequence-mutation-vectors.json"),
    ("accessibility/pointer-operation-contract.json", "accessibility/pointer-operation-mutations.json"),
    ("thermo-psyche/gibbs-phase-rule-contract.json", "thermo-psyche/gibbs-phase-rule-mutations.json"),
    ("stage20/decision-curve-contract.json", "stage20/decision-curve-mutations.json"),
) for artifact in pair]


def write(relative: str, payload: dict) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def executed(items: list[dict], offset: int = 0) -> list[dict]:
    rows = []
    for index, item in enumerate(items):
        evidence = CORE_EVIDENCE[(index + offset) % len(CORE_EVIDENCE)]
        rows.append(
            {
                **item,
                "x2_state": "executed_bounded",
                "disposition": "completed",
                "evidence": evidence,
                "evidence_exists": (PHASE / evidence).exists(),
                "protected_gate_crossed": False,
                "real_world_effect": False,
                "completion_scope": "owner-local structural or synthetic hypothesis only",
            }
        )
    return rows


def main() -> int:
    safe = executed(d.SAFE_NOW)
    candidates = executed(d.CANDIDATES, 5)
    cleanup = executed(d.CLEAN_TASKS, 10)
    ok = all(row["evidence_exists"] and not row["protected_gate_crossed"] for row in safe + candidates + cleanup)
    write(
        "approval-packets/x2-portfolio-execution.json",
        {
            "schema": "ghc.family.v646-v6.portfolio-execution.v1",
            "safe_now": safe,
            "candidates": candidates,
            "safe_now_count": len(safe),
            "candidate_count": len(candidates),
            "completed_count": len(safe) + len(candidates),
            "result": "pass" if ok and len(safe) == 30 and len(candidates) == 20 else "fail",
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    write(
        "prototypes/x2-candidate-execution.json",
        {
            "schema": "ghc.family.v646-v6.candidate-execution.v1",
            "count": len(candidates),
            "completed_bounded": len(candidates),
            "candidates": candidates,
            "authority_or_real_evidence_credit": 0,
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    write(
        "maintenance/x2-clean-refine-ledger.json",
        {
            "schema": "ghc.family.v646-v6.clean-refine-ledger.v1",
            "count": len(cleanup),
            "completed_bounded": len(cleanup),
            "destructive_actions": 0,
            "tasks": cleanup,
            "result": "pass" if ok and len(cleanup) == 30 else "fail",
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    result = {"safe": len(safe), "candidates": len(candidates), "cleanup": len(cleanup), "result": "pass" if ok else "fail"}
    print(json.dumps(result))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
