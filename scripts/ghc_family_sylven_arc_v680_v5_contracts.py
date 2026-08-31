from __future__ import annotations

import copy
import hashlib
import json
from typing import Any


LIFECYCLE = ["planned", "held", "recorded"]
MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "safety_status_promotion",
    "authority_promotion",
]


def proposal_digest(proposal: dict[str, Any]) -> str:
    raw = json.dumps(proposal, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def positive_fixture(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "authority_conferred": False,
        "lifecycle": list(LIFECYCLE),
        "production": False,
        "proposal_digest": proposal_digest(proposal),
        "proposal_id": proposal["proposal_id"],
        "real_rows": 0,
        "real_world_action": False,
        "safety_status": "unknown_not_measured",
        "synthetic": True,
        "synthetic_namespace": "synthetic.example.invalid",
    }


def mutate(fixture: dict[str, Any], mutation_type: str) -> dict[str, Any]:
    result = copy.deepcopy(fixture)
    if mutation_type == "missing_required_field":
        result.pop("proposal_id", None)
    elif mutation_type == "lifecycle_inversion":
        result["lifecycle"] = list(reversed(LIFECYCLE))
    elif mutation_type == "stale_provenance_digest":
        result["proposal_digest"] = "0" * 64
    elif mutation_type == "safety_status_promotion":
        result["safety_status"] = "approved_safe_for_work"
    elif mutation_type == "authority_promotion":
        result["authority_conferred"] = True
    else:
        raise ValueError(mutation_type)
    return result


def validate(proposal: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    if fixture.get("proposal_id") != proposal["proposal_id"]:
        reasons.append("missing_or_wrong_proposal_id")
    if fixture.get("lifecycle") != LIFECYCLE:
        reasons.append("lifecycle_inversion")
    if fixture.get("proposal_digest") != proposal_digest(proposal):
        reasons.append("stale_provenance_digest")
    if fixture.get("safety_status") != "unknown_not_measured":
        reasons.append("safety_status_promotion")
    if fixture.get("authority_conferred") is not False:
        reasons.append("authority_promotion")
    if fixture.get("synthetic") is not True or fixture.get("synthetic_namespace") != "synthetic.example.invalid":
        reasons.append("non_synthetic_fixture")
    if fixture.get("real_rows") != 0 or fixture.get("real_world_action") is not False:
        reasons.append("real_world_scope_violation")
    if fixture.get("production") is not False:
        reasons.append("production_promotion")
    return {
        "accepted": not reasons,
        "authority_conferred": False,
        "proposal_id": proposal["proposal_id"],
        "real_world_action": False,
        "reasons": reasons,
        "structural_only": True,
    }
