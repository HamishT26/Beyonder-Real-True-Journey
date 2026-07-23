#!/usr/bin/env python3
"""Bounded synthetic execution engine for Eiren Kestrel v652-v5."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

try:
    import ghc_family_v652_v5_phase_data as d
except ModuleNotFoundError:
    from scripts import ghc_family_v652_v5_phase_data as d


PROMOTION_GATES = {
    "empirical_confirmation",
    "production_readiness",
    "professional_authority",
    "legal_authority",
    "cultural_authority",
    "maori_authority",
    "complete_accessibility",
    "privacy_complete",
    "exhaustive_security",
    "independent_reproduction",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
}


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")


def obligations_for(proposal: dict[str, Any]) -> list[str]:
    """Derive stable declared obligations from the frozen comma-separated title."""
    title = proposal["title"]
    terminal_terms = {
        "tribunal",
        "board",
        "profile",
        "proxy",
        "adapter",
        "reservation",
        "classifier",
        "audit",
        "refusal",
        "nonproduction",
        "nonpromotion",
        "observation-firewall",
        "agency-nonconversion",
        "likelihood-refusal",
    }
    obligations: list[str] = []
    for part in title.split(","):
        token = _slug(part)
        for terminal in terminal_terms:
            token = token.removesuffix("-" + terminal).removesuffix(terminal)
        token = token.strip("-")
        if token and token not in obligations:
            obligations.append(token)
    if len(obligations) < 6:
        raise ValueError(f"{proposal['proposal_id']} has too few derived obligations")
    return obligations


def contract_for(proposal: dict[str, Any]) -> dict[str, Any]:
    obligations = obligations_for(proposal)
    return {
        "schema": "ghc.family.v652-v5.bounded-contract.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "proposal_id": proposal["proposal_id"],
        "slug": proposal["slug"],
        "title": proposal["title"],
        "pillar": proposal["pillar"],
        "approval_class": proposal["approval_class"],
        "execution_lane": proposal["execution_lane"],
        "declared_obligations": obligations,
        "official_or_primary_source_needs": proposal[
            "official_or_primary_source_needs"
        ],
        "protected_gates": proposal["protected_gates"],
        "expected_disposition": proposal["expected_disposition"],
        "resource_budget": {
            "maximum_fixture_bytes": 65536,
            "maximum_records": 64,
            "maximum_depth": 16,
        },
        "real_world_counters_required_zero": {
            "queries": 0,
            "downloads": 0,
            "real_rows": 0,
            "real_people": 0,
            "real_keys": 0,
            "real_services": 0,
            "real_stations": 0,
            "real_instruments": 0,
            "real_observations": 0,
            "real_bulletins": 0,
            "real_decisions": 0,
            "likelihoods": 0,
            "posteriors": 0,
            "constraints": 0,
        },
        "falsifier_or_acceptance_gate": proposal[
            "falsifier_or_acceptance_gate"
        ],
        "rollback_or_recovery": proposal["rollback_or_recovery"],
        "boundary": (
            "Disposable owner-local software, symbolic, formal, structural, or "
            "synthetic evidence only. The declared outcome class does not promote "
            "another class or confer empirical, professional, identity, legal, "
            "cultural, Māori, production, or Stage 20 authority."
        ),
    }


def good_candidate(contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "proposal_id": contract["proposal_id"],
        "execution_lane": contract["execution_lane"],
        "obligations": {
            obligation: {"present": True, "typed": True, "unit_or_domain_checked": True}
            for obligation in contract["declared_obligations"]
        },
        "fixture_bytes": 1024,
        "records": min(8, contract["resource_budget"]["maximum_records"]),
        "depth": min(4, contract["resource_budget"]["maximum_depth"]),
        "promotion_attempts": [],
        "privacy_or_authority_breach": False,
        "real_world_counters": dict(contract["real_world_counters_required_zero"]),
    }


def evaluate(contract: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    quarantine = False
    if candidate.get("execution_lane") != contract["execution_lane"]:
        reasons.append("execution_lane_mismatch")
    obligations = candidate.get("obligations", {})
    for obligation in contract["declared_obligations"]:
        row = obligations.get(obligation)
        if not row or not row.get("present"):
            reasons.append(f"missing_obligation:{obligation}")
        elif not row.get("typed") or not row.get("unit_or_domain_checked"):
            reasons.append(f"type_or_unit_failure:{obligation}")
    budget = contract["resource_budget"]
    if candidate.get("fixture_bytes", 0) > budget["maximum_fixture_bytes"]:
        reasons.append("fixture_byte_budget_exceeded")
    if candidate.get("records", 0) > budget["maximum_records"]:
        reasons.append("record_budget_exceeded")
    if candidate.get("depth", 0) > budget["maximum_depth"]:
        reasons.append("depth_budget_exceeded")
    promotions = set(candidate.get("promotion_attempts", []))
    unsupported = sorted(promotions & PROMOTION_GATES)
    if unsupported:
        quarantine = True
        reasons.extend(f"unsupported_promotion:{item}" for item in unsupported)
    if candidate.get("privacy_or_authority_breach"):
        quarantine = True
        reasons.append("privacy_or_authority_breach")
    counters = candidate.get("real_world_counters", {})
    for key, expected in contract["real_world_counters_required_zero"].items():
        if counters.get(key) != expected:
            quarantine = True
            reasons.append(f"real_world_counter_nonzero:{key}")
    accepted = not reasons
    return {
        "accepted": accepted,
        "decision": "accept" if accepted else ("quarantine" if quarantine else "reject"),
        "reasons": sorted(set(reasons)),
        "observed_disposition": (
            contract["expected_disposition"] if accepted else "not_credited"
        ),
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": contract["boundary"],
    }


def mutations(contract: dict[str, Any]) -> list[dict[str, Any]]:
    first = contract["declared_obligations"][0]
    rows: list[tuple[str, str, dict[str, Any]]] = []

    missing = good_candidate(contract)
    missing["obligations"].pop(first)
    rows.append(("M01", "missing_required_obligation", missing))

    wrong_type = good_candidate(contract)
    wrong_type["obligations"][first]["typed"] = False
    wrong_type["obligations"][first]["unit_or_domain_checked"] = False
    rows.append(("M02", "wrong_type_or_unit", wrong_type))

    overrun = good_candidate(contract)
    overrun["fixture_bytes"] = contract["resource_budget"]["maximum_fixture_bytes"] + 1
    overrun["records"] = contract["resource_budget"]["maximum_records"] + 1
    rows.append(("M03", "resource_or_replay_overrun", overrun))

    promotion = good_candidate(contract)
    promotion["promotion_attempts"] = ["stage20", "empirical_confirmation"]
    rows.append(("M04", "unsupported_promotion", promotion))

    authority = good_candidate(contract)
    authority["privacy_or_authority_breach"] = True
    authority["real_world_counters"]["real_decisions"] = 1
    rows.append(("M05", "authority_or_privacy_breach", authority))

    output = []
    for suffix, dimension, candidate in rows:
        result = evaluate(contract, candidate)
        output.append(
            {
                "mutation_id": f"{contract['proposal_id']}-{suffix}",
                "dimension": dimension,
                "decision": result["decision"],
                "accepted": result["accepted"],
                "reasons": result["reasons"],
                "expected": "reject_or_quarantine",
                "passed": not result["accepted"]
                and result["decision"] in {"reject", "quarantine"},
            }
        )
    return output


def execute_proposal(proposal: dict[str, Any]) -> dict[str, Any]:
    contract = contract_for(proposal)
    baseline = evaluate(contract, good_candidate(contract))
    mutation_rows = mutations(contract)
    valid = baseline["accepted"] and all(row["passed"] for row in mutation_rows)
    digest_payload = json.dumps(
        {
            "proposal_id": proposal["proposal_id"],
            "contract": contract,
            "baseline": baseline,
            "mutations": mutation_rows,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return {
        "contract": contract,
        "mutation_results": {
            "schema": "ghc.family.v652-v5.mutation-results.v1",
            "proposal_id": proposal["proposal_id"],
            "count": len(mutation_rows),
            "rejected_or_quarantined_count": sum(
                1 for row in mutation_rows if row["passed"]
            ),
            "rows": mutation_rows,
            "valid": all(row["passed"] for row in mutation_rows),
            "boundary": (
                "Executed synthetic mutations only; rejection or quarantine is "
                "bounded guard evidence, not real-world assurance."
            ),
        },
        "bounded_receipt": {
            "schema": "ghc.family.v652-v5.bounded-receipt.v1",
            "proposal_id": proposal["proposal_id"],
            "observed_outcome": (
                proposal["expected_disposition"] if valid else "not_credited"
            ),
            "baseline_accepted": baseline["accepted"],
            "mutation_count": len(mutation_rows),
            "mutation_rejected_or_quarantined_count": sum(
                1 for row in mutation_rows if row["passed"]
            ),
            "real_world_counters": contract["real_world_counters_required_zero"],
            "evidence_digest": hashlib.sha256(digest_payload).hexdigest(),
            "valid": valid,
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": contract["boundary"],
        },
    }


def execute_ids(
    proposal_ids: Iterable[str], output_root: Path | None = None
) -> list[dict[str, Any]]:
    by_id = {proposal["proposal_id"]: proposal for proposal in d.PROPOSALS}
    results = []
    for proposal_id in proposal_ids:
        if proposal_id not in by_id:
            raise KeyError(f"unknown proposal {proposal_id}")
        result = execute_proposal(by_id[proposal_id])
        if output_root is not None:
            proposal = by_id[proposal_id]
            target = output_root / proposal["slug"]
            target.mkdir(parents=True, exist_ok=True)
            for key, filename in (
                ("contract", "contract.json"),
                ("mutation_results", "mutation-results.json"),
                ("bounded_receipt", "bounded-receipt.json"),
            ):
                (target / filename).write_text(
                    json.dumps(
                        result[key], ensure_ascii=False, indent=2, sort_keys=True
                    )
                    + "\n",
                    encoding="utf-8",
                    newline="\n",
                )
        results.append(result)
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposal-id", action="append", required=True)
    parser.add_argument("--output-root", type=Path)
    args = parser.parse_args()
    results = execute_ids(args.proposal_id, args.output_root)
    print(
        json.dumps(
            {
                "proposal_count": len(results),
                "valid_count": sum(
                    1 for result in results if result["bounded_receipt"]["valid"]
                ),
                "mutation_count": sum(
                    result["mutation_results"]["count"] for result in results
                ),
                "mutation_rejected_or_quarantined_count": sum(
                    result["mutation_results"][
                        "rejected_or_quarantined_count"
                    ]
                    for result in results
                ),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
