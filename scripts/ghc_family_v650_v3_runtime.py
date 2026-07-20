"""Bounded structural runtime shared by v650-v3 proposal and runner witnesses."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}
FORBIDDEN_PROMOTIONS = {
    "empirical_confirmation", "production_ready", "personhood", "agi", "asi",
    "legal_authority", "cultural_authority", "maori_authority", "stage20_ready",
    "independent_reproduction", "exhaustive_security", "complete_accessibility",
}


def validate_contract(contract: dict) -> dict:
    issues: list[str] = []
    if not contract.get("obligations"):
        issues.append("missing_obligations")
    if contract.get("disposition") not in ALLOWED:
        issues.append("invalid_disposition")
    if not contract.get("boundaries"):
        issues.append("missing_boundaries")
    if set(contract.get("claims", [])) & FORBIDDEN_PROMOTIONS:
        issues.append("unsupported_promotion")
    if int(contract.get("resource_budget", 0)) <= 0 or int(contract.get("resource_budget", 0)) > 100_000:
        issues.append("resource_budget")
    if contract.get("disposition") == "open_gap":
        if contract.get("real_rows", 0) != 0 or contract.get("likelihood_evaluations", 0) != 0:
            issues.append("open_gap_data_or_likelihood")
    if contract.get("disposition") == "exact_gate" and contract.get("authority_decisions", 0) != 0:
        issues.append("exact_gate_authority_decision")
    return {"accepted": not issues, "issues": issues, "bounded": True}


def cli(surface: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    contract = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = validate_contract(contract)
    result["surface"] = surface
    print(json.dumps(result, sort_keys=True))
    return 0 if result["accepted"] else 2
