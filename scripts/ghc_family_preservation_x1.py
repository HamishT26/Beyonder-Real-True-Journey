#!/usr/bin/env python3
"""Strict bounded x1 content-framing and fixity operations for Vesper v689-v7."""

from __future__ import annotations

import base64
import binascii
import copy
import json
import sys
import zlib
from collections.abc import Iterable
from typing import Any

MAX_INPUT_BYTES = 65_536
MAX_DATA_BYTES = 4_096
MAX_CHUNKS = 64
MAX_UNSIGNED = (1 << 64) - 1
MAX_SIGNED = (1 << 63) - 1
X1_OPERATIONS = {
    "unsigned_varint_encode",
    "unsigned_varint_decode",
    "zigzag_encode",
    "zigzag_decode",
    "fixed_chunk_ranges",
    "chunk_reassemble",
    "base32_encode",
    "base32_decode",
    "crc32_envelope",
    "crc32_verify",
}


class ContractError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        if key in output:
            raise ContractError("E_JSON_DUPLICATE", f"duplicate key: {key}")
        output[key] = value
    return output


def loads_strict(text: str) -> Any:
    try:
        return json.loads(
            text,
            object_pairs_hook=strict_object,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ContractError("E_JSON_NONFINITE", f"nonfinite value: {value}")
            ),
        )
    except ContractError:
        raise
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ContractError("E_JSON", "invalid UTF-8 JSON") from exc


def exact_fields(value: dict[str, Any], expected: Iterable[str]) -> None:
    if set(value) != set(expected):
        raise ContractError("E_FIELDS", "unexpected or missing fields")


def integer(value: Any, *, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ContractError("E_TYPE", "expected integer")
    if not minimum <= value <= maximum:
        raise ContractError("E_BOUNDS", "integer outside declared bounds")
    return value


def hex_bytes(value: Any, *, maximum: int = MAX_DATA_BYTES) -> bytes:
    if not isinstance(value, str) or len(value) % 2:
        raise ContractError("E_ENCODING", "expected even-length lowercase hexadecimal")
    if value.lower() != value or not all(char in "0123456789abcdef" for char in value):
        raise ContractError("E_ENCODING", "hexadecimal profile is lowercase canonical")
    if len(value) // 2 > maximum:
        raise ContractError("E_BOUNDS", "byte input exceeds declared ceiling")
    try:
        return bytes.fromhex(value)
    except ValueError as exc:
        raise ContractError("E_ENCODING", "malformed hexadecimal") from exc


def encode_varint(value: int) -> bytes:
    output = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        output.append(byte | (0x80 if value else 0))
        if not value:
            return bytes(output)


def decode_varint(data: bytes) -> int:
    if not 1 <= len(data) <= 10:
        raise ContractError("E_BOUNDS", "varint must contain one through ten bytes")
    value = 0
    shift = 0
    for index, byte in enumerate(data):
        value |= (byte & 0x7F) << shift
        if not byte & 0x80:
            if index != len(data) - 1 or value > MAX_UNSIGNED:
                raise ContractError("E_ENCODING", "noncanonical or overflowing varint")
            if encode_varint(value) != data:
                raise ContractError("E_ENCODING", "nonminimal varint")
            return value
        shift += 7
    raise ContractError("E_ENCODING", "unterminated varint")


def op_unsigned_varint_encode(payload: dict[str, Any]) -> str:
    exact_fields(payload, ["value"])
    return encode_varint(integer(payload["value"], minimum=0, maximum=MAX_UNSIGNED)).hex()


def op_unsigned_varint_decode(payload: dict[str, Any]) -> int:
    exact_fields(payload, ["encoded_hex"])
    return decode_varint(hex_bytes(payload["encoded_hex"], maximum=10))


def op_zigzag_encode(payload: dict[str, Any]) -> int:
    exact_fields(payload, ["value"])
    value = integer(payload["value"], minimum=-MAX_SIGNED, maximum=MAX_SIGNED)
    return value * 2 if value >= 0 else (-value * 2) - 1


def op_zigzag_decode(payload: dict[str, Any]) -> int:
    exact_fields(payload, ["value"])
    value = integer(payload["value"], minimum=0, maximum=MAX_UNSIGNED)
    return value // 2 if value % 2 == 0 else -((value + 1) // 2)


def op_fixed_chunk_ranges(payload: dict[str, Any]) -> list[list[int]]:
    exact_fields(payload, ["length", "width"])
    length = integer(payload["length"], minimum=1, maximum=MAX_DATA_BYTES)
    width = integer(payload["width"], minimum=1, maximum=MAX_DATA_BYTES)
    ranges = [[start, min(start + width, length)] for start in range(0, length, width)]
    if len(ranges) > MAX_CHUNKS:
        raise ContractError("E_BOUNDS", "chunk count exceeds declared ceiling")
    return ranges


def op_chunk_reassemble(payload: dict[str, Any]) -> str:
    exact_fields(payload, ["chunks_hex"])
    chunks = payload["chunks_hex"]
    if not isinstance(chunks, list) or not 1 <= len(chunks) <= MAX_CHUNKS:
        raise ContractError("E_TYPE", "chunks must be a bounded nonempty list")
    decoded = [hex_bytes(chunk) for chunk in chunks]
    if sum(map(len, decoded)) > MAX_DATA_BYTES:
        raise ContractError("E_BOUNDS", "reassembled byte count exceeds ceiling")
    return b"".join(decoded).hex()


def op_base32_encode(payload: dict[str, Any]) -> str:
    exact_fields(payload, ["data_hex"])
    return base64.b32encode(hex_bytes(payload["data_hex"])).decode("ascii").rstrip("=")


def op_base32_decode(payload: dict[str, Any]) -> str:
    exact_fields(payload, ["encoded"])
    encoded = payload["encoded"]
    if not isinstance(encoded, str) or not encoded or len(encoded) > 8192:
        raise ContractError("E_ENCODING", "expected bounded nonempty base32 text")
    if encoded.upper() != encoded or "=" in encoded or not all(char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567" for char in encoded):
        raise ContractError("E_ENCODING", "base32 profile is uppercase and unpadded")
    padded = encoded + "=" * ((8 - len(encoded) % 8) % 8)
    try:
        decoded = base64.b32decode(padded, casefold=False)
    except binascii.Error as exc:
        raise ContractError("E_ENCODING", "malformed base32 text") from exc
    if len(decoded) > MAX_DATA_BYTES or base64.b32encode(decoded).decode("ascii").rstrip("=") != encoded:
        raise ContractError("E_ENCODING", "noncanonical base32 text")
    return decoded.hex()


def op_crc32_envelope(payload: dict[str, Any]) -> dict[str, Any]:
    exact_fields(payload, ["data_hex"])
    data = hex_bytes(payload["data_hex"])
    return {"algorithm": "crc32", "authentication": False, "bytes": len(data), "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"}


def op_crc32_verify(payload: dict[str, Any]) -> dict[str, Any]:
    exact_fields(payload, ["data_hex", "declared_crc32"])
    data = hex_bytes(payload["data_hex"])
    declared = payload["declared_crc32"]
    if not isinstance(declared, str) or not re_full_crc(declared):
        raise ContractError("E_ENCODING", "declared CRC32 must be eight lowercase hex digits")
    observed = f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"
    return {"authentication": False, "matches": observed == declared, "observed_crc32": observed}


def re_full_crc(value: str) -> bool:
    return len(value) == 8 and value.lower() == value and all(char in "0123456789abcdef" for char in value)


DISPATCH = {
    "unsigned_varint_encode": op_unsigned_varint_encode,
    "unsigned_varint_decode": op_unsigned_varint_decode,
    "zigzag_encode": op_zigzag_encode,
    "zigzag_decode": op_zigzag_decode,
    "fixed_chunk_ranges": op_fixed_chunk_ranges,
    "chunk_reassemble": op_chunk_reassemble,
    "base32_encode": op_base32_encode,
    "base32_decode": op_base32_decode,
    "crc32_envelope": op_crc32_envelope,
    "crc32_verify": op_crc32_verify,
}


def evaluate(request: Any, allowed_operations: set[str] | None = None) -> dict[str, Any]:
    try:
        if not isinstance(request, dict):
            raise ContractError("E_TYPE", "request must be an object")
        exact_fields(request, ["op", "payload", "synthetic"])
        if request["synthetic"] is not True:
            raise ContractError("E_SYNTHETIC", "only declared synthetic fixtures are admitted")
        operation = request["op"]
        if not isinstance(operation, str) or operation not in DISPATCH:
            raise ContractError("E_OP", "unknown x1 operation")
        if allowed_operations is not None and operation not in allowed_operations:
            raise ContractError("E_OP", "operation outside runner pair")
        payload = request["payload"]
        if not isinstance(payload, dict):
            raise ContractError("E_TYPE", "payload must be an object")
        before = copy.deepcopy(request)
        value = DISPATCH[operation](payload)
        if request != before:
            raise ContractError("E_MUTATION", "operation mutated its input")
        return {"error": None, "ok": True, "value": value}
    except ContractError as exc:
        return {"error": exc.code, "ok": False, "value": None}


def cli_main(allowed_operations: set[str]) -> int:
    raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        envelope = {"error": "E_BOUNDS", "ok": False, "value": None}
    else:
        try:
            request = loads_strict(raw.decode("utf-8"))
            envelope = evaluate(request, allowed_operations)
        except ContractError as exc:
            envelope = {"error": exc.code, "ok": False, "value": None}
    sys.stdout.write(json.dumps(envelope, sort_keys=True, separators=(",", ":")) + "\n")
    return 0 if envelope["ok"] else 2
