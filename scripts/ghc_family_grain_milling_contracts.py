"""Synthetic grain-milling contracts for the Lyren Moss v670-v1 evidence lane."""

from __future__ import annotations

import json
import math
from collections.abc import Mapping, Sequence
from decimal import Decimal
from typing import Any

ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}


class ContractError(ValueError):
    """A fail-closed synthetic contract rejection."""


def _finite_tree(value: Any) -> None:
    if isinstance(value, bool) or value is None or isinstance(value, str | int):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ContractError("nonfinite_number")
        return
    if isinstance(value, Mapping):
        if not all(isinstance(key, str) for key in value):
            raise ContractError("nonstring_key")
        for child in value.values():
            _finite_tree(child)
        return
    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        for child in value:
            _finite_tree(child)
        return
    raise ContractError("unsupported_json_value")


def canonical_json_bytes(payload: Mapping[str, Any]) -> bytes:
    """Return deterministic fixture bytes without claiming canonical truth outside this schema."""
    _finite_tree(payload)
    return (
        json.dumps(
            payload,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def validate_proposal_record(record: Mapping[str, Any]) -> dict[str, Any]:
    required = {
        "proposal_id",
        "title",
        "planned_outcome",
        "real_people",
        "real_grain_or_food",
        "devices_or_samples",
        "external_actions",
    }
    missing = sorted(required - set(record))
    if missing:
        raise ContractError("missing_fields:" + ",".join(missing))
    if record["planned_outcome"] not in ALLOWED_OUTCOMES:
        raise ContractError("unknown_outcome")
    if any(
        int(record[field]) != 0
        for field in (
            "real_people",
            "real_grain_or_food",
            "devices_or_samples",
            "external_actions",
        )
    ):
        raise ContractError("non_synthetic_or_external_surface")
    if record.get("authority_claim", False):
        raise ContractError("authority_claim_prohibited")
    if not str(record["proposal_id"]).startswith("LM6701-"):
        raise ContractError("owner_namespace_mismatch")
    return {
        "accepted": True,
        "proposal_id": record["proposal_id"],
        "outcome": record["planned_outcome"],
        "real_world_actions": 0,
    }


def net_mass_kg(gross_kg: float, tare_kg: float) -> Decimal:
    gross = Decimal(str(gross_kg))
    tare = Decimal(str(tare_kg))
    if not gross.is_finite() or not tare.is_finite():
        raise ContractError("nonfinite_mass")
    if gross < 0 or tare < 0:
        raise ContractError("negative_mass")
    if tare > gross:
        raise ContractError("tare_exceeds_gross")
    return gross - tare


def mass_balance(
    input_kg: float,
    outputs_kg: Mapping[str, float],
    *,
    tolerance_kg: float = 0.001,
) -> dict[str, Any]:
    input_mass = Decimal(str(input_kg))
    tolerance = Decimal(str(tolerance_kg))
    if not input_mass.is_finite() or input_mass < 0:
        raise ContractError("invalid_input_mass")
    if not tolerance.is_finite() or tolerance < 0:
        raise ContractError("invalid_tolerance")
    if not outputs_kg:
        raise ContractError("missing_outputs")
    outputs: dict[str, Decimal] = {}
    for label, value in outputs_kg.items():
        amount = Decimal(str(value))
        if not label or not amount.is_finite() or amount < 0:
            raise ContractError("invalid_output")
        outputs[label] = amount
    output_total = sum(outputs.values(), Decimal(0))
    variance = input_mass - output_total
    return {
        "input_kg": str(input_mass),
        "output_kg": str(output_total),
        "variance_kg": str(variance),
        "within_fixture_tolerance": abs(variance) <= tolerance,
        "release_authorized": False,
        "boundary": "fixed synthetic arithmetic only; not a measurement or process release",
    }


def fixed_fixture() -> dict[str, Any]:
    return {
        "proposal_id": "LM6701-N006",
        "title": "synthetic fixed mass-balance control",
        "planned_outcome": "completed",
        "real_people": 0,
        "real_grain_or_food": 0,
        "devices_or_samples": 0,
        "external_actions": 0,
    }
