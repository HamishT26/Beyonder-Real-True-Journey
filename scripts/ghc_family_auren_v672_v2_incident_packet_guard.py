#!/usr/bin/env python3
"""Synthetic public-interest incident-documentation guard for Auren v672-v2."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ALLOWED_SOURCE_STATES = {"current", "stable", "draft", "watch"}
ALLOWED_UNCERTAINTY = {"observed", "reported", "inferred", "unknown", "contested"}
ALLOWED_READBACK = {"pending", "acknowledged", "exception"}
AUTHORITY_VACANCIES = {"professional", "legal", "affected_party", "maori", "public_release"}


def _require(condition: bool, code: str, errors: list[str]) -> None:
    if not condition:
        errors.append(code)


def validate(surface: str, payload: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["payload_not_object"]
    _require(payload.get("fixture_surface") == surface, "surface_mismatch", errors)
    _require(payload.get("synthetic") is True, "synthetic_boundary_missing", errors)
    _require(payload.get("authority_promoted") is False, "authority_promotion", errors)
    _require(payload.get("raw_identifiers") == [], "raw_identifier_present", errors)

    if surface == "chronology":
        events = payload.get("events")
        _require(isinstance(events, list) and len(events) >= 2, "events_missing", errors)
        if isinstance(events, list) and events:
            sequences = [row.get("sequence") for row in events if isinstance(row, dict)]
            _require(sequences == list(range(1, len(events) + 1)), "sequence_not_contiguous", errors)
            _require(
                all(row.get("observed_at") and row.get("recorded_at") for row in events if isinstance(row, dict)),
                "bitemporal_fields_missing",
                errors,
            )
    elif surface == "source_status":
        sources = payload.get("sources")
        _require(isinstance(sources, list) and bool(sources), "sources_missing", errors)
        if isinstance(sources, list):
            states = {row.get("status") for row in sources if isinstance(row, dict)}
            _require(states <= ALLOWED_SOURCE_STATES and bool(states), "source_status_invalid", errors)
    elif surface == "correction_log":
        corrections = payload.get("corrections")
        _require(isinstance(corrections, list) and bool(corrections), "corrections_missing", errors)
        if isinstance(corrections, list):
            _require(all(row.get("reason") for row in corrections if isinstance(row, dict)), "correction_reason_missing", errors)
            _require(all(row.get("supersedes") != row.get("correction_id") for row in corrections if isinstance(row, dict)), "self_supersession", errors)
    elif surface == "uncertainty":
        statements = payload.get("statements")
        _require(isinstance(statements, list) and bool(statements), "statements_missing", errors)
        if isinstance(statements, list):
            states = {row.get("uncertainty") for row in statements if isinstance(row, dict)}
            _require(states <= ALLOWED_UNCERTAINTY and bool(states), "uncertainty_invalid", errors)
    elif surface == "authority_boundary":
        vacancies = set(payload.get("vacancies", []))
        _require(vacancies == AUTHORITY_VACANCIES, "authority_vacancies_incomplete", errors)
        _require(payload.get("external_action") is False, "external_action_present", errors)
        _require(payload.get("public_release") == "blocked", "release_not_blocked", errors)
    elif surface == "privacy_minimization":
        _require(payload.get("purpose_limited") is True, "purpose_limit_missing", errors)
        _require(payload.get("private_data_used") is False, "private_data_present", errors)
        fields = payload.get("allowed_fields")
        _require(isinstance(fields, list) and 1 <= len(fields) <= 8, "field_budget_invalid", errors)
    elif surface == "accessibility_handoff":
        _require(payload.get("structural_proxy") is True, "structural_proxy_missing", errors)
        _require(payload.get("complete_accessibility_claim") is False, "accessibility_complete_promotion", errors)
        _require(bool(payload.get("text_alternatives")), "text_alternatives_missing", errors)
        _require(bool(payload.get("table_headers")), "table_headers_missing", errors)
    elif surface == "evidence_chain":
        attachments = payload.get("attachments")
        _require(isinstance(attachments, list) and bool(attachments), "attachments_missing", errors)
        if isinstance(attachments, list):
            _require(
                all(re.fullmatch(r"[0-9a-f]{64}", str(row.get("sha256", ""))) for row in attachments if isinstance(row, dict)),
                "fixity_invalid",
                errors,
            )
            _require(all(row.get("bytes", 0) > 0 for row in attachments if isinstance(row, dict)), "byte_count_invalid", errors)
        _require(payload.get("document_truth_inferred") is False, "document_truth_promotion", errors)
    elif surface == "readback":
        items = payload.get("items")
        _require(isinstance(items, list) and bool(items), "readback_items_missing", errors)
        if isinstance(items, list):
            states = {row.get("status") for row in items if isinstance(row, dict)}
            _require(states <= ALLOWED_READBACK and bool(states), "readback_status_invalid", errors)
        _require(payload.get("acceptance_authority") is False, "acceptance_authority_promotion", errors)
    elif surface == "packet":
        _require(str(payload.get("packet_id", "")).startswith("SYN-INC-"), "packet_id_invalid", errors)
        _require(payload.get("real_incident") is False, "real_incident_present", errors)
        _require(bool(payload.get("events")), "packet_events_missing", errors)
        _require(payload.get("release_state") == "blocked", "packet_release_not_blocked", errors)
    else:
        errors.append("unknown_surface")
    return sorted(set(errors))


def run_surface(surface: str) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--expect", choices=("accept", "reject"), required=True)
    args = parser.parse_args()
    wrapper = json.loads(Path(args.input).read_text(encoding="utf-8"))
    errors = validate(surface, wrapper.get("payload"))
    passed = (args.expect == "accept" and not errors) or (args.expect == "reject" and bool(errors))
    print(json.dumps({"surface": surface, "expect": args.expect, "passed": passed, "errors": errors}, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    run_surface("packet")
