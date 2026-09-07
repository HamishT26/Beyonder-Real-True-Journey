"""Strict synthetic font-outline and glyph-metadata evaluator.

This module accepts only the twenty frozen Tamar v688-v3 operation profiles.
It does not open real fonts, render glyphs, shape real text, fetch external
references, or make professional, accessibility, rights, legal, cultural, or
authority decisions.
"""
from __future__ import annotations

import copy
import json
import re
from fractions import Fraction


class ContractError(ValueError):
    """A bounded refusal with a stable public error label."""


def ok(value):
    return {"accepted": True, "error": None, "external_credit": False, "value": value}


def bad(error):
    return {"accepted": False, "error": error, "external_credit": False, "value": None}


def _pairs(sequence):
    result = {}
    for key, value in sequence:
        if key in result:
            raise ContractError("DUPLICATE_KEY")
        result[key] = value
    return result


def _strict_loads(raw):
    try:
        return json.loads(
            raw,
            object_pairs_hook=_pairs,
            parse_constant=lambda value: (_ for _ in ()).throw(ContractError("NONFINITE")),
        )
    except ContractError:
        raise
    except (TypeError, UnicodeError, json.JSONDecodeError) as exc:
        raise ContractError("JSON_SYNTAX") from exc


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def _fields(payload, required):
    if set(payload) != {"operation", *required}:
        raise ContractError("FIELD_SET")


def _text(value):
    if type(value) is not str:
        raise ContractError("TEXT_TYPE")
    return value


def _integer(value):
    if type(value) is not int:
        raise ContractError("INTEGER_TYPE")
    return value


NUMBER = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")


def _fraction(value):
    text = _text(value)
    if not NUMBER.fullmatch(text):
        raise ContractError("NUMBER_SYNTAX")
    match = re.search(r"[eE]([+-]?\d+)$", text)
    if match and abs(int(match.group(1))) > 12:
        raise ContractError("NUMBER_BOUND")
    return Fraction(text)


def _fmt(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _pair(value, integer_only=True):
    if not isinstance(value, list) or len(value) != 2:
        raise ContractError("POINT_SHAPE")
    result = []
    for item in value:
        number = _fraction(item)
        if integer_only and number.denominator != 1:
            raise ContractError("COORDINATE_INTEGER")
        if number < -32768 or number > 32767:
            raise ContractError("COORDINATE_RANGE")
        result.append(number)
    return result


def _tag(value):
    text = _text(value)
    if len(text) != 4:
        raise ContractError("TAG_LENGTH")
    if any(ord(char) < 32 or ord(char) > 126 for char in text):
        raise ContractError("TAG_ASCII")
    return text


def _scalar(value):
    value = _integer(value)
    if value < 0 or value > 0x10FFFF:
        raise ContractError("SCALAR_RANGE")
    if 0xD800 <= value <= 0xDFFF:
        raise ContractError("SURROGATE")
    return value


GLYPH_NAME = re.compile(r"^[A-Za-z_.][A-Za-z0-9_.]*$")


def _glyph_name(value):
    text = _text(value)
    if not GLYPH_NAME.fullmatch(text):
        raise ContractError("GLYPH_NAME")
    return text


def _unicode_scalar(payload):
    _fields(payload, {"token"})
    token = _text(payload["token"])
    if not re.fullmatch(r"U\+[0-9A-Fa-f]{4,6}", token):
        raise ContractError("SCALAR_SYNTAX")
    value = int(token[2:], 16)
    if value > 0x10FFFF:
        raise ContractError("SCALAR_RANGE")
    if 0xD800 <= value <= 0xDFFF:
        raise ContractError("SURROGATE")
    return {"codepoint": value, "hex": f"{value:04X}", "plane": value >> 16, "scalar": True}


def _glyph_name_operation(payload):
    _fields(payload, {"name"})
    name = _glyph_name(payload["name"])
    return {"characters": len(name), "name": name, "reserved_notdef": name == ".notdef"}


def _table_tag(payload):
    _fields(payload, {"tag"})
    tag = _tag(payload["tag"])
    return {"ascii_hex": tag.encode("ascii").hex(), "length": 4, "tag": tag}


def _table_directory(payload):
    _fields(payload, {"records"})
    records = payload["records"]
    if not isinstance(records, list):
        raise ContractError("RECORD_LIST")
    parsed = []
    for record in records:
        if not isinstance(record, dict) or set(record) != {"tag", "offset", "length", "checksum"}:
            raise ContractError("RECORD_SHAPE")
        tag = _tag(record["tag"])
        offset = _integer(record["offset"])
        length = _integer(record["length"])
        checksum = _integer(record["checksum"])
        if any(value < 0 or value > 0xFFFFFFFF for value in [offset, length, checksum]):
            raise ContractError("INTEGER_RANGE")
        parsed.append({"tag": tag, "offset": offset, "length": length, "checksum": checksum})
    tags = [record["tag"] for record in parsed]
    if len(tags) != len(set(tags)):
        raise ContractError("DUPLICATE_TAG")
    if tags != sorted(tags):
        raise ContractError("TAG_ORDER")
    by_offset = sorted(parsed, key=lambda record: (record["offset"], record["length"], record["tag"]))
    for left, right in zip(by_offset, by_offset[1:]):
        if right["offset"] < left["offset"] + left["length"]:
            raise ContractError("TABLE_OVERLAP")
    return {
        "aligned": all(record["offset"] % 4 == 0 for record in parsed),
        "count": len(parsed),
        "nonoverlap": True,
        "tags": tags,
    }


def _segment(payload, degree):
    controls = ["control"] if degree == 2 else ["control1", "control2"]
    _fields(payload, {"start", *controls, "end"})
    names = ["start", *controls, "end"]
    points = {name: _pair(payload[name]) for name in names}
    all_points = list(points.values())
    xs = [point[0] for point in all_points]
    ys = [point[1] for point in all_points]
    result = {name: [_fmt(value) for value in points[name]] for name in names}
    result["degree"] = degree
    result["envelope"] = [_fmt(min(xs)), _fmt(min(ys)), _fmt(max(xs)), _fmt(max(ys))]
    return result


def _glyph_bbox(payload):
    _fields(payload, {"points"})
    points = payload["points"]
    if not isinstance(points, list):
        raise ContractError("POINT_LIST")
    if not points:
        raise ContractError("NO_POINTS")
    parsed = [_pair(point) for point in points]
    xs = [point[0] for point in parsed]
    ys = [point[1] for point in parsed]
    x_min, x_max, y_min, y_max = min(xs), max(xs), min(ys), max(ys)
    return {
        "height": _fmt(y_max - y_min),
        "point_count": len(parsed),
        "width": _fmt(x_max - x_min),
        "x_max": _fmt(x_max),
        "x_min": _fmt(x_min),
        "y_max": _fmt(y_max),
        "y_min": _fmt(y_min),
    }


def _horizontal_metrics(payload):
    _fields(payload, {"advance_width", "lsb", "x_min", "x_max"})
    advance = _integer(payload["advance_width"])
    lsb = _integer(payload["lsb"])
    x_min = _integer(payload["x_min"])
    x_max = _integer(payload["x_max"])
    if advance < 0 or advance > 65535:
        raise ContractError("ADVANCE_RANGE")
    if any(value < -32768 or value > 32767 for value in [lsb, x_min, x_max]):
        raise ContractError("COORDINATE_RANGE")
    if x_min > x_max:
        raise ContractError("BBOX_ORDER")
    return {
        "advance_width": advance,
        "lsb": lsb,
        # Frozen x1 defines this field as a contract-local envelope residual,
        # not the OpenType right-side-bearing formula.  The x2 correction
        # receipt preserves that semantic discrepancy and prohibits
        # conformance or real-font credit.
        "rsb": advance - (x_max - x_min) - max(lsb, 0),
        "x_min_matches_lsb": x_min == lsb,
    }


def _units_per_em(payload):
    _fields(payload, {"value"})
    value = _integer(payload["value"])
    if value < 16 or value > 16384:
        raise ContractError("UPEM_RANGE")
    return {"power_of_two": value & (value - 1) == 0, "reciprocal": f"1/{value}", "units_per_em": value}


def _cmap_record(payload):
    _fields(payload, {"codepoint", "glyph_id", "glyph_count", "existing"})
    codepoint = _scalar(payload["codepoint"])
    glyph_id = _integer(payload["glyph_id"])
    glyph_count = _integer(payload["glyph_count"])
    if glyph_count < 0 or glyph_id < 0 or glyph_id >= glyph_count:
        raise ContractError("GLYPH_RANGE")
    existing = payload["existing"]
    if not isinstance(existing, list):
        raise ContractError("RECORD_LIST")
    mapping = {}
    for record in existing:
        if not isinstance(record, dict) or set(record) != {"codepoint", "glyph_id"}:
            raise ContractError("RECORD_SHAPE")
        old_codepoint = _scalar(record["codepoint"])
        old_glyph = _integer(record["glyph_id"])
        if old_glyph < 0 or old_glyph >= glyph_count:
            raise ContractError("GLYPH_RANGE")
        if old_codepoint in mapping:
            raise ContractError("DUPLICATE_CODEPOINT")
        mapping[old_codepoint] = old_glyph
    if codepoint in mapping and mapping[codepoint] != glyph_id:
        raise ContractError("CMAP_CONFLICT")
    idempotent = mapping.get(codepoint) == glyph_id
    mapping[codepoint] = glyph_id
    return {"codepoint": codepoint, "glyph_id": glyph_id, "idempotent": idempotent, "mapping_count": len(mapping)}


def _variation_axis(payload):
    _fields(payload, {"tag", "minimum", "default", "maximum"})
    tag = _tag(payload["tag"])
    minimum = _fraction(payload["minimum"])
    default = _fraction(payload["default"])
    maximum = _fraction(payload["maximum"])
    if minimum > default or default > maximum or minimum == maximum:
        raise ContractError("AXIS_ORDER")
    return {"default": _fmt(default), "maximum": _fmt(maximum), "minimum": _fmt(minimum), "span": _fmt(maximum - minimum), "tag": tag}


def _axis_coordinate(payload):
    _fields(payload, {"minimum", "default", "maximum", "value"})
    minimum = _fraction(payload["minimum"])
    default = _fraction(payload["default"])
    maximum = _fraction(payload["maximum"])
    value = _fraction(payload["value"])
    if minimum == maximum:
        raise ContractError("AXIS_DEGENERATE")
    if minimum > default or default > maximum:
        raise ContractError("AXIS_ORDER")
    if value < minimum or value > maximum:
        raise ContractError("COORDINATE_RANGE")
    if value == default:
        normalized, zone = Fraction(0), "default"
    elif value < default:
        if default == minimum:
            raise ContractError("AXIS_DEGENERATE")
        normalized, zone = (value - default) / (default - minimum), "lower"
    else:
        if maximum == default:
            raise ContractError("AXIS_DEGENERATE")
        normalized, zone = (value - default) / (maximum - default), "upper"
    return {"normalized": _fmt(normalized), "zone": zone}


def _name_record(payload):
    _fields(payload, {"platform_id", "encoding_id", "language_id", "name_id", "text"})
    values = [
        _integer(payload["platform_id"]),
        _integer(payload["encoding_id"]),
        _integer(payload["language_id"]),
        _integer(payload["name_id"]),
    ]
    if any(value < 0 or value > 65535 for value in values):
        raise ContractError("ID_RANGE")
    text = _text(payload["text"])
    if "\x00" in text:
        raise ContractError("TEXT_CONTROL")
    return {
        "characters": len(text),
        "empty": text == "",
        "key": ":".join(str(value) for value in values),
        "text": text,
    }


def _language_tag_value(value):
    tag = _text(value)
    if not tag or "_" in tag or "--" in tag:
        raise ContractError("LANGUAGE_PROFILE")
    parts = tag.split("-")
    language = parts.pop(0).lower()
    if not re.fullmatch(r"[a-z]{2,3}", language):
        raise ContractError("LANGUAGE_PROFILE")
    script = None
    region = None
    variants = []
    if parts and re.fullmatch(r"[A-Za-z]{4}", parts[0]):
        script = parts.pop(0).title()
    if parts and re.fullmatch(r"(?:[A-Za-z]{2}|\d{3})", parts[0]):
        region = parts.pop(0).upper()
    for part in parts:
        if not re.fullmatch(r"(?:[0-9][A-Za-z0-9]{3}|[A-Za-z0-9]{5,8})", part):
            raise ContractError("LANGUAGE_PROFILE")
        variants.append(part.lower())
    normalized = "-".join([language] + ([script] if script else []) + ([region] if region else []) + variants)
    return {"language": language, "normalized": normalized, "region": region, "script": script, "variants": variants}


def _font_language_tag(payload):
    _fields(payload, {"tag"})
    return _language_tag_value(payload["tag"])


def _feature_lookup(payload):
    _fields(payload, {"feature_tag", "lookup_indices", "lookup_count"})
    tag = _tag(payload["feature_tag"])
    count = _integer(payload["lookup_count"])
    if count < 0:
        raise ContractError("LOOKUP_RANGE")
    indices = payload["lookup_indices"]
    if not isinstance(indices, list):
        raise ContractError("LOOKUP_LIST")
    parsed = [_integer(index) for index in indices]
    if len(parsed) != len(set(parsed)):
        raise ContractError("DUPLICATE_LOOKUP")
    if any(index < 0 or index >= count for index in parsed):
        raise ContractError("LOOKUP_RANGE")
    return {"feature_tag": tag, "lookup_indices": parsed, "lookup_total": len(parsed)}


def _glyph_class(payload):
    _fields(payload, {"class_name", "glyph_ids", "glyph_count"})
    name = _text(payload["class_name"])
    codes = {"base": 1, "ligature": 2, "mark": 3, "component": 4}
    if name not in codes:
        raise ContractError("GLYPH_CLASS")
    count = _integer(payload["glyph_count"])
    if count < 0:
        raise ContractError("GLYPH_RANGE")
    glyphs = payload["glyph_ids"]
    if not isinstance(glyphs, list):
        raise ContractError("GLYPH_LIST")
    glyphs = [_integer(glyph) for glyph in glyphs]
    if len(glyphs) != len(set(glyphs)):
        raise ContractError("DUPLICATE_GLYPH")
    if glyphs != sorted(glyphs):
        raise ContractError("GLYPH_ORDER")
    if any(glyph < 0 or glyph >= count for glyph in glyphs):
        raise ContractError("GLYPH_RANGE")
    return {"class_code": codes[name], "class_name": name, "glyph_ids": glyphs}


def _color_layers(payload):
    _fields(payload, {"base_glyph", "glyph_count", "palette_count", "layers"})
    base = _integer(payload["base_glyph"])
    glyph_count = _integer(payload["glyph_count"])
    palette_count = _integer(payload["palette_count"])
    if glyph_count <= 0 or base < 0 or base >= glyph_count:
        raise ContractError("GLYPH_REFERENCE")
    if palette_count <= 0:
        raise ContractError("PALETTE_REFERENCE")
    layers = payload["layers"]
    if not isinstance(layers, list):
        raise ContractError("LAYER_LIST")
    parsed = []
    for layer in layers:
        if not isinstance(layer, dict) or set(layer) != {"glyph_id", "palette_index"}:
            raise ContractError("LAYER_SHAPE")
        glyph = _integer(layer["glyph_id"])
        palette = _integer(layer["palette_index"])
        if glyph < 0 or glyph >= glyph_count:
            raise ContractError("GLYPH_REFERENCE")
        if palette < 0 or palette >= palette_count:
            raise ContractError("PALETTE_REFERENCE")
        parsed.append({"glyph_id": glyph, "palette_index": palette})
    pairs = [(layer["glyph_id"], layer["palette_index"]) for layer in parsed]
    if len(pairs) != len(set(pairs)):
        raise ContractError("DUPLICATE_LAYER")
    return {"base_glyph": base, "layer_count": len(parsed), "layers": parsed}


def _local_glyph_reference(payload):
    _fields(payload, {"available_glyphs", "reference"})
    reference = _text(payload["reference"])
    if "://" in reference or reference.startswith("data:") or re.search(r"\.(?:otf|ttf|otc|ttc)#", reference, re.I):
        raise ContractError("EXTERNAL_REFERENCE")
    reference = _glyph_name(reference)
    available = payload["available_glyphs"]
    if not isinstance(available, list):
        raise ContractError("GLYPH_LIST")
    available = [_glyph_name(name) for name in available]
    if len(available) != len(set(available)):
        raise ContractError("DUPLICATE_TARGET")
    return {"external_fetch": False, "reference": reference, "resolved": reference in available}


def _rights_record(payload):
    _fields(payload, {"status"})
    status = _text(payload["status"])
    allowed = {"unknown", "owner_asserted", "license_reference_present", "public_domain_reference", "disputed", "withdrawn"}
    if status == "cleared":
        raise ContractError("RIGHTS_PROMOTION")
    if status not in allowed:
        raise ContractError("RIGHTS_STATUS")
    return {"authority_required": True, "authorized_for_publication": False, "evidence_state": status}


def _accessibility_handover(payload):
    _fields(payload, {"label", "description", "language", "correction_ref", "manual_evaluation"})
    label = _text(payload["label"])
    description = _text(payload["description"])
    correction = _text(payload["correction_ref"])
    manual = payload["manual_evaluation"]
    if type(manual) is not bool:
        raise ContractError("BOOLEAN_TYPE")
    if manual:
        raise ContractError("AUTHORITY_REQUIRED")
    language = _language_tag_value(payload["language"])["normalized"]
    return {
        "correction_present": bool(correction),
        "description_present": bool(description),
        "label_present": bool(label),
        "language": language,
        "manual_evaluation": False,
        "ready_for_affected_user": False,
    }


OPERATIONS = {
    "unicode_scalar": _unicode_scalar,
    "glyph_name": _glyph_name_operation,
    "table_tag": _table_tag,
    "table_directory": _table_directory,
    "quadratic_segment": lambda payload: _segment(payload, 2),
    "cubic_segment": lambda payload: _segment(payload, 3),
    "glyph_bbox": _glyph_bbox,
    "horizontal_metrics": _horizontal_metrics,
    "units_per_em": _units_per_em,
    "cmap_record": _cmap_record,
    "variation_axis": _variation_axis,
    "axis_coordinate": _axis_coordinate,
    "name_record": _name_record,
    "font_language_tag": _font_language_tag,
    "feature_lookup": _feature_lookup,
    "glyph_class": _glyph_class,
    "color_layers": _color_layers,
    "local_glyph_reference": _local_glyph_reference,
    "rights_record": _rights_record,
    "accessibility_handover": _accessibility_handover,
}


def evaluate(payload):
    before = canonical(payload)
    try:
        if not isinstance(payload, dict):
            raise ContractError("OBJECT_TYPE")
        operation = _text(payload.get("operation"))
        if operation not in OPERATIONS:
            raise ContractError("OPERATION")
        result = ok(OPERATIONS[operation](payload))
    except ContractError as exc:
        result = bad(str(exc))
    if canonical(payload) != before:
        raise AssertionError("INPUT_MUTATED")
    return result


def evaluate_raw(raw):
    try:
        payload = _strict_loads(raw)
        return evaluate(payload)
    except ContractError as exc:
        return bad(str(exc))


def evaluate_copy(payload):
    """Public helper emphasizing that callers retain their own input object."""
    return evaluate(copy.deepcopy(payload))
