"""Lyren v690-v1 finite error-control operations for the x2 tranche."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from collections import Counter
from itertools import pairwise
from typing import Any

OPERATIONS = {
    "crc_append",
    "crc_verify",
    "xor_checksum",
    "row_interleave",
    "row_deinterleave",
    "erasure_inventory",
    "sequence_gap_map",
    "provenance_digest",
    "accessible_error_summary",
    "coding_evidence_reservation",
}

FIELDS = {
    "crc_append": {"data", "polynomial"},
    "crc_verify": {"codeword", "polynomial"},
    "xor_checksum": {"bytes"},
    "row_interleave": {"bits", "rows"},
    "row_deinterleave": {"codeword", "rows"},
    "erasure_inventory": {"values"},
    "sequence_gap_map": {"sequence"},
    "provenance_digest": {"record", "source_sha256"},
    "accessible_error_summary": {"detected", "corrected", "uncorrectable", "unknown"},
    "coding_evidence_reservation": {"obligation", "kind", "evidence", "authority"},
}


def _error(name: str) -> dict[str, Any]:
    return {"ok": False, "error": name, "original_success_credit": 0}


def _bits(value: Any) -> str:
    if not isinstance(value, str) or not value or any(char not in "01" for char in value):
        raise ValueError("invalid_bits")
    return value


def _polynomial(value: Any) -> str:
    polynomial = _bits(value)
    if len(polynomial) < 2 or polynomial[0] != "1" or polynomial[-1] != "1":
        raise ValueError("invalid_polynomial")
    return polynomial


def _integer(value: Any, *, minimum: int | None = None, maximum: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("invalid_integer")
    if minimum is not None and value < minimum:
        raise ValueError("integer_below_minimum")
    if maximum is not None and value > maximum:
        raise ValueError("integer_above_maximum")
    return value


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def _object_sha256(value: object) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _gf2_remainder(dividend: str, polynomial: str) -> str:
    dividend = _bits(dividend)
    polynomial = _polynomial(polynomial)
    work = [int(char) for char in dividend]
    divisor = [int(char) for char in polynomial]
    for start in range(max(0, len(work) - len(divisor) + 1)):
        if work[start]:
            for offset, bit in enumerate(divisor):
                work[start + offset] ^= bit
    degree = len(divisor) - 1
    tail = work[-degree:] if len(work) >= degree else [0] * (degree - len(work)) + work
    return "".join(str(bit) for bit in tail)


def _crc_remainder(data: str, polynomial: str) -> str:
    data = _bits(data)
    polynomial = _polynomial(polynomial)
    return _gf2_remainder(data + "0" * (len(polynomial) - 1), polynomial)


def _rows(value: Any, length: int) -> int:
    rows = _integer(value, minimum=1)
    if length % rows:
        raise ValueError("non_rectangular_interleave")
    return rows


def _interleave(bits: str, rows: int) -> str:
    columns = len(bits) // rows
    return "".join(bits[row * columns + column] for column in range(columns) for row in range(rows))


def _deinterleave(codeword: str, rows: int) -> str:
    columns = len(codeword) // rows
    grid = [["0"] * columns for _ in range(rows)]
    cursor = 0
    for column in range(columns):
        for row in range(rows):
            grid[row][column] = codeword[cursor]
            cursor += 1
    return "".join("".join(row) for row in grid)


def evaluate(operation: str, payload: dict[str, Any]) -> Any:
    if operation == "crc_append":
        data = _bits(payload["data"])
        polynomial = _polynomial(payload["polynomial"])
        remainder = _crc_remainder(data, polynomial)
        return {"codeword": data + remainder, "remainder": remainder, "cryptographic": False}
    if operation == "crc_verify":
        codeword = _bits(payload["codeword"])
        polynomial = _polynomial(payload["polynomial"])
        remainder = _gf2_remainder(codeword, polynomial)
        return {"valid": set(remainder) <= {"0"}, "remainder": remainder, "repair_performed": False}
    if operation == "xor_checksum":
        values = payload["bytes"]
        if not isinstance(values, list) or not values:
            raise ValueError("invalid_byte_list")
        checksum = 0
        for value in values:
            checksum ^= _integer(value, minimum=0, maximum=255)
        return {"checksum": checksum, "bits": f"{checksum:08b}", "cryptographic": False}
    if operation == "row_interleave":
        bits = _bits(payload["bits"])
        rows = _rows(payload["rows"], len(bits))
        return {"codeword": _interleave(bits, rows), "rows": rows, "columns": len(bits) // rows}
    if operation == "row_deinterleave":
        codeword = _bits(payload["codeword"])
        rows = _rows(payload["rows"], len(codeword))
        return {"bits": _deinterleave(codeword, rows), "rows": rows, "columns": len(codeword) // rows}
    if operation == "erasure_inventory":
        values = payload["values"]
        if not isinstance(values, list) or not values or any(value not in {0, 1, None} for value in values):
            raise ValueError("invalid_erasure_vector")
        positions = [index for index, value in enumerate(values) if value is None]
        return {"erasures": positions, "erasure_count": len(positions), "known_count": len(values) - len(positions), "repair_performed": False}
    if operation == "sequence_gap_map":
        sequence = payload["sequence"]
        if not isinstance(sequence, list) or not sequence:
            raise ValueError("invalid_sequence")
        values = [_integer(value) for value in sequence]
        counts = Counter(values)
        missing = sorted(set(range(min(values), max(values) + 1)) - set(values))
        return {
            "missing": missing,
            "duplicates": sorted(value for value, count in counts.items() if count > 1),
            "strictly_increasing": all(left < right for left, right in pairwise(values)),
            "source_retained": True,
        }
    if operation == "provenance_digest":
        record = payload["record"]
        source = payload["source_sha256"]
        if not isinstance(record, dict) or not record:
            raise ValueError("invalid_record")
        if not isinstance(source, str) or re.fullmatch(r"[0-9a-f]{64}", source) is None:
            raise ValueError("invalid_source_digest")
        record_copy = copy.deepcopy(record)
        record_digest = _object_sha256(record_copy)
        return {
            "record_sha256": record_digest,
            "source_sha256": source,
            "binding_sha256": _object_sha256({"record_sha256": record_digest, "source_sha256": source}),
            "identity_established": False,
        }
    if operation == "accessible_error_summary":
        detected = _integer(payload["detected"], minimum=0)
        corrected = _integer(payload["corrected"], minimum=0)
        uncorrectable = _integer(payload["uncorrectable"], minimum=0)
        unknown = _integer(payload["unknown"], minimum=0)
        return {
            "text": f"Synthetic blocks: detected {detected}; corrected {corrected}; uncorrectable {uncorrectable}; unknown {unknown}.",
            "manual_evaluation": "reserved",
            "empirical": False,
        }
    if operation == "coding_evidence_reservation":
        if payload["kind"] not in {"scientific_evidence", "competent_authority"}:
            raise ValueError("invalid_obligation_kind")
        if not isinstance(payload["obligation"], str) or not payload["obligation"]:
            raise ValueError("invalid_obligation")
        if payload["evidence"] is not None or payload["authority"] is not None:
            raise ValueError("unsupported_evidence_or_authority_promotion")
        state = "open_gap" if payload["kind"] == "scientific_evidence" else "exact_gate"
        return {"obligation": payload["obligation"], "state": state, "evidence": None, "authority": None}
    raise ValueError("unknown_operation")


def run(request: Any) -> dict[str, Any]:
    original = copy.deepcopy(request)
    if not isinstance(request, dict) or set(request) != {"operation", "payload"}:
        return _error("invalid_request_shape")
    operation = request.get("operation")
    payload = request.get("payload")
    if operation not in OPERATIONS:
        return _error("unknown_operation")
    if not isinstance(payload, dict):
        return _error("invalid_payload")
    if set(payload) != FIELDS[operation]:
        return _error("unknown_payload_field")
    try:
        value = evaluate(operation, copy.deepcopy(payload))
    except (KeyError, TypeError, ValueError) as exc:
        return _error(str(exc) or "invalid_payload")
    if request != original:
        return _error("input_mutated")
    outcome = (
        "represented"
        if operation == "accessible_error_summary"
        else value["state"]
        if operation == "coding_evidence_reservation"
        else "completed"
    )
    return {"ok": True, "operation": operation, "outcome": outcome, "value": value}
