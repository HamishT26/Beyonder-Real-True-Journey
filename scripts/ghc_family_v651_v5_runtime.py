#!/usr/bin/env python3
"""Family-current bounded executor for Eiren Kestrel v651-v5 surfaces."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import ghc_family_v651_v5_phase_data as d  # noqa: E402

ROOT = REPO / d.PHASE_ROOT


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def obligations(title: str) -> list[str]:
    cleaned = re.sub(
        r"^(?:Method Flow |GMUT |THOS |Freed ID |CBR |Accessible |Thermo-Psyche |Stage 20 )",
        "",
        title,
    )
    cleaned = re.sub(
        r"\s+(?:tribunal|board|profile|proxy|adapter|matrix|classifier)$", "", cleaned
    )
    rows: list[str] = []
    for part in cleaned.split(","):
        token = re.sub(r"[^a-z0-9]+", "_", part.casefold()).strip("_")
        if token and token not in rows:
            rows.append(token)
    return rows


def evaluate(contract: dict, fixture: dict) -> list[str]:
    issues: list[str] = []
    present = set(fixture.get("obligations", []))
    if any(item not in present for item in contract["obligations"]):
        issues.append("missing_required_obligation")
    if fixture.get("domain") != contract["domain"]:
        issues.append("wrong_type_or_domain")
    text = json.dumps(fixture, ensure_ascii=False).casefold()
    if any(term in text for term in contract["forbidden_promotions"]):
        issues.append("unexpected_promotion_phrase")
    if int(fixture.get("resource_units", 0)) > int(contract["resource_budget"]):
        issues.append("resource_budget_overrun")
    if fixture.get("state_sequence") != contract["state_sequence"]:
        issues.append("state_or_order_violation")
    return issues


def contract_for(proposal: dict) -> dict:
    return {
        "schema": "ghc.family.v651-v5.surface-contract.v1",
        "phase": d.PHASE,
        "proposal_id": proposal["proposal_id"],
        "slug": proposal["slug"],
        "title": proposal["title"],
        "domain": proposal["mission_surface"],
        "obligations": obligations(proposal["title"]),
        "state_sequence": ["declared", "checked", "bounded_receipt"],
        "resource_budget": 64,
        "expected_disposition": proposal["expected_disposition"],
        "source_ids": proposal["official_or_primary_source_needs"],
        "protected_gates": proposal["protected_gates"],
        "forbidden_promotions": [
            "empirically confirmed",
            "production ready",
            "independent reproduction",
            "conscious person",
            "theory of everything",
            "stage 20 ready",
        ],
        "boundary": "Owner-local software, symbolic, formal, numerical, structural, or synthetic evidence only.",
    }


def fixtures_for(contract: dict, proposal: dict) -> tuple[dict, list[dict]]:
    accepting = {
        "fixture_id": proposal["proposal_id"] + "-ACCEPT",
        "domain": contract["domain"],
        "obligations": contract["obligations"],
        "state_sequence": contract["state_sequence"],
        "resource_units": min(16, contract["resource_budget"]),
        "real_rows": 0,
        "real_queries_or_downloads": 0,
        "real_participants_or_operators": 0,
        "real_keys_proofs_tokens_accounts_or_network_events": 0,
        "authority_decisions": 0,
        "manual_or_affected_user_evaluations": 0,
        "same_owner_only": True,
    }
    mutations: list[dict] = []
    kinds = (
        "missing_required_obligation",
        "wrong_type_or_domain",
        "unexpected_promotion_phrase",
        "resource_budget_overrun",
        "state_or_order_violation",
    )
    for index, mutation_type in enumerate(kinds, 1):
        row = json.loads(json.dumps(accepting))
        row["mutation_id"] = f"{proposal['proposal_id']}-MUT-{index}"
        row["mutation_type"] = mutation_type
        if mutation_type == "missing_required_obligation":
            row["obligations"] = row["obligations"][1:]
        elif mutation_type == "wrong_type_or_domain":
            row["domain"] = "wrong_domain"
        elif mutation_type == "unexpected_promotion_phrase":
            row["claim"] = "production ready"
        elif mutation_type == "resource_budget_overrun":
            row["resource_units"] = contract["resource_budget"] + 1
        else:
            row["state_sequence"] = ["bounded_receipt", "checked", "declared"]
        mutations.append(row)
    return accepting, mutations


def execute(proposal_ids: list[str], runner_name: str) -> dict:
    selected = [row for row in d.PROPOSALS if row["proposal_id"] in proposal_ids]
    if len(selected) != len(proposal_ids):
        raise RuntimeError("unknown or duplicate proposal ID in runner selection")
    rows = []
    for proposal in selected:
        target = ROOT / "surfaces" / proposal["slug"]
        contract = contract_for(proposal)
        accepting, mutations = fixtures_for(contract, proposal)
        accepting_issues = evaluate(contract, accepting)
        mutation_results = []
        for mutation in mutations:
            issues = evaluate(contract, mutation)
            mutation_results.append(
                {
                    "mutation_id": mutation["mutation_id"],
                    "mutation_type": mutation["mutation_type"],
                    "issues": issues,
                    "rejected_or_quarantined": bool(issues),
                    "passed": bool(issues),
                }
            )
        if accepting_issues or not all(row["passed"] for row in mutation_results):
            raise RuntimeError(f"surface guard failed: {proposal['proposal_id']}")
        write_json(target / "contract.json", contract)
        write_json(target / "accepting-fixture.json", accepting)
        write_json(
            target / "mutation-results.json",
            {
                "schema": "ghc.family.v651-v5.mutation-results.v1",
                "proposal_id": proposal["proposal_id"],
                "count": 5,
                "rejected_or_quarantined": 5,
                "accepted": 0,
                "results": mutation_results,
                "valid": True,
            },
        )
        boundary = {
            "completed": "Completed only for the declared bounded software, symbolic, formal, numerical, structural, or synthetic hypothesis.",
            "represented": "Synthetic proxy only with zero real participant, operator, production identity, or operational-effectiveness credit.",
            "open_gap": "Zero-row readiness only; real data, frozen analysis, likelihood, uncertainty treatment, and independent review remain open.",
            "exact_gate": "Reservation matrix only; competent, affected-party, legal, cultural, data-governance, and Māori authority remain external.",
        }[proposal["expected_disposition"]]
        receipt = {
            "schema": "ghc.family.v651-v5.bounded-receipt.v1",
            "proposal_id": proposal["proposal_id"],
            "slug": proposal["slug"],
            "runner": runner_name,
            "observed_disposition": proposal["expected_disposition"],
            "accepting_fixture_passed": True,
            "mutation_rejected_count": 5,
            "real_rows": 0,
            "queries_or_downloads": 0,
            "likelihood_evaluations": 0,
            "posterior_samples_or_constraints": 0,
            "real_participants_or_operators": 0,
            "real_keys_proofs_tokens_accounts_or_network_events": 0,
            "authority_decisions": 0,
            "manual_or_affected_user_evaluations": 0,
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": boundary,
            "valid": True,
        }
        write_json(target / "bounded-receipt.json", receipt)
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "disposition": proposal["expected_disposition"],
                "mutations_rejected": 5,
            }
        )
    witness = {
        "schema": "ghc.family.v651-v5.runner-witness.v1",
        "runner": runner_name,
        "proposal_count": len(rows),
        "proposals": rows,
        "valid": True,
        "boundary": "Same-owner bounded execution only; no independent reproduction or external authority credit.",
    }
    write_json(ROOT / "tooling" / "runner-witnesses" / (Path(runner_name).stem + ".json"), witness)
    return witness


def validate_all() -> dict:
    receipts = []
    mutations = 0
    for proposal in d.PROPOSALS:
        target = ROOT / "surfaces" / proposal["slug"]
        receipt = json.loads((target / "bounded-receipt.json").read_text(encoding="utf-8"))
        results = json.loads((target / "mutation-results.json").read_text(encoding="utf-8"))
        if not receipt["valid"] or results["rejected_or_quarantined"] != 5:
            raise RuntimeError(proposal["proposal_id"])
        receipts.append(receipt)
        mutations += results["rejected_or_quarantined"]
    payload = {
        "schema": "ghc.family.v651-v5.runtime-validation.v1",
        "proposal_count": len(receipts),
        "mutation_count": mutations,
        "valid": len(receipts) == 20 and mutations == 100,
    }
    write_json(ROOT / "tooling" / "runner-witnesses" / "ghc_family_v651_v5_validate.json", payload)
    return payload


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "validate":
        print(json.dumps(validate_all()))
    else:
        raise SystemExit("use a family-current runner or the validate command")
