#!/usr/bin/env python3
"""Bounded validation tools for one owner's exact source-to-final Git delta.

The toolkit deliberately avoids repository-wide discovery, sibling worktree
enumeration, and unchanged-history execution.  Every file operation is derived
from an exact Git range or an explicit literal allowlist.
"""

from __future__ import annotations

import argparse
import ast
import base64
import binascii
from copy import deepcopy
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import unicodedata
from ast import parse as parse_python_ast
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from urllib.parse import urlsplit


SCHEMA = "ghc.family.owner-delta-toolkit.v2"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
ALLOWED_BLOB_MODES = {"100644", "100755"}
WINDOWS_RESERVED_COMPONENTS = {
    "con",
    "prn",
    "aux",
    "nul",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}
DECLARED_CLOCK_SOURCES = {
    "caller_supplied_utc",
    "wall_clock_observation",
    "monotonic_duration",
}
DECLARED_DIGEST_ALGORITHMS = {"sha256"}
DECLARED_MEDIA_TYPES = {
    "application/vnd.in-toto+json",
    "application/vnd.ghc.synthetic-condition+json",
}
DECLARED_PREDICATE_TYPES = {
    "https://example.invalid/ghc/synthetic-condition/v1",
}
JSON_NUMBER_LEXEME = re.compile(
    r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\Z"
)
URI_UNRESERVED = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
)
BOUNDED_CONFUSABLE_MAP = str.maketrans(
    {
        "Α": "A",
        "А": "A",
        "Β": "B",
        "В": "B",
        "Ε": "E",
        "Е": "E",
        "Ι": "I",
        "І": "I",
        "Κ": "K",
        "К": "K",
        "Μ": "M",
        "М": "M",
        "Ν": "N",
        "О": "O",
        "Ρ": "P",
        "Р": "P",
        "Τ": "T",
        "Т": "T",
        "Χ": "X",
        "Х": "X",
        "Υ": "Y",
    }
)
DISALLOWED_BIDI = {
    "LRE", "RLE", "LRO", "RLO", "PDF", "LRI", "RLI", "FSI", "PDI",
}
UNSAFE_LINK_SCHEMES = {"app", "codex", "data", "file", "javascript", "vscode"}
PRIVATE_PATTERNS = {
    "private_absolute_path": re.compile(
        r"(?i)(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/(?:home|Users)/)"
    ),
    "raw_uuid_or_task_identifier": re.compile(
        r"(?i)(?:\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b|\"(?:task|thread|session|agent)_id\"\s*:)"
    ),
    "credential_or_private_key": re.compile(
        r"(?i)(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bAKIA[0-9A-Z]{16}\b|\"(?:password|api_key|access_token|resume_token)\"\s*:\s*\"(?!\[REDACTED_SECRET\]))"
    ),
    "private_route": re.compile(
        r"(?i)(?:codex" r"://|vscode" r"://|app" r"://connector_[0-9a-f]+)"
    ),
    "raw_transcript_or_app_state": re.compile(
        r"(?i)\"(?:raw_transcript|session_stream|private_app_state|browser_route)\"\s*:"
    ),
}
SECURITY_PATTERNS = {
    "dynamic_eval": re.compile(r"(?m)^\s*(?:eval|exec)\s*\("),
    "unsafe_pickle_load": re.compile(r"\bpickle\.loads?\s*\("),
    "shell_true": re.compile(r"\bshell\s*=\s*True\b"),
    "destructive_git": re.compile(r"git\s+(?:reset\s+--hard|push\s+--force)"),
    "recursive_delete": re.compile(
        r"(?i)(?:rm\s+-" r"rf|Remove-" r"Item\b[^\n]*-Recurse)"
    ),
}
REMOTE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")


class DeltaError(RuntimeError):
    """Raised when an exact-delta contract is violated."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    """Return a deterministic UTF-8 JSON encoding for bounded receipt commitments."""
    try:
        rendered = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    except (TypeError, ValueError) as exc:
        raise DeltaError(f"value is not canonically JSON encodable: {exc}") from exc
    return rendered.encode("utf-8")


def canonical_json_sha256(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def canonical_owner(value: str) -> str:
    owner = value.strip()
    if not owner:
        raise DeltaError("canonical owner must be explicit")
    return owner


def strict_json_loads(raw: bytes | str, label: str = "JSON") -> Any:
    """Decode UTF-8 JSON while refusing duplicate object keys."""
    if isinstance(raw, bytes):
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise DeltaError(f"{label} is not UTF-8: {exc}") from exc
    else:
        text = raw

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        duplicates: list[str] = []
        for key, value in pairs:
            if key in result:
                duplicates.append(key)
            else:
                result[key] = value
        if duplicates:
            raise DeltaError(f"{label} contains duplicate object keys: {sorted(set(duplicates))}")
        return result

    try:
        return json.loads(text, object_pairs_hook=reject_duplicates)
    except json.JSONDecodeError as exc:
        raise DeltaError(f"{label} parse failed: {exc}") from exc


def normalize_relative(raw: str) -> str:
    candidate = raw.replace("\\", "/")
    if re.match(r"^[A-Za-z]:", candidate):
        raise DeltaError(f"absolute drive path rejected: {raw}")
    path = PurePosixPath(candidate)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise DeltaError(f"non-literal repository-relative path rejected: {raw}")
    return path.as_posix()


def path_security_record(raw: str) -> dict[str, Any]:
    path = normalize_relative(raw)
    nfc = unicodedata.normalize("NFC", path)
    disallowed: list[dict[str, str]] = []
    for character in path:
        category = unicodedata.category(character)
        bidi = unicodedata.bidirectional(character)
        if category == "Cc" or bidi in DISALLOWED_BIDI:
            disallowed.append(
                {
                    "codepoint": f"U+{ord(character):04X}",
                    "category": category,
                    "bidi": bidi or "NONE",
                }
            )
    return {
        "path": path,
        "nfc": nfc,
        "casefold_nfc": nfc.casefold(),
        "already_nfc": path == nfc,
        "disallowed_controls": disallowed,
        "valid": path == nfc and not disallowed,
    }


def audit_paths(paths: Iterable[str]) -> dict[str, Any]:
    records = [path_security_record(path) for path in ensure_unique(paths, "path-audit")]
    nfc_groups: dict[str, list[str]] = {}
    casefold_groups: dict[str, list[str]] = {}
    for record in records:
        nfc_groups.setdefault(record["nfc"], []).append(record["path"])
        casefold_groups.setdefault(record["casefold_nfc"], []).append(record["path"])
    nfc_collisions = [sorted(group) for group in nfc_groups.values() if len(group) > 1]
    casefold_collisions = [sorted(group) for group in casefold_groups.values() if len(group) > 1]
    issues = [record["path"] for record in records if not record["valid"]]
    return {
        "records": records,
        "nfc_collisions": sorted(nfc_collisions),
        "casefold_collisions": sorted(casefold_collisions),
        "invalid_paths": sorted(issues),
        "valid": not issues and not nfc_collisions and not casefold_collisions,
        "boundary": "Exact allowlist Unicode and collision review only; not exhaustive cross-platform path assurance.",
    }


def validate_windows_component(raw: str) -> str:
    """Validate one bounded Windows-compatible lexical path component."""

    if not isinstance(raw, str) or not raw:
        raise DeltaError("path component must be a nonempty string")
    if raw in {".", ".."}:
        raise DeltaError("dot path components are not allowed")
    if raw.endswith((".", " ")):
        raise DeltaError("trailing dot or space is not allowed")
    if any(ord(char) < 32 or char in {"\x00", "/", "\\"} for char in raw):
        raise DeltaError("control or separator is not allowed in a component")
    base = raw.split(".", 1)[0].casefold()
    if base in WINDOWS_RESERVED_COMPONENTS:
        raise DeltaError("Windows reserved device component is not allowed")
    return raw


def normalize_archive_member(raw: str) -> str:
    """Normalize one synthetic archive member and refuse lexical traversal."""

    if not isinstance(raw, str) or not raw:
        raise DeltaError("archive member must be a nonempty string")
    if "\x00" in raw or any(ord(char) < 32 for char in raw):
        raise DeltaError("archive member contains a control character")
    value = raw.replace("\\", "/")
    if value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        raise DeltaError("absolute or drive-qualified archive member is not allowed")
    components: list[str] = []
    for component in value.split("/"):
        if component in {"", "."}:
            continue
        if component == "..":
            raise DeltaError("parent traversal archive member is not allowed")
        components.append(validate_windows_component(component))
    if not components:
        raise DeltaError("archive member normalizes to an empty path")
    return "/".join(components)


def bounded_confusable_skeleton(value: str) -> str:
    """Return a deliberately bounded review skeleton, never an exhaustive one."""

    if not isinstance(value, str) or not value:
        raise DeltaError("confusable-review value must be a nonempty string")
    normalized = unicodedata.normalize("NFKC", value)
    return normalized.translate(BOUNDED_CONFUSABLE_MAP).casefold()


def validate_dsse_envelope(value: Any) -> dict[str, Any]:
    """Validate synthetic DSSE envelope shape without verifying signatures."""

    if not isinstance(value, dict):
        raise DeltaError("DSSE envelope must be an object")
    payload_type = value.get("payloadType")
    payload = value.get("payload")
    signatures = value.get("signatures")
    if not isinstance(payload_type, str) or not payload_type.strip():
        raise DeltaError("DSSE payloadType must be a nonempty string")
    if not isinstance(payload, str):
        raise DeltaError("DSSE payload must be base64 text")
    try:
        decoded_payload = base64.b64decode(payload, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise DeltaError("DSSE payload is not strict base64") from exc
    if not isinstance(signatures, list) or not signatures:
        raise DeltaError("DSSE signatures must be a nonempty array")
    key_ids: list[str] = []
    for signature in signatures:
        if not isinstance(signature, dict):
            raise DeltaError("DSSE signature must be an object")
        key_id = signature.get("keyid")
        encoded_signature = signature.get("sig")
        if not isinstance(key_id, str) or not key_id.strip():
            raise DeltaError("DSSE keyid must be a nonempty string")
        if not isinstance(encoded_signature, str):
            raise DeltaError("DSSE sig must be base64 text")
        try:
            base64.b64decode(encoded_signature, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise DeltaError("DSSE sig is not strict base64") from exc
        key_ids.append(key_id)
    ensure_unique(key_ids, "DSSE key identifiers")
    return {
        "payload_type": payload_type,
        "payload_sha256": sha256_bytes(decoded_payload),
        "signature_count": len(signatures),
        "signature_verified": False,
        "valid": True,
    }


def validate_intoto_statement(value: Any) -> dict[str, Any]:
    """Validate a bounded in-toto Statement v1 shape without provenance proof."""

    if not isinstance(value, dict):
        raise DeltaError("in-toto statement must be an object")
    if value.get("_type") != "https://in-toto.io/Statement/v1":
        raise DeltaError("in-toto statement type is not Statement v1")
    subjects = value.get("subject")
    if not isinstance(subjects, list) or not subjects:
        raise DeltaError("in-toto subject must be a nonempty array")
    names: list[str] = []
    for subject in subjects:
        if not isinstance(subject, dict):
            raise DeltaError("in-toto subject must be an object")
        name = subject.get("name")
        digest = subject.get("digest")
        if not isinstance(name, str) or not name:
            raise DeltaError("in-toto subject name must be nonempty")
        if not isinstance(digest, dict) or not digest:
            raise DeltaError("in-toto subject digest must be a nonempty object")
        for algorithm, encoded in digest.items():
            if not isinstance(algorithm, str) or not algorithm:
                raise DeltaError("in-toto digest algorithm must be nonempty")
            if not isinstance(encoded, str) or not re.fullmatch(r"[0-9a-fA-F]+", encoded):
                raise DeltaError("in-toto digest value must be nonempty hexadecimal text")
        names.append(name)
    ensure_unique(names, "in-toto subject names")
    predicate_type = value.get("predicateType")
    if not isinstance(predicate_type, str) or not predicate_type.strip():
        raise DeltaError("in-toto predicateType must be nonempty")
    if not isinstance(value.get("predicate"), dict):
        raise DeltaError("in-toto predicate must be an object")
    return {
        "statement_type": value["_type"],
        "subject_count": len(subjects),
        "predicate_type": predicate_type,
        "provenance_verified": False,
        "valid": True,
    }


def validate_clock_source(value: str) -> str:
    if not isinstance(value, str) or value.startswith("-"):
        raise DeltaError("clock source must be a literal declared label")
    if value not in DECLARED_CLOCK_SOURCES:
        raise DeltaError("unknown clock source")
    return value


def locale_invariant_order(values: Iterable[str]) -> list[str]:
    records = list(values)
    if not all(isinstance(value, str) for value in records):
        raise DeltaError("ordered identifiers must all be strings")
    return sorted(records)


def semantic_content_sha256(
    value: dict[str, Any],
    observation_fields: Iterable[str] = ("observed_at_utc", "observed_at_nz"),
) -> str:
    if not isinstance(value, dict):
        raise DeltaError("semantic commitment input must be an object")
    excluded = set(observation_fields)
    semantic = {key: item for key, item in value.items() if key not in excluded}
    return canonical_json_sha256(semantic)


def validate_executable_modes(
    records: Iterable[dict[str, Any]],
    executable_allowlist: Iterable[str],
) -> dict[str, Any]:
    rows = list(records)
    allowed = set(ensure_unique(executable_allowlist, "executable allowlist paths"))
    observed: set[str] = set()
    paths: list[str] = []
    for record in rows:
        if not isinstance(record, dict):
            raise DeltaError("mode record must be an object")
        path = normalize_relative(record.get("path", ""))
        mode = record.get("mode")
        if mode not in ALLOWED_BLOB_MODES:
            raise DeltaError("mode record contains an unsupported mode")
        if mode == "100755":
            if path not in allowed:
                raise DeltaError("executable path is not allowlisted")
            observed.add(path)
        elif path in allowed:
            raise DeltaError("allowlisted executable path is not mode 100755")
        paths.append(path)
    ensure_unique(paths, "mode record paths")
    if observed != allowed:
        raise DeltaError("executable allowlist does not match observed executables")
    return {
        "record_count": len(rows),
        "executable_count": len(observed),
        "valid": True,
    }


def decode_utf8_strict(raw: bytes, label: str = "text blob") -> str:
    if not isinstance(raw, bytes):
        raise DeltaError(f"{label} must be bytes")
    try:
        return raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise DeltaError(f"{label} is not strict UTF-8") from exc


def validate_digest_algorithm(value: str) -> str:
    if not isinstance(value, str) or value.startswith("-"):
        raise DeltaError("digest algorithm must be a literal label")
    normalized = value.strip().casefold()
    if normalized not in DECLARED_DIGEST_ALGORITHMS:
        raise DeltaError("unknown digest algorithm")
    return normalized


def normalize_unique_archive_members(values: Iterable[str]) -> list[str]:
    original = list(values)
    normalized = [normalize_archive_member(value) for value in original]
    duplicates = [name for name, count in Counter(normalized).items() if count > 1]
    if duplicates:
        raise DeltaError(f"duplicate normalized archive members: {sorted(duplicates)}")
    return normalized


def frame_merkle_leaf(entry: dict[str, Any]) -> bytes:
    """Frame one exact leaf with field tags and unsigned 64-bit lengths."""

    if not isinstance(entry, dict):
        raise DeltaError("Merkle leaf entry must be an object")
    fields = ("path", "mode", "git_blob", "bytes", "sha256")
    framed = bytearray(b"GHC-OWNER-DELTA-LEAF-V2\x00")
    for field in fields:
        if field not in entry:
            raise DeltaError(f"Merkle leaf missing field: {field}")
        raw = str(entry[field]).encode("utf-8")
        tag = field.encode("ascii")
        framed.extend(len(tag).to_bytes(2, "big"))
        framed.extend(tag)
        framed.extend(len(raw).to_bytes(8, "big"))
        framed.extend(raw)
    return bytes(framed)


def validate_decompression_budget(
    compressed_bytes: int,
    expanded_bytes: int,
    maximum_expanded_bytes: int,
    maximum_ratio: int,
) -> dict[str, Any]:
    """Validate synthetic size metadata without decoding or allocating output."""

    values = (
        compressed_bytes,
        expanded_bytes,
        maximum_expanded_bytes,
        maximum_ratio,
    )
    if any(isinstance(value, bool) or not isinstance(value, int) for value in values):
        raise DeltaError("decompression budget values must be integers")
    if compressed_bytes <= 0:
        raise DeltaError("compressed size must be positive")
    if expanded_bytes < 0 or maximum_expanded_bytes < 0:
        raise DeltaError("expanded sizes must be nonnegative")
    if maximum_ratio < 1:
        raise DeltaError("maximum decompression ratio must be at least one")
    if expanded_bytes > maximum_expanded_bytes:
        raise DeltaError("expanded size exceeds declared budget")
    if expanded_bytes > compressed_bytes * maximum_ratio:
        raise DeltaError("declared decompression ratio exceeds budget")
    return {
        "compressed_bytes": compressed_bytes,
        "expanded_bytes": expanded_bytes,
        "maximum_expanded_bytes": maximum_expanded_bytes,
        "maximum_ratio": maximum_ratio,
        "decoder_invoked": False,
        "valid": True,
    }


def sparse_size_record(logical_bytes: int, stored_bytes: int) -> dict[str, Any]:
    """Represent logical and stored size without creating a sparse file."""

    if any(
        isinstance(value, bool) or not isinstance(value, int)
        for value in (logical_bytes, stored_bytes)
    ):
        raise DeltaError("sparse size values must be integers")
    if logical_bytes < 0 or stored_bytes < 0:
        raise DeltaError("sparse size values must be nonnegative")
    if stored_bytes > logical_bytes:
        raise DeltaError("stored size cannot exceed logical size")
    return {
        "logical_bytes": logical_bytes,
        "stored_bytes": stored_bytes,
        "sparse": stored_bytes < logical_bytes,
        "file_materialized": False,
        "valid": True,
    }


def validate_archive_entry_kind(kind: str) -> str:
    """Allow only non-link synthetic archive entry kinds."""

    if not isinstance(kind, str) or not kind or kind.startswith("-"):
        raise DeltaError("archive entry kind must be a literal label")
    normalized = kind.strip().casefold()
    if normalized in {"symlink", "hardlink"}:
        raise DeltaError("archive link metadata is not allowed")
    if normalized not in {"regular_file", "directory"}:
        raise DeltaError("unknown archive entry kind")
    return normalized


def validate_windows_archive_reference(raw: str) -> str:
    """Refuse UNC, device, extended, rooted, and drive-qualified forms."""

    if not isinstance(raw, str) or not raw:
        raise DeltaError("Windows archive reference must be nonempty text")
    lowered = raw.casefold()
    if raw.startswith(("\\\\", "//", "\\", "/")):
        raise DeltaError("rooted or UNC archive reference is not allowed")
    if lowered.startswith(("\\\\?\\", "\\\\.\\", "//?/", "//./")):
        raise DeltaError("device or extended Windows path is not allowed")
    if re.match(r"^[A-Za-z]:", raw):
        raise DeltaError("drive-qualified Windows path is not allowed")
    return normalize_archive_member(raw)


def normalize_uri_member_reference(raw: str) -> str:
    """Normalize one URI-shaped member path once, without dereferencing it."""

    if not isinstance(raw, str) or not raw:
        raise DeltaError("URI member reference must be nonempty text")
    if any(char.isspace() or ord(char) < 32 for char in raw):
        raise DeltaError("URI member reference contains whitespace or control data")
    split = urlsplit(raw)
    if split.scheme or split.netloc or split.query or split.fragment:
        raise DeltaError("URI member reference must contain a relative path only")
    value = split.path
    output: list[str] = []
    index = 0
    while index < len(value):
        char = value[index]
        if char != "%":
            output.append(char)
            index += 1
            continue
        if index + 2 >= len(value) or not re.fullmatch(
            r"[0-9A-Fa-f]{2}", value[index + 1 : index + 3]
        ):
            raise DeltaError("URI member reference contains malformed percent encoding")
        octet = int(value[index + 1 : index + 3], 16)
        decoded = chr(octet)
        if decoded in URI_UNRESERVED:
            output.append(decoded)
        else:
            output.append(f"%{octet:02X}")
        index += 3
    return validate_windows_archive_reference("".join(output))


def validate_json_number_lexeme(
    raw: str,
    maximum_characters: int = 64,
    maximum_absolute_exponent: int = 308,
) -> str:
    """Validate a bounded JSON number spelling before numeric conversion."""

    if not isinstance(raw, str) or not raw:
        raise DeltaError("JSON number lexeme must be nonempty text")
    if len(raw) > maximum_characters:
        raise DeltaError("JSON number lexeme exceeds the declared character budget")
    if not JSON_NUMBER_LEXEME.fullmatch(raw):
        raise DeltaError("invalid JSON number lexeme")
    exponent = re.search(r"[eE]([+-]?[0-9]+)\Z", raw)
    if exponent and abs(int(exponent.group(1))) > maximum_absolute_exponent:
        raise DeltaError("JSON number exponent exceeds the declared budget")
    return raw


def validate_schema_finite_number(value: int | float) -> int | float:
    """Refuse booleans, nonfinite floats, and schema-forbidden negative zero."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise DeltaError("schema number must be an integer or float")
    if isinstance(value, float):
        if not math.isfinite(value):
            raise DeltaError("nonfinite schema number is not allowed")
        if value == 0.0 and math.copysign(1.0, value) < 0:
            raise DeltaError("negative zero is not allowed by this schema")
    return value


def validate_media_type(
    value: str,
    allowlist: Iterable[str] = DECLARED_MEDIA_TYPES,
) -> str:
    """Apply a closed media-type allowlist without opening any payload."""

    if not isinstance(value, str) or not value or value.startswith("-"):
        raise DeltaError("media type must be a literal label")
    normalized = value.strip().casefold()
    if ";" in normalized or not re.fullmatch(
        r"[a-z0-9][a-z0-9!#$&^_.+-]*/[a-z0-9][a-z0-9!#$&^_.+-]*",
        normalized,
    ):
        raise DeltaError("media type is not in the bounded parameter-free form")
    allowed = set(ensure_unique((item.casefold() for item in allowlist), "media type"))
    if normalized not in allowed:
        raise DeltaError("media type is not declared")
    return normalized


def validate_subject_digest_agreement(
    subjects: Iterable[dict[str, Any]],
    declared_algorithm: str = "sha256",
) -> dict[str, Any]:
    """Validate synthetic subject digests without establishing provenance."""

    algorithm = validate_digest_algorithm(declared_algorithm)
    rows = list(subjects)
    if not rows:
        raise DeltaError("attestation subjects must be nonempty")
    names: list[str] = []
    expected_length = 64 if algorithm == "sha256" else 0
    for row in rows:
        if not isinstance(row, dict):
            raise DeltaError("attestation subject must be an object")
        name = row.get("name")
        digest = row.get("digest")
        if not isinstance(name, str) or not name:
            raise DeltaError("attestation subject name must be nonempty")
        if not isinstance(digest, dict) or set(digest) != {algorithm}:
            raise DeltaError("attestation digest algorithm disagrees with policy")
        encoded = digest[algorithm]
        if not isinstance(encoded, str) or not re.fullmatch(
            rf"[0-9a-f]{{{expected_length}}}", encoded
        ):
            raise DeltaError("attestation digest has the wrong width or encoding")
        names.append(name)
    ensure_unique(names, "attestation subject names")
    return {
        "subject_count": len(rows),
        "algorithm": algorithm,
        "provenance_verified": False,
        "valid": True,
    }


def dsse_pae(payload_type: str, payload: bytes) -> bytes:
    """Build a bounded ASCII-type DSSE PAE vector without signing it."""

    if not isinstance(payload_type, str) or not payload_type:
        raise DeltaError("DSSE payload type must be nonempty text")
    try:
        encoded_type = payload_type.encode("ascii", errors="strict")
    except UnicodeEncodeError as exc:
        raise DeltaError("bounded DSSE payload type must be ASCII") from exc
    if any(byte < 0x21 or byte > 0x7E for byte in encoded_type):
        raise DeltaError("bounded DSSE payload type contains whitespace or control data")
    if not isinstance(payload, bytes):
        raise DeltaError("DSSE payload must be bytes")
    return (
        b"DSSEv1 "
        + str(len(encoded_type)).encode("ascii")
        + b" "
        + encoded_type
        + b" "
        + str(len(payload)).encode("ascii")
        + b" "
        + payload
    )


def validate_predicate_type(
    value: str,
    allowlist: Iterable[str] = DECLARED_PREDICATE_TYPES,
) -> str:
    """Reserve exact synthetic in-toto predicate versions."""

    if not isinstance(value, str) or not value or value.startswith("-"):
        raise DeltaError("predicate type must be a literal URI")
    split = urlsplit(value)
    if split.scheme != "https" or not split.netloc or split.fragment:
        raise DeltaError("predicate type must be an absolute HTTPS URI")
    allowed = set(ensure_unique(allowlist, "predicate type"))
    if value not in allowed:
        raise DeltaError("predicate type is not declared")
    return value


def clock_separation_record(
    previous_wall_seconds: int | float,
    current_wall_seconds: int | float,
    monotonic_elapsed_seconds: int | float,
) -> dict[str, Any]:
    """Keep wall-clock rollback detection separate from elapsed duration."""

    values = (
        previous_wall_seconds,
        current_wall_seconds,
        monotonic_elapsed_seconds,
    )
    for value in values:
        validate_schema_finite_number(value)
    if monotonic_elapsed_seconds < 0:
        raise DeltaError("monotonic elapsed duration must be nonnegative")
    return {
        "wall_clock_rollback_detected": current_wall_seconds < previous_wall_seconds,
        "monotonic_elapsed_seconds": monotonic_elapsed_seconds,
        "trusted_time": False,
        "valid": True,
    }


def normalize_rfc3339_utc(value: str) -> str:
    """Normalize a strict explicit-offset timestamp without civil-time inference."""

    if not isinstance(value, str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?(?:Z|[+-][0-9]{2}:[0-9]{2})",
        value,
    ):
        raise DeltaError("timestamp is not in the bounded RFC 3339 form")
    if value.endswith("-00:00"):
        raise DeltaError("unknown local offset is outside the bounded UTC normalizer")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
    except ValueError as exc:
        raise DeltaError("timestamp cannot be parsed") from exc
    if parsed.utcoffset() is None:
        raise DeltaError("timestamp lacks an explicit offset")
    normalized = parsed.astimezone(timezone.utc).isoformat()
    return normalized.replace("+00:00", "Z")


def normalize_json_pointer(pointer: str) -> str:
    """Canonicalize a bounded non-root JSON Pointer target."""

    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise DeltaError("JSON Pointer target must be a non-root absolute pointer")
    normalized_tokens: list[str] = []
    for token in pointer[1:].split("/"):
        decoded: list[str] = []
        index = 0
        while index < len(token):
            if token[index] != "~":
                decoded.append(token[index])
                index += 1
                continue
            if index + 1 >= len(token) or token[index + 1] not in {"0", "1"}:
                raise DeltaError("JSON Pointer contains an invalid escape")
            decoded.append("~" if token[index + 1] == "0" else "/")
            index += 2
        canonical = "".join(decoded).replace("~", "~0").replace("/", "~1")
        normalized_tokens.append(canonical)
    return "/" + "/".join(normalized_tokens)


def validate_unique_json_pointer_targets(values: Iterable[str]) -> list[str]:
    normalized = [normalize_json_pointer(value) for value in values]
    if len(normalized) != len(set(normalized)):
        raise DeltaError("duplicate normalized JSON Pointer targets")
    return normalized


def _require_nonnegative_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise DeltaError(f"{label} must be an integer")
    if value < 0:
        raise DeltaError(f"{label} must be nonnegative")
    return value


def validate_byte_order(value: str) -> str:
    """Require an explicit standard byte order without parsing any payload."""

    if not isinstance(value, str) or not value or value != value.strip():
        raise DeltaError("byte order must be an exact nonempty declaration")
    normalized = value.casefold()
    if normalized not in {"little", "big", "network"}:
        raise DeltaError("byte order must be little, big, or network")
    return normalized


def normalize_permission_mode(value: int, allowed_mask: int = 0o777) -> dict[str, Any]:
    """Normalize symbolic permission bits without touching a filesystem."""

    mode = _require_nonnegative_int(value, "permission mode")
    mask = _require_nonnegative_int(allowed_mask, "permission mask")
    if mask > 0o7777:
        raise DeltaError("permission mask exceeds the bounded symbolic surface")
    if mode & ~mask:
        raise DeltaError("permission mode contains bits outside the declared mask")
    return {
        "mode": mode,
        "octal": f"{mode:04o}",
        "allowed_mask": mask,
        "filesystem_mutated": False,
        "valid": True,
    }


def validate_nested_resource_budget(
    nodes: Iterable[dict[str, Any]],
    maximum_depth: int,
    maximum_members: int,
    maximum_total_bytes: int,
) -> dict[str, Any]:
    """Aggregate bounded synthetic declarations without allocating resources."""

    depth_limit = _require_nonnegative_int(maximum_depth, "maximum depth")
    member_limit = _require_nonnegative_int(maximum_members, "maximum members")
    byte_limit = _require_nonnegative_int(maximum_total_bytes, "maximum total bytes")
    if depth_limit < 1 or member_limit < 1:
        raise DeltaError("nested resource depth and member limits must be positive")
    rows = list(nodes)
    if not rows:
        raise DeltaError("nested resource declarations must be nonempty")
    if len(rows) > member_limit:
        raise DeltaError("nested resource member count exceeds budget")
    total = 0
    observed_depth = 0
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"depth", "declared_bytes"}:
            raise DeltaError("nested resource row must contain depth and declared_bytes")
        depth = _require_nonnegative_int(row["depth"], "resource depth")
        declared = _require_nonnegative_int(
            row["declared_bytes"], "declared resource bytes"
        )
        if depth < 1 or depth > depth_limit:
            raise DeltaError("nested resource depth exceeds budget")
        if declared > byte_limit - total:
            raise DeltaError("nested resource total exceeds budget")
        total += declared
        observed_depth = max(observed_depth, depth)
    return {
        "member_count": len(rows),
        "maximum_depth_observed": observed_depth,
        "total_declared_bytes": total,
        "resources_allocated": False,
        "valid": True,
    }


def checked_size_product(left: int, right: int, maximum: int) -> int:
    """Multiply two declared dimensions only when the product fits a ceiling."""

    left_value = _require_nonnegative_int(left, "left size factor")
    right_value = _require_nonnegative_int(right, "right size factor")
    limit = _require_nonnegative_int(maximum, "maximum size product")
    if left_value and right_value > limit // left_value:
        raise DeltaError("declared size product exceeds the configured ceiling")
    return left_value * right_value


def validate_uri_member_components(raw: str) -> str:
    """Refuse external or ambiguous URI components without dereferencing them."""

    if not isinstance(raw, str) or not raw or "?" in raw or "#" in raw:
        raise DeltaError("URI member reference contains a query or fragment delimiter")
    split = urlsplit(raw)
    if split.scheme or split.netloc or split.query or split.fragment:
        raise DeltaError("URI member reference must contain a relative path only")
    for match in re.finditer(r"%([0-9A-Fa-f]{2})", raw):
        if int(match.group(1), 16) in {0x2F, 0x5C}:
            raise DeltaError("URI member reference contains an encoded separator")
    return normalize_uri_member_reference(raw)


def parse_media_type_parameters(
    raw: str,
    allowed_media_types: Iterable[str] = DECLARED_MEDIA_TYPES,
    allowed_charsets: Iterable[str] = ("utf-8",),
    maximum_parameters: int = 4,
) -> dict[str, Any]:
    """Parse a closed, token-only media-type parameter subset without content IO."""

    if not isinstance(raw, str) or not raw or len(raw) > 512:
        raise DeltaError("media type declaration is empty or over budget")
    maximum = _require_nonnegative_int(maximum_parameters, "maximum parameters")
    if maximum < 1:
        raise DeltaError("maximum parameters must be positive")
    parts = [part.strip() for part in raw.split(";")]
    if not parts[0] or any(not part for part in parts[1:]):
        raise DeltaError("media type contains an empty component")
    media_type = parts[0].casefold()
    allowed_types = {item.casefold() for item in allowed_media_types}
    if media_type not in allowed_types:
        raise DeltaError("media type is not declared")
    if len(parts) - 1 > maximum:
        raise DeltaError("media type parameter count exceeds budget")
    token = re.compile(r"[A-Za-z0-9!#$&^_.+:-]+\Z")
    parameters: dict[str, str] = {}
    for part in parts[1:]:
        name, separator, value = part.partition("=")
        if not separator or not token.fullmatch(name) or not token.fullmatch(value):
            raise DeltaError("media type parameter is outside the bounded token grammar")
        normalized_name = name.casefold()
        if normalized_name not in {"charset", "profile", "version"}:
            raise DeltaError("media type parameter name is not declared")
        if normalized_name in parameters:
            raise DeltaError("duplicate media type parameter")
        normalized_value = value.casefold() if normalized_name == "charset" else value
        if normalized_name == "charset" and normalized_value not in {
            item.casefold() for item in allowed_charsets
        }:
            raise DeltaError("media type charset is not declared")
        parameters[normalized_name] = normalized_value
    return {
        "media_type": media_type,
        "parameters": dict(sorted(parameters.items())),
        "content_opened": False,
        "valid": True,
    }


def validate_digest_policy(
    digests: dict[str, str],
    required_algorithms: Iterable[str] = ("sha256",),
    allowed_algorithms: Iterable[str] = ("sha256", "sha512"),
    reserved_algorithms: Iterable[str] = ("sha1", "md5"),
) -> dict[str, Any]:
    """Validate digest-map shape without computing or trusting any digest."""

    if not isinstance(digests, dict) or not digests:
        raise DeltaError("digest policy input must be a nonempty object")
    required = set(ensure_unique(required_algorithms, "required digest algorithms"))
    allowed = set(ensure_unique(allowed_algorithms, "allowed digest algorithms"))
    reserved = set(ensure_unique(reserved_algorithms, "reserved digest algorithms"))
    if not required <= allowed or allowed & reserved:
        raise DeltaError("digest policy declarations conflict")
    widths = {"sha256": 64, "sha512": 128}
    observed: set[str] = set()
    for algorithm, encoded in digests.items():
        if not isinstance(algorithm, str) or algorithm != algorithm.casefold():
            raise DeltaError("digest algorithm labels must be exact lower-case text")
        if algorithm in reserved or algorithm not in allowed or algorithm not in widths:
            raise DeltaError("digest algorithm is reserved or undeclared")
        if not isinstance(encoded, str) or not re.fullmatch(
            rf"[0-9a-f]{{{widths[algorithm]}}}", encoded
        ):
            raise DeltaError("digest value has the wrong width or encoding")
        observed.add(algorithm)
    if not required <= observed:
        raise DeltaError("required digest algorithm is absent")
    return {
        "algorithms": sorted(observed),
        "cryptographic_validity_verified": False,
        "provenance_verified": False,
        "valid": True,
    }


def validate_dsse_payload_type(value: str, maximum_bytes: int = 128) -> str:
    """Validate a bounded visible-ASCII DSSE payload type without PAE or signing."""

    maximum = _require_nonnegative_int(maximum_bytes, "maximum payload-type bytes")
    if maximum < 1 or not isinstance(value, str) or not value:
        raise DeltaError("DSSE payload type must be nonempty bounded text")
    try:
        encoded = value.encode("ascii", errors="strict")
    except UnicodeEncodeError as exc:
        raise DeltaError("DSSE payload type must be ASCII") from exc
    if len(encoded) > maximum or any(byte < 0x21 or byte > 0x7E for byte in encoded):
        raise DeltaError("DSSE payload type is over budget or contains whitespace/control data")
    return value


def validate_unique_attestation_subject_names(
    values: Iterable[str],
    maximum_items: int = 64,
    maximum_characters: int = 256,
) -> list[str]:
    """Refuse normalized subject-name collisions without resolving identity."""

    item_limit = _require_nonnegative_int(maximum_items, "maximum subject names")
    character_limit = _require_nonnegative_int(
        maximum_characters, "maximum subject-name characters"
    )
    rows = list(values)
    if not rows or len(rows) > item_limit:
        raise DeltaError("attestation subject-name count is empty or over budget")
    normalized: list[str] = []
    for value in rows:
        if (
            not isinstance(value, str)
            or not value
            or value != value.strip()
            or len(value) > character_limit
        ):
            raise DeltaError("attestation subject name is empty, padded, or over budget")
        nfc = unicodedata.normalize("NFC", value)
        if value != nfc or any(unicodedata.category(char) in {"Cc", "Cf"} for char in value):
            raise DeltaError("attestation subject name is noncanonical or contains controls")
        normalized.append(nfc.casefold())
    if len(normalized) != len(set(normalized)):
        raise DeltaError("attestation subject names collide after normalization")
    return rows


def validate_rfc3339_leap_second_reservation(
    value: str, allow_reserved_leap_second: bool = False
) -> dict[str, Any]:
    """Reserve lexical second 60 instead of silently normalizing trusted time."""

    if not isinstance(allow_reserved_leap_second, bool):
        raise DeltaError("leap-second policy must be Boolean")
    pattern = re.compile(
        r"(?P<prefix>[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:)"
        r"(?P<second>[0-9]{2})(?P<fraction>\.[0-9]+)?(?P<offset>Z|[+-][0-9]{2}:[0-9]{2})\Z"
    )
    match = pattern.fullmatch(value) if isinstance(value, str) else None
    if not match or value.endswith("-00:00"):
        raise DeltaError("timestamp is outside the bounded explicit-offset form")
    second = int(match.group("second"))
    if second > 60:
        raise DeltaError("timestamp second is outside the bounded range")
    probe = (
        match.group("prefix")
        + ("59" if second == 60 else match.group("second"))
        + (match.group("fraction") or "")
        + match.group("offset")
    )
    normalize_rfc3339_utc(probe)
    if second == 60 and not allow_reserved_leap_second:
        raise DeltaError("leap-second timestamp is reserved by policy")
    return {
        "value": value,
        "reserved_leap_second": second == 60,
        "trusted_time": False,
        "valid": True,
    }


def validate_json_pointer_array_index(token: str, maximum_index: int = 1_000_000) -> int:
    """Validate canonical decimal array-index syntax without document traversal."""

    maximum = _require_nonnegative_int(maximum_index, "maximum JSON array index")
    if not isinstance(token, str) or not re.fullmatch(r"(?:0|[1-9][0-9]*)", token):
        raise DeltaError("JSON Pointer array index is not canonical decimal text")
    if len(token) > 19:
        raise DeltaError("JSON Pointer array index exceeds the lexical budget")
    value = int(token)
    if value > maximum:
        raise DeltaError("JSON Pointer array index exceeds the declared maximum")
    return value


def validate_revision_pair(
    primary: dict[str, Any], alternative: dict[str, Any]
) -> dict[str, Any]:
    """Require exact report revision parity without claiming accessibility equivalence."""

    required = {"record_ids", "schema_revision", "content_revision"}
    normalized_rows: list[dict[str, Any]] = []
    for label, row in (("primary", primary), ("alternative", alternative)):
        if not isinstance(row, dict) or set(row) != required:
            raise DeltaError(f"{label} report descriptor has the wrong fields")
        identifiers = row["record_ids"]
        if not isinstance(identifiers, list) or not identifiers:
            raise DeltaError(f"{label} report record IDs must be a nonempty list")
        normalized_ids = validate_unique_attestation_subject_names(identifiers)
        revisions = (row["schema_revision"], row["content_revision"])
        if any(
            not isinstance(value, str)
            or not value
            or value != value.strip()
            or len(value) > 64
            for value in revisions
        ):
            raise DeltaError(f"{label} report revision is invalid")
        normalized_rows.append(
            {
                "record_ids": sorted(normalized_ids),
                "schema_revision": revisions[0],
                "content_revision": revisions[1],
            }
        )
    if normalized_rows[0] != normalized_rows[1]:
        raise DeltaError("alternative-format report revision parity failed")
    return {
        "record_count": len(normalized_rows[0]["record_ids"]),
        "schema_revision": normalized_rows[0]["schema_revision"],
        "content_revision": normalized_rows[0]["content_revision"],
        "accessibility_complete": False,
        "valid": True,
    }


def validate_condition_term_revision(
    term: str,
    glossary_id: str,
    glossary_revision: str,
    glossary: dict[str, Any],
) -> dict[str, Any]:
    """Bind a synthetic term to one declared glossary revision without authority."""

    if not isinstance(glossary, dict) or set(glossary) != {
        "glossary_id",
        "revision",
        "terms",
    }:
        raise DeltaError("condition glossary has the wrong fields")
    for label, value in (
        ("term", term),
        ("glossary ID", glossary_id),
        ("glossary revision", glossary_revision),
    ):
        if not isinstance(value, str) or not value or value != value.strip() or len(value) > 128:
            raise DeltaError(f"{label} is invalid")
    if glossary["glossary_id"] != glossary_id or glossary["revision"] != glossary_revision:
        raise DeltaError("condition glossary identity or revision differs")
    terms = validate_unique_attestation_subject_names(
        glossary["terms"], maximum_items=128, maximum_characters=128
    )
    if term not in terms:
        raise DeltaError("condition term is absent from the declared glossary revision")
    return {
        "term": term,
        "glossary_id": glossary_id,
        "glossary_revision": glossary_revision,
        "professional_authority": False,
        "cultural_authority": False,
        "valid": True,
    }


def validate_custody_transition(
    previous_state: str,
    next_state: str,
    observed_revision: int,
    expected_revision: int,
    hold_active: bool,
    previous_actor: str,
    next_actor: str,
    allowed_edges: Iterable[tuple[str, str]] = (
        ("storage", "review"),
        ("review", "storage"),
        ("review", "handover"),
    ),
) -> dict[str, Any]:
    """Quarantine conflicting synthetic custody transitions without real action."""

    if not isinstance(hold_active, bool):
        raise DeltaError("custody hold status must be Boolean")
    revision = _require_nonnegative_int(observed_revision, "observed custody revision")
    expected = _require_nonnegative_int(expected_revision, "expected custody revision")
    states = (previous_state, next_state)
    if any(
        not isinstance(state, str)
        or not re.fullmatch(r"[a-z][a-z0-9_]{0,31}", state)
        for state in states
    ):
        raise DeltaError("custody state is outside the bounded grammar")
    edges = set(tuple(edge) for edge in allowed_edges)
    if any(len(edge) != 2 for edge in edges) or (previous_state, next_state) not in edges:
        raise DeltaError("custody transition edge is not declared")
    if previous_state == next_state or revision != expected or hold_active:
        raise DeltaError("custody transition conflicts with state, revision, or hold")
    actors = validate_unique_attestation_subject_names(
        [previous_actor, next_actor], maximum_items=2, maximum_characters=128
    )
    return {
        "previous_state": previous_state,
        "next_state": next_state,
        "previous_actor": actors[0],
        "next_actor": actors[1],
        "next_revision": revision + 1,
        "custody_authority": False,
        "valid": True,
    }


def validate_rdf_canonicalization_descriptor(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a no-input RDFC descriptor without canonicalizing an RDF dataset."""

    required = {
        "algorithm",
        "hash_algorithm",
        "maximum_n_degree_calls",
        "dataset_present",
        "canonical_output_present",
    }
    if not isinstance(record, dict) or set(record) != required:
        raise DeltaError("RDFC descriptor has the wrong fields")
    if record["algorithm"] != "RDFC-1.0":
        raise DeltaError("RDFC algorithm declaration is unsupported")
    if record["hash_algorithm"] not in {"sha256", "sha384"}:
        raise DeltaError("RDFC hash declaration is unsupported")
    maximum = _require_nonnegative_int(
        record["maximum_n_degree_calls"], "maximum RDFC N-degree calls"
    )
    if maximum < 1 or maximum > 1_000_000:
        raise DeltaError("RDFC work declaration is outside the bounded range")
    if not isinstance(record["dataset_present"], bool) or not isinstance(
        record["canonical_output_present"], bool
    ):
        raise DeltaError("RDFC input and output presence flags must be Boolean")
    if record["dataset_present"] or record["canonical_output_present"]:
        raise DeltaError("RDFC descriptor must not carry a dataset or canonical output")
    return {
        "algorithm": record["algorithm"],
        "hash_algorithm": record["hash_algorithm"],
        "maximum_n_degree_calls": maximum,
        "dataset_canonicalized": False,
        "digest_computed": False,
        "valid": True,
    }


def validate_shacl_report_shape(report: dict[str, Any]) -> dict[str, Any]:
    """Validate a bounded SHACL report vocabulary subset without graph processing."""

    if not isinstance(report, dict) or set(report) != {"conforms", "results"}:
        raise DeltaError("SHACL report has the wrong fields")
    if not isinstance(report["conforms"], bool) or not isinstance(report["results"], list):
        raise DeltaError("SHACL conforms and results have the wrong types")
    results = report["results"]
    if len(results) > 64:
        raise DeltaError("SHACL result count exceeds budget")
    if report["conforms"] != (len(results) == 0):
        raise DeltaError("SHACL conforms value and result cardinality disagree")
    mandatory = {"severity", "focus_node", "source_constraint_component"}
    allowed = mandatory | {"result_path"}
    for row in results:
        if not isinstance(row, dict) or not mandatory <= set(row) <= allowed:
            raise DeltaError("SHACL result has missing or undeclared fields")
        for field, value in row.items():
            if (
                not isinstance(value, str)
                or not value
                or value != value.strip()
                or len(value) > 512
                or any(unicodedata.category(char) in {"Cc", "Cf"} for char in value)
            ):
                raise DeltaError(f"SHACL result {field} is invalid")
    return {
        "conforms": report["conforms"],
        "result_count": len(results),
        "graph_processed": False,
        "complete_shacl_conformance": False,
        "valid": True,
    }


def validate_sparql_result_bindings(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate a bounded SPARQL JSON result shape without issuing a query."""

    if not isinstance(payload, dict) or "head" not in payload:
        raise DeltaError("SPARQL result lacks a head object")
    forms = [name for name in ("boolean", "results") if name in payload]
    if len(forms) != 1 or set(payload) != {"head", forms[0]}:
        raise DeltaError("SPARQL result must contain exactly one ASK or SELECT form")
    head = payload["head"]
    if not isinstance(head, dict) or set(head) != {"vars"} or not isinstance(
        head["vars"], list
    ):
        raise DeltaError("SPARQL head has the wrong shape")
    variables = head["vars"]
    if len(variables) > 64 or any(
        not isinstance(value, str)
        or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,63}", value)
        for value in variables
    ):
        raise DeltaError("SPARQL variable declaration is invalid or over budget")
    ensure_unique(variables, "SPARQL head variable")
    if forms[0] == "boolean":
        if not isinstance(payload["boolean"], bool) or variables:
            raise DeltaError("SPARQL ASK result is inconsistent")
        binding_count = 0
    else:
        results = payload["results"]
        if not isinstance(results, dict) or set(results) != {"bindings"} or not isinstance(
            results["bindings"], list
        ):
            raise DeltaError("SPARQL SELECT results have the wrong shape")
        if len(results["bindings"]) > 128:
            raise DeltaError("SPARQL binding count exceeds budget")
        declared = set(variables)
        for row in results["bindings"]:
            if not isinstance(row, dict) or not set(row) <= declared:
                raise DeltaError("SPARQL binding uses an undeclared variable")
            for term in row.values():
                if not isinstance(term, dict) or not {"type", "value"} <= set(term):
                    raise DeltaError("SPARQL RDF term lacks type or value")
                if set(term) - {"type", "value", "datatype", "xml:lang"}:
                    raise DeltaError("SPARQL RDF term contains an undeclared field")
                if term["type"] not in {"uri", "bnode", "literal", "typed-literal"}:
                    raise DeltaError("SPARQL RDF term type is unsupported")
                if not isinstance(term["value"], str) or len(term["value"]) > 2048:
                    raise DeltaError("SPARQL RDF term value is invalid or over budget")
                if "datatype" in term and "xml:lang" in term:
                    raise DeltaError("SPARQL literal cannot carry datatype and language")
        binding_count = len(results["bindings"])
    return {
        "form": "ASK" if forms[0] == "boolean" else "SELECT",
        "declared_variable_count": len(variables),
        "binding_count": binding_count,
        "query_executed": False,
        "endpoint_accessed": False,
        "valid": True,
    }


def validate_dcat_distribution_descriptor(record: dict[str, Any]) -> dict[str, Any]:
    """Validate DCAT distribution metadata without dereferencing a resource."""

    required = {"access_urls", "download_urls", "media_type", "checksum"}
    if not isinstance(record, dict) or set(record) != required:
        raise DeltaError("DCAT distribution descriptor has the wrong fields")
    access_urls = record["access_urls"]
    download_urls = record["download_urls"]
    if not isinstance(access_urls, list) or not isinstance(download_urls, list):
        raise DeltaError("DCAT location declarations must be lists")
    if not access_urls and not download_urls:
        raise DeltaError("DCAT distribution requires an access or download location")
    if len(access_urls) + len(download_urls) > 8:
        raise DeltaError("DCAT location count exceeds budget")
    all_urls = ensure_unique([*access_urls, *download_urls], "DCAT distribution URL")
    for value in all_urls:
        split = urlsplit(value) if isinstance(value, str) else None
        if (
            split is None
            or split.scheme != "https"
            or not split.netloc
            or split.username is not None
            or split.password is not None
            or split.fragment
        ):
            raise DeltaError("DCAT distribution URL is outside the bounded HTTPS form")
    media_type = record["media_type"]
    if not isinstance(media_type, str) or not re.fullmatch(
        r"[a-z0-9][a-z0-9!#$&^_.+-]*/[a-z0-9][a-z0-9!#$&^_.+-]{0,126}", media_type
    ):
        raise DeltaError("DCAT media type is invalid")
    checksum = record["checksum"]
    if not isinstance(checksum, dict) or set(checksum) != {"algorithm", "value"}:
        raise DeltaError("DCAT checksum descriptor has the wrong fields")
    if checksum["algorithm"] != "sha256" or not isinstance(
        checksum["value"], str
    ) or not re.fullmatch(r"[0-9a-f]{64}", checksum["value"]):
        raise DeltaError("DCAT checksum declaration is unsupported or malformed")
    return {
        "access_url_count": len(access_urls),
        "download_url_count": len(download_urls),
        "media_type": media_type,
        "checksum_algorithm": "sha256",
        "url_dereferenced": False,
        "rights_interpreted": False,
        "valid": True,
    }


def validate_openpgp_one_pass_sequence(packet_types: Iterable[str]) -> dict[str, Any]:
    """Validate a synthetic one-pass packet sequence without parsing OpenPGP bytes."""

    packets = list(packet_types)
    if not packets or len(packets) > 32 or packets.count("literal") != 1:
        raise DeltaError("OpenPGP packet sequence is empty, over budget, or lacks one literal packet")
    literal_index = packets.index("literal")
    opening = packets[:literal_index]
    closing = packets[literal_index + 1 :]
    if not opening or len(opening) != len(closing):
        raise DeltaError("OpenPGP one-pass and signature packet counts disagree")
    signers: list[str] = []
    for index, packet in enumerate(opening):
        match = re.fullmatch(r"one_pass:([A-Za-z0-9._-]{1,64}):(more|last)", packet)
        if not match:
            raise DeltaError("OpenPGP one-pass packet declaration is malformed")
        expected_flag = "last" if index == len(opening) - 1 else "more"
        if match.group(2) != expected_flag:
            raise DeltaError("OpenPGP one-pass nesting flag is inconsistent")
        signers.append(match.group(1))
    if len(signers) != len(set(signers)):
        raise DeltaError("OpenPGP one-pass signer labels repeat")
    expected_closing = [f"signature:{signer}" for signer in reversed(signers)]
    if closing != expected_closing:
        raise DeltaError("OpenPGP signatures do not close in reverse one-pass order")
    return {
        "one_pass_packets": len(opening),
        "signature_packets": len(closing),
        "bytes_parsed": False,
        "signature_verified": False,
        "valid": True,
    }


def validate_sse_event_block(
    fields: Iterable[dict[str, str]], maximum_lines: int = 64, maximum_bytes: int = 4096
) -> dict[str, Any]:
    """Validate a bounded synthetic SSE field block without opening a connection."""

    line_limit = _require_nonnegative_int(maximum_lines, "maximum SSE lines")
    byte_limit = _require_nonnegative_int(maximum_bytes, "maximum SSE bytes")
    rows = list(fields)
    if not rows or len(rows) > line_limit:
        raise DeltaError("SSE field count is empty or over budget")
    allowed = {"data", "event", "id", "retry", "comment"}
    total = 0
    data_lines = 0
    seen_singletons: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"name", "value"}:
            raise DeltaError("SSE field row has the wrong shape")
        name, value = row["name"], row["value"]
        if name not in allowed or not isinstance(value, str) or "\r" in value or "\n" in value:
            raise DeltaError("SSE field name or value is invalid")
        total += len(name.encode("utf-8")) + len(value.encode("utf-8")) + 2
        if total > byte_limit:
            raise DeltaError("SSE field block exceeds byte budget")
        if name == "data":
            data_lines += 1
        elif name in {"event", "id", "retry"}:
            if name in seen_singletons:
                raise DeltaError("SSE singleton field repeats")
            seen_singletons.add(name)
        if name == "id" and ("\x00" in value or len(value) > 256):
            raise DeltaError("SSE event identifier is invalid or over budget")
        if name == "event" and value and not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]{0,63}", value):
            raise DeltaError("SSE event type is outside the bounded grammar")
        if name == "retry" and (
            not re.fullmatch(r"(?:0|[1-9][0-9]{0,6})", value) or int(value) > 600_000
        ):
            raise DeltaError("SSE retry value is invalid or over budget")
    if data_lines < 1:
        raise DeltaError("SSE block contains no data field")
    return {
        "line_count": len(rows),
        "data_line_count": data_lines,
        "declared_bytes": total,
        "network_opened": False,
        "event_dispatched": False,
        "valid": True,
    }


def validate_grpc_status_trailers(trailers: dict[str, str]) -> dict[str, Any]:
    """Validate bounded gRPC status trailers without creating an RPC channel."""

    allowed = {"grpc-status", "grpc-message", "grpc-status-details-bin"}
    if not isinstance(trailers, dict) or "grpc-status" not in trailers or not set(trailers) <= allowed:
        raise DeltaError("gRPC trailer map is missing status or has undeclared fields")
    status_raw = trailers["grpc-status"]
    if not isinstance(status_raw, str) or not re.fullmatch(r"(?:0|[1-9][0-9]?)", status_raw):
        raise DeltaError("gRPC status is not canonical decimal text")
    status = int(status_raw)
    if status > 16:
        raise DeltaError("gRPC status is outside the defined range")
    message = trailers.get("grpc-message", "")
    if not isinstance(message, str) or len(message.encode("utf-8")) > 512:
        raise DeltaError("gRPC message is invalid or over budget")
    for match in re.finditer("%", message):
        if not re.match(r"[0-9A-Fa-f]{2}", message[match.start() + 1 : match.start() + 3]):
            raise DeltaError("gRPC message contains a malformed percent escape")
    details = trailers.get("grpc-status-details-bin")
    if details is not None:
        if status == 0:
            raise DeltaError("gRPC success status carries failure-only details")
        if not isinstance(details, str) or len(details) > 1368 or len(details) % 4:
            raise DeltaError("gRPC details declaration is invalid or over budget")
        if not re.fullmatch(r"(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?", details):
            raise DeltaError("gRPC details declaration is not canonical base64 shape")
    return {
        "status": status,
        "message_bytes": len(message.encode("utf-8")),
        "details_declared": details is not None,
        "details_decoded": False,
        "rpc_invoked": False,
        "valid": True,
    }


def validate_xmp_identifier_lineage(record: dict[str, Any]) -> dict[str, Any]:
    """Validate synthetic XMP identifier lineage without provenance inference."""

    required = {"document_id", "instance_id", "original_document_id", "history"}
    if not isinstance(record, dict) or set(record) != required or not isinstance(
        record["history"], list
    ):
        raise DeltaError("XMP lineage descriptor has the wrong fields")
    identifiers = [
        record["document_id"],
        record["instance_id"],
        record["original_document_id"],
    ]
    if any(
        not isinstance(value, str)
        or not re.fullmatch(r"xmp\.(?:did|iid|oid):[A-Za-z0-9._-]{1,64}", value)
        for value in identifiers
    ) or len(set(identifiers)) != 3:
        raise DeltaError("XMP document identifiers are invalid or not distinct")
    if not record["history"] or len(record["history"]) > 64:
        raise DeltaError("XMP history is empty or over budget")
    seen: set[str] = set()
    for row in record["history"]:
        if not isinstance(row, dict) or set(row) != {"event_id", "parent_event_id", "action"}:
            raise DeltaError("XMP history row has the wrong fields")
        event_id = row["event_id"]
        parent = row["parent_event_id"]
        action = row["action"]
        if not isinstance(event_id, str) or not re.fullmatch(r"evt-[A-Za-z0-9._-]{1,64}", event_id):
            raise DeltaError("XMP history event identifier is invalid")
        if event_id in seen or parent == event_id:
            raise DeltaError("XMP history repeats or self-references an event")
        if parent is not None and parent not in seen:
            raise DeltaError("XMP history parent is absent or forward-referenced")
        if not isinstance(action, str) or not re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", action):
            raise DeltaError("XMP history action is invalid")
        seen.add(event_id)
    return {
        "history_count": len(seen),
        "provenance_verified": False,
        "authenticity_verified": False,
        "custody_authority": False,
        "valid": True,
    }


def validate_ttml_time_expression(descriptor: dict[str, Any]) -> dict[str, Any]:
    """Validate a bounded TTML timing subset without rendering media."""

    required = {"begin", "end", "frame_rate", "tick_rate", "region", "known_regions"}
    if not isinstance(descriptor, dict) or set(descriptor) != required:
        raise DeltaError("TTML timing descriptor has the wrong fields")
    frame_rate = _require_nonnegative_int(descriptor["frame_rate"], "TTML frame rate")
    tick_rate = _require_nonnegative_int(descriptor["tick_rate"], "TTML tick rate")
    if not 1 <= frame_rate <= 240 or not 1 <= tick_rate <= 1_000_000:
        raise DeltaError("TTML rate declaration is outside the bounded range")
    regions = descriptor["known_regions"]
    if not isinstance(regions, list) or not regions or len(regions) > 64:
        raise DeltaError("TTML region list is empty or over budget")
    ensure_unique(regions, "TTML region")
    if any(
        not isinstance(value, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]{0,63}", value)
        for value in regions
    ) or descriptor["region"] not in regions:
        raise DeltaError("TTML region reference is invalid or unknown")

    def seconds(value: Any) -> float:
        if not isinstance(value, str) or len(value) > 64:
            raise DeltaError("TTML time expression is invalid or over budget")
        offset = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)s", value)
        if offset:
            parsed = float(offset.group(1))
            if not math.isfinite(parsed):
                raise DeltaError("TTML offset time is nonfinite")
            return parsed
        clock = re.fullmatch(r"([0-9]{2,}):([0-5][0-9]):([0-5][0-9]):([0-9]{2})", value)
        if not clock or int(clock.group(4)) >= frame_rate:
            raise DeltaError("TTML clock time is malformed or frame is out of range")
        return (
            int(clock.group(1)) * 3600
            + int(clock.group(2)) * 60
            + int(clock.group(3))
            + int(clock.group(4)) / frame_rate
        )

    begin = seconds(descriptor["begin"])
    end = seconds(descriptor["end"])
    if begin < 0 or end <= begin or end > 86_400:
        raise DeltaError("TTML timing interval is invalid or over budget")
    return {
        "begin_seconds": begin,
        "end_seconds": end,
        "region": descriptor["region"],
        "media_rendered": False,
        "accessibility_complete": False,
        "valid": True,
    }


def validate_otel_baggage_members(
    members: Iterable[dict[str, Any]], maximum_members: int = 16, maximum_bytes: int = 1024
) -> dict[str, Any]:
    """Validate bounded local baggage declarations without telemetry propagation."""

    member_limit = _require_nonnegative_int(maximum_members, "maximum baggage members")
    byte_limit = _require_nonnegative_int(maximum_bytes, "maximum baggage bytes")
    rows = list(members)
    if not rows or len(rows) > member_limit:
        raise DeltaError("baggage member count is empty or over budget")
    keys: list[str] = []
    total = 0
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"key", "value", "properties"}:
            raise DeltaError("baggage member has the wrong fields")
        key, value, properties = row["key"], row["value"], row["properties"]
        if not isinstance(key, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_.*/-]{0,63}", key):
            raise DeltaError("baggage key is outside the bounded grammar")
        if not isinstance(value, str) or len(value) > 256 or any(ord(char) < 0x20 for char in value):
            raise DeltaError("baggage value is invalid or over budget")
        for match in re.finditer("%", value):
            if not re.match(r"[0-9A-Fa-f]{2}", value[match.start() + 1 : match.start() + 3]):
                raise DeltaError("baggage value contains a malformed percent escape")
        if not isinstance(properties, list) or len(properties) > 8 or any(
            not isinstance(prop, str)
            or not re.fullmatch(r"[a-z][a-z0-9_-]{0,31}(?:=[A-Za-z0-9._-]{1,64})?", prop)
            for prop in properties
        ):
            raise DeltaError("baggage properties are invalid or over budget")
        keys.append(key)
        total += len(key.encode()) + len(value.encode()) + sum(len(prop.encode()) for prop in properties) + 2
        if total > byte_limit:
            raise DeltaError("baggage aggregate exceeds byte budget")
    ensure_unique(keys, "baggage key")
    return {
        "member_count": len(rows),
        "declared_bytes": total,
        "telemetry_propagated": False,
        "privacy_complete": False,
        "valid": True,
    }


def validate_authentication_results_shape(record: dict[str, Any]) -> dict[str, Any]:
    """Validate Authentication-Results metadata without authenticating a message."""

    if not isinstance(record, dict) or set(record) != {"authserv_id", "results"}:
        raise DeltaError("Authentication-Results descriptor has the wrong fields")
    authserv_id = record["authserv_id"]
    if not isinstance(authserv_id, str) or not re.fullmatch(
        r"[A-Za-z0-9](?:[A-Za-z0-9.-]{0,251}[A-Za-z0-9])?", authserv_id
    ):
        raise DeltaError("Authentication-Results authserv-id is invalid")
    rows = record["results"]
    if not isinstance(rows, list) or not rows or len(rows) > 16:
        raise DeltaError("Authentication-Results count is empty or over budget")
    allowed_results = {"none", "pass", "fail", "policy", "neutral", "temperror", "permerror", "softfail"}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"method", "result", "properties"}:
            raise DeltaError("Authentication-Results row has the wrong fields")
        if not isinstance(row["method"], str) or not re.fullmatch(r"[a-z][a-z0-9_-]{0,31}", row["method"]):
            raise DeltaError("Authentication-Results method is invalid")
        if row["result"] not in allowed_results:
            raise DeltaError("Authentication-Results result token is unsupported")
        if not isinstance(row["properties"], dict) or len(row["properties"]) > 8:
            raise DeltaError("Authentication-Results properties are invalid or over budget")
        for key, value in row["properties"].items():
            if not isinstance(key, str) or not re.fullmatch(r"[a-z][a-z0-9_-]{0,15}\.[a-z][a-z0-9_-]{0,31}", key):
                raise DeltaError("Authentication-Results property name is invalid")
            if not isinstance(value, str) or not value or len(value) > 256 or any(ord(char) < 0x20 for char in value):
                raise DeltaError("Authentication-Results property value is invalid")
    return {
        "authserv_id": authserv_id,
        "result_count": len(rows),
        "message_authenticated": False,
        "mail_processed": False,
        "valid": True,
    }


def validate_mta_sts_policy(policy: dict[str, Any]) -> dict[str, Any]:
    """Validate a synthetic MTA-STS policy without DNS, SMTP, or deployment."""

    required = {"version", "mode", "mx", "max_age", "previous_mode"}
    if not isinstance(policy, dict) or set(policy) != required:
        raise DeltaError("MTA-STS policy has the wrong fields")
    if policy["version"] != "STSv1" or policy["mode"] not in {"none", "testing", "enforce"}:
        raise DeltaError("MTA-STS version or mode is unsupported")
    if policy["previous_mode"] not in {"none", "testing", "enforce"}:
        raise DeltaError("MTA-STS previous mode is unsupported")
    max_age = _require_nonnegative_int(policy["max_age"], "MTA-STS max_age")
    if max_age > 31_557_600:
        raise DeltaError("MTA-STS max_age exceeds the bounded range")
    mx = policy["mx"]
    if not isinstance(mx, list) or len(mx) > 16:
        raise DeltaError("MTA-STS MX list is invalid or over budget")
    ensure_unique(mx, "MTA-STS MX pattern")
    for value in mx:
        if not isinstance(value, str) or not re.fullmatch(
            r"(?:\*\.)?[A-Za-z0-9](?:[A-Za-z0-9.-]{0,251}[A-Za-z0-9])?", value
        ):
            raise DeltaError("MTA-STS MX pattern is invalid")
    if policy["mode"] == "none" and mx:
        raise DeltaError("MTA-STS none mode must not declare MX patterns")
    if policy["mode"] in {"testing", "enforce"} and not mx:
        raise DeltaError("MTA-STS testing or enforce mode requires an MX pattern")
    if policy["previous_mode"] == "none" and policy["mode"] == "enforce":
        raise DeltaError("MTA-STS none-to-enforce transition requires an explicit testing hold")
    return {
        "mode": policy["mode"],
        "mx_count": len(mx),
        "max_age": max_age,
        "dns_accessed": False,
        "smtp_accessed": False,
        "policy_deployed": False,
        "valid": True,
    }


def validate_security_txt_fields(fields: dict[str, Any]) -> dict[str, Any]:
    """Validate bounded security.txt fields without retrieval or publication."""

    required = {"contact", "expires", "canonical", "preferred_languages"}
    if not isinstance(fields, dict) or set(fields) != required:
        raise DeltaError("security.txt field map has the wrong fields")
    contacts = fields["contact"]
    canonical = fields["canonical"]
    languages = fields["preferred_languages"]
    if not isinstance(contacts, list) or not 1 <= len(contacts) <= 8:
        raise DeltaError("security.txt contact list is empty or over budget")
    if not isinstance(canonical, list) or not 1 <= len(canonical) <= 8:
        raise DeltaError("security.txt canonical list is empty or over budget")
    if not isinstance(languages, list) or not 1 <= len(languages) <= 16:
        raise DeltaError("security.txt language list is empty or over budget")
    ensure_unique(contacts, "security.txt contact")
    ensure_unique(canonical, "security.txt canonical URI")
    ensure_unique(languages, "security.txt preferred language")
    for value in contacts:
        split = urlsplit(value) if isinstance(value, str) else None
        if split is None or (
            not (value.startswith("mailto:") and "@" in split.path)
            and not (split.scheme == "https" and split.netloc)
        ):
            raise DeltaError("security.txt contact is outside the bounded URI forms")
    for value in canonical:
        split = urlsplit(value) if isinstance(value, str) else None
        if split is None or split.scheme != "https" or not split.netloc or not split.path.endswith(
            "/.well-known/security.txt"
        ) or split.query or split.fragment:
            raise DeltaError("security.txt canonical URI is invalid")
    expires = fields["expires"]
    if not isinstance(expires, str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", expires
    ):
        raise DeltaError("security.txt expiry is not bounded UTC text")
    try:
        datetime.fromisoformat(expires.replace("Z", "+00:00"))
    except ValueError as exc:
        raise DeltaError("security.txt expiry is not a real calendar time") from exc
    if any(
        not isinstance(value, str)
        or not re.fullmatch(r"[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8}){0,3}", value)
        for value in languages
    ):
        raise DeltaError("security.txt preferred language is invalid")
    return {
        "contact_count": len(contacts),
        "canonical_count": len(canonical),
        "preferred_language_count": len(languages),
        "retrieved": False,
        "published": False,
        "disclosure_authority": False,
        "valid": True,
    }


def validate_problem_details_shape(problem: dict[str, Any]) -> dict[str, Any]:
    """Validate a bounded RFC 9457 shape without serving an HTTP response."""

    allowed = {"type", "title", "status", "detail", "instance", "extensions"}
    if not isinstance(problem, dict) or not {"type", "title", "status"} <= set(problem) <= allowed:
        raise DeltaError("Problem Details object has missing or undeclared fields")
    status = _require_nonnegative_int(problem["status"], "Problem Details status")
    if not 100 <= status <= 599:
        raise DeltaError("Problem Details status is outside the HTTP range")
    type_uri = problem["type"]
    if type_uri != "about:blank":
        split = urlsplit(type_uri) if isinstance(type_uri, str) else None
        if split is None or split.scheme != "https" or not split.netloc:
            raise DeltaError("Problem Details type is outside the bounded URI form")
    for field in ("title", "detail"):
        if field in problem and (
            not isinstance(problem[field], str)
            or not problem[field]
            or len(problem[field]) > 2048
            or any(ord(char) < 0x20 and char not in "\t" for char in problem[field])
        ):
            raise DeltaError(f"Problem Details {field} is invalid or over budget")
    detail = problem.get("detail", "")
    if re.search(r"(?i)(?:api[_-]?key|password|access[_-]?token)\s*[:=]", detail):
        raise DeltaError("Problem Details detail contains a secret-shaped marker")
    if "instance" in problem:
        instance = problem["instance"]
        split = urlsplit(instance) if isinstance(instance, str) else None
        if split is None or not (
            (split.scheme == "https" and split.netloc) or (not split.scheme and not split.netloc and instance.startswith("/"))
        ):
            raise DeltaError("Problem Details instance is outside the bounded URI form")
    extensions = problem.get("extensions", {})
    if not isinstance(extensions, dict) or len(extensions) > 16:
        raise DeltaError("Problem Details extensions are invalid or over budget")
    core_casefold = {name.casefold() for name in allowed - {"extensions"}}
    for key, value in extensions.items():
        if not isinstance(key, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]{0,63}", key):
            raise DeltaError("Problem Details extension name is invalid")
        if key.casefold() in core_casefold:
            raise DeltaError("Problem Details extension collides with a core member")
        if not isinstance(value, (str, int, bool, type(None))) or isinstance(value, float):
            raise DeltaError("Problem Details extension value is outside the bounded scalar set")
        if isinstance(value, str) and len(value) > 512:
            raise DeltaError("Problem Details extension value exceeds budget")
    return {
        "status": status,
        "extension_count": len(extensions),
        "http_served": False,
        "privacy_complete": False,
        "valid": True,
    }


_CAVE_TOKEN = re.compile(r"[a-z][a-z0-9_-]{0,63}\Z")


def _cave_record(record: Any, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(record, dict) or set(record) != fields:
        raise DeltaError(f"{label} has the wrong fields")
    return record


def _cave_token(value: Any, label: str) -> str:
    if not isinstance(value, str) or _CAVE_TOKEN.fullmatch(value) is None:
        raise DeltaError(f"{label} is outside the bounded token grammar")
    return value


def _cave_finite(
    value: Any,
    label: str,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
    minimum_inclusive: bool = True,
    maximum_inclusive: bool = True,
) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise DeltaError(f"{label} must be a non-Boolean number")
    parsed = float(value)
    if not math.isfinite(parsed):
        raise DeltaError(f"{label} must be finite")
    if minimum is not None and (
        parsed < minimum if minimum_inclusive else parsed <= minimum
    ):
        raise DeltaError(f"{label} is below the bounded range")
    if maximum is not None and (
        parsed > maximum if maximum_inclusive else parsed >= maximum
    ):
        raise DeltaError(f"{label} is above the bounded range")
    return parsed


def _cave_timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not 20 <= len(value) <= 40:
        raise DeltaError(f"{label} is not a bounded timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise DeltaError(f"{label} is not an ISO timestamp") from exc
    if parsed.tzinfo is None:
        raise DeltaError(f"{label} lacks an explicit offset")
    return parsed.astimezone(timezone.utc)


def _cave_false(value: Any, label: str) -> None:
    if value is not False:
        raise DeltaError(f"{label} must remain explicitly false")


def validate_cave_station_shot_topology(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a fictional station-shot graph without producing a cave survey."""

    _cave_record(
        record,
        {
            "project_token",
            "stations",
            "shots",
            "root_station",
            "synthetic",
            "real_location_present",
        },
        "cave topology record",
    )
    _cave_token(record["project_token"], "cave project token")
    stations = record["stations"]
    if not isinstance(stations, list) or not 2 <= len(stations) <= 64:
        raise DeltaError("cave station count is outside the bounded range")
    station_tokens = [_cave_token(value, "cave station token") for value in stations]
    ensure_unique(station_tokens, "cave station token")
    root = _cave_token(record["root_station"], "cave root station")
    if root not in station_tokens:
        raise DeltaError("cave root station is unknown")
    shots = record["shots"]
    if not isinstance(shots, list) or not 1 <= len(shots) <= 128:
        raise DeltaError("cave shot count is outside the bounded range")
    shot_tokens: list[str] = []
    adjacency = {station: set() for station in station_tokens}
    for shot in shots:
        _cave_record(
            shot,
            {"shot_token", "from_station", "to_station"},
            "cave shot row",
        )
        shot_token = _cave_token(shot["shot_token"], "cave shot token")
        start = _cave_token(shot["from_station"], "cave shot origin")
        end = _cave_token(shot["to_station"], "cave shot destination")
        if start not in adjacency or end not in adjacency:
            raise DeltaError("cave shot references an unknown station")
        if start == end:
            raise DeltaError("cave shot self-loop is not allowed")
        shot_tokens.append(shot_token)
        adjacency[start].add(end)
        adjacency[end].add(start)
    ensure_unique(shot_tokens, "cave shot token")
    reached = {root}
    frontier = [root]
    while frontier:
        current = frontier.pop()
        for neighbour in adjacency[current] - reached:
            reached.add(neighbour)
            frontier.append(neighbour)
    if reached != set(station_tokens):
        raise DeltaError("cave station-shot graph is disconnected")
    if record["synthetic"] is not True:
        raise DeltaError("cave topology record must be explicitly synthetic")
    _cave_false(record["real_location_present"], "real cave location presence")
    return {
        "station_count": len(station_tokens),
        "shot_count": len(shot_tokens),
        "graph_connected": True,
        "survey_computed": False,
        "real_location_present": False,
        "valid": True,
    }


def validate_cave_measurement_domain(record: dict[str, Any]) -> dict[str, Any]:
    """Validate bounded declaration units without claiming a measurement."""

    _cave_record(
        record,
        {
            "bearing",
            "inclination",
            "distance",
            "bearing_unit",
            "inclination_unit",
            "distance_unit",
            "measurement_claimed",
        },
        "cave measurement record",
    )
    bearing = _cave_finite(
        record["bearing"],
        "cave bearing",
        minimum=0.0,
        maximum=360.0,
        maximum_inclusive=False,
    )
    inclination = _cave_finite(
        record["inclination"], "cave inclination", minimum=-90.0, maximum=90.0
    )
    distance = _cave_finite(
        record["distance"],
        "cave distance",
        minimum=0.0,
        maximum=100_000.0,
        minimum_inclusive=False,
    )
    if record["bearing_unit"] != "degree" or record["inclination_unit"] != "degree":
        raise DeltaError("cave angular units must be declared as degree")
    if record["distance_unit"] != "m":
        raise DeltaError("cave distance unit must be declared as m")
    _cave_false(record["measurement_claimed"], "real cave measurement claim")
    return {
        "bearing": bearing,
        "inclination": inclination,
        "distance": distance,
        "measurement_claimed": False,
        "survey_accuracy_claimed": False,
        "valid": True,
    }


def validate_cave_instrument_lineage(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional instrument lineage without calibration authority."""

    _cave_record(
        record,
        {
            "instrument_token",
            "calibration_reference",
            "effective_from",
            "effective_until",
            "uncertainty",
            "calibration_status",
            "calibration_authority_claimed",
        },
        "cave instrument record",
    )
    _cave_token(record["instrument_token"], "cave instrument token")
    reference = record["calibration_reference"]
    if not isinstance(reference, str) or re.fullmatch(r"cal-[a-z0-9_-]{1,63}", reference) is None:
        raise DeltaError("cave calibration reference is invalid")
    start = _cave_timestamp(record["effective_from"], "calibration effective-from")
    end = _cave_timestamp(record["effective_until"], "calibration effective-until")
    if end <= start or (end - start).total_seconds() > 366 * 86_400:
        raise DeltaError("cave calibration interval is reversed or over budget")
    uncertainty = _cave_finite(
        record["uncertainty"],
        "cave instrument uncertainty",
        minimum=0.0,
        maximum=100.0,
        minimum_inclusive=False,
    )
    if record["calibration_status"] != "current":
        raise DeltaError("cave instrument calibration status is not current")
    _cave_false(
        record["calibration_authority_claimed"], "calibration authority claim"
    )
    return {
        "instrument_token": record["instrument_token"],
        "uncertainty": uncertainty,
        "lineage_preserved": True,
        "calibration_performed": False,
        "calibration_authority_claimed": False,
        "valid": True,
    }


def validate_cave_passage_lrud(record: dict[str, Any]) -> dict[str, Any]:
    """Validate an LRUD declaration without reconstructing passage geometry."""

    _cave_record(
        record,
        {
            "station_token",
            "left",
            "right",
            "up",
            "down",
            "omissions",
            "navigable_geometry",
        },
        "cave LRUD record",
    )
    _cave_token(record["station_token"], "LRUD station token")
    omissions = record["omissions"]
    names = ("left", "right", "up", "down")
    if not isinstance(omissions, list) or any(name not in names for name in omissions):
        raise DeltaError("LRUD omissions are invalid")
    ensure_unique(omissions, "LRUD omission")
    numeric_count = 0
    for name in names:
        value = record[name]
        if value is None:
            if name not in omissions:
                raise DeltaError("LRUD null is not declared as omitted")
        else:
            _cave_finite(value, f"LRUD {name}", minimum=0.0, maximum=10_000.0)
            numeric_count += 1
            if name in omissions:
                raise DeltaError("LRUD numeric value is also declared omitted")
    if numeric_count < 1:
        raise DeltaError("LRUD record has no declared numeric offset")
    _cave_false(record["navigable_geometry"], "navigable cave geometry")
    return {
        "numeric_offset_count": numeric_count,
        "omission_count": len(omissions),
        "passage_reconstructed": False,
        "navigable_geometry": False,
        "valid": True,
    }


def validate_cave_loop_closure(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a synthetic loop residual without coordinate adjustment."""

    _cave_record(
        record,
        {
            "station_sequence",
            "residual",
            "residual_unit",
            "adjustment_method",
            "adjustment_applied",
            "accuracy_claimed",
        },
        "cave loop record",
    )
    sequence = record["station_sequence"]
    if not isinstance(sequence, list) or not 4 <= len(sequence) <= 64:
        raise DeltaError("cave loop station sequence is outside the bounded range")
    tokens = [_cave_token(value, "cave loop station") for value in sequence]
    if tokens[0] != tokens[-1]:
        raise DeltaError("cave loop is not closed")
    if any(left == right for left, right in zip(tokens, tokens[1:])):
        raise DeltaError("cave loop repeats adjacent stations")
    if len(set(tokens[:-1])) != len(tokens) - 1:
        raise DeltaError("cave loop repeats an internal station")
    residual = record["residual"]
    _cave_record(residual, {"x", "y", "z"}, "cave loop residual")
    parsed = {
        name: _cave_finite(value, f"cave residual {name}", minimum=-100_000.0, maximum=100_000.0)
        for name, value in residual.items()
    }
    if record["residual_unit"] != "m":
        raise DeltaError("cave loop residual unit must be m")
    if record["adjustment_method"] not in {"none", "least_squares_reserved"}:
        raise DeltaError("cave loop adjustment method is unsupported")
    _cave_false(record["adjustment_applied"], "coordinate adjustment")
    _cave_false(record["accuracy_claimed"], "survey accuracy claim")
    return {
        "station_count": len(tokens) - 1,
        "residual": parsed,
        "adjustment_applied": False,
        "accuracy_claimed": False,
        "valid": True,
    }


def validate_cave_location_minimization(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a withheld coarse location descriptor with no raw coordinates."""

    _cave_record(
        record,
        {
            "location_token",
            "datum_label",
            "precision_class",
            "purpose",
            "disclosure_state",
            "review_hold",
        },
        "cave location record",
    )
    _cave_token(record["location_token"], "cave location token")
    if record["datum_label"] not in {"NZGD2000", "unspecified"}:
        raise DeltaError("cave datum label is unsupported")
    if record["precision_class"] not in {"region_only", "withheld"}:
        raise DeltaError("cave location precision is too specific")
    if record["purpose"] not in {"synthetic_review", "authority_hold"}:
        raise DeltaError("cave location purpose is unsupported")
    if record["disclosure_state"] != "withheld" or record["review_hold"] is not True:
        raise DeltaError("cave location is not withheld under review")
    return {
        "datum_label": record["datum_label"],
        "precision_class": record["precision_class"],
        "raw_coordinates_present": False,
        "location_disclosed": False,
        "privacy_complete": False,
        "valid": True,
    }


def validate_cave_sensitive_feature(record: dict[str, Any]) -> dict[str, Any]:
    """Validate redacted feature metadata without releasing a real feature."""

    _cave_record(
        record,
        {
            "feature_token",
            "feature_class",
            "sensitivity",
            "location_state",
            "redaction_reason",
            "review_authority_class",
            "release_authorized",
            "real_feature",
        },
        "cave sensitive-feature record",
    )
    _cave_token(record["feature_token"], "cave feature token")
    if record["feature_class"] not in {
        "habitat",
        "biodiversity",
        "archaeology",
        "heritage",
        "taonga",
        "unknown",
    }:
        raise DeltaError("cave feature class is unsupported")
    if record["sensitivity"] not in {"restricted", "high"}:
        raise DeltaError("cave feature sensitivity is not restrictive")
    if record["location_state"] != "withheld":
        raise DeltaError("cave feature location is not withheld")
    reason = record["redaction_reason"]
    if not isinstance(reason, str) or not 1 <= len(reason) <= 256 or reason != reason.strip():
        raise DeltaError("cave feature redaction reason is invalid")
    if record["review_authority_class"] not in {
        "competent_external",
        "affected_authority",
        "tangata_whenua_iwi_hapu",
    }:
        raise DeltaError("cave feature review authority class is unsupported")
    _cave_false(record["release_authorized"], "cave feature release")
    _cave_false(record["real_feature"], "real cave feature presence")
    return {
        "feature_class": record["feature_class"],
        "location_state": "withheld",
        "release_authorized": False,
        "authority_exercised": False,
        "valid": True,
    }


def validate_cave_equipment_observation(record: dict[str, Any]) -> dict[str, Any]:
    """Validate equipment observations without a safety assessment or instruction."""

    _cave_record(
        record,
        {
            "equipment_token",
            "equipment_class",
            "observations",
            "unresolved",
            "safety_assessed",
            "use_authorized",
            "instruction_provided",
        },
        "cave equipment record",
    )
    _cave_token(record["equipment_token"], "cave equipment token")
    if record["equipment_class"] not in {"fixed_aid", "anchor", "rope", "rigging", "unknown"}:
        raise DeltaError("cave equipment class is unsupported")
    observations = record["observations"]
    unresolved = record["unresolved"]
    if not isinstance(observations, list) or not 1 <= len(observations) <= 16:
        raise DeltaError("cave equipment observation count is invalid")
    if not isinstance(unresolved, list) or not unresolved:
        raise DeltaError("cave equipment record must retain an unresolved item")
    observation_tokens = [_cave_token(value, "equipment observation token") for value in observations]
    unresolved_tokens = [_cave_token(value, "unresolved equipment token") for value in unresolved]
    ensure_unique(observation_tokens, "equipment observation token")
    ensure_unique(unresolved_tokens, "unresolved equipment token")
    if not set(unresolved_tokens) <= set(observation_tokens):
        raise DeltaError("unresolved equipment item is not an observation")
    _cave_false(record["safety_assessed"], "equipment safety assessment")
    _cave_false(record["use_authorized"], "equipment use authorization")
    _cave_false(record["instruction_provided"], "equipment instruction")
    return {
        "observation_count": len(observation_tokens),
        "unresolved_count": len(unresolved_tokens),
        "safety_assessed": False,
        "use_authorized": False,
        "valid": True,
    }


def validate_cave_condition_cue(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a time-bounded condition cue while refusing entry decisions."""

    _cave_record(
        record,
        {
            "cue_token",
            "source_class",
            "observed_at",
            "expires_at",
            "uncertainty",
            "entry_state",
            "forecast_made",
            "live_feed",
            "entry_authorized",
        },
        "cave condition cue",
    )
    _cave_token(record["cue_token"], "cave condition cue token")
    if record["source_class"] not in {"fictional_observation", "official_notice_placeholder"}:
        raise DeltaError("cave condition source class is unsupported")
    observed = _cave_timestamp(record["observed_at"], "condition observed-at")
    expires = _cave_timestamp(record["expires_at"], "condition expires-at")
    if expires <= observed or (expires - observed).total_seconds() > 86_400:
        raise DeltaError("cave condition cue interval is invalid or over budget")
    if record["uncertainty"] not in {"unknown", "high", "bounded_placeholder"}:
        raise DeltaError("cave condition uncertainty is unsupported")
    if record["entry_state"] != "hold":
        raise DeltaError("cave condition cue must preserve a stop-entry hold")
    _cave_false(record["forecast_made"], "condition forecast")
    _cave_false(record["live_feed"], "live condition feed")
    _cave_false(record["entry_authorized"], "cave entry authorization")
    return {
        "entry_state": "hold",
        "forecast_made": False,
        "live_feed": False,
        "entry_authorized": False,
        "valid": True,
    }


def validate_cave_atmosphere_sensor(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a fictional sensor declaration while refusing atmosphere clearance."""

    _cave_record(
        record,
        {
            "sensor_token",
            "unit",
            "value",
            "uncertainty",
            "calibration_state",
            "live_sensor",
            "atmosphere_cleared",
            "threshold_advice",
        },
        "cave atmosphere sensor record",
    )
    _cave_token(record["sensor_token"], "cave sensor token")
    if record["unit"] not in {"ppm", "percent", "celsius", "hpa"}:
        raise DeltaError("cave sensor unit is unsupported")
    value = _cave_finite(record["value"], "cave sensor value", minimum=-1_000_000.0, maximum=1_000_000.0)
    uncertainty = _cave_finite(
        record["uncertainty"],
        "cave sensor uncertainty",
        minimum=0.0,
        maximum=1_000_000.0,
        minimum_inclusive=False,
    )
    if record["calibration_state"] != "current_placeholder":
        raise DeltaError("cave sensor calibration state is not current-placeholder")
    _cave_false(record["live_sensor"], "live cave sensor")
    _cave_false(record["atmosphere_cleared"], "atmosphere clearance")
    _cave_false(record["threshold_advice"], "atmosphere threshold advice")
    return {
        "unit": record["unit"],
        "value": value,
        "uncertainty": uncertainty,
        "live_sensor": False,
        "atmosphere_cleared": False,
        "valid": True,
    }


def validate_cave_callout_state(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a fictional callout state without tracking or dispatch."""

    _cave_record(
        record,
        {
            "team_token",
            "callout_token",
            "due_at",
            "checked_at",
            "state",
            "escalation_state",
            "live_tracking",
            "automated_dispatch",
            "raw_identity_present",
        },
        "cave callout record",
    )
    _cave_token(record["team_token"], "fictional cave team token")
    _cave_token(record["callout_token"], "cave callout token")
    due = _cave_timestamp(record["due_at"], "callout due-at")
    state = record["state"]
    if state not in {"checked_in", "overdue_hold"}:
        raise DeltaError("cave callout state is unsupported")
    checked_raw = record["checked_at"]
    if state == "checked_in":
        checked = _cave_timestamp(checked_raw, "callout checked-at")
        if checked > due:
            raise DeltaError("checked-in cave callout is after its due time")
        if record["escalation_state"] != "not_required":
            raise DeltaError("checked-in cave callout has a contradictory escalation")
    else:
        if checked_raw is not None or record["escalation_state"] != "awaiting_competent_review":
            raise DeltaError("overdue cave callout lacks its review hold")
    _cave_false(record["live_tracking"], "live team tracking")
    _cave_false(record["automated_dispatch"], "automated emergency dispatch")
    _cave_false(record["raw_identity_present"], "raw team identity presence")
    return {
        "state": state,
        "live_tracking": False,
        "automated_dispatch": False,
        "emergency_authority": False,
        "valid": True,
    }


def validate_cave_incident_lineage(record: dict[str, Any]) -> dict[str, Any]:
    """Validate append-only fictional incident lineage without adjudication."""

    _cave_record(
        record,
        {"incident_token", "records", "closure_authorized", "real_person_data"},
        "cave incident record",
    )
    _cave_token(record["incident_token"], "cave incident token")
    rows = record["records"]
    if not isinstance(rows, list) or not 1 <= len(rows) <= 32:
        raise DeltaError("cave incident lineage is empty or over budget")
    seen: set[str] = set()
    events: list[str] = []
    for index, row in enumerate(rows):
        _cave_record(row, {"record_token", "parent_token", "event"}, "incident lineage row")
        token = _cave_token(row["record_token"], "incident lineage token")
        parent = row["parent_token"]
        event = row["event"]
        if token in seen or parent == token:
            raise DeltaError("incident lineage repeats or self-references a token")
        if index == 0:
            if parent is not None or event != "reported":
                raise DeltaError("incident lineage lacks an original report")
        elif not isinstance(parent, str) or parent not in seen:
            raise DeltaError("incident lineage parent is absent or forward-referenced")
        if event not in {"reported", "corrected", "superseded", "evidence_preserved"}:
            raise DeltaError("incident lineage event is unsupported")
        seen.add(token)
        events.append(event)
    _cave_false(record["closure_authorized"], "incident closure authorization")
    _cave_false(record["real_person_data"], "real person data presence")
    return {
        "record_count": len(rows),
        "correction_present": "corrected" in events,
        "original_preserved": True,
        "closure_authorized": False,
        "remedy_adjudicated": False,
        "valid": True,
    }


def validate_cave_accessible_companion(record: dict[str, Any]) -> dict[str, Any]:
    """Validate structural alternatives without claiming complete accessibility."""

    _cave_record(
        record,
        {
            "document_token",
            "headings",
            "station_summaries",
            "text_alternative",
            "noncolour_status",
            "manual_review_required",
            "accessibility_complete",
            "raw_location_present",
            "imperative_route_instruction",
        },
        "cave accessible companion",
    )
    _cave_token(record["document_token"], "accessible document token")
    headings = record["headings"]
    summaries = record["station_summaries"]
    if not isinstance(headings, list) or not 1 <= len(headings) <= 16:
        raise DeltaError("accessible cave heading count is invalid")
    if any(not isinstance(value, str) or not value.strip() or len(value) > 128 for value in headings):
        raise DeltaError("accessible cave heading is invalid")
    ensure_unique(headings, "accessible cave heading")
    if not isinstance(summaries, list) or not 1 <= len(summaries) <= 64:
        raise DeltaError("accessible station summary count is invalid")
    for row in summaries:
        _cave_record(row, {"station_token", "summary"}, "accessible station summary")
        _cave_token(row["station_token"], "accessible station token")
        if not isinstance(row["summary"], str) or not row["summary"].strip() or len(row["summary"]) > 512:
            raise DeltaError("accessible station summary text is invalid")
    alternative = record["text_alternative"]
    if not isinstance(alternative, str) or not alternative.strip() or len(alternative) > 2048:
        raise DeltaError("cave text alternative is absent or over budget")
    if record["noncolour_status"] is not True or record["manual_review_required"] is not True:
        raise DeltaError("cave companion lacks noncolour status or manual review")
    _cave_false(record["accessibility_complete"], "accessibility completeness")
    _cave_false(record["raw_location_present"], "raw cave location presence")
    _cave_false(record["imperative_route_instruction"], "imperative route instruction")
    return {
        "heading_count": len(headings),
        "station_summary_count": len(summaries),
        "manual_review_required": True,
        "accessibility_complete": False,
        "route_guidance_provided": False,
        "valid": True,
    }


def validate_cave_handover(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a fictional workload handover while refusing operational release."""

    _cave_record(
        record,
        {
            "handover_token",
            "queue_ceiling",
            "active_items",
            "unfinished_items",
            "stop_token",
            "correction_readback",
            "next_owner_acknowledged",
            "release_authorized",
            "real_operator",
        },
        "cave handover record",
    )
    _cave_token(record["handover_token"], "cave handover token")
    ceiling = _require_nonnegative_int(record["queue_ceiling"], "cave queue ceiling")
    if not 1 <= ceiling <= 100:
        raise DeltaError("cave queue ceiling is outside the bounded range")
    active = record["active_items"]
    unfinished = record["unfinished_items"]
    if not isinstance(active, list) or not active or len(active) > ceiling:
        raise DeltaError("cave active queue is empty or over its ceiling")
    if not isinstance(unfinished, list) or not unfinished:
        raise DeltaError("cave handover erases unfinished work")
    active_tokens = [_cave_token(value, "cave active item") for value in active]
    unfinished_tokens = [_cave_token(value, "cave unfinished item") for value in unfinished]
    ensure_unique(active_tokens, "cave active item")
    ensure_unique(unfinished_tokens, "cave unfinished item")
    if not set(unfinished_tokens) <= set(active_tokens):
        raise DeltaError("cave unfinished item is not in the active queue")
    if record["stop_token"] is not True or record["correction_readback"] is not True:
        raise DeltaError("cave handover lacks stop dominance or correction readback")
    if record["next_owner_acknowledged"] is not True:
        raise DeltaError("cave handover lacks fictional next-owner acknowledgement")
    _cave_false(record["release_authorized"], "operational release authorization")
    _cave_false(record["real_operator"], "real operator presence")
    return {
        "queue_ceiling": ceiling,
        "active_count": len(active_tokens),
        "unfinished_count": len(unfinished_tokens),
        "release_authorized": False,
        "real_operator": False,
        "valid": True,
    }


def validate_choir_packet_identity(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a fictional packet identity while refusing a real event or content."""

    _cave_record(
        record,
        {
            "packet_token",
            "revision",
            "source_pin",
            "cancellation_state",
            "performance_authorized",
            "synthetic",
            "lyrics_present",
            "score_content_present",
            "real_event_present",
        },
        "choir packet identity",
    )
    _cave_token(record["packet_token"], "choir packet token")
    revision = _require_nonnegative_int(record["revision"], "choir packet revision")
    if not 1 <= revision <= 10_000:
        raise DeltaError("choir packet revision is outside the bounded range")
    source_pin = record["source_pin"]
    if not isinstance(source_pin, str) or re.fullmatch(r"sha256:[0-9a-f]{64}", source_pin) is None:
        raise DeltaError("choir packet source pin is not an explicit SHA-256 commitment")
    if record["cancellation_state"] not in {"active_placeholder", "cancelled_placeholder", "hold"}:
        raise DeltaError("choir packet cancellation state is unsupported")
    if record["synthetic"] is not True:
        raise DeltaError("choir packet must remain explicitly synthetic")
    _cave_false(record["performance_authorized"], "choir performance authorization")
    _cave_false(record["lyrics_present"], "choir lyrics presence")
    _cave_false(record["score_content_present"], "choir score-content presence")
    _cave_false(record["real_event_present"], "real choir event presence")
    return {
        "packet_token": record["packet_token"],
        "revision": revision,
        "source_pinned": True,
        "performance_authorized": False,
        "real_event_present": False,
        "valid": True,
    }


def validate_choir_section_topology(record: dict[str, Any]) -> dict[str, Any]:
    """Validate surrogate section links without classifying or identifying a singer."""

    _cave_record(
        record,
        {"sections", "singer_rows", "raw_identity_present", "vocal_classification_claimed"},
        "choir section topology",
    )
    sections = record["sections"]
    if not isinstance(sections, list) or not 2 <= len(sections) <= 16:
        raise DeltaError("choir section count is outside the bounded range")
    section_tokens = [_cave_token(value, "choir section token") for value in sections]
    ensure_unique(section_tokens, "choir section token")
    rows = record["singer_rows"]
    if not isinstance(rows, list) or not 2 <= len(rows) <= 64:
        raise DeltaError("choir singer-row count is outside the bounded range")
    singer_tokens: list[str] = []
    substitutions: list[tuple[str, str | None]] = []
    vacancies = 0
    for row in rows:
        _cave_record(
            row,
            {"singer_token", "section_token", "seat_group", "substitute_for", "vacant"},
            "choir singer row",
        )
        singer = _cave_token(row["singer_token"], "choir singer token")
        section = _cave_token(row["section_token"], "choir singer section")
        _cave_token(row["seat_group"], "choir seat-group token")
        if section not in section_tokens:
            raise DeltaError("choir singer row references an unknown section")
        substitute_for = row["substitute_for"]
        if substitute_for is not None:
            substitute_for = _cave_token(substitute_for, "choir substitute target")
        if not isinstance(row["vacant"], bool):
            raise DeltaError("choir vacancy state must be Boolean")
        vacancies += int(row["vacant"])
        singer_tokens.append(singer)
        substitutions.append((singer, substitute_for))
    ensure_unique(singer_tokens, "choir singer token")
    for singer, target in substitutions:
        if target is not None and (target not in singer_tokens or target == singer):
            raise DeltaError("choir substitute target is absent or self-referential")
    if vacancies < 1:
        raise DeltaError("choir topology hides every vacancy")
    _cave_false(record["raw_identity_present"], "raw choir identity presence")
    _cave_false(record["vocal_classification_claimed"], "vocal classification claim")
    return {
        "section_count": len(section_tokens),
        "singer_token_count": len(singer_tokens),
        "vacancy_count": vacancies,
        "raw_identity_present": False,
        "vocal_classification_claimed": False,
        "valid": True,
    }


def validate_choir_rehearsal_sequence(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a content-free fictional dependency sequence without directing rehearsal."""

    _cave_record(record, {"items", "rehearsal_authorized"}, "choir rehearsal sequence")
    items = record["items"]
    if not isinstance(items, list) or not 2 <= len(items) <= 32:
        raise DeltaError("choir rehearsal item count is outside the bounded range")
    seen: set[str] = set()
    incomplete_count = 0
    total_duration = 0.0
    for item in items:
        _cave_record(
            item,
            {
                "item_token",
                "kind",
                "duration_minutes",
                "prerequisites",
                "incomplete",
                "content_present",
                "instruction_provided",
            },
            "choir rehearsal item",
        )
        token = _cave_token(item["item_token"], "choir rehearsal item token")
        if token in seen:
            raise DeltaError("choir rehearsal item token is duplicated")
        if item["kind"] not in {"warmup_placeholder", "repertoire_placeholder", "review_placeholder"}:
            raise DeltaError("choir rehearsal item kind is unsupported")
        duration = _cave_finite(
            item["duration_minutes"],
            "choir rehearsal duration",
            minimum=0.0,
            maximum=240.0,
            minimum_inclusive=False,
        )
        prerequisites = item["prerequisites"]
        if not isinstance(prerequisites, list):
            raise DeltaError("choir rehearsal prerequisites are not a list")
        parsed_prerequisites = [
            _cave_token(value, "choir rehearsal prerequisite") for value in prerequisites
        ]
        ensure_unique(parsed_prerequisites, "choir rehearsal prerequisite")
        if any(value not in seen for value in parsed_prerequisites):
            raise DeltaError("choir rehearsal prerequisite is absent or forward-referenced")
        if not isinstance(item["incomplete"], bool):
            raise DeltaError("choir rehearsal incomplete state must be Boolean")
        incomplete_count += int(item["incomplete"])
        _cave_false(item["content_present"], "choir rehearsal content presence")
        _cave_false(item["instruction_provided"], "choir rehearsal instruction")
        seen.add(token)
        total_duration += duration
    if incomplete_count < 1:
        raise DeltaError("choir rehearsal sequence hides all incomplete work")
    _cave_false(record["rehearsal_authorized"], "real choir rehearsal authorization")
    return {
        "item_count": len(items),
        "incomplete_count": incomplete_count,
        "declared_duration_minutes": total_duration,
        "content_present": False,
        "rehearsal_authorized": False,
        "valid": True,
    }


def validate_choir_score_reference(record: dict[str, Any]) -> dict[str, Any]:
    """Validate tokenized score references while rejecting all musical content."""

    _cave_record(
        record,
        {
            "edition_token",
            "cue_token",
            "measure_reference",
            "page_reference",
            "rehearsal_mark",
            "annotation_tokens",
            "notation_present",
            "lyrics_present",
            "media_present",
            "authenticity_claimed",
            "rights_cleared",
        },
        "choir score reference",
    )
    _cave_token(record["edition_token"], "choir edition token")
    _cave_token(record["cue_token"], "choir cue token")
    for name in ("measure_reference", "page_reference"):
        value = _require_nonnegative_int(record[name], f"choir {name}")
        if not 1 <= value <= 1_000_000:
            raise DeltaError(f"choir {name} is outside the bounded range")
    mark = record["rehearsal_mark"]
    if not isinstance(mark, str) or re.fullmatch(r"[A-Za-z0-9_-]{1,32}", mark) is None:
        raise DeltaError("choir rehearsal mark is outside the bounded grammar")
    annotations = record["annotation_tokens"]
    if not isinstance(annotations, list) or not 1 <= len(annotations) <= 16:
        raise DeltaError("choir annotation-token count is invalid")
    annotation_tokens = [_cave_token(value, "choir annotation token") for value in annotations]
    ensure_unique(annotation_tokens, "choir annotation token")
    for field, label in (
        ("notation_present", "notation content"),
        ("lyrics_present", "lyrics content"),
        ("media_present", "media content"),
        ("authenticity_claimed", "score authenticity claim"),
        ("rights_cleared", "score rights-clearance claim"),
    ):
        _cave_false(record[field], label)
    return {
        "annotation_count": len(annotation_tokens),
        "musical_content_present": False,
        "authenticity_claimed": False,
        "rights_cleared": False,
        "valid": True,
    }


def validate_choir_tempo_domain(record: dict[str, Any]) -> dict[str, Any]:
    """Validate finite declaration placeholders without performance inference."""

    _cave_record(
        record,
        {
            "tempo_bpm",
            "metre",
            "beat_unit",
            "duration_minutes",
            "clock_source",
            "uncertainty_bpm",
            "performance_inference",
        },
        "choir tempo domain",
    )
    tempo = _cave_finite(
        record["tempo_bpm"], "choir tempo", minimum=1.0, maximum=400.0
    )
    duration = _cave_finite(
        record["duration_minutes"],
        "choir duration",
        minimum=0.0,
        maximum=240.0,
        minimum_inclusive=False,
    )
    uncertainty = _cave_finite(
        record["uncertainty_bpm"],
        "choir tempo uncertainty",
        minimum=0.0,
        maximum=100.0,
        minimum_inclusive=False,
    )
    if record["metre"] not in {"2/4", "3/4", "4/4", "6/8", "free_placeholder"}:
        raise DeltaError("choir metre is unsupported")
    if record["beat_unit"] not in {"quarter", "eighth", "half"}:
        raise DeltaError("choir beat unit is unsupported")
    if record["clock_source"] not in {"caller_supplied_utc", "synthetic_counter"}:
        raise DeltaError("choir clock source is unsupported")
    _cave_false(record["performance_inference"], "choir performance inference")
    return {
        "tempo_bpm": tempo,
        "duration_minutes": duration,
        "uncertainty_bpm": uncertainty,
        "performance_inference": False,
        "valid": True,
    }


def validate_choir_pitch_boundary(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a fictional pitch placeholder without personal vocal assessment."""

    _cave_record(
        record,
        {
            "pitch_hz",
            "unit",
            "transposition_semitones",
            "uncertainty_hz",
            "contradiction_state",
            "personal_range_present",
            "diagnosis_claimed",
            "placement_claimed",
        },
        "choir pitch boundary",
    )
    pitch = _cave_finite(
        record["pitch_hz"], "choir pitch", minimum=1.0, maximum=20_000.0
    )
    uncertainty = _cave_finite(
        record["uncertainty_hz"],
        "choir pitch uncertainty",
        minimum=0.0,
        maximum=1_000.0,
        minimum_inclusive=False,
    )
    if record["unit"] != "Hz":
        raise DeltaError("choir pitch unit must be Hz")
    transposition = record["transposition_semitones"]
    if isinstance(transposition, bool) or not isinstance(transposition, int) or not -24 <= transposition <= 24:
        raise DeltaError("choir transposition is outside the bounded integer range")
    if record["contradiction_state"] != "preserved_for_review":
        raise DeltaError("choir pitch contradiction is not preserved")
    _cave_false(record["personal_range_present"], "personal vocal-range presence")
    _cave_false(record["diagnosis_claimed"], "vocal diagnosis claim")
    _cave_false(record["placement_claimed"], "vocal placement claim")
    return {
        "pitch_hz": pitch,
        "uncertainty_hz": uncertainty,
        "transposition_semitones": transposition,
        "personal_range_present": False,
        "assessment_performed": False,
        "valid": True,
    }


def validate_choir_room_cue(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional unresolved room cues while refusing venue clearance."""

    _cave_record(
        record,
        {
            "zone_tokens",
            "occupancy_placeholder",
            "acoustic_cue",
            "noise_cue",
            "ventilation_state",
            "accessibility_route_state",
            "real_address_present",
            "safety_cleared",
            "accessibility_complete",
            "emergency_instruction",
        },
        "choir room cue",
    )
    zones = record["zone_tokens"]
    if not isinstance(zones, list) or not 1 <= len(zones) <= 16:
        raise DeltaError("choir room-zone count is invalid")
    zone_tokens = [_cave_token(value, "choir room-zone token") for value in zones]
    ensure_unique(zone_tokens, "choir room-zone token")
    occupancy = _require_nonnegative_int(
        record["occupancy_placeholder"], "choir occupancy placeholder"
    )
    if occupancy > 500:
        raise DeltaError("choir occupancy placeholder is over budget")
    if record["acoustic_cue"] not in {"unknown", "review_required"}:
        raise DeltaError("choir acoustic cue is not unresolved")
    if record["noise_cue"] not in {"unknown", "review_required"}:
        raise DeltaError("choir noise cue is not unresolved")
    if record["ventilation_state"] != "vacant_external_assessment":
        raise DeltaError("choir ventilation assessment is not vacant")
    if record["accessibility_route_state"] != "manual_review_required":
        raise DeltaError("choir accessibility route lacks manual review")
    for field, label in (
        ("real_address_present", "real room address presence"),
        ("safety_cleared", "room safety clearance"),
        ("accessibility_complete", "room accessibility completeness"),
        ("emergency_instruction", "room emergency instruction"),
    ):
        _cave_false(record[field], label)
    return {
        "zone_count": len(zone_tokens),
        "occupancy_placeholder": occupancy,
        "safety_cleared": False,
        "accessibility_complete": False,
        "real_address_present": False,
        "valid": True,
    }


def validate_choir_privacy(record: dict[str, Any]) -> dict[str, Any]:
    """Validate purpose-bound fictional placeholders with no real participation data."""

    _cave_record(
        record,
        {
            "availability_token",
            "attendance_state",
            "contact_channel",
            "purpose",
            "retention_days",
            "correction_state",
            "raw_identity_present",
            "participation_inferred",
            "secondary_purpose",
        },
        "choir privacy record",
    )
    _cave_token(record["availability_token"], "choir availability token")
    if record["attendance_state"] not in {"unknown_placeholder", "not_recorded"}:
        raise DeltaError("choir attendance state is not a nonparticipation placeholder")
    if record["contact_channel"] not in {"none", "surrogate_portal"}:
        raise DeltaError("choir contact-channel class is unsupported")
    if record["purpose"] != "synthetic_coordination":
        raise DeltaError("choir privacy purpose is unsupported")
    retention = _require_nonnegative_int(record["retention_days"], "choir retention days")
    if not 1 <= retention <= 365:
        raise DeltaError("choir retention period is outside the bounded range")
    if record["correction_state"] != "available_placeholder":
        raise DeltaError("choir correction state is not available")
    _cave_false(record["raw_identity_present"], "raw choir identity presence")
    _cave_false(record["participation_inferred"], "choir participation inference")
    _cave_false(record["secondary_purpose"], "choir secondary purpose")
    return {
        "retention_days": retention,
        "raw_identity_present": False,
        "participation_inferred": False,
        "privacy_complete": False,
        "valid": True,
    }


def validate_choir_rights_vacancy(record: dict[str, Any]) -> dict[str, Any]:
    """Validate an external-authority rights hold without granting any right."""

    _cave_record(
        record,
        {
            "source_token",
            "licence_basis_placeholder",
            "requested_actions",
            "effective_from",
            "expires_at",
            "permission_state",
            "rights_holder_confirmed",
            "content_present",
            "copy_authorized",
            "distribution_authorized",
            "recording_authorized",
            "streaming_authorized",
            "legal_interpretation",
        },
        "choir rights vacancy",
    )
    _cave_token(record["source_token"], "choir rights source token")
    if record["licence_basis_placeholder"] not in {"unknown", "external_review_required"}:
        raise DeltaError("choir licence-basis placeholder is unsupported")
    actions = record["requested_actions"]
    allowed = {"copy", "distribute", "record", "stream"}
    if not isinstance(actions, list) or not actions or any(value not in allowed for value in actions):
        raise DeltaError("choir requested rights actions are invalid")
    ensure_unique(actions, "choir requested rights action")
    start = _cave_timestamp(record["effective_from"], "choir rights effective-from")
    end = _cave_timestamp(record["expires_at"], "choir rights expiry")
    if end <= start or (end - start).total_seconds() > 10 * 366 * 86_400:
        raise DeltaError("choir rights interval is reversed or over budget")
    if record["permission_state"] != "authority_hold":
        raise DeltaError("choir permission state is not held for external authority")
    for field, label in (
        ("rights_holder_confirmed", "rights-holder confirmation"),
        ("content_present", "rights-record content presence"),
        ("copy_authorized", "copy authorization"),
        ("distribution_authorized", "distribution authorization"),
        ("recording_authorized", "recording authorization"),
        ("streaming_authorized", "streaming authorization"),
        ("legal_interpretation", "copyright legal interpretation"),
    ):
        _cave_false(record[field], label)
    return {
        "requested_action_count": len(actions),
        "permission_state": "authority_hold",
        "rights_granted": False,
        "legal_interpretation": False,
        "valid": True,
    }


def validate_choir_language_provenance(record: dict[str, Any]) -> dict[str, Any]:
    """Validate source-marked language placeholders without ratifying wording."""

    _cave_record(
        record,
        {
            "language_tag",
            "dialect_token",
            "pronunciation_source_token",
            "transliteration_state",
            "confidence",
            "correction_state",
            "cultural_context_state",
            "authority_vacant",
            "wording_ratified",
            "translation_quality_claimed",
            "maori_authority_claimed",
        },
        "choir language provenance",
    )
    tag = record["language_tag"]
    if not isinstance(tag, str) or re.fullmatch(r"(?:und|[a-z]{2,3}(?:-[A-Z]{2})?)", tag) is None:
        raise DeltaError("choir language tag is outside the bounded grammar")
    _cave_token(record["dialect_token"], "choir dialect token")
    _cave_token(record["pronunciation_source_token"], "choir pronunciation-source token")
    if record["transliteration_state"] not in {"not_supplied", "placeholder"}:
        raise DeltaError("choir transliteration state is unsupported")
    confidence = _cave_finite(
        record["confidence"], "choir language confidence", minimum=0.0, maximum=1.0
    )
    if record["correction_state"] not in {"open", "available_placeholder"}:
        raise DeltaError("choir language correction state is unsupported")
    if record["cultural_context_state"] != "external_review_required":
        raise DeltaError("choir cultural context is not reserved for external review")
    if record["authority_vacant"] is not True:
        raise DeltaError("choir language authority vacancy is not explicit")
    _cave_false(record["wording_ratified"], "choir wording ratification")
    _cave_false(record["translation_quality_claimed"], "translation quality claim")
    _cave_false(record["maori_authority_claimed"], "Maori authority claim")
    return {
        "language_tag": tag,
        "confidence": confidence,
        "authority_vacant": True,
        "wording_ratified": False,
        "maori_authority_claimed": False,
        "valid": True,
    }


def validate_choir_accessible_companion(record: dict[str, Any]) -> dict[str, Any]:
    """Validate structural alternatives while reserving every human evaluation."""

    _cave_record(
        record,
        {
            "headings",
            "text_alternative",
            "large_print_placeholder",
            "high_contrast_placeholder",
            "audio_description_state",
            "braille_request_state",
            "noncolour_status",
            "manual_review_required",
            "affected_user_reviewed",
            "accessibility_complete",
        },
        "choir accessible companion",
    )
    headings = record["headings"]
    if not isinstance(headings, list) or not 2 <= len(headings) <= 16:
        raise DeltaError("choir accessible heading count is invalid")
    if any(not isinstance(value, str) or not value.strip() or len(value) > 128 for value in headings):
        raise DeltaError("choir accessible heading is invalid")
    ensure_unique(headings, "choir accessible heading")
    alternative = record["text_alternative"]
    if not isinstance(alternative, str) or not alternative.strip() or len(alternative) > 2048:
        raise DeltaError("choir text alternative is absent or over budget")
    if record["large_print_placeholder"] is not True or record["high_contrast_placeholder"] is not True:
        raise DeltaError("choir accessible companion lacks visual placeholders")
    if record["audio_description_state"] not in {"requested_placeholder", "unavailable_placeholder"}:
        raise DeltaError("choir audio-description state is unsupported")
    if record["braille_request_state"] not in {"requested_placeholder", "pending_external"}:
        raise DeltaError("choir braille-request state is unsupported")
    if record["noncolour_status"] is not True or record["manual_review_required"] is not True:
        raise DeltaError("choir companion lacks noncolour status or manual review")
    _cave_false(record["affected_user_reviewed"], "affected-user accessibility review")
    _cave_false(record["accessibility_complete"], "accessibility completeness")
    return {
        "heading_count": len(headings),
        "manual_review_required": True,
        "affected_user_reviewed": False,
        "accessibility_complete": False,
        "valid": True,
    }


def validate_choir_correction_lineage(record: dict[str, Any]) -> dict[str, Any]:
    """Validate append-only fictional correction lineage without scheduling authority."""

    _cave_record(
        record,
        {"note_token", "records", "schedule_authorized", "real_event_present"},
        "choir correction lineage",
    )
    _cave_token(record["note_token"], "choir note token")
    rows = record["records"]
    if not isinstance(rows, list) or not 2 <= len(rows) <= 32:
        raise DeltaError("choir correction lineage is outside the bounded range")
    seen: set[str] = set()
    ambiguity_open = False
    for index, row in enumerate(rows):
        _cave_record(
            row,
            {
                "record_token",
                "parent_token",
                "event",
                "reason",
                "readback",
                "ambiguity_open",
                "cancellation_explicit",
            },
            "choir correction row",
        )
        token = _cave_token(row["record_token"], "choir correction token")
        parent = row["parent_token"]
        event = row["event"]
        if token in seen or parent == token:
            raise DeltaError("choir correction lineage duplicates or self-references a token")
        if index == 0:
            if parent is not None or event != "recorded":
                raise DeltaError("choir correction lineage lacks an original record")
        elif not isinstance(parent, str) or parent not in seen:
            raise DeltaError("choir correction parent is absent or forward-referenced")
        if event not in {"recorded", "corrected", "superseded", "cancelled", "ambiguity_retained"}:
            raise DeltaError("choir correction event is unsupported")
        reason = row["reason"]
        if not isinstance(reason, str) or len(reason) > 256 or reason != reason.strip():
            raise DeltaError("choir correction reason is invalid")
        if event != "recorded" and not reason:
            raise DeltaError("choir correction event lacks a reason")
        if event in {"corrected", "superseded", "cancelled"} and row["readback"] is not True:
            raise DeltaError("choir correction event lacks readback")
        if not isinstance(row["ambiguity_open"], bool) or not isinstance(row["cancellation_explicit"], bool):
            raise DeltaError("choir correction state flags must be Boolean")
        ambiguity_open = ambiguity_open or row["ambiguity_open"]
        seen.add(token)
    if not ambiguity_open:
        raise DeltaError("choir correction lineage hides unresolved ambiguity")
    _cave_false(record["schedule_authorized"], "choir schedule authorization")
    _cave_false(record["real_event_present"], "real choir event presence")
    return {
        "record_count": len(rows),
        "original_preserved": True,
        "ambiguity_open": True,
        "schedule_authorized": False,
        "valid": True,
    }


def validate_choir_wellbeing_cue(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional wellbeing cues while refusing diagnosis, treatment, or clearance."""

    _cave_record(
        record,
        {
            "cue_token",
            "cue_categories",
            "break_state",
            "stop_state",
            "referral_state",
            "medical_assessment",
            "psychosocial_assessment",
            "diagnosis",
            "treatment",
            "fitness_clearance",
            "forced_disclosure",
            "emergency_claim",
            "real_person_present",
        },
        "choir wellbeing cue",
    )
    _cave_token(record["cue_token"], "choir wellbeing cue token")
    categories = record["cue_categories"]
    allowed = {"fatigue_placeholder", "hearing_placeholder", "illness_vacancy", "psychosocial_vacancy"}
    if not isinstance(categories, list) or not categories or any(value not in allowed for value in categories):
        raise DeltaError("choir wellbeing cue categories are invalid")
    ensure_unique(categories, "choir wellbeing cue category")
    if record["break_state"] not in {"optional", "requested_placeholder"}:
        raise DeltaError("choir wellbeing break state is unsupported")
    if record["stop_state"] != "honoured_placeholder":
        raise DeltaError("choir wellbeing stop state is not dominant")
    if record["referral_state"] not in {"not_requested", "external_placeholder"}:
        raise DeltaError("choir wellbeing referral state is unsupported")
    for field, label in (
        ("medical_assessment", "medical assessment"),
        ("psychosocial_assessment", "psychosocial assessment"),
        ("diagnosis", "diagnosis"),
        ("treatment", "treatment"),
        ("fitness_clearance", "fitness clearance"),
        ("forced_disclosure", "forced disclosure"),
        ("emergency_claim", "emergency claim"),
        ("real_person_present", "real person presence"),
    ):
        _cave_false(record[field], label)
    return {
        "cue_category_count": len(categories),
        "stop_state": "honoured_placeholder",
        "assessment_performed": False,
        "real_person_present": False,
        "valid": True,
    }


def validate_choir_handover(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a fictional workload handover without evaluating or assigning a person."""

    _cave_record(
        record,
        {
            "handover_token",
            "queue_ceiling",
            "active_items",
            "unfinished_items",
            "stop_token",
            "correction_readback",
            "next_owner_placeholder",
            "performance_evaluated",
            "release_authorized",
            "real_person_present",
        },
        "choir workload handover",
    )
    _cave_token(record["handover_token"], "choir handover token")
    ceiling = _require_nonnegative_int(record["queue_ceiling"], "choir queue ceiling")
    if not 1 <= ceiling <= 100:
        raise DeltaError("choir queue ceiling is outside the bounded range")
    active = record["active_items"]
    unfinished = record["unfinished_items"]
    if not isinstance(active, list) or not active or len(active) > ceiling:
        raise DeltaError("choir active queue is empty or over its ceiling")
    if not isinstance(unfinished, list) or not unfinished:
        raise DeltaError("choir handover erases unfinished work")
    active_tokens = [_cave_token(value, "choir active item") for value in active]
    unfinished_tokens = [_cave_token(value, "choir unfinished item") for value in unfinished]
    ensure_unique(active_tokens, "choir active item")
    ensure_unique(unfinished_tokens, "choir unfinished item")
    if not set(unfinished_tokens) <= set(active_tokens):
        raise DeltaError("choir unfinished item is not in the active queue")
    if record["stop_token"] is not True or record["correction_readback"] is not True:
        raise DeltaError("choir handover lacks stop dominance or correction readback")
    _cave_token(record["next_owner_placeholder"], "choir next-owner placeholder")
    _cave_false(record["performance_evaluated"], "choir performance evaluation")
    _cave_false(record["release_authorized"], "choir operational release")
    _cave_false(record["real_person_present"], "real choir person presence")
    return {
        "queue_ceiling": ceiling,
        "active_count": len(active_tokens),
        "unfinished_count": len(unfinished_tokens),
        "performance_evaluated": False,
        "release_authorized": False,
        "valid": True,
    }


def merkle_root(entries: Iterable[dict[str, Any]]) -> str:
    leaves: list[bytes] = []
    for entry in sorted(entries, key=lambda row: row["path"]):
        stable = {
            "path": entry["path"],
            "status": entry["status"],
            "mode": entry.get("mode"),
            "git_blob": entry.get("git_blob"),
            "sha256": entry.get("sha256"),
        }
        leaves.append(hashlib.sha256(b"\x00" + canonical_json_bytes(stable)).digest())
    if not leaves:
        return sha256_bytes(b"")
    level = leaves
    while len(level) > 1:
        if len(level) % 2:
            level = [*level, level[-1]]
        level = [
            hashlib.sha256(b"\x01" + level[index] + level[index + 1]).digest()
            for index in range(0, len(level), 2)
        ]
    return level[0].hex()


def hardening_payload() -> dict[str, Any]:
    """Run Ilyra's bounded positive/negative synthetic hardening fixtures."""

    def rejection(identifier: str, label: str, callback: Any) -> dict[str, Any]:
        try:
            callback()
        except (DeltaError, UnicodeError, ValueError, TypeError) as exc:
            return {
                "fixture_id": identifier,
                "failed_witness": label,
                "rejected": True,
                "error_class": type(exc).__name__,
            }
        raise DeltaError(f"negative fixture was not rejected: {identifier}")

    records = [
        rejection(
            "I6626-HF-001",
            "expanded metadata over decompression budget",
            lambda: validate_decompression_budget(10, 101, 100, 20),
        ),
        rejection(
            "I6626-HF-002",
            "stored sparse size greater than logical size",
            lambda: sparse_size_record(10, 11),
        ),
        rejection(
            "I6626-HF-003",
            "archive symlink metadata",
            lambda: validate_archive_entry_kind("symlink"),
        ),
        rejection(
            "I6626-HF-004",
            "extended Windows device path",
            lambda: validate_windows_archive_reference(r"\\?\C:\escape.txt"),
        ),
        rejection(
            "I6626-HF-005",
            "percent-encoded parent URI member",
            lambda: normalize_uri_member_reference("safe/%2e%2e/escape.txt"),
        ),
        rejection(
            "I6626-HF-006",
            "leading-zero JSON number lexeme",
            lambda: validate_json_number_lexeme("01"),
        ),
        rejection(
            "I6626-HF-007",
            "schema-forbidden negative zero",
            lambda: validate_schema_finite_number(-0.0),
        ),
        rejection(
            "I6626-HF-008",
            "unknown content type",
            lambda: validate_media_type("application/octet-stream"),
        ),
        rejection(
            "I6626-HF-009",
            "attestation subject digest algorithm disagreement",
            lambda: validate_subject_digest_agreement(
                [{"name": "object.json", "digest": {"sha512": "00" * 64}}]
            ),
        ),
        rejection(
            "I6626-HF-010",
            "non-ASCII DSSE payload type outside the bounded subset",
            lambda: dsse_pae("application/vnd.ghc.mānuka", b"payload"),
        ),
        rejection(
            "I6626-HF-011",
            "unreviewed in-toto predicate version",
            lambda: validate_predicate_type(
                "https://example.invalid/ghc/synthetic-condition/v2"
            ),
        ),
        rejection(
            "I6626-HF-012",
            "negative monotonic duration",
            lambda: clock_separation_record(10, 9, -1),
        ),
        rejection(
            "I6626-HF-013",
            "offset-free timestamp",
            lambda: normalize_rfc3339_utc("2026-08-18T10:00:00"),
        ),
        rejection(
            "I6626-HF-014",
            "duplicate JSON Pointer target",
            lambda: validate_unique_json_pointer_targets(["/a~1b", "/a~1b"]),
        ),
    ]
    if not all(record.get("rejected") is True for record in records):
        raise DeltaError("one or more hardening negative fixtures was not detected")
    positive_checks = [
        validate_decompression_budget(10, 100, 100, 10)["decoder_invoked"] is False,
        sparse_size_record(100, 10)["file_materialized"] is False,
        validate_archive_entry_kind("regular_file") == "regular_file",
        validate_windows_archive_reference("safe/nested.txt") == "safe/nested.txt",
        normalize_uri_member_reference("safe/%7eitem.txt") == "safe/~item.txt",
        validate_json_number_lexeme("-1.25e+3") == "-1.25e+3",
        validate_schema_finite_number(1.25) == 1.25,
        validate_media_type("application/vnd.in-toto+json")
        == "application/vnd.in-toto+json",
        validate_subject_digest_agreement(
            [{"name": "object.json", "digest": {"sha256": "00" * 32}}]
        )["provenance_verified"]
        is False,
        dsse_pae("application/vnd.in-toto+json", b"payload")
        == b"DSSEv1 28 application/vnd.in-toto+json 7 payload",
        validate_predicate_type(
            "https://example.invalid/ghc/synthetic-condition/v1"
        )
        == "https://example.invalid/ghc/synthetic-condition/v1",
        clock_separation_record(10, 9, 1)["wall_clock_rollback_detected"] is True,
        normalize_rfc3339_utc("2026-08-18T22:00:00+12:00")
        == "2026-08-18T10:00:00Z",
        validate_unique_json_pointer_targets(["/condition", "/custody/state"])
        == ["/condition", "/custody/state"],
    ]
    if not all(positive_checks):
        raise DeltaError("one or more hardening passing fixtures failed")
    return {
        "schema": f"{SCHEMA}.hardening-fixtures.v2",
        "negative_fixture_count": len(records),
        "rejected_fixture_count": sum(
            record["rejected"] is True for record in records
        ),
        "positive_fixture_count": len(positive_checks),
        "passing_fixture_count": sum(bool(value) for value in positive_checks),
        "records": records,
        "signature_verified": False,
        "provenance_verified": False,
        "exhaustive_security": False,
        "valid": True,
        "boundary": "Bounded synthetic metadata, byte, path, numeric, attestation-shape, and time fixtures only; not decompression, sparse-file measurement, exhaustive platform safety, cryptographic verification, provenance truth, trusted time, production assurance, independent reproduction, professional validation, or authority.",
    }


def auren_hardening_payload() -> dict[str, Any]:
    """Run Auren's fourteen paired bounded synthetic hardening fixtures."""

    def rejection(identifier: str, label: str, callback: Any) -> dict[str, Any]:
        try:
            callback()
        except (DeltaError, UnicodeError, ValueError, TypeError) as exc:
            return {
                "fixture_id": identifier,
                "failed_witness": label,
                "rejected": True,
                "error_class": type(exc).__name__,
            }
        raise DeltaError(f"negative fixture was not rejected: {identifier}")

    primary = {
        "record_ids": ["object-001"],
        "schema_revision": "condition-v1",
        "content_revision": "7",
    }
    glossary = {
        "glossary_id": "condition-v1",
        "revision": "7",
        "terms": ["stable", "surface_change"],
    }
    records = [
        rejection("A6627-HF-001", "native byte order", lambda: validate_byte_order("native")),
        rejection(
            "A6627-HF-002",
            "permission bit outside the declared mask",
            lambda: normalize_permission_mode(0o1000, 0o777),
        ),
        rejection(
            "A6627-HF-003",
            "nested resource total over budget",
            lambda: validate_nested_resource_budget(
                [
                    {"depth": 1, "declared_bytes": 60},
                    {"depth": 2, "declared_bytes": 50},
                ],
                2,
                2,
                100,
            ),
        ),
        rejection(
            "A6627-HF-004",
            "declared size product over ceiling",
            lambda: checked_size_product(11, 10, 100),
        ),
        rejection(
            "A6627-HF-005",
            "URI member query component",
            lambda: validate_uri_member_components("safe/item.json?revision=1"),
        ),
        rejection(
            "A6627-HF-006",
            "duplicate media type parameter",
            lambda: parse_media_type_parameters(
                "application/vnd.in-toto+json; charset=utf-8; CHARSET=utf-8"
            ),
        ),
        rejection(
            "A6627-HF-007",
            "reserved digest algorithm",
            lambda: validate_digest_policy({"sha1": "00" * 20}),
        ),
        rejection(
            "A6627-HF-008",
            "non-ASCII DSSE payload type",
            lambda: validate_dsse_payload_type("application/vnd.ghc.mānuka"),
        ),
        rejection(
            "A6627-HF-009",
            "case-fold-colliding attestation subject names",
            lambda: validate_unique_attestation_subject_names(["Object", "object"]),
        ),
        rejection(
            "A6627-HF-010",
            "reserved leap-second timestamp",
            lambda: validate_rfc3339_leap_second_reservation("2016-12-31T23:59:60Z"),
        ),
        rejection(
            "A6627-HF-011",
            "leading-zero JSON Pointer array index",
            lambda: validate_json_pointer_array_index("01"),
        ),
        rejection(
            "A6627-HF-012",
            "alternative-format content revision mismatch",
            lambda: validate_revision_pair(
                primary,
                {**primary, "content_revision": "8"},
            ),
        ),
        rejection(
            "A6627-HF-013",
            "condition glossary revision mismatch",
            lambda: validate_condition_term_revision("stable", "condition-v1", "8", glossary),
        ),
        rejection(
            "A6627-HF-014",
            "custody transition while a hold is active",
            lambda: validate_custody_transition(
                "storage", "review", 2, 2, True, "registrar-a", "registrar-b"
            ),
        ),
    ]
    if not all(record.get("rejected") is True for record in records):
        raise DeltaError("one or more Auren hardening negative fixtures was not detected")
    positive_checks = [
        validate_byte_order("big") == "big",
        normalize_permission_mode(0o640)["filesystem_mutated"] is False,
        validate_nested_resource_budget(
            [
                {"depth": 1, "declared_bytes": 10},
                {"depth": 2, "declared_bytes": 20},
            ],
            2,
            2,
            30,
        )["total_declared_bytes"]
        == 30,
        checked_size_product(6, 7, 42) == 42,
        validate_uri_member_components("safe/item.json") == "safe/item.json",
        parse_media_type_parameters(
            "APPLICATION/VND.IN-TOTO+JSON; charset=UTF-8; version=1"
        )["content_opened"]
        is False,
        validate_digest_policy({"sha256": "00" * 32})[
            "cryptographic_validity_verified"
        ]
        is False,
        validate_dsse_payload_type("application/vnd.in-toto+json")
        == "application/vnd.in-toto+json",
        validate_unique_attestation_subject_names(["Object-A", "Object-B"])
        == ["Object-A", "Object-B"],
        validate_rfc3339_leap_second_reservation("2026-08-18T10:00:00Z")[
            "reserved_leap_second"
        ]
        is False,
        validate_json_pointer_array_index("10") == 10,
        validate_revision_pair(primary, dict(primary))["accessibility_complete"] is False,
        validate_condition_term_revision("stable", "condition-v1", "7", glossary)[
            "professional_authority"
        ]
        is False,
        validate_custody_transition(
            "storage", "review", 2, 2, False, "registrar-a", "registrar-b"
        )["custody_authority"]
        is False,
    ]
    if not all(positive_checks):
        raise DeltaError("one or more Auren hardening passing fixtures failed")
    return {
        "schema": f"{SCHEMA}.hardening-fixtures.v3",
        "profile": "auren-v662-v7",
        "negative_fixture_count": len(records),
        "rejected_fixture_count": sum(record["rejected"] is True for record in records),
        "positive_fixture_count": len(positive_checks),
        "passing_fixture_count": sum(bool(value) for value in positive_checks),
        "records": records,
        "binary_payload_parsed": False,
        "filesystem_mutated": False,
        "network_accessed": False,
        "signature_verified": False,
        "provenance_verified": False,
        "trusted_time": False,
        "accessibility_complete": False,
        "professional_authority": False,
        "cultural_authority": False,
        "exhaustive_security": False,
        "valid": True,
        "boundary": "Bounded synthetic declarations and paired refusal fixtures only; not binary parsing, filesystem authorization, resource allocation, URI dereference, content safety, cryptographic validity, provenance truth, trusted time, accessibility completeness, professional validation, legal or cultural ratification, Maori authority, production assurance, or independent reproduction.",
    }


def sable_hardening_payload() -> dict[str, Any]:
    """Run Sable's fourteen paired bounded synthetic hardening fixtures."""

    def rejection(identifier: str, label: str, callback: Any) -> dict[str, Any]:
        try:
            callback()
        except (DeltaError, UnicodeError, ValueError, TypeError) as exc:
            return {
                "fixture_id": identifier,
                "failed_witness": label,
                "rejected": True,
                "error_class": type(exc).__name__,
            }
        raise DeltaError(f"negative fixture was not rejected: {identifier}")

    records = [
        rejection(
            "S6628-HF-001",
            "unsupported RDFC algorithm declaration",
            lambda: validate_rdf_canonicalization_descriptor(
                {
                    "algorithm": "URDNA2015",
                    "hash_algorithm": "sha256",
                    "maximum_n_degree_calls": 100,
                    "dataset_present": False,
                    "canonical_output_present": False,
                }
            ),
        ),
        rejection(
            "S6628-HF-002",
            "SHACL conforming report carrying a result",
            lambda: validate_shacl_report_shape(
                {
                    "conforms": True,
                    "results": [
                        {
                            "severity": "sh:Violation",
                            "focus_node": "ex:item",
                            "source_constraint_component": "sh:ClassConstraintComponent",
                        }
                    ],
                }
            ),
        ),
        rejection(
            "S6628-HF-003",
            "SPARQL binding for undeclared variable",
            lambda: validate_sparql_result_bindings(
                {
                    "head": {"vars": ["item"]},
                    "results": {
                        "bindings": [
                            {"other": {"type": "literal", "value": "synthetic"}}
                        ]
                    },
                }
            ),
        ),
        rejection(
            "S6628-HF-004",
            "non-HTTPS DCAT download location",
            lambda: validate_dcat_distribution_descriptor(
                {
                    "access_urls": [],
                    "download_urls": ["http://example.invalid/data.json"],
                    "media_type": "application/json",
                    "checksum": {"algorithm": "sha256", "value": "00" * 32},
                }
            ),
        ),
        rejection(
            "S6628-HF-005",
            "OpenPGP signatures close in forward order",
            lambda: validate_openpgp_one_pass_sequence(
                [
                    "one_pass:alpha:more",
                    "one_pass:beta:last",
                    "literal",
                    "signature:alpha",
                    "signature:beta",
                ]
            ),
        ),
        rejection(
            "S6628-HF-006",
            "SSE identifier contains NUL",
            lambda: validate_sse_event_block(
                [
                    {"name": "data", "value": "synthetic"},
                    {"name": "id", "value": "bad\x00id"},
                ]
            ),
        ),
        rejection(
            "S6628-HF-007",
            "gRPC status outside the defined range",
            lambda: validate_grpc_status_trailers({"grpc-status": "17"}),
        ),
        rejection(
            "S6628-HF-008",
            "XMP document identifiers are duplicated",
            lambda: validate_xmp_identifier_lineage(
                {
                    "document_id": "xmp.did:item",
                    "instance_id": "xmp.did:item",
                    "original_document_id": "xmp.oid:origin",
                    "history": [
                        {"event_id": "evt-create", "parent_event_id": None, "action": "created"}
                    ],
                }
            ),
        ),
        rejection(
            "S6628-HF-009",
            "TTML cue references an unknown region",
            lambda: validate_ttml_time_expression(
                {
                    "begin": "0s",
                    "end": "2.5s",
                    "frame_rate": 30,
                    "tick_rate": 1000,
                    "region": "missing",
                    "known_regions": ["caption"],
                }
            ),
        ),
        rejection(
            "S6628-HF-010",
            "OpenTelemetry baggage key repeats",
            lambda: validate_otel_baggage_members(
                [
                    {"key": "trace.item", "value": "one", "properties": []},
                    {"key": "trace.item", "value": "two", "properties": []},
                ]
            ),
        ),
        rejection(
            "S6628-HF-011",
            "Authentication-Results carries an unknown result",
            lambda: validate_authentication_results_shape(
                {
                    "authserv_id": "mail.example.invalid",
                    "results": [{"method": "spf", "result": "maybe", "properties": {}}],
                }
            ),
        ),
        rejection(
            "S6628-HF-012",
            "MTA-STS jumps directly from none to enforce",
            lambda: validate_mta_sts_policy(
                {
                    "version": "STSv1",
                    "mode": "enforce",
                    "mx": ["mx.example.invalid"],
                    "max_age": 86400,
                    "previous_mode": "none",
                }
            ),
        ),
        rejection(
            "S6628-HF-013",
            "security.txt canonical URI uses HTTP",
            lambda: validate_security_txt_fields(
                {
                    "contact": ["mailto:security@example.invalid"],
                    "expires": "2030-01-01T00:00:00Z",
                    "canonical": ["http://example.invalid/.well-known/security.txt"],
                    "preferred_languages": ["en"],
                }
            ),
        ),
        rejection(
            "S6628-HF-014",
            "Problem Details extension collides with a core member",
            lambda: validate_problem_details_shape(
                {
                    "type": "about:blank",
                    "title": "Synthetic refusal",
                    "status": 400,
                    "extensions": {"Status": 401},
                }
            ),
        ),
    ]
    if not all(record.get("rejected") is True for record in records):
        raise DeltaError("one or more Sable hardening negative fixtures was not detected")

    positive_checks = [
        validate_rdf_canonicalization_descriptor(
            {
                "algorithm": "RDFC-1.0",
                "hash_algorithm": "sha256",
                "maximum_n_degree_calls": 100,
                "dataset_present": False,
                "canonical_output_present": False,
            }
        )["dataset_canonicalized"]
        is False,
        validate_shacl_report_shape(
            {
                "conforms": False,
                "results": [
                    {
                        "severity": "sh:Violation",
                        "focus_node": "ex:item",
                        "source_constraint_component": "sh:ClassConstraintComponent",
                        "result_path": "ex:kind",
                    }
                ],
            }
        )["graph_processed"]
        is False,
        validate_sparql_result_bindings(
            {
                "head": {"vars": ["item"]},
                "results": {
                    "bindings": [
                        {"item": {"type": "literal", "value": "synthetic"}}
                    ]
                },
            }
        )["query_executed"]
        is False,
        validate_dcat_distribution_descriptor(
            {
                "access_urls": ["https://example.invalid/catalog/item"],
                "download_urls": ["https://example.invalid/data/item.json"],
                "media_type": "application/json",
                "checksum": {"algorithm": "sha256", "value": "00" * 32},
            }
        )["url_dereferenced"]
        is False,
        validate_openpgp_one_pass_sequence(
            [
                "one_pass:alpha:more",
                "one_pass:beta:last",
                "literal",
                "signature:beta",
                "signature:alpha",
            ]
        )["signature_verified"]
        is False,
        validate_sse_event_block(
            [
                {"name": "event", "value": "update"},
                {"name": "id", "value": "evt-1"},
                {"name": "retry", "value": "1000"},
                {"name": "data", "value": "synthetic"},
            ]
        )["network_opened"]
        is False,
        validate_grpc_status_trailers(
            {
                "grpc-status": "5",
                "grpc-message": "not%20found",
                "grpc-status-details-bin": "YWJj",
            }
        )["rpc_invoked"]
        is False,
        validate_xmp_identifier_lineage(
            {
                "document_id": "xmp.did:document-1",
                "instance_id": "xmp.iid:instance-2",
                "original_document_id": "xmp.oid:original-1",
                "history": [
                    {"event_id": "evt-create", "parent_event_id": None, "action": "created"},
                    {"event_id": "evt-revise", "parent_event_id": "evt-create", "action": "revised"},
                ],
            }
        )["provenance_verified"]
        is False,
        validate_ttml_time_expression(
            {
                "begin": "0s",
                "end": "2.5s",
                "frame_rate": 30,
                "tick_rate": 1000,
                "region": "caption",
                "known_regions": ["caption"],
            }
        )["media_rendered"]
        is False,
        validate_otel_baggage_members(
            [{"key": "trace.item", "value": "synthetic%20value", "properties": ["privacy=bounded"]}]
        )["telemetry_propagated"]
        is False,
        validate_authentication_results_shape(
            {
                "authserv_id": "mail.example.invalid",
                "results": [
                    {"method": "spf", "result": "none", "properties": {"smtp.mailfrom": "example.invalid"}}
                ],
            }
        )["message_authenticated"]
        is False,
        validate_mta_sts_policy(
            {
                "version": "STSv1",
                "mode": "testing",
                "mx": ["mx.example.invalid"],
                "max_age": 86400,
                "previous_mode": "none",
            }
        )["policy_deployed"]
        is False,
        validate_security_txt_fields(
            {
                "contact": ["mailto:security@example.invalid"],
                "expires": "2030-01-01T00:00:00Z",
                "canonical": ["https://example.invalid/.well-known/security.txt"],
                "preferred_languages": ["en", "mi-NZ"],
            }
        )["published"]
        is False,
        validate_problem_details_shape(
            {
                "type": "about:blank",
                "title": "Synthetic refusal",
                "status": 400,
                "detail": "The bounded fixture was refused.",
                "instance": "/synthetic/problems/1",
                "extensions": {"retryable": False},
            }
        )["http_served"]
        is False,
    ]
    if not all(positive_checks):
        raise DeltaError("one or more Sable hardening passing fixtures failed")
    return {
        "schema": f"{SCHEMA}.hardening-fixtures.v4",
        "profile": "sable-v662-v8",
        "negative_fixture_count": len(records),
        "rejected_fixture_count": sum(record["rejected"] is True for record in records),
        "positive_fixture_count": len(positive_checks),
        "passing_fixture_count": sum(bool(value) for value in positive_checks),
        "records": records,
        "rdf_dataset_canonicalized": False,
        "graph_processed": False,
        "query_executed": False,
        "url_dereferenced": False,
        "signature_verified": False,
        "network_accessed": False,
        "media_rendered": False,
        "telemetry_propagated": False,
        "mail_authenticated": False,
        "policy_deployed": False,
        "privacy_complete": False,
        "accessibility_complete": False,
        "professional_authority": False,
        "cultural_authority": False,
        "exhaustive_security": False,
        "valid": True,
        "boundary": "Fourteen paired bounded synthetic descriptor and refusal fixtures only; not graph canonicalization, SHACL or SPARQL processing, URL dereference, OpenPGP parsing, cryptographic verification, stream or RPC execution, provenance truth, media rendering, telemetry transmission, mail authentication, policy deployment, vulnerability disclosure, privacy or accessibility completeness, professional validation, legal or cultural ratification, Maori authority, production assurance, or independent reproduction.",
    }


def caelen_fixture_cases() -> list[dict[str, Any]]:
    """Return Caelen's preregistered positive and five-per-proposal rejection cases."""

    topology = {
        "project_token": "project_alpha",
        "stations": ["s1", "s2", "s3"],
        "shots": [
            {"shot_token": "shot_1", "from_station": "s1", "to_station": "s2"},
            {"shot_token": "shot_2", "from_station": "s2", "to_station": "s3"},
        ],
        "root_station": "s1",
        "synthetic": True,
        "real_location_present": False,
    }
    measurement = {
        "bearing": 42.5,
        "inclination": -12.0,
        "distance": 8.25,
        "bearing_unit": "degree",
        "inclination_unit": "degree",
        "distance_unit": "m",
        "measurement_claimed": False,
    }
    instrument = {
        "instrument_token": "instrument_alpha",
        "calibration_reference": "cal-alpha",
        "effective_from": "2026-01-01T00:00:00Z",
        "effective_until": "2026-12-31T00:00:00Z",
        "uncertainty": 0.5,
        "calibration_status": "current",
        "calibration_authority_claimed": False,
    }
    lrud = {
        "station_token": "s1",
        "left": 1.0,
        "right": 2.0,
        "up": None,
        "down": 0.5,
        "omissions": ["up"],
        "navigable_geometry": False,
    }
    loop = {
        "station_sequence": ["s1", "s2", "s3", "s1"],
        "residual": {"x": 0.1, "y": -0.1, "z": 0.05},
        "residual_unit": "m",
        "adjustment_method": "least_squares_reserved",
        "adjustment_applied": False,
        "accuracy_claimed": False,
    }
    location = {
        "location_token": "location_alpha",
        "datum_label": "NZGD2000",
        "precision_class": "region_only",
        "purpose": "authority_hold",
        "disclosure_state": "withheld",
        "review_hold": True,
    }
    feature = {
        "feature_token": "feature_alpha",
        "feature_class": "habitat",
        "sensitivity": "high",
        "location_state": "withheld",
        "redaction_reason": "Synthetic sensitive-feature reservation.",
        "review_authority_class": "affected_authority",
        "release_authorized": False,
        "real_feature": False,
    }
    equipment = {
        "equipment_token": "equipment_alpha",
        "equipment_class": "anchor",
        "observations": ["visual_placeholder", "unresolved_placeholder"],
        "unresolved": ["unresolved_placeholder"],
        "safety_assessed": False,
        "use_authorized": False,
        "instruction_provided": False,
    }
    condition = {
        "cue_token": "cue_alpha",
        "source_class": "fictional_observation",
        "observed_at": "2026-08-18T00:00:00Z",
        "expires_at": "2026-08-18T06:00:00Z",
        "uncertainty": "high",
        "entry_state": "hold",
        "forecast_made": False,
        "live_feed": False,
        "entry_authorized": False,
    }
    sensor = {
        "sensor_token": "sensor_alpha",
        "unit": "ppm",
        "value": 20.0,
        "uncertainty": 1.0,
        "calibration_state": "current_placeholder",
        "live_sensor": False,
        "atmosphere_cleared": False,
        "threshold_advice": False,
    }
    callout = {
        "team_token": "team_alpha",
        "callout_token": "callout_alpha",
        "due_at": "2026-08-18T02:00:00Z",
        "checked_at": None,
        "state": "overdue_hold",
        "escalation_state": "awaiting_competent_review",
        "live_tracking": False,
        "automated_dispatch": False,
        "raw_identity_present": False,
    }
    incident = {
        "incident_token": "incident_alpha",
        "records": [
            {"record_token": "record_1", "parent_token": None, "event": "reported"},
            {"record_token": "record_2", "parent_token": "record_1", "event": "corrected"},
        ],
        "closure_authorized": False,
        "real_person_data": False,
    }
    accessible = {
        "document_token": "document_alpha",
        "headings": ["Scope", "Synthetic station summary", "Review hold"],
        "station_summaries": [
            {"station_token": "s1", "summary": "Synthetic station token; no route or location."}
        ],
        "text_alternative": "A fictional graph has three station tokens and two unlocated edges.",
        "noncolour_status": True,
        "manual_review_required": True,
        "accessibility_complete": False,
        "raw_location_present": False,
        "imperative_route_instruction": False,
    }
    handover = {
        "handover_token": "handover_alpha",
        "queue_ceiling": 3,
        "active_items": ["item_a", "item_b"],
        "unfinished_items": ["item_b"],
        "stop_token": True,
        "correction_readback": True,
        "next_owner_acknowledged": True,
        "release_authorized": False,
        "real_operator": False,
    }
    return [
        {
            "fixture_id": "CA6631-HF-001",
            "proposal_id": "CA6631-N001",
            "validator": "validate_cave_station_shot_topology",
            "positive": topology,
            "mutations": [
                {"label": "duplicate cave station token", "record": {**topology, "stations": ["s1", "s1"]}},
                {"label": "unknown cave shot endpoint", "record": {**topology, "shots": [{"shot_token": "shot_1", "from_station": "s1", "to_station": "missing"}]}},
                {"label": "cave shot self-loop", "record": {**topology, "shots": [{"shot_token": "shot_1", "from_station": "s1", "to_station": "s1"}]}},
                {"label": "disconnected cave station", "record": {**topology, "shots": [{"shot_token": "shot_1", "from_station": "s1", "to_station": "s2"}]}},
                {"label": "real cave location flag", "record": {**topology, "real_location_present": True}},
            ],
        },
        {
            "fixture_id": "CA6631-HF-002",
            "proposal_id": "CA6631-N002",
            "validator": "validate_cave_measurement_domain",
            "positive": measurement,
            "mutations": [
                {"label": "nonfinite cave bearing", "record": {**measurement, "bearing": float("nan")}},
                {"label": "Boolean cave bearing", "record": {**measurement, "bearing": True}},
                {"label": "out-of-range cave bearing", "record": {**measurement, "bearing": 360.0}},
                {"label": "out-of-range cave inclination", "record": {**measurement, "inclination": 91.0}},
                {"label": "nonpositive cave distance", "record": {**measurement, "distance": 0.0}},
            ],
        },
        {
            "fixture_id": "CA6631-HF-003",
            "proposal_id": "CA6631-N003",
            "validator": "validate_cave_instrument_lineage",
            "positive": instrument,
            "mutations": [
                {"label": "missing calibration lineage field", "record": {key: value for key, value in instrument.items() if key != "calibration_reference"}},
                {"label": "reversed calibration interval", "record": {**instrument, "effective_from": "2026-12-31T00:00:00Z", "effective_until": "2026-01-01T00:00:00Z"}},
                {"label": "stale calibration status", "record": {**instrument, "calibration_status": "stale"}},
                {"label": "zero calibration uncertainty", "record": {**instrument, "uncertainty": 0.0}},
                {"label": "calibration authority claim", "record": {**instrument, "calibration_authority_claimed": True}},
            ],
        },
        {
            "fixture_id": "CA6631-HF-004",
            "proposal_id": "CA6631-N004",
            "validator": "validate_cave_passage_lrud",
            "positive": lrud,
            "mutations": [
                {"label": "negative LRUD offset", "record": {**lrud, "left": -1.0}},
                {"label": "nonfinite LRUD offset", "record": {**lrud, "right": float("inf")}},
                {"label": "undeclared LRUD omission", "record": {**lrud, "omissions": []}},
                {"label": "numeric LRUD field marked omitted", "record": {**lrud, "omissions": ["up", "left"]}},
                {"label": "navigable cave geometry claim", "record": {**lrud, "navigable_geometry": True}},
            ],
        },
        {
            "fixture_id": "CA6631-HF-005",
            "proposal_id": "CA6631-N005",
            "validator": "validate_cave_loop_closure",
            "positive": loop,
            "mutations": [
                {"label": "open cave loop", "record": {**loop, "station_sequence": ["s1", "s2", "s3", "s4"]}},
                {"label": "adjacent repeated loop station", "record": {**loop, "station_sequence": ["s1", "s2", "s2", "s1"]}},
                {"label": "nonfinite loop residual", "record": {**loop, "residual": {"x": float("nan"), "y": 0.0, "z": 0.0}}},
                {"label": "unsupported adjustment method", "record": {**loop, "adjustment_method": "automatic"}},
                {"label": "coordinate adjustment applied", "record": {**loop, "adjustment_applied": True}},
            ],
        },
        {
            "fixture_id": "CA6631-HF-006",
            "proposal_id": "CA6631-N006",
            "validator": "validate_cave_location_minimization",
            "positive": location,
            "mutations": [
                {"label": "raw cave latitude field", "record": {**location, "latitude": -41.0}},
                {"label": "raw cave address field", "record": {**location, "address": "withheld"}},
                {"label": "exact cave precision class", "record": {**location, "precision_class": "exact"}},
                {"label": "public cave disclosure state", "record": {**location, "disclosure_state": "public"}},
                {"label": "removed cave location review hold", "record": {**location, "review_hold": False}},
            ],
        },
        {
            "fixture_id": "CA6631-HF-007",
            "proposal_id": "CA6631-N007",
            "validator": "validate_cave_sensitive_feature",
            "positive": feature,
            "mutations": [
                {"label": "raw sensitive-feature location field", "record": {**feature, "raw_location": "withheld"}},
                {"label": "public sensitive-feature classification", "record": {**feature, "sensitivity": "public"}},
                {"label": "missing redaction reason", "record": {**feature, "redaction_reason": ""}},
                {"label": "unauthorized sensitive-feature release", "record": {**feature, "release_authorized": True}},
                {"label": "real sensitive feature assertion", "record": {**feature, "real_feature": True}},
            ],
        },
        {
            "fixture_id": "CA6631-HF-008",
            "proposal_id": "CA6631-N008",
            "validator": "validate_cave_equipment_observation",
            "positive": equipment,
            "mutations": [
                {"label": "equipment load-rating field", "record": {**equipment, "load_rating": 10}},
                {"label": "equipment safety assessment claim", "record": {**equipment, "safety_assessed": True}},
                {"label": "equipment use authorization claim", "record": {**equipment, "use_authorized": True}},
                {"label": "equipment instruction claim", "record": {**equipment, "instruction_provided": True}},
                {"label": "erased unresolved equipment item", "record": {**equipment, "unresolved": []}},
            ],
        },
        {
            "fixture_id": "CA6631-HF-009",
            "proposal_id": "CA6631-N009",
            "validator": "validate_cave_condition_cue",
            "positive": condition,
            "mutations": [
                {"label": "reversed condition-cue interval", "record": {**condition, "expires_at": "2026-08-17T23:00:00Z"}},
                {"label": "condition forecast claim", "record": {**condition, "forecast_made": True}},
                {"label": "live condition feed claim", "record": {**condition, "live_feed": True}},
                {"label": "cave entry authorization claim", "record": {**condition, "entry_authorized": True}},
                {"label": "go-state condition cue", "record": {**condition, "entry_state": "go"}},
            ],
        },
        {
            "fixture_id": "CA6631-HF-010",
            "proposal_id": "CA6631-N010",
            "validator": "validate_cave_atmosphere_sensor",
            "positive": sensor,
            "mutations": [
                {"label": "unsupported cave sensor unit", "record": {**sensor, "unit": "unknown"}},
                {"label": "nonfinite cave sensor value", "record": {**sensor, "value": float("inf")}},
                {"label": "zero cave sensor uncertainty", "record": {**sensor, "uncertainty": 0.0}},
                {"label": "stale cave sensor calibration", "record": {**sensor, "calibration_state": "stale"}},
                {"label": "atmosphere clearance claim", "record": {**sensor, "atmosphere_cleared": True}},
            ],
        },
        {
            "fixture_id": "CA6631-HF-011",
            "proposal_id": "CA6631-N011",
            "validator": "validate_cave_callout_state",
            "positive": callout,
            "mutations": [
                {"label": "raw callout identity", "record": {**callout, "raw_identity_present": True}},
                {"label": "live callout tracking", "record": {**callout, "live_tracking": True}},
                {"label": "automated callout dispatch", "record": {**callout, "automated_dispatch": True}},
                {"label": "overdue callout without review hold", "record": {**callout, "escalation_state": "not_required"}},
                {"label": "checked-in callout without timestamp", "record": {**callout, "state": "checked_in", "escalation_state": "not_required"}},
            ],
        },
        {
            "fixture_id": "CA6631-HF-012",
            "proposal_id": "CA6631-N012",
            "validator": "validate_cave_incident_lineage",
            "positive": incident,
            "mutations": [
                {"label": "duplicate incident record token", "record": {**incident, "records": [{"record_token": "record_1", "parent_token": None, "event": "reported"}, {"record_token": "record_1", "parent_token": "record_1", "event": "corrected"}]}},
                {"label": "forward incident parent reference", "record": {**incident, "records": [{"record_token": "record_1", "parent_token": None, "event": "reported"}, {"record_token": "record_2", "parent_token": "record_3", "event": "corrected"}]}},
                {"label": "self-referencing incident correction", "record": {**incident, "records": [{"record_token": "record_1", "parent_token": None, "event": "reported"}, {"record_token": "record_2", "parent_token": "record_2", "event": "corrected"}]}},
                {"label": "incident lineage without original report", "record": {**incident, "records": [{"record_token": "record_1", "parent_token": None, "event": "corrected"}]}},
                {"label": "incident closure authorization claim", "record": {**incident, "closure_authorized": True}},
            ],
        },
        {
            "fixture_id": "CA6631-HF-013",
            "proposal_id": "CA6631-N013",
            "validator": "validate_cave_accessible_companion",
            "positive": accessible,
            "mutations": [
                {"label": "missing accessible headings", "record": {**accessible, "headings": []}},
                {"label": "missing cave text alternative", "record": {**accessible, "text_alternative": ""}},
                {"label": "colour-only cave status", "record": {**accessible, "noncolour_status": False}},
                {"label": "accessibility-complete claim", "record": {**accessible, "accessibility_complete": True}},
                {"label": "imperative cave route instruction", "record": {**accessible, "imperative_route_instruction": True}},
            ],
        },
        {
            "fixture_id": "CA6631-HF-014",
            "proposal_id": "CA6631-N014",
            "validator": "validate_cave_handover",
            "positive": handover,
            "mutations": [
                {"label": "cave queue over ceiling", "record": {**handover, "queue_ceiling": 1}},
                {"label": "unknown unfinished cave item", "record": {**handover, "unfinished_items": ["item_missing"]}},
                {"label": "cave stop token overridden", "record": {**handover, "stop_token": False}},
                {"label": "missing cave correction readback", "record": {**handover, "correction_readback": False}},
                {"label": "operational cave release claim", "record": {**handover, "release_authorized": True}},
            ],
        },
    ]


def _caelen_validators() -> dict[str, Any]:
    return {
        function.__name__: function
        for function in (
            validate_cave_station_shot_topology,
            validate_cave_measurement_domain,
            validate_cave_instrument_lineage,
            validate_cave_passage_lrud,
            validate_cave_loop_closure,
            validate_cave_location_minimization,
            validate_cave_sensitive_feature,
            validate_cave_equipment_observation,
            validate_cave_condition_cue,
            validate_cave_atmosphere_sensor,
            validate_cave_callout_state,
            validate_cave_incident_lineage,
            validate_cave_accessible_companion,
            validate_cave_handover,
        )
    }


def caelen_mutation_payload() -> dict[str, Any]:
    """Execute all five preregistered rejecting mutations for each completed proposal."""

    validators = _caelen_validators()
    records: list[dict[str, Any]] = []
    positives: list[dict[str, Any]] = []
    for case_index, case in enumerate(caelen_fixture_cases(), 1):
        validator = validators[case["validator"]]
        positive = validator(case["positive"])
        if positive.get("valid") is not True:
            raise DeltaError(f"Caelen positive fixture failed: {case['fixture_id']}")
        positives.append(
            {
                "proposal_id": case["proposal_id"],
                "validator": case["validator"],
                "valid": True,
            }
        )
        mutations = case["mutations"]
        if len(mutations) != 5:
            raise DeltaError(f"Caelen fixture does not declare five mutations: {case['fixture_id']}")
        for mutation_index, mutation in enumerate(mutations, 1):
            try:
                validator(mutation["record"])
            except (DeltaError, UnicodeError, ValueError, TypeError) as exc:
                records.append(
                    {
                        "mutation_id": f"CA6631-MUT-{case_index:03d}-{mutation_index:02d}",
                        "proposal_id": case["proposal_id"],
                        "validator": case["validator"],
                        "failed_witness": mutation["label"],
                        "rejected": True,
                        "error_class": type(exc).__name__,
                        "zero_credit": True,
                    }
                )
            else:
                raise DeltaError(
                    f"Caelen negative mutation was not rejected: {case['fixture_id']}:{mutation_index}"
                )
    return {
        "schema": f"{SCHEMA}.caelen-mutation-matrix.v1",
        "profile": "caelen-v663-v1",
        "proposal_count": len(positives),
        "mutations_per_proposal": 5,
        "negative_fixture_count": len(records),
        "rejected_fixture_count": sum(record["rejected"] is True for record in records),
        "positive_fixture_count": len(positives),
        "passing_fixture_count": len(positives),
        "records": records,
        "positive_records": positives,
        "failed_witnesses_erased": 0,
        "valid": len(records) == 70 and len(positives) == 14,
        "boundary": "Seventy rejected synthetic mutations and fourteen passing record-shape fixtures only; no real cave, measurement, location, person, sensor, safety decision, authority, empirical result, production result or independent reproduction.",
    }


def caelen_hardening_payload() -> dict[str, Any]:
    """Run one primary rejecting mutation and one pass for each Caelen validator."""

    matrix = caelen_mutation_payload()
    primary_by_proposal = {record["proposal_id"]: record for record in matrix["records"] if record["mutation_id"].endswith("-01")}
    records = []
    for case in caelen_fixture_cases():
        primary = primary_by_proposal[case["proposal_id"]]
        records.append(
            {
                "fixture_id": case["fixture_id"],
                "failed_witness": primary["failed_witness"],
                "rejected": True,
                "error_class": primary["error_class"],
            }
        )
    if len(records) != 14 or not all(record["rejected"] is True for record in records):
        raise DeltaError("one or more Caelen hardening fixtures was not rejected")
    return {
        "schema": f"{SCHEMA}.hardening-fixtures.v5",
        "profile": "caelen-v663-v1",
        "negative_fixture_count": len(records),
        "rejected_fixture_count": len(records),
        "positive_fixture_count": matrix["positive_fixture_count"],
        "passing_fixture_count": matrix["passing_fixture_count"],
        "records": records,
        "full_mutation_matrix_negative_count": matrix["negative_fixture_count"],
        "real_cave_accessed": False,
        "survey_computed": False,
        "measurement_claimed": False,
        "real_location_present": False,
        "live_sensor_used": False,
        "safety_assessed": False,
        "entry_authorized": False,
        "emergency_dispatched": False,
        "privacy_complete": False,
        "accessibility_complete": False,
        "professional_authority": False,
        "cultural_authority": False,
        "maori_authority": False,
        "exhaustive_security": False,
        "valid": True,
        "boundary": "Fourteen primary and seventy total paired bounded synthetic cave-record refusal fixtures only; not caving, surveying, measurement, location publication, live monitoring, safety clearance, rescue, professional validation, legal or cultural ratification, Māori authority, production assurance or independent reproduction.",
    }


def orin_fixture_cases() -> list[dict[str, Any]]:
    """Return Orin's positive choir fixtures and five rejections per completed proposal."""

    packet = {
        "packet_token": "packet_alpha",
        "revision": 1,
        "source_pin": "sha256:" + "00" * 32,
        "cancellation_state": "hold",
        "performance_authorized": False,
        "synthetic": True,
        "lyrics_present": False,
        "score_content_present": False,
        "real_event_present": False,
    }
    topology = {
        "sections": ["section_a", "section_b"],
        "singer_rows": [
            {
                "singer_token": "singer_a",
                "section_token": "section_a",
                "seat_group": "seat_a",
                "substitute_for": None,
                "vacant": False,
            },
            {
                "singer_token": "singer_b",
                "section_token": "section_b",
                "seat_group": "seat_b",
                "substitute_for": None,
                "vacant": True,
            },
        ],
        "raw_identity_present": False,
        "vocal_classification_claimed": False,
    }
    sequence = {
        "items": [
            {
                "item_token": "item_a",
                "kind": "warmup_placeholder",
                "duration_minutes": 10.0,
                "prerequisites": [],
                "incomplete": False,
                "content_present": False,
                "instruction_provided": False,
            },
            {
                "item_token": "item_b",
                "kind": "review_placeholder",
                "duration_minutes": 15.0,
                "prerequisites": ["item_a"],
                "incomplete": True,
                "content_present": False,
                "instruction_provided": False,
            },
        ],
        "rehearsal_authorized": False,
    }
    score = {
        "edition_token": "edition_alpha",
        "cue_token": "cue_alpha",
        "measure_reference": 12,
        "page_reference": 3,
        "rehearsal_mark": "mark_a",
        "annotation_tokens": ["annotation_a", "annotation_b"],
        "notation_present": False,
        "lyrics_present": False,
        "media_present": False,
        "authenticity_claimed": False,
        "rights_cleared": False,
    }
    tempo = {
        "tempo_bpm": 96.0,
        "metre": "4/4",
        "beat_unit": "quarter",
        "duration_minutes": 20.0,
        "clock_source": "synthetic_counter",
        "uncertainty_bpm": 2.0,
        "performance_inference": False,
    }
    pitch = {
        "pitch_hz": 440.0,
        "unit": "Hz",
        "transposition_semitones": 0,
        "uncertainty_hz": 0.5,
        "contradiction_state": "preserved_for_review",
        "personal_range_present": False,
        "diagnosis_claimed": False,
        "placement_claimed": False,
    }
    room = {
        "zone_tokens": ["zone_a", "zone_b"],
        "occupancy_placeholder": 0,
        "acoustic_cue": "review_required",
        "noise_cue": "unknown",
        "ventilation_state": "vacant_external_assessment",
        "accessibility_route_state": "manual_review_required",
        "real_address_present": False,
        "safety_cleared": False,
        "accessibility_complete": False,
        "emergency_instruction": False,
    }
    privacy = {
        "availability_token": "availability_alpha",
        "attendance_state": "unknown_placeholder",
        "contact_channel": "none",
        "purpose": "synthetic_coordination",
        "retention_days": 30,
        "correction_state": "available_placeholder",
        "raw_identity_present": False,
        "participation_inferred": False,
        "secondary_purpose": False,
    }
    rights = {
        "source_token": "source_alpha",
        "licence_basis_placeholder": "external_review_required",
        "requested_actions": ["copy", "record"],
        "effective_from": "2026-01-01T00:00:00Z",
        "expires_at": "2026-12-31T00:00:00Z",
        "permission_state": "authority_hold",
        "rights_holder_confirmed": False,
        "content_present": False,
        "copy_authorized": False,
        "distribution_authorized": False,
        "recording_authorized": False,
        "streaming_authorized": False,
        "legal_interpretation": False,
    }
    language = {
        "language_tag": "und",
        "dialect_token": "dialect_unknown",
        "pronunciation_source_token": "source_unknown",
        "transliteration_state": "not_supplied",
        "confidence": 0.25,
        "correction_state": "open",
        "cultural_context_state": "external_review_required",
        "authority_vacant": True,
        "wording_ratified": False,
        "translation_quality_claimed": False,
        "maori_authority_claimed": False,
    }
    accessible = {
        "headings": ["Scope", "Synthetic alternatives", "Review vacancies"],
        "text_alternative": "A fictional content-free rehearsal packet has two placeholder items.",
        "large_print_placeholder": True,
        "high_contrast_placeholder": True,
        "audio_description_state": "unavailable_placeholder",
        "braille_request_state": "pending_external",
        "noncolour_status": True,
        "manual_review_required": True,
        "affected_user_reviewed": False,
        "accessibility_complete": False,
    }
    correction = {
        "note_token": "note_alpha",
        "records": [
            {
                "record_token": "record_a",
                "parent_token": None,
                "event": "recorded",
                "reason": "",
                "readback": False,
                "ambiguity_open": True,
                "cancellation_explicit": False,
            },
            {
                "record_token": "record_b",
                "parent_token": "record_a",
                "event": "corrected",
                "reason": "Synthetic correction placeholder.",
                "readback": True,
                "ambiguity_open": True,
                "cancellation_explicit": False,
            },
        ],
        "schedule_authorized": False,
        "real_event_present": False,
    }
    wellbeing = {
        "cue_token": "wellbeing_alpha",
        "cue_categories": ["fatigue_placeholder", "hearing_placeholder"],
        "break_state": "optional",
        "stop_state": "honoured_placeholder",
        "referral_state": "not_requested",
        "medical_assessment": False,
        "psychosocial_assessment": False,
        "diagnosis": False,
        "treatment": False,
        "fitness_clearance": False,
        "forced_disclosure": False,
        "emergency_claim": False,
        "real_person_present": False,
    }
    handover = {
        "handover_token": "handover_alpha",
        "queue_ceiling": 3,
        "active_items": ["item_a", "item_b"],
        "unfinished_items": ["item_b"],
        "stop_token": True,
        "correction_readback": True,
        "next_owner_placeholder": "owner_next",
        "performance_evaluated": False,
        "release_authorized": False,
        "real_person_present": False,
    }
    return [
        {
            "fixture_id": "OR6632-HF-001",
            "proposal_id": "OR6632-N001",
            "validator": "validate_choir_packet_identity",
            "positive": packet,
            "mutations": [
                {"label": "zero choir packet revision", "record": {**packet, "revision": 0}},
                {"label": "non-SHA256 choir source pin", "record": {**packet, "source_pin": "sha1:00"}},
                {"label": "choir performance authorization claim", "record": {**packet, "performance_authorized": True}},
                {"label": "choir lyrics presence", "record": {**packet, "lyrics_present": True}},
                {"label": "real choir event presence", "record": {**packet, "real_event_present": True}},
            ],
        },
        {
            "fixture_id": "OR6632-HF-002",
            "proposal_id": "OR6632-N002",
            "validator": "validate_choir_section_topology",
            "positive": topology,
            "mutations": [
                {"label": "duplicate choir section token", "record": {**topology, "sections": ["section_a", "section_a"]}},
                {"label": "duplicate choir singer token", "record": {**topology, "singer_rows": [topology["singer_rows"][0], {**topology["singer_rows"][1], "singer_token": "singer_a"}]}},
                {"label": "unknown choir section reference", "record": {**topology, "singer_rows": [{**topology["singer_rows"][0], "section_token": "section_missing"}, topology["singer_rows"][1]]}},
                {"label": "raw choir identity flag", "record": {**topology, "raw_identity_present": True}},
                {"label": "vocal classification claim", "record": {**topology, "vocal_classification_claimed": True}},
            ],
        },
        {
            "fixture_id": "OR6632-HF-003",
            "proposal_id": "OR6632-N003",
            "validator": "validate_choir_rehearsal_sequence",
            "positive": sequence,
            "mutations": [
                {"label": "forward choir rehearsal prerequisite", "record": {**sequence, "items": [{**sequence["items"][0], "prerequisites": ["item_b"]}, sequence["items"][1]]}},
                {"label": "duplicate choir rehearsal item", "record": {**sequence, "items": [sequence["items"][0], {**sequence["items"][1], "item_token": "item_a"}]}},
                {"label": "zero choir rehearsal duration", "record": {**sequence, "items": [{**sequence["items"][0], "duration_minutes": 0.0}, sequence["items"][1]]}},
                {"label": "choir rehearsal content presence", "record": {**sequence, "items": [sequence["items"][0], {**sequence["items"][1], "content_present": True}]}},
                {"label": "choir rehearsal instruction claim", "record": {**sequence, "items": [{**sequence["items"][0], "instruction_provided": True}, sequence["items"][1]]}},
            ],
        },
        {
            "fixture_id": "OR6632-HF-004",
            "proposal_id": "OR6632-N004",
            "validator": "validate_choir_score_reference",
            "positive": score,
            "mutations": [
                {"label": "zero choir measure reference", "record": {**score, "measure_reference": 0}},
                {"label": "duplicate choir annotation token", "record": {**score, "annotation_tokens": ["annotation_a", "annotation_a"]}},
                {"label": "score notation content presence", "record": {**score, "notation_present": True}},
                {"label": "score authenticity claim", "record": {**score, "authenticity_claimed": True}},
                {"label": "score rights-clearance claim", "record": {**score, "rights_cleared": True}},
            ],
        },
        {
            "fixture_id": "OR6632-HF-005",
            "proposal_id": "OR6632-N005",
            "validator": "validate_choir_tempo_domain",
            "positive": tempo,
            "mutations": [
                {"label": "nonfinite choir tempo", "record": {**tempo, "tempo_bpm": float("nan")}},
                {"label": "nonpositive choir tempo", "record": {**tempo, "tempo_bpm": 0.0}},
                {"label": "nonpositive choir duration", "record": {**tempo, "duration_minutes": 0.0}},
                {"label": "unsupported choir beat unit", "record": {**tempo, "beat_unit": "tick"}},
                {"label": "choir performance inference", "record": {**tempo, "performance_inference": True}},
            ],
        },
        {
            "fixture_id": "OR6632-HF-006",
            "proposal_id": "OR6632-N006",
            "validator": "validate_choir_pitch_boundary",
            "positive": pitch,
            "mutations": [
                {"label": "nonfinite choir pitch", "record": {**pitch, "pitch_hz": float("inf")}},
                {"label": "unsupported choir pitch unit", "record": {**pitch, "unit": "kHz"}},
                {"label": "Boolean choir transposition", "record": {**pitch, "transposition_semitones": True}},
                {"label": "personal vocal-range presence", "record": {**pitch, "personal_range_present": True}},
                {"label": "vocal placement claim", "record": {**pitch, "placement_claimed": True}},
            ],
        },
        {
            "fixture_id": "OR6632-HF-007",
            "proposal_id": "OR6632-N007",
            "validator": "validate_choir_room_cue",
            "positive": room,
            "mutations": [
                {"label": "missing choir room zone", "record": {**room, "zone_tokens": []}},
                {"label": "choir occupancy placeholder over budget", "record": {**room, "occupancy_placeholder": 501}},
                {"label": "choir ventilation clearance", "record": {**room, "ventilation_state": "cleared"}},
                {"label": "choir room safety clearance", "record": {**room, "safety_cleared": True}},
                {"label": "real choir room address", "record": {**room, "real_address_present": True}},
            ],
        },
        {
            "fixture_id": "OR6632-HF-008",
            "proposal_id": "OR6632-N008",
            "validator": "validate_choir_privacy",
            "positive": privacy,
            "mutations": [
                {"label": "raw choir identity presence", "record": {**privacy, "raw_identity_present": True}},
                {"label": "choir participation inference", "record": {**privacy, "participation_inferred": True}},
                {"label": "choir secondary purpose", "record": {**privacy, "secondary_purpose": True}},
                {"label": "zero choir retention period", "record": {**privacy, "retention_days": 0}},
                {"label": "raw choir email field", "record": {**privacy, "email": "withheld@example.invalid"}},
            ],
        },
        {
            "fixture_id": "OR6632-HF-009",
            "proposal_id": "OR6632-N009",
            "validator": "validate_choir_rights_vacancy",
            "positive": rights,
            "mutations": [
                {"label": "duplicate choir requested right", "record": {**rights, "requested_actions": ["copy", "copy"]}},
                {"label": "reversed choir rights interval", "record": {**rights, "expires_at": "2025-12-31T00:00:00Z"}},
                {"label": "choir permission grant", "record": {**rights, "permission_state": "granted"}},
                {"label": "choir copy authorization", "record": {**rights, "copy_authorized": True}},
                {"label": "choir copyright interpretation", "record": {**rights, "legal_interpretation": True}},
            ],
        },
        {
            "fixture_id": "OR6632-HF-010",
            "proposal_id": "OR6632-N010",
            "validator": "validate_choir_language_provenance",
            "positive": language,
            "mutations": [
                {"label": "invalid choir language tag", "record": {**language, "language_tag": "invalid_tag"}},
                {"label": "choir language confidence over range", "record": {**language, "confidence": 1.5}},
                {"label": "hidden choir language authority vacancy", "record": {**language, "authority_vacant": False}},
                {"label": "choir wording ratification", "record": {**language, "wording_ratified": True}},
                {"label": "choir Maori authority claim", "record": {**language, "maori_authority_claimed": True}},
            ],
        },
        {
            "fixture_id": "OR6632-HF-011",
            "proposal_id": "OR6632-N011",
            "validator": "validate_choir_accessible_companion",
            "positive": accessible,
            "mutations": [
                {"label": "missing choir accessible headings", "record": {**accessible, "headings": []}},
                {"label": "missing choir text alternative", "record": {**accessible, "text_alternative": ""}},
                {"label": "missing choir high-contrast placeholder", "record": {**accessible, "high_contrast_placeholder": False}},
                {"label": "unsupported affected-user review claim", "record": {**accessible, "affected_user_reviewed": True}},
                {"label": "choir accessibility-complete claim", "record": {**accessible, "accessibility_complete": True}},
            ],
        },
        {
            "fixture_id": "OR6632-HF-012",
            "proposal_id": "OR6632-N012",
            "validator": "validate_choir_correction_lineage",
            "positive": correction,
            "mutations": [
                {"label": "duplicate choir correction token", "record": {**correction, "records": [correction["records"][0], {**correction["records"][1], "record_token": "record_a"}]}},
                {"label": "forward choir correction parent", "record": {**correction, "records": [correction["records"][0], {**correction["records"][1], "parent_token": "record_missing"}]}},
                {"label": "choir lineage without original record", "record": {**correction, "records": [{**correction["records"][0], "event": "corrected"}, correction["records"][1]]}},
                {"label": "choir correction without reason", "record": {**correction, "records": [correction["records"][0], {**correction["records"][1], "reason": ""}]}},
                {"label": "choir correction without readback", "record": {**correction, "records": [correction["records"][0], {**correction["records"][1], "readback": False}]}},
            ],
        },
        {
            "fixture_id": "OR6632-HF-013",
            "proposal_id": "OR6632-N013",
            "validator": "validate_choir_wellbeing_cue",
            "positive": wellbeing,
            "mutations": [
                {"label": "unsupported choir wellbeing category", "record": {**wellbeing, "cue_categories": ["diagnosis"]}},
                {"label": "choir stop state overridden", "record": {**wellbeing, "stop_state": "ignored"}},
                {"label": "choir diagnosis claim", "record": {**wellbeing, "diagnosis": True}},
                {"label": "forced choir disclosure", "record": {**wellbeing, "forced_disclosure": True}},
                {"label": "real choir person presence", "record": {**wellbeing, "real_person_present": True}},
            ],
        },
        {
            "fixture_id": "OR6632-HF-014",
            "proposal_id": "OR6632-N014",
            "validator": "validate_choir_handover",
            "positive": handover,
            "mutations": [
                {"label": "choir queue over ceiling", "record": {**handover, "queue_ceiling": 1}},
                {"label": "unknown unfinished choir item", "record": {**handover, "unfinished_items": ["item_missing"]}},
                {"label": "choir stop token overridden", "record": {**handover, "stop_token": False}},
                {"label": "missing choir correction readback", "record": {**handover, "correction_readback": False}},
                {"label": "choir performance evaluation claim", "record": {**handover, "performance_evaluated": True}},
            ],
        },
    ]


def _orin_validators() -> dict[str, Any]:
    return {
        function.__name__: function
        for function in (
            validate_choir_packet_identity,
            validate_choir_section_topology,
            validate_choir_rehearsal_sequence,
            validate_choir_score_reference,
            validate_choir_tempo_domain,
            validate_choir_pitch_boundary,
            validate_choir_room_cue,
            validate_choir_privacy,
            validate_choir_rights_vacancy,
            validate_choir_language_provenance,
            validate_choir_accessible_companion,
            validate_choir_correction_lineage,
            validate_choir_wellbeing_cue,
            validate_choir_handover,
        )
    }


def orin_mutation_payload() -> dict[str, Any]:
    """Execute all five preregistered rejecting mutations for each Orin completion."""

    validators = _orin_validators()
    records: list[dict[str, Any]] = []
    positives: list[dict[str, Any]] = []
    for case_index, case in enumerate(orin_fixture_cases(), 1):
        validator = validators[case["validator"]]
        positive = validator(case["positive"])
        if positive.get("valid") is not True:
            raise DeltaError(f"Orin positive fixture failed: {case['fixture_id']}")
        positives.append(
            {
                "proposal_id": case["proposal_id"],
                "validator": case["validator"],
                "valid": True,
            }
        )
        mutations = case["mutations"]
        if len(mutations) != 5:
            raise DeltaError(f"Orin fixture does not declare five mutations: {case['fixture_id']}")
        for mutation_index, mutation in enumerate(mutations, 1):
            try:
                validator(mutation["record"])
            except (DeltaError, UnicodeError, ValueError, TypeError) as exc:
                records.append(
                    {
                        "fixture_id": f"OR6632-HF-{case_index:03d}-{mutation_index:02d}",
                        "mutation_id": f"OR6632-MUT-{case_index:03d}-{mutation_index:02d}",
                        "proposal_id": case["proposal_id"],
                        "validator": case["validator"],
                        "failed_witness": mutation["label"],
                        "rejected": True,
                        "error_class": type(exc).__name__,
                        "zero_credit": True,
                    }
                )
            else:
                raise DeltaError(
                    f"Orin negative mutation was not rejected: {case['fixture_id']}:{mutation_index}"
                )
    return {
        "schema": f"{SCHEMA}.orin-mutation-matrix.v1",
        "profile": "orin-v663-v2",
        "proposal_count": len(positives),
        "mutations_per_proposal": 5,
        "negative_fixture_count": len(records),
        "rejected_fixture_count": sum(record["rejected"] is True for record in records),
        "positive_fixture_count": len(positives),
        "passing_fixture_count": len(positives),
        "records": records,
        "positive_records": positives,
        "failed_witnesses_erased": 0,
        "valid": len(records) == 70 and len(positives) == 14,
        "boundary": "Seventy rejected synthetic mutations and fourteen passing content-free choir record-shape fixtures only; no real person, choir, repertoire, venue, rehearsal, performance, right, language decision, cultural decision, health assessment, empirical result, production result, authority act or independent reproduction.",
    }


def orin_hardening_payload() -> dict[str, Any]:
    """Return every retained Orin rejection plus the fourteen paired positives."""

    matrix = orin_mutation_payload()
    if not matrix["valid"]:
        raise DeltaError("one or more Orin hardening fixtures failed")
    return {
        "schema": f"{SCHEMA}.hardening-fixtures.v6",
        "profile": "orin-v663-v2",
        "negative_fixture_count": matrix["negative_fixture_count"],
        "rejected_fixture_count": matrix["rejected_fixture_count"],
        "positive_fixture_count": matrix["positive_fixture_count"],
        "passing_fixture_count": matrix["passing_fixture_count"],
        "records": matrix["records"],
        "full_mutation_matrix_negative_count": matrix["negative_fixture_count"],
        "real_person_present": False,
        "real_choir_present": False,
        "lyrics_present": False,
        "score_content_present": False,
        "real_repertoire_present": False,
        "real_venue_present": False,
        "rehearsal_authorized": False,
        "performance_authorized": False,
        "rights_granted": False,
        "health_assessed": False,
        "privacy_complete": False,
        "accessibility_complete": False,
        "professional_authority": False,
        "legal_authority": False,
        "cultural_authority": False,
        "maori_authority": False,
        "exhaustive_security": False,
        "valid": True,
        "boundary": "All seventy preregistered choir mutations were rejected and fourteen paired positives passed as bounded content-free software fixtures only; not rehearsal, performance, vocal assessment, health or safety clearance, rights permission, legal interpretation, cultural ratification, Maori authority, privacy or accessibility completeness, production assurance, empirical evidence or independent reproduction.",
    }


def _garden_required_false(record: dict[str, Any], fields: Iterable[str]) -> None:
    """Require explicit false values for garden authority and real-world flags."""

    for field in fields:
        _cave_false(record[field], f"garden {field.replace('_', ' ')}")


def validate_garden_season_packet(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a fictional season packet while refusing cultivation authority."""

    _cave_record(
        record,
        {
            "season_token",
            "revision",
            "source_pin",
            "cancellation_state",
            "synthetic",
            "cultivation_authorized",
            "real_site_present",
            "raw_identity_present",
        },
        "garden season packet",
    )
    _cave_token(record["season_token"], "garden season token")
    revision = _require_nonnegative_int(record["revision"], "garden season revision")
    if not 1 <= revision <= 10_000:
        raise DeltaError("garden season revision is outside the bounded range")
    source_pin = record["source_pin"]
    if not isinstance(source_pin, str) or re.fullmatch(r"sha256:[0-9a-f]{64}", source_pin) is None:
        raise DeltaError("garden season source pin is not an explicit SHA-256 commitment")
    if record["cancellation_state"] not in {"active_placeholder", "cancelled_placeholder", "hold"}:
        raise DeltaError("garden season cancellation state is unsupported")
    if record["synthetic"] is not True:
        raise DeltaError("garden season packet must remain explicitly synthetic")
    _garden_required_false(
        record,
        ("cultivation_authorized", "real_site_present", "raw_identity_present"),
    )
    return {
        "season_token": record["season_token"],
        "revision": revision,
        "source_pinned": True,
        "cultivation_authorized": False,
        "real_site_present": False,
        "valid": True,
    }


def validate_garden_plot_topology(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a fictional plot graph without location, land, or build claims."""

    _cave_record(
        record,
        {"nodes", "real_location_present", "land_right_claimed", "construction_released"},
        "garden plot topology",
    )
    nodes = record["nodes"]
    if not isinstance(nodes, list) or not 3 <= len(nodes) <= 32:
        raise DeltaError("garden plot-node count is outside the bounded range")
    allowed_kinds = {"plot", "raised_bed", "row", "path", "compost_bay", "water_point"}
    seen: set[str] = set()
    kinds: Counter[str] = Counter()
    for index, node in enumerate(nodes):
        _cave_record(node, {"node_token", "kind", "parent_token"}, "garden plot node")
        token = _cave_token(node["node_token"], "garden plot-node token")
        if token in seen:
            raise DeltaError("garden plot-node token is duplicated")
        kind = node["kind"]
        if kind not in allowed_kinds:
            raise DeltaError("garden plot-node kind is unsupported")
        parent = node["parent_token"]
        if index == 0:
            if parent is not None or kind != "plot":
                raise DeltaError("garden topology lacks a root plot")
        elif not isinstance(parent, str) or parent not in seen:
            raise DeltaError("garden plot-node parent is absent or forward-referenced")
        seen.add(token)
        kinds[kind] += 1
    if kinds["path"] < 1 or kinds["raised_bed"] < 1:
        raise DeltaError("garden topology lacks a path or raised-bed placeholder")
    _garden_required_false(
        record,
        ("real_location_present", "land_right_claimed", "construction_released"),
    )
    return {
        "node_count": len(nodes),
        "kind_counts": dict(sorted(kinds.items())),
        "real_location_present": False,
        "land_right_claimed": False,
        "valid": True,
    }


def validate_garden_seed_lot(record: dict[str, Any]) -> dict[str, Any]:
    """Validate surrogate seed-lot lineage without botanical or custody claims."""

    _cave_record(
        record,
        {
            "lots",
            "real_organism_present",
            "authenticity_claimed",
            "viability_claimed",
            "custody_claimed",
        },
        "garden seed-lot ledger",
    )
    lots = record["lots"]
    if not isinstance(lots, list) or not 2 <= len(lots) <= 16:
        raise DeltaError("garden seed-lot count is outside the bounded range")
    seen: set[str] = set()
    holds = 0
    for lot in lots:
        _cave_record(
            lot,
            {"lot_token", "label_token", "source_token", "substitution_for", "quarantine_state"},
            "garden seed-lot row",
        )
        token = _cave_token(lot["lot_token"], "garden seed-lot token")
        if token in seen:
            raise DeltaError("garden seed-lot token is duplicated")
        _cave_token(lot["label_token"], "garden plant-label token")
        _cave_token(lot["source_token"], "garden seed source token")
        substitution = lot["substitution_for"]
        if substitution is not None and (
            not isinstance(substitution, str) or substitution not in seen
        ):
            raise DeltaError("garden seed substitution target is absent or forward-referenced")
        if lot["quarantine_state"] not in {"hold", "review_required"}:
            raise DeltaError("garden seed-lot quarantine is not retained")
        holds += 1
        seen.add(token)
    _garden_required_false(
        record,
        ("real_organism_present", "authenticity_claimed", "viability_claimed", "custody_claimed"),
    )
    return {
        "lot_count": len(lots),
        "quarantine_count": holds,
        "real_organism_present": False,
        "botanical_assessment_performed": False,
        "valid": True,
    }


def validate_garden_activity_plan(record: dict[str, Any]) -> dict[str, Any]:
    """Validate content-free activity dependencies without agronomic direction."""

    _cave_record(record, {"items", "work_authorized"}, "garden activity plan")
    items = record["items"]
    if not isinstance(items, list) or not 2 <= len(items) <= 32:
        raise DeltaError("garden activity count is outside the bounded range")
    allowed_kinds = {"sowing_placeholder", "transplant_placeholder", "rotation_placeholder", "review_placeholder"}
    seen: set[str] = set()
    incomplete = 0
    for item in items:
        _cave_record(
            item,
            {
                "activity_token",
                "kind",
                "window_start",
                "window_end",
                "dependencies",
                "incomplete",
                "instruction_provided",
                "recommendation_provided",
            },
            "garden activity row",
        )
        token = _cave_token(item["activity_token"], "garden activity token")
        if token in seen:
            raise DeltaError("garden activity token is duplicated")
        if item["kind"] not in allowed_kinds:
            raise DeltaError("garden activity kind is unsupported")
        start = _cave_timestamp(item["window_start"], "garden activity window start")
        end = _cave_timestamp(item["window_end"], "garden activity window end")
        if end <= start or (end - start).total_seconds() > 366 * 86_400:
            raise DeltaError("garden activity window is reversed or over budget")
        dependencies = item["dependencies"]
        if not isinstance(dependencies, list):
            raise DeltaError("garden activity dependencies are not a list")
        parsed = [_cave_token(value, "garden activity dependency") for value in dependencies]
        ensure_unique(parsed, "garden activity dependency")
        if any(value not in seen for value in parsed):
            raise DeltaError("garden activity dependency is absent or forward-referenced")
        if not isinstance(item["incomplete"], bool):
            raise DeltaError("garden activity incomplete state must be Boolean")
        incomplete += int(item["incomplete"])
        _garden_required_false(item, ("instruction_provided", "recommendation_provided"))
        seen.add(token)
    if incomplete < 1:
        raise DeltaError("garden activity plan hides all incomplete work")
    _cave_false(record["work_authorized"], "garden work authorization")
    return {
        "activity_count": len(items),
        "incomplete_count": incomplete,
        "instruction_provided": False,
        "work_authorized": False,
        "valid": True,
    }


def validate_garden_soil_observation(record: dict[str, Any]) -> dict[str, Any]:
    """Validate finite fictional soil placeholders without a soil conclusion."""

    _cave_record(
        record,
        {
            "sample_token",
            "depth_cm",
            "ph_placeholder",
            "nutrient_placeholder",
            "nutrient_unit",
            "uncertainty",
            "contamination_cue",
            "real_sample_present",
            "fertility_inference",
            "contamination_diagnosis",
        },
        "garden soil observation",
    )
    _cave_token(record["sample_token"], "garden sample token")
    depth = _cave_finite(record["depth_cm"], "garden depth", minimum=0.0, maximum=500.0, minimum_inclusive=False)
    ph = _cave_finite(record["ph_placeholder"], "garden pH placeholder", minimum=0.0, maximum=14.0)
    nutrient = _cave_finite(record["nutrient_placeholder"], "garden nutrient placeholder", minimum=0.0, maximum=1_000.0)
    uncertainty = _cave_finite(record["uncertainty"], "garden soil uncertainty", minimum=0.0, maximum=1_000.0, minimum_inclusive=False)
    if record["nutrient_unit"] != "synthetic_index":
        raise DeltaError("garden nutrient unit is unsupported")
    if record["contamination_cue"] not in {"unknown", "review_required"}:
        raise DeltaError("garden contamination cue is not unresolved")
    _garden_required_false(
        record,
        ("real_sample_present", "fertility_inference", "contamination_diagnosis"),
    )
    return {
        "depth_cm": depth,
        "ph_placeholder": ph,
        "nutrient_placeholder": nutrient,
        "uncertainty": uncertainty,
        "real_sample_present": False,
        "inference_performed": False,
        "valid": True,
    }


def validate_garden_compost_input(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional compost batches while refusing clearance or application."""

    _cave_record(
        record,
        {"batches", "real_material_present", "safety_cleared", "application_authorized"},
        "garden compost input",
    )
    batches = record["batches"]
    if not isinstance(batches, list) or not 1 <= len(batches) <= 16:
        raise DeltaError("garden compost batch count is invalid")
    allowed_classes = {"green_placeholder", "brown_placeholder", "amendment_placeholder"}
    seen: set[str] = set()
    total = 0.0
    for batch in batches:
        _cave_record(
            batch,
            {"batch_token", "material_class", "source_token", "quantity", "unit", "maturity_state", "contamination_state"},
            "garden compost batch",
        )
        token = _cave_token(batch["batch_token"], "garden compost batch token")
        if token in seen:
            raise DeltaError("garden compost batch token is duplicated")
        if batch["material_class"] not in allowed_classes:
            raise DeltaError("garden compost material class is unsupported")
        _cave_token(batch["source_token"], "garden compost source token")
        quantity = _cave_finite(batch["quantity"], "garden compost quantity", minimum=0.0, maximum=1_000.0, minimum_inclusive=False)
        if batch["unit"] != "synthetic_kg":
            raise DeltaError("garden compost unit is unsupported")
        if batch["maturity_state"] != "external_review_required":
            raise DeltaError("garden compost maturity is not vacant")
        if batch["contamination_state"] not in {"unknown", "review_required"}:
            raise DeltaError("garden compost contamination state is not unresolved")
        seen.add(token)
        total += quantity
    _garden_required_false(record, ("real_material_present", "safety_cleared", "application_authorized"))
    return {
        "batch_count": len(batches),
        "declared_quantity": total,
        "maturity_assessed": False,
        "application_authorized": False,
        "valid": True,
    }


def validate_garden_irrigation_reservation(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional irrigation bounds while reserving water authority."""

    _cave_record(
        record,
        {
            "zone_token",
            "source_state",
            "volume_liters",
            "interval_start",
            "interval_end",
            "leak_cue",
            "restriction_state",
            "real_water_source_present",
            "allocation_authorized",
            "operation_authorized",
        },
        "garden irrigation reservation",
    )
    _cave_token(record["zone_token"], "garden irrigation zone token")
    if record["source_state"] != "surrogate_unverified":
        raise DeltaError("garden irrigation source is not explicitly unverified")
    volume = _cave_finite(record["volume_liters"], "garden irrigation volume", minimum=0.0, maximum=100_000.0, minimum_inclusive=False)
    start = _cave_timestamp(record["interval_start"], "garden irrigation interval start")
    end = _cave_timestamp(record["interval_end"], "garden irrigation interval end")
    if end <= start or (end - start).total_seconds() > 31 * 86_400:
        raise DeltaError("garden irrigation interval is reversed or over budget")
    if record["leak_cue"] not in {"unknown", "review_required"}:
        raise DeltaError("garden irrigation leak cue is unsupported")
    if record["restriction_state"] != "external_review_required":
        raise DeltaError("garden irrigation restriction state is not externally reserved")
    _garden_required_false(
        record,
        ("real_water_source_present", "allocation_authorized", "operation_authorized"),
    )
    return {
        "zone_token": record["zone_token"],
        "volume_liters": volume,
        "allocation_authorized": False,
        "operation_authorized": False,
        "valid": True,
    }


def validate_garden_tool_reservation(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional tool state while refusing inspection, competence, and release."""

    _cave_record(
        record,
        {"tools", "real_tool_present", "inspected", "competence_claimed", "safety_cleared", "use_released"},
        "garden tool reservation",
    )
    tools = record["tools"]
    if not isinstance(tools, list) or not 1 <= len(tools) <= 16:
        raise DeltaError("garden tool count is invalid")
    seen: set[str] = set()
    for tool in tools:
        _cave_record(
            tool,
            {"tool_token", "condition_state", "isolation_token", "sharps_state"},
            "garden tool row",
        )
        token = _cave_token(tool["tool_token"], "garden tool token")
        if token in seen:
            raise DeltaError("garden tool token is duplicated")
        if tool["condition_state"] not in {"unknown", "review_required"}:
            raise DeltaError("garden tool condition is not unresolved")
        _cave_token(tool["isolation_token"], "garden tool isolation token")
        if tool["sharps_state"] not in {"not_applicable", "review_required"}:
            raise DeltaError("garden tool sharps state is unsupported")
        seen.add(token)
    _garden_required_false(
        record,
        ("real_tool_present", "inspected", "competence_claimed", "safety_cleared", "use_released"),
    )
    return {
        "tool_count": len(tools),
        "inspected": False,
        "competence_claimed": False,
        "use_released": False,
        "valid": True,
    }


def validate_garden_privacy_notice(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a purpose-bound fictional notice with no participation data."""

    _cave_record(
        record,
        {
            "availability_token",
            "membership_state",
            "contact_channel",
            "purpose",
            "retention_days",
            "correction_state",
            "raw_identity_present",
            "participation_inferred",
            "secondary_purpose",
        },
        "garden privacy notice",
    )
    _cave_token(record["availability_token"], "garden availability token")
    if record["membership_state"] not in {"unknown_placeholder", "not_recorded"}:
        raise DeltaError("garden membership state is not a nonparticipation placeholder")
    if record["contact_channel"] not in {"none", "surrogate_portal"}:
        raise DeltaError("garden contact channel is unsupported")
    if record["purpose"] != "synthetic_coordination":
        raise DeltaError("garden privacy purpose is unsupported")
    retention = _require_nonnegative_int(record["retention_days"], "garden retention days")
    if not 1 <= retention <= 365:
        raise DeltaError("garden retention period is outside the bounded range")
    if record["correction_state"] != "available_placeholder":
        raise DeltaError("garden correction state is not available")
    _garden_required_false(record, ("raw_identity_present", "participation_inferred", "secondary_purpose"))
    return {
        "retention_days": retention,
        "raw_identity_present": False,
        "participation_inferred": False,
        "privacy_complete": False,
        "valid": True,
    }


def validate_garden_accessible_layout(record: dict[str, Any]) -> dict[str, Any]:
    """Validate structural alternatives while reserving physical and human review."""

    _cave_record(
        record,
        {
            "headings",
            "text_alternative",
            "path_state",
            "reach_state",
            "surface_state",
            "gradient_placeholder",
            "signage_placeholder",
            "seating_placeholder",
            "alternative_format",
            "noncolour_status",
            "manual_review_required",
            "physical_access_confirmed",
            "affected_user_reviewed",
            "accessibility_complete",
        },
        "garden accessible layout",
    )
    headings = record["headings"]
    if not isinstance(headings, list) or not 2 <= len(headings) <= 16:
        raise DeltaError("garden accessible heading count is invalid")
    if any(not isinstance(value, str) or not value.strip() or len(value) > 128 for value in headings):
        raise DeltaError("garden accessible heading is invalid")
    ensure_unique(headings, "garden accessible heading")
    alternative = record["text_alternative"]
    if not isinstance(alternative, str) or not alternative.strip() or len(alternative) > 2048:
        raise DeltaError("garden text alternative is absent or over budget")
    for field in ("path_state", "reach_state", "surface_state"):
        if record[field] != "manual_review_required":
            raise DeltaError(f"garden {field} lacks manual review")
    gradient = _cave_finite(record["gradient_placeholder"], "garden gradient placeholder", minimum=0.0, maximum=1.0)
    if record["signage_placeholder"] is not True or record["seating_placeholder"] is not True:
        raise DeltaError("garden accessibility placeholders are missing")
    if record["alternative_format"] not in {"text_only", "large_print_placeholder"}:
        raise DeltaError("garden alternative format is unsupported")
    if record["noncolour_status"] is not True or record["manual_review_required"] is not True:
        raise DeltaError("garden layout lacks noncolour state or manual review")
    _garden_required_false(
        record,
        ("physical_access_confirmed", "affected_user_reviewed", "accessibility_complete"),
    )
    return {
        "heading_count": len(headings),
        "gradient_placeholder": gradient,
        "manual_review_required": True,
        "affected_user_reviewed": False,
        "accessibility_complete": False,
        "valid": True,
    }


def validate_garden_environment_cue(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional environmental cues without diagnosis or clearance."""

    _cave_record(
        record,
        {
            "cue_token",
            "cue_categories",
            "source_state",
            "stop_state",
            "referral_state",
            "diagnosis",
            "treatment",
            "safety_clearance",
            "emergency_claim",
            "real_person_present",
        },
        "garden environment cue",
    )
    _cave_token(record["cue_token"], "garden environment cue token")
    categories = record["cue_categories"]
    allowed = {"weather_placeholder", "heat_placeholder", "frost_placeholder", "wind_placeholder", "pest_vacancy", "disease_vacancy", "allergen_vacancy"}
    if not isinstance(categories, list) or not categories or any(value not in allowed for value in categories):
        raise DeltaError("garden environment cue categories are invalid")
    ensure_unique(categories, "garden environment cue category")
    if record["source_state"] != "external_review_required":
        raise DeltaError("garden environmental source is not externally reserved")
    if record["stop_state"] != "honoured_placeholder":
        raise DeltaError("garden environmental stop state is not dominant")
    if record["referral_state"] not in {"not_requested", "external_placeholder"}:
        raise DeltaError("garden environmental referral state is unsupported")
    _garden_required_false(
        record,
        ("diagnosis", "treatment", "safety_clearance", "emergency_claim", "real_person_present"),
    )
    return {
        "cue_category_count": len(categories),
        "stop_state": "honoured_placeholder",
        "assessment_performed": False,
        "real_person_present": False,
        "valid": True,
    }


def validate_garden_harvest_hold(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a fictional harvest lot while refusing food and consumption release."""

    _cave_record(
        record,
        {
            "lot_token",
            "quantity_placeholder",
            "unit",
            "destination_state",
            "allergen_state",
            "food_safety_state",
            "traceability_state",
            "donation_authorized",
            "transfer_authorized",
            "consumption_released",
            "real_food_present",
        },
        "garden harvest hold",
    )
    _cave_token(record["lot_token"], "garden harvest-lot token")
    quantity = _cave_finite(record["quantity_placeholder"], "garden harvest quantity", minimum=0.0, maximum=10_000.0, minimum_inclusive=False)
    if record["unit"] != "synthetic_kg":
        raise DeltaError("garden harvest unit is unsupported")
    if record["destination_state"] != "external_review_required":
        raise DeltaError("garden harvest destination is not vacant")
    if record["allergen_state"] not in {"unknown", "review_required"}:
        raise DeltaError("garden harvest allergen state is not unresolved")
    if record["food_safety_state"] != "authority_hold":
        raise DeltaError("garden harvest food-safety state is not held")
    if record["traceability_state"] != "placeholder_only":
        raise DeltaError("garden harvest traceability exceeds a placeholder")
    _garden_required_false(
        record,
        ("donation_authorized", "transfer_authorized", "consumption_released", "real_food_present"),
    )
    return {
        "quantity_placeholder": quantity,
        "food_safety_cleared": False,
        "consumption_released": False,
        "real_food_present": False,
        "valid": True,
    }


def validate_garden_correction_lineage(record: dict[str, Any]) -> dict[str, Any]:
    """Validate append-only fictional correction lineage without action authority."""

    _cave_record(
        record,
        {"packet_token", "records", "real_schedule_present", "action_authorized"},
        "garden correction lineage",
    )
    _cave_token(record["packet_token"], "garden correction packet token")
    rows = record["records"]
    if not isinstance(rows, list) or not 2 <= len(rows) <= 32:
        raise DeltaError("garden correction lineage is outside the bounded range")
    seen: set[str] = set()
    ambiguity_open = False
    for index, row in enumerate(rows):
        _cave_record(
            row,
            {"record_token", "parent_token", "event", "reason", "readback", "ambiguity_open", "cancellation_explicit"},
            "garden correction row",
        )
        token = _cave_token(row["record_token"], "garden correction token")
        parent = row["parent_token"]
        event = row["event"]
        if token in seen or parent == token:
            raise DeltaError("garden correction lineage duplicates or self-references a token")
        if index == 0:
            if parent is not None or event != "recorded":
                raise DeltaError("garden correction lineage lacks an original record")
        elif not isinstance(parent, str) or parent not in seen:
            raise DeltaError("garden correction parent is absent or forward-referenced")
        if event not in {"recorded", "corrected", "superseded", "cancelled", "ambiguity_retained"}:
            raise DeltaError("garden correction event is unsupported")
        reason = row["reason"]
        if not isinstance(reason, str) or len(reason) > 256 or reason != reason.strip():
            raise DeltaError("garden correction reason is invalid")
        if event != "recorded" and not reason:
            raise DeltaError("garden correction event lacks a reason")
        if event in {"corrected", "superseded", "cancelled"} and row["readback"] is not True:
            raise DeltaError("garden correction event lacks readback")
        if not isinstance(row["ambiguity_open"], bool) or not isinstance(row["cancellation_explicit"], bool):
            raise DeltaError("garden correction flags must be Boolean")
        ambiguity_open = ambiguity_open or row["ambiguity_open"]
        seen.add(token)
    if not ambiguity_open:
        raise DeltaError("garden correction lineage hides unresolved ambiguity")
    _garden_required_false(record, ("real_schedule_present", "action_authorized"))
    return {
        "record_count": len(rows),
        "original_preserved": True,
        "ambiguity_open": True,
        "action_authorized": False,
        "valid": True,
    }


def validate_garden_handover(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional workload handover without evaluating or assigning a person."""

    _cave_record(
        record,
        {
            "handover_token",
            "queue_ceiling",
            "active_tasks",
            "unfinished_tasks",
            "heat_fatigue_cue",
            "stop_token",
            "correction_readback",
            "next_owner_placeholder",
            "performance_evaluated",
            "release_authorized",
            "real_person_present",
        },
        "garden workload handover",
    )
    _cave_token(record["handover_token"], "garden handover token")
    ceiling = _require_nonnegative_int(record["queue_ceiling"], "garden queue ceiling")
    if not 1 <= ceiling <= 100:
        raise DeltaError("garden queue ceiling is outside the bounded range")
    active = record["active_tasks"]
    unfinished = record["unfinished_tasks"]
    if not isinstance(active, list) or not active or len(active) > ceiling:
        raise DeltaError("garden active queue is empty or over its ceiling")
    if not isinstance(unfinished, list) or not unfinished:
        raise DeltaError("garden unfinished queue must remain visible")
    active_tokens = [_cave_token(value, "garden active task") for value in active]
    unfinished_tokens = [_cave_token(value, "garden unfinished task") for value in unfinished]
    ensure_unique(active_tokens, "garden active task")
    ensure_unique(unfinished_tokens, "garden unfinished task")
    if any(value not in active_tokens for value in unfinished_tokens):
        raise DeltaError("garden unfinished task is absent from the active queue")
    if record["heat_fatigue_cue"] not in {"unknown", "review_required"}:
        raise DeltaError("garden heat and fatigue cue is unsupported")
    if record["stop_token"] is not True or record["correction_readback"] is not True:
        raise DeltaError("garden handover lacks a dominant stop or correction readback")
    _cave_token(record["next_owner_placeholder"], "garden next-owner placeholder")
    _garden_required_false(
        record,
        ("performance_evaluated", "release_authorized", "real_person_present"),
    )
    return {
        "active_task_count": len(active_tokens),
        "unfinished_task_count": len(unfinished_tokens),
        "stop_token": True,
        "performance_evaluated": False,
        "release_authorized": False,
        "valid": True,
    }


def liora_fixture_cases() -> list[dict[str, Any]]:
    """Return Liora's positive garden fixtures and five rejections per completion."""

    season = {
        "season_token": "season_alpha",
        "revision": 1,
        "source_pin": "sha256:" + "00" * 32,
        "cancellation_state": "hold",
        "synthetic": True,
        "cultivation_authorized": False,
        "real_site_present": False,
        "raw_identity_present": False,
    }
    topology = {
        "nodes": [
            {"node_token": "plot_alpha", "kind": "plot", "parent_token": None},
            {"node_token": "bed_alpha", "kind": "raised_bed", "parent_token": "plot_alpha"},
            {"node_token": "path_alpha", "kind": "path", "parent_token": "plot_alpha"},
        ],
        "real_location_present": False,
        "land_right_claimed": False,
        "construction_released": False,
    }
    seed = {
        "lots": [
            {
                "lot_token": "lot_alpha",
                "label_token": "label_alpha",
                "source_token": "source_alpha",
                "substitution_for": None,
                "quarantine_state": "hold",
            },
            {
                "lot_token": "lot_beta",
                "label_token": "label_beta",
                "source_token": "source_beta",
                "substitution_for": "lot_alpha",
                "quarantine_state": "review_required",
            },
        ],
        "real_organism_present": False,
        "authenticity_claimed": False,
        "viability_claimed": False,
        "custody_claimed": False,
    }
    activity = {
        "items": [
            {
                "activity_token": "activity_alpha",
                "kind": "sowing_placeholder",
                "window_start": "2026-01-01T00:00:00Z",
                "window_end": "2026-01-02T00:00:00Z",
                "dependencies": [],
                "incomplete": False,
                "instruction_provided": False,
                "recommendation_provided": False,
            },
            {
                "activity_token": "activity_beta",
                "kind": "review_placeholder",
                "window_start": "2026-01-03T00:00:00Z",
                "window_end": "2026-01-04T00:00:00Z",
                "dependencies": ["activity_alpha"],
                "incomplete": True,
                "instruction_provided": False,
                "recommendation_provided": False,
            },
        ],
        "work_authorized": False,
    }
    soil = {
        "sample_token": "sample_alpha",
        "depth_cm": 10.0,
        "ph_placeholder": 7.0,
        "nutrient_placeholder": 0.0,
        "nutrient_unit": "synthetic_index",
        "uncertainty": 0.5,
        "contamination_cue": "review_required",
        "real_sample_present": False,
        "fertility_inference": False,
        "contamination_diagnosis": False,
    }
    compost = {
        "batches": [
            {
                "batch_token": "batch_alpha",
                "material_class": "green_placeholder",
                "source_token": "source_alpha",
                "quantity": 2.0,
                "unit": "synthetic_kg",
                "maturity_state": "external_review_required",
                "contamination_state": "unknown",
            },
            {
                "batch_token": "batch_beta",
                "material_class": "brown_placeholder",
                "source_token": "source_beta",
                "quantity": 3.0,
                "unit": "synthetic_kg",
                "maturity_state": "external_review_required",
                "contamination_state": "review_required",
            },
        ],
        "real_material_present": False,
        "safety_cleared": False,
        "application_authorized": False,
    }
    irrigation = {
        "zone_token": "zone_alpha",
        "source_state": "surrogate_unverified",
        "volume_liters": 10.0,
        "interval_start": "2026-01-01T00:00:00Z",
        "interval_end": "2026-01-01T01:00:00Z",
        "leak_cue": "unknown",
        "restriction_state": "external_review_required",
        "real_water_source_present": False,
        "allocation_authorized": False,
        "operation_authorized": False,
    }
    tool = {
        "tools": [
            {"tool_token": "tool_alpha", "condition_state": "unknown", "isolation_token": "isolation_alpha", "sharps_state": "not_applicable"},
            {"tool_token": "tool_beta", "condition_state": "review_required", "isolation_token": "isolation_beta", "sharps_state": "review_required"},
        ],
        "real_tool_present": False,
        "inspected": False,
        "competence_claimed": False,
        "safety_cleared": False,
        "use_released": False,
    }
    privacy = {
        "availability_token": "availability_alpha",
        "membership_state": "unknown_placeholder",
        "contact_channel": "none",
        "purpose": "synthetic_coordination",
        "retention_days": 30,
        "correction_state": "available_placeholder",
        "raw_identity_present": False,
        "participation_inferred": False,
        "secondary_purpose": False,
    }
    accessible = {
        "headings": ["Scope", "Synthetic layout", "Review vacancies"],
        "text_alternative": "A fictional garden layout contains one plot, one raised-bed placeholder, and one path placeholder.",
        "path_state": "manual_review_required",
        "reach_state": "manual_review_required",
        "surface_state": "manual_review_required",
        "gradient_placeholder": 0.0,
        "signage_placeholder": True,
        "seating_placeholder": True,
        "alternative_format": "text_only",
        "noncolour_status": True,
        "manual_review_required": True,
        "physical_access_confirmed": False,
        "affected_user_reviewed": False,
        "accessibility_complete": False,
    }
    environment = {
        "cue_token": "cue_alpha",
        "cue_categories": ["weather_placeholder", "heat_placeholder", "pest_vacancy"],
        "source_state": "external_review_required",
        "stop_state": "honoured_placeholder",
        "referral_state": "not_requested",
        "diagnosis": False,
        "treatment": False,
        "safety_clearance": False,
        "emergency_claim": False,
        "real_person_present": False,
    }
    harvest = {
        "lot_token": "harvest_alpha",
        "quantity_placeholder": 1.0,
        "unit": "synthetic_kg",
        "destination_state": "external_review_required",
        "allergen_state": "unknown",
        "food_safety_state": "authority_hold",
        "traceability_state": "placeholder_only",
        "donation_authorized": False,
        "transfer_authorized": False,
        "consumption_released": False,
        "real_food_present": False,
    }
    correction = {
        "packet_token": "packet_alpha",
        "records": [
            {
                "record_token": "record_alpha",
                "parent_token": None,
                "event": "recorded",
                "reason": "",
                "readback": False,
                "ambiguity_open": True,
                "cancellation_explicit": False,
            },
            {
                "record_token": "record_beta",
                "parent_token": "record_alpha",
                "event": "corrected",
                "reason": "Synthetic correction placeholder.",
                "readback": True,
                "ambiguity_open": True,
                "cancellation_explicit": False,
            },
        ],
        "real_schedule_present": False,
        "action_authorized": False,
    }
    handover = {
        "handover_token": "handover_alpha",
        "queue_ceiling": 3,
        "active_tasks": ["task_alpha", "task_beta"],
        "unfinished_tasks": ["task_beta"],
        "heat_fatigue_cue": "review_required",
        "stop_token": True,
        "correction_readback": True,
        "next_owner_placeholder": "owner_next",
        "performance_evaluated": False,
        "release_authorized": False,
        "real_person_present": False,
    }
    return [
        {
            "fixture_id": "LI6633-HF-001",
            "proposal_id": "LI6633-N001",
            "validator": "validate_garden_season_packet",
            "positive": season,
            "mutations": [
                {"label": "zero garden season revision", "record": {**season, "revision": 0}},
                {"label": "non-SHA256 garden source pin", "record": {**season, "source_pin": "sha1:00"}},
                {"label": "garden cultivation authorization", "record": {**season, "cultivation_authorized": True}},
                {"label": "real garden site presence", "record": {**season, "real_site_present": True}},
                {"label": "raw garden identity presence", "record": {**season, "raw_identity_present": True}},
            ],
        },
        {
            "fixture_id": "LI6633-HF-002",
            "proposal_id": "LI6633-N002",
            "validator": "validate_garden_plot_topology",
            "positive": topology,
            "mutations": [
                {"label": "duplicate garden topology token", "record": {**topology, "nodes": [topology["nodes"][0], {**topology["nodes"][1], "node_token": "plot_alpha"}, topology["nodes"][2]]}},
                {"label": "orphan garden topology parent", "record": {**topology, "nodes": [topology["nodes"][0], {**topology["nodes"][1], "parent_token": "plot_missing"}, topology["nodes"][2]]}},
                {"label": "raw garden coordinate field", "record": {**topology, "coordinates": [0, 0]}},
                {"label": "garden land-right claim", "record": {**topology, "land_right_claimed": True}},
                {"label": "garden construction release", "record": {**topology, "construction_released": True}},
            ],
        },
        {
            "fixture_id": "LI6633-HF-003",
            "proposal_id": "LI6633-N003",
            "validator": "validate_garden_seed_lot",
            "positive": seed,
            "mutations": [
                {"label": "duplicate garden seed-lot token", "record": {**seed, "lots": [seed["lots"][0], {**seed["lots"][1], "lot_token": "lot_alpha"}]}},
                {"label": "unknown garden seed substitution", "record": {**seed, "lots": [seed["lots"][0], {**seed["lots"][1], "substitution_for": "lot_missing"}]}},
                {"label": "real garden organism presence", "record": {**seed, "real_organism_present": True}},
                {"label": "garden botanical-authenticity claim", "record": {**seed, "authenticity_claimed": True}},
                {"label": "garden viability claim", "record": {**seed, "viability_claimed": True}},
            ],
        },
        {
            "fixture_id": "LI6633-HF-004",
            "proposal_id": "LI6633-N004",
            "validator": "validate_garden_activity_plan",
            "positive": activity,
            "mutations": [
                {"label": "forward garden activity dependency", "record": {**activity, "items": [{**activity["items"][0], "dependencies": ["activity_beta"]}, activity["items"][1]]}},
                {"label": "duplicate garden activity token", "record": {**activity, "items": [activity["items"][0], {**activity["items"][1], "activity_token": "activity_alpha"}]}},
                {"label": "reversed garden activity window", "record": {**activity, "items": [{**activity["items"][0], "window_end": "2025-12-31T00:00:00Z"}, activity["items"][1]]}},
                {"label": "garden activity instruction", "record": {**activity, "items": [{**activity["items"][0], "instruction_provided": True}, activity["items"][1]]}},
                {"label": "garden agronomic recommendation", "record": {**activity, "items": [activity["items"][0], {**activity["items"][1], "recommendation_provided": True}]}},
            ],
        },
        {
            "fixture_id": "LI6633-HF-005",
            "proposal_id": "LI6633-N005",
            "validator": "validate_garden_soil_observation",
            "positive": soil,
            "mutations": [
                {"label": "nonfinite garden pH placeholder", "record": {**soil, "ph_placeholder": float("nan")}},
                {"label": "zero garden depth placeholder", "record": {**soil, "depth_cm": 0.0}},
                {"label": "unsupported garden nutrient unit", "record": {**soil, "nutrient_unit": "mg/kg"}},
                {"label": "real garden soil sample", "record": {**soil, "real_sample_present": True}},
                {"label": "garden fertility inference", "record": {**soil, "fertility_inference": True}},
            ],
        },
        {
            "fixture_id": "LI6633-HF-006",
            "proposal_id": "LI6633-N006",
            "validator": "validate_garden_compost_input",
            "positive": compost,
            "mutations": [
                {"label": "duplicate garden compost batch", "record": {**compost, "batches": [compost["batches"][0], {**compost["batches"][1], "batch_token": "batch_alpha"}]}},
                {"label": "zero garden compost quantity", "record": {**compost, "batches": [{**compost["batches"][0], "quantity": 0.0}, compost["batches"][1]]}},
                {"label": "garden compost maturity clearance", "record": {**compost, "batches": [{**compost["batches"][0], "maturity_state": "ready"}, compost["batches"][1]]}},
                {"label": "garden compost contamination clearance", "record": {**compost, "batches": [compost["batches"][0], {**compost["batches"][1], "contamination_state": "cleared"}]}},
                {"label": "garden compost application authorization", "record": {**compost, "application_authorized": True}},
            ],
        },
        {
            "fixture_id": "LI6633-HF-007",
            "proposal_id": "LI6633-N007",
            "validator": "validate_garden_irrigation_reservation",
            "positive": irrigation,
            "mutations": [
                {"label": "zero garden irrigation volume", "record": {**irrigation, "volume_liters": 0.0}},
                {"label": "reversed garden irrigation interval", "record": {**irrigation, "interval_end": "2025-12-31T00:00:00Z"}},
                {"label": "verified garden water source claim", "record": {**irrigation, "source_state": "verified"}},
                {"label": "garden water allocation authorization", "record": {**irrigation, "allocation_authorized": True}},
                {"label": "garden irrigation operation authorization", "record": {**irrigation, "operation_authorized": True}},
            ],
        },
        {
            "fixture_id": "LI6633-HF-008",
            "proposal_id": "LI6633-N008",
            "validator": "validate_garden_tool_reservation",
            "positive": tool,
            "mutations": [
                {"label": "duplicate garden tool token", "record": {**tool, "tools": [tool["tools"][0], {**tool["tools"][1], "tool_token": "tool_alpha"}]}},
                {"label": "invalid garden isolation token", "record": {**tool, "tools": [{**tool["tools"][0], "isolation_token": ""}, tool["tools"][1]]}},
                {"label": "garden tool inspection claim", "record": {**tool, "inspected": True}},
                {"label": "garden tool competence claim", "record": {**tool, "competence_claimed": True}},
                {"label": "garden tool use release", "record": {**tool, "use_released": True}},
            ],
        },
        {
            "fixture_id": "LI6633-HF-009",
            "proposal_id": "LI6633-N009",
            "validator": "validate_garden_privacy_notice",
            "positive": privacy,
            "mutations": [
                {"label": "raw garden identity presence", "record": {**privacy, "raw_identity_present": True}},
                {"label": "garden participation inference", "record": {**privacy, "participation_inferred": True}},
                {"label": "garden secondary purpose", "record": {**privacy, "secondary_purpose": True}},
                {"label": "zero garden retention period", "record": {**privacy, "retention_days": 0}},
                {"label": "raw garden email field", "record": {**privacy, "email": "withheld@example.invalid"}},
            ],
        },
        {
            "fixture_id": "LI6633-HF-010",
            "proposal_id": "LI6633-N010",
            "validator": "validate_garden_accessible_layout",
            "positive": accessible,
            "mutations": [
                {"label": "missing garden accessible headings", "record": {**accessible, "headings": []}},
                {"label": "missing garden text alternative", "record": {**accessible, "text_alternative": ""}},
                {"label": "garden colour-only status", "record": {**accessible, "noncolour_status": False}},
                {"label": "unsupported garden affected-user review", "record": {**accessible, "affected_user_reviewed": True}},
                {"label": "garden accessibility-complete claim", "record": {**accessible, "accessibility_complete": True}},
            ],
        },
        {
            "fixture_id": "LI6633-HF-011",
            "proposal_id": "LI6633-N011",
            "validator": "validate_garden_environment_cue",
            "positive": environment,
            "mutations": [
                {"label": "unsupported garden environmental cue", "record": {**environment, "cue_categories": ["diagnosis"]}},
                {"label": "garden stop state overridden", "record": {**environment, "stop_state": "ignored"}},
                {"label": "garden diagnosis claim", "record": {**environment, "diagnosis": True}},
                {"label": "garden treatment claim", "record": {**environment, "treatment": True}},
                {"label": "garden safety-clearance claim", "record": {**environment, "safety_clearance": True}},
            ],
        },
        {
            "fixture_id": "LI6633-HF-012",
            "proposal_id": "LI6633-N012",
            "validator": "validate_garden_harvest_hold",
            "positive": harvest,
            "mutations": [
                {"label": "zero garden harvest quantity", "record": {**harvest, "quantity_placeholder": 0.0}},
                {"label": "garden harvest destination release", "record": {**harvest, "destination_state": "released"}},
                {"label": "garden food-safety clearance", "record": {**harvest, "food_safety_state": "cleared"}},
                {"label": "garden donation authorization", "record": {**harvest, "donation_authorized": True}},
                {"label": "garden consumption release", "record": {**harvest, "consumption_released": True}},
            ],
        },
        {
            "fixture_id": "LI6633-HF-013",
            "proposal_id": "LI6633-N013",
            "validator": "validate_garden_correction_lineage",
            "positive": correction,
            "mutations": [
                {"label": "duplicate garden correction token", "record": {**correction, "records": [correction["records"][0], {**correction["records"][1], "record_token": "record_alpha"}]}},
                {"label": "forward garden correction parent", "record": {**correction, "records": [correction["records"][0], {**correction["records"][1], "parent_token": "record_missing"}]}},
                {"label": "garden lineage without original", "record": {**correction, "records": [{**correction["records"][0], "event": "corrected"}, correction["records"][1]]}},
                {"label": "garden correction without reason", "record": {**correction, "records": [correction["records"][0], {**correction["records"][1], "reason": ""}]}},
                {"label": "garden correction without readback", "record": {**correction, "records": [correction["records"][0], {**correction["records"][1], "readback": False}]}},
            ],
        },
        {
            "fixture_id": "LI6633-HF-014",
            "proposal_id": "LI6633-N014",
            "validator": "validate_garden_handover",
            "positive": handover,
            "mutations": [
                {"label": "garden queue over ceiling", "record": {**handover, "queue_ceiling": 1}},
                {"label": "unknown unfinished garden task", "record": {**handover, "unfinished_tasks": ["task_missing"]}},
                {"label": "garden stop token overridden", "record": {**handover, "stop_token": False}},
                {"label": "missing garden correction readback", "record": {**handover, "correction_readback": False}},
                {"label": "garden performance evaluation claim", "record": {**handover, "performance_evaluated": True}},
            ],
        },
    ]


def _liora_validators() -> dict[str, Any]:
    return {
        function.__name__: function
        for function in (
            validate_garden_season_packet,
            validate_garden_plot_topology,
            validate_garden_seed_lot,
            validate_garden_activity_plan,
            validate_garden_soil_observation,
            validate_garden_compost_input,
            validate_garden_irrigation_reservation,
            validate_garden_tool_reservation,
            validate_garden_privacy_notice,
            validate_garden_accessible_layout,
            validate_garden_environment_cue,
            validate_garden_harvest_hold,
            validate_garden_correction_lineage,
            validate_garden_handover,
        )
    }


def liora_mutation_payload() -> dict[str, Any]:
    """Execute five preregistered rejecting mutations per Liora completion."""

    validators = _liora_validators()
    records: list[dict[str, Any]] = []
    positives: list[dict[str, Any]] = []
    for case_index, case in enumerate(liora_fixture_cases(), 1):
        validator = validators[case["validator"]]
        positive = validator(case["positive"])
        if positive.get("valid") is not True:
            raise DeltaError(f"Liora positive fixture failed: {case['fixture_id']}")
        positives.append(
            {
                "proposal_id": case["proposal_id"],
                "validator": case["validator"],
                "valid": True,
            }
        )
        mutations = case["mutations"]
        if len(mutations) != 5:
            raise DeltaError(f"Liora fixture does not declare five mutations: {case['fixture_id']}")
        for mutation_index, mutation in enumerate(mutations, 1):
            try:
                validator(mutation["record"])
            except (DeltaError, UnicodeError, ValueError, TypeError) as exc:
                records.append(
                    {
                        "fixture_id": f"LI6633-HF-{case_index:03d}-{mutation_index:02d}",
                        "mutation_id": f"LI6633-MUT-{case_index:03d}-{mutation_index:02d}",
                        "proposal_id": case["proposal_id"],
                        "validator": case["validator"],
                        "failed_witness": mutation["label"],
                        "rejected": True,
                        "error_class": type(exc).__name__,
                        "zero_credit": True,
                    }
                )
            else:
                raise DeltaError(
                    f"Liora negative mutation was not rejected: {case['fixture_id']}:{mutation_index}"
                )
    return {
        "schema": f"{SCHEMA}.liora-mutation-matrix.v1",
        "profile": "liora-v663-v3",
        "proposal_count": len(positives),
        "mutations_per_proposal": 5,
        "negative_fixture_count": len(records),
        "rejected_fixture_count": sum(record["rejected"] is True for record in records),
        "positive_fixture_count": len(positives),
        "passing_fixture_count": len(positives),
        "records": records,
        "positive_records": positives,
        "failed_witnesses_erased": 0,
        "valid": len(records) == 70 and len(positives) == 14,
        "boundary": "Seventy rejected synthetic mutations and fourteen passing community-garden record-shape fixtures only; no real person, site, land, plant, seed, soil, compost, water, tool, harvest, food, measurement, action, authority act, empirical result, production result or independent reproduction.",
    }


def liora_hardening_payload() -> dict[str, Any]:
    """Return every retained Liora rejection plus fourteen bounded positives."""

    matrix = liora_mutation_payload()
    if not matrix["valid"]:
        raise DeltaError("one or more Liora hardening fixtures failed")
    return {
        "schema": f"{SCHEMA}.hardening-fixtures.v7",
        "profile": "liora-v663-v3",
        "negative_fixture_count": matrix["negative_fixture_count"],
        "rejected_fixture_count": matrix["rejected_fixture_count"],
        "positive_fixture_count": matrix["positive_fixture_count"],
        "passing_fixture_count": matrix["passing_fixture_count"],
        "records": matrix["records"],
        "full_mutation_matrix_negative_count": matrix["negative_fixture_count"],
        "real_person_present": False,
        "real_site_present": False,
        "real_plant_present": False,
        "real_measurement_present": False,
        "cultivation_authorized": False,
        "water_allocated": False,
        "tool_use_released": False,
        "food_safety_cleared": False,
        "privacy_complete": False,
        "accessibility_complete": False,
        "professional_authority": False,
        "legal_authority": False,
        "cultural_authority": False,
        "maori_authority": False,
        "exhaustive_security": False,
        "valid": True,
        "boundary": "All seventy preregistered garden mutations were rejected and fourteen paired positives passed as bounded software fixtures only; not cultivation, botanical identification, soil or water assessment, material clearance, equipment release, harvest or food-safety release, professional validation, legal or cultural ratification, Māori authority, privacy or accessibility completeness, production assurance, empirical evidence or independent reproduction.",
    }




def _kite_required_false(record: dict[str, Any], fields: Iterable[str]) -> None:
    """Require explicit false values for synthetic kite authority boundaries."""

    for field in fields:
        _cave_false(record[field], f"kite {field.replace('_', ' ')}")


def _kite_valid(kind: str, *, record_count: int = 1) -> dict[str, Any]:
    return {
        "kind": kind,
        "record_count": record_count,
        "real_person_present": False,
        "real_asset_present": False,
        "real_measurement_present": False,
        "flight_authorized": False,
        "professional_authority": False,
        "legal_authority": False,
        "cultural_authority": False,
        "maori_authority": False,
        "valid": True,
    }


def validate_kite_workshop_packet(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a fictional workshop packet without authorizing build or flight."""

    _cave_record(
        record,
        {
            "workshop_token",
            "revision",
            "source_pin",
            "cancellation_state",
            "synthetic",
            "raw_identity_present",
            "real_workshop_present",
            "build_authorized",
            "flight_authorized",
        },
        "kite workshop packet",
    )
    _cave_token(record["workshop_token"], "kite workshop token")
    revision = _require_nonnegative_int(record["revision"], "kite workshop revision")
    if not 1 <= revision <= 10_000:
        raise DeltaError("kite workshop revision is outside the bounded range")
    if re.fullmatch(r"sha256:[0-9a-f]{64}", record["source_pin"]) is None:
        raise DeltaError("kite workshop source pin is not an explicit SHA-256 commitment")
    if record["cancellation_state"] not in {"planned", "cancelled", "superseded"}:
        raise DeltaError("kite workshop cancellation state is unsupported")
    if record["synthetic"] is not True:
        raise DeltaError("kite workshop packet must remain explicitly synthetic")
    _kite_required_false(
        record,
        (
            "raw_identity_present",
            "real_workshop_present",
            "build_authorized",
            "flight_authorized",
        ),
    )
    return _kite_valid("kite_workshop_packet")


def validate_kite_component_topology(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional kite-component topology and refuse physical release."""

    _cave_record(
        record,
        {
            "components",
            "real_asset_present",
            "assembly_authorized",
            "flight_authorized",
        },
        "kite component topology",
    )
    components = record["components"]
    if not isinstance(components, list) or not 3 <= len(components) <= 32:
        raise DeltaError("kite component count is outside the bounded range")
    seen: set[str] = set()
    kinds: set[str] = set()
    for index, component in enumerate(components):
        _cave_record(
            component,
            {"component_token", "kind", "parent_token"},
            "kite component row",
        )
        token = _cave_token(component["component_token"], "kite component token")
        if token in seen:
            raise DeltaError("kite component token is duplicated")
        if component["kind"] not in {"root", "frame", "sail", "bridle", "tail", "line"}:
            raise DeltaError("kite component kind is unsupported")
        parent = component["parent_token"]
        if index == 0:
            if component["kind"] != "root" or parent is not None:
                raise DeltaError("kite topology lacks a valid root")
        elif not isinstance(parent, str) or parent not in seen:
            raise DeltaError("kite component parent is absent or forward-referenced")
        seen.add(token)
        kinds.add(component["kind"])
    if not {"sail", "bridle"} <= kinds:
        raise DeltaError("kite topology lacks sail and bridle placeholders")
    _kite_required_false(record, ("real_asset_present", "assembly_authorized", "flight_authorized"))
    return _kite_valid("kite_component_topology", record_count=len(components))


def validate_kite_material_lots(record: dict[str, Any]) -> dict[str, Any]:
    """Validate synthetic material provenance and quarantine only."""

    _cave_record(
        record,
        {
            "lots",
            "real_material_present",
            "authenticity_claimed",
            "suitability_claimed",
            "custody_claimed",
            "safety_cleared",
        },
        "kite material ledger",
    )
    lots = record["lots"]
    if not isinstance(lots, list) or not 2 <= len(lots) <= 32:
        raise DeltaError("kite material-lot count is outside the bounded range")
    seen: set[str] = set()
    for lot in lots:
        _cave_record(
            lot,
            {
                "lot_token",
                "source_token",
                "material_class",
                "substitution_for",
                "quarantined",
            },
            "kite material-lot row",
        )
        token = _cave_token(lot["lot_token"], "kite material-lot token")
        if token in seen:
            raise DeltaError("kite material-lot token is duplicated")
        _cave_token(lot["source_token"], "kite material source token")
        if lot["material_class"] not in {"paper", "fabric", "spar", "cord", "adhesive"}:
            raise DeltaError("kite material class is unsupported")
        substitute = lot["substitution_for"]
        if substitute is not None and (not isinstance(substitute, str) or substitute not in seen):
            raise DeltaError("kite material substitution is absent or forward-referenced")
        if lot["quarantined"] is not True:
            raise DeltaError("kite material quarantine is not retained")
        seen.add(token)
    _kite_required_false(
        record,
        (
            "real_material_present",
            "authenticity_claimed",
            "suitability_claimed",
            "custody_claimed",
            "safety_cleared",
        ),
    )
    return _kite_valid("kite_material_lots", record_count=len(lots))


def validate_kite_workshop_plan(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional dependency windows without instructions or work release."""

    _cave_record(record, {"items", "work_authorized"}, "kite workshop plan")
    items = record["items"]
    if not isinstance(items, list) or not 2 <= len(items) <= 32:
        raise DeltaError("kite workshop-plan count is outside the bounded range")
    seen: set[str] = set()
    incomplete = 0
    for item in items:
        _cave_record(
            item,
            {
                "item_token",
                "kind",
                "window_start",
                "window_end",
                "dependencies",
                "incomplete",
                "instruction_provided",
                "recommendation_provided",
            },
            "kite workshop-plan row",
        )
        token = _cave_token(item["item_token"], "kite workshop item token")
        if token in seen:
            raise DeltaError("kite workshop item token is duplicated")
        if item["kind"] not in {"pattern", "template", "cut", "assembly", "hold"}:
            raise DeltaError("kite workshop item kind is unsupported")
        start = _cave_timestamp(item["window_start"], "kite workshop start")
        end = _cave_timestamp(item["window_end"], "kite workshop end")
        if end <= start or (end - start).total_seconds() > 86_400:
            raise DeltaError("kite workshop window is reversed or over budget")
        deps = item["dependencies"]
        if not isinstance(deps, list):
            raise DeltaError("kite workshop dependencies are not a list")
        parsed = [_cave_token(value, "kite workshop dependency") for value in deps]
        ensure_unique(parsed, "kite workshop dependency")
        if any(value not in seen for value in parsed):
            raise DeltaError("kite workshop dependency is absent or forward-referenced")
        if not isinstance(item["incomplete"], bool):
            raise DeltaError("kite workshop incomplete state must be Boolean")
        incomplete += int(item["incomplete"])
        _kite_required_false(item, ("instruction_provided", "recommendation_provided"))
        seen.add(token)
    if incomplete == 0:
        raise DeltaError("kite workshop plan hides all incomplete work")
    _cave_false(record["work_authorized"], "kite workshop work authorization")
    return _kite_valid("kite_workshop_plan", record_count=len(items))


def validate_kite_geometry_envelope(record: dict[str, Any]) -> dict[str, Any]:
    """Validate typed placeholders without representing a measurement or prediction."""

    _cave_record(
        record,
        {
            "record_token",
            "projected_area",
            "area_unit",
            "span",
            "chord",
            "length_unit",
            "mass",
            "mass_unit",
            "center_of_gravity_state",
            "uncertainty",
            "real_measurement_present",
            "calibrated",
            "prediction_made",
            "safety_cleared",
        },
        "kite geometry envelope",
    )
    _cave_token(record["record_token"], "kite geometry record token")
    _cave_finite(record["projected_area"], "kite projected area", minimum=0.0, maximum=10_000.0, minimum_inclusive=False)
    _cave_finite(record["span"], "kite span", minimum=0.0, maximum=1_000.0, minimum_inclusive=False)
    _cave_finite(record["chord"], "kite chord", minimum=0.0, maximum=1_000.0, minimum_inclusive=False)
    _cave_finite(record["mass"], "kite mass", minimum=0.0, maximum=10_000.0, minimum_inclusive=False)
    _cave_finite(record["uncertainty"], "kite geometry uncertainty", minimum=0.0, maximum=10_000.0, minimum_inclusive=False)
    if record["area_unit"] != "m2" or record["length_unit"] != "m" or record["mass_unit"] != "kg":
        raise DeltaError("kite geometry envelope uses unsupported SI units")
    if record["center_of_gravity_state"] != "vacant":
        raise DeltaError("kite center-of-gravity state is not vacant")
    _kite_required_false(record, ("real_measurement_present", "calibrated", "prediction_made", "safety_cleared"))
    return _kite_valid("kite_geometry_envelope")


def validate_kite_material_cues(record: dict[str, Any]) -> dict[str, Any]:
    """Validate unresolved synthetic material cues and a dominant stop."""

    _cave_record(
        record,
        {
            "cue_kinds",
            "resolution_state",
            "stop",
            "real_material_present",
            "diagnosis_made",
            "treatment_provided",
            "emergency_instruction",
            "safety_cleared",
        },
        "kite material cue board",
    )
    cues = record["cue_kinds"]
    allowed = {"adhesive", "paint", "dye", "coating", "allergen", "ventilation", "fire"}
    if not isinstance(cues, list) or not cues or len(cues) > 16:
        raise DeltaError("kite material cue list is invalid")
    parsed = [_cave_token(value, "kite material cue") for value in cues]
    ensure_unique(parsed, "kite material cue")
    if any(value not in allowed for value in parsed):
        raise DeltaError("kite material cue is unsupported")
    if record["resolution_state"] != "unresolved" or record["stop"] is not True:
        raise DeltaError("kite material cue lacks unresolved dominant stop")
    _kite_required_false(record, ("real_material_present", "diagnosis_made", "treatment_provided", "emergency_instruction", "safety_cleared"))
    return _kite_valid("kite_material_cues", record_count=len(cues))


def validate_kite_tool_reservation(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional tool isolation without inspection or use release."""

    _cave_record(
        record,
        {
            "tools",
            "real_tool_present",
            "inspected",
            "competence_claimed",
            "maintenance_instruction",
            "use_released",
        },
        "kite tool reservation",
    )
    tools = record["tools"]
    if not isinstance(tools, list) or not 2 <= len(tools) <= 32:
        raise DeltaError("kite tool count is outside the bounded range")
    seen: set[str] = set()
    for tool in tools:
        _cave_record(
            tool,
            {
                "tool_token",
                "condition_state",
                "isolation_token",
                "hazard_class",
                "quarantined",
            },
            "kite tool row",
        )
        token = _cave_token(tool["tool_token"], "kite tool token")
        if token in seen:
            raise DeltaError("kite tool token is duplicated")
        if tool["condition_state"] not in {"unresolved", "isolated"}:
            raise DeltaError("kite tool condition is unsupported")
        _cave_token(tool["isolation_token"], "kite tool isolation token")
        if tool["hazard_class"] not in {"sharps", "heat", "manual"}:
            raise DeltaError("kite tool hazard class is unsupported")
        if tool["quarantined"] is not True:
            raise DeltaError("kite tool quarantine is not retained")
        seen.add(token)
    _kite_required_false(record, ("real_tool_present", "inspected", "competence_claimed", "maintenance_instruction", "use_released"))
    return _kite_valid("kite_tool_reservation", record_count=len(tools))


def validate_kite_privacy_notice(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional purpose and retention without personal information."""

    _cave_record(
        record,
        {
            "record_token",
            "purpose",
            "retention_days",
            "correction_available",
            "raw_identity_present",
            "participation_inferred",
            "secondary_purpose",
            "privacy_complete",
        },
        "kite privacy notice",
    )
    _cave_token(record["record_token"], "kite privacy record token")
    if record["purpose"] != "workshop_notice":
        raise DeltaError("kite privacy purpose is unsupported")
    retention = _require_nonnegative_int(record["retention_days"], "kite privacy retention")
    if not 1 <= retention <= 3_650:
        raise DeltaError("kite privacy retention is outside the bounded range")
    if record["correction_available"] is not True:
        raise DeltaError("kite privacy correction is unavailable")
    _kite_required_false(record, ("raw_identity_present", "participation_inferred", "secondary_purpose", "privacy_complete"))
    return _kite_valid("kite_privacy_notice")


def validate_kite_accessibility_companion(record: dict[str, Any]) -> dict[str, Any]:
    """Validate structural accessibility fields while reserving manual review."""

    _cave_record(
        record,
        {
            "headings",
            "text_alternative",
            "status_text",
            "colour_only",
            "keyboard_order",
            "manual_review_required",
            "assistive_technology_reviewed",
            "affected_user_approved",
            "accessibility_complete",
        },
        "kite accessibility companion",
    )
    headings = record["headings"]
    order = record["keyboard_order"]
    if not isinstance(headings, list) or not 2 <= len(headings) <= 16:
        raise DeltaError("kite accessibility headings are invalid")
    if not all(isinstance(value, str) and value.strip() for value in headings):
        raise DeltaError("kite accessibility heading is empty")
    ensure_unique(headings, "kite accessibility heading")
    if not isinstance(order, list) or not order or len(order) > 32:
        raise DeltaError("kite accessibility keyboard order is invalid")
    parsed_order = [_cave_token(value, "kite accessibility focus token") for value in order]
    ensure_unique(parsed_order, "kite accessibility focus token")
    if not isinstance(record["text_alternative"], str) or not record["text_alternative"].strip():
        raise DeltaError("kite accessibility text alternative is absent")
    if not isinstance(record["status_text"], str) or not record["status_text"].strip():
        raise DeltaError("kite accessibility status text is absent")
    if record["manual_review_required"] is not True:
        raise DeltaError("kite accessibility manual review is not reserved")
    _kite_required_false(record, ("colour_only", "assistive_technology_reviewed", "affected_user_approved", "accessibility_complete"))
    return _kite_valid("kite_accessibility_companion")


def validate_kite_rights_hold(record: dict[str, Any]) -> dict[str, Any]:
    """Validate unresolved rights fields without deciding permission or ownership."""

    _cave_record(
        record,
        {
            "pattern_token",
            "source_token",
            "rightsholder_state",
            "license_state",
            "provenance_notice",
            "real_work_present",
            "recording_released",
            "publication_released",
            "exhibition_released",
            "derivative_use_released",
            "ownership_decided",
            "cultural_approval",
        },
        "kite rights hold",
    )
    _cave_token(record["pattern_token"], "kite pattern token")
    _cave_token(record["source_token"], "kite rights source token")
    if record["rightsholder_state"] != "unresolved" or record["license_state"] != "unresolved":
        raise DeltaError("kite rights state is not unresolved")
    if not isinstance(record["provenance_notice"], str) or not 1 <= len(record["provenance_notice"].strip()) <= 512:
        raise DeltaError("kite provenance notice is invalid")
    _kite_required_false(record, ("real_work_present", "recording_released", "publication_released", "exhibition_released", "derivative_use_released", "ownership_decided", "cultural_approval"))
    return _kite_valid("kite_rights_hold")


def validate_kite_external_cues(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a fictional external cue board with no flight or legal clearance."""

    _cave_record(
        record,
        {
            "cue_kinds",
            "stop",
            "real_location_present",
            "real_weather_present",
            "flight_authorized",
            "emergency_instruction",
            "safety_cleared",
            "airspace_cleared",
            "legal_interpretation",
        },
        "kite external cue board",
    )
    cues = record["cue_kinds"]
    allowed = {"weather", "wind", "power_line", "road", "water", "aerodrome"}
    if not isinstance(cues, list) or not cues or len(cues) > 16:
        raise DeltaError("kite external cue list is invalid")
    parsed = [_cave_token(value, "kite external cue") for value in cues]
    ensure_unique(parsed, "kite external cue")
    if any(value not in allowed for value in parsed):
        raise DeltaError("kite external cue is unsupported")
    if record["stop"] is not True:
        raise DeltaError("kite external cue lacks a dominant stop")
    _kite_required_false(record, ("real_location_present", "real_weather_present", "flight_authorized", "emergency_instruction", "safety_cleared", "airspace_cleared", "legal_interpretation"))
    return _kite_valid("kite_external_cues", record_count=len(cues))


def validate_kite_custody_placeholder(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional container links without ownership or transfer release."""

    _cave_record(
        record,
        {
            "containers",
            "items",
            "condition_state",
            "real_asset_present",
            "ownership_claimed",
            "handling_instruction",
            "transport_authorized",
            "custody_released",
        },
        "kite custody placeholder",
    )
    containers = record["containers"]
    items = record["items"]
    if not isinstance(containers, list) or not 1 <= len(containers) <= 16:
        raise DeltaError("kite container list is invalid")
    parsed_containers = [_cave_token(value, "kite container token") for value in containers]
    ensure_unique(parsed_containers, "kite container token")
    if not isinstance(items, list) or not 1 <= len(items) <= 32:
        raise DeltaError("kite custody item list is invalid")
    seen: set[str] = set()
    for item in items:
        _cave_record(item, {"item_token", "container_token"}, "kite custody item")
        token = _cave_token(item["item_token"], "kite custody item token")
        if token in seen:
            raise DeltaError("kite custody item token is duplicated")
        if item["container_token"] not in parsed_containers:
            raise DeltaError("kite custody item references an absent container")
        seen.add(token)
    if record["condition_state"] != "unresolved":
        raise DeltaError("kite custody condition is not unresolved")
    _kite_required_false(record, ("real_asset_present", "ownership_claimed", "handling_instruction", "transport_authorized", "custody_released"))
    return _kite_valid("kite_custody_placeholder", record_count=len(items))


def validate_kite_correction_lineage(record: dict[str, Any]) -> dict[str, Any]:
    """Validate append-only fictional corrections with ambiguity retained."""

    _cave_record(
        record,
        {"records", "real_schedule_present", "action_authorized"},
        "kite correction lineage",
    )
    rows = record["records"]
    if not isinstance(rows, list) or not 2 <= len(rows) <= 32:
        raise DeltaError("kite correction lineage is outside the bounded range")
    seen: set[str] = set()
    unresolved = 0
    for index, row in enumerate(rows):
        _cave_record(
            row,
            {
                "record_token",
                "parent_token",
                "event",
                "reason",
                "readback",
                "original_retained",
                "ambiguity_unresolved",
            },
            "kite correction row",
        )
        token = _cave_token(row["record_token"], "kite correction token")
        if token in seen:
            raise DeltaError("kite correction token is duplicated")
        parent = row["parent_token"]
        if index == 0:
            if parent is not None or row["event"] != "original":
                raise DeltaError("kite correction lineage lacks an original")
        elif not isinstance(parent, str) or parent not in seen:
            raise DeltaError("kite correction parent is absent or forward-referenced")
        if row["event"] not in {"original", "corrected", "cancelled", "superseded"}:
            raise DeltaError("kite correction event is unsupported")
        if index > 0 and (not isinstance(row["reason"], str) or not row["reason"].strip()):
            raise DeltaError("kite correction reason is absent")
        if row["readback"] is not True or row["original_retained"] is not True:
            raise DeltaError("kite correction lacks readback or original retention")
        if not isinstance(row["ambiguity_unresolved"], bool):
            raise DeltaError("kite correction ambiguity flag is not Boolean")
        unresolved += int(row["ambiguity_unresolved"])
        seen.add(token)
    if unresolved == 0:
        raise DeltaError("kite correction lineage hides all ambiguity")
    _kite_required_false(record, ("real_schedule_present", "action_authorized"))
    return _kite_valid("kite_correction_lineage", record_count=len(rows))


def validate_kite_handover(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a bounded zero-person handover without evaluating work."""

    _cave_record(
        record,
        {
            "handover_token",
            "queue_ceiling",
            "active_queue",
            "unfinished_queue",
            "fatigue_cue",
            "stop",
            "correction_readback",
            "next_owner_placeholder",
            "real_worker_present",
            "performance_evaluated",
            "work_released",
        },
        "kite workload handover",
    )
    _cave_token(record["handover_token"], "kite handover token")
    ceiling = _require_nonnegative_int(record["queue_ceiling"], "kite queue ceiling")
    if not 1 <= ceiling <= 64:
        raise DeltaError("kite queue ceiling is outside the bounded range")
    active = record["active_queue"]
    unfinished = record["unfinished_queue"]
    if not isinstance(active, list) or not active or len(active) > ceiling:
        raise DeltaError("kite active queue is empty or over ceiling")
    if not isinstance(unfinished, list) or not unfinished:
        raise DeltaError("kite unfinished queue must remain visible")
    active_tokens = [_cave_token(value, "kite active task") for value in active]
    unfinished_tokens = [_cave_token(value, "kite unfinished task") for value in unfinished]
    ensure_unique(active_tokens, "kite active task")
    ensure_unique(unfinished_tokens, "kite unfinished task")
    if any(value not in active_tokens for value in unfinished_tokens):
        raise DeltaError("kite unfinished task is absent from the active queue")
    if record["fatigue_cue"] not in {"none", "watch", "stop"}:
        raise DeltaError("kite fatigue cue is unsupported")
    if record["stop"] is not True or record["correction_readback"] is not True:
        raise DeltaError("kite handover lacks a dominant stop or correction readback")
    _cave_token(record["next_owner_placeholder"], "kite next-owner placeholder")
    _kite_required_false(record, ("real_worker_present", "performance_evaluated", "work_released"))
    return _kite_valid("kite_handover", record_count=len(active_tokens))


def tamar_fixture_cases() -> list[dict[str, Any]]:
    """Return fourteen bounded positives and five rejecting mutations per proposal."""

    source_pin = "sha256:" + ("a" * 64)
    packet = {
        "workshop_token": "workshop_alpha",
        "revision": 1,
        "source_pin": source_pin,
        "cancellation_state": "planned",
        "synthetic": True,
        "raw_identity_present": False,
        "real_workshop_present": False,
        "build_authorized": False,
        "flight_authorized": False,
    }
    topology = {
        "components": [
            {"component_token": "root_alpha", "kind": "root", "parent_token": None},
            {"component_token": "sail_alpha", "kind": "sail", "parent_token": "root_alpha"},
            {"component_token": "bridle_alpha", "kind": "bridle", "parent_token": "root_alpha"},
        ],
        "real_asset_present": False,
        "assembly_authorized": False,
        "flight_authorized": False,
    }
    materials = {
        "lots": [
            {"lot_token": "lot_alpha", "source_token": "source_alpha", "material_class": "paper", "substitution_for": None, "quarantined": True},
            {"lot_token": "lot_beta", "source_token": "source_beta", "material_class": "cord", "substitution_for": "lot_alpha", "quarantined": True},
        ],
        "real_material_present": False,
        "authenticity_claimed": False,
        "suitability_claimed": False,
        "custody_claimed": False,
        "safety_cleared": False,
    }
    plan = {
        "items": [
            {"item_token": "step_alpha", "kind": "pattern", "window_start": "2026-01-01T00:00:00Z", "window_end": "2026-01-01T01:00:00Z", "dependencies": [], "incomplete": False, "instruction_provided": False, "recommendation_provided": False},
            {"item_token": "step_beta", "kind": "hold", "window_start": "2026-01-01T01:00:00Z", "window_end": "2026-01-01T02:00:00Z", "dependencies": ["step_alpha"], "incomplete": True, "instruction_provided": False, "recommendation_provided": False},
        ],
        "work_authorized": False,
    }
    geometry = {
        "record_token": "geometry_alpha",
        "projected_area": 1.0,
        "area_unit": "m2",
        "span": 1.0,
        "chord": 0.5,
        "length_unit": "m",
        "mass": 0.2,
        "mass_unit": "kg",
        "center_of_gravity_state": "vacant",
        "uncertainty": 0.1,
        "real_measurement_present": False,
        "calibrated": False,
        "prediction_made": False,
        "safety_cleared": False,
    }
    material_cues = {
        "cue_kinds": ["adhesive", "ventilation"],
        "resolution_state": "unresolved",
        "stop": True,
        "real_material_present": False,
        "diagnosis_made": False,
        "treatment_provided": False,
        "emergency_instruction": False,
        "safety_cleared": False,
    }
    tools = {
        "tools": [
            {"tool_token": "tool_alpha", "condition_state": "unresolved", "isolation_token": "isolation_alpha", "hazard_class": "sharps", "quarantined": True},
            {"tool_token": "tool_beta", "condition_state": "isolated", "isolation_token": "isolation_beta", "hazard_class": "manual", "quarantined": True},
        ],
        "real_tool_present": False,
        "inspected": False,
        "competence_claimed": False,
        "maintenance_instruction": False,
        "use_released": False,
    }
    privacy = {
        "record_token": "notice_alpha",
        "purpose": "workshop_notice",
        "retention_days": 30,
        "correction_available": True,
        "raw_identity_present": False,
        "participation_inferred": False,
        "secondary_purpose": False,
        "privacy_complete": False,
    }
    accessibility = {
        "headings": ["Workshop packet", "Status"],
        "text_alternative": "A fictional kite-workshop packet with unresolved status.",
        "status_text": "Stopped pending external review.",
        "colour_only": False,
        "keyboard_order": ["packet", "status"],
        "manual_review_required": True,
        "assistive_technology_reviewed": False,
        "affected_user_approved": False,
        "accessibility_complete": False,
    }
    rights = {
        "pattern_token": "pattern_alpha",
        "source_token": "source_alpha",
        "rightsholder_state": "unresolved",
        "license_state": "unresolved",
        "provenance_notice": "Fictional source lineage only; every right remains unresolved.",
        "real_work_present": False,
        "recording_released": False,
        "publication_released": False,
        "exhibition_released": False,
        "derivative_use_released": False,
        "ownership_decided": False,
        "cultural_approval": False,
    }
    external = {
        "cue_kinds": ["weather", "aerodrome"],
        "stop": True,
        "real_location_present": False,
        "real_weather_present": False,
        "flight_authorized": False,
        "emergency_instruction": False,
        "safety_cleared": False,
        "airspace_cleared": False,
        "legal_interpretation": False,
    }
    custody = {
        "containers": ["container_alpha"],
        "items": [{"item_token": "item_alpha", "container_token": "container_alpha"}],
        "condition_state": "unresolved",
        "real_asset_present": False,
        "ownership_claimed": False,
        "handling_instruction": False,
        "transport_authorized": False,
        "custody_released": False,
    }
    correction = {
        "records": [
            {"record_token": "record_alpha", "parent_token": None, "event": "original", "reason": "", "readback": True, "original_retained": True, "ambiguity_unresolved": True},
            {"record_token": "record_beta", "parent_token": "record_alpha", "event": "corrected", "reason": "fictional correction", "readback": True, "original_retained": True, "ambiguity_unresolved": True},
        ],
        "real_schedule_present": False,
        "action_authorized": False,
    }
    handover = {
        "handover_token": "handover_alpha",
        "queue_ceiling": 4,
        "active_queue": ["task_alpha", "task_beta"],
        "unfinished_queue": ["task_beta"],
        "fatigue_cue": "watch",
        "stop": True,
        "correction_readback": True,
        "next_owner_placeholder": "owner_next",
        "real_worker_present": False,
        "performance_evaluated": False,
        "work_released": False,
    }
    return [
        {"fixture_id": "TV6634-HF-001", "proposal_id": "TV6634-N001", "validator": "validate_kite_workshop_packet", "positive": packet, "mutations": [
            {"label": "zero workshop revision", "record": {**packet, "revision": 0}},
            {"label": "non-SHA256 workshop source pin", "record": {**packet, "source_pin": "sha1:00"}},
            {"label": "kite build authorization", "record": {**packet, "build_authorized": True}},
            {"label": "kite flight authorization", "record": {**packet, "flight_authorized": True}},
            {"label": "raw workshop identity presence", "record": {**packet, "raw_identity_present": True}},
        ]},
        {"fixture_id": "TV6634-HF-002", "proposal_id": "TV6634-N002", "validator": "validate_kite_component_topology", "positive": topology, "mutations": [
            {"label": "duplicate kite component", "record": {**topology, "components": [topology["components"][0], {**topology["components"][1], "component_token": "root_alpha"}, topology["components"][2]]}},
            {"label": "orphan kite component", "record": {**topology, "components": [topology["components"][0], {**topology["components"][1], "parent_token": "root_missing"}, topology["components"][2]]}},
            {"label": "real kite asset presence", "record": {**topology, "real_asset_present": True}},
            {"label": "kite assembly authorization", "record": {**topology, "assembly_authorized": True}},
            {"label": "kite topology flight authorization", "record": {**topology, "flight_authorized": True}},
        ]},
        {"fixture_id": "TV6634-HF-003", "proposal_id": "TV6634-N003", "validator": "validate_kite_material_lots", "positive": materials, "mutations": [
            {"label": "duplicate material lot", "record": {**materials, "lots": [materials["lots"][0], {**materials["lots"][1], "lot_token": "lot_alpha"}]}},
            {"label": "unknown material substitution", "record": {**materials, "lots": [materials["lots"][0], {**materials["lots"][1], "substitution_for": "lot_missing"}]}},
            {"label": "real material presence", "record": {**materials, "real_material_present": True}},
            {"label": "material authenticity claim", "record": {**materials, "authenticity_claimed": True}},
            {"label": "material safety clearance", "record": {**materials, "safety_cleared": True}},
        ]},
        {"fixture_id": "TV6634-HF-004", "proposal_id": "TV6634-N004", "validator": "validate_kite_workshop_plan", "positive": plan, "mutations": [
            {"label": "forward workshop dependency", "record": {**plan, "items": [{**plan["items"][0], "dependencies": ["step_beta"]}, plan["items"][1]]}},
            {"label": "duplicate workshop item", "record": {**plan, "items": [plan["items"][0], {**plan["items"][1], "item_token": "step_alpha"}]}},
            {"label": "reversed workshop window", "record": {**plan, "items": [{**plan["items"][0], "window_end": "2025-12-31T00:00:00Z"}, plan["items"][1]]}},
            {"label": "workshop instruction provided", "record": {**plan, "items": [{**plan["items"][0], "instruction_provided": True}, plan["items"][1]]}},
            {"label": "workshop authorization", "record": {**plan, "work_authorized": True}},
        ]},
        {"fixture_id": "TV6634-HF-005", "proposal_id": "TV6634-N005", "validator": "validate_kite_geometry_envelope", "positive": geometry, "mutations": [
            {"label": "nonfinite projected area", "record": {**geometry, "projected_area": float("nan")}},
            {"label": "unsupported geometry unit", "record": {**geometry, "area_unit": "cm2"}},
            {"label": "real geometry measurement", "record": {**geometry, "real_measurement_present": True}},
            {"label": "kite performance prediction", "record": {**geometry, "prediction_made": True}},
            {"label": "kite geometry safety clearance", "record": {**geometry, "safety_cleared": True}},
        ]},
        {"fixture_id": "TV6634-HF-006", "proposal_id": "TV6634-N006", "validator": "validate_kite_material_cues", "positive": material_cues, "mutations": [
            {"label": "unsupported material cue", "record": {**material_cues, "cue_kinds": ["unknown"]}},
            {"label": "resolved material cue", "record": {**material_cues, "resolution_state": "cleared"}},
            {"label": "material stop overridden", "record": {**material_cues, "stop": False}},
            {"label": "material treatment provided", "record": {**material_cues, "treatment_provided": True}},
            {"label": "material safety clearance", "record": {**material_cues, "safety_cleared": True}},
        ]},
        {"fixture_id": "TV6634-HF-007", "proposal_id": "TV6634-N007", "validator": "validate_kite_tool_reservation", "positive": tools, "mutations": [
            {"label": "duplicate kite tool", "record": {**tools, "tools": [tools["tools"][0], {**tools["tools"][1], "tool_token": "tool_alpha"}]}},
            {"label": "invalid tool isolation token", "record": {**tools, "tools": [{**tools["tools"][0], "isolation_token": ""}, tools["tools"][1]]}},
            {"label": "tool inspection claim", "record": {**tools, "inspected": True}},
            {"label": "tool competence claim", "record": {**tools, "competence_claimed": True}},
            {"label": "tool use release", "record": {**tools, "use_released": True}},
        ]},
        {"fixture_id": "TV6634-HF-008", "proposal_id": "TV6634-N008", "validator": "validate_kite_privacy_notice", "positive": privacy, "mutations": [
            {"label": "raw maker identity", "record": {**privacy, "raw_identity_present": True}},
            {"label": "maker participation inference", "record": {**privacy, "participation_inferred": True}},
            {"label": "privacy secondary purpose", "record": {**privacy, "secondary_purpose": True}},
            {"label": "zero privacy retention", "record": {**privacy, "retention_days": 0}},
            {"label": "privacy completeness claim", "record": {**privacy, "privacy_complete": True}},
        ]},
        {"fixture_id": "TV6634-HF-009", "proposal_id": "TV6634-N009", "validator": "validate_kite_accessibility_companion", "positive": accessibility, "mutations": [
            {"label": "missing accessibility headings", "record": {**accessibility, "headings": []}},
            {"label": "missing text alternative", "record": {**accessibility, "text_alternative": ""}},
            {"label": "colour-only workshop status", "record": {**accessibility, "colour_only": True}},
            {"label": "manual review not reserved", "record": {**accessibility, "manual_review_required": False}},
            {"label": "accessibility completeness claim", "record": {**accessibility, "accessibility_complete": True}},
        ]},
        {"fixture_id": "TV6634-HF-010", "proposal_id": "TV6634-N010", "validator": "validate_kite_rights_hold", "positive": rights, "mutations": [
            {"label": "missing rights source token", "record": {**rights, "source_token": ""}},
            {"label": "cleared rightsholder state", "record": {**rights, "rightsholder_state": "cleared"}},
            {"label": "recording release", "record": {**rights, "recording_released": True}},
            {"label": "publication release", "record": {**rights, "publication_released": True}},
            {"label": "cultural approval claim", "record": {**rights, "cultural_approval": True}},
        ]},
        {"fixture_id": "TV6634-HF-011", "proposal_id": "TV6634-N011", "validator": "validate_kite_external_cues", "positive": external, "mutations": [
            {"label": "unsupported external cue", "record": {**external, "cue_kinds": ["unknown"]}},
            {"label": "external stop overridden", "record": {**external, "stop": False}},
            {"label": "real kite location present", "record": {**external, "real_location_present": True}},
            {"label": "kite flight authorization", "record": {**external, "flight_authorized": True}},
            {"label": "kite legal interpretation", "record": {**external, "legal_interpretation": True}},
        ]},
        {"fixture_id": "TV6634-HF-012", "proposal_id": "TV6634-N012", "validator": "validate_kite_custody_placeholder", "positive": custody, "mutations": [
            {"label": "duplicate container token", "record": {**custody, "containers": ["container_alpha", "container_alpha"]}},
            {"label": "orphan custody container", "record": {**custody, "items": [{**custody["items"][0], "container_token": "container_missing"}]}},
            {"label": "real custody asset", "record": {**custody, "real_asset_present": True}},
            {"label": "ownership claim", "record": {**custody, "ownership_claimed": True}},
            {"label": "transport authorization", "record": {**custody, "transport_authorized": True}},
        ]},
        {"fixture_id": "TV6634-HF-013", "proposal_id": "TV6634-N013", "validator": "validate_kite_correction_lineage", "positive": correction, "mutations": [
            {"label": "duplicate correction token", "record": {**correction, "records": [correction["records"][0], {**correction["records"][1], "record_token": "record_alpha"}]}},
            {"label": "forward correction parent", "record": {**correction, "records": [correction["records"][0], {**correction["records"][1], "parent_token": "record_missing"}]}},
            {"label": "erased correction original", "record": {**correction, "records": [{**correction["records"][0], "original_retained": False}, correction["records"][1]]}},
            {"label": "correction reason absent", "record": {**correction, "records": [correction["records"][0], {**correction["records"][1], "reason": ""}]}},
            {"label": "correction readback absent", "record": {**correction, "records": [correction["records"][0], {**correction["records"][1], "readback": False}]}},
        ]},
        {"fixture_id": "TV6634-HF-014", "proposal_id": "TV6634-N014", "validator": "validate_kite_handover", "positive": handover, "mutations": [
            {"label": "zero queue ceiling", "record": {**handover, "queue_ceiling": 0}},
            {"label": "unknown unfinished task", "record": {**handover, "unfinished_queue": ["task_missing"]}},
            {"label": "handover stop overridden", "record": {**handover, "stop": False}},
            {"label": "handover readback absent", "record": {**handover, "correction_readback": False}},
            {"label": "worker performance evaluation", "record": {**handover, "performance_evaluated": True}},
        ]},
    ]


def tamar_mutation_payload() -> dict[str, Any]:
    """Execute and retain every Tamar mutation with zero negative credit."""

    validators = {
        function.__name__: function
        for function in (
            validate_kite_workshop_packet,
            validate_kite_component_topology,
            validate_kite_material_lots,
            validate_kite_workshop_plan,
            validate_kite_geometry_envelope,
            validate_kite_material_cues,
            validate_kite_tool_reservation,
            validate_kite_privacy_notice,
            validate_kite_accessibility_companion,
            validate_kite_rights_hold,
            validate_kite_external_cues,
            validate_kite_custody_placeholder,
            validate_kite_correction_lineage,
            validate_kite_handover,
        )
    }
    records: list[dict[str, Any]] = []
    positives: list[dict[str, Any]] = []
    cases = tamar_fixture_cases()
    for case_index, case in enumerate(cases, 1):
        validator = validators[case["validator"]]
        result = validator(case["positive"])
        if result.get("valid") is not True:
            raise DeltaError(f"Tamar positive fixture failed: {case['fixture_id']}")
        positives.append(
            {
                "fixture_id": case["fixture_id"],
                "proposal_id": case["proposal_id"],
                "validator": case["validator"],
                "valid": True,
            }
        )
        if len(case["mutations"]) != 5:
            raise DeltaError(f"Tamar fixture does not declare five mutations: {case['fixture_id']}")
        for mutation_index, mutation in enumerate(case["mutations"], 1):
            try:
                validator(mutation["record"])
            except (DeltaError, UnicodeError, ValueError, TypeError) as exc:
                records.append(
                    {
                        "fixture_id": f"TV6634-HF-{case_index:03d}-{mutation_index:02d}",
                        "mutation_id": f"TV6634-MUT-{case_index:03d}-{mutation_index:02d}",
                        "proposal_id": case["proposal_id"],
                        "validator": case["validator"],
                        "failed_witness": mutation["label"],
                        "rejected": True,
                        "error_class": type(exc).__name__,
                        "zero_credit": True,
                    }
                )
            else:
                raise DeltaError(
                    f"Tamar negative mutation was not rejected: {case['fixture_id']}:{mutation_index}"
                )
    return {
        "schema": f"{SCHEMA}.tamar-mutation-matrix.v1",
        "profile": "tamar-v663-v4",
        "proposal_count": len(positives),
        "mutations_per_proposal": 5,
        "negative_fixture_count": len(records),
        "rejected_fixture_count": sum(record["rejected"] is True for record in records),
        "positive_fixture_count": len(positives),
        "passing_fixture_count": len(positives),
        "records": records,
        "positive_records": positives,
        "failed_witnesses_erased": 0,
        "valid": len(records) == 70 and len(positives) == 14,
        "boundary": "Seventy rejected synthetic mutations and fourteen passing kite-workshop record-shape fixtures only; no real person, workshop, kite, material, tool, site, airspace, weather observation, flight, measurement, authority act, empirical result, production result, or independent reproduction.",
    }


def tamar_hardening_payload() -> dict[str, Any]:
    """Return every retained Tamar rejection plus fourteen bounded positives."""

    matrix = tamar_mutation_payload()
    if not matrix["valid"]:
        raise DeltaError("one or more Tamar hardening fixtures failed")
    return {
        "schema": f"{SCHEMA}.hardening-fixtures.v8",
        "profile": "tamar-v663-v4",
        "negative_fixture_count": matrix["negative_fixture_count"],
        "rejected_fixture_count": matrix["rejected_fixture_count"],
        "positive_fixture_count": matrix["positive_fixture_count"],
        "passing_fixture_count": matrix["passing_fixture_count"],
        "records": matrix["records"],
        "full_mutation_matrix_negative_count": matrix["negative_fixture_count"],
        "real_person_present": False,
        "real_workshop_present": False,
        "real_kite_present": False,
        "real_material_present": False,
        "real_tool_present": False,
        "real_location_present": False,
        "real_measurement_present": False,
        "build_authorized": False,
        "flight_authorized": False,
        "airspace_cleared": False,
        "tool_use_released": False,
        "privacy_complete": False,
        "accessibility_complete": False,
        "professional_authority": False,
        "legal_authority": False,
        "cultural_authority": False,
        "maori_authority": False,
        "exhaustive_security": False,
        "valid": True,
        "boundary": "All seventy preregistered kite-workshop mutations were rejected and fourteen paired positives passed as bounded software fixtures only; not construction or flight advice, material or tool clearance, airspace or legal interpretation, professional validation, legal or cultural ratification, Maori authority, privacy or accessibility completeness, production assurance, empirical evidence, or independent reproduction.",
    }


def _print_required_false(record: dict[str, Any], fields: Iterable[str]) -> None:
    """Require explicit false values for synthetic print and archive boundaries."""

    for field in fields:
        _cave_false(record[field], f"print {field.replace('_', ' ')}")


def _print_valid(kind: str, *, record_count: int = 1) -> dict[str, Any]:
    return {
        "kind": kind,
        "record_count": record_count,
        "real_person_present": False,
        "real_asset_present": False,
        "real_material_present": False,
        "real_measurement_present": False,
        "equipment_use_authorized": False,
        "reproduction_authorized": False,
        "professional_authority": False,
        "legal_authority": False,
        "cultural_authority": False,
        "maori_authority": False,
        "valid": True,
    }


def validate_print_work_packet(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a fictional print-work packet without authorizing use or reproduction."""

    _cave_record(
        record,
        {
            "packet_token",
            "revision",
            "source_pin",
            "cancellation_state",
            "synthetic",
            "raw_identity_present",
            "real_workshop_present",
            "equipment_use_authorized",
            "reproduction_authorized",
        },
        "print-work packet",
    )
    _cave_token(record["packet_token"], "print-work packet token")
    revision = _require_nonnegative_int(record["revision"], "print-work packet revision")
    if not 1 <= revision <= 10_000:
        raise DeltaError("print-work packet revision is outside the bounded range")
    if re.fullmatch(r"sha256:[0-9a-f]{64}", record["source_pin"]) is None:
        raise DeltaError("print-work packet source pin is not an explicit SHA-256 commitment")
    if record["cancellation_state"] not in {"planned", "cancelled", "superseded"}:
        raise DeltaError("print-work packet cancellation state is unsupported")
    if record["synthetic"] is not True:
        raise DeltaError("print-work packet must remain explicitly synthetic")
    _print_required_false(
        record,
        (
            "raw_identity_present",
            "real_workshop_present",
            "equipment_use_authorized",
            "reproduction_authorized",
        ),
    )
    return _print_valid("print_work_packet")


def validate_print_component_topology(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional type and print-component topology."""

    _cave_record(
        record,
        {
            "components",
            "real_asset_present",
            "assembly_authorized",
            "equipment_use_authorized",
        },
        "print component topology",
    )
    components = record["components"]
    if not isinstance(components, list) or not 3 <= len(components) <= 48:
        raise DeltaError("print component count is outside the bounded range")
    seen: set[str] = set()
    kinds: set[str] = set()
    for index, component in enumerate(components):
        _cave_record(
            component,
            {"component_token", "kind", "parent_token"},
            "print component row",
        )
        token = _cave_token(component["component_token"], "print component token")
        if token in seen:
            raise DeltaError("print component token is duplicated")
        if component["kind"] not in {
            "root",
            "type_case",
            "sort",
            "furniture",
            "chase",
            "forme",
            "proof",
        }:
            raise DeltaError("print component kind is unsupported")
        parent = component["parent_token"]
        if index == 0:
            if component["kind"] != "root" or parent is not None:
                raise DeltaError("print topology lacks a valid root")
        elif not isinstance(parent, str) or parent not in seen:
            raise DeltaError("print component parent is absent or forward-referenced")
        seen.add(token)
        kinds.add(component["kind"])
    if not {"sort", "forme"} <= kinds:
        raise DeltaError("print topology lacks sort and forme placeholders")
    _print_required_false(
        record,
        ("real_asset_present", "assembly_authorized", "equipment_use_authorized"),
    )
    return _print_valid("print_component_topology", record_count=len(components))


def validate_print_material_lots(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional paper, ink, plate, polymer, and solvent lots."""

    _cave_record(
        record,
        {
            "lots",
            "real_material_present",
            "authenticity_claimed",
            "suitability_claimed",
            "custody_claimed",
            "safety_cleared",
            "disposal_instruction",
        },
        "print material ledger",
    )
    lots = record["lots"]
    if not isinstance(lots, list) or not 2 <= len(lots) <= 40:
        raise DeltaError("print material-lot count is outside the bounded range")
    seen: set[str] = set()
    for lot in lots:
        _cave_record(
            lot,
            {
                "lot_token",
                "source_token",
                "material_class",
                "substitution_for",
                "quarantined",
            },
            "print material-lot row",
        )
        token = _cave_token(lot["lot_token"], "print material-lot token")
        if token in seen:
            raise DeltaError("print material-lot token is duplicated")
        _cave_token(lot["source_token"], "print material source token")
        if lot["material_class"] not in {
            "paper",
            "ink",
            "plate",
            "polymer",
            "solvent",
            "pigment",
            "adhesive",
        }:
            raise DeltaError("print material class is unsupported")
        substitute = lot["substitution_for"]
        if substitute is not None and (
            not isinstance(substitute, str) or substitute not in seen
        ):
            raise DeltaError("print material substitution is absent or forward-referenced")
        if lot["quarantined"] is not True:
            raise DeltaError("print material quarantine is not retained")
        seen.add(token)
    _print_required_false(
        record,
        (
            "real_material_present",
            "authenticity_claimed",
            "suitability_claimed",
            "custody_claimed",
            "safety_cleared",
            "disposal_instruction",
        ),
    )
    return _print_valid("print_material_lots", record_count=len(lots))


def validate_print_edition_dependencies(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional edition dependencies without production instructions."""

    _cave_record(
        record,
        {"items", "production_authorized", "canon_claimed"},
        "print edition dependency plan",
    )
    items = record["items"]
    if not isinstance(items, list) or not 2 <= len(items) <= 40:
        raise DeltaError("print edition dependency count is outside the bounded range")
    seen: set[str] = set()
    incomplete = 0
    for item in items:
        _cave_record(
            item,
            {
                "item_token",
                "kind",
                "window_start",
                "window_end",
                "dependencies",
                "incomplete",
                "instruction_provided",
                "release_provided",
            },
            "print edition dependency row",
        )
        token = _cave_token(item["item_token"], "print edition item token")
        if token in seen:
            raise DeltaError("print edition item token is duplicated")
        if item["kind"] not in {
            "manuscript",
            "plate",
            "imposition",
            "proof",
            "correction",
            "edition",
            "cancellation",
        }:
            raise DeltaError("print edition item kind is unsupported")
        start = _cave_timestamp(item["window_start"], "print edition start")
        end = _cave_timestamp(item["window_end"], "print edition end")
        if end <= start or (end - start).total_seconds() > 604_800:
            raise DeltaError("print edition window is reversed or over budget")
        deps = item["dependencies"]
        if not isinstance(deps, list):
            raise DeltaError("print edition dependencies are not a list")
        parsed = [_cave_token(value, "print edition dependency") for value in deps]
        ensure_unique(parsed, "print edition dependency")
        if any(value not in seen for value in parsed):
            raise DeltaError("print edition dependency is absent or forward-referenced")
        if not isinstance(item["incomplete"], bool):
            raise DeltaError("print edition incomplete state must be Boolean")
        incomplete += int(item["incomplete"])
        _print_required_false(item, ("instruction_provided", "release_provided"))
        seen.add(token)
    if incomplete == 0:
        raise DeltaError("print edition plan hides all incomplete work")
    _print_required_false(record, ("production_authorized", "canon_claimed"))
    return _print_valid("print_edition_dependencies", record_count=len(items))


def validate_print_si_placeholders(record: dict[str, Any]) -> dict[str, Any]:
    """Validate SI-typed fictional placeholders without measurement or prediction."""

    _cave_record(
        record,
        {
            "record_token",
            "sheet_area",
            "area_unit",
            "type_height",
            "leading",
            "margin",
            "length_unit",
            "pressure",
            "pressure_unit",
            "ink_film",
            "film_unit",
            "uncertainty",
            "real_measurement_present",
            "calibrated",
            "tolerance_decided",
            "prediction_made",
            "safety_cleared",
        },
        "print SI placeholder envelope",
    )
    _cave_token(record["record_token"], "print SI record token")
    _cave_finite(record["sheet_area"], "print sheet area", minimum=0.0, maximum=10_000.0, minimum_inclusive=False)
    _cave_finite(record["type_height"], "print type height", minimum=0.0, maximum=10.0, minimum_inclusive=False)
    _cave_finite(record["leading"], "print leading", minimum=0.0, maximum=10.0, minimum_inclusive=False)
    _cave_finite(record["margin"], "print margin", minimum=0.0, maximum=10.0, minimum_inclusive=False)
    _cave_finite(record["pressure"], "print pressure", minimum=0.0, maximum=1.0e12, minimum_inclusive=False)
    _cave_finite(record["ink_film"], "print ink film", minimum=0.0, maximum=1.0, minimum_inclusive=False)
    _cave_finite(record["uncertainty"], "print placeholder uncertainty", minimum=0.0, maximum=1.0e12, minimum_inclusive=False)
    if (
        record["area_unit"] != "m2"
        or record["length_unit"] != "m"
        or record["pressure_unit"] != "Pa"
        or record["film_unit"] != "m"
    ):
        raise DeltaError("print placeholder envelope uses unsupported SI units")
    _print_required_false(
        record,
        (
            "real_measurement_present",
            "calibrated",
            "tolerance_decided",
            "prediction_made",
            "safety_cleared",
        ),
    )
    return _print_valid("print_si_placeholders")


def validate_print_material_cues(record: dict[str, Any]) -> dict[str, Any]:
    """Validate unresolved print-material cues and a dominant stop."""

    _cave_record(
        record,
        {
            "cue_kinds",
            "resolution_state",
            "stop",
            "real_material_present",
            "diagnosis_made",
            "treatment_provided",
            "disposal_instruction",
            "emergency_instruction",
            "safety_cleared",
        },
        "print material cue board",
    )
    cues = record["cue_kinds"]
    allowed = {
        "ink",
        "solvent",
        "cleaner",
        "pigment",
        "adhesive",
        "ventilation",
        "fire",
        "allergy",
        "disposal",
    }
    if not isinstance(cues, list) or not cues or len(cues) > 20:
        raise DeltaError("print material cue list is invalid")
    parsed = [_cave_token(value, "print material cue") for value in cues]
    ensure_unique(parsed, "print material cue")
    if any(value not in allowed for value in parsed):
        raise DeltaError("print material cue is unsupported")
    if record["resolution_state"] != "unresolved" or record["stop"] is not True:
        raise DeltaError("print material cue lacks an unresolved dominant stop")
    _print_required_false(
        record,
        (
            "real_material_present",
            "diagnosis_made",
            "treatment_provided",
            "disposal_instruction",
            "emergency_instruction",
            "safety_cleared",
        ),
    )
    return _print_valid("print_material_cues", record_count=len(cues))


def validate_print_equipment_reservations(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional equipment isolation without inspection or use release."""

    _cave_record(
        record,
        {
            "equipment",
            "real_equipment_present",
            "inspected",
            "competence_claimed",
            "maintenance_instruction",
            "guarding_cleared",
            "use_released",
        },
        "print equipment reservation",
    )
    equipment = record["equipment"]
    if not isinstance(equipment, list) or not 2 <= len(equipment) <= 32:
        raise DeltaError("print equipment count is outside the bounded range")
    seen: set[str] = set()
    for item in equipment:
        _cave_record(
            item,
            {
                "equipment_token",
                "kind",
                "condition_state",
                "isolation_token",
                "quarantined",
            },
            "print equipment row",
        )
        token = _cave_token(item["equipment_token"], "print equipment token")
        if token in seen:
            raise DeltaError("print equipment token is duplicated")
        if item["kind"] not in {"press", "roller", "cutter", "quoin_key", "tool"}:
            raise DeltaError("print equipment kind is unsupported")
        if item["condition_state"] not in {"unresolved", "isolated"}:
            raise DeltaError("print equipment condition is unsupported")
        _cave_token(item["isolation_token"], "print equipment isolation token")
        if item["quarantined"] is not True:
            raise DeltaError("print equipment quarantine is not retained")
        seen.add(token)
    _print_required_false(
        record,
        (
            "real_equipment_present",
            "inspected",
            "competence_claimed",
            "maintenance_instruction",
            "guarding_cleared",
            "use_released",
        ),
    )
    return _print_valid("print_equipment_reservations", record_count=len(equipment))


def validate_print_privacy_notice(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional purpose and retention without personal information."""

    _cave_record(
        record,
        {
            "record_token",
            "purpose",
            "retention_days",
            "correction_available",
            "raw_identity_present",
            "contributor_inferred",
            "commission_inferred",
            "secondary_purpose",
            "disclosure_authorized",
            "privacy_complete",
        },
        "print privacy notice",
    )
    _cave_token(record["record_token"], "print privacy record token")
    if record["purpose"] != "synthetic_archive_notice":
        raise DeltaError("print privacy purpose is unsupported")
    retention = _require_nonnegative_int(record["retention_days"], "print privacy retention")
    if not 1 <= retention <= 3_650:
        raise DeltaError("print privacy retention is outside the bounded range")
    if record["correction_available"] is not True:
        raise DeltaError("print privacy correction is unavailable")
    _print_required_false(
        record,
        (
            "raw_identity_present",
            "contributor_inferred",
            "commission_inferred",
            "secondary_purpose",
            "disclosure_authorized",
            "privacy_complete",
        ),
    )
    return _print_valid("print_privacy_notice")


def validate_print_accessibility_companion(record: dict[str, Any]) -> dict[str, Any]:
    """Validate structural accessibility while reserving every human review."""

    _cave_record(
        record,
        {
            "headings",
            "text_alternative",
            "status_text",
            "colour_only",
            "keyboard_order",
            "manual_review_required",
            "assistive_technology_reviewed",
            "maori_language_reviewed",
            "affected_user_approved",
            "accessibility_complete",
        },
        "print accessibility companion",
    )
    headings = record["headings"]
    order = record["keyboard_order"]
    if not isinstance(headings, list) or not 2 <= len(headings) <= 16:
        raise DeltaError("print accessibility headings are invalid")
    if not all(isinstance(value, str) and value.strip() for value in headings):
        raise DeltaError("print accessibility heading is empty")
    ensure_unique(headings, "print accessibility heading")
    if not isinstance(order, list) or not order or len(order) > 32:
        raise DeltaError("print accessibility keyboard order is invalid")
    parsed_order = [_cave_token(value, "print accessibility focus token") for value in order]
    ensure_unique(parsed_order, "print accessibility focus token")
    if not isinstance(record["text_alternative"], str) or not record["text_alternative"].strip():
        raise DeltaError("print accessibility text alternative is absent")
    if not isinstance(record["status_text"], str) or not record["status_text"].strip():
        raise DeltaError("print accessibility status text is absent")
    if record["manual_review_required"] is not True:
        raise DeltaError("print accessibility manual review is not reserved")
    _print_required_false(
        record,
        (
            "colour_only",
            "assistive_technology_reviewed",
            "maori_language_reviewed",
            "affected_user_approved",
            "accessibility_complete",
        ),
    )
    return _print_valid("print_accessibility_companion")


def validate_print_rights_hold(record: dict[str, Any]) -> dict[str, Any]:
    """Validate unresolved print rights without deciding permission or ownership."""

    _cave_record(
        record,
        {
            "work_token",
            "source_token",
            "rightsholder_state",
            "license_state",
            "provenance_notice",
            "real_work_present",
            "authorship_decided",
            "typeface_use_released",
            "image_use_released",
            "reproduction_released",
            "publication_released",
            "exhibition_released",
            "derivative_use_released",
            "ownership_decided",
            "cultural_approval",
        },
        "print rights hold",
    )
    _cave_token(record["work_token"], "print work token")
    _cave_token(record["source_token"], "print rights source token")
    if record["rightsholder_state"] != "unresolved" or record["license_state"] != "unresolved":
        raise DeltaError("print rights state is not unresolved")
    if not isinstance(record["provenance_notice"], str) or not 1 <= len(record["provenance_notice"].strip()) <= 512:
        raise DeltaError("print provenance notice is invalid")
    _print_required_false(
        record,
        (
            "real_work_present",
            "authorship_decided",
            "typeface_use_released",
            "image_use_released",
            "reproduction_released",
            "publication_released",
            "exhibition_released",
            "derivative_use_released",
            "ownership_decided",
            "cultural_approval",
        ),
    )
    return _print_valid("print_rights_hold")


def validate_print_external_cues(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional workplace cues without safety or legal clearance."""

    _cave_record(
        record,
        {
            "cue_kinds",
            "stop",
            "real_workplace_present",
            "real_observation_present",
            "emergency_instruction",
            "safety_cleared",
            "legal_interpretation",
        },
        "print external cue board",
    )
    cues = record["cue_kinds"]
    allowed = {
        "electrical",
        "mechanical",
        "nip_point",
        "fire",
        "ventilation",
        "ergonomic",
        "noise",
    }
    if not isinstance(cues, list) or not cues or len(cues) > 16:
        raise DeltaError("print external cue list is invalid")
    parsed = [_cave_token(value, "print external cue") for value in cues]
    ensure_unique(parsed, "print external cue")
    if any(value not in allowed for value in parsed):
        raise DeltaError("print external cue is unsupported")
    if record["stop"] is not True:
        raise DeltaError("print external cue lacks a dominant stop")
    _print_required_false(
        record,
        (
            "real_workplace_present",
            "real_observation_present",
            "emergency_instruction",
            "safety_cleared",
            "legal_interpretation",
        ),
    )
    return _print_valid("print_external_cues", record_count=len(cues))


def validate_print_custody_placeholder(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional archive containment without ownership or transfer release."""

    _cave_record(
        record,
        {
            "containers",
            "items",
            "condition_state",
            "real_asset_present",
            "ownership_claimed",
            "authenticity_claimed",
            "handling_instruction",
            "transport_authorized",
            "custody_released",
        },
        "print custody placeholder",
    )
    containers = record["containers"]
    items = record["items"]
    if not isinstance(containers, list) or not 1 <= len(containers) <= 24:
        raise DeltaError("print container list is invalid")
    parsed_containers = [_cave_token(value, "print container token") for value in containers]
    ensure_unique(parsed_containers, "print container token")
    if not isinstance(items, list) or not 1 <= len(items) <= 48:
        raise DeltaError("print custody item list is invalid")
    seen: set[str] = set()
    for item in items:
        _cave_record(
            item,
            {"item_token", "item_kind", "container_token"},
            "print custody item",
        )
        token = _cave_token(item["item_token"], "print custody item token")
        if token in seen:
            raise DeltaError("print custody item token is duplicated")
        if item["item_kind"] not in {"folder", "box", "shelf", "impression", "plate", "loan"}:
            raise DeltaError("print custody item kind is unsupported")
        if item["container_token"] not in parsed_containers:
            raise DeltaError("print custody item references an absent container")
        seen.add(token)
    if record["condition_state"] != "unresolved":
        raise DeltaError("print custody condition is not unresolved")
    _print_required_false(
        record,
        (
            "real_asset_present",
            "ownership_claimed",
            "authenticity_claimed",
            "handling_instruction",
            "transport_authorized",
            "custody_released",
        ),
    )
    return _print_valid("print_custody_placeholder", record_count=len(items))


def validate_print_correction_lineage(record: dict[str, Any]) -> dict[str, Any]:
    """Validate append-only fictional print corrections with ambiguity retained."""

    _cave_record(
        record,
        {"records", "real_edition_present", "action_authorized", "canon_claimed"},
        "print correction lineage",
    )
    rows = record["records"]
    if not isinstance(rows, list) or not 2 <= len(rows) <= 40:
        raise DeltaError("print correction lineage is outside the bounded range")
    seen: set[str] = set()
    unresolved = 0
    for index, row in enumerate(rows):
        _cave_record(
            row,
            {
                "record_token",
                "parent_token",
                "event",
                "reason",
                "readback",
                "original_retained",
                "ambiguity_unresolved",
            },
            "print correction row",
        )
        token = _cave_token(row["record_token"], "print correction token")
        if token in seen:
            raise DeltaError("print correction token is duplicated")
        parent = row["parent_token"]
        if index == 0:
            if parent is not None or row["event"] != "manuscript":
                raise DeltaError("print correction lineage lacks a manuscript origin")
        elif not isinstance(parent, str) or parent not in seen:
            raise DeltaError("print correction parent is absent or forward-referenced")
        if row["event"] not in {
            "manuscript",
            "type",
            "plate",
            "proof",
            "edition",
            "cancelled",
            "superseded",
        }:
            raise DeltaError("print correction event is unsupported")
        if index > 0 and (not isinstance(row["reason"], str) or not row["reason"].strip()):
            raise DeltaError("print correction reason is absent")
        if row["readback"] is not True or row["original_retained"] is not True:
            raise DeltaError("print correction lacks readback or origin retention")
        if not isinstance(row["ambiguity_unresolved"], bool):
            raise DeltaError("print correction ambiguity flag is not Boolean")
        unresolved += int(row["ambiguity_unresolved"])
        seen.add(token)
    if unresolved == 0:
        raise DeltaError("print correction lineage hides all ambiguity")
    _print_required_false(record, ("real_edition_present", "action_authorized", "canon_claimed"))
    return _print_valid("print_correction_lineage", record_count=len(rows))


def validate_print_handover(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a bounded zero-person print-archive handover."""

    _cave_record(
        record,
        {
            "handover_token",
            "queue_ceiling",
            "active_queue",
            "unfinished_queue",
            "fatigue_cue",
            "stop",
            "correction_readback",
            "next_owner_placeholder",
            "real_worker_present",
            "performance_evaluated",
            "competence_claimed",
            "wellbeing_concluded",
            "work_released",
        },
        "print workload handover",
    )
    _cave_token(record["handover_token"], "print handover token")
    ceiling = _require_nonnegative_int(record["queue_ceiling"], "print queue ceiling")
    if not 1 <= ceiling <= 64:
        raise DeltaError("print queue ceiling is outside the bounded range")
    active = record["active_queue"]
    unfinished = record["unfinished_queue"]
    if not isinstance(active, list) or not active or len(active) > ceiling:
        raise DeltaError("print active queue is empty or over ceiling")
    if not isinstance(unfinished, list) or not unfinished:
        raise DeltaError("print unfinished queue must remain visible")
    active_tokens = [_cave_token(value, "print active task") for value in active]
    unfinished_tokens = [_cave_token(value, "print unfinished task") for value in unfinished]
    ensure_unique(active_tokens, "print active task")
    ensure_unique(unfinished_tokens, "print unfinished task")
    if any(value not in active_tokens for value in unfinished_tokens):
        raise DeltaError("print unfinished task is absent from the active queue")
    if record["fatigue_cue"] not in {"none", "watch", "stop"}:
        raise DeltaError("print fatigue cue is unsupported")
    if record["stop"] is not True or record["correction_readback"] is not True:
        raise DeltaError("print handover lacks a dominant stop or correction readback")
    _cave_token(record["next_owner_placeholder"], "print next-owner placeholder")
    _print_required_false(
        record,
        (
            "real_worker_present",
            "performance_evaluated",
            "competence_claimed",
            "wellbeing_concluded",
            "work_released",
        ),
    )
    return _print_valid("print_handover", record_count=len(active_tokens))


def validate_print_privacy_accessibility(record: dict[str, Any]) -> dict[str, Any]:
    """Validate paired privacy and accessibility records with separate gates."""

    _cave_record(record, {"privacy", "accessibility"}, "print privacy and accessibility pair")
    privacy = validate_print_privacy_notice(record["privacy"])
    accessibility = validate_print_accessibility_companion(record["accessibility"])
    return _print_valid(
        "print_privacy_accessibility",
        record_count=privacy["record_count"] + accessibility["record_count"],
    )


def validate_print_rights_custody(record: dict[str, Any]) -> dict[str, Any]:
    """Validate paired rights and custody records without combining their authority."""

    _cave_record(record, {"rights", "custody"}, "print rights and custody pair")
    rights = validate_print_rights_hold(record["rights"])
    custody = validate_print_custody_placeholder(record["custody"])
    return _print_valid(
        "print_rights_custody",
        record_count=rights["record_count"] + custody["record_count"],
    )


def validate_print_trinity_boundaries(record: dict[str, Any]) -> dict[str, Any]:
    """Validate explicit zero-evidence boundaries for GMUT, THOS, Freed ID, and CBR."""

    _cave_record(
        record,
        {
            "gmut_observations",
            "gmut_likelihoods",
            "thos_participants",
            "thos_operators",
            "freed_id_real_keys",
            "freed_id_real_proofs",
            "cbr_real_decisions",
            "psyche_inferences",
            "empirical_claimed",
            "deployment_claimed",
            "stage_20_claimed",
        },
        "print Trinity boundary record",
    )
    for field in (
        "gmut_observations",
        "gmut_likelihoods",
        "thos_participants",
        "thos_operators",
        "freed_id_real_keys",
        "freed_id_real_proofs",
        "cbr_real_decisions",
        "psyche_inferences",
    ):
        if _require_nonnegative_int(record[field], field) != 0:
            raise DeltaError(f"{field} must remain zero")
    _print_required_false(record, ("empirical_claimed", "deployment_claimed", "stage_20_claimed"))
    return _print_valid("print_trinity_boundaries")


def validate_print_zero_row_adapter(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a Library of Congress adapter contract that performs no operation."""

    _cave_record(
        record,
        {
            "source_url",
            "network_calls",
            "downloaded_rows",
            "ingested_rows",
            "credentials_requested",
            "rights_reviewed",
            "coverage_claimed",
            "completeness_claimed",
            "open_gap",
        },
        "print zero-row adapter",
    )
    if record["source_url"] not in {
        "https://www.loc.gov/apis/additional-apis/prints-and-photographs-api/",
        "https://www.loc.gov/apis/json-and-yaml/",
    }:
        raise DeltaError("print zero-row adapter source is unsupported")
    for field in ("network_calls", "downloaded_rows", "ingested_rows"):
        if _require_nonnegative_int(record[field], field) != 0:
            raise DeltaError(f"{field} must remain zero")
    _print_required_false(
        record,
        ("credentials_requested", "rights_reviewed", "coverage_claimed", "completeness_claimed"),
    )
    if record["open_gap"] is not True:
        raise DeltaError("print zero-row adapter must retain its open gap")
    return _print_valid("print_zero_row_adapter", record_count=0)


def elowen_fixture_cases() -> list[dict[str, Any]]:
    """Return fourteen bounded positives and five rejecting mutations per proposal."""

    packet = {
        "packet_token": "packet_alpha",
        "revision": 1,
        "source_pin": "sha256:" + ("b" * 64),
        "cancellation_state": "planned",
        "synthetic": True,
        "raw_identity_present": False,
        "real_workshop_present": False,
        "equipment_use_authorized": False,
        "reproduction_authorized": False,
    }
    topology = {
        "components": [
            {"component_token": "root_alpha", "kind": "root", "parent_token": None},
            {"component_token": "sort_alpha", "kind": "sort", "parent_token": "root_alpha"},
            {"component_token": "forme_alpha", "kind": "forme", "parent_token": "root_alpha"},
        ],
        "real_asset_present": False,
        "assembly_authorized": False,
        "equipment_use_authorized": False,
    }
    materials = {
        "lots": [
            {"lot_token": "lot_alpha", "source_token": "source_alpha", "material_class": "paper", "substitution_for": None, "quarantined": True},
            {"lot_token": "lot_beta", "source_token": "source_beta", "material_class": "ink", "substitution_for": "lot_alpha", "quarantined": True},
        ],
        "real_material_present": False,
        "authenticity_claimed": False,
        "suitability_claimed": False,
        "custody_claimed": False,
        "safety_cleared": False,
        "disposal_instruction": False,
    }
    dependencies = {
        "items": [
            {"item_token": "manuscript_alpha", "kind": "manuscript", "window_start": "2026-01-01T00:00:00Z", "window_end": "2026-01-02T00:00:00Z", "dependencies": [], "incomplete": False, "instruction_provided": False, "release_provided": False},
            {"item_token": "proof_alpha", "kind": "proof", "window_start": "2026-01-02T00:00:00Z", "window_end": "2026-01-03T00:00:00Z", "dependencies": ["manuscript_alpha"], "incomplete": True, "instruction_provided": False, "release_provided": False},
        ],
        "production_authorized": False,
        "canon_claimed": False,
    }
    placeholders = {
        "record_token": "si_alpha",
        "sheet_area": 1.0,
        "area_unit": "m2",
        "type_height": 0.01,
        "leading": 0.002,
        "margin": 0.02,
        "length_unit": "m",
        "pressure": 1000.0,
        "pressure_unit": "Pa",
        "ink_film": 0.00001,
        "film_unit": "m",
        "uncertainty": 1.0,
        "real_measurement_present": False,
        "calibrated": False,
        "tolerance_decided": False,
        "prediction_made": False,
        "safety_cleared": False,
    }
    material_cues = {
        "cue_kinds": ["ink", "ventilation", "fire"],
        "resolution_state": "unresolved",
        "stop": True,
        "real_material_present": False,
        "diagnosis_made": False,
        "treatment_provided": False,
        "disposal_instruction": False,
        "emergency_instruction": False,
        "safety_cleared": False,
    }
    equipment = {
        "equipment": [
            {"equipment_token": "press_alpha", "kind": "press", "condition_state": "isolated", "isolation_token": "isolation_alpha", "quarantined": True},
            {"equipment_token": "cutter_alpha", "kind": "cutter", "condition_state": "unresolved", "isolation_token": "isolation_beta", "quarantined": True},
        ],
        "real_equipment_present": False,
        "inspected": False,
        "competence_claimed": False,
        "maintenance_instruction": False,
        "guarding_cleared": False,
        "use_released": False,
    }
    privacy = {
        "record_token": "notice_alpha",
        "purpose": "synthetic_archive_notice",
        "retention_days": 30,
        "correction_available": True,
        "raw_identity_present": False,
        "contributor_inferred": False,
        "commission_inferred": False,
        "secondary_purpose": False,
        "disclosure_authorized": False,
        "privacy_complete": False,
    }
    accessibility = {
        "headings": ["Overview", "Status"],
        "text_alternative": "Synthetic print packet status.",
        "status_text": "Held for external review.",
        "colour_only": False,
        "keyboard_order": ["overview", "status"],
        "manual_review_required": True,
        "assistive_technology_reviewed": False,
        "maori_language_reviewed": False,
        "affected_user_approved": False,
        "accessibility_complete": False,
    }
    rights = {
        "work_token": "work_alpha",
        "source_token": "source_alpha",
        "rightsholder_state": "unresolved",
        "license_state": "unresolved",
        "provenance_notice": "Fictional source lineage only; every right remains unresolved.",
        "real_work_present": False,
        "authorship_decided": False,
        "typeface_use_released": False,
        "image_use_released": False,
        "reproduction_released": False,
        "publication_released": False,
        "exhibition_released": False,
        "derivative_use_released": False,
        "ownership_decided": False,
        "cultural_approval": False,
    }
    external = {
        "cue_kinds": ["electrical", "nip_point", "ventilation"],
        "stop": True,
        "real_workplace_present": False,
        "real_observation_present": False,
        "emergency_instruction": False,
        "safety_cleared": False,
        "legal_interpretation": False,
    }
    custody = {
        "containers": ["container_alpha"],
        "items": [{"item_token": "item_alpha", "item_kind": "impression", "container_token": "container_alpha"}],
        "condition_state": "unresolved",
        "real_asset_present": False,
        "ownership_claimed": False,
        "authenticity_claimed": False,
        "handling_instruction": False,
        "transport_authorized": False,
        "custody_released": False,
    }
    correction = {
        "records": [
            {"record_token": "record_alpha", "parent_token": None, "event": "manuscript", "reason": "", "readback": True, "original_retained": True, "ambiguity_unresolved": True},
            {"record_token": "record_beta", "parent_token": "record_alpha", "event": "proof", "reason": "fictional correction", "readback": True, "original_retained": True, "ambiguity_unresolved": True},
        ],
        "real_edition_present": False,
        "action_authorized": False,
        "canon_claimed": False,
    }
    handover = {
        "handover_token": "handover_alpha",
        "queue_ceiling": 4,
        "active_queue": ["task_alpha", "task_beta"],
        "unfinished_queue": ["task_beta"],
        "fatigue_cue": "watch",
        "stop": True,
        "correction_readback": True,
        "next_owner_placeholder": "owner_next",
        "real_worker_present": False,
        "performance_evaluated": False,
        "competence_claimed": False,
        "wellbeing_concluded": False,
        "work_released": False,
    }
    return [
        {"fixture_id": "EC6635-HF-001", "proposal_id": "EC6635-N001", "validator": "validate_print_work_packet", "positive": packet, "mutations": [
            {"label": "zero packet revision", "record": {**packet, "revision": 0}},
            {"label": "non-SHA256 packet source pin", "record": {**packet, "source_pin": "sha1:00"}},
            {"label": "equipment use authorization", "record": {**packet, "equipment_use_authorized": True}},
            {"label": "reproduction authorization", "record": {**packet, "reproduction_authorized": True}},
            {"label": "raw print identity presence", "record": {**packet, "raw_identity_present": True}},
        ]},
        {"fixture_id": "EC6635-HF-002", "proposal_id": "EC6635-N002", "validator": "validate_print_component_topology", "positive": topology, "mutations": [
            {"label": "duplicate print component", "record": {**topology, "components": [topology["components"][0], {**topology["components"][1], "component_token": "root_alpha"}, topology["components"][2]]}},
            {"label": "orphan print component", "record": {**topology, "components": [topology["components"][0], {**topology["components"][1], "parent_token": "root_missing"}, topology["components"][2]]}},
            {"label": "real print asset presence", "record": {**topology, "real_asset_present": True}},
            {"label": "print assembly authorization", "record": {**topology, "assembly_authorized": True}},
            {"label": "print equipment use authorization", "record": {**topology, "equipment_use_authorized": True}},
        ]},
        {"fixture_id": "EC6635-HF-003", "proposal_id": "EC6635-N003", "validator": "validate_print_material_lots", "positive": materials, "mutations": [
            {"label": "duplicate print material lot", "record": {**materials, "lots": [materials["lots"][0], {**materials["lots"][1], "lot_token": "lot_alpha"}]}},
            {"label": "unknown print material substitution", "record": {**materials, "lots": [materials["lots"][0], {**materials["lots"][1], "substitution_for": "lot_missing"}]}},
            {"label": "real print material presence", "record": {**materials, "real_material_present": True}},
            {"label": "print material authenticity claim", "record": {**materials, "authenticity_claimed": True}},
            {"label": "print material safety clearance", "record": {**materials, "safety_cleared": True}},
        ]},
        {"fixture_id": "EC6635-HF-004", "proposal_id": "EC6635-N004", "validator": "validate_print_edition_dependencies", "positive": dependencies, "mutations": [
            {"label": "forward print dependency", "record": {**dependencies, "items": [{**dependencies["items"][0], "dependencies": ["proof_alpha"]}, dependencies["items"][1]]}},
            {"label": "duplicate print dependency item", "record": {**dependencies, "items": [dependencies["items"][0], {**dependencies["items"][1], "item_token": "manuscript_alpha"}]}},
            {"label": "reversed print dependency window", "record": {**dependencies, "items": [{**dependencies["items"][0], "window_end": "2025-12-31T00:00:00Z"}, dependencies["items"][1]]}},
            {"label": "print instruction provided", "record": {**dependencies, "items": [{**dependencies["items"][0], "instruction_provided": True}, dependencies["items"][1]]}},
            {"label": "print production authorization", "record": {**dependencies, "production_authorized": True}},
        ]},
        {"fixture_id": "EC6635-HF-005", "proposal_id": "EC6635-N005", "validator": "validate_print_si_placeholders", "positive": placeholders, "mutations": [
            {"label": "nonfinite print sheet area", "record": {**placeholders, "sheet_area": float("nan")}},
            {"label": "unsupported print area unit", "record": {**placeholders, "area_unit": "cm2"}},
            {"label": "real print measurement", "record": {**placeholders, "real_measurement_present": True}},
            {"label": "print prediction made", "record": {**placeholders, "prediction_made": True}},
            {"label": "print SI safety clearance", "record": {**placeholders, "safety_cleared": True}},
        ]},
        {"fixture_id": "EC6635-HF-006", "proposal_id": "EC6635-N006", "validator": "validate_print_material_cues", "positive": material_cues, "mutations": [
            {"label": "unsupported print material cue", "record": {**material_cues, "cue_kinds": ["unknown"]}},
            {"label": "resolved print material cue", "record": {**material_cues, "resolution_state": "cleared"}},
            {"label": "print material stop overridden", "record": {**material_cues, "stop": False}},
            {"label": "print material treatment provided", "record": {**material_cues, "treatment_provided": True}},
            {"label": "print material safety clearance", "record": {**material_cues, "safety_cleared": True}},
        ]},
        {"fixture_id": "EC6635-HF-007", "proposal_id": "EC6635-N007", "validator": "validate_print_equipment_reservations", "positive": equipment, "mutations": [
            {"label": "duplicate print equipment", "record": {**equipment, "equipment": [equipment["equipment"][0], {**equipment["equipment"][1], "equipment_token": "press_alpha"}]}},
            {"label": "invalid equipment isolation token", "record": {**equipment, "equipment": [{**equipment["equipment"][0], "isolation_token": ""}, equipment["equipment"][1]]}},
            {"label": "print equipment inspection claim", "record": {**equipment, "inspected": True}},
            {"label": "print equipment competence claim", "record": {**equipment, "competence_claimed": True}},
            {"label": "print equipment use release", "record": {**equipment, "use_released": True}},
        ]},
        {"fixture_id": "EC6635-HF-008", "proposal_id": "EC6635-N008", "validator": "validate_print_privacy_notice", "positive": privacy, "mutations": [
            {"label": "raw contributor identity", "record": {**privacy, "raw_identity_present": True}},
            {"label": "contributor inference", "record": {**privacy, "contributor_inferred": True}},
            {"label": "print privacy secondary purpose", "record": {**privacy, "secondary_purpose": True}},
            {"label": "zero print privacy retention", "record": {**privacy, "retention_days": 0}},
            {"label": "print privacy completeness claim", "record": {**privacy, "privacy_complete": True}},
        ]},
        {"fixture_id": "EC6635-HF-009", "proposal_id": "EC6635-N009", "validator": "validate_print_accessibility_companion", "positive": accessibility, "mutations": [
            {"label": "missing print accessibility headings", "record": {**accessibility, "headings": []}},
            {"label": "missing print text alternative", "record": {**accessibility, "text_alternative": ""}},
            {"label": "colour-only print status", "record": {**accessibility, "colour_only": True}},
            {"label": "print manual review not reserved", "record": {**accessibility, "manual_review_required": False}},
            {"label": "print accessibility completeness claim", "record": {**accessibility, "accessibility_complete": True}},
        ]},
        {"fixture_id": "EC6635-HF-010", "proposal_id": "EC6635-N010", "validator": "validate_print_rights_hold", "positive": rights, "mutations": [
            {"label": "missing print rights source token", "record": {**rights, "source_token": ""}},
            {"label": "cleared print rightsholder state", "record": {**rights, "rightsholder_state": "cleared"}},
            {"label": "print reproduction release", "record": {**rights, "reproduction_released": True}},
            {"label": "print publication release", "record": {**rights, "publication_released": True}},
            {"label": "print cultural approval claim", "record": {**rights, "cultural_approval": True}},
        ]},
        {"fixture_id": "EC6635-HF-011", "proposal_id": "EC6635-N011", "validator": "validate_print_external_cues", "positive": external, "mutations": [
            {"label": "unsupported print external cue", "record": {**external, "cue_kinds": ["unknown"]}},
            {"label": "print external stop overridden", "record": {**external, "stop": False}},
            {"label": "real print workplace present", "record": {**external, "real_workplace_present": True}},
            {"label": "print emergency instruction", "record": {**external, "emergency_instruction": True}},
            {"label": "print legal interpretation", "record": {**external, "legal_interpretation": True}},
        ]},
        {"fixture_id": "EC6635-HF-012", "proposal_id": "EC6635-N012", "validator": "validate_print_custody_placeholder", "positive": custody, "mutations": [
            {"label": "duplicate print container", "record": {**custody, "containers": ["container_alpha", "container_alpha"]}},
            {"label": "orphan print custody container", "record": {**custody, "items": [{**custody["items"][0], "container_token": "container_missing"}]}},
            {"label": "real print custody asset", "record": {**custody, "real_asset_present": True}},
            {"label": "print ownership claim", "record": {**custody, "ownership_claimed": True}},
            {"label": "print transport authorization", "record": {**custody, "transport_authorized": True}},
        ]},
        {"fixture_id": "EC6635-HF-013", "proposal_id": "EC6635-N013", "validator": "validate_print_correction_lineage", "positive": correction, "mutations": [
            {"label": "duplicate print correction token", "record": {**correction, "records": [correction["records"][0], {**correction["records"][1], "record_token": "record_alpha"}]}},
            {"label": "forward print correction parent", "record": {**correction, "records": [correction["records"][0], {**correction["records"][1], "parent_token": "record_missing"}]}},
            {"label": "erased print correction origin", "record": {**correction, "records": [{**correction["records"][0], "original_retained": False}, correction["records"][1]]}},
            {"label": "print correction reason absent", "record": {**correction, "records": [correction["records"][0], {**correction["records"][1], "reason": ""}]}},
            {"label": "print correction readback absent", "record": {**correction, "records": [correction["records"][0], {**correction["records"][1], "readback": False}]}},
        ]},
        {"fixture_id": "EC6635-HF-014", "proposal_id": "EC6635-N014", "validator": "validate_print_handover", "positive": handover, "mutations": [
            {"label": "zero print queue ceiling", "record": {**handover, "queue_ceiling": 0}},
            {"label": "unknown unfinished print task", "record": {**handover, "unfinished_queue": ["task_missing"]}},
            {"label": "print handover stop overridden", "record": {**handover, "stop": False}},
            {"label": "print handover readback absent", "record": {**handover, "correction_readback": False}},
            {"label": "print worker performance evaluation", "record": {**handover, "performance_evaluated": True}},
        ]},
    ]


def elowen_mutation_payload() -> dict[str, Any]:
    """Execute and retain every Elowen mutation with zero negative credit."""

    validators = {
        function.__name__: function
        for function in (
            validate_print_work_packet,
            validate_print_component_topology,
            validate_print_material_lots,
            validate_print_edition_dependencies,
            validate_print_si_placeholders,
            validate_print_material_cues,
            validate_print_equipment_reservations,
            validate_print_privacy_notice,
            validate_print_accessibility_companion,
            validate_print_rights_hold,
            validate_print_external_cues,
            validate_print_custody_placeholder,
            validate_print_correction_lineage,
            validate_print_handover,
        )
    }
    records: list[dict[str, Any]] = []
    positives: list[dict[str, Any]] = []
    cases = elowen_fixture_cases()
    for case_index, case in enumerate(cases, 1):
        validator = validators[case["validator"]]
        result = validator(case["positive"])
        if result.get("valid") is not True:
            raise DeltaError(f"Elowen positive fixture failed: {case['fixture_id']}")
        positives.append(
            {
                "fixture_id": case["fixture_id"],
                "proposal_id": case["proposal_id"],
                "validator": case["validator"],
                "valid": True,
            }
        )
        if len(case["mutations"]) != 5:
            raise DeltaError(f"Elowen fixture does not declare five mutations: {case['fixture_id']}")
        for mutation_index, mutation in enumerate(case["mutations"], 1):
            try:
                validator(mutation["record"])
            except (DeltaError, UnicodeError, ValueError, TypeError) as exc:
                records.append(
                    {
                        "fixture_id": f"EC6635-HF-{case_index:03d}-{mutation_index:02d}",
                        "mutation_id": f"EC6635-MUT-{case_index:03d}-{mutation_index:02d}",
                        "proposal_id": case["proposal_id"],
                        "validator": case["validator"],
                        "failed_witness": mutation["label"],
                        "rejected": True,
                        "error_class": type(exc).__name__,
                        "zero_credit": True,
                    }
                )
            else:
                raise DeltaError(
                    f"Elowen negative mutation was not rejected: {case['fixture_id']}:{mutation_index}"
                )
    return {
        "schema": f"{SCHEMA}.elowen-mutation-matrix.v1",
        "profile": "elowen-v663-v5",
        "proposal_count": len(positives),
        "mutations_per_proposal": 5,
        "negative_fixture_count": len(records),
        "rejected_fixture_count": sum(record["rejected"] is True for record in records),
        "positive_fixture_count": len(positives),
        "passing_fixture_count": len(positives),
        "records": records,
        "positive_records": positives,
        "failed_witnesses_erased": 0,
        "valid": len(records) == 70 and len(positives) == 14,
        "boundary": "Seventy rejected synthetic mutations and fourteen passing letterpress record-shape fixtures only; no real person, workshop, press, cutter, type, material, print, archive object, measurement, right, authority act, empirical result, production result, or independent reproduction.",
    }


def elowen_hardening_payload() -> dict[str, Any]:
    """Return every retained Elowen rejection plus fourteen bounded positives."""

    matrix = elowen_mutation_payload()
    if not matrix["valid"]:
        raise DeltaError("one or more Elowen hardening fixtures failed")
    return {
        "schema": f"{SCHEMA}.hardening-fixtures.v9",
        "profile": "elowen-v663-v5",
        "negative_fixture_count": matrix["negative_fixture_count"],
        "rejected_fixture_count": matrix["rejected_fixture_count"],
        "positive_fixture_count": matrix["positive_fixture_count"],
        "passing_fixture_count": matrix["passing_fixture_count"],
        "records": matrix["records"],
        "full_mutation_matrix_negative_count": matrix["negative_fixture_count"],
        "real_person_present": False,
        "real_workshop_present": False,
        "real_equipment_present": False,
        "real_material_present": False,
        "real_print_present": False,
        "real_archive_object_present": False,
        "real_measurement_present": False,
        "equipment_use_authorized": False,
        "reproduction_authorized": False,
        "rights_released": False,
        "privacy_complete": False,
        "accessibility_complete": False,
        "professional_authority": False,
        "legal_authority": False,
        "cultural_authority": False,
        "maori_authority": False,
        "exhaustive_security": False,
        "valid": True,
        "boundary": "All seventy preregistered letterpress mutations were rejected and fourteen paired positives passed as bounded software fixtures only; not printing, equipment, chemical, handling, conservation, rights, privacy, accessibility, professional, legal, cultural, Maori-authority, production, empirical, independent-reproduction, or Stage 20 evidence.",
    }


def _glass_required_false(record: dict[str, Any], fields: Iterable[str]) -> None:
    """Require explicit false values at every stained-glass authority boundary."""

    for field in fields:
        _cave_false(record[field], f"stained-glass {field.replace('_', ' ')}")


def _glass_valid(kind: str, *, record_count: int = 1) -> dict[str, Any]:
    return {
        "kind": kind,
        "record_count": record_count,
        "real_person_present": False,
        "real_panel_present": False,
        "real_material_present": False,
        "real_measurement_present": False,
        "handling_authorized": False,
        "intervention_authorized": False,
        "professional_authority": False,
        "legal_authority": False,
        "cultural_authority": False,
        "maori_authority": False,
        "valid": True,
    }


def validate_stained_glass_survey_packet(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a fictional documentation packet without authorizing survey work."""

    _cave_record(
        record,
        {
            "packet_token",
            "revision",
            "source_pin",
            "cancellation_state",
            "synthetic",
            "raw_identity_present",
            "real_panel_present",
            "survey_authorized",
            "intervention_authorized",
            "safety_cleared",
        },
        "stained-glass survey packet",
    )
    _cave_token(record["packet_token"], "stained-glass packet token")
    revision = _require_nonnegative_int(record["revision"], "stained-glass revision")
    if not 1 <= revision <= 10_000:
        raise DeltaError("stained-glass revision is outside the bounded range")
    if re.fullmatch(r"sha256:[0-9a-f]{64}", record["source_pin"]) is None:
        raise DeltaError("stained-glass source pin is not an explicit SHA-256 commitment")
    if record["cancellation_state"] not in {"planned", "cancelled", "superseded"}:
        raise DeltaError("stained-glass cancellation state is unsupported")
    if record["synthetic"] is not True:
        raise DeltaError("stained-glass survey packet must remain synthetic")
    _glass_required_false(
        record,
        (
            "raw_identity_present",
            "real_panel_present",
            "survey_authorized",
            "intervention_authorized",
            "safety_cleared",
        ),
    )
    return _glass_valid("stained_glass_survey_packet")


def validate_stained_glass_topology(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional panel and glazing-component topology."""

    _cave_record(
        record,
        {"components", "real_panel_present", "handling_authorized", "intervention_authorized"},
        "stained-glass topology",
    )
    components = record["components"]
    if not isinstance(components, list) or not 4 <= len(components) <= 96:
        raise DeltaError("stained-glass component count is outside the bounded range")
    seen: set[str] = set()
    kinds: set[str] = set()
    allowed = {"root", "panel", "quarry", "came", "support_bar", "tie_wire", "frame", "glazing"}
    for index, component in enumerate(components):
        _cave_record(component, {"component_token", "kind", "parent_token"}, "stained-glass component")
        token = _cave_token(component["component_token"], "stained-glass component token")
        if token in seen:
            raise DeltaError("stained-glass component token is duplicated")
        if component["kind"] not in allowed:
            raise DeltaError("stained-glass component kind is unsupported")
        parent = component["parent_token"]
        if index == 0:
            if component["kind"] != "root" or parent is not None:
                raise DeltaError("stained-glass topology lacks a valid root")
        elif not isinstance(parent, str) or parent not in seen:
            raise DeltaError("stained-glass parent is absent or forward-referenced")
        seen.add(token)
        kinds.add(component["kind"])
    if not {"panel", "quarry", "came"} <= kinds:
        raise DeltaError("stained-glass topology lacks panel, quarry, and came placeholders")
    _glass_required_false(record, ("real_panel_present", "handling_authorized", "intervention_authorized"))
    return _glass_valid("stained_glass_topology", record_count=len(components))


def validate_stained_glass_material_lots(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional glass and repair-material provenance lots."""

    _cave_record(
        record,
        {
            "lots",
            "real_material_present",
            "authenticity_claimed",
            "suitability_claimed",
            "treatment_authorized",
            "safety_cleared",
        },
        "stained-glass material ledger",
    )
    lots = record["lots"]
    if not isinstance(lots, list) or not 2 <= len(lots) <= 48:
        raise DeltaError("stained-glass material-lot count is outside the bounded range")
    seen: set[str] = set()
    allowed = {"glass", "came", "solder", "putty", "paint", "foil", "support", "coating", "repair"}
    for lot in lots:
        _cave_record(
            lot,
            {"lot_token", "source_token", "material_class", "substitution_for", "quarantined"},
            "stained-glass material lot",
        )
        token = _cave_token(lot["lot_token"], "stained-glass material-lot token")
        if token in seen:
            raise DeltaError("stained-glass material-lot token is duplicated")
        _cave_token(lot["source_token"], "stained-glass material source token")
        if lot["material_class"] not in allowed:
            raise DeltaError("stained-glass material class is unsupported")
        substitute = lot["substitution_for"]
        if substitute is not None and (not isinstance(substitute, str) or substitute not in seen):
            raise DeltaError("stained-glass substitution is absent or forward-referenced")
        if lot["quarantined"] is not True:
            raise DeltaError("stained-glass material quarantine is not retained")
        seen.add(token)
    _glass_required_false(
        record,
        ("real_material_present", "authenticity_claimed", "suitability_claimed", "treatment_authorized", "safety_cleared"),
    )
    return _glass_valid("stained_glass_material_lots", record_count=len(lots))


def validate_stained_glass_document_dependencies(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional documentation dependencies and visible incompleteness."""

    _cave_record(record, {"items", "action_authorized", "canon_claimed"}, "stained-glass dependency plan")
    items = record["items"]
    if not isinstance(items, list) or not 2 <= len(items) <= 48:
        raise DeltaError("stained-glass dependency count is outside the bounded range")
    seen: set[str] = set()
    incomplete = 0
    allowed = {"intake", "diagram", "condition", "option", "review", "correction", "cancellation", "handover"}
    for item in items:
        _cave_record(
            item,
            {"item_token", "kind", "dependencies", "incomplete", "instruction_provided", "release_provided"},
            "stained-glass dependency row",
        )
        token = _cave_token(item["item_token"], "stained-glass dependency token")
        if token in seen:
            raise DeltaError("stained-glass dependency token is duplicated")
        if item["kind"] not in allowed:
            raise DeltaError("stained-glass dependency kind is unsupported")
        dependencies = item["dependencies"]
        if not isinstance(dependencies, list):
            raise DeltaError("stained-glass dependencies are not a list")
        parsed = [_cave_token(value, "stained-glass dependency") for value in dependencies]
        ensure_unique(parsed, "stained-glass dependency")
        if any(value not in seen for value in parsed):
            raise DeltaError("stained-glass dependency is absent or forward-referenced")
        if not isinstance(item["incomplete"], bool):
            raise DeltaError("stained-glass incomplete state must be Boolean")
        incomplete += int(item["incomplete"])
        _glass_required_false(item, ("instruction_provided", "release_provided"))
        seen.add(token)
    if incomplete == 0:
        raise DeltaError("stained-glass plan hides all incomplete work")
    _glass_required_false(record, ("action_authorized", "canon_claimed"))
    return _glass_valid("stained_glass_document_dependencies", record_count=len(items))


def validate_stained_glass_si_placeholders(record: dict[str, Any]) -> dict[str, Any]:
    """Validate SI-typed fictional placeholders without measurement or diagnosis."""

    _cave_record(
        record,
        {
            "record_token",
            "panel_area",
            "area_unit",
            "displacement",
            "length_unit",
            "uncertainty",
            "real_measurement_present",
            "calibrated",
            "diagnosis_made",
            "tolerance_decided",
            "prediction_made",
            "safety_cleared",
        },
        "stained-glass SI placeholder envelope",
    )
    _cave_token(record["record_token"], "stained-glass SI token")
    _cave_finite(record["panel_area"], "stained-glass panel area", minimum=0.0, maximum=10_000.0, minimum_inclusive=False)
    _cave_finite(record["displacement"], "stained-glass displacement", minimum=-10.0, maximum=10.0)
    _cave_finite(record["uncertainty"], "stained-glass uncertainty", minimum=0.0, maximum=10.0, minimum_inclusive=False)
    if record["area_unit"] != "m2" or record["length_unit"] != "m":
        raise DeltaError("stained-glass placeholder envelope uses unsupported SI units")
    _glass_required_false(
        record,
        ("real_measurement_present", "calibrated", "diagnosis_made", "tolerance_decided", "prediction_made", "safety_cleared"),
    )
    return _glass_valid("stained_glass_si_placeholders")


def validate_stained_glass_condition_cues(record: dict[str, Any]) -> dict[str, Any]:
    """Validate unresolved visual cues with a dominant no-action stop."""

    _cave_record(
        record,
        {
            "cue_kinds",
            "resolution_state",
            "stop",
            "real_panel_present",
            "diagnosis_made",
            "treatment_provided",
            "emergency_instruction",
            "safety_cleared",
        },
        "stained-glass condition cue board",
    )
    allowed = {"bowing", "bulging", "crack", "loss", "corrosion", "condensation", "paint_change", "putty_change", "frame_change"}
    cues = record["cue_kinds"]
    if not isinstance(cues, list) or not cues or len(cues) > 24:
        raise DeltaError("stained-glass condition cue list is invalid")
    parsed = [_cave_token(value, "stained-glass condition cue") for value in cues]
    ensure_unique(parsed, "stained-glass condition cue")
    if any(value not in allowed for value in parsed):
        raise DeltaError("stained-glass condition cue is unsupported")
    if record["resolution_state"] != "unresolved" or record["stop"] is not True:
        raise DeltaError("stained-glass cue board lacks an unresolved dominant stop")
    _glass_required_false(
        record,
        ("real_panel_present", "diagnosis_made", "treatment_provided", "emergency_instruction", "safety_cleared"),
    )
    return _glass_valid("stained_glass_condition_cues", record_count=len(cues))


def validate_stained_glass_equipment_reservations(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional access and equipment isolation without use release."""

    _cave_record(
        record,
        {"equipment", "real_equipment_present", "inspected", "competence_claimed", "use_released", "safety_cleared"},
        "stained-glass equipment reservation",
    )
    equipment = record["equipment"]
    if not isinstance(equipment, list) or not 2 <= len(equipment) <= 32:
        raise DeltaError("stained-glass equipment count is outside the bounded range")
    allowed = {"access_aid", "inspection_light", "magnifier", "soldering_tool", "dust_control", "edge_guard", "enclosure"}
    seen: set[str] = set()
    for item in equipment:
        _cave_record(item, {"equipment_token", "kind", "condition_state", "isolation_token", "quarantined"}, "stained-glass equipment row")
        token = _cave_token(item["equipment_token"], "stained-glass equipment token")
        if token in seen:
            raise DeltaError("stained-glass equipment token is duplicated")
        if item["kind"] not in allowed or item["condition_state"] not in {"unresolved", "isolated"}:
            raise DeltaError("stained-glass equipment kind or condition is unsupported")
        _cave_token(item["isolation_token"], "stained-glass isolation token")
        if item["quarantined"] is not True:
            raise DeltaError("stained-glass equipment quarantine is not retained")
        seen.add(token)
    _glass_required_false(record, ("real_equipment_present", "inspected", "competence_claimed", "use_released", "safety_cleared"))
    return _glass_valid("stained_glass_equipment_reservations", record_count=len(equipment))


def validate_stained_glass_privacy_accessibility(record: dict[str, Any]) -> dict[str, Any]:
    """Validate minimized synthetic notice fields and reserve all human review."""

    _cave_record(
        record,
        {
            "record_token",
            "purpose",
            "retention_days",
            "correction_available",
            "headings",
            "text_alternative",
            "status_text",
            "manual_review_required",
            "raw_identity_present",
            "location_precision_present",
            "secondary_purpose",
            "colour_only",
            "assistive_technology_reviewed",
            "maori_language_reviewed",
            "affected_user_approved",
            "privacy_complete",
            "accessibility_complete",
        },
        "stained-glass privacy and accessibility notice",
    )
    _cave_token(record["record_token"], "stained-glass notice token")
    if record["purpose"] != "synthetic_conservation_documentation":
        raise DeltaError("stained-glass notice purpose is unsupported")
    retention = _require_nonnegative_int(record["retention_days"], "stained-glass retention")
    if not 1 <= retention <= 3_650 or record["correction_available"] is not True:
        raise DeltaError("stained-glass retention or correction contract is invalid")
    headings = record["headings"]
    if not isinstance(headings, list) or not 2 <= len(headings) <= 16 or not all(isinstance(value, str) and value.strip() for value in headings):
        raise DeltaError("stained-glass headings are invalid")
    ensure_unique(headings, "stained-glass heading")
    if not isinstance(record["text_alternative"], str) or not record["text_alternative"].strip():
        raise DeltaError("stained-glass text alternative is absent")
    if not isinstance(record["status_text"], str) or not record["status_text"].strip():
        raise DeltaError("stained-glass status text is absent")
    if record["manual_review_required"] is not True:
        raise DeltaError("stained-glass manual accessibility review is not reserved")
    _glass_required_false(
        record,
        (
            "raw_identity_present",
            "location_precision_present",
            "secondary_purpose",
            "colour_only",
            "assistive_technology_reviewed",
            "maori_language_reviewed",
            "affected_user_approved",
            "privacy_complete",
            "accessibility_complete",
        ),
    )
    return _glass_valid("stained_glass_privacy_accessibility")


def validate_stained_glass_rights_custody(record: dict[str, Any]) -> dict[str, Any]:
    """Validate unresolved rights and fictional custody placeholders."""

    _cave_record(
        record,
        {
            "work_token",
            "source_token",
            "rightsholder_state",
            "license_state",
            "containers",
            "items",
            "condition_state",
            "real_asset_present",
            "ownership_decided",
            "handling_authorized",
            "transport_authorized",
            "publication_released",
            "cultural_approval",
        },
        "stained-glass rights and custody hold",
    )
    _cave_token(record["work_token"], "stained-glass work token")
    _cave_token(record["source_token"], "stained-glass rights source token")
    if record["rightsholder_state"] != "unresolved" or record["license_state"] != "unresolved":
        raise DeltaError("stained-glass rights state is not unresolved")
    containers = record["containers"]
    if not isinstance(containers, list) or not containers:
        raise DeltaError("stained-glass custody containers are absent")
    parsed_containers = [_cave_token(value, "stained-glass container token") for value in containers]
    ensure_unique(parsed_containers, "stained-glass container token")
    items = record["items"]
    if not isinstance(items, list) or not items:
        raise DeltaError("stained-glass custody items are absent")
    seen_items: list[str] = []
    for item in items:
        _cave_record(item, {"item_token", "item_kind", "container_token"}, "stained-glass custody item")
        seen_items.append(_cave_token(item["item_token"], "stained-glass custody item token"))
        if item["item_kind"] not in {"diagram", "image_placeholder", "condition_record", "option_record"}:
            raise DeltaError("stained-glass custody item kind is unsupported")
        if item["container_token"] not in parsed_containers:
            raise DeltaError("stained-glass custody item references an unknown container")
    ensure_unique(seen_items, "stained-glass custody item token")
    if record["condition_state"] != "unresolved":
        raise DeltaError("stained-glass custody condition is not unresolved")
    _glass_required_false(
        record,
        ("real_asset_present", "ownership_decided", "handling_authorized", "transport_authorized", "publication_released", "cultural_approval"),
    )
    return _glass_valid("stained_glass_rights_custody", record_count=len(items))


def validate_stained_glass_external_cues(record: dict[str, Any]) -> dict[str, Any]:
    """Validate fictional external hazard cues without safety or legal clearance."""

    _cave_record(
        record,
        {"cue_kinds", "stop", "real_site_present", "real_observation_present", "emergency_instruction", "safety_cleared", "legal_interpretation"},
        "stained-glass external cue board",
    )
    allowed = {"access", "height", "lead", "dust", "heat", "sharp_edge", "electrical", "falling_material", "occupancy"}
    cues = record["cue_kinds"]
    if not isinstance(cues, list) or not cues or len(cues) > 20:
        raise DeltaError("stained-glass external cue list is invalid")
    parsed = [_cave_token(value, "stained-glass external cue") for value in cues]
    ensure_unique(parsed, "stained-glass external cue")
    if any(value not in allowed for value in parsed) or record["stop"] is not True:
        raise DeltaError("stained-glass external cue is unsupported or stop is absent")
    _glass_required_false(record, ("real_site_present", "real_observation_present", "emergency_instruction", "safety_cleared", "legal_interpretation"))
    return _glass_valid("stained_glass_external_cues", record_count=len(cues))


def validate_stained_glass_correction_lineage(record: dict[str, Any]) -> dict[str, Any]:
    """Validate append-only fictional correction lineage and readback."""

    _cave_record(record, {"records", "real_record_present", "action_authorized", "canon_claimed"}, "stained-glass correction lineage")
    rows = record["records"]
    if not isinstance(rows, list) or not 2 <= len(rows) <= 48:
        raise DeltaError("stained-glass correction count is outside the bounded range")
    seen: set[str] = set()
    for index, row in enumerate(rows):
        _cave_record(row, {"record_token", "parent_token", "event", "reason", "readback", "original_retained", "ambiguity_unresolved"}, "stained-glass correction row")
        token = _cave_token(row["record_token"], "stained-glass correction token")
        if token in seen:
            raise DeltaError("stained-glass correction token is duplicated")
        parent = row["parent_token"]
        if index == 0:
            if parent is not None:
                raise DeltaError("stained-glass correction origin has a parent")
        elif not isinstance(parent, str) or parent not in seen:
            raise DeltaError("stained-glass correction parent is absent or forward-referenced")
        if row["event"] not in {"intake", "condition", "option", "correction", "cancellation", "handover"}:
            raise DeltaError("stained-glass correction event is unsupported")
        if index > 0 and (not isinstance(row["reason"], str) or not row["reason"].strip()):
            raise DeltaError("stained-glass correction reason is absent")
        if row["readback"] is not True or row["original_retained"] is not True or row["ambiguity_unresolved"] is not True:
            raise DeltaError("stained-glass correction retention or readback failed")
        seen.add(token)
    _glass_required_false(record, ("real_record_present", "action_authorized", "canon_claimed"))
    return _glass_valid("stained_glass_correction_lineage", record_count=len(rows))


def validate_stained_glass_handover(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a fictional workload and handover stop without evaluating people."""

    _cave_record(
        record,
        {
            "handover_token",
            "queue_ceiling",
            "active_queue",
            "unfinished_queue",
            "fatigue_cue",
            "stop",
            "correction_readback",
            "next_owner_placeholder",
            "real_worker_present",
            "performance_evaluated",
            "competence_claimed",
            "wellbeing_concluded",
            "work_released",
        },
        "stained-glass handover",
    )
    _cave_token(record["handover_token"], "stained-glass handover token")
    ceiling = _require_nonnegative_int(record["queue_ceiling"], "stained-glass queue ceiling")
    active = record["active_queue"]
    unfinished = record["unfinished_queue"]
    if not 1 <= ceiling <= 64 or not isinstance(active, list) or len(active) > ceiling:
        raise DeltaError("stained-glass active queue is outside the bounded range")
    parsed_active = [_cave_token(value, "stained-glass active task") for value in active]
    ensure_unique(parsed_active, "stained-glass active task")
    if not isinstance(unfinished, list):
        raise DeltaError("stained-glass unfinished queue is not a list")
    parsed_unfinished = [_cave_token(value, "stained-glass unfinished task") for value in unfinished]
    ensure_unique(parsed_unfinished, "stained-glass unfinished task")
    if any(value not in parsed_active for value in parsed_unfinished):
        raise DeltaError("stained-glass unfinished task is absent from the active queue")
    if record["fatigue_cue"] not in {"none", "watch", "stop"} or record["stop"] is not True or record["correction_readback"] is not True:
        raise DeltaError("stained-glass handover stop or readback is absent")
    _cave_token(record["next_owner_placeholder"], "stained-glass next-owner placeholder")
    _glass_required_false(record, ("real_worker_present", "performance_evaluated", "competence_claimed", "wellbeing_concluded", "work_released"))
    return _glass_valid("stained_glass_handover", record_count=len(active))


def validate_stained_glass_trinity_boundaries(record: dict[str, Any]) -> dict[str, Any]:
    """Validate nonconversion across GMUT, THOS, Freed ID, CBR, and Stage 20."""

    _cave_record(
        record,
        {
            "gmut_state",
            "thos_state",
            "freed_id_state",
            "cbr_state",
            "real_likelihood_evaluated",
            "empirical_claim_made",
            "participant_effect_claimed",
            "live_identity_event",
            "rights_decision_made",
            "psyche_law_claimed",
            "agi_asi_claimed",
            "consciousness_personhood_claimed",
            "theory_of_everything_claimed",
            "stage20_promoted",
        },
        "stained-glass Trinity boundary board",
    )
    if record["gmut_state"] != "typed_symbolic" or record["thos_state"] != "proxy_only" or record["freed_id_state"] != "synthetic_nonproduction" or record["cbr_state"] != "exact_gated":
        raise DeltaError("stained-glass Trinity boundary state is unsupported")
    _glass_required_false(
        record,
        (
            "real_likelihood_evaluated",
            "empirical_claim_made",
            "participant_effect_claimed",
            "live_identity_event",
            "rights_decision_made",
            "psyche_law_claimed",
            "agi_asi_claimed",
            "consciousness_personhood_claimed",
            "theory_of_everything_claimed",
            "stage20_promoted",
        ),
    )
    return _glass_valid("stained_glass_trinity_boundaries")


def validate_stained_glass_zero_row_adapter(record: dict[str, Any]) -> dict[str, Any]:
    """Validate the V&A official-source adapter's zero-row refusal state."""

    _cave_record(
        record,
        {
            "source_uri",
            "network_called",
            "downloaded_rows",
            "ingested_rows",
            "real_record_present",
            "likelihood_evaluated",
            "constraint_emitted",
            "empirical_claim_made",
        },
        "stained-glass zero-row adapter",
    )
    if record["source_uri"] != "https://developers.vam.ac.uk/guide/v2/":
        raise DeltaError("stained-glass zero-row adapter source is not the pinned official guide")
    if record["network_called"] is not False:
        raise DeltaError("stained-glass zero-row adapter made a network call")
    if _require_nonnegative_int(record["downloaded_rows"], "downloaded rows") != 0 or _require_nonnegative_int(record["ingested_rows"], "ingested rows") != 0:
        raise DeltaError("stained-glass zero-row adapter received or ingested rows")
    _glass_required_false(record, ("real_record_present", "likelihood_evaluated", "constraint_emitted", "empirical_claim_made"))
    return _glass_valid("stained_glass_zero_row_adapter", record_count=0)


def _glass_mutation(record: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    mutated = deepcopy(record)
    path = spec["path"]
    cursor: Any = mutated
    for component in path[:-1]:
        cursor = cursor[component]
    if spec.get("delete") is True:
        del cursor[path[-1]]
    else:
        cursor[path[-1]] = spec["value"]
    return mutated


def sylven_fixture_cases() -> list[dict[str, Any]]:
    """Return fourteen positive fixtures and five declared mutations per fixture."""

    packet = {
        "packet_token": "packet_alpha",
        "revision": 1,
        "source_pin": "sha256:" + ("a" * 64),
        "cancellation_state": "planned",
        "synthetic": True,
        "raw_identity_present": False,
        "real_panel_present": False,
        "survey_authorized": False,
        "intervention_authorized": False,
        "safety_cleared": False,
    }
    topology = {
        "components": [
            {"component_token": "root_alpha", "kind": "root", "parent_token": None},
            {"component_token": "panel_alpha", "kind": "panel", "parent_token": "root_alpha"},
            {"component_token": "quarry_alpha", "kind": "quarry", "parent_token": "panel_alpha"},
            {"component_token": "came_alpha", "kind": "came", "parent_token": "panel_alpha"},
        ],
        "real_panel_present": False,
        "handling_authorized": False,
        "intervention_authorized": False,
    }
    materials = {
        "lots": [
            {"lot_token": "lot_alpha", "source_token": "source_alpha", "material_class": "glass", "substitution_for": None, "quarantined": True},
            {"lot_token": "lot_beta", "source_token": "source_beta", "material_class": "came", "substitution_for": "lot_alpha", "quarantined": True},
        ],
        "real_material_present": False,
        "authenticity_claimed": False,
        "suitability_claimed": False,
        "treatment_authorized": False,
        "safety_cleared": False,
    }
    dependencies = {
        "items": [
            {"item_token": "intake_alpha", "kind": "intake", "dependencies": [], "incomplete": False, "instruction_provided": False, "release_provided": False},
            {"item_token": "condition_alpha", "kind": "condition", "dependencies": ["intake_alpha"], "incomplete": True, "instruction_provided": False, "release_provided": False},
        ],
        "action_authorized": False,
        "canon_claimed": False,
    }
    placeholders = {
        "record_token": "metric_alpha",
        "panel_area": 1.0,
        "area_unit": "m2",
        "displacement": 0.001,
        "length_unit": "m",
        "uncertainty": 0.0001,
        "real_measurement_present": False,
        "calibrated": False,
        "diagnosis_made": False,
        "tolerance_decided": False,
        "prediction_made": False,
        "safety_cleared": False,
    }
    cues = {
        "cue_kinds": ["bowing", "crack", "corrosion"],
        "resolution_state": "unresolved",
        "stop": True,
        "real_panel_present": False,
        "diagnosis_made": False,
        "treatment_provided": False,
        "emergency_instruction": False,
        "safety_cleared": False,
    }
    equipment = {
        "equipment": [
            {"equipment_token": "access_alpha", "kind": "access_aid", "condition_state": "unresolved", "isolation_token": "isolation_alpha", "quarantined": True},
            {"equipment_token": "light_alpha", "kind": "inspection_light", "condition_state": "isolated", "isolation_token": "isolation_beta", "quarantined": True},
        ],
        "real_equipment_present": False,
        "inspected": False,
        "competence_claimed": False,
        "use_released": False,
        "safety_cleared": False,
    }
    privacy_accessibility = {
        "record_token": "notice_alpha",
        "purpose": "synthetic_conservation_documentation",
        "retention_days": 30,
        "correction_available": True,
        "headings": ["Overview", "Status"],
        "text_alternative": "Synthetic stained-glass panel diagram status.",
        "status_text": "Held for qualified and affected-user review.",
        "manual_review_required": True,
        "raw_identity_present": False,
        "location_precision_present": False,
        "secondary_purpose": False,
        "colour_only": False,
        "assistive_technology_reviewed": False,
        "maori_language_reviewed": False,
        "affected_user_approved": False,
        "privacy_complete": False,
        "accessibility_complete": False,
    }
    rights_custody = {
        "work_token": "work_alpha",
        "source_token": "source_alpha",
        "rightsholder_state": "unresolved",
        "license_state": "unresolved",
        "containers": ["container_alpha"],
        "items": [{"item_token": "diagram_alpha", "item_kind": "diagram", "container_token": "container_alpha"}],
        "condition_state": "unresolved",
        "real_asset_present": False,
        "ownership_decided": False,
        "handling_authorized": False,
        "transport_authorized": False,
        "publication_released": False,
        "cultural_approval": False,
    }
    external = {
        "cue_kinds": ["access", "lead", "dust", "sharp_edge"],
        "stop": True,
        "real_site_present": False,
        "real_observation_present": False,
        "emergency_instruction": False,
        "safety_cleared": False,
        "legal_interpretation": False,
    }
    correction = {
        "records": [
            {"record_token": "record_alpha", "parent_token": None, "event": "intake", "reason": "", "readback": True, "original_retained": True, "ambiguity_unresolved": True},
            {"record_token": "record_beta", "parent_token": "record_alpha", "event": "correction", "reason": "synthetic correction", "readback": True, "original_retained": True, "ambiguity_unresolved": True},
        ],
        "real_record_present": False,
        "action_authorized": False,
        "canon_claimed": False,
    }
    handover = {
        "handover_token": "handover_alpha",
        "queue_ceiling": 4,
        "active_queue": ["task_alpha", "task_beta"],
        "unfinished_queue": ["task_beta"],
        "fatigue_cue": "watch",
        "stop": True,
        "correction_readback": True,
        "next_owner_placeholder": "owner_next",
        "real_worker_present": False,
        "performance_evaluated": False,
        "competence_claimed": False,
        "wellbeing_concluded": False,
        "work_released": False,
    }
    trinity = {
        "gmut_state": "typed_symbolic",
        "thos_state": "proxy_only",
        "freed_id_state": "synthetic_nonproduction",
        "cbr_state": "exact_gated",
        "real_likelihood_evaluated": False,
        "empirical_claim_made": False,
        "participant_effect_claimed": False,
        "live_identity_event": False,
        "rights_decision_made": False,
        "psyche_law_claimed": False,
        "agi_asi_claimed": False,
        "consciousness_personhood_claimed": False,
        "theory_of_everything_claimed": False,
        "stage20_promoted": False,
    }
    zero_row = {
        "source_uri": "https://developers.vam.ac.uk/guide/v2/",
        "network_called": False,
        "downloaded_rows": 0,
        "ingested_rows": 0,
        "real_record_present": False,
        "likelihood_evaluated": False,
        "constraint_emitted": False,
        "empirical_claim_made": False,
    }

    def case(fid: int, proposal: int, validator: str, positive: dict[str, Any], mutations: list[dict[str, Any]]) -> dict[str, Any]:
        if len(mutations) != 5:
            raise DeltaError("Sylven fixture case must declare exactly five mutations")
        return {"fixture_id": f"SA6636-HF-{fid:03d}", "proposal_id": f"SA6636-N{proposal:03d}", "validator": validator, "positive": positive, "mutations": mutations}

    def mutation(label: str, path: tuple[Any, ...], value: Any = None, *, delete: bool = False) -> dict[str, Any]:
        return {"label": label, "path": path, "value": value, "delete": delete}

    return [
        case(1, 1, "validate_stained_glass_survey_packet", packet, [
            mutation("missing stained-glass packet token", ("packet_token",), delete=True),
            mutation("unexpected stained-glass packet field", ("unexpected_guard",), True),
            mutation("zero stained-glass packet revision", ("revision",), 0),
            mutation("non-SHA256 stained-glass source pin", ("source_pin",), "sha1:00"),
            mutation("stained-glass intervention authorization", ("intervention_authorized",), True),
        ]),
        case(2, 2, "validate_stained_glass_topology", topology, [
            mutation("missing stained-glass topology", ("components",), delete=True),
            mutation("unexpected stained-glass topology field", ("unexpected_guard",), True),
            mutation("duplicate stained-glass component token", ("components", 1, "component_token"), "root_alpha"),
            mutation("orphan stained-glass component", ("components", 1, "parent_token"), "root_missing"),
            mutation("stained-glass handling authorization", ("handling_authorized",), True),
        ]),
        case(3, 3, "validate_stained_glass_material_lots", materials, [
            mutation("missing stained-glass lots", ("lots",), delete=True),
            mutation("unexpected stained-glass material field", ("unexpected_guard",), True),
            mutation("duplicate stained-glass lot token", ("lots", 1, "lot_token"), "lot_alpha"),
            mutation("unknown stained-glass substitution", ("lots", 1, "substitution_for"), "lot_missing"),
            mutation("stained-glass treatment authorization", ("treatment_authorized",), True),
        ]),
        case(4, 4, "validate_stained_glass_document_dependencies", dependencies, [
            mutation("missing stained-glass dependency items", ("items",), delete=True),
            mutation("unexpected stained-glass dependency field", ("unexpected_guard",), True),
            mutation("forward stained-glass dependency", ("items", 0, "dependencies"), ["condition_alpha"]),
            mutation("hidden stained-glass incomplete work", ("items", 1, "incomplete"), False),
            mutation("stained-glass action authorization", ("action_authorized",), True),
        ]),
        case(5, 5, "validate_stained_glass_si_placeholders", placeholders, [
            mutation("missing stained-glass SI token", ("record_token",), delete=True),
            mutation("unexpected stained-glass SI field", ("unexpected_guard",), True),
            mutation("nonfinite stained-glass panel area", ("panel_area",), float("nan")),
            mutation("unsupported stained-glass area unit", ("area_unit",), "cm2"),
            mutation("stained-glass measurement claim", ("real_measurement_present",), True),
        ]),
        case(6, 6, "validate_stained_glass_condition_cues", cues, [
            mutation("missing stained-glass condition cues", ("cue_kinds",), delete=True),
            mutation("unexpected stained-glass condition field", ("unexpected_guard",), True),
            mutation("unsupported stained-glass condition cue", ("cue_kinds",), ["unknown"]),
            mutation("stained-glass condition stop overridden", ("stop",), False),
            mutation("stained-glass diagnosis claim", ("diagnosis_made",), True),
        ]),
        case(7, 7, "validate_stained_glass_equipment_reservations", equipment, [
            mutation("missing stained-glass equipment", ("equipment",), delete=True),
            mutation("unexpected stained-glass equipment field", ("unexpected_guard",), True),
            mutation("duplicate stained-glass equipment token", ("equipment", 1, "equipment_token"), "access_alpha"),
            mutation("empty stained-glass isolation token", ("equipment", 0, "isolation_token"), ""),
            mutation("stained-glass equipment use release", ("use_released",), True),
        ]),
        case(8, 8, "validate_stained_glass_privacy_accessibility", privacy_accessibility, [
            mutation("missing stained-glass notice purpose", ("purpose",), delete=True),
            mutation("unexpected stained-glass notice field", ("unexpected_guard",), True),
            mutation("raw stained-glass identity", ("raw_identity_present",), True),
            mutation("missing stained-glass text alternative", ("text_alternative",), ""),
            mutation("stained-glass accessibility completeness claim", ("accessibility_complete",), True),
        ]),
        case(9, 10, "validate_stained_glass_rights_custody", rights_custody, [
            mutation("missing stained-glass rights source", ("source_token",), delete=True),
            mutation("unexpected stained-glass rights field", ("unexpected_guard",), True),
            mutation("cleared stained-glass rightsholder state", ("rightsholder_state",), "cleared"),
            mutation("orphan stained-glass custody item", ("items", 0, "container_token"), "container_missing"),
            mutation("stained-glass cultural approval claim", ("cultural_approval",), True),
        ]),
        case(10, 11, "validate_stained_glass_external_cues", external, [
            mutation("missing stained-glass external cues", ("cue_kinds",), delete=True),
            mutation("unexpected stained-glass external field", ("unexpected_guard",), True),
            mutation("unsupported stained-glass external cue", ("cue_kinds",), ["unknown"]),
            mutation("stained-glass external stop overridden", ("stop",), False),
            mutation("stained-glass safety clearance", ("safety_cleared",), True),
        ]),
        case(11, 13, "validate_stained_glass_correction_lineage", correction, [
            mutation("missing stained-glass correction records", ("records",), delete=True),
            mutation("unexpected stained-glass correction field", ("unexpected_guard",), True),
            mutation("duplicate stained-glass correction token", ("records", 1, "record_token"), "record_alpha"),
            mutation("erased stained-glass correction origin", ("records", 0, "original_retained"), False),
            mutation("stained-glass correction readback absent", ("records", 1, "readback"), False),
        ]),
        case(12, 14, "validate_stained_glass_handover", handover, [
            mutation("missing stained-glass handover token", ("handover_token",), delete=True),
            mutation("unexpected stained-glass handover field", ("unexpected_guard",), True),
            mutation("zero stained-glass queue ceiling", ("queue_ceiling",), 0),
            mutation("unknown unfinished stained-glass task", ("unfinished_queue",), ["task_missing"]),
            mutation("stained-glass performance evaluation", ("performance_evaluated",), True),
        ]),
        case(13, 18, "validate_stained_glass_trinity_boundaries", trinity, [
            mutation("unsupported stained-glass GMUT state", ("gmut_state",), "empirical"),
            mutation("unsupported stained-glass THOS state", ("thos_state",), "deployed"),
            mutation("live stained-glass identity event", ("live_identity_event",), True),
            mutation("stained-glass psyche-law claim", ("psyche_law_claimed",), True),
            mutation("stained-glass Stage 20 promotion", ("stage20_promoted",), True),
        ]),
        case(14, 19, "validate_stained_glass_zero_row_adapter", zero_row, [
            mutation("missing stained-glass source URI", ("source_uri",), delete=True),
            mutation("stained-glass adapter network call", ("network_called",), True),
            mutation("stained-glass adapter downloaded row", ("downloaded_rows",), 1),
            mutation("stained-glass adapter ingested row", ("ingested_rows",), 1),
            mutation("stained-glass empirical claim", ("empirical_claim_made",), True),
        ]),
    ]


def sylven_mutation_payload() -> dict[str, Any]:
    """Execute and retain every Sylven mutation with zero negative credit."""

    validators = {
        function.__name__: function
        for function in (
            validate_stained_glass_survey_packet,
            validate_stained_glass_topology,
            validate_stained_glass_material_lots,
            validate_stained_glass_document_dependencies,
            validate_stained_glass_si_placeholders,
            validate_stained_glass_condition_cues,
            validate_stained_glass_equipment_reservations,
            validate_stained_glass_privacy_accessibility,
            validate_stained_glass_rights_custody,
            validate_stained_glass_external_cues,
            validate_stained_glass_correction_lineage,
            validate_stained_glass_handover,
            validate_stained_glass_trinity_boundaries,
            validate_stained_glass_zero_row_adapter,
        )
    }
    records: list[dict[str, Any]] = []
    positives: list[dict[str, Any]] = []
    cases = sylven_fixture_cases()
    for case_index, case in enumerate(cases, 1):
        validator = validators[case["validator"]]
        result = validator(case["positive"])
        if result.get("valid") is not True:
            raise DeltaError(f"Sylven positive fixture failed: {case['fixture_id']}")
        positives.append(
            {
                "fixture_id": case["fixture_id"],
                "proposal_id": case["proposal_id"],
                "validator": case["validator"],
                "valid": True,
            }
        )
        if len(case["mutations"]) != 5:
            raise DeltaError(f"Sylven fixture does not declare five mutations: {case['fixture_id']}")
        for mutation_index, mutation in enumerate(case["mutations"], 1):
            mutated = _glass_mutation(case["positive"], mutation)
            try:
                validator(mutated)
            except (DeltaError, UnicodeError, ValueError, TypeError, KeyError) as exc:
                records.append(
                    {
                        "fixture_id": f"SA6636-HF-{case_index:03d}-{mutation_index:02d}",
                        "mutation_id": f"SA6636-MUT-{case_index:03d}-{mutation_index:02d}",
                        "proposal_id": case["proposal_id"],
                        "validator": case["validator"],
                        "failed_witness": mutation["label"],
                        "rejected": True,
                        "error_class": type(exc).__name__,
                        "zero_credit": True,
                    }
                )
            else:
                raise DeltaError(f"Sylven negative mutation was not rejected: {case['fixture_id']}:{mutation_index}")
    return {
        "schema": f"{SCHEMA}.sylven-mutation-matrix.v1",
        "profile": "sylven-v663-v6",
        "proposal_count": len(positives),
        "mutations_per_proposal": 5,
        "negative_fixture_count": len(records),
        "rejected_fixture_count": sum(record["rejected"] is True for record in records),
        "positive_fixture_count": len(positives),
        "passing_fixture_count": len(positives),
        "records": records,
        "positive_records": positives,
        "failed_witnesses_erased": 0,
        "valid": len(records) == 70 and len(positives) == 14,
        "boundary": "Seventy rejected synthetic mutations and fourteen passing stained-glass documentation record-shape fixtures only; no real person, site, panel, window, glass, came, material, equipment, measurement, inspection, diagnosis, treatment, handling, right, authority act, empirical result, production result, or independent reproduction.",
    }


def sylven_hardening_payload() -> dict[str, Any]:
    """Return every retained Sylven rejection plus fourteen bounded positives."""

    matrix = sylven_mutation_payload()
    if not matrix["valid"]:
        raise DeltaError("one or more Sylven hardening fixtures failed")
    return {
        "schema": f"{SCHEMA}.hardening-fixtures.v10",
        "profile": "sylven-v663-v6",
        "negative_fixture_count": matrix["negative_fixture_count"],
        "rejected_fixture_count": matrix["rejected_fixture_count"],
        "positive_fixture_count": matrix["positive_fixture_count"],
        "passing_fixture_count": matrix["passing_fixture_count"],
        "records": matrix["records"],
        "full_mutation_matrix_negative_count": matrix["negative_fixture_count"],
        "real_person_present": False,
        "real_site_present": False,
        "real_panel_present": False,
        "real_material_present": False,
        "real_equipment_present": False,
        "real_measurement_present": False,
        "survey_authorized": False,
        "handling_authorized": False,
        "intervention_authorized": False,
        "safety_cleared": False,
        "rights_released": False,
        "privacy_complete": False,
        "accessibility_complete": False,
        "professional_authority": False,
        "legal_authority": False,
        "cultural_authority": False,
        "maori_authority": False,
        "exhaustive_security": False,
        "valid": True,
        "boundary": "All seventy preregistered stained-glass mutations were rejected and fourteen paired positives passed as bounded software fixtures only; not survey, conservation, handling, equipment, lead, dust, access, safety, rights, privacy, accessibility, professional, legal, cultural, Maori-authority, production, empirical, independent-reproduction, or Stage 20 evidence.",
    }


def hardening_payload_for_profile(profile: str) -> dict[str, Any]:
    """Select one exact bounded fixture family; reject implicit substitution."""

    if profile == "ilyra-v662-v6":
        return hardening_payload()
    if profile == "auren-v662-v7":
        return auren_hardening_payload()
    if profile == "sable-v662-v8":
        return sable_hardening_payload()
    if profile == "caelen-v663-v1":
        return caelen_hardening_payload()
    if profile == "orin-v663-v2":
        return orin_hardening_payload()
    if profile == "liora-v663-v3":
        return liora_hardening_payload()
    if profile == "tamar-v663-v4":
        return tamar_hardening_payload()
    if profile == "elowen-v663-v5":
        return elowen_hardening_payload()
    if profile == "sylven-v663-v6":
        return sylven_hardening_payload()
    raise DeltaError(f"unknown hardening profile: {profile}")


def ensure_unique(values: Iterable[str], label: str) -> list[str]:
    items = list(values)
    if len(items) != len(set(items)):
        raise DeltaError(f"duplicate {label} values rejected")
    return items


def run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    command = ["git", "-C", str(repo), *args]
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if check and result.returncode:
        raise DeltaError(
            f"git command failed ({result.returncode}): {' '.join(args)}: {result.stderr.strip()}"
        )
    return result


def run_git_bytes(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode:
        error = result.stderr.decode("utf-8", errors="replace").strip()
        raise DeltaError(f"git command failed ({result.returncode}): {' '.join(args)}: {error}")
    return result


def resolve_commit(repo: Path, value: str) -> str:
    result = run_git(repo, "rev-parse", "--verify", "--end-of-options", f"{value}^{{commit}}")
    resolved = result.stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", resolved):
        raise DeltaError(f"commit did not resolve to a full object id: {value}")
    return resolved


def parse_name_status_z(raw: bytes) -> list[dict[str, Any]]:
    """Parse Git's NUL-framed name-status stream without line ambiguity."""
    tokens = raw.split(b"\0")
    if not tokens or tokens[-1] != b"":
        raise DeltaError("NUL-delimited Git delta did not terminate cleanly")
    tokens.pop()
    rows: list[dict[str, Any]] = []
    index = 0
    while index < len(tokens):
        try:
            status = tokens[index].decode("ascii", errors="strict")
        except UnicodeDecodeError as exc:
            raise DeltaError("non-ASCII Git delta status rejected") from exc
        index += 1
        path_count = 2 if status.startswith(("R", "C")) else 1
        if index + path_count > len(tokens):
            raise DeltaError(f"malformed NUL-delimited delta row: {status}")
        try:
            path_tokens = [token.decode("utf-8", errors="strict") for token in tokens[index:index + path_count]]
        except UnicodeDecodeError as exc:
            raise DeltaError(f"non-UTF-8 Git delta path rejected for status {status}") from exc
        index += path_count
        if status.startswith(("R", "C")):
            old_path = normalize_relative(path_tokens[0])
            path = normalize_relative(path_tokens[1])
        else:
            old_path = None
            path = normalize_relative(path_tokens[0])
        rows.append({"status": status, "path": path, "old_path": old_path})
    return rows


def delta_rows(repo: Path, source: str, target: str) -> list[dict[str, Any]]:
    source_id = resolve_commit(repo, source)
    target_id = resolve_commit(repo, target)
    ancestor = run_git(repo, "merge-base", "--is-ancestor", source_id, target_id, check=False)
    if ancestor.returncode != 0:
        raise DeltaError("source is not an ancestor of target")
    raw = run_git_bytes(
        repo,
        "diff",
        "--name-status",
        "-z",
        "--find-renames",
        "--end-of-options",
        source_id,
        target_id,
    ).stdout
    rows = parse_name_status_z(raw)
    paths = [row["path"] for row in rows]
    ensure_unique(paths, "delta path")
    return rows


def tree_entry(repo: Path, commit: str, relative_path: str) -> dict[str, str] | None:
    path = normalize_relative(relative_path)
    raw = run_git_bytes(repo, "ls-tree", "-z", commit, "--", path).stdout
    if not raw:
        return None
    records = raw.split(b"\0")
    if records[-1] != b"" or len(records) != 2:
        raise DeltaError(f"ambiguous tree entry for {path}")
    try:
        metadata, observed_raw = records[0].split(b"\t", 1)
        mode_raw, type_raw, object_raw = metadata.split(b" ")
        observed = observed_raw.decode("utf-8", errors="strict")
        mode = mode_raw.decode("ascii", errors="strict")
        object_type = type_raw.decode("ascii", errors="strict")
        object_id = object_raw.decode("ascii", errors="strict")
    except (ValueError, UnicodeDecodeError) as exc:
        raise DeltaError(f"malformed tree entry for {path}") from exc
    if normalize_relative(observed) != path or not re.fullmatch(r"[0-9a-f]{40}", object_id):
        raise DeltaError(f"unexpected tree entry for {path}")
    return {"mode": mode, "object_type": object_type, "object_id": object_id}


def blob_object(repo: Path, object_id: str) -> bytes:
    if not re.fullmatch(r"[0-9a-f]{40}", object_id):
        raise DeltaError("invalid blob object id")
    result = run_git_bytes(repo, "cat-file", "blob", object_id)
    return result.stdout


def blob_at(repo: Path, commit: str, relative_path: str) -> bytes:
    entry = tree_entry(repo, commit, relative_path)
    if entry is None or entry["object_type"] != "blob":
        raise DeltaError(f"unable to read exact blob {relative_path} at {commit}")
    return blob_object(repo, entry["object_id"])


def manifest_payload(repo: Path, source: str, target: str) -> dict[str, Any]:
    source_id = resolve_commit(repo, source)
    target_id = resolve_commit(repo, target)
    entries: list[dict[str, Any]] = []
    for row in delta_rows(repo, source_id, target_id):
        entry = dict(row)
        prior_path = row["old_path"] or row["path"]
        old_entry = tree_entry(repo, source_id, prior_path)
        new_entry = tree_entry(repo, target_id, row["path"])
        if row["status"].startswith("D"):
            entry.update(
                {
                    "bytes": 0,
                    "sha256": None,
                    "git_blob": None,
                    "mode": None,
                    "object_type": None,
                    "old_mode": old_entry["mode"] if old_entry else None,
                    "old_object_type": old_entry["object_type"] if old_entry else None,
                }
            )
        else:
            if new_entry is None:
                raise DeltaError(f"missing target tree entry for {row['path']}")
            if new_entry["object_type"] != "blob" or new_entry["mode"] not in ALLOWED_BLOB_MODES:
                raise DeltaError(
                    f"unsupported target entry kind for {row['path']}: "
                    f"{new_entry['mode']} {new_entry['object_type']}"
                )
            content = blob_object(repo, new_entry["object_id"])
            entry.update(
                {
                    "bytes": len(content),
                    "sha256": sha256_bytes(content),
                    "git_blob": new_entry["object_id"],
                    "mode": new_entry["mode"],
                    "object_type": new_entry["object_type"],
                    "old_mode": old_entry["mode"] if old_entry else None,
                    "old_object_type": old_entry["object_type"] if old_entry else None,
                }
            )
        entries.append(entry)
    path_audit = audit_paths(row["path"] for row in entries)
    if not path_audit["valid"]:
        raise DeltaError("exact delta contains a Unicode, control-character, or collision path issue")
    stable_commitment = {
        "source_commit": source_id,
        "target_commit": target_id,
        "entries": entries,
    }
    return {
        "schema": f"{SCHEMA}.manifest",
        "generated_at_utc": utc_now(),
        "source_commit": source_id,
        "target_commit": target_id,
        "entry_count": len(entries),
        "entries": entries,
        "path_audit": path_audit,
        "merkle_root_sha256": merkle_root(entries),
        "canonical_commitment_sha256": canonical_json_sha256(stable_commitment),
        "scope": "exact source-to-target owner delta only",
        "valid": True,
    }


def write_json(path: Path | None, payload: dict[str, Any]) -> None:
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path is None:
        sys.stdout.write(rendered)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8", newline="\n")


def write_json_exclusive(path: Path, payload: dict[str, Any]) -> None:
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        if os.name == "nt":
            import ctypes
            import msvcrt
            from ctypes import wintypes

            create_file = ctypes.WinDLL("kernel32", use_last_error=True).CreateFileW
            create_file.argtypes = [
                wintypes.LPCWSTR,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.LPVOID,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.HANDLE,
            ]
            create_file.restype = wintypes.HANDLE
            handle_value = create_file(
                os.path.abspath(path),
                0x40000000,
                0,
                None,
                1,
                0x00000080 | 0x00200000,
                None,
            )
            invalid_handle = wintypes.HANDLE(-1).value
            if handle_value == invalid_handle:
                error = ctypes.get_last_error()
                if error in {80, 183}:
                    raise FileExistsError(error, "exclusive receipt path already exists", str(path))
                raise OSError(error, "unable to create exclusive receipt", str(path))
            try:
                descriptor = msvcrt.open_osfhandle(handle_value, os.O_WRONLY | getattr(os, "O_BINARY", 0))
            except Exception:
                ctypes.WinDLL("kernel32", use_last_error=True).CloseHandle(handle_value)
                raise
        else:
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            descriptor = os.open(path, flags, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(rendered)
    except FileExistsError as exc:
        raise DeltaError("canonical receipt already exists; aggregate replay is forbidden") from exc


def exact_paths(repo: Path, source: str, target: str, suffix: str | None = None) -> list[str]:
    rows = delta_rows(repo, source, target)
    paths = [row["path"] for row in rows if not row["status"].startswith("D")]
    if suffix:
        paths = [path for path in paths if path.lower().endswith(suffix.lower())]
    return paths


def json_payload(repo: Path, source: str, target: str) -> dict[str, Any]:
    target_id = resolve_commit(repo, target)
    records = []
    for path in exact_paths(repo, source, target, ".json"):
        raw = blob_at(repo, target_id, path)
        try:
            parsed = strict_json_loads(raw, path)
        except DeltaError as exc:
            raise DeltaError(f"JSON parse failed for {path}: {exc}") from exc
        records.append(
            {
                "path": path,
                "bytes": len(raw),
                "top_level_type": type(parsed).__name__,
                "canonical_sha256": canonical_json_sha256(parsed),
                "duplicate_keys": 0,
            }
        )
    return {
        "schema": f"{SCHEMA}.json",
        "source_commit": resolve_commit(repo, source),
        "target_commit": target_id,
        "parsed_count": len(records),
        "records": records,
        "valid": True,
    }


def markdown_target_records(repo: Path, target: str, path: str, text: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for match in re.finditer(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", text):
        raw_target = match.group(1).strip().split(maxsplit=1)[0].strip("<>")
        parsed = urlsplit(raw_target)
        scheme = parsed.scheme.lower()
        issue: str | None = None
        resolved_path: str | None = None
        if scheme in UNSAFE_LINK_SCHEMES:
            issue = f"unsafe scheme: {scheme}"
        elif scheme and scheme not in {"http", "https", "mailto"}:
            issue = f"unreviewed scheme: {scheme}"
        elif not scheme and not raw_target.startswith("#"):
            candidate = parsed.path.replace("\\", "/")
            if re.match(r"^[A-Za-z]:", candidate) or candidate.startswith("/"):
                issue = "absolute local target"
            elif candidate:
                parent = PurePosixPath(path).parent
                parts: list[str] = []
                for part in (parent / candidate).parts:
                    if part in {"", "."}:
                        continue
                    if part == "..":
                        if not parts:
                            issue = "target escapes repository root"
                            break
                        parts.pop()
                    else:
                        parts.append(part)
                if issue is None:
                    resolved_path = normalize_relative(PurePosixPath(*parts).as_posix())
                    if tree_entry(repo, target, resolved_path) is None:
                        issue = "missing committed local target"
        records.append(
            {
                "target": raw_target,
                "scheme": scheme or "relative",
                "resolved_path": resolved_path,
                "issue": issue,
                "valid": issue is None,
            }
        )
    return records


def markdown_payload(repo: Path, source: str, target: str) -> dict[str, Any]:
    target_id = resolve_commit(repo, target)
    records = []
    for path in exact_paths(repo, source, target, ".md"):
        try:
            text = blob_at(repo, target_id, path).decode("utf-8")
        except UnicodeDecodeError as exc:
            raise DeltaError(f"Markdown is not UTF-8: {path}") from exc
        if not text.strip():
            raise DeltaError(f"empty Markdown file: {path}")
        targets = markdown_target_records(repo, target_id, path, text)
        records.append(
            {
                "path": path,
                "words": len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE)),
                "headings": len(re.findall(r"(?m)^#{1,6}\s+", text)),
                "target_count": len(targets),
                "target_issues": [record for record in targets if not record["valid"]],
            }
        )
    issues = [
        {"path": record["path"], **target}
        for record in records
        for target in record["target_issues"]
    ]
    return {
        "schema": f"{SCHEMA}.markdown",
        "source_commit": resolve_commit(repo, source),
        "target_commit": target_id,
        "checked_count": len(records),
        "records": records,
        "target_issue_count": len(issues),
        "target_issues": issues,
        "valid": not issues,
        "boundary": "Structural exact-delta Markdown target review only; not complete accessibility or external-link safety assurance.",
    }


def python_payload(repo: Path, source: str, target: str) -> dict[str, Any]:
    target_id = resolve_commit(repo, target)
    records = []
    for path in exact_paths(repo, source, target, ".py"):
        raw = blob_at(repo, target_id, path)
        try:
            source_text = raw.decode("utf-8")
            compile(source_text, path, "exec", dont_inherit=True)
        except (UnicodeDecodeError, SyntaxError) as exc:
            raise DeltaError(f"Python compile failed for {path}: {exc}") from exc
        records.append({"path": path, "bytes": len(raw), "sha256": sha256_bytes(raw)})
    return {
        "schema": f"{SCHEMA}.python",
        "source_commit": resolve_commit(repo, source),
        "target_commit": target_id,
        "compiled_count": len(records),
        "records": records,
        "valid": True,
    }


def privacy_payload(repo: Path, source: str, target: str) -> dict[str, Any]:
    target_id = resolve_commit(repo, target)
    files = 0
    candidates: list[dict[str, str]] = []
    for path in exact_paths(repo, source, target):
        raw = blob_at(repo, target_id, path)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        files += 1
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": label})
    return {
        "schema": f"{SCHEMA}.privacy",
        "source_commit": resolve_commit(repo, source),
        "target_commit": target_id,
        "classes": sorted(PRIVATE_PATTERNS),
        "scanned_text_files": files,
        "candidate_count": len(candidates),
        "confirmed_hits": candidates,
        "valid": not candidates,
        "boundary": "Five-class exact-delta pattern scan only; not complete privacy assurance.",
    }


def security_payload(repo: Path, source: str, target: str) -> dict[str, Any]:
    target_id = resolve_commit(repo, target)
    checked = 0
    findings: list[dict[str, str]] = []
    for path in exact_paths(repo, source, target, ".py"):
        checked += 1
        text = blob_at(repo, target_id, path).decode("utf-8")
        for label, pattern in SECURITY_PATTERNS.items():
            if pattern.search(text):
                findings.append({"path": path, "rule": label, "severity": "review"})
    return {
        "schema": f"{SCHEMA}.security",
        "source_commit": resolve_commit(repo, source),
        "target_commit": target_id,
        "checked_python_files": checked,
        "finding_count": len(findings),
        "findings": findings,
        "valid": not findings,
        "boundary": "Bounded exact-delta static pattern review only; not exhaustive security assurance.",
    }


def path_audit_payload(repo: Path, source: str, target: str) -> dict[str, Any]:
    source_id = resolve_commit(repo, source)
    target_id = resolve_commit(repo, target)
    result = audit_paths(row["path"] for row in delta_rows(repo, source_id, target_id))
    return {
        "schema": f"{SCHEMA}.path-audit",
        "source_commit": source_id,
        "target_commit": target_id,
        **result,
    }


def route_payload(
    roster_path: Path,
    auth_path: Path,
    expected_current_owner: str,
    expected_next_owner: str,
) -> dict[str, Any]:
    if not expected_current_owner.strip() or not expected_next_owner.strip():
        raise DeltaError("expected current and next owners must be explicit")
    roster = strict_json_loads(roster_path.read_bytes(), roster_path.name)
    auth = strict_json_loads(auth_path.read_bytes(), auth_path.name)
    execution = roster.get("validation_scope", {}).get("execution_authority", {})
    auth_execution = auth.get("validation_scope", {}).get("execution_authority", {})
    active = roster.get("active_main_tasks", [])
    repeat = roster.get("live_route_override", {}).get("repeat_cycle", [])
    current = roster.get("current_route", {})
    issues: list[str] = []
    if active != repeat or len(active) != 15:
        issues.append("active and repeat cycle must contain the same fifteen main tasks")
    if roster.get("standby_members", [{}])[0].get("relational_name") != "Tavian Sol":
        issues.append("Tavian Sol standby record missing")
    if execution.get("policy") != "owner_self_scoped_delta" or execution != auth_execution:
        issues.append("roster and authorization validation policies differ")
    if current.get("current", {}).get("owner") != expected_current_owner:
        issues.append(f"current owner is not {expected_current_owner}")
    if current.get("next", {}).get("owner") != expected_next_owner:
        issues.append(f"next owner is not {expected_next_owner}")
    return {
        "schema": f"{SCHEMA}.route",
        "active_main_task_count": len(active),
        "standby": [row.get("relational_name") for row in roster.get("standby_members", [])],
        "current_owner": current.get("current", {}).get("owner"),
        "next_owner": current.get("next", {}).get("owner"),
        "expected_current_owner": expected_current_owner,
        "expected_next_owner": expected_next_owner,
        "validation_policy": execution.get("policy"),
        "issue_count": len(issues),
        "issues": issues,
        "valid": not issues,
    }


def parse_label_path(values: Iterable[str]) -> list[tuple[str, Path]]:
    pairs: list[tuple[str, Path]] = []
    labels: list[str] = []
    for value in values:
        if "=" not in value:
            raise DeltaError("skill mapping must be LABEL=PATH")
        label, raw_path = value.split("=", 1)
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", label):
            raise DeltaError(f"invalid sanitized skill label: {label}")
        path = Path(raw_path)
        if not path.is_file():
            raise DeltaError(f"skill file missing for {label}")
        labels.append(label)
        pairs.append((label, path))
    ensure_unique(labels, "skill label")
    return pairs


def skill_hash_payload(values: Iterable[str]) -> dict[str, Any]:
    records = []
    for label, path in parse_label_path(values):
        raw = path.read_bytes()
        records.append({"label": label, "bytes": len(raw), "sha256": sha256_bytes(raw)})
    return {
        "schema": f"{SCHEMA}.skill-hashes",
        "skill_count": len(records),
        "records": records,
        "paths_sanitized": True,
        "valid": True,
    }


def materialized_paths(repo: Path) -> list[str]:
    paths: list[str] = []
    for root, dirs, files in os.walk(repo):
        dirs[:] = [directory for directory in dirs if directory != ".git" and directory != "__pycache__"]
        root_path = Path(root)
        for filename in files:
            candidate = root_path / filename
            paths.append(candidate.relative_to(repo).as_posix())
    return sorted(paths)


def file_budget_payload(repo: Path, source: str, target: str, threshold: int) -> dict[str, Any]:
    if threshold != 2000:
        raise DeltaError("live materialized-file threshold must be exactly 2000")
    materialized = materialized_paths(repo)
    delta = exact_paths(repo, source, target)
    return {
        "schema": f"{SCHEMA}.file-budget",
        "source_commit": resolve_commit(repo, source),
        "target_commit": resolve_commit(repo, target),
        "materialized_file_count": len(materialized),
        "owner_delta_file_count": len(delta),
        "threshold": threshold,
        "rotation_required": len(materialized) >= threshold or len(delta) >= threshold,
        "sparse_before_checkout_required": True,
        "new_remote_repository": "pending_exact_action",
        "valid": len(materialized) < threshold and len(delta) < threshold,
    }


def sparse_payload(
    repo: Path,
    source: str,
    target: str,
    threshold: int,
    expected_patterns: Iterable[str],
) -> dict[str, Any]:
    expected = ensure_unique((value.strip() for value in expected_patterns), "sparse pattern")
    if not expected or any(not value for value in expected):
        raise DeltaError("at least one non-empty sparse pattern is required")
    observed = [
        line.strip()
        for line in run_git(repo, "sparse-checkout", "list").stdout.splitlines()
        if line.strip()
    ]
    budget = file_budget_payload(repo, source, target, threshold)
    issues: list[str] = []
    if observed != expected:
        issues.append("observed sparse patterns differ from the explicit expected order")
    if not budget["valid"]:
        issues.append("materialized or owner-delta file count reached the rotation threshold")
    return {
        "schema": f"{SCHEMA}.sparse",
        "source_commit": budget["source_commit"],
        "target_commit": budget["target_commit"],
        "expected_patterns": expected,
        "observed_patterns": observed,
        "patterns_match": observed == expected,
        "materialized_file_count": budget["materialized_file_count"],
        "owner_delta_file_count": budget["owner_delta_file_count"],
        "threshold": threshold,
        "rotation_required": budget["rotation_required"],
        "issue_count": len(issues),
        "issues": issues,
        "valid": not issues,
        "boundary": "Current owner worktree only; no sibling-lane inventory and no separate-remote authorization.",
    }


def baton_integrity_payload(
    repo: Path,
    source: str,
    target: str,
    path: str,
    expected_sha256: str,
    minimum_words: int,
    maximum_words: int,
) -> dict[str, Any]:
    source_id = resolve_commit(repo, source)
    target_id = resolve_commit(repo, target)
    normalized = normalize_relative(path)
    if normalized not in exact_paths(repo, source_id, target_id):
        raise DeltaError("baton path is not present in the exact owner delta")
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        raise DeltaError("expected baton SHA-256 must be a lowercase 64-hex digest")
    if minimum_words < 1 or maximum_words < minimum_words:
        raise DeltaError("invalid baton word range")
    entry = tree_entry(repo, target_id, normalized)
    if entry is None or entry["object_type"] != "blob" or entry["mode"] not in ALLOWED_BLOB_MODES:
        raise DeltaError("baton must be a regular committed Git blob")
    raw = blob_object(repo, entry["object_id"])
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise DeltaError("baton is not UTF-8") from exc
    observed_sha256 = sha256_bytes(raw)
    word_count = len(re.findall(r"\S+", text, flags=re.UNICODE))
    issues: list[str] = []
    if observed_sha256 != expected_sha256:
        issues.append("baton SHA-256 differs from the expected digest")
    if not minimum_words <= word_count <= maximum_words:
        issues.append("baton word count is outside the declared range")
    return {
        "schema": f"{SCHEMA}.baton-integrity",
        "source_commit": source_id,
        "target_commit": target_id,
        "repository_relative_path": normalized,
        "git_blob": entry["object_id"],
        "bytes": len(raw),
        "sha256": observed_sha256,
        "expected_sha256": expected_sha256,
        "word_count": word_count,
        "minimum_words": minimum_words,
        "maximum_words": maximum_words,
        "issue_count": len(issues),
        "issues": issues,
        "valid": not issues,
        "boundary": "Committed file integrity only; not delivery acknowledgement, authorship, authority, or independent reproduction.",
    }


def canonical_digest_payload(path: Path) -> dict[str, Any]:
    parsed = strict_json_loads(path.read_bytes(), path.name)
    return {
        "schema": f"{SCHEMA}.canonical-digest",
        "label": path.name,
        "canonical_sha256": canonical_json_sha256(parsed),
        "valid": True,
        "boundary": "Deterministic payload digest only; not a digital signature or trust anchor.",
    }


def collect_outcomes(value: Any, counts: Counter[str], unknown: set[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"outcome", "intended_outcome", "planning_state"} and isinstance(child, str):
                if child in ALLOWED_OUTCOMES:
                    counts[child] += 1
                else:
                    unknown.add(child)
            else:
                collect_outcomes(child, counts, unknown)
    elif isinstance(value, list):
        for child in value:
            collect_outcomes(child, counts, unknown)


def data_quality_payload(paths: Iterable[Path]) -> dict[str, Any]:
    files = list(paths)
    if not files:
        raise DeltaError("at least one ledger is required")
    counts: Counter[str] = Counter()
    unknown: set[str] = set()
    records = []
    for path in files:
        parsed = strict_json_loads(path.read_bytes(), path.name)
        local_counts: Counter[str] = Counter()
        local_unknown: set[str] = set()
        collect_outcomes(parsed, local_counts, local_unknown)
        counts.update(local_counts)
        unknown.update(local_unknown)
        records.append(
            {
                "label": path.name,
                "sha256": sha256_bytes(path.read_bytes()),
                "outcome_counts": dict(sorted(local_counts.items())),
                "unknown_labels": sorted(local_unknown),
            }
        )
    return {
        "schema": f"{SCHEMA}.data-quality",
        "ledger_count": len(files),
        "records": records,
        "outcome_counts": dict(sorted(counts.items())),
        "allowed_outcomes": sorted(ALLOWED_OUTCOMES),
        "unknown_labels": sorted(unknown),
        "valid": not unknown,
        "boundary": "Structured ledger quality only; not evidence promotion.",
    }


def normalized_test_output(text: str) -> str:
    normalized = text.replace("\r\n", "\n")
    normalized = re.sub(r"Ran (\d+) tests? in [0-9.]+s", r"Ran \1 tests in <elapsed>", normalized)
    normalized = re.sub(r"(?i)[A-Z]:\\[^\n\r]+?\\Temp\\tmp[^\\\s:]+", "<temp>", normalized)
    normalized = re.sub(r"/(?:tmp|var/folders)/[^\s:]+", "<temp>", normalized)
    return normalized


def python_imports(path: Path) -> list[str]:
    try:
        tree = parse_python_ast(path.read_text(encoding="utf-8"), filename=str(path))
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise DeltaError(f"unable to inspect imports for {path.name}: {exc}") from exc
    imports: set[str] = set()
    for node in getattr(tree, "body", []):
        if node.__class__.__name__ == "Import":
            imports.update(alias.name for alias in node.names)
        elif node.__class__.__name__ == "ImportFrom" and node.module:
            imports.add(node.module)
    return sorted(imports)


def declared_repository_dependencies(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError, UnicodeError) as exc:
        raise DeltaError(f"unable to parse test dependency declaration: {path.name}") from exc
    declaration: Any = None
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(
            isinstance(target, ast.Name)
            and target.id == "DECLARED_REPOSITORY_DEPENDENCIES"
            for target in node.targets
        ):
            try:
                declaration = ast.literal_eval(node.value)
            except (ValueError, TypeError, SyntaxError) as exc:
                raise DeltaError("test dependency declaration must be a literal sequence") from exc
    if declaration is None:
        raise DeltaError(
            f"test module lacks DECLARED_REPOSITORY_DEPENDENCIES: {path.name}"
        )
    if not isinstance(declaration, (list, tuple)) or not all(
        isinstance(value, str) for value in declaration
    ):
        raise DeltaError("test dependency declaration must contain only paths")
    return ensure_unique(
        (normalize_relative(value) for value in declaration),
        f"declared repository dependency in {path.name}",
    )


def run_exact_tests(
    repo: Path,
    modules: Iterable[str],
    dependencies: Iterable[str] = (),
) -> dict[str, Any]:
    normalized = ensure_unique((normalize_relative(value) for value in modules), "test module")
    dependency_paths = ensure_unique(
        (normalize_relative(value) for value in dependencies), "test dependency"
    )
    dependency_records: list[dict[str, Any]] = []
    for dependency in dependency_paths:
        path = repo / Path(dependency)
        if not path.is_file():
            raise DeltaError(f"materialized test dependency missing: {dependency}")
        raw = path.read_bytes()
        dependency_records.append(
            {"path": dependency, "bytes": len(raw), "sha256": sha256_bytes(raw)}
        )
    records = []
    for module in normalized:
        module_path = PurePosixPath(module)
        if (
            not module.endswith(".py")
            or len(module_path.parts) < 2
            or module_path.parts[0] != "tests"
            or not module_path.name.startswith("test_")
        ):
            raise DeltaError(f"test module must be a tests/test_*.py file: {module}")
        path = repo / Path(module)
        if not path.is_file():
            raise DeltaError(f"materialized test module missing: {module}")
        declared_dependencies = declared_repository_dependencies(path)
        if declared_dependencies != dependency_paths:
            raise DeltaError(
                f"test dependency closure differs for {module}: "
                f"{declared_dependencies} != {dependency_paths}"
            )
        result = subprocess.run(
            [sys.executable, str(path)],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        stable_output = normalized_test_output(result.stdout)
        records.append(
            {
                "module": module,
                "returncode": result.returncode,
                "module_sha256": sha256_bytes(path.read_bytes()),
                "declared_imports": python_imports(path),
                "declared_repository_dependencies": declared_dependencies,
                "normalized_output_sha256": sha256_bytes(stable_output.encode("utf-8")),
                "output_tail": result.stdout.splitlines()[-8:],
            }
        )
        if result.returncode:
            raise DeltaError(f"selected test module failed: {module}")
    stable_contract = {
        "modules": [record["module"] for record in records],
        "dependencies": dependency_records,
        "results": [
            {
                "module": record["module"],
                "returncode": record["returncode"],
                "module_sha256": record["module_sha256"],
                "normalized_output_sha256": record["normalized_output_sha256"],
            }
            for record in records
        ],
    }
    return {
        "module_count": len(records),
        "dependency_count": len(dependency_records),
        "dependencies": dependency_records,
        "records": records,
        "contract_sha256": canonical_json_sha256(stable_contract),
        "valid": True,
    }


def validate_remote_name(repo: Path, remote: str) -> str:
    if not REMOTE_NAME.fullmatch(remote):
        raise DeltaError(f"invalid configured remote name rejected: {remote}")
    run_git(repo, "remote", "get-url", "--", remote)
    return remote


def validate_branch_name(repo: Path, branch: str) -> str:
    if not branch or branch.startswith("-"):
        raise DeltaError(f"option-like or empty branch name rejected: {branch}")
    result = run_git(repo, "check-ref-format", "--branch", branch, check=False)
    if result.returncode:
        raise DeltaError(f"invalid branch name rejected: {branch}")
    return branch


def clean_and_equal_payload(repo: Path, target: str, branch: str, remote: str) -> dict[str, Any]:
    branch = validate_branch_name(repo, branch)
    remote = validate_remote_name(repo, remote)
    target_id = resolve_commit(repo, target)
    head = resolve_commit(repo, "HEAD")
    current_branch = run_git(repo, "branch", "--show-current").stdout.strip()
    unstaged = run_git(repo, "diff", "--quiet", check=False).returncode
    staged = run_git(repo, "diff", "--cached", "--quiet", check=False).returncode
    untracked = [line for line in run_git(repo, "ls-files", "--others", "--exclude-standard").stdout.splitlines() if line]
    upstream = resolve_commit(repo, "@{u}")
    tracking = resolve_commit(repo, f"refs/remotes/{remote}/{branch}")
    live_result = run_git(repo, "ls-remote", "--heads", "--end-of-options", remote, f"refs/heads/{branch}")
    live_fields = live_result.stdout.strip().split()
    live = live_fields[0] if live_fields else None
    issues = []
    if head != target_id:
        issues.append("HEAD differs from target")
    if current_branch != branch:
        issues.append("current branch differs from expected branch")
    if unstaged or staged or untracked:
        issues.append("worktree is not clean")
    if len({target_id, head, upstream, tracking, live}) != 1:
        issues.append("local, upstream, tracking, and fresh-live commits differ")
    return {
        "target": target_id,
        "head": head,
        "branch_matches": current_branch == branch,
        "unstaged_changes": bool(unstaged),
        "staged_changes": bool(staged),
        "untracked_count": len(untracked),
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "four_way_equal": len({target_id, head, upstream, tracking, live}) == 1,
        "issues": issues,
        "valid": not issues,
    }


def canonical_payload(args: argparse.Namespace) -> dict[str, Any]:
    repo = args.repo.resolve()
    owner = canonical_owner(args.owner)
    if args.commit_limit != 8:
        raise DeltaError("live phase commit limit must be exactly 8")
    source = resolve_commit(repo, args.source)
    target = resolve_commit(repo, args.target)
    ancestry = run_git(repo, "rev-list", "--parents", f"{source}..{target}").stdout.splitlines()
    merge_count = sum(len(line.split()) > 2 for line in ancestry)
    if merge_count:
        raise DeltaError("merge commit detected in owner delta")
    if len(ancestry) > args.commit_limit:
        raise DeltaError("owner delta exceeds the declared commit limit")
    if any(len(line.split()) != 2 for line in ancestry):
        raise DeltaError("owner delta contains a non-single-parent commit")
    x1 = resolve_commit(repo, args.x1)
    x1_parents = run_git(repo, "rev-list", "--parents", "-n", "1", x1).stdout.split()
    if len(x1_parents) != 2 or x1_parents[1] != source:
        raise DeltaError("x1 is not the direct child of source")
    manifest = manifest_payload(repo, source, target)
    json_check = json_payload(repo, source, target)
    markdown_check = markdown_payload(repo, source, target)
    python_check = python_payload(repo, source, target)
    privacy = privacy_payload(repo, source, target)
    security = security_payload(repo, source, target)
    path_audit = path_audit_payload(repo, source, target)
    file_budget = file_budget_payload(repo, source, target, args.threshold)
    sparse = sparse_payload(repo, source, target, args.threshold, args.sparse_pattern)
    route = route_payload(
        args.roster,
        args.auth,
        args.expected_current_owner,
        args.expected_next_owner,
    )
    skills = skill_hash_payload(args.skill)
    quality = data_quality_payload(args.ledger)
    tests = run_exact_tests(repo, args.test_module, args.test_dependency)
    baton = baton_integrity_payload(
        repo,
        source,
        target,
        args.baton_path,
        args.baton_sha256,
        args.baton_min_words,
        args.baton_max_words,
    )
    git_gate = clean_and_equal_payload(repo, target, args.branch, args.remote)
    valid = all(
        part.get("valid", False)
        for part in (
            manifest,
            json_check,
            markdown_check,
            python_check,
            privacy,
            security,
            path_audit,
            file_budget,
            sparse,
            route,
            skills,
            quality,
            tests,
            baton,
            git_gate,
        )
    )
    payload = {
        "schema": f"{SCHEMA}.canonical",
        "invoked_at_utc": utc_now(),
        "invocation_count": 1,
        "successful_invocation_count": 1 if valid else 0,
        "post_success_replay": False,
        "execution_authority": "owner_self_scoped_delta",
        "owner": owner,
        "source_commit": source,
        "x1_commit": x1,
        "target_commit": target,
        "commit_count": len(ancestry),
        "commit_limit": args.commit_limit,
        "merge_count": merge_count,
        "single_parent_history": True,
        "manifest": manifest,
        "json": json_check,
        "markdown": markdown_check,
        "python": python_check,
        "privacy": privacy,
        "security": security,
        "path_audit": path_audit,
        "file_budget": file_budget,
        "sparse": sparse,
        "route": route,
        "skills": skills,
        "data_quality": quality,
        "tests": tests,
        "baton": baton,
        "git_gate": git_gate,
        "valid": valid,
        "verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "One same-owner exact-delta software validation pass only; not a full-repository suite, independent reproduction, empirical or professional evidence, authority, personhood evidence, Theory-of-Everything proof, or Stage 20 authority.",
    }
    payload["canonical_payload_sha256"] = canonical_json_sha256(
        {key: value for key, value in payload.items() if key not in {"invoked_at_utc"}}
    )
    write_json_exclusive(args.receipt, payload)
    return payload


def add_range(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--output", type=Path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("manifest", "json", "markdown", "python", "privacy", "security", "path-audit"):
        add_range(commands.add_parser(name))
    route = commands.add_parser("route")
    route.add_argument("--roster", type=Path, required=True)
    route.add_argument("--auth", type=Path, required=True)
    route.add_argument("--expected-current-owner", required=True)
    route.add_argument("--expected-next-owner", required=True)
    route.add_argument("--output", type=Path)
    skills = commands.add_parser("skill-hashes")
    skills.add_argument("--skill", action="append", required=True)
    skills.add_argument("--output", type=Path)
    budget = commands.add_parser("file-budget")
    add_range(budget)
    budget.add_argument("--threshold", type=int, default=2000)
    sparse = commands.add_parser("sparse")
    add_range(sparse)
    sparse.add_argument("--threshold", type=int, default=2000)
    sparse.add_argument("--expected-pattern", action="append", required=True)
    baton = commands.add_parser("baton-integrity")
    add_range(baton)
    baton.add_argument("--path", required=True)
    baton.add_argument("--expected-sha256", required=True)
    baton.add_argument("--minimum-words", type=int, default=10000)
    baton.add_argument("--maximum-words", type=int, default=100000)
    digest = commands.add_parser("canonical-digest")
    digest.add_argument("--json", type=Path, required=True)
    digest.add_argument("--output", type=Path)
    quality = commands.add_parser("data-quality")
    quality.add_argument("--ledger", type=Path, action="append", required=True)
    quality.add_argument("--output", type=Path)
    hardening = commands.add_parser("hardening")
    hardening.add_argument("--profile", default="ilyra-v662-v6")
    hardening.add_argument("--output", type=Path)
    canonical = commands.add_parser("canonical")
    canonical.add_argument("--repo", type=Path, required=True)
    canonical.add_argument("--owner", required=True)
    canonical.add_argument("--source", required=True)
    canonical.add_argument("--x1", required=True)
    canonical.add_argument("--target", required=True)
    canonical.add_argument("--branch", required=True)
    canonical.add_argument("--remote", default="origin")
    canonical.add_argument("--threshold", type=int, default=2000)
    canonical.add_argument("--commit-limit", type=int, default=8)
    canonical.add_argument("--roster", type=Path, required=True)
    canonical.add_argument("--auth", type=Path, required=True)
    canonical.add_argument("--expected-current-owner", required=True)
    canonical.add_argument("--expected-next-owner", required=True)
    canonical.add_argument("--skill", action="append", required=True)
    canonical.add_argument("--ledger", type=Path, action="append", required=True)
    canonical.add_argument("--test-module", action="append", required=True)
    canonical.add_argument("--test-dependency", action="append", default=[])
    canonical.add_argument("--sparse-pattern", action="append", required=True)
    canonical.add_argument("--baton-path", required=True)
    canonical.add_argument("--baton-sha256", required=True)
    canonical.add_argument("--baton-min-words", type=int, default=10000)
    canonical.add_argument("--baton-max-words", type=int, default=100000)
    canonical.add_argument("--receipt", type=Path, required=True)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "manifest":
            payload = manifest_payload(args.repo, args.source, args.target)
        elif args.command == "json":
            payload = json_payload(args.repo, args.source, args.target)
        elif args.command == "markdown":
            payload = markdown_payload(args.repo, args.source, args.target)
        elif args.command == "python":
            payload = python_payload(args.repo, args.source, args.target)
        elif args.command == "privacy":
            payload = privacy_payload(args.repo, args.source, args.target)
        elif args.command == "security":
            payload = security_payload(args.repo, args.source, args.target)
        elif args.command == "path-audit":
            payload = path_audit_payload(args.repo, args.source, args.target)
        elif args.command == "route":
            payload = route_payload(
                args.roster,
                args.auth,
                args.expected_current_owner,
                args.expected_next_owner,
            )
        elif args.command == "skill-hashes":
            payload = skill_hash_payload(args.skill)
        elif args.command == "file-budget":
            payload = file_budget_payload(args.repo, args.source, args.target, args.threshold)
        elif args.command == "sparse":
            payload = sparse_payload(
                args.repo,
                args.source,
                args.target,
                args.threshold,
                args.expected_pattern,
            )
        elif args.command == "baton-integrity":
            payload = baton_integrity_payload(
                args.repo,
                args.source,
                args.target,
                args.path,
                args.expected_sha256,
                args.minimum_words,
                args.maximum_words,
            )
        elif args.command == "canonical-digest":
            payload = canonical_digest_payload(args.json)
        elif args.command == "data-quality":
            payload = data_quality_payload(args.ledger)
        elif args.command == "hardening":
            payload = hardening_payload_for_profile(args.profile)
        elif args.command == "canonical":
            payload = canonical_payload(args)
            sys.stdout.write(json.dumps({"valid": payload["valid"], "target": payload["target_commit"]}) + "\n")
            return 0 if payload["valid"] else 2
        else:
            raise DeltaError(f"unsupported command: {args.command}")
        write_json(getattr(args, "output", None), payload)
        return 0 if payload.get("valid", True) else 2
    except (DeltaError, OSError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"OWNER_DELTA_TOOLKIT_ERROR: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
