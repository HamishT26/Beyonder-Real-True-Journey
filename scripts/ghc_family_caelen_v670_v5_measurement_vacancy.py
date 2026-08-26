"""Synthetic astronomical measurement-vacancy contract; never observational evidence."""

from __future__ import annotations

import math
from copy import deepcopy
from datetime import datetime
from typing import Any


class EnvironmentContractError(ValueError):
    """Raised when a synthetic metadata fixture crosses an evidence boundary."""


def positive_fixture(lens: str = "photographic_plate") -> dict[str, Any]:
    return {
        "fixture_class": "synthetic_only",
        "lens": lens,
        "plate_alias": f"synthetic-{lens}-plate",
        "exposure_start": "2030-01-01T00:00:00Z",
        "exposure_end": "2030-01-01T00:05:00Z",
        "time_scale": "synthetic_unspecified",
        "coordinate_frame": None,
        "coordinate_values": None,
        "scan_ppi": 1200.0,
        "pixel_scale": None,
        "bit_depth": 16,
        "fits_header_state": "synthetic_unpopulated",
        "calibration_authority": None,
        "quality_acceptance_authority": None,
        "real_measurement": False,
        "real_observation": False,
        "empirical_likelihood": False,
        "external_actions": 0,
    }


def rejecting_fixtures(lens: str = "photographic_plate") -> list[dict[str, Any]]:
    base = positive_fixture(lens)
    missing = deepcopy(base)
    missing.pop("time_scale")
    reversed_time = deepcopy(base)
    reversed_time["exposure_end"] = "2029-12-31T23:59:00Z"
    real = deepcopy(base)
    real["real_measurement"] = True
    authority = deepcopy(base)
    authority["quality_acceptance_authority"] = "repository software"
    return [missing, reversed_time, real, authority]


def validate_contract(row: dict[str, Any]) -> dict[str, Any]:
    required = {
        "fixture_class", "lens", "plate_alias", "exposure_start", "exposure_end",
        "time_scale", "coordinate_frame", "coordinate_values", "scan_ppi",
        "pixel_scale", "bit_depth", "fits_header_state", "calibration_authority",
        "quality_acceptance_authority", "real_measurement", "real_observation",
        "empirical_likelihood", "external_actions",
    }
    missing = sorted(required - set(row))
    if missing:
        raise EnvironmentContractError(f"missing fields: {missing}")
    start = datetime.fromisoformat(row["exposure_start"].replace("Z", "+00:00"))
    end = datetime.fromisoformat(row["exposure_end"].replace("Z", "+00:00"))
    if end <= start:
        raise EnvironmentContractError("exposure chronology drifted")
    if not isinstance(row["scan_ppi"], (int, float)) or not math.isfinite(row["scan_ppi"]) or row["scan_ppi"] <= 0:
        raise EnvironmentContractError("scan sampling is not a bounded synthetic scalar")
    if row["bit_depth"] not in {8, 16, 32}:
        raise EnvironmentContractError("unsupported synthetic bit depth")
    if row["coordinate_frame"] is not None or row["coordinate_values"] is not None or row["pixel_scale"] is not None:
        raise EnvironmentContractError("data-bearing coordinate or pixel-scale claim")
    if row["fixture_class"] != "synthetic_only" or row["real_measurement"] is not False or row["real_observation"] is not False or row["empirical_likelihood"] is not False or row["external_actions"] != 0:
        raise EnvironmentContractError("synthetic or empirical boundary crossed")
    if row["calibration_authority"] is not None or row["quality_acceptance_authority"] is not None:
        raise EnvironmentContractError("vacant calibration or quality authority was filled")
    return {
        "accepted": True, "lens": row["lens"], "typed_exposure_interval": True,
        "coordinate_vacancy": True, "pixel_scale_vacancy": True,
        "real_measurement": False, "real_observation": False,
        "empirical_likelihood": False, "authority_conferred": False,
        "external_actions": 0,
    }
