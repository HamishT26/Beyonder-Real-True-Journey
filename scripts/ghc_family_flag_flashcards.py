"""Four-tier Freed ID flashcard projection and acyclic-card validator."""
from __future__ import annotations
import hashlib
import json
from typing import Any

TIERS = {"freed_id", "pillar", "practice", "task"}

def content_hash(card: dict[str, Any]) -> str:
    body = {key: value for key, value in card.items() if key != "sha256"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()

def validate_deck(cards: list[dict[str, Any]]) -> dict[str, Any]:
    ids = {card.get("card_id") for card in cards}
    issues = []
    if len(ids) != len(cards) or None in ids:
        issues.append("unique_card_ids_required")
    for card in cards:
        if card.get("tier") not in TIERS:
            issues.append(f"invalid_tier:{card.get('card_id')}")
        if any(parent not in ids for parent in card.get("parents", [])):
            issues.append(f"missing_parent:{card.get('card_id')}")
        if card.get("card_id") in card.get("parents", []):
            issues.append(f"self_cycle:{card.get('card_id')}")
        if card.get("sha256") != content_hash(card):
            issues.append(f"hash_mismatch:{card.get('card_id')}")
    return {"valid": not issues, "issues": issues, "card_count": len(cards), "external_actions": 0}
