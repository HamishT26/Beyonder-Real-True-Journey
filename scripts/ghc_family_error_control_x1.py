"""Lyren v690-v1 finite error-control operations for the immutable x1 tranche."""

from __future__ import annotations

import copy
from typing import Any

OPERATIONS = {
    "even_parity_append",
    "even_parity_verify",
    "hamming_distance",
    "repetition_encode",
    "repetition_decode",
    "hamming74_encode",
    "hamming74_syndrome",
    "hamming74_correct",
    "gf2_division_remainder",
    "crc_remainder",
}

FIELDS = {
    "even_parity_append": {"bits"},
    "even_parity_verify": {"codeword"},
    "hamming_distance": {"left", "right"},
    "repetition_encode": {"bits", "copies"},
    "repetition_decode": {"codeword", "copies"},
    "hamming74_encode": {"data"},
    "hamming74_syndrome": {"codeword"},
    "hamming74_correct": {"codeword"},
    "gf2_division_remainder": {"dividend", "polynomial"},
    "crc_remainder": {"data", "polynomial"},
}


def _error(name: str) -> dict[str, Any]:
    return {"ok": False, "error": name, "original_success_credit": 0}


def _bits(value: Any, *, width: int | None = None, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not value and not allow_empty) or any(char not in "01" for char in value):
        raise ValueError("invalid_bits")
    if width is not None and len(value) != width:
        raise ValueError("invalid_width")
    return value


def _odd_copies(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1 or value > 9 or value % 2 == 0:
        raise ValueError("copies_must_be_small_positive_odd_integer")
    return value


def _hamming74_encode(data: str) -> str:
    data = _bits(data, width=4)
    d1, d2, d3, d4 = [int(char) for char in data]
    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p4 = d2 ^ d3 ^ d4
    return "".join(str(value) for value in [p1, p2, d1, p4, d2, d3, d4])


def _hamming74_syndrome(codeword: str) -> int:
    codeword = _bits(codeword, width=7)
    values = [int(char) for char in codeword]
    s1 = values[0] ^ values[2] ^ values[4] ^ values[6]
    s2 = values[1] ^ values[2] ^ values[5] ^ values[6]
    s4 = values[3] ^ values[4] ^ values[5] ^ values[6]
    return s1 + 2 * s2 + 4 * s4


def _polynomial(polynomial: Any) -> str:
    polynomial = _bits(polynomial)
    if len(polynomial) < 2 or polynomial[0] != "1" or polynomial[-1] != "1":
        raise ValueError("invalid_polynomial")
    return polynomial


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


def evaluate(operation: str, payload: dict[str, Any]) -> Any:
    if operation == "even_parity_append":
        bits = _bits(payload["bits"])
        parity = bits.count("1") % 2
        return {"codeword": bits + str(parity), "parity_bit": parity, "source_retained": True}
    if operation == "even_parity_verify":
        codeword = _bits(payload["codeword"])
        return {"valid": codeword.count("1") % 2 == 0, "ones": codeword.count("1"), "repair_performed": False}
    if operation == "hamming_distance":
        left = _bits(payload["left"])
        right = _bits(payload["right"], width=len(left))
        positions = [index for index, (a, b) in enumerate(zip(left, right)) if a != b]
        return {"distance": len(positions), "positions": positions}
    if operation == "repetition_encode":
        bits = _bits(payload["bits"])
        copies = _odd_copies(payload["copies"])
        return {"codeword": "".join(char * copies for char in bits), "copies": copies}
    if operation == "repetition_decode":
        codeword = _bits(payload["codeword"])
        copies = _odd_copies(payload["copies"])
        if len(codeword) % copies:
            raise ValueError("incomplete_repetition_group")
        groups = [codeword[index : index + copies] for index in range(0, len(codeword), copies)]
        decoded = "".join("1" if group.count("1") > group.count("0") else "0" for group in groups)
        disagreements = [index for index, group in enumerate(groups) if len(set(group)) > 1]
        return {"decoded": decoded, "disagreement_groups": disagreements, "assumed_model": "strict_odd_majority"}
    if operation == "hamming74_encode":
        return {"codeword": _hamming74_encode(payload["data"]), "layout": "p1_p2_d1_p4_d2_d3_d4"}
    if operation == "hamming74_syndrome":
        syndrome = _hamming74_syndrome(payload["codeword"])
        return {"syndrome": syndrome, "indicated_position": syndrome or None, "repair_performed": False}
    if operation == "hamming74_correct":
        codeword = _bits(payload["codeword"], width=7)
        syndrome = _hamming74_syndrome(codeword)
        corrected = list(codeword)
        if syndrome:
            corrected[syndrome - 1] = "1" if corrected[syndrome - 1] == "0" else "0"
        result = "".join(corrected)
        return {
            "corrected": result,
            "syndrome": syndrome,
            "post_syndrome": _hamming74_syndrome(result),
            "correction_applied": bool(syndrome),
            "assumed_model": "at_most_one_bit_error",
        }
    if operation == "gf2_division_remainder":
        return {"remainder": _gf2_remainder(payload["dividend"], payload["polynomial"]), "field": "GF(2)"}
    if operation == "crc_remainder":
        data = _bits(payload["data"])
        polynomial = _polynomial(payload["polynomial"])
        return {"remainder": _gf2_remainder(data + "0" * (len(polynomial) - 1), polynomial), "cryptographic": False}
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
    return {"ok": True, "operation": operation, "outcome": "completed", "value": value}
