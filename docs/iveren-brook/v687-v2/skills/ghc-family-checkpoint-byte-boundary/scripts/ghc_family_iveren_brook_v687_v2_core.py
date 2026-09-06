"""Bounded synthetic evidence interchange. No route, authority, or deployment effects."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import math
from pathlib import Path
import re
import unicodedata

import cbor2
import jsonlines
import msgpack

MAX_INPUT_BYTES = 65536
MAX_DEPTH = 16
MAX_NODES = 4096


class Refusal(ValueError):
    """A stable contract refusal, independent of library exception wording."""


def shape(value, keys):
    return type(value) is dict and set(value) == set(keys)


def utf8(value):
    try:
        return value.encode("utf-8", errors="strict")
    except UnicodeError as exc:
        raise Refusal("INVALID_UTF8") from exc


def pairs_unique(items):
    result = {}
    for key, value in items:
        if key in result:
            raise Refusal("DUPLICATE_KEY")
        result[key] = value
    return result


def reject_constant(value):
    raise Refusal("NONFINITE")


def finite_tree(value, *, profile=False):
    remaining = MAX_NODES

    def walk(node, depth):
        nonlocal remaining
        remaining -= 1
        if depth > MAX_DEPTH or remaining < 0:
            raise Refusal("VALUE_PROFILE" if profile else "RESOURCE_BOUND")
        kind = type(node)
        if kind is float:
            if not math.isfinite(node):
                raise Refusal("NONFINITE")
        elif kind is int:
            if profile and not -(2**63) <= node < 2**64:
                raise Refusal("VALUE_PROFILE")
        elif kind is str:
            if profile:
                if len(utf8(node)) > MAX_INPUT_BYTES:
                    raise Refusal("VALUE_PROFILE")
        elif kind is list:
            for child in node:
                walk(child, depth + 1)
        elif kind is dict:
            for key, child in node.items():
                if type(key) is not str:
                    raise Refusal("VALUE_PROFILE")
                if profile:
                    utf8(key)
                walk(child, depth + 1)
        elif node is not None and kind is not bool:
            raise Refusal("VALUE_PROFILE")

    walk(value, 0)


def strict_json(text):
    try:
        value = json.loads(
            text, object_pairs_hook=pairs_unique, parse_constant=reject_constant
        )
    except Refusal:
        raise
    except (ValueError, TypeError, RecursionError) as exc:
        raise Refusal("INVALID_JSON") from exc
    finite_tree(value)
    return value


def ordered(value):
    if type(value) is dict:
        return {key: ordered(value[key]) for key in sorted(value)}
    if type(value) is list:
        return [ordered(item) for item in value]
    return value


def cbor_profile(request):
    if not shape(request, ["value"]):
        raise Refusal("INVALID_SHAPE")
    finite_tree(request["value"], profile=True)
    return {"hex": cbor2.dumps(request["value"], canonical=True).hex()}


def msgpack_profile(request):
    if not shape(request, ["value"]):
        raise Refusal("INVALID_SHAPE")
    finite_tree(request["value"], profile=True)
    return {
        "hex": msgpack.packb(
            ordered(request["value"]), use_bin_type=True, strict_types=True
        ).hex()
    }


def jsonl_frames(request):
    if not shape(request, ["text"]) or type(request["text"]) is not str:
        raise Refusal("INVALID_SHAPE")
    text = request["text"]
    if not text:
        return {"records": [], "record_count": 0}
    lines = text.split("\n")
    if lines[-1] == "":
        lines.pop()
    records = []
    for number, line in enumerate(lines, 1):
        try:
            if not line.strip() or line.startswith("\ufeff"):
                raise Refusal("INVALID_JSON")
            with jsonlines.Reader(io.StringIO(line), loads=strict_json) as reader:
                value = reader.read(allow_none=True, skip_empty=False)
            records.append(value)
        except (Refusal, jsonlines.Error, EOFError, UnicodeError):
            return {"error": "INVALID_LINE", "line": number}
    return {"records": records, "record_count": len(records)}


def json_unique(request):
    if not shape(request, ["text"]) or type(request["text"]) is not str:
        raise Refusal("INVALID_SHAPE")
    return {"value": strict_json(request["text"])}


def unicode_bytes(request):
    if not shape(request, ["text", "form"]) or type(request["text"]) is not str:
        raise Refusal("INVALID_SHAPE")
    if request["form"] not in ("NFC", "NFD", "NFKC", "NFKD"):
        raise Refusal("INVALID_FORM")
    original = utf8(request["text"])
    normalized = utf8(unicodedata.normalize(request["form"], request["text"]))
    return {
        "original_hex": original.hex(),
        "normalized_hex": normalized.hex(),
        "changed": original != normalized,
        "identity_equivalence": False,
    }


def digest_envelope(request):
    if not shape(request, ["text", "sha256", "domain"]) or type(request["text"]) is not str:
        raise Refusal("INVALID_SHAPE")
    if request["domain"] != "utf8":
        raise Refusal("INVALID_DOMAIN")
    claimed = request["sha256"]
    if type(claimed) is not str or not re.fullmatch("[0-9a-f]{64}", claimed):
        raise Refusal("INVALID_DIGEST")
    payload = utf8(request["text"])
    return {
        "match": hashlib.sha256(payload).hexdigest() == claimed,
        "byte_length": len(payload),
        "authority": False,
    }


def receipt_join(request):
    binding = ("owner", "phase", "head", "scope")
    if not shape(request, ["claim", "receipt"]):
        raise Refusal("INVALID_JOIN")
    claim, receipt = request["claim"], request["receipt"]
    if not shape(claim, binding) or not shape(receipt, (*binding, "passed", "evidence_class")):
        raise Refusal("INVALID_JOIN")
    if any(type(obj[key]) is not str or not obj[key] for obj in (claim, receipt) for key in binding):
        raise Refusal("INVALID_JOIN")
    if type(receipt["passed"]) is not bool or type(receipt["evidence_class"]) is not str or not receipt["evidence_class"]:
        raise Refusal("INVALID_JOIN")
    reasons = [key for key in binding if claim[key] != receipt[key]]
    if not receipt["passed"]:
        reasons.append("passed")
    if receipt["evidence_class"] != "synthetic":
        reasons.append("evidence_class")
    return {
        "matched": not reasons,
        "outcome": "open_gap" if reasons else "completed",
        "reasons": reasons,
        "external_credit": False,
    }


def event_prefix(request):
    if not shape(request, ["events"]) or type(request["events"]) is not list:
        raise Refusal("INVALID_SHAPE")
    transitions = {
        ("EMPTY", "prepared"): "PREPARED",
        ("PREPARED", "validated"): "VALIDATED",
        ("VALIDATED", "sent"): "SENT_ONCE",
        ("VALIDATED", "unavailable"): "UNAVAILABLE_NO_RESEND",
        ("SENT_ONCE", "acknowledged"): "ACKNOWLEDGED",
        ("SENT_ONCE", "opaque"): "OPAQUE_NO_RESEND",
        ("SENT_ONCE", "rejected"): "REJECTED_NO_RESEND",
    }
    state, sends = "EMPTY", 0
    for index, event in enumerate(request["events"], 1):
        if not shape(event, ["seq", "kind"]) or type(event["kind"]) is not str:
            return {"error": "INVALID_EVENT", "index": index}
        if type(event["seq"]) is not int or event["seq"] != index:
            return {"error": "INVALID_SEQUENCE", "index": index}
        target = transitions.get((state, event["kind"]))
        if target is None:
            return {"error": "INVALID_TRANSITION", "index": index}
        state = target
        sends += event["kind"] == "sent"
    return {"state": state, "send_count": sends, "resend_allowed": False}


def checkpoint(request):
    if not shape(request, ["text", "offset"]) or type(request["text"]) is not str:
        raise Refusal("INVALID_SHAPE")
    data, offset = utf8(request["text"]), request["offset"]
    if type(offset) is not int or not 0 <= offset <= len(data):
        raise Refusal("INVALID_OFFSET")
    if offset and data[offset - 1] != 10:
        raise Refusal("NOT_RECORD_BOUNDARY")
    prefix = data[:offset].decode("utf-8")
    result = jsonl_frames({"text": prefix})
    if "error" in result:
        raise Refusal("INVALID_PREFIX")
    return {
        "valid": True,
        "committed_records": result["record_count"],
        "pending_bytes": len(data) - offset,
    }


def artifact_budget(request):
    if not shape(request, ["files", "bytes", "file_limit", "byte_limit"]):
        raise Refusal("INVALID_BUDGET")
    if any(type(value) is not int for value in request.values()):
        raise Refusal("INVALID_BUDGET")
    files, size, limit, capacity = (request[key] for key in ("files", "bytes", "file_limit", "byte_limit"))
    if min(files, size) < 0 or not 1 <= limit <= 2000 or capacity < 1:
        raise Refusal("INVALID_BUDGET")
    decision = (
        "exceeded" if files > limit or size > capacity
        else "at_limit" if files == limit or size == capacity
        else "within"
    )
    return {
        "decision": decision,
        "remaining_files": max(0, limit - files),
        "remaining_bytes": max(0, capacity - size),
        "rotation_required": files >= limit,
    }


OPERATIONS = {
    "cbor_profile": cbor_profile,
    "msgpack_profile": msgpack_profile,
    "jsonl_frames": jsonl_frames,
    "json_unique": json_unique,
    "unicode_bytes": unicode_bytes,
    "digest_envelope": digest_envelope,
    "receipt_join": receipt_join,
    "event_prefix": event_prefix,
    "checkpoint": checkpoint,
    "artifact_budget": artifact_budget,
}


def dispatch(operation, request):
    if operation not in OPERATIONS:
        return {"error": "UNKNOWN_OPERATION"}
    try:
        # This is a software resource guard, not a measured machine capacity claim.
        if len(json.dumps(request, ensure_ascii=True, allow_nan=False)) > MAX_INPUT_BYTES:
            raise Refusal("INPUT_BOUND")
        return OPERATIONS[operation](request)
    except Refusal as exc:
        return {"error": str(exc)}
    except (TypeError, ValueError, OverflowError, RecursionError):
        return {"error": "INVALID_INPUT"}


def cli(allowed):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--operation", required=True, choices=allowed)
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()
    with args.input.open("rb") as stream:
        data = stream.read(MAX_INPUT_BYTES + 1)
    if len(data) > MAX_INPUT_BYTES:
        result = {"error": "INPUT_BOUND"}
    else:
        try:
            request = strict_json(data.decode("utf-8"))
            result = dispatch(args.operation, request)
        except (Refusal, UnicodeError) as exc:
            result = {"error": str(exc) if isinstance(exc, Refusal) else "INVALID_UTF8"}
    print(json.dumps(result, ensure_ascii=True, sort_keys=True, allow_nan=False))
