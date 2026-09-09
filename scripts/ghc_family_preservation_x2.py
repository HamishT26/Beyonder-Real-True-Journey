#!/usr/bin/env python3
"""Strict bounded x2 integrity, Merkle, recovery, and reservation operations."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from typing import Any

from ghc_family_preservation_x1 import (
    MAX_DATA_BYTES,
    MAX_INPUT_BYTES,
    ContractError,
    exact_fields,
    hex_bytes,
    integer,
    loads_strict,
)

X2_OPERATIONS = {
    "sha256_digest",
    "digest_match",
    "deterministic_json",
    "json_roundtrip",
    "merkle_root",
    "merkle_proof",
    "merkle_verify",
    "xor_parity",
    "xor_recover",
    "claim_reservation",
}
BOUNDED_SCOPES = {
    "software_fixture",
    "fixity_record",
    "synthetic_chunk",
    "local_test",
    "documentation",
}
PROTECTED_SCOPES = {
    "credential_issuance",
    "public_policy",
    "maori_authority",
    "theory_of_everything",
    "stage20",
}


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def leaf_hash(data: bytes) -> bytes:
    return sha256(b"\x00" + data)


def parent_hash(left: bytes, right: bytes) -> bytes:
    return sha256(b"\x01" + left + right)


def bounded_json(value: Any, *, depth: int = 0, counter: list[int] | None = None) -> None:
    if counter is None:
        counter = [0]
    counter[0] += 1
    if counter[0] > 256 or depth > 8:
        raise ContractError("E_BOUNDS", "JSON structure exceeds declared complexity")
    if value is None or isinstance(value, (str, bool, int)):
        if isinstance(value, str) and len(value.encode("utf-8")) > MAX_DATA_BYTES:
            raise ContractError("E_BOUNDS", "string exceeds declared byte ceiling")
        return
    if isinstance(value, float):
        raise ContractError("E_TYPE", "floating-point values are outside this deterministic profile")
    if isinstance(value, list):
        for item in value:
            bounded_json(item, depth=depth + 1, counter=counter)
        return
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise ContractError("E_TYPE", "map keys must be strings")
        for key, item in value.items():
            bounded_json(key, depth=depth + 1, counter=counter)
            bounded_json(item, depth=depth + 1, counter=counter)
        return
    raise ContractError("E_TYPE", "unsupported JSON value")


def canonical_json(value: Any) -> bytes:
    bounded_json(value)
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    if len(encoded) > MAX_DATA_BYTES:
        raise ContractError("E_BOUNDS", "canonical JSON exceeds byte ceiling")
    return encoded


def merkle_levels(leaves: list[bytes]) -> list[list[bytes]]:
    levels = [[leaf_hash(leaf) for leaf in leaves]]
    while len(levels[-1]) > 1:
        current = levels[-1]
        next_level = []
        for index in range(0, len(current), 2):
            right = current[index + 1] if index + 1 < len(current) else current[index]
            next_level.append(parent_hash(current[index], right))
        levels.append(next_level)
    return levels


def leaves_from_payload(value: Any) -> list[bytes]:
    if not isinstance(value, list) or not 1 <= len(value) <= 64:
        raise ContractError("E_TYPE", "leaves must be a bounded nonempty list")
    leaves = [hex_bytes(item) for item in value]
    if sum(map(len, leaves)) > MAX_DATA_BYTES:
        raise ContractError("E_BOUNDS", "leaf bytes exceed declared ceiling")
    return leaves


def op_sha256_digest(payload: dict[str, Any]) -> str:
    exact_fields(payload, ["data_hex"])
    return sha256(hex_bytes(payload["data_hex"])).hex()


def op_digest_match(payload: dict[str, Any]) -> dict[str, Any]:
    exact_fields(payload, ["data_hex", "declared_sha256"])
    data = hex_bytes(payload["data_hex"])
    declared = payload["declared_sha256"]
    if not isinstance(declared, str) or len(declared) != 64 or declared.lower() != declared or not all(char in "0123456789abcdef" for char in declared):
        raise ContractError("E_ENCODING", "declared SHA-256 must be canonical lowercase hex")
    observed = sha256(data).hex()
    return {"authority_transferred": False, "matches": observed == declared, "observed_sha256": observed}


def op_deterministic_json(payload: dict[str, Any]) -> str:
    exact_fields(payload, ["record"])
    return canonical_json(payload["record"]).hex()


def op_json_roundtrip(payload: dict[str, Any]) -> Any:
    exact_fields(payload, ["encoded_hex"])
    encoded = hex_bytes(payload["encoded_hex"])
    try:
        value = loads_strict(encoded.decode("utf-8"))
    except UnicodeDecodeError as exc:
        raise ContractError("E_ENCODING", "JSON bytes are not UTF-8") from exc
    canonical_json(value)
    return value


def op_merkle_root(payload: dict[str, Any]) -> str:
    exact_fields(payload, ["leaves_hex"])
    return merkle_levels(leaves_from_payload(payload["leaves_hex"]))[-1][0].hex()


def op_merkle_proof(payload: dict[str, Any]) -> dict[str, Any]:
    exact_fields(payload, ["index", "leaves_hex"])
    leaves = leaves_from_payload(payload["leaves_hex"])
    selected = integer(payload["index"], minimum=0, maximum=len(leaves) - 1)
    levels = merkle_levels(leaves)
    proof = []
    index = selected
    for level in levels[:-1]:
        sibling = index - 1 if index % 2 else index + 1
        if sibling >= len(level):
            sibling = index
        proof.append({"side": "left" if sibling < index else "right", "sha256": level[sibling].hex()})
        index //= 2
    return {"proof": proof, "root": levels[-1][0].hex()}


def op_merkle_verify(payload: dict[str, Any]) -> bool:
    exact_fields(payload, ["index", "leaf_hex", "proof", "root"])
    leaf = hex_bytes(payload["leaf_hex"])
    index = integer(payload["index"], minimum=0, maximum=(1 << 31) - 1)
    proof = payload["proof"]
    root = payload["root"]
    if not isinstance(proof, list) or len(proof) > 16:
        raise ContractError("E_TYPE", "proof must be a bounded list")
    if not isinstance(root, str) or len(root) != 64 or root.lower() != root or not all(char in "0123456789abcdef" for char in root):
        raise ContractError("E_ENCODING", "root must be canonical SHA-256 hex")
    current = leaf_hash(leaf)
    for step in proof:
        if not isinstance(step, dict):
            raise ContractError("E_TYPE", "proof step must be an object")
        exact_fields(step, ["sha256", "side"])
        sibling = hex_bytes(step["sha256"], maximum=32)
        if len(sibling) != 32 or step["side"] not in {"left", "right"}:
            raise ContractError("E_ENCODING", "invalid proof step")
        expected_side = "left" if index % 2 else "right"
        if step["side"] != expected_side:
            raise ContractError("E_PROOF", "proof side conflicts with selected index")
        current = parent_hash(sibling, current) if step["side"] == "left" else parent_hash(current, sibling)
        index //= 2
    return current.hex() == root


def equal_shards(value: Any) -> list[bytes]:
    if not isinstance(value, list) or not 2 <= len(value) <= 32:
        raise ContractError("E_TYPE", "shards must be a bounded list")
    shards = [hex_bytes(item) for item in value]
    widths = {len(item) for item in shards}
    if len(widths) != 1 or not next(iter(widths)):
        raise ContractError("E_SHAPE", "shards must have equal positive width")
    return shards


def xor_all(shards: list[bytes]) -> bytes:
    output = bytearray(len(shards[0]))
    for shard in shards:
        for index, value in enumerate(shard):
            output[index] ^= value
    return bytes(output)


def op_xor_parity(payload: dict[str, Any]) -> str:
    exact_fields(payload, ["shards_hex"])
    return xor_all(equal_shards(payload["shards_hex"])).hex()


def op_xor_recover(payload: dict[str, Any]) -> str:
    exact_fields(payload, ["available", "missing_index", "parity_hex", "total_shards"])
    total = integer(payload["total_shards"], minimum=2, maximum=32)
    missing = integer(payload["missing_index"], minimum=0, maximum=total - 1)
    available = payload["available"]
    if not isinstance(available, list) or len(available) != total - 1:
        raise ContractError("E_SHAPE", "exactly one shard must be absent")
    seen = set()
    shards = []
    for row in available:
        if not isinstance(row, dict):
            raise ContractError("E_TYPE", "available shard must be an object")
        exact_fields(row, ["index", "shard_hex"])
        index = integer(row["index"], minimum=0, maximum=total - 1)
        if index == missing or index in seen:
            raise ContractError("E_SHAPE", "shard indexes must be unique and exclude the missing index")
        seen.add(index)
        shards.append(hex_bytes(row["shard_hex"]))
    parity = hex_bytes(payload["parity_hex"])
    if not parity or any(len(shard) != len(parity) for shard in shards):
        raise ContractError("E_SHAPE", "parity and shards must have equal positive width")
    return xor_all([parity, *shards]).hex()


def op_claim_reservation(payload: dict[str, Any]) -> dict[str, Any]:
    exact_fields(payload, ["execute", "requested_scope", "synthetic_evidence"])
    if payload["execute"] is not False or payload["synthetic_evidence"] is not True:
        raise ContractError("E_AUTHORITY", "claim reservation cannot execute")
    scope = payload["requested_scope"]
    if scope in BOUNDED_SCOPES:
        disposition = "represented"
    elif scope in PROTECTED_SCOPES:
        disposition = "exact_gate"
    else:
        raise ContractError("E_SCOPE", "unknown reservation scope")
    return {"disposition": disposition, "executed": False, "scope": scope}


DISPATCH = {
    "sha256_digest": op_sha256_digest,
    "digest_match": op_digest_match,
    "deterministic_json": op_deterministic_json,
    "json_roundtrip": op_json_roundtrip,
    "merkle_root": op_merkle_root,
    "merkle_proof": op_merkle_proof,
    "merkle_verify": op_merkle_verify,
    "xor_parity": op_xor_parity,
    "xor_recover": op_xor_recover,
    "claim_reservation": op_claim_reservation,
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
            raise ContractError("E_OP", "unknown x2 operation")
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
            envelope = evaluate(loads_strict(raw.decode("utf-8")), allowed_operations)
        except ContractError as exc:
            envelope = {"error": exc.code, "ok": False, "value": None}
    sys.stdout.write(json.dumps(envelope, sort_keys=True, separators=(",", ":")) + "\n")
    return 0 if envelope["ok"] else 2
