"""
freed_id_minimum_disclosure.py
------------------------------

Minimum-disclosure helpers for GOV-002 privacy-by-design controls.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Iterable, Set

DEFAULT_SENSITIVE_FIELDS: Set[str] = {
    "full_name",
    "legal_name",
    "government_id",
    "birth_date",
    "email",
    "phone",
    "home_address",
}


@dataclass
class MinimumDisclosurePolicy:
    policy_version: str = "v0"
    sensitive_fields: Set[str] = field(default_factory=lambda: set(DEFAULT_SENSITIVE_FIELDS))
    allowed_sensitive_fields: Set[str] = field(default_factory=set)


def build_minimum_disclosure_presentation(
    subject_did: str,
    credential_id: str,
    claims: Dict[str, object],
    requested_fields: Iterable[str],
    policy: MinimumDisclosurePolicy,
) -> Dict[str, object]:
    requested = [field for field in requested_fields]
    requested_set = set(requested)

    disclosed_claims: Dict[str, object] = {}
    redacted_fields: list[str] = []
    denied_sensitive_fields: list[str] = []

    for field_name, field_value in claims.items():
        if field_name not in requested_set:
            redacted_fields.append(field_name)
            continue
        if field_name in policy.sensitive_fields and field_name not in policy.allowed_sensitive_fields:
            denied_sensitive_fields.append(field_name)
            redacted_fields.append(field_name)
            continue
        disclosed_claims[field_name] = field_value

    return {
        "subject_did": subject_did,
        "credential_id": credential_id,
        "requested_fields": requested,
        "disclosed_claims": disclosed_claims,
        "redacted_fields": sorted(set(redacted_fields)),
        "denied_sensitive_fields": sorted(set(denied_sensitive_fields)),
        "policy_version": policy.policy_version,
        "created_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }


def validate_minimum_disclosure_presentation(
    presentation: Dict[str, object],
    policy: MinimumDisclosurePolicy,
) -> tuple[bool, str]:
    required = {
        "subject_did",
        "credential_id",
        "requested_fields",
        "disclosed_claims",
        "redacted_fields",
        "denied_sensitive_fields",
        "policy_version",
        "created_utc",
    }
    missing = sorted(required - set(presentation.keys()))
    if missing:
        return False, f"missing_required_fields={missing}"

    requested_fields = presentation.get("requested_fields")
    disclosed_claims = presentation.get("disclosed_claims")
    denied_sensitive_fields = presentation.get("denied_sensitive_fields")
    if not isinstance(requested_fields, list):
        return False, "requested_fields must be a list"
    if not isinstance(disclosed_claims, dict):
        return False, "disclosed_claims must be a dict"
    if not isinstance(denied_sensitive_fields, list):
        return False, "denied_sensitive_fields must be a list"

    requested_set = set(str(field) for field in requested_fields)
    disclosed_fields = set(str(field) for field in disclosed_claims.keys())
    if not disclosed_fields.issubset(requested_set):
        leaked = sorted(disclosed_fields - requested_set)
        return False, f"disclosed_fields_not_requested={leaked}"

    denied_set = set(str(field) for field in denied_sensitive_fields)
    leaked_sensitive = sorted(
        field
        for field in disclosed_fields
        if field in policy.sensitive_fields and field not in policy.allowed_sensitive_fields
    )
    if leaked_sensitive:
        return False, f"sensitive_fields_disclosed_without_allowance={leaked_sensitive}"

    missing_denied = sorted(
        field
        for field in denied_set
        if field not in policy.sensitive_fields
    )
    if missing_denied:
        return False, f"denied_sensitive_fields_not_marked_sensitive={missing_denied}"

    return True, "presentation_valid"
