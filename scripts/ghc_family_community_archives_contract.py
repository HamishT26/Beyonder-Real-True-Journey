#!/usr/bin/env python3
"""Zero-row synthetic community-archives contract helpers.

The module validates structural fixtures only. It never downloads, edits,
identifies, describes, publishes, redacts, releases, corrects, deletes, or
authorizes a real archival record, collection, person, identity event, access
decision, or external action.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from typing import Any


REQUIRED_FIELDS = {
    "proposal_id",
    "synthetic",
    "real_rows",
    "external_actions",
    "collection_id",
    "description_id",
    "review_sequence",
    "source_digest",
    "applied_digest",
    "authority_state",
    "terminal_verdict",
}


def expected_source_digest(proposal_id: str) -> str:
    return hashlib.sha256(f"liora-v684-v8:source:{proposal_id}".encode("utf-8")).hexdigest()


def expected_applied_digest(proposal_id: str, sequence: int) -> str:
    payload = f"liora-v684-v8:applied:{proposal_id}:{sequence}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def positive_fixture(proposal_id: str) -> dict[str, Any]:
    sequence = 1
    return {
        "proposal_id": proposal_id,
        "synthetic": True,
        "real_rows": 0,
        "external_actions": 0,
        "collection_id": f"synthetic-collection-{proposal_id.lower()}",
        "description_id": f"synthetic-description-{proposal_id.lower()}",
        "review_sequence": sequence,
        "source_digest": expected_source_digest(proposal_id),
        "applied_digest": expected_applied_digest(proposal_id, sequence),
        "authority_state": "WITHHELD_SYNTHETIC_ONLY",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def validate_fixture(value: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(value))
    if missing:
        reasons.append("missing_required_field:" + ",".join(missing))

    proposal_id = value.get("proposal_id")
    sequence = value.get("review_sequence")
    if isinstance(proposal_id, str):
        if value.get("source_digest") != expected_source_digest(proposal_id):
            reasons.append("stale_precondition_digest")
        if isinstance(sequence, int) and sequence > 0:
            if value.get("applied_digest") != expected_applied_digest(proposal_id, sequence):
                reasons.append("correction_order_inversion")
        else:
            reasons.append("correction_order_inversion")

    collection_id = value.get("collection_id")
    description_id = value.get("description_id")
    if not (
        isinstance(collection_id, str)
        and collection_id.startswith("synthetic-collection-")
        and isinstance(description_id, str)
        and description_id.startswith("synthetic-description-")
    ):
        reasons.append("identifier_role_swap")

    if value.get("synthetic") is not True:
        reasons.append("authority_promotion")
    if value.get("real_rows") != 0 or value.get("external_actions") != 0:
        reasons.append("authority_promotion")
    if value.get("authority_state") != "WITHHELD_SYNTHETIC_ONLY":
        reasons.append("authority_promotion")
    if value.get("terminal_verdict") != "NOT_READY_FOR_STAGE_20":
        reasons.append("authority_promotion")

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
    elif mutation_type == "identifier_role_swap":
        changed["collection_id"], changed["description_id"] = (
            changed["description_id"],
            changed["collection_id"],
        )
    elif mutation_type == "stale_precondition_digest":
        changed["source_digest"] = "0" * 64
    elif mutation_type == "correction_order_inversion":
        changed["review_sequence"] = 0
        changed["applied_digest"] = "0" * 64
    elif mutation_type == "authority_promotion":
        changed["synthetic"] = False
        changed["real_rows"] = 1
        changed["external_actions"] = 1
        changed["authority_state"] = "RELEASED"
        changed["terminal_verdict"] = "READY_FOR_STAGE_20"
    else:
        raise ValueError(f"unsupported mutation type: {mutation_type}")
    return changed


RUNNER_NAMES = [
    "accession",
    "hierarchy",
    "provenance",
    "privacy",
    "access",
    "correction",
    "flashcard",
    "accessibility",
    "handover",
    "stage20",
]


def runner_smoke(runner_number: int) -> dict[str, Any]:
    if runner_number < 1 or runner_number > len(RUNNER_NAMES):
        raise ValueError("runner_number must be between 1 and 10")
    proposal_id = f"LV6848-N{runner_number:03d}"
    positive = validate_fixture(positive_fixture(proposal_id))
    invalid = validate_fixture(mutate(positive_fixture(proposal_id), "authority_promotion"))
    name = RUNNER_NAMES[runner_number - 1]
    return {
        "runner": f"ghc_family_community_archives_{name}_runner",
        "proposal_id": proposal_id,
        "positive_accepted": positive["accepted"],
        "invalid_rejected": not invalid["accepted"],
        "invalid_reasons": invalid["reasons"],
        "real_world_rows": 0,
        "external_actions": 0,
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
