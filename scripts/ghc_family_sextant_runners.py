"""Ten family-current bounded runners used by Vesper Arlen v673-v6."""

from __future__ import annotations

from collections import Counter
from typing import Any, Callable

from ghc_family_sextant_contracts import (
    canonical_digest,
    component_tree_receipt,
    jsonpath_values,
    structural_html_audit,
    validate_outcome_ledger,
    validate_synthetic_record,
)


def contract_runner(context: dict[str, Any]) -> dict[str, Any]:
    results = [validate_synthetic_record(row) for row in context["positive_records"]]
    return {"accepted": sum(result.accepted for result in results), "total": len(results), "passed": all(result.accepted for result in results)}


def mutation_runner(context: dict[str, Any]) -> dict[str, Any]:
    rejected = sum(not row["accepted"] for row in context["mutations"])
    return {"rejected": rejected, "total": len(context["mutations"]), "passed": rejected == len(context["mutations"])}


def provenance_runner(context: dict[str, Any]) -> dict[str, Any]:
    missing = [row["synthetic_id"] for row in context["positive_records"] if row["provenance"].get("fixture_origin") != "invented_phase_local"]
    return {"checked": len(context["positive_records"]), "missing": missing, "passed": not missing}


def canonical_runner(context: dict[str, Any]) -> dict[str, Any]:
    first = canonical_digest(context["ledger"])
    second = canonical_digest(dict(reversed(list(context["ledger"].items()))))
    return {"first": first["sha256"], "second": second["sha256"], "passed": first["sha256"] == second["sha256"]}


def query_runner(context: dict[str, Any]) -> dict[str, Any]:
    values = jsonpath_values(context["ledger"], "$.rows[*].outcome")
    return {"count": len(values), "counts": dict(sorted(Counter(values).items())), "passed": len(values) == 40}


def topology_runner(context: dict[str, Any]) -> dict[str, Any]:
    receipt = component_tree_receipt()
    return {**receipt, "passed": receipt["node_count"] == 9 and receipt["edge_count"] == 8 and receipt["depth"] == 2}


def gate_runner(context: dict[str, Any]) -> dict[str, Any]:
    protected = [row for row in context["ledger"]["rows"] if row["outcome"] in {"open_gap", "exact_gate"}]
    return {"protected_count": len(protected), "passed": len(protected) == 4 and all(row["real_rows"] == 0 for row in protected)}


def portfolio_runner(context: dict[str, Any]) -> dict[str, Any]:
    counts = context["portfolio_counts"]
    expected = {"safe_now": 60, "candidate": 30, "owner_skills": 20, "owner_runners": 10, "owner_clean_fix_refine": 60}
    return {"counts": counts, "expected": expected, "passed": all(counts.get(key) == value for key, value in expected.items())}


def accessibility_runner(context: dict[str, Any]) -> dict[str, Any]:
    return structural_html_audit(context["html"])


def terminal_refusal_runner(context: dict[str, Any]) -> dict[str, Any]:
    ledger_result = validate_outcome_ledger(context["ledger"]["rows"])
    forbidden = context.get("stage20_authorized") is True or context.get("independent_reproduction") is True
    return {"ledger_errors": list(ledger_result.errors), "stage20_authorized": False, "independent_reproduction": False, "passed": ledger_result.accepted and not forbidden}


RUNNERS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "ghc_family_sextant_contract_runner": contract_runner,
    "ghc_family_sextant_mutation_runner": mutation_runner,
    "ghc_family_sextant_provenance_runner": provenance_runner,
    "ghc_family_sextant_canonical_runner": canonical_runner,
    "ghc_family_sextant_query_runner": query_runner,
    "ghc_family_sextant_topology_runner": topology_runner,
    "ghc_family_sextant_gate_runner": gate_runner,
    "ghc_family_sextant_portfolio_runner": portfolio_runner,
    "ghc_family_sextant_accessibility_runner": accessibility_runner,
    "ghc_family_sextant_terminal_refusal_runner": terminal_refusal_runner,
}


def run_all(context: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for name, runner in RUNNERS.items():
        result = runner(context)
        rows.append({"runner": name, "tested": True, "used": True, "result": result, "passed": bool(result.get("passed") or result.get("structural_pass"))})
    return rows
