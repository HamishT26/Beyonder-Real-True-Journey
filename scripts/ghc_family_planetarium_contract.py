#!/usr/bin/env python3
"""Shared zero-row contract for Caelen Ash v681-v7 planetarium runners."""
from __future__ import annotations

REQUIRED = (
    "record_id", "title", "identifiers", "sequence_start", "sequence_end",
    "status", "authority_claim", "real_rows", "private_material", "provenance",
)


def validate_record(record: dict) -> dict:
    reasons = []
    missing = [field for field in REQUIRED if field not in record]
    if missing:
        reasons.append("missing_required:" + ",".join(missing))
    identifiers = record.get("identifiers", [])
    if not isinstance(identifiers, list) or len(identifiers) < 2 or len(identifiers) != len(set(identifiers)):
        reasons.append("identifier_uniqueness_failed")
    start, end = record.get("sequence_start"), record.get("sequence_end")
    if not isinstance(start, int) or not isinstance(end, int) or start >= end:
        reasons.append("sequence_interval_invalid")
    if record.get("status") != "synthetic_only":
        reasons.append("synthetic_status_required")
    if record.get("authority_claim") != "reserved":
        reasons.append("authority_promotion_rejected")
    if record.get("real_rows") != 0 or record.get("private_material") is not False:
        reasons.append("real_or_private_row_rejected")
    provenance = record.get("provenance", {})
    if not isinstance(provenance, dict) or provenance.get("source") != "immutable_x1_contract":
        reasons.append("provenance_link_invalid")
    return {"accepted": not reasons, "reasons": sorted(set(reasons))}
