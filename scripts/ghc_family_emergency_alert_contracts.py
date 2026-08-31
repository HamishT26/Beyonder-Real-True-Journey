#!/usr/bin/env python3
"""Zero-row synthetic emergency-alert contract helpers.

The module validates structural fixtures only.  It never sends, receives,
downloads, signs, verifies, geotargets, publishes, updates, or cancels a real
alert.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from typing import Any


REQUIRED_FIELDS = {
    "proposal_id",
    "message_id",
    "sender_domain",
    "sent_at",
    "expires_at",
    "base_digest",
    "status",
    "message_type",
    "scope",
    "authority_claim",
    "real_world",
}


def expected_digest(proposal_id: str) -> str:
    return hashlib.sha256(f"orin-v680-v1:{proposal_id}".encode("utf-8")).hexdigest()


def positive_fixture(proposal_id: str) -> dict[str, Any]:
    return {
        "proposal_id": proposal_id,
        "message_id": f"synthetic-{proposal_id.lower()}",
        "sender_domain": "synthetic.example.invalid",
        "sent_at": "2026-01-01T00:00:00+00:00",
        "expires_at": "2026-01-01T00:05:00+00:00",
        "base_digest": expected_digest(proposal_id),
        "status": "Test",
        "message_type": "Alert",
        "scope": "Restricted",
        "authority_claim": False,
        "real_world": False,
    }


def validate_fixture(value: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(value))
    if missing:
        reasons.append("missing_required_field:" + ",".join(missing))
    proposal_id = value.get("proposal_id")
    if isinstance(proposal_id, str):
        if value.get("base_digest") != expected_digest(proposal_id):
            reasons.append("stale_precondition_digest")
    if value.get("sender_domain") != "synthetic.example.invalid":
        reasons.append("identity_role_swap")
    try:
        sent = datetime.fromisoformat(value["sent_at"])
        expires = datetime.fromisoformat(value["expires_at"])
        if sent >= expires:
            reasons.append("chronology_inversion")
    except (KeyError, TypeError, ValueError):
        if "missing_required_field:sent_at" not in reasons:
            reasons.append("invalid_chronology")
    if value.get("authority_claim") is not False or value.get("real_world") is not False:
        reasons.append("authority_promotion")
    if value.get("status") != "Test":
        reasons.append("non_test_status")
    if value.get("message_type") != "Alert":
        reasons.append("unsupported_message_type")
    if value.get("scope") != "Restricted":
        reasons.append("unsupported_scope")
    return {
        "accepted": not reasons,
        "reasons": sorted(set(reasons)),
        "structural_only": True,
        "real_world_action": False,
        "authority_conferred": False,
    }


def mutate(fixture: dict[str, Any], mutation_type: str) -> dict[str, Any]:
    changed = dict(fixture)
    if mutation_type == "missing_required_field":
        changed.pop("proposal_id", None)
    elif mutation_type == "identity_role_swap":
        changed["sender_domain"] = "operator.example.invalid"
    elif mutation_type == "stale_precondition_digest":
        changed["base_digest"] = "0" * 64
    elif mutation_type == "chronology_inversion":
        changed["sent_at"], changed["expires_at"] = changed["expires_at"], changed["sent_at"]
    elif mutation_type == "authority_promotion":
        changed["authority_claim"] = True
        changed["real_world"] = True
    else:
        raise ValueError(f"unsupported mutation type: {mutation_type}")
    return changed


def runner_smoke(runner_number: int) -> dict[str, Any]:
    proposal_id = f"OR6801-N{runner_number:03d}"
    positive = validate_fixture(positive_fixture(proposal_id))
    invalid = validate_fixture(mutate(positive_fixture(proposal_id), "authority_promotion"))
    return {
        "runner": f"ghc_family_emergency_alert_runner_{runner_number:02d}",
        "proposal_id": proposal_id,
        "positive_accepted": positive["accepted"],
        "invalid_rejected": not invalid["accepted"],
        "invalid_reasons": invalid["reasons"],
        "real_world_rows": 0,
        "authority_conferred": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runner-number", type=int, required=True)
    args = parser.parse_args()
    result = runner_smoke(args.runner_number)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["positive_accepted"] and result["invalid_rejected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
