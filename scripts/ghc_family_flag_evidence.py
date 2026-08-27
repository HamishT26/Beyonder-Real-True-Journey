"""Deterministic synthetic evidence-envelope helper."""
from __future__ import annotations
import hashlib
import json
from typing import Any

def seal(payload: Any) -> dict[str, Any]:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return {"sha256": hashlib.sha256(encoded).hexdigest(), "bytes": len(encoded), "hash_domain": "canonical_utf8_json", "external_actions": 0}

def verify(payload: Any, receipt: dict[str, Any]) -> bool:
    return seal(payload) == receipt
