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


def hardening_payload_for_profile(profile: str) -> dict[str, Any]:
    """Select one exact bounded fixture family; reject implicit substitution."""

    if profile == "ilyra-v662-v6":
        return hardening_payload()
    if profile == "auren-v662-v7":
        return auren_hardening_payload()
    if profile == "sable-v662-v8":
        return sable_hardening_payload()
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
