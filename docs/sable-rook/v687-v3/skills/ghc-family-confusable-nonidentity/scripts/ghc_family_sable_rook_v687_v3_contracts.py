#!/usr/bin/env python3
"""Bounded synthetic evidence-interchange contracts for Sable v687-v3."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import re
from typing import Any


RISKY_CONFUSABLES = {"а", "Α", "о", "ρ", "Μ", "С"}
SAFE_GMUT_TYPES = {"typed_value", "serialization", "dimension", "unit", "schema"}


def strict_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(strict_equal(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(strict_equal(a, b) for a, b in zip(left, right))
    return left == right


def _require_dict(value: Any, keys: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("INVALID_SHAPE")
    return value


def jcs_canonical_profile(payload: Any) -> dict[str, Any]:
    _require_dict(payload, {"value"})
    import rfc8785

    encoded = rfc8785.dumps(payload["value"])
    return {
        "authority": False,
        "canonical_utf8": encoded.decode("utf-8"),
        "sha256": hashlib.sha256(encoded).hexdigest(),
    }


def confusable_nonidentity(payload: Any) -> dict[str, Any]:
    _require_dict(payload, {"text", "preferred_script"})
    if not isinstance(payload["text"], str) or payload["preferred_script"] != "latin":
        raise ValueError("INVALID_SHAPE")
    from confusable_homoglyphs import confusables

    # Exercise the frozen package dataset, while keeping the phase policy's
    # curated decision and its nonidentity boundary explicit.
    confusables.is_confusable(payload["text"], greedy=True, preferred_aliases=["latin"])
    return {
        "identity_equivalence": False,
        "requires_human_review": any(char in RISKY_CONFUSABLES for char in payload["text"]),
        "skeleton_persisted": False,
        "source_profile": "UTS39_ADVISORY_ONLY",
    }


def digest_migration_ledger(payload: Any) -> dict[str, Any]:
    _require_dict(payload, {"record_id", "old_algorithm", "new_algorithm", "old_digest_present", "new_digest_present"})
    if payload["old_algorithm"] != "sha256" or payload["new_algorithm"] != "blake3":
        raise ValueError("INVALID_ALGORITHM")
    if type(payload["old_digest_present"]) is not bool or type(payload["new_digest_present"]) is not bool:
        raise ValueError("INVALID_SHAPE")
    reasons = []
    if not payload["old_digest_present"]:
        reasons.append("missing_old_digest")
    if not payload["new_digest_present"]:
        reasons.append("missing_new_digest")
    return {"authority": False, "decision": "DUAL_BOUND" if not reasons else "HOLD", "reasons": reasons}


def receipt_expiry_conjunction(payload: Any) -> dict[str, Any]:
    _require_dict(payload, {"issued", "expires", "observed"})
    if any(type(payload[key]) is not int for key in payload):
        raise ValueError("INVALID_TIME")
    if payload["issued"] > payload["observed"]:
        state = "NOT_YET_VALID"
    elif payload["expires"] < payload["observed"]:
        state = "EXPIRED"
    else:
        state = "FRESH"
    return {"decision": state, "external_credit": False}


def event_branch_conflict(payload: Any) -> dict[str, Any]:
    _require_dict(payload, {"stream", "branch_heads"})
    heads = payload["branch_heads"]
    if not isinstance(payload["stream"], str) or not isinstance(heads, list) or len(heads) != 2 or not all(isinstance(item, str) for item in heads):
        raise ValueError("INVALID_BRANCH")
    return {"decision": "CONSISTENT" if heads[0] == heads[1] else "CONFLICT", "live_action": False}


def checkpoint_parent_fixity(payload: Any) -> dict[str, Any]:
    _require_dict(payload, {"parent_sha256", "observed_parent_sha256"})
    digest = re.compile(r"^[0-9a-f]{64}$")
    if not all(isinstance(payload[key], str) and digest.fullmatch(payload[key]) for key in payload):
        raise ValueError("INVALID_DIGEST")
    return {"decision": "VALID" if payload["parent_sha256"] == payload["observed_parent_sha256"] else "HOLD", "records_rewritten": 0}


def artifact_budget_uncertainty(payload: Any) -> dict[str, Any]:
    _require_dict(payload, {"files_low", "files_high", "file_limit"})
    if any(type(payload[key]) is not int for key in payload) or payload["files_low"] < 0 or payload["files_high"] < payload["files_low"] or payload["file_limit"] != 2000:
        raise ValueError("INVALID_BUDGET")
    if payload["files_low"] > 2000:
        decision = "EXCEEDED"
    elif payload["files_high"] >= 2000:
        decision = "UNCERTAIN_HOLD"
    else:
        decision = "WITHIN"
    return {"decision": decision, "remaining_conservative": max(0, 2000 - payload["files_high"])}


def accessible_codec_comparison(payload: Any) -> dict[str, Any]:
    _require_dict(payload, {"surface", "caption", "column_headers", "text_alternative", "status_text"})
    flags = [payload[key] for key in ["caption", "column_headers", "text_alternative", "status_text"]]
    if not isinstance(payload["surface"], str) or not all(type(value) is bool for value in flags):
        raise ValueError("INVALID_ACCESSIBILITY_SHAPE")
    return {"decision": "STRUCTURAL_PASS" if all(flags) else "HOLD", "manual_evaluation_reserved": True}


def gmut_claim_firewall(payload: Any) -> dict[str, Any]:
    _require_dict(payload, {"claim_type", "evidence_class"})
    if not isinstance(payload["claim_type"], str) or payload["evidence_class"] != "synthetic_software":
        raise ValueError("INVALID_CLAIM")
    return {
        "classification": "represented",
        "promotion_blocked": payload["claim_type"] not in SAFE_GMUT_TYPES,
        "empirical": False,
        "theory_of_everything": False,
    }


def authority_vacancy_matrix(payload: Any) -> dict[str, Any]:
    _require_dict(payload, {"topic", "evidence_present"})
    if not isinstance(payload["topic"], str) or type(payload["evidence_present"]) is not bool:
        raise ValueError("INVALID_AUTHORITY_REQUEST")
    open_topics = {
        "real participant evidence", "real collection measurement", "independent review",
        "production interoperability", "complete privacy review", "complete accessibility review",
        "empirical GMUT likelihood", "THOS matched-budget arm", "real cryptographic proof",
        "affected-user evaluation",
    }
    disposition = "open_gap" if payload["topic"] in open_topics else "exact_gate"
    return {"decision": "HOLD", "disposition": disposition, "authority_conferred": False}


OPERATIONS = {
    "jcs_canonical_profile": jcs_canonical_profile,
    "confusable_nonidentity": confusable_nonidentity,
    "digest_migration_ledger": digest_migration_ledger,
    "receipt_expiry_conjunction": receipt_expiry_conjunction,
    "event_branch_conflict": event_branch_conflict,
    "checkpoint_parent_fixity": checkpoint_parent_fixity,
    "artifact_budget_uncertainty": artifact_budget_uncertainty,
    "accessible_codec_comparison": accessible_codec_comparison,
    "gmut_claim_firewall": gmut_claim_firewall,
    "authority_vacancy_matrix": authority_vacancy_matrix,
}


def evaluate(operation: str, payload: Any) -> dict[str, Any]:
    if operation not in OPERATIONS:
        raise ValueError("UNKNOWN_OPERATION")
    return OPERATIONS[operation](payload)


def mutate_result(expected: dict[str, Any], kind: str, target: str) -> dict[str, Any]:
    changed = json.loads(json.dumps(expected, ensure_ascii=False))
    if kind == "remove_field":
        changed.pop(target, None)
    elif kind == "unexpected_field":
        changed[target] = "unexpected"
    elif kind == "type_flip":
        value = changed.get(target)
        changed[target] = 1 if type(value) is bool else True if isinstance(value, (int, str)) else "changed"
    elif kind == "authority_promotion":
        changed[target] = True
    elif kind == "value_change":
        value = changed.get(target)
        if type(value) is bool:
            changed[target] = not value
        elif isinstance(value, int):
            changed[target] = value + 1
        elif isinstance(value, str):
            changed[target] = value + "_changed"
        elif isinstance(value, list):
            changed[target] = value + ["changed"]
        else:
            changed[target] = "changed"
    else:
        raise ValueError("UNKNOWN_MUTATION")
    return changed


def accept_result(expected: dict[str, Any], submitted: Any) -> bool:
    return strict_equal(expected, submitted)


def package_smoke() -> dict[str, Any]:
    import rfc8785
    from blake3 import blake3
    from confusable_homoglyphs import confusables

    versions = {
        "rfc8785": importlib.metadata.version("rfc8785"),
        "confusable-homoglyphs": importlib.metadata.version("confusable-homoglyphs"),
        "blake3": importlib.metadata.version("blake3"),
    }
    positives = {
        "rfc8785": rfc8785.dumps({"b": 1, "a": 2}) == b'{"a":2,"b":1}',
        "confusable_homoglyphs": bool(confusables.is_confusable("pаypal", greedy=True, preferred_aliases=["latin"])),
        "blake3": blake3(b"abc").hexdigest() == blake3().update(b"a").update(b"bc").hexdigest(),
    }
    adverse = {}
    try:
        rfc8785.dumps({1: "x"})
        adverse["rfc8785"] = False
    except Exception:
        adverse["rfc8785"] = True
    try:
        confusables.is_confusable(123)
        adverse["confusable_homoglyphs"] = False
    except Exception:
        adverse["confusable_homoglyphs"] = True
    try:
        blake3(key=b"short")
        adverse["blake3"] = False
    except Exception:
        adverse["blake3"] = True
    return {"versions": versions, "positive": positives, "adverse": adverse}
