"""Bounded synthetic sourdough contracts for Vesper Arlen v669-v8.

No function in this module accepts real food, people, measurements, external
actions, professional decisions, or protected authority claims.  The records
are deterministic software fixtures only.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
REQUIRED_FIELDS = {"proposal_id", "state", "domain", "unit_policy", "external_actions", "protected_claim"}


@dataclass(frozen=True)
class Decision:
    accepted: bool
    reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {"accepted": self.accepted, "reasons": list(self.reasons)}


def canonical_bytes(payload: Any) -> bytes:
    """Return deterministic UTF-8 JSON bytes; this is not RFC 8785 certification."""
    return json.dumps(payload, ensure_ascii=False, allow_nan=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def digest_payload(payload: Any) -> str:
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def validate_fixture(record: dict[str, Any]) -> Decision:
    reasons: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(record))
    if missing:
        reasons.append("missing_required_state:" + ",".join(missing))
    if record.get("state") in {None, "", "unknown_without_vacancy"}:
        reasons.append("missing_or_unbounded_state")
    if record.get("domain") in {None, "", "ambiguous", "unbounded"}:
        reasons.append("ambiguous_domain")
    if record.get("unit_policy") in {None, "", "ambiguous", "implicit"}:
        reasons.append("ambiguous_unit_policy")
    if record.get("external_actions") != 0:
        reasons.append("external_action_forbidden")
    if record.get("protected_claim") is not False:
        reasons.append("protected_claim_forbidden")
    if record.get("real_people", 0) != 0 or record.get("real_food_items", 0) != 0:
        reasons.append("real_world_entity_forbidden")
    return Decision(accepted=not reasons, reasons=tuple(reasons))


def positive_fixture(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "domain": "owner_local_synthetic_documentation",
        "external_actions": 0,
        "fixture": "synthetic",
        "protected_claim": False,
        "proposal_id": proposal["proposal_id"],
        "real_food_items": 0,
        "real_people": 0,
        "state": "declared_bounded_state",
        "unit_policy": "explicit_or_not_applicable",
    }


def mutate_fixture(base: dict[str, Any], kind: str) -> dict[str, Any]:
    value = dict(base)
    if kind == "missing_required_state":
        value.pop("state", None)
    elif kind == "ambiguous_domain_or_unit":
        value["domain"] = "ambiguous"
        value["unit_policy"] = "ambiguous"
    elif kind == "real_world_or_external_action":
        value["external_actions"] = 1
        value["real_food_items"] = 1
    elif kind == "protected_claim_promotion":
        value["protected_claim"] = True
    else:
        raise ValueError(f"unknown mutation kind: {kind}")
    return value


def bakers_percentage(component_mass: str, flour_mass: str) -> str:
    """Compute a fixed-fixture percentage with explicit zero/number refusal."""
    try:
        component = Decimal(component_mass)
        flour = Decimal(flour_mass)
    except InvalidOperation as exc:
        raise ValueError("masses must be decimal strings") from exc
    if component < 0 or flour <= 0:
        raise ValueError("component must be nonnegative and flour must be positive")
    return str((component / flour * Decimal(100)).quantize(Decimal("0.001")))


def allowed_state_transition(current: str, event: str) -> str:
    transitions = {
        ("planned", "start_mix"): "mixing",
        ("mixing", "begin_bulk"): "bulk",
        ("bulk", "divide"): "divided",
        ("divided", "begin_proof"): "proofing",
        ("proofing", "hold"): "held",
    }
    try:
        return transitions[(current, event)]
    except KeyError as exc:
        raise ValueError("forbidden synthetic state transition") from exc


def interval_contains(start: Decimal, end: Decimal, value: Decimal, *, closed: bool = True) -> bool:
    if start > end:
        raise ValueError("interval start exceeds end")
    return start <= value <= end if closed else start < value < end


def flashcard(proposal: dict[str, Any], outcome: str) -> dict[str, Any]:
    if outcome not in ALLOWED_OUTCOMES:
        raise ValueError("unknown outcome label")
    index = int(str(proposal["proposal_id"]).split("N")[-1])
    pillar = "THOS Body" if index <= 32 else "GMUT Mind" if index <= 36 else "Freed ID and CBR Heart"
    return {
        "card_id": f"VA6698-CARD-{index:03d}",
        "identity_boundary": "relational working label only; not personhood or identity-continuity evidence",
        "tier_1_freed_id": "Vesper Arlen owner-local relational card namespace",
        "tier_2_pillar": pillar,
        "tier_3_practices": ["baker process handover", "food-microbiology provenance", "HACCP-style review vocabulary"],
        "tier_4_task": proposal["title"],
        "outcome": outcome,
        "paragraphs": [
            "Scope: wholly synthetic owner-local fixture with no real person, food, sample, measurement, or external action.",
            "Evidence: deterministic contract state plus explicit positive or held-gap receipt.",
            "Falsifier: missing state, ambiguous domain or unit, external action, or protected-claim promotion.",
            "Rollback: retain the failed witness and stop the smallest owner-local dependency.",
            "Authority: professional, legal, cultural, affected-party, Maori-authority, and Stage 20 boundaries remain reserved.",
            "GMUT: analogy is not force, prediction, likelihood, confirmation, final physics, or Theory of Everything evidence.",
            "THOS: process representation is not operational effectiveness, AGI, ASI, or deployment evidence.",
            "Freed ID: the envelope is synthetic, keyless, proofless, and nonproduction.",
            "CBR: rights vocabulary makes no real remedy, adjudication, compliance, or authority decision.",
            "Handoff: preserve the outcome label, unresolved items, correction lineage, and no-overclaim boundary.",
        ],
    }


def runner_entry(kind: str) -> dict[str, Any]:
    fixture = {
        "domain": "owner_local_synthetic_documentation",
        "external_actions": 0,
        "protected_claim": False,
        "proposal_id": f"runner-{kind}",
        "real_food_items": 0,
        "real_people": 0,
        "state": "declared_bounded_state",
        "unit_policy": "explicit_or_not_applicable",
    }
    decision = validate_fixture(fixture)
    return {"kind": kind, "passed": decision.accepted, "external_actions": 0, "decision": decision.as_dict()}
