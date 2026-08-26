"""Synthetic bicycle-share service-state vacancy contracts."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


class EnvironmentContractError(ValueError):
    """Raised when a synthetic vacancy fixture asserts real evidence or authority."""


LENSES = {"maintenance_ticket", "station_notice", "community_cooperative"}


def positive_fixture(lens: str) -> dict[str, Any]:
    if lens not in LENSES:
        raise EnvironmentContractError(f"unknown lens: {lens}")
    return {
        "lens": lens, "synthetic": True, "real_people": 0, "real_assets": 0,
        "real_feed_rows": 0, "real_measurement": False, "authority_conferred": False,
        "external_actions": 0, "service_state": "structural_fixture_only",
    }


def validate_contract(row: dict[str, Any]) -> dict[str, Any]:
    if row.get("lens") not in LENSES or row.get("synthetic") is not True:
        raise EnvironmentContractError("declared synthetic lens required")
    if any(row.get(field) != 0 for field in ("real_people", "real_assets", "real_feed_rows", "external_actions")):
        raise EnvironmentContractError("real or external activity rejected")
    if row.get("real_measurement") is not False or row.get("authority_conferred") is not False:
        raise EnvironmentContractError("measurement or authority promotion rejected")
    return {**row, "accepted": True}


def rejecting_fixtures() -> list[dict[str, Any]]:
    base = positive_fixture("maintenance_ticket")
    rows: list[dict[str, Any]] = []
    for field, value in (("synthetic", False), ("real_people", 1), ("authority_conferred", True), ("external_actions", 1)):
        row = deepcopy(base); row[field] = value; rows.append(row)
    return rows
