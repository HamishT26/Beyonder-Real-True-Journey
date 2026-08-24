#!/usr/bin/env python3
"""Bounded synthetic weather-observation controls for Caelen Ash v668-v6 x2."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


class RejectedFixture(ValueError):
    """An expected fail-closed fixture rejection."""


CONTROL_NAMES = (
    "station_identity",
    "sensor_inventory",
    "observation_clock",
    "unit_dimension",
    "site_exposure",
    "calibration_vacancy",
    "quality_flag",
    "aggregation_window",
    "correction_nonerasure",
    "authority_firewall",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RejectedFixture(message)


def require_keys(payload: dict[str, Any], *keys: str) -> None:
    missing = [key for key in keys if key not in payload]
    require(not missing, f"missing required fields: {missing}")


def stable_digest(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def evaluate_envelope(payload: dict[str, Any]) -> dict[str, Any]:
    require(isinstance(payload, dict), "envelope must be an object")
    require_keys(
        payload,
        "schema_version",
        "owner",
        "phase",
        "proposal_id",
        "expected_disposition",
        "protected_claims",
        "authority_override",
    )
    require(payload["schema_version"] == 1, "unsupported envelope schema")
    require(payload["owner"] == "Caelen Ash", "wrong owner")
    require(payload["phase"] == "v668-v6", "wrong phase")
    require(
        isinstance(payload["proposal_id"], str) and payload["proposal_id"].startswith("CA6686-N"),
        "invalid proposal id",
    )
    require(
        payload["expected_disposition"] in {"completed", "represented", "open_gap", "exact_gate"},
        "invalid outcome vocabulary",
    )
    require(isinstance(payload["protected_claims"], dict), "protected claims must be an object")
    require(
        payload["protected_claims"] and all(value is False for value in payload["protected_claims"].values()),
        "protected claim promotion refused",
    )
    require(payload["authority_override"] is False, "authority override refused")
    return {
        "accepted": True,
        "proposal_id": payload["proposal_id"],
        "envelope_sha256": stable_digest(payload),
    }


def station_identity(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(
        payload,
        "station_alias",
        "platform_alias",
        "instrument_aliases",
        "synthetic",
        "wigos_registration_claim",
    )
    station = payload["station_alias"]
    platform = payload["platform_alias"]
    instruments = payload["instrument_aliases"]
    require(isinstance(station, str) and station, "station alias required")
    require(isinstance(platform, str) and platform, "platform alias required")
    require(station != platform, "station and platform identities must remain distinct")
    require(isinstance(instruments, list) and instruments, "instrument aliases required")
    require(all(isinstance(value, str) and value for value in instruments), "instrument aliases must be nonempty")
    require(len(instruments) == len(set(instruments)), "instrument aliases must be unique")
    require({station, platform}.isdisjoint(instruments), "station platform and instrument identities may not conflate")
    require(payload["synthetic"] is True, "only synthetic identity fixtures are allowed")
    require(payload["wigos_registration_claim"] is False, "WIGOS registration claim refused")
    return {"accepted": True, "instrument_count": len(instruments), "identity_sha256": stable_digest(payload)}


def sensor_inventory(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "channels", "declared_channel_aliases", "undeclared_channel_count", "fitness_claim")
    channels = payload["channels"]
    require(isinstance(channels, list) and channels, "sensor channels required")
    require(
        all(
            isinstance(row, dict)
            and isinstance(row.get("alias"), str)
            and bool(row["alias"])
            and isinstance(row.get("variable"), str)
            and bool(row["variable"])
            and isinstance(row.get("unit"), str)
            and bool(row["unit"])
            for row in channels
        ),
        "channel alias variable and unit required",
    )
    aliases = [row["alias"] for row in channels]
    require(len(aliases) == len(set(aliases)), "channel aliases must be unique")
    require(payload["declared_channel_aliases"] == aliases, "declared channel order or membership mismatch")
    require(payload["undeclared_channel_count"] == 0, "undeclared channels refused")
    require(payload["fitness_claim"] is False, "instrument fitness claim refused")
    return {"accepted": True, "channel_count": len(channels), "inventory_sha256": stable_digest(channels)}


def observation_clock(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "receipt_seconds", "cadence_seconds", "timezone", "gap_policy", "leap_second_assessed")
    instants = payload["receipt_seconds"]
    cadence = payload["cadence_seconds"]
    require(isinstance(instants, list) and len(instants) >= 2, "at least two receipt instants required")
    require(all(type(value) is int and value >= 0 for value in instants), "receipt instants must be nonnegative integers")
    require(all(left < right for left, right in zip(instants, instants[1:])), "receipt instants must be strictly increasing")
    require(type(cadence) is int and cadence > 0, "positive cadence required")
    require(all((right - left) % cadence == 0 for left, right in zip(instants, instants[1:])), "cadence grid mismatch")
    require(payload["timezone"] == "UTC", "non-UTC synthetic clock refused")
    require(payload["gap_policy"] in {"preserve", "quarantine"}, "gap policy must preserve or quarantine")
    require(payload["leap_second_assessed"] is False, "leap-second assessment authority is absent")
    return {"accepted": True, "instant_count": len(instants), "cadence_seconds": cadence}


def unit_dimension(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "records", "conversion_applied", "measurement_validity_claim")
    records = payload["records"]
    allowed = {
        "air_temperature": "K",
        "station_pressure": "Pa",
        "relative_humidity": "1",
        "wind_speed": "m s-1",
        "precipitation_amount": "kg m-2",
    }
    require(isinstance(records, list) and records, "variable-unit records required")
    require(
        all(isinstance(row, dict) and row.get("variable") in allowed and row.get("unit") == allowed[row["variable"]] for row in records),
        "variable and declared unit dimension mismatch",
    )
    variables = [row["variable"] for row in records]
    require(len(variables) == len(set(variables)), "duplicate variable record")
    require(payload["conversion_applied"] is False, "unreviewed unit conversion refused")
    require(payload["measurement_validity_claim"] is False, "measurement-validity claim refused")
    return {"accepted": True, "record_count": len(records), "unit_sha256": stable_digest(records)}


def site_exposure(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "site_alias", "height_m", "reference_surface", "obstructions", "relocation_state", "fitness_claim")
    require(isinstance(payload["site_alias"], str) and payload["site_alias"], "site alias required")
    require(type(payload["height_m"]) in {int, float} and payload["height_m"] > 0, "positive sensor height required")
    require(payload["reference_surface"] in {"synthetic_ground", "synthetic_platform"}, "declared reference surface required")
    require(isinstance(payload["obstructions"], list), "obstructions must be a list")
    require(all(isinstance(value, str) and value for value in payload["obstructions"]), "obstruction aliases must be nonempty")
    require(payload["relocation_state"] in {"stable", "pending_review"}, "invalid relocation state")
    require(payload["fitness_claim"] is False, "site or exposure fitness claim refused")
    return {"accepted": True, "obstruction_count": len(payload["obstructions"]), "fitness_decision": None}


def calibration_vacancy(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "certificates", "traceability_claim", "return_to_service_authority")
    certificates = payload["certificates"]
    require(isinstance(certificates, list) and certificates, "calibration-vacancy records required")
    for row in certificates:
        require(
            isinstance(row, dict)
            and isinstance(row.get("instrument_alias"), str)
            and bool(row["instrument_alias"])
            and isinstance(row.get("certificate_alias"), str)
            and bool(row["certificate_alias"]),
            "instrument and certificate aliases required",
        )
        require(isinstance(row.get("valid_from"), str) and isinstance(row.get("valid_until"), str), "validity bounds required")
        require(row["valid_from"] < row["valid_until"], "calibration validity interval must be ordered")
        require(row.get("uncertainty_declared") is True, "uncertainty declaration vacancy must be explicit")
    require(payload["traceability_claim"] is False, "metrological traceability claim refused")
    require(payload["return_to_service_authority"] == "vacant", "return-to-service authority promotion refused")
    return {"accepted": True, "certificate_count": len(certificates), "traceability_established": False}


def quality_flag(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "raw_value", "quality_flag", "adjusted_value", "adjustment_lineage", "release_decision")
    require(type(payload["raw_value"]) in {int, float}, "numeric raw value required")
    require(payload["quality_flag"] in {"unchanged", "suspect", "rejected", "missing"}, "unknown quality flag")
    require(payload["adjusted_value"] is None, "undeclared adjustment refused")
    require(isinstance(payload["adjustment_lineage"], list) and not payload["adjustment_lineage"], "adjustment lineage must remain empty when no adjustment exists")
    require(payload["release_decision"] == "vacant", "observation release decision promotion refused")
    return {"accepted": True, "flag": payload["quality_flag"], "raw_retained": True}


def aggregation_window(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "expected_slots", "observed_slots", "missing_reasons", "closure_state", "denominator")
    expected = payload["expected_slots"]
    observed = payload["observed_slots"]
    require(type(expected) is int and expected > 0, "positive expected-slot count required")
    require(isinstance(observed, list), "observed slots must be a list")
    require(all(type(value) is int and 0 <= value < expected for value in observed), "observed slot outside window")
    require(len(observed) == len(set(observed)), "duplicate observed slot")
    missing = [slot for slot in range(expected) if slot not in set(observed)]
    reasons = payload["missing_reasons"]
    require(isinstance(reasons, dict), "missing-reason map required")
    require(set(reasons) == {str(slot) for slot in missing}, "every and only missing slot needs a reason")
    require(all(value in {"not_observed", "sensor_fault", "quarantined"} for value in reasons.values()), "unknown missing reason")
    require(payload["closure_state"] == ("complete" if not missing else "incomplete"), "closure state contradicts coverage")
    require(payload["denominator"] == expected, "coverage denominator mismatch")
    return {"accepted": True, "observed_count": len(observed), "missing_count": len(missing), "denominator": expected}


def correction_nonerasure(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "events", "readback_state")
    events = payload["events"]
    require(isinstance(events, list) and len(events) >= 2, "baseline and correction events required")
    ids = [event.get("event_id") for event in events if isinstance(event, dict)]
    require(len(ids) == len(events) and all(isinstance(value, str) and value for value in ids), "event ids required")
    require(len(ids) == len(set(ids)), "event ids must be unique")
    require(events[0].get("kind") == "baseline", "first event must retain the baseline")
    corrections = [event for event in events[1:] if event.get("kind") == "correction"]
    require(
        any(event.get("supersedes") == events[0]["event_id"] and event.get("channel_alias") for event in corrections),
        "channel-addressed correction must supersede the retained baseline",
    )
    require(payload["readback_state"] in {"synthetic_acknowledged", "synthetic_pending"}, "invalid correction readback state")
    return {"accepted": True, "event_count": len(events), "baseline_retained": True, "ledger_sha256": stable_digest(events)}


def authority_firewall(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "decisions", "reserved_authorities", "software_decision_count")
    require(isinstance(payload["decisions"], dict) and payload["decisions"], "decision vacancy map required")
    require(all(value == "vacant" for value in payload["decisions"].values()), "authority decision promotion refused")
    require(
        isinstance(payload["reserved_authorities"], list)
        and {"professional", "legal", "cultural", "Maori", "affected_party"} <= set(payload["reserved_authorities"]),
        "required authority reservations missing",
    )
    require(payload["software_decision_count"] == 0, "software may not make reserved decisions")
    return {"accepted": True, "vacancy_count": len(payload["decisions"]), "authority_conferred": False}


CONTROLS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "station_identity": station_identity,
    "sensor_inventory": sensor_inventory,
    "observation_clock": observation_clock,
    "unit_dimension": unit_dimension,
    "site_exposure": site_exposure,
    "calibration_vacancy": calibration_vacancy,
    "quality_flag": quality_flag,
    "aggregation_window": aggregation_window,
    "correction_nonerasure": correction_nonerasure,
    "authority_firewall": authority_firewall,
}


def evaluate_control(name: str, payload: dict[str, Any]) -> dict[str, Any]:
    require(name in CONTROLS, "unknown control")
    return CONTROLS[name](payload)


def runner_main(control_name: str) -> int:
    parser = argparse.ArgumentParser(description=f"bounded synthetic {control_name} runner")
    parser.add_argument("--fixture", required=True)
    args = parser.parse_args()
    try:
        payload = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
        result = evaluate_control(control_name, payload)
    except (OSError, json.JSONDecodeError, RejectedFixture) as exc:
        print(
            json.dumps(
                {
                    "accepted": False,
                    "control": control_name,
                    "error_class": type(exc).__name__,
                    "boundary": "synthetic rejection only",
                },
                sort_keys=True,
            )
        )
        return 2
    print(
        json.dumps(
            {
                "accepted": True,
                "control": control_name,
                "result": result,
                "boundary": "synthetic acceptance only",
            },
            sort_keys=True,
        )
    )
    return 0
