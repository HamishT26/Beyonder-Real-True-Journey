#!/usr/bin/env python3
"""Bounded synthetic contract runtime for Elaren Kestrel v665-v8.

The runtime validates JSON fixtures only.  It never performs network, device,
identity, filesystem-destructive, professional, legal, cultural, or authority
actions.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any


ALLOWED_DISPOSITIONS = {"completed", "represented", "open_gap", "exact_gate"}
FORBIDDEN_VALUE_MARKERS = {
    "operate_scanner",
    "authority_granted",
    "professional_conformance",
    "stage_20_ready",
    "real_person_record",
    "production_deployment",
}


def _type_matches(value: Any, expected: str) -> bool:
    if expected == "bool":
        return isinstance(value, bool)
    if expected == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "str":
        return isinstance(value, str)
    if expected == "list":
        return isinstance(value, list)
    if expected == "dict":
        return isinstance(value, dict)
    return False


def validate_fixture(contract: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    """Validate one synthetic fixture against one frozen proposal contract."""

    errors: list[str] = []
    required_core = {
        "proposal_id",
        "synthetic_only",
        "real_data_rows",
        "participant_count",
        "network_calls",
        "external_actions",
        "authority_status",
        "production",
        "deployment",
        "outcome_claim",
        "domain_payload",
    }
    missing_core = sorted(required_core - fixture.keys())
    if missing_core:
        errors.append("missing_core:" + ",".join(missing_core))

    if fixture.get("proposal_id") != contract.get("proposal_id"):
        errors.append("proposal_id_mismatch")
    if fixture.get("synthetic_only") is not True:
        errors.append("synthetic_only_required")
    for zero_field in ("real_data_rows", "participant_count", "network_calls"):
        if fixture.get(zero_field) != 0 or isinstance(fixture.get(zero_field), bool):
            errors.append(zero_field + "_must_be_zero")
    if fixture.get("external_actions") != []:
        errors.append("external_actions_must_be_empty")
    if fixture.get("authority_status") != "none":
        errors.append("authority_status_must_be_none")
    if fixture.get("production") is not False:
        errors.append("production_must_be_false")
    if fixture.get("deployment") is not False:
        errors.append("deployment_must_be_false")
    if fixture.get("outcome_claim") != "bounded_structural_only":
        errors.append("outcome_claim_exceeds_boundary")

    domain = fixture.get("domain_payload")
    rules = contract.get("required_domain_fields", {})
    if not isinstance(domain, dict):
        errors.append("domain_payload_must_be_object")
        domain = {}
    missing_domain = sorted(set(rules) - set(domain))
    extra_domain = sorted(set(domain) - set(rules))
    if missing_domain:
        errors.append("missing_domain:" + ",".join(missing_domain))
    if extra_domain:
        errors.append("unexpected_domain:" + ",".join(extra_domain))
    for field, rule in rules.items():
        if field not in domain:
            continue
        value = domain[field]
        if not _type_matches(value, rule["type"]):
            errors.append(f"wrong_type:{field}:{rule['type']}")
            continue
        if "allowed" in rule and value not in rule["allowed"]:
            errors.append("value_not_allowed:" + field)
        if "const" in rule and value != rule["const"]:
            errors.append("const_mismatch:" + field)
        if rule.get("nonempty") and hasattr(value, "__len__") and len(value) == 0:
            errors.append("empty_value:" + field)

    serialized = json.dumps(fixture, ensure_ascii=False, sort_keys=True).casefold()
    for marker in sorted(FORBIDDEN_VALUE_MARKERS):
        if marker in serialized:
            errors.append("forbidden_value_marker:" + marker)

    disposition = contract.get("expected_disposition")
    if disposition not in ALLOWED_DISPOSITIONS:
        errors.append("invalid_expected_disposition")

    return {
        "proposal_id": contract.get("proposal_id"),
        "valid": not errors,
        "errors": errors,
        "error_count": len(errors),
        "synthetic_only": True,
        "external_actions": 0,
    }


def _wrong_type(value: Any) -> Any:
    if isinstance(value, bool):
        return "not-a-boolean"
    if isinstance(value, int):
        return "not-an-integer"
    if isinstance(value, float):
        return "not-a-number"
    if isinstance(value, str):
        return ["not", "a", "string"]
    if isinstance(value, list):
        return {"not": "a-list"}
    if isinstance(value, dict):
        return ["not", "an", "object"]
    return None


def build_mutations(contract: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    positive = contract["bounded_positive_fixture"]
    first_domain = next(iter(contract["required_domain_fields"]))
    mutations: list[tuple[str, dict[str, Any]]] = []

    missing = copy.deepcopy(positive)
    del missing["domain_payload"][first_domain]
    mutations.append(("M01", missing))

    wrong = copy.deepcopy(positive)
    wrong["domain_payload"][first_domain] = _wrong_type(
        wrong["domain_payload"][first_domain]
    )
    mutations.append(("M02", wrong))

    authority = copy.deepcopy(positive)
    authority["authority_status"] = "authority_granted"
    mutations.append(("M03", authority))

    external = copy.deepcopy(positive)
    external["external_actions"] = ["operate_scanner"]
    mutations.append(("M04", external))

    promotion = copy.deepcopy(positive)
    promotion["outcome_claim"] = "professional_conformance"
    mutations.append(("M05", promotion))
    return mutations


def evaluate_contract(contract: dict[str, Any]) -> dict[str, Any]:
    positive = validate_fixture(contract, contract["bounded_positive_fixture"])
    mutation_rows = []
    for suffix, fixture in build_mutations(contract):
        result = validate_fixture(contract, fixture)
        mutation_rows.append(
            {
                "mutation_id": f"{contract['proposal_id']}-{suffix}",
                "accepted": result["valid"],
                "rejected": not result["valid"],
                "errors": result["errors"],
                "aggregate_credit": 0,
                "retained_negative": True,
            }
        )
    return {
        "proposal_id": contract["proposal_id"],
        "positive": positive,
        "mutations": mutation_rows,
        "mutation_count": len(mutation_rows),
        "rejected_mutation_count": sum(row["rejected"] for row in mutation_rows),
        "passed": positive["valid"] and all(row["rejected"] for row in mutation_rows),
    }


def load_contract(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_tree(phase_root: Path) -> dict[str, Any]:
    paths = sorted((phase_root / "x2" / "proposals").glob("*/contract.json"))
    rows = [evaluate_contract(load_contract(path)) for path in paths]
    return {
        "contract_count": len(rows),
        "passed_contract_count": sum(row["passed"] for row in rows),
        "mutation_count": sum(row["mutation_count"] for row in rows),
        "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in rows),
        "rows": rows,
        "passed": bool(rows) and all(row["passed"] for row in rows),
    }


def self_test() -> dict[str, Any]:
    contract = {
        "proposal_id": "SELF-TEST",
        "expected_disposition": "completed",
        "required_domain_fields": {"token": {"type": "str", "nonempty": True}},
        "bounded_positive_fixture": {
            "proposal_id": "SELF-TEST",
            "synthetic_only": True,
            "real_data_rows": 0,
            "participant_count": 0,
            "network_calls": 0,
            "external_actions": [],
            "authority_status": "none",
            "production": False,
            "deployment": False,
            "outcome_claim": "bounded_structural_only",
            "domain_payload": {"token": "SYNTHETIC"},
        },
    }
    result = evaluate_contract(contract)
    result["self_test"] = True
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("self-test", "contract", "tree"))
    parser.add_argument("path", nargs="?")
    args = parser.parse_args()
    if args.mode == "self-test":
        result = self_test()
    elif args.mode == "contract":
        if not args.path:
            parser.error("contract mode requires a path")
        result = evaluate_contract(load_contract(Path(args.path)))
    else:
        if not args.path:
            parser.error("tree mode requires the phase root")
        result = evaluate_tree(Path(args.path))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
