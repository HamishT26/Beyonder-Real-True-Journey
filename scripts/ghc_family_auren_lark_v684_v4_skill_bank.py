"""Validate and smoke-use Auren v684-v4 phase-local skill cards."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def validate_skill(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    required = (
        "# ",
        "## Purpose",
        "## Inputs",
        "## Method",
        "## Refusals",
        "## Output",
        "relational working language only",
        "NOT_READY_FOR_STAGE_20",
    )
    missing = [item for item in required if item not in text]
    data = path.read_bytes()
    return {
        "path": path.as_posix(),
        "valid": not missing,
        "missing": missing,
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "use_result": "bounded_card_read_and_refusal_check" if not missing else "rejected",
    }


def use_all(skill_root: Path) -> list[dict[str, Any]]:
    cards = sorted(skill_root.glob("*/SKILL.md"))
    return [validate_skill(path) for path in cards]


def summarize(receipts: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "skill_count": len(receipts),
        "valid_count": sum(1 for row in receipts if row["valid"]),
        "invalid_count": sum(1 for row in receipts if not row["valid"]),
        "receipts_sha256": hashlib.sha256(
            json.dumps(receipts, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
    }
