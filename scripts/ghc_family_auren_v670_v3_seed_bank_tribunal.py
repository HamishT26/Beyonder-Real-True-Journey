"""Synthetic temperature-point and interval tribunal for Auren v670-v3.

The module validates declared software structure only. It does not observe a
temperature, calibrate a logger, assess seed viability, or authorize any hold,
transfer, release, disposal, safety, or professional decision.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

REQUIRED = {
    "contract_id",
    "synthetic",
    "quantity_kind",
    "unit_symbol",
    "synthetic_value",
    "conversion_provenance",
    "uncertainty_state",
    "calibration_state",
    "traceability_claim",
    "release_authority",
    "real_observations",
    "real_seed_records",
    "external_actions",
}


class TemperatureContractError(ValueError):
    """Raised when a bounded temperature contract is absent or promoted."""


def positive_fixture() -> dict[str, Any]:
    return {
        "contract_id": "synthetic-temperature-contract-01",
        "synthetic": True,
        "quantity_kind": "temperature_point",
        "unit_symbol": "degree_Celsius",
        "synthetic_value": -18.0,
        "conversion_provenance": "declared_not_converted",
        "uncertainty_state": "declared_unknown",
        "calibration_state": "vacant_no_accuracy_claim",
        "traceability_claim": False,
        "release_authority": "vacant",
        "real_observations": 0,
        "real_seed_records": 0,
        "external_actions": 0,
    }


def validate_contract(contract: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(contract, dict):
        raise TemperatureContractError("contract must be an object")
    missing = sorted(REQUIRED - contract.keys())
    if missing:
        raise TemperatureContractError(f"missing obligations: {missing}")
    if contract["synthetic"] is not True:
        raise TemperatureContractError("only synthetic fixtures are permitted")
    if contract["quantity_kind"] not in {"temperature_point", "temperature_interval"}:
        raise TemperatureContractError("temperature point and interval must remain distinct")
    if contract["unit_symbol"] not in {"K", "degree_Celsius"}:
        raise TemperatureContractError("only declared kelvin or degree Celsius vocabulary is permitted")
    if not isinstance(contract["synthetic_value"], (int, float)) or isinstance(contract["synthetic_value"], bool):
        raise TemperatureContractError("synthetic value must be numeric")
    if contract["uncertainty_state"] != "declared_unknown":
        raise TemperatureContractError("unknown uncertainty may not be promoted")
    if contract["calibration_state"] != "vacant_no_accuracy_claim" or contract["traceability_claim"] is not False:
        raise TemperatureContractError("calibration or traceability cannot be inferred")
    if contract["release_authority"] != "vacant":
        raise TemperatureContractError("release authority cannot be supplied by software")
    if any(contract[key] != 0 for key in ("real_observations", "real_seed_records", "external_actions")):
        raise TemperatureContractError("real observations, records, and actions must remain zero")
    return {
        "accepted": True,
        "contract_id": contract["contract_id"],
        "quantity_kind": contract["quantity_kind"],
        "unit_symbol": contract["unit_symbol"],
        "professional_claim": False,
        "authority_conferred": False,
        "boundary": "synthetic temperature vocabulary contract only",
    }


def rejecting_fixtures() -> list[dict[str, Any]]:
    fixtures = []
    for mutator in (
        lambda row: row.pop("quantity_kind"),
        lambda row: row.update({"uncertainty_state": "known_exact"}),
        lambda row: row.update({"traceability_claim": True}),
        lambda row: row.update({"real_observations": 1}),
    ):
        row = deepcopy(positive_fixture())
        mutator(row)
        fixtures.append(row)
    return fixtures
