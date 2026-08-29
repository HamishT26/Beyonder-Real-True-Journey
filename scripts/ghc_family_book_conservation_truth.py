from __future__ import annotations

from typing import Any

FOCUS = 'truth'
REQUIRED_FIELDS = ['core_outcome', 'protected_gates', 'authority_conferred']
FORBIDDEN_FIELDS = [
    "real_person",
    "real_object",
    "real_measurement",
    "professional_release",
    "authority_claim",
]


def run(payload: dict[str, Any]) -> dict[str, Any]:
    missing = [field for field in REQUIRED_FIELDS if field not in payload]
    forbidden = [field for field in FORBIDDEN_FIELDS if payload.get(field)]
    passed = not missing and not forbidden
    return {
        "focus": FOCUS,
        "passed": passed,
        "missing": missing,
        "forbidden": forbidden,
        "authority_conferred": False,
    }
