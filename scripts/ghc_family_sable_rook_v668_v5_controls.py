#!/usr/bin/env python3
"""Bounded synthetic score-edition controls for Sable Rook v668-v5 x2."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


class RejectedFixture(ValueError):
    """An expected fail-closed fixture rejection."""


CONTROL_NAMES = (
    "score_identity",
    "measure_address",
    "edition_lineage",
    "part_projection",
    "transposition_roundtrip",
    "duration_tuplet",
    "repeat_traversal",
    "tempo_unit",
    "correction_ledger",
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
    require_keys(payload, "schema_version", "owner", "phase", "proposal_id", "expected_disposition", "protected_claims", "authority_override")
    require(payload["schema_version"] == 1, "unsupported envelope schema")
    require(payload["owner"] == "Sable Rook", "wrong owner")
    require(payload["phase"] == "v668-v5", "wrong phase")
    require(isinstance(payload["proposal_id"], str) and payload["proposal_id"].startswith("SR6685-N"), "invalid proposal id")
    require(payload["expected_disposition"] in {"completed", "represented", "open_gap", "exact_gate"}, "invalid outcome vocabulary")
    require(isinstance(payload["protected_claims"], dict), "protected claims must be an object")
    require(payload["protected_claims"] and all(value is False for value in payload["protected_claims"].values()), "protected claim promotion refused")
    require(payload["authority_override"] is False, "authority override refused")
    return {"accepted": True, "proposal_id": payload["proposal_id"], "envelope_sha256": stable_digest(payload)}


def score_identity(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "work_alias", "edition_alias", "instance_alias", "part_aliases", "synthetic", "real_resource_claim")
    aliases = [payload[key] for key in ("work_alias", "edition_alias", "instance_alias")]
    require(all(isinstance(value, str) and value for value in aliases), "identity aliases must be nonempty")
    require(len(set(aliases)) == len(aliases), "work edition and instance identities must remain distinct")
    parts = payload["part_aliases"]
    require(isinstance(parts, list) and parts, "at least one part alias is required")
    require(all(isinstance(value, str) and value for value in parts), "part aliases must be nonempty")
    require(len(parts) == len(set(parts)), "part aliases must be unique")
    require(set(parts).isdisjoint(aliases), "part aliases may not conflate work edition or instance")
    require(payload["synthetic"] is True and payload["real_resource_claim"] is False, "real resource claim refused")
    return {"accepted": True, "identity_sha256": stable_digest(payload), "part_count": len(parts)}


def measure_address(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "movement_alias", "measure_number", "beat_numerator", "beat_denominator", "pickup", "repeat_pass")
    require(isinstance(payload["movement_alias"], str) and payload["movement_alias"], "movement alias required")
    require(type(payload["measure_number"]) is int and payload["measure_number"] >= 0, "measure number must be nonnegative")
    require(type(payload["beat_numerator"]) is int and payload["beat_numerator"] >= 0, "beat numerator must be nonnegative")
    require(type(payload["beat_denominator"]) is int and payload["beat_denominator"] > 0, "beat denominator must be positive")
    require(type(payload["pickup"]) is bool, "pickup must be Boolean")
    require(type(payload["repeat_pass"]) is int and payload["repeat_pass"] >= 1, "repeat pass must be positive")
    beat = Fraction(payload["beat_numerator"], payload["beat_denominator"])
    address = [payload["movement_alias"], payload["measure_number"], str(beat), payload["repeat_pass"]]
    return {"accepted": True, "canonical_address": address, "pickup": payload["pickup"]}


def edition_lineage(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "witnesses", "edition_alias", "derivations", "authenticity_claim", "editorial_authority")
    witnesses = payload["witnesses"]
    require(isinstance(witnesses, list) and len(witnesses) >= 2, "at least two source witnesses required")
    aliases = [row.get("alias") for row in witnesses if isinstance(row, dict)]
    digests = [row.get("digest") for row in witnesses if isinstance(row, dict)]
    require(len(aliases) == len(witnesses) and all(isinstance(value, str) and value for value in aliases), "witness aliases required")
    require(len(set(aliases)) == len(aliases), "witness aliases must be unique")
    require(all(isinstance(value, str) and len(value) == 64 for value in digests), "witness digests must be 64 characters")
    require(isinstance(payload["edition_alias"], str) and payload["edition_alias"], "edition alias required")
    require(isinstance(payload["derivations"], list) and set(payload["derivations"]) == set(aliases), "every witness must remain in derivation lineage")
    require(payload["authenticity_claim"] is False, "authenticity claim refused")
    require(payload["editorial_authority"] == "vacant", "editorial authority promotion refused")
    return {"accepted": True, "lineage_sha256": stable_digest(payload), "witness_count": len(witnesses)}


def part_projection(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "score_events", "requested_part", "projected_event_ids", "tacet_policy")
    events = payload["score_events"]
    require(isinstance(events, list) and events, "score events required")
    require(all(isinstance(row, dict) and isinstance(row.get("event_id"), str) and isinstance(row.get("part_alias"), str) for row in events), "event identities and part aliases required")
    event_ids = [row["event_id"] for row in events]
    require(len(event_ids) == len(set(event_ids)), "event identities must be unique")
    require(isinstance(payload["requested_part"], str) and payload["requested_part"], "requested part required")
    expected = [row["event_id"] for row in events if row["part_alias"] == payload["requested_part"]]
    require(payload["projected_event_ids"] == expected, "part projection omits or imports score events")
    require(payload["tacet_policy"] in {"explicit", "not_applicable"}, "tacet policy must be explicit")
    return {"accepted": True, "projected_count": len(expected), "projection_sha256": stable_digest(expected)}


def transposition_roundtrip(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "source_pitches", "semitones", "transposed_pitches", "source_domain", "target_domain")
    source, target, shift = payload["source_pitches"], payload["transposed_pitches"], payload["semitones"]
    require(isinstance(source, list) and source, "source pitches required")
    require(all(type(value) is int and 0 <= value <= 127 for value in source), "source pitches must be MIDI-domain integers")
    require(type(shift) is int and -24 <= shift <= 24, "transposition shift outside bounded domain")
    require(isinstance(target, list) and target == [value + shift for value in source], "forward transposition mismatch")
    require(all(0 <= value <= 127 for value in target), "transposed pitch outside bounded domain")
    require([value - shift for value in target] == source, "round-trip mismatch")
    require(payload["source_domain"] != payload["target_domain"], "written and sounding domains must remain distinct")
    return {"accepted": True, "pitch_count": len(source), "roundtrip": True}


def duration_tuplet(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "events", "measure_total", "tuplet_ratio", "float_duration_used")
    events = payload["events"]
    require(isinstance(events, list) and events, "duration events required")
    fractions: list[Fraction] = []
    for row in events:
        require(isinstance(row, dict) and type(row.get("numerator")) is int and type(row.get("denominator")) is int, "exact event fraction required")
        require(row["numerator"] >= 0 and row["denominator"] > 0, "invalid event fraction")
        fractions.append(Fraction(row["numerator"], row["denominator"]))
    total = payload["measure_total"]
    require(isinstance(total, dict) and type(total.get("numerator")) is int and type(total.get("denominator")) is int and total["denominator"] > 0, "exact measure total required")
    expected = Fraction(total["numerator"], total["denominator"])
    ratio = payload["tuplet_ratio"]
    require(isinstance(ratio, list) and len(ratio) == 2 and all(type(value) is int and value > 0 for value in ratio), "positive tuplet ratio required")
    require(payload["float_duration_used"] is False, "floating duration conversion refused")
    require(sum(fractions, Fraction()) == expected, "duration closure mismatch")
    return {"accepted": True, "event_count": len(events), "total": str(expected), "exact_arithmetic": True}


def repeat_traversal(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "edges", "traversal", "start", "end", "max_visits_per_section")
    edges, traversal = payload["edges"], payload["traversal"]
    require(isinstance(edges, list) and edges, "repeat edges required")
    edge_set = {tuple(edge) for edge in edges if isinstance(edge, list) and len(edge) == 2 and all(isinstance(value, str) and value for value in edge)}
    require(len(edge_set) == len(edges), "invalid or duplicate repeat edge")
    require(isinstance(traversal, list) and len(traversal) >= 2, "traversal required")
    require(traversal[0] == payload["start"] and traversal[-1] == payload["end"], "start or termination mismatch")
    require(all((left, right) in edge_set for left, right in zip(traversal, traversal[1:])), "undeclared repeat transition")
    require(type(payload["max_visits_per_section"]) is int and payload["max_visits_per_section"] > 0, "positive visit budget required")
    require(max(Counter(traversal).values()) <= payload["max_visits_per_section"], "repeat traversal exceeds visit budget")
    return {"accepted": True, "transition_count": len(traversal) - 1, "terminated": True}


def tempo_unit(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "markings", "metric_modulations", "uncertainty_bpm", "tempo_authority")
    markings = payload["markings"]
    require(isinstance(markings, list) and markings, "tempo markings required")
    allowed_units = {"whole", "half", "quarter", "eighth", "sixteenth"}
    for row in markings:
        require(isinstance(row, dict) and row.get("unit") in allowed_units, "unknown tempo unit")
        require(type(row.get("bpm")) in {int, float} and row["bpm"] > 0, "tempo must be positive")
    require(isinstance(payload["metric_modulations"], list), "metric modulations must be a list")
    require(all(isinstance(row, list) and len(row) == 2 and all(type(value) is int and value > 0 for value in row) for row in payload["metric_modulations"]), "positive exact modulation ratios required")
    require(type(payload["uncertainty_bpm"]) in {int, float} and payload["uncertainty_bpm"] >= 0, "tempo uncertainty must be nonnegative")
    require(payload["tempo_authority"] == "vacant", "tempo authority promotion refused")
    return {"accepted": True, "marking_count": len(markings), "tempo_decision": None}


def correction_ledger(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "events", "readback_state")
    events = payload["events"]
    require(isinstance(events, list) and len(events) >= 2, "at least baseline and correction events required")
    ids = [event.get("event_id") for event in events if isinstance(event, dict)]
    require(len(ids) == len(events) and all(isinstance(value, str) and value for value in ids), "event ids required")
    require(len(ids) == len(set(ids)), "event ids must be unique")
    require(events[0].get("kind") == "baseline", "first event must retain baseline")
    corrections = [event for event in events[1:] if event.get("kind") == "correction"]
    require(any(event.get("supersedes") == events[0]["event_id"] and event.get("component_address") for event in corrections), "component-addressed correction required")
    require(payload["readback_state"] in {"synthetic_acknowledged", "synthetic_pending"}, "invalid readback state")
    return {"accepted": True, "event_count": len(events), "baseline_retained": True, "ledger_sha256": stable_digest(events)}


def authority_firewall(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "decisions", "reserved_authorities", "software_decision_count")
    require(isinstance(payload["decisions"], dict) and payload["decisions"], "decision vacancy map required")
    require(all(value == "vacant" for value in payload["decisions"].values()), "authority decision promotion refused")
    require(isinstance(payload["reserved_authorities"], list) and {"professional", "legal", "cultural", "Maori", "affected_party"} <= set(payload["reserved_authorities"]), "required authority reservations missing")
    require(payload["software_decision_count"] == 0, "software may not make reserved decisions")
    return {"accepted": True, "vacancy_count": len(payload["decisions"]), "authority_conferred": False}


CONTROLS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "score_identity": score_identity,
    "measure_address": measure_address,
    "edition_lineage": edition_lineage,
    "part_projection": part_projection,
    "transposition_roundtrip": transposition_roundtrip,
    "duration_tuplet": duration_tuplet,
    "repeat_traversal": repeat_traversal,
    "tempo_unit": tempo_unit,
    "correction_ledger": correction_ledger,
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
        print(json.dumps({"accepted": False, "control": control_name, "error_class": type(exc).__name__, "boundary": "synthetic rejection only"}, sort_keys=True))
        return 2
    print(json.dumps({"accepted": True, "control": control_name, "result": result, "boundary": "synthetic acceptance only"}, sort_keys=True))
    return 0
