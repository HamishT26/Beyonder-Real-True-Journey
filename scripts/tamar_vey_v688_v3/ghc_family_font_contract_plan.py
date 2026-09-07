"""Planning-only literal font-outline and glyph-metadata contracts.

This module contains frozen inputs and expected outputs only.  It deliberately
contains no evaluator, package import, font parsing, rendering, shaping, file
write, or external action.
"""
from __future__ import annotations


def ok(value):
    return {"accepted": True, "error": None, "external_credit": False, "value": value}


def bad(error):
    return {"accepted": False, "error": error, "external_credit": False, "value": None}


def case(title, fields, expected, outcome="completed"):
    return (title, fields, expected, outcome)


GROUPS = {
    "unicode_scalar": [
        case("Font scalar U plus 0041 records the basic Latin code point", {"token": "U+0041"}, ok({"codepoint": 65, "hex": "0041", "plane": 0, "scalar": True})),
        case("Font scalar U plus 0000 preserves the null scalar numerically", {"token": "U+0000"}, ok({"codepoint": 0, "hex": "0000", "plane": 0, "scalar": True})),
        case("Font scalar lowercase hex normalizes its hexadecimal digits", {"token": "U+00e9"}, ok({"codepoint": 233, "hex": "00E9", "plane": 0, "scalar": True})),
        case("Font scalar supplementary emoji value records plane one without a glyph claim", {"token": "U+1F600"}, ok({"codepoint": 128512, "hex": "1F600", "plane": 1, "scalar": True})),
        case("Font scalar maximum Unicode value remains inside plane sixteen", {"token": "U+10FFFF"}, ok({"codepoint": 1114111, "hex": "10FFFF", "plane": 16, "scalar": True})),
        case("Font scalar immediately below the surrogate block remains valid", {"token": "U+D7FF"}, ok({"codepoint": 55295, "hex": "D7FF", "plane": 0, "scalar": True})),
        case("Font scalar immediately above the surrogate block remains valid", {"token": "U+E000"}, ok({"codepoint": 57344, "hex": "E000", "plane": 0, "scalar": True})),
        case("Font scalar refuses a surrogate code point", {"token": "U+D800"}, bad("SURROGATE")),
        case("Font scalar refuses a value above the Unicode maximum", {"token": "U+110000"}, bad("SCALAR_RANGE")),
        case("Font scalar refuses a JSON Boolean token", {"token": True}, bad("TEXT_TYPE")),
    ],
    "glyph_name": [
        case("Glyph name preserves the reserved dot notdef spelling", {"name": ".notdef"}, ok({"characters": 7, "name": ".notdef", "reserved_notdef": True})),
        case("Glyph name preserves one ASCII letter", {"name": "A"}, ok({"characters": 1, "name": "A", "reserved_notdef": False})),
        case("Glyph name preserves a dotted alternate suffix", {"name": "A.alt"}, ok({"characters": 5, "name": "A.alt", "reserved_notdef": False})),
        case("Glyph name preserves a uni hexadecimal convention as metadata", {"name": "uni0041"}, ok({"characters": 7, "name": "uni0041", "reserved_notdef": False})),
        case("Glyph name preserves a supplementary u convention as metadata", {"name": "u1F600"}, ok({"characters": 6, "name": "u1F600", "reserved_notdef": False})),
        case("Glyph name permits a synthetic underscore identifier", {"name": "synthetic_1"}, ok({"characters": 11, "name": "synthetic_1", "reserved_notdef": False})),
        case("Glyph name refuses an empty identifier", {"name": ""}, bad("GLYPH_NAME")),
        case("Glyph name refuses embedded whitespace", {"name": "A B"}, bad("GLYPH_NAME")),
        case("Glyph name refuses a path separator", {"name": "A/B"}, bad("GLYPH_NAME")),
        case("Glyph name refuses a numeric JSON value", {"name": 7}, bad("TEXT_TYPE")),
    ],
    "table_tag": [
        case("OpenType head tag records four printable ASCII bytes", {"tag": "head"}, ok({"ascii_hex": "68656164", "length": 4, "tag": "head"})),
        case("OpenType cmap tag records four printable ASCII bytes", {"tag": "cmap"}, ok({"ascii_hex": "636d6170", "length": 4, "tag": "cmap"})),
        case("OpenType OS slash 2 tag retains punctuation", {"tag": "OS/2"}, ok({"ascii_hex": "4f532f32", "length": 4, "tag": "OS/2"})),
        case("OpenType CFF tag retains its trailing space", {"tag": "CFF "}, ok({"ascii_hex": "43464620", "length": 4, "tag": "CFF "})),
        case("OpenType SVG tag retains its trailing space", {"tag": "SVG "}, ok({"ascii_hex": "53564720", "length": 4, "tag": "SVG "})),
        case("OpenType GSUB tag retains uppercase spelling", {"tag": "GSUB"}, ok({"ascii_hex": "47535542", "length": 4, "tag": "GSUB"})),
        case("OpenType tag refuses three characters", {"tag": "abc"}, bad("TAG_LENGTH")),
        case("OpenType tag refuses five characters", {"tag": "abcde"}, bad("TAG_LENGTH")),
        case("OpenType tag refuses a non ASCII character", {"tag": "\u00e9abc"}, bad("TAG_ASCII")),
        case("OpenType tag refuses a JSON Boolean", {"tag": False}, bad("TEXT_TYPE")),
    ],
    "table_directory": [
        case("Font table directory may be empty in the bounded structural profile", {"records": []}, ok({"aligned": True, "count": 0, "nonoverlap": True, "tags": []})),
        case("Font table directory records one aligned head table", {"records": [{"checksum": 1, "length": 54, "offset": 0, "tag": "head"}]}, ok({"aligned": True, "count": 1, "nonoverlap": True, "tags": ["head"]})),
        case("Font table directory preserves two ascending nonoverlapping tags", {"records": [{"checksum": 2, "length": 32, "offset": 0, "tag": "cmap"}, {"checksum": 1, "length": 54, "offset": 32, "tag": "head"}]}, ok({"aligned": True, "count": 2, "nonoverlap": True, "tags": ["cmap", "head"]})),
        case("Font table directory distinguishes a zero length table from absence", {"records": [{"checksum": 0, "length": 0, "offset": 0, "tag": "cmap"}, {"checksum": 1, "length": 4, "offset": 0, "tag": "head"}]}, ok({"aligned": True, "count": 2, "nonoverlap": True, "tags": ["cmap", "head"]})),
        case("Font table directory exposes rather than repairs an unaligned offset", {"records": [{"checksum": 1, "length": 4, "offset": 2, "tag": "head"}]}, ok({"aligned": False, "count": 1, "nonoverlap": True, "tags": ["head"]})),
        case("Font table directory records an aligned gap between tables", {"records": [{"checksum": 2, "length": 4, "offset": 0, "tag": "cmap"}, {"checksum": 1, "length": 4, "offset": 8, "tag": "head"}]}, ok({"aligned": True, "count": 2, "nonoverlap": True, "tags": ["cmap", "head"]})),
        case("Font table directory refuses descending tag order", {"records": [{"checksum": 1, "length": 4, "offset": 0, "tag": "head"}, {"checksum": 2, "length": 4, "offset": 4, "tag": "cmap"}]}, bad("TAG_ORDER")),
        case("Font table directory refuses duplicate top level tags", {"records": [{"checksum": 1, "length": 4, "offset": 0, "tag": "head"}, {"checksum": 2, "length": 4, "offset": 4, "tag": "head"}]}, bad("DUPLICATE_TAG")),
        case("Font table directory refuses overlapping byte ranges", {"records": [{"checksum": 2, "length": 8, "offset": 0, "tag": "cmap"}, {"checksum": 1, "length": 8, "offset": 4, "tag": "head"}]}, bad("TABLE_OVERLAP")),
        case("Font table directory refuses a Boolean offset", {"records": [{"checksum": 1, "length": 4, "offset": True, "tag": "head"}]}, bad("INTEGER_TYPE")),
    ],
    "quadratic_segment": [
        case("Quadratic glyph segment preserves start control and end points", {"control": ["1", "2"], "end": ["3", "0"], "start": ["0", "0"]}, ok({"control": ["1", "2"], "degree": 2, "end": ["3", "0"], "envelope": ["0", "0", "3", "2"], "start": ["0", "0"]})),
        case("Quadratic glyph segment retains negative coordinates", {"control": ["-3", "5"], "end": ["0", "1"], "start": ["-4", "-2"]}, ok({"control": ["-3", "5"], "degree": 2, "end": ["0", "1"], "envelope": ["-4", "-2", "0", "5"], "start": ["-4", "-2"]})),
        case("Quadratic glyph segment keeps coincident points explicit", {"control": ["1", "1"], "end": ["1", "1"], "start": ["1", "1"]}, ok({"control": ["1", "1"], "degree": 2, "end": ["1", "1"], "envelope": ["1", "1", "1", "1"], "start": ["1", "1"]})),
        case("Quadratic glyph segment accepts signed coordinate boundaries", {"control": ["0", "0"], "end": ["32767", "-32768"], "start": ["-32768", "32767"]}, ok({"control": ["0", "0"], "degree": 2, "end": ["32767", "-32768"], "envelope": ["-32768", "-32768", "32767", "32767"], "start": ["-32768", "32767"]})),
        case("Quadratic glyph segment exposes a vertical control envelope", {"control": ["2", "5"], "end": ["2", "3"], "start": ["2", "-1"]}, ok({"control": ["2", "5"], "degree": 2, "end": ["2", "3"], "envelope": ["2", "-1", "2", "5"], "start": ["2", "-1"]})),
        case("Quadratic glyph segment keeps a collinear zero crossing", {"control": ["0", "0"], "end": ["1", "0"], "start": ["-1", "0"]}, ok({"control": ["0", "0"], "degree": 2, "end": ["1", "0"], "envelope": ["-1", "0", "1", "0"], "start": ["-1", "0"]})),
        case("Quadratic glyph segment refuses a one coordinate point", {"control": ["1", "2"], "end": ["3", "4"], "start": ["0"]}, bad("POINT_SHAPE")),
        case("Quadratic glyph segment refuses a Boolean coordinate", {"control": [True, "2"], "end": ["3", "4"], "start": ["0", "0"]}, bad("TEXT_TYPE")),
        case("Quadratic glyph segment refuses a coordinate above int16", {"control": ["32768", "0"], "end": ["3", "4"], "start": ["0", "0"]}, bad("COORDINATE_RANGE")),
        case("Quadratic glyph segment refuses an undeclared render field", {"control": ["1", "2"], "end": ["3", "4"], "render": True, "start": ["0", "0"]}, bad("FIELD_SET")),
    ],
    "cubic_segment": [
        case("Cubic glyph segment preserves two controls and endpoints", {"control1": ["1", "2"], "control2": ["3", "4"], "end": ["5", "0"], "start": ["0", "0"]}, ok({"control1": ["1", "2"], "control2": ["3", "4"], "degree": 3, "end": ["5", "0"], "envelope": ["0", "0", "5", "4"], "start": ["0", "0"]})),
        case("Cubic glyph segment retains negative controls", {"control1": ["-8", "2"], "control2": ["-3", "-7"], "end": ["0", "0"], "start": ["-5", "-1"]}, ok({"control1": ["-8", "2"], "control2": ["-3", "-7"], "degree": 3, "end": ["0", "0"], "envelope": ["-8", "-7", "0", "2"], "start": ["-5", "-1"]})),
        case("Cubic glyph segment keeps all coincident points", {"control1": ["2", "2"], "control2": ["2", "2"], "end": ["2", "2"], "start": ["2", "2"]}, ok({"control1": ["2", "2"], "control2": ["2", "2"], "degree": 3, "end": ["2", "2"], "envelope": ["2", "2", "2", "2"], "start": ["2", "2"]})),
        case("Cubic glyph segment records a horizontal control envelope", {"control1": ["-2", "0"], "control2": ["4", "0"], "end": ["3", "0"], "start": ["0", "0"]}, ok({"control1": ["-2", "0"], "control2": ["4", "0"], "degree": 3, "end": ["3", "0"], "envelope": ["-2", "0", "4", "0"], "start": ["0", "0"]})),
        case("Cubic glyph segment accepts signed int16 boundaries", {"control1": ["-32768", "0"], "control2": ["32767", "0"], "end": ["0", "-32768"], "start": ["0", "32767"]}, ok({"control1": ["-32768", "0"], "control2": ["32767", "0"], "degree": 3, "end": ["0", "-32768"], "envelope": ["-32768", "-32768", "32767", "32767"], "start": ["0", "32767"]})),
        case("Cubic glyph segment preserves control order when bounds match", {"control1": ["3", "3"], "control2": ["-3", "-3"], "end": ["0", "0"], "start": ["0", "0"]}, ok({"control1": ["3", "3"], "control2": ["-3", "-3"], "degree": 3, "end": ["0", "0"], "envelope": ["-3", "-3", "3", "3"], "start": ["0", "0"]})),
        case("Cubic glyph segment refuses a malformed second control", {"control1": ["1", "2"], "control2": ["3"], "end": ["5", "6"], "start": ["0", "0"]}, bad("POINT_SHAPE")),
        case("Cubic glyph segment refuses a numeric JSON coordinate", {"control1": [1, "2"], "control2": ["3", "4"], "end": ["5", "6"], "start": ["0", "0"]}, bad("TEXT_TYPE")),
        case("Cubic glyph segment refuses a coordinate below int16", {"control1": ["-32769", "0"], "control2": ["3", "4"], "end": ["5", "6"], "start": ["0", "0"]}, bad("COORDINATE_RANGE")),
        case("Cubic glyph segment refuses an undeclared flatten field", {"control1": ["1", "2"], "control2": ["3", "4"], "end": ["5", "6"], "flatten": True, "start": ["0", "0"]}, bad("FIELD_SET")),
    ],
    "glyph_bbox": [
        case("Glyph bounding box encloses a synthetic triangle", {"points": [["0", "0"], ["10", "0"], ["4", "8"]]}, ok({"height": "8", "point_count": 3, "width": "10", "x_max": "10", "x_min": "0", "y_max": "8", "y_min": "0"})),
        case("Glyph bounding box retains negative coordinates", {"points": [["-5", "-2"], ["-1", "-7"]]}, ok({"height": "5", "point_count": 2, "width": "4", "x_max": "-1", "x_min": "-5", "y_max": "-2", "y_min": "-7"})),
        case("Glyph bounding box for one point has zero extents", {"points": [["3", "4"]]}, ok({"height": "0", "point_count": 1, "width": "0", "x_max": "3", "x_min": "3", "y_max": "4", "y_min": "4"})),
        case("Glyph bounding box retains duplicate points in its count", {"points": [["1", "1"], ["1", "1"]]}, ok({"height": "0", "point_count": 2, "width": "0", "x_max": "1", "x_min": "1", "y_max": "1", "y_min": "1"})),
        case("Glyph bounding box records a vertical outline", {"points": [["2", "-3"], ["2", "5"]]}, ok({"height": "8", "point_count": 2, "width": "0", "x_max": "2", "x_min": "2", "y_max": "5", "y_min": "-3"})),
        case("Glyph bounding box records a horizontal outline", {"points": [["-9", "0"], ["9", "0"]]}, ok({"height": "0", "point_count": 2, "width": "18", "x_max": "9", "x_min": "-9", "y_max": "0", "y_min": "0"})),
        case("Glyph bounding box refuses an empty point list", {"points": []}, bad("NO_POINTS")),
        case("Glyph bounding box refuses a three coordinate point", {"points": [["1", "2", "3"]]}, bad("POINT_SHAPE")),
        case("Glyph bounding box refuses a Boolean coordinate", {"points": [[False, "0"]]}, bad("TEXT_TYPE")),
        case("Glyph bounding box refuses an out of range coordinate", {"points": [["0", "40000"]]}, bad("COORDINATE_RANGE")),
    ],
    "horizontal_metrics": [
        case("Font horizontal metrics derive a right side bearing", {"advance_width": 600, "lsb": 50, "x_max": 500, "x_min": 0}, ok({"advance_width": 600, "lsb": 50, "rsb": 50, "x_min_matches_lsb": False})),
        case("Font horizontal metrics expose matching x minimum and side bearing", {"advance_width": 500, "lsb": 0, "x_max": 500, "x_min": 0}, ok({"advance_width": 500, "lsb": 0, "rsb": 0, "x_min_matches_lsb": True})),
        case("Font horizontal metrics retain a negative left side bearing", {"advance_width": 500, "lsb": -20, "x_max": 480, "x_min": -20}, ok({"advance_width": 500, "lsb": -20, "rsb": 0, "x_min_matches_lsb": True})),
        case("Font horizontal metrics retain a negative right side bearing", {"advance_width": 400, "lsb": 20, "x_max": 500, "x_min": 0}, ok({"advance_width": 400, "lsb": 20, "rsb": -120, "x_min_matches_lsb": False})),
        case("Font horizontal metrics preserve a zero advance empty extent", {"advance_width": 0, "lsb": 0, "x_max": 0, "x_min": 0}, ok({"advance_width": 0, "lsb": 0, "rsb": 0, "x_min_matches_lsb": True})),
        case("Font horizontal metrics preserve unsigned and signed boundaries", {"advance_width": 65535, "lsb": 32767, "x_max": 32767, "x_min": -32768}, ok({"advance_width": 65535, "lsb": 32767, "rsb": -32767, "x_min_matches_lsb": False})),
        case("Font horizontal metrics refuse a negative advance width", {"advance_width": -1, "lsb": 0, "x_max": 0, "x_min": 0}, bad("ADVANCE_RANGE")),
        case("Font horizontal metrics refuse a Boolean width", {"advance_width": True, "lsb": 0, "x_max": 0, "x_min": 0}, bad("INTEGER_TYPE")),
        case("Font horizontal metrics refuse reversed x bounds", {"advance_width": 500, "lsb": 0, "x_max": -1, "x_min": 1}, bad("BBOX_ORDER")),
        case("Font horizontal metrics refuse an undeclared measured field", {"advance_width": 500, "lsb": 0, "measured": True, "x_max": 500, "x_min": 0}, bad("FIELD_SET")),
    ],
    "units_per_em": [
        case("Font units per em accepts the minimum bounded value", {"value": 16}, ok({"power_of_two": True, "reciprocal": "1/16", "units_per_em": 16})),
        case("Font units per em preserves the common one thousand grid", {"value": 1000}, ok({"power_of_two": False, "reciprocal": "1/1000", "units_per_em": 1000})),
        case("Font units per em recognizes a two thousand forty eight grid", {"value": 2048}, ok({"power_of_two": True, "reciprocal": "1/2048", "units_per_em": 2048})),
        case("Font units per em recognizes a four thousand ninety six grid", {"value": 4096}, ok({"power_of_two": True, "reciprocal": "1/4096", "units_per_em": 4096})),
        case("Font units per em accepts the maximum bounded value", {"value": 16384}, ok({"power_of_two": True, "reciprocal": "1/16384", "units_per_em": 16384})),
        case("Font units per em refuses a value below sixteen", {"value": 15}, bad("UPEM_RANGE")),
        case("Font units per em refuses a value above sixteen thousand three hundred eighty four", {"value": 16385}, bad("UPEM_RANGE")),
        case("Font units per em refuses zero", {"value": 0}, bad("UPEM_RANGE")),
        case("Font units per em refuses a JSON Boolean", {"value": True}, bad("INTEGER_TYPE")),
        case("Font units per em refuses a textual integer", {"value": "1000"}, bad("INTEGER_TYPE")),
    ],
    "cmap_record": [
        case("Font cmap records a new basic scalar mapping", {"codepoint": 65, "existing": [], "glyph_count": 2, "glyph_id": 1}, ok({"codepoint": 65, "glyph_id": 1, "idempotent": False, "mapping_count": 1})),
        case("Font cmap recognizes an identical existing mapping", {"codepoint": 65, "existing": [{"codepoint": 65, "glyph_id": 1}], "glyph_count": 2, "glyph_id": 1}, ok({"codepoint": 65, "glyph_id": 1, "idempotent": True, "mapping_count": 1})),
        case("Font cmap appends a mapping after a different scalar", {"codepoint": 65, "existing": [{"codepoint": 66, "glyph_id": 1}], "glyph_count": 3, "glyph_id": 2}, ok({"codepoint": 65, "glyph_id": 2, "idempotent": False, "mapping_count": 2})),
        case("Font cmap records a supplementary scalar without a glyph-shape claim", {"codepoint": 128512, "existing": [], "glyph_count": 3, "glyph_id": 2}, ok({"codepoint": 128512, "glyph_id": 2, "idempotent": False, "mapping_count": 1})),
        case("Font cmap permits an explicit scalar zero mapping to glyph zero", {"codepoint": 0, "existing": [], "glyph_count": 1, "glyph_id": 0}, ok({"codepoint": 0, "glyph_id": 0, "idempotent": False, "mapping_count": 1})),
        case("Font cmap refuses a conflicting mapping for one scalar", {"codepoint": 65, "existing": [{"codepoint": 65, "glyph_id": 1}], "glyph_count": 3, "glyph_id": 2}, bad("CMAP_CONFLICT")),
        case("Font cmap refuses a glyph id outside the declared count", {"codepoint": 65, "existing": [], "glyph_count": 2, "glyph_id": 2}, bad("GLYPH_RANGE")),
        case("Font cmap refuses a surrogate code point", {"codepoint": 55296, "existing": [], "glyph_count": 2, "glyph_id": 1}, bad("SURROGATE")),
        case("Font cmap refuses duplicate existing scalar records", {"codepoint": 66, "existing": [{"codepoint": 65, "glyph_id": 1}, {"codepoint": 65, "glyph_id": 1}], "glyph_count": 3, "glyph_id": 2}, bad("DUPLICATE_CODEPOINT")),
        case("Font cmap refuses a Boolean code point", {"codepoint": True, "existing": [], "glyph_count": 2, "glyph_id": 1}, bad("INTEGER_TYPE")),
    ],
    "variation_axis": [
        case("Font weight axis records ordered minimum default and maximum", {"default": "400", "maximum": "900", "minimum": "100", "tag": "wght"}, ok({"default": "400", "maximum": "900", "minimum": "100", "span": "800", "tag": "wght"})),
        case("Font width axis records a symmetric bounded span", {"default": "100", "maximum": "125", "minimum": "75", "tag": "wdth"}, ok({"default": "100", "maximum": "125", "minimum": "75", "span": "50", "tag": "wdth"})),
        case("Font italic axis permits the default at its minimum", {"default": "0", "maximum": "1", "minimum": "0", "tag": "ital"}, ok({"default": "0", "maximum": "1", "minimum": "0", "span": "1", "tag": "ital"})),
        case("Font slant axis permits the default at its maximum", {"default": "0", "maximum": "0", "minimum": "-12", "tag": "slnt"}, ok({"default": "0", "maximum": "0", "minimum": "-12", "span": "12", "tag": "slnt"})),
        case("Font optical size axis records a wider positive span", {"default": "14", "maximum": "72", "minimum": "8", "tag": "opsz"}, ok({"default": "14", "maximum": "72", "minimum": "8", "span": "64", "tag": "opsz"})),
        case("Font synthetic axis preserves exact fractional bounds", {"default": "1", "maximum": "1.5", "minimum": ".5", "tag": "TEST"}, ok({"default": "1", "maximum": "3/2", "minimum": "1/2", "span": "1", "tag": "TEST"})),
        case("Font variation axis refuses a short tag", {"default": "0", "maximum": "1", "minimum": "-1", "tag": "abc"}, bad("TAG_LENGTH")),
        case("Font variation axis refuses a default below its minimum", {"default": "-1", "maximum": "1", "minimum": "0", "tag": "TEST"}, bad("AXIS_ORDER")),
        case("Font variation axis refuses a default above its maximum", {"default": "2", "maximum": "1", "minimum": "0", "tag": "TEST"}, bad("AXIS_ORDER")),
        case("Font variation axis refuses a Boolean bound", {"default": True, "maximum": "1", "minimum": "0", "tag": "TEST"}, bad("TEXT_TYPE")),
    ],
    "axis_coordinate": [
        case("Font variation coordinate normalizes the default to zero", {"default": "400", "maximum": "900", "minimum": "100", "value": "400"}, ok({"normalized": "0", "zone": "default"})),
        case("Font variation coordinate normalizes the minimum to negative one", {"default": "400", "maximum": "900", "minimum": "100", "value": "100"}, ok({"normalized": "-1", "zone": "lower"})),
        case("Font variation coordinate normalizes the maximum to positive one", {"default": "400", "maximum": "900", "minimum": "100", "value": "900"}, ok({"normalized": "1", "zone": "upper"})),
        case("Font variation coordinate preserves an exact lower half", {"default": "400", "maximum": "900", "minimum": "100", "value": "250"}, ok({"normalized": "-1/2", "zone": "lower"})),
        case("Font variation coordinate preserves an exact upper half", {"default": "400", "maximum": "900", "minimum": "100", "value": "650"}, ok({"normalized": "1/2", "zone": "upper"})),
        case("Font variation coordinate handles a negative lower interval", {"default": "0", "maximum": "0", "minimum": "-12", "value": "-6"}, ok({"normalized": "-1/2", "zone": "lower"})),
        case("Font variation coordinate refuses a value below the axis", {"default": "400", "maximum": "900", "minimum": "100", "value": "50"}, bad("COORDINATE_RANGE")),
        case("Font variation coordinate refuses a value above the axis", {"default": "400", "maximum": "900", "minimum": "100", "value": "901"}, bad("COORDINATE_RANGE")),
        case("Font variation coordinate refuses a degenerate axis", {"default": "1", "maximum": "1", "minimum": "1", "value": "1"}, bad("AXIS_DEGENERATE")),
        case("Font variation coordinate refuses a Boolean value", {"default": "0", "maximum": "1", "minimum": "-1", "value": False}, bad("TEXT_TYPE")),
    ],
    "name_record": [
        case("Font naming record preserves a synthetic family string", {"encoding_id": 1, "language_id": 1033, "name_id": 1, "platform_id": 3, "text": "Synthetic Sans"}, ok({"characters": 14, "empty": False, "key": "3:1:1033:1", "text": "Synthetic Sans"})),
        case("Font naming record preserves a Unicode platform string", {"encoding_id": 4, "language_id": 0, "name_id": 1, "platform_id": 0, "text": "Test"}, ok({"characters": 4, "empty": False, "key": "0:4:0:1", "text": "Test"})),
        case("Font naming record keeps an empty structural string visible", {"encoding_id": 0, "language_id": 0, "name_id": 2, "platform_id": 1, "text": ""}, ok({"characters": 0, "empty": True, "key": "1:0:0:2", "text": ""})),
        case("Font naming record counts Unicode code points without encoding authority", {"encoding_id": 10, "language_id": 1033, "name_id": 256, "platform_id": 3, "text": "Caf\u00e9"}, ok({"characters": 4, "empty": False, "key": "3:10:1033:256", "text": "Caf\u00e9"})),
        case("Font naming record preserves a synthetic version string", {"encoding_id": 1, "language_id": 0, "name_id": 5, "platform_id": 3, "text": "Version 1.0"}, ok({"characters": 11, "empty": False, "key": "3:1:0:5", "text": "Version 1.0"})),
        case("Font naming record refuses a negative platform id", {"encoding_id": 1, "language_id": 0, "name_id": 1, "platform_id": -1, "text": "Test"}, bad("ID_RANGE")),
        case("Font naming record refuses a name id above uint16", {"encoding_id": 1, "language_id": 0, "name_id": 65536, "platform_id": 3, "text": "Test"}, bad("ID_RANGE")),
        case("Font naming record refuses a Boolean encoding id", {"encoding_id": True, "language_id": 0, "name_id": 1, "platform_id": 3, "text": "Test"}, bad("INTEGER_TYPE")),
        case("Font naming record refuses a numeric text field", {"encoding_id": 1, "language_id": 0, "name_id": 1, "platform_id": 3, "text": 7}, bad("TEXT_TYPE")),
        case("Font naming record refuses embedded null control text", {"encoding_id": 1, "language_id": 0, "name_id": 1, "platform_id": 3, "text": "A\u0000B"}, bad("TEXT_CONTROL")),
    ],
    "font_language_tag": [
        case("Font language tag preserves undetermined language", {"tag": "und"}, ok({"language": "und", "normalized": "und", "region": None, "script": None, "variants": []})),
        case("Font language tag preserves a basic English tag", {"tag": "en"}, ok({"language": "en", "normalized": "en", "region": None, "script": None, "variants": []})),
        case("Font language tag normalizes an English New Zealand region", {"tag": "en-nz"}, ok({"language": "en", "normalized": "en-NZ", "region": "NZ", "script": None, "variants": []})),
        case("Font language tag normalizes a Latin script subtag", {"tag": "sr-latn"}, ok({"language": "sr", "normalized": "sr-Latn", "region": None, "script": "Latn", "variants": []})),
        case("Font language tag preserves script and region ordering", {"tag": "zh-Hant-TW"}, ok({"language": "zh", "normalized": "zh-Hant-TW", "region": "TW", "script": "Hant", "variants": []})),
        case("Font language tag retains a numeric variant", {"tag": "de-1996"}, ok({"language": "de", "normalized": "de-1996", "region": None, "script": None, "variants": ["1996"]})),
        case("Font language tag refuses underscore separators", {"tag": "en_US"}, bad("LANGUAGE_PROFILE")),
        case("Font language tag refuses an empty value", {"tag": ""}, bad("LANGUAGE_PROFILE")),
        case("Font language tag refuses an empty interior subtag", {"tag": "en--US"}, bad("LANGUAGE_PROFILE")),
        case("Font language tag refuses a JSON Boolean", {"tag": True}, bad("TEXT_TYPE")),
    ],
    "feature_lookup": [
        case("Font feature lookup preserves liga lookup order", {"feature_tag": "liga", "lookup_count": 3, "lookup_indices": [0, 2]}, ok({"feature_tag": "liga", "lookup_indices": [0, 2], "lookup_total": 2})),
        case("Font feature lookup permits an empty kern lookup list", {"feature_tag": "kern", "lookup_count": 0, "lookup_indices": []}, ok({"feature_tag": "kern", "lookup_indices": [], "lookup_total": 0})),
        case("Font feature lookup preserves a nonascending salt lookup order", {"feature_tag": "salt", "lookup_count": 2, "lookup_indices": [1, 0]}, ok({"feature_tag": "salt", "lookup_indices": [1, 0], "lookup_total": 2})),
        case("Font feature lookup records one zero index", {"feature_tag": "zero", "lookup_count": 1, "lookup_indices": [0]}, ok({"feature_tag": "zero", "lookup_indices": [0], "lookup_total": 1})),
        case("Font feature lookup preserves three distinct references", {"feature_tag": "TEST", "lookup_count": 4, "lookup_indices": [3, 1, 2]}, ok({"feature_tag": "TEST", "lookup_indices": [3, 1, 2], "lookup_total": 3})),
        case("Font feature lookup refuses a short feature tag", {"feature_tag": "lig", "lookup_count": 1, "lookup_indices": [0]}, bad("TAG_LENGTH")),
        case("Font feature lookup refuses an index at the lookup count", {"feature_tag": "liga", "lookup_count": 2, "lookup_indices": [2]}, bad("LOOKUP_RANGE")),
        case("Font feature lookup refuses duplicate lookup indices", {"feature_tag": "liga", "lookup_count": 2, "lookup_indices": [1, 1]}, bad("DUPLICATE_LOOKUP")),
        case("Font feature lookup refuses a Boolean index", {"feature_tag": "liga", "lookup_count": 2, "lookup_indices": [True]}, bad("INTEGER_TYPE")),
        case("Font feature lookup refuses a negative lookup count", {"feature_tag": "liga", "lookup_count": -1, "lookup_indices": []}, bad("LOOKUP_RANGE")),
    ],
    "glyph_class": [
        case("Font glyph class records base glyph ids", {"class_name": "base", "glyph_count": 4, "glyph_ids": [0, 2]}, ok({"class_code": 1, "class_name": "base", "glyph_ids": [0, 2]})),
        case("Font glyph class records a ligature glyph", {"class_name": "ligature", "glyph_count": 4, "glyph_ids": [1]}, ok({"class_code": 2, "class_name": "ligature", "glyph_ids": [1]})),
        case("Font glyph class records ordered mark glyphs", {"class_name": "mark", "glyph_count": 5, "glyph_ids": [2, 3, 4]}, ok({"class_code": 3, "class_name": "mark", "glyph_ids": [2, 3, 4]})),
        case("Font glyph class records a component glyph", {"class_name": "component", "glyph_count": 3, "glyph_ids": [2]}, ok({"class_code": 4, "class_name": "component", "glyph_ids": [2]})),
        case("Font glyph class permits an empty base class", {"class_name": "base", "glyph_count": 0, "glyph_ids": []}, ok({"class_code": 1, "class_name": "base", "glyph_ids": []})),
        case("Font glyph class preserves a complete ascending range", {"class_name": "base", "glyph_count": 4, "glyph_ids": [0, 1, 2, 3]}, ok({"class_code": 1, "class_name": "base", "glyph_ids": [0, 1, 2, 3]})),
        case("Font glyph class refuses an unknown class", {"class_name": "letter", "glyph_count": 2, "glyph_ids": [0]}, bad("GLYPH_CLASS")),
        case("Font glyph class refuses duplicate glyph ids", {"class_name": "mark", "glyph_count": 3, "glyph_ids": [1, 1]}, bad("DUPLICATE_GLYPH")),
        case("Font glyph class refuses an id outside the glyph count", {"class_name": "base", "glyph_count": 2, "glyph_ids": [2]}, bad("GLYPH_RANGE")),
        case("Font glyph class refuses a Boolean id", {"class_name": "base", "glyph_count": 2, "glyph_ids": [False]}, bad("INTEGER_TYPE")),
    ],
    "color_layers": [
        case("Font color layer record permits an empty layer list", {"base_glyph": 0, "glyph_count": 1, "layers": [], "palette_count": 1}, ok({"base_glyph": 0, "layer_count": 0, "layers": []}), "represented"),
        case("Font color layer record preserves one glyph palette reference", {"base_glyph": 0, "glyph_count": 2, "layers": [{"glyph_id": 1, "palette_index": 0}], "palette_count": 1}, ok({"base_glyph": 0, "layer_count": 1, "layers": [{"glyph_id": 1, "palette_index": 0}]}), "represented"),
        case("Font color layer record preserves two ordered layer references", {"base_glyph": 0, "glyph_count": 3, "layers": [{"glyph_id": 1, "palette_index": 0}, {"glyph_id": 2, "palette_index": 1}], "palette_count": 2}, ok({"base_glyph": 0, "layer_count": 2, "layers": [{"glyph_id": 1, "palette_index": 0}, {"glyph_id": 2, "palette_index": 1}]}), "represented"),
        case("Font color layer record permits one glyph in two palette slots", {"base_glyph": 0, "glyph_count": 2, "layers": [{"glyph_id": 1, "palette_index": 0}, {"glyph_id": 1, "palette_index": 1}], "palette_count": 2}, ok({"base_glyph": 0, "layer_count": 2, "layers": [{"glyph_id": 1, "palette_index": 0}, {"glyph_id": 1, "palette_index": 1}]}), "represented"),
        case("Font color layer record keeps an explicit base glyph layer", {"base_glyph": 0, "glyph_count": 1, "layers": [{"glyph_id": 0, "palette_index": 0}], "palette_count": 1}, ok({"base_glyph": 0, "layer_count": 1, "layers": [{"glyph_id": 0, "palette_index": 0}]}), "represented"),
        case("Font color layer record refuses a missing glyph reference", {"base_glyph": 0, "glyph_count": 2, "layers": [{"glyph_id": 2, "palette_index": 0}], "palette_count": 1}, bad("GLYPH_REFERENCE")),
        case("Font color layer record refuses a missing palette entry", {"base_glyph": 0, "glyph_count": 2, "layers": [{"glyph_id": 1, "palette_index": 1}], "palette_count": 1}, bad("PALETTE_REFERENCE")),
        case("Font color layer record refuses an exact duplicate layer", {"base_glyph": 0, "glyph_count": 2, "layers": [{"glyph_id": 1, "palette_index": 0}, {"glyph_id": 1, "palette_index": 0}], "palette_count": 1}, bad("DUPLICATE_LAYER")),
        case("Font color layer record refuses a Boolean glyph id", {"base_glyph": 0, "glyph_count": 2, "layers": [{"glyph_id": True, "palette_index": 0}], "palette_count": 1}, bad("INTEGER_TYPE")),
        case("Font color layer record refuses an incomplete layer shape", {"base_glyph": 0, "glyph_count": 2, "layers": [{"glyph_id": 1}], "palette_count": 1}, bad("LAYER_SHAPE")),
    ],
    "local_glyph_reference": [
        case("Font local glyph reference resolves an available synthetic name", {"available_glyphs": ["A"], "reference": "A"}, ok({"external_fetch": False, "reference": "A", "resolved": True})),
        case("Font unavailable local glyph reference remains unresolved", {"available_glyphs": ["A"], "reference": "B"}, ok({"external_fetch": False, "reference": "B", "resolved": False}), "open_gap"),
        case("Font local glyph reference preserves case and remains unresolved", {"available_glyphs": ["A"], "reference": "a"}, ok({"external_fetch": False, "reference": "a", "resolved": False}), "open_gap"),
        case("Font local glyph reference resolves dot notdef explicitly", {"available_glyphs": [".notdef"], "reference": ".notdef"}, ok({"external_fetch": False, "reference": ".notdef", "resolved": True})),
        case("Font network glyph reference requires separate authority", {"available_glyphs": [], "reference": "https://example.invalid/font.otf#A"}, bad("EXTERNAL_REFERENCE"), "exact_gate"),
        case("Font relative document glyph reference requires separate authority", {"available_glyphs": [], "reference": "other.otf#A"}, bad("EXTERNAL_REFERENCE"), "exact_gate"),
        case("Font data URI glyph reference remains outside the local profile", {"available_glyphs": [], "reference": "data:font/otf,synthetic"}, bad("EXTERNAL_REFERENCE"), "exact_gate"),
        case("Font local glyph reference refuses duplicate available names", {"available_glyphs": ["A", "A"], "reference": "A"}, bad("DUPLICATE_TARGET")),
        case("Font local glyph reference refuses an empty name", {"available_glyphs": [], "reference": ""}, bad("GLYPH_NAME")),
        case("Font local glyph reference refuses a Boolean name", {"available_glyphs": [], "reference": True}, bad("TEXT_TYPE")),
    ],
    "rights_record": [
        case("Font rights record keeps unknown status unauthorised", {"status": "unknown"}, ok({"authority_required": True, "authorized_for_publication": False, "evidence_state": "unknown"}), "represented"),
        case("Font rights record keeps owner asserted status unverified", {"status": "owner_asserted"}, ok({"authority_required": True, "authorized_for_publication": False, "evidence_state": "owner_asserted"}), "represented"),
        case("Font rights record keeps a license reference nonconclusive", {"status": "license_reference_present"}, ok({"authority_required": True, "authorized_for_publication": False, "evidence_state": "license_reference_present"}), "represented"),
        case("Font rights record keeps a public domain reference nonconclusive", {"status": "public_domain_reference"}, ok({"authority_required": True, "authorized_for_publication": False, "evidence_state": "public_domain_reference"}), "represented"),
        case("Font rights record preserves a disputed state", {"status": "disputed"}, ok({"authority_required": True, "authorized_for_publication": False, "evidence_state": "disputed"}), "represented"),
        case("Font rights record preserves a withdrawn state", {"status": "withdrawn"}, ok({"authority_required": True, "authorized_for_publication": False, "evidence_state": "withdrawn"}), "represented"),
        case("Font rights record refuses a synthetic cleared claim", {"status": "cleared"}, bad("RIGHTS_PROMOTION")),
        case("Font rights record refuses an empty status", {"status": ""}, bad("RIGHTS_STATUS")),
        case("Font rights record refuses a Boolean status", {"status": True}, bad("TEXT_TYPE")),
        case("Font rights record refuses an undeclared authority flag", {"authority": True, "status": "unknown"}, bad("FIELD_SET")),
    ],
    "accessibility_handover": [
        case("Font accessibility handover records all structural labels", {"correction_ref": "corr-001", "description": "Synthetic glyph set", "label": "Synthetic font", "language": "en", "manual_evaluation": False}, ok({"correction_present": True, "description_present": True, "label_present": True, "language": "en", "manual_evaluation": False, "ready_for_affected_user": False}), "represented"),
        case("Font accessibility handover exposes a missing description", {"correction_ref": "corr-002", "description": "", "label": "Synthetic font", "language": "en", "manual_evaluation": False}, ok({"correction_present": True, "description_present": False, "label_present": True, "language": "en", "manual_evaluation": False, "ready_for_affected_user": False}), "represented"),
        case("Font accessibility handover exposes a missing label", {"correction_ref": "corr-003", "description": "Synthetic glyph set", "label": "", "language": "en", "manual_evaluation": False}, ok({"correction_present": True, "description_present": True, "label_present": False, "language": "en", "manual_evaluation": False, "ready_for_affected_user": False}), "represented"),
        case("Font accessibility handover preserves an undetermined language tag", {"correction_ref": "corr-004", "description": "Synthetic glyph set", "label": "Synthetic font", "language": "und", "manual_evaluation": False}, ok({"correction_present": True, "description_present": True, "label_present": True, "language": "und", "manual_evaluation": False, "ready_for_affected_user": False}), "represented"),
        case("Font accessibility handover exposes an absent correction reference", {"correction_ref": "", "description": "Synthetic glyph set", "label": "Synthetic font", "language": "en", "manual_evaluation": False}, ok({"correction_present": False, "description_present": True, "label_present": True, "language": "en", "manual_evaluation": False, "ready_for_affected_user": False}), "represented"),
        case("Font accessibility handover preserves a regional language label structurally", {"correction_ref": "corr-005", "description": "Synthetic glyph set", "label": "Synthetic font", "language": "en-NZ", "manual_evaluation": False}, ok({"correction_present": True, "description_present": True, "label_present": True, "language": "en-NZ", "manual_evaluation": False, "ready_for_affected_user": False}), "represented"),
        case("Font accessibility handover refuses a preclaimed manual evaluation", {"correction_ref": "corr-006", "description": "Synthetic glyph set", "label": "Synthetic font", "language": "en", "manual_evaluation": True}, bad("AUTHORITY_REQUIRED")),
        case("Font accessibility handover refuses a numeric label", {"correction_ref": "corr-007", "description": "Synthetic glyph set", "label": 7, "language": "en", "manual_evaluation": False}, bad("TEXT_TYPE")),
        case("Font accessibility handover refuses an unsupported language shape", {"correction_ref": "corr-008", "description": "Synthetic glyph set", "label": "Synthetic font", "language": "en_US", "manual_evaluation": False}, bad("LANGUAGE_PROFILE")),
        case("Font accessibility handover refuses an undeclared certified field", {"certified": True, "correction_ref": "corr-009", "description": "Synthetic glyph set", "label": "Synthetic font", "language": "en", "manual_evaluation": False}, bad("FIELD_SET")),
    ],
}


SKILL_PAIRS = [
    ("ghc-family-font-scalar-and-name-tokens", ["unicode_scalar", "glyph_name"]),
    ("ghc-family-font-table-tags-and-directory", ["table_tag", "table_directory"]),
    ("ghc-family-font-outline-segments", ["quadratic_segment", "cubic_segment"]),
    ("ghc-family-font-bounds-and-metrics", ["glyph_bbox", "horizontal_metrics"]),
    ("ghc-family-font-cmap-and-units", ["units_per_em", "cmap_record"]),
    ("ghc-family-font-variation-metadata", ["variation_axis", "axis_coordinate"]),
    ("ghc-family-font-name-and-language-records", ["name_record", "font_language_tag"]),
    ("ghc-family-font-feature-and-glyph-classes", ["feature_lookup", "glyph_class"]),
    ("ghc-family-font-color-and-local-references", ["color_layers", "local_glyph_reference"]),
    ("ghc-family-font-rights-and-access-handover", ["rights_record", "accessibility_handover"]),
]


def literal_contracts():
    rows = []
    for operation, cases in GROUPS.items():
        if len(cases) != 10:
            raise ValueError(f"{operation} must contain exactly ten distinct contracts")
        for title, fields, expected, outcome in cases:
            rows.append(
                {
                    "proposal_id": f"TV6883-N{len(rows) + 1:03}",
                    "operation": operation,
                    "title": title,
                    "input": {"operation": operation, **fields},
                    "expected_output": expected,
                    "expected_execution_disposition": outcome,
                }
            )
    if len(rows) != 200:
        raise ValueError("The planning freeze requires exactly 200 contracts")
    return rows
