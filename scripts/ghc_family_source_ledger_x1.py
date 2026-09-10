#!/usr/bin/env python3
"""Field-closed x1 source-ledger operations for Vesper v689-v7-r2."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Callable
from typing import Any

TOP_FIELDS = {"op", "payload", "synthetic"}
RANKS = {"direct_user": 4, "current_reference": 3, "exact_owner_evidence": 2, "historical_doc": 1, "screenshot": 0, "external_post": 0}
STATUSES = {"controlling", "current", "sealed", "historical", "corroborating"}
GRADES = {"aspiration", "formal_proposal", "synthetic_structure", "same_owner_test", "external_demo_claim", "empirical_gap", "authority_gap", "historical_assertion", "correction", "reservation"}
DOMAINS = {"standard", "package_metadata", "software_docs", "historical_text", "external_post", "simulation", "identity", "rights", "physics", "accessibility"}


class ContractError(ValueError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def closed(payload: Any, fields: set[str]) -> dict[str, Any]:
    if not isinstance(payload, dict) or set(payload) != fields:
        raise ContractError("E_PAYLOAD_FIELDS")
    return payload


def require_string(value: Any) -> str:
    if not isinstance(value, str):
        raise ContractError("E_TYPE")
    return value


def source_record_shape(payload: Any) -> dict[str, Any]:
    value = closed(payload, {"source_id", "kind", "status"})
    source_id, kind, status = map(require_string, (value["source_id"], value["kind"], value["status"]))
    return {"field_count": 3, "has_source_id": bool(source_id), "recognized_kind": kind in RANKS, "recognized_status": status in STATUSES}


def digest_envelope(payload: Any) -> dict[str, Any]:
    value = closed(payload, {"data_hex", "declared_sha256"})
    try:
        data = bytes.fromhex(require_string(value["data_hex"]))
    except ValueError as exc:
        raise ContractError("E_HEX") from exc
    declared = require_string(value["declared_sha256"])
    observed = hashlib.sha256(data).hexdigest()
    return {"algorithm": "sha256", "bytes": len(data), "matches": observed == declared, "authenticity_proven": False}


def encoding_observation(payload: Any) -> dict[str, Any]:
    value = closed(payload, {"data_hex"})
    try:
        data = bytes.fromhex(require_string(value["data_hex"]))
        text = data.decode("utf-8")
    except (ValueError, UnicodeDecodeError) as exc:
        raise ContractError("E_UTF8") from exc
    return {"bom": data.startswith(b"\xef\xbb\xbf"), "replacement_characters": text.count("\ufffd"), "text": text.lstrip("\ufeff"), "utf8_valid": True}


def version_token(payload: Any) -> dict[str, Any]:
    token = require_string(closed(payload, {"token"})["token"])
    match = re.fullmatch(r"v(\d+)(?:-v(\d+))?(?:-r(\d+))?", token)
    if not match:
        raise ContractError("E_VERSION")
    parts = [int(item) for item in match.groups() if item is not None]
    normalized = "v" + "-v".join(str(item) for item in parts[:2]) + (f"-r{parts[2]}" if len(parts) == 3 else "")
    return {"normalized": normalized, "parts": parts}


def authority_tier(payload: Any) -> dict[str, Any]:
    kind = require_string(closed(payload, {"source_kind"})["source_kind"])
    if kind not in RANKS:
        raise ContractError("E_SOURCE_KIND")
    return {"action_authority": kind == "direct_user", "rank": RANKS[kind], "source_kind": kind}


def instruction_quarantine(payload: Any) -> dict[str, Any]:
    value = closed(payload, {"source_kind", "text"})
    kind, text = require_string(value["source_kind"]), require_string(value["text"])
    imperative = bool(re.search(r"(?i)\b(please|must|should|install|create|run|execute|continue|update|message|activate|deploy|do not)\b", text))
    if kind != "historical_doc":
        raise ContractError("E_SOURCE_KIND")
    return {"action_authorized": False, "content_role": "historical_source", "embedded_instruction": imperative, "retained": True}


def claim_grade(payload: Any) -> dict[str, Any]:
    value = closed(payload, {"declared_grade", "has_real_rows", "independent_review", "competent_authority"})
    grade = require_string(value["declared_grade"])
    if grade not in GRADES or any(type(value[field]) is not bool for field in ("has_real_rows", "independent_review", "competent_authority")):
        raise ContractError("E_GRADE")
    return {"accepted_grade": grade, "empirical_confirmation": False, "self_reported_flags_only": True}


def citation_scope(payload: Any) -> dict[str, Any]:
    value = closed(payload, {"domain", "source_present"})
    domain = require_string(value["domain"])
    if domain not in DOMAINS or type(value["source_present"]) is not bool:
        raise ContractError("E_CITATION")
    return {"citation_is_execution": False, "domain": domain, "scope": "bounded_context_only"}


def lineage_nonidentity(payload: Any) -> dict[str, Any]:
    value = closed(payload, {"left_sha256", "right_sha256"})
    left, right = require_string(value["left_sha256"]), require_string(value["right_sha256"])
    if not re.fullmatch(r"[0-9a-f]{64}", left) or not re.fullmatch(r"[0-9a-f]{64}", right):
        raise ContractError("E_DIGEST")
    return {"byte_correspondence": left == right, "identity_continuity": False, "same_record_claim": False}


def excerpt_window(payload: Any) -> dict[str, Any]:
    value = closed(payload, {"items", "start", "width"})
    items, start, width = value["items"], value["start"], value["width"]
    if not isinstance(items, list) or not all(isinstance(item, str) for item in items) or type(start) is not int or type(width) is not int or start < 0 or width < 1 or start > len(items):
        raise ContractError("E_WINDOW")
    return {"items": items[start : start + width], "start": start, "truncated": start + width < len(items)}


OPERATIONS: dict[str, Callable[[Any], Any]] = {
    "source_record_shape": source_record_shape,
    "digest_envelope": digest_envelope,
    "encoding_observation": encoding_observation,
    "version_token": version_token,
    "authority_tier": authority_tier,
    "instruction_quarantine": instruction_quarantine,
    "claim_grade": claim_grade,
    "citation_scope": citation_scope,
    "lineage_nonidentity": lineage_nonidentity,
    "excerpt_window": excerpt_window,
}


def evaluate(request: Any) -> dict[str, Any]:
    if not isinstance(request, dict) or set(request) != TOP_FIELDS:
        return {"error": "E_FIELDS", "ok": False, "value": None}
    if request.get("synthetic") is not True:
        return {"error": "E_SYNTHETIC", "ok": False, "value": None}
    operation = request.get("op")
    if operation not in OPERATIONS:
        return {"error": "E_OPERATION", "ok": False, "value": None}
    try:
        value = OPERATIONS[operation](request.get("payload"))
        return {"error": None, "ok": True, "value": value}
    except ContractError as exc:
        return {"error": exc.code, "ok": False, "value": None}
