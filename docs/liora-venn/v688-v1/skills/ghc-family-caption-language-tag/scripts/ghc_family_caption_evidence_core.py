"""Deterministic, zero-row caption contract evaluator for Liora v688-v1."""
from __future__ import annotations

import copy
import argparse
import json
import re
import sys
from fractions import Fraction


MAX_MILLISECONDS = 86_400_000
MAX_FRAME = 1_000_000_000
RELATIONS = {"caption_of", "transcript_of", "description_of"}
ACCESS_FEATURES = {
    "captions",
    "transcript",
    "audio_description",
    "chapters",
    "sign_language",
    "easy_read_summary",
}
PUBLICATION_REQUIREMENTS = {
    "publish_captions": ["rights_holder", "affected_people", "privacy_review"],
    "publish_transcript": ["rights_holder", "speaker_consent", "privacy_review"],
    "name_speaker": ["affected_people", "competent_identity_review"],
    "translate_caption": ["competent_language_review", "affected_people"],
    "assign_maori_wording": ["maori_authority", "affected_people"],
    "release_maori_data": ["maori_data_governance", "tangata_whenua_iwi_hapu"],
    "assert_tikanga": ["maori_authority"],
    "assert_taonga_status": ["maori_authority"],
    "declare_accessibility_complete": ["affected_user_evaluation", "assistive_technology_review"],
    "deploy_caption_service": ["production_security_review", "service_owner"],
    "delete_source_media": ["exact_destructive_authority", "recoverable_backup"],
    "replace_master_transcript": ["record_custodian", "correction_authority"],
    "determine_copyright": ["competent_legal_authority", "rights_holder"],
    "share_private_caption": ["privacy_review", "affected_people"],
    "use_real_participants": ["governed_consent", "safety_monitoring", "competent_review"],
    "claim_thos_effectiveness": ["preregistered_real_arms", "independent_review"],
    "claim_gmut_confirmation": ["empirical_model_comparison", "independent_review"],
    "promote_stage20": ["all_exact_external_gates", "competent_affected_authority"],
}


def accept(value):
    return {"accepted": True, "value": value, "error": None, "external_credit": False}


def hold(code):
    return {"accepted": False, "value": None, "error": code, "external_credit": False}


def exact_type_equal(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(exact_type_equal(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(exact_type_equal(a, b) for a, b in zip(left, right))
    return left == right


def output_matches(candidate, expected):
    return exact_type_equal(candidate, expected)


def altered_output(expected, mutation):
    candidate = copy.deepcopy(expected)
    if mutation == "missing_accepted":
        candidate.pop("accepted", None)
    elif mutation == "accepted_type":
        candidate["accepted"] = 1 if expected["accepted"] else 0
    elif mutation == "extra_authority":
        candidate["authority_granted"] = True
    elif mutation == "value_replaced":
        candidate["value"] = {"unexpected": True} if expected["value"] is None else None
    elif mutation == "external_credit_promoted":
        candidate["external_credit"] = True
    else:
        raise ValueError("UNKNOWN_MUTATION")
    return candidate


def _exact_fields(record, expected):
    return set(record) == {"operation", *expected}


def _format_vtt(total):
    hours, remainder = divmod(total, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, millis = divmod(remainder, 1_000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{millis:03d}"


def _vtt(record):
    if not _exact_fields(record, {"timestamp"}):
        return hold("FIELD_SET")
    value = record["timestamp"]
    if type(value) is not str:
        return hold("TIMESTAMP_TYPE")
    match = re.fullmatch(r"(?:(\d{2,3}):)?(\d{2}):(\d{2})\.(\d{3})", value)
    if not match:
        return hold("TIMESTAMP_SYNTAX")
    hours = int(match.group(1) or 0)
    minutes, seconds, millis = map(int, match.groups()[1:])
    if minutes >= 60 or seconds >= 60:
        return hold("TIMESTAMP_RANGE")
    total = ((hours * 60 + minutes) * 60 + seconds) * 1000 + millis
    return accept({"milliseconds": total, "normalized": _format_vtt(total)})


def _srt(record):
    if not _exact_fields(record, {"timestamp"}):
        return hold("FIELD_SET")
    value = record["timestamp"]
    if type(value) is not str:
        return hold("TIMESTAMP_TYPE")
    match = re.fullmatch(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})", value)
    if not match:
        return hold("TIMESTAMP_SYNTAX")
    hours, minutes, seconds, millis = map(int, match.groups())
    if minutes >= 60 or seconds >= 60:
        return hold("TIMESTAMP_RANGE")
    total = ((hours * 60 + minutes) * 60 + seconds) * 1000 + millis
    return accept({"milliseconds": total, "normalized": value})


def _cue_interval(record):
    if not _exact_fields(record, {"start_ms", "end_ms", "previous_end_ms"}):
        return hold("FIELD_SET")
    start, end, previous = record["start_ms"], record["end_ms"], record["previous_end_ms"]
    if type(start) is not int or type(end) is not int or (previous is not None and type(previous) is not int):
        return hold("INTEGER_TYPE")
    if previous is not None and previous < 0:
        return hold("PREVIOUS_END")
    if start < 0 or end > MAX_MILLISECONDS or start >= end:
        return hold("CUE_BOUNDS")
    if previous is None:
        relation, gap = "initial", None
    elif start < previous:
        return hold("CUE_OVERLAP")
    elif start == previous:
        relation, gap = "touching", 0
    else:
        relation, gap = "gap", start - previous
    return accept({"duration_ms": end - start, "gap_ms": gap, "relation": relation})


def _frame_timebase(record):
    if set(record) - {"operation", "mode", "rate_num", "rate_den", "frame", "seconds"}:
        return hold("FIELD_SET")
    if not {"operation", "mode", "rate_num", "rate_den"} <= set(record):
        return hold("FIELD_SET")
    mode, numerator, denominator = record["mode"], record["rate_num"], record["rate_den"]
    if mode not in {"to_seconds", "to_frame"}:
        return hold("MODE")
    expected = {"operation", "mode", "rate_num", "rate_den", "frame" if mode == "to_seconds" else "seconds"}
    if set(record) != expected:
        return hold("FIELD_SET")
    if type(numerator) is not int or type(denominator) is not int:
        return hold("INTEGER_TYPE")
    if numerator <= 0 or denominator <= 0:
        return hold("RATE")
    if mode == "to_seconds":
        frame = record["frame"]
        if type(frame) is not int:
            return hold("INTEGER_TYPE")
        if frame < 0 or frame > MAX_FRAME:
            return hold("FRAME")
        seconds = Fraction(frame * denominator, numerator)
        return accept({"frame": frame, "seconds": str(seconds)})
    seconds_text = record["seconds"]
    if type(seconds_text) is not str or not re.fullmatch(r"\d+(?:/\d+)?", seconds_text):
        return hold("RATIONAL_SYNTAX")
    seconds = Fraction(seconds_text)
    frame = seconds * numerator / denominator
    if frame.denominator != 1:
        return hold("OFF_FRAME_GRID")
    if frame < 0 or frame > MAX_FRAME:
        return hold("FRAME")
    return accept({"frame": int(frame), "seconds": str(seconds)})


def _cue_order(record):
    if not _exact_fields(record, {"cues"}):
        return hold("FIELD_SET")
    cues = record["cues"]
    if type(cues) is not list or len(cues) > 32:
        return hold("CUE_ARRAY")
    parsed = []
    for cue in cues:
        if type(cue) is not list or len(cue) != 2 or any(type(value) is not int for value in cue):
            return hold("CUE_TYPE")
        start, end = cue
        if start < 0 or end > MAX_MILLISECONDS or start >= end:
            return hold("CUE_BOUNDS")
        if parsed and start < parsed[-1][1]:
            return hold("CUE_OVERLAP")
        parsed.append([start, end])
    gaps = [[parsed[index - 1][1], parsed[index][0]] for index in range(1, len(parsed)) if parsed[index][0] > parsed[index - 1][1]]
    span = None if not parsed else [parsed[0][0], parsed[-1][1]]
    return accept({"cue_count": len(parsed), "gaps": gaps, "span": span})


def _payload(record):
    if not _exact_fields(record, {"mode", "lines"}):
        return hold("FIELD_SET")
    mode, lines = record["mode"], record["lines"]
    if mode not in {"caption", "transcript"}:
        return hold("MODE")
    if type(lines) is not list or len(lines) > 8:
        return hold("LINE_ARRAY")
    if any(type(line) is not str for line in lines):
        return hold("LINE_TYPE")
    if any(len(line) > 200 for line in lines):
        return hold("LINE_LENGTH")
    if any(any(ord(character) < 32 for character in line) for line in lines):
        return hold("CONTROL_CHARACTER")
    markup = any(re.search(r"<[^>]+>", line) for line in lines)
    return accept(
        {
            "mode": mode,
            "line_count": len(lines),
            "character_count": sum(len(line) for line in lines),
            "empty_line_indices": [index for index, line in enumerate(lines) if line == ""],
            "markup_detected": markup,
            "speaker_identity_established": False,
        }
    )


def _canonical_language_tag(tag):
    pieces = tag.split("-")
    result = [pieces[0].lower()]
    for piece in pieces[1:]:
        if len(piece) == 4:
            result.append(piece.title())
        elif len(piece) == 2:
            result.append(piece.upper())
        else:
            result.append(piece)
    return "-".join(result)


def _language(record):
    if not _exact_fields(record, {"tag"}):
        return hold("FIELD_SET")
    tag = record["tag"]
    if type(tag) is not str:
        return hold("LANGUAGE_TAG_TYPE")
    if tag.startswith("x-") or "-u-" in tag:
        return hold("LANGUAGE_TAG_PROFILE")
    if not re.fullmatch(r"[A-Za-z]{2,3}(?:-[A-Za-z]{4})?(?:-(?:[A-Za-z]{2}|\d{3}))?", tag):
        return hold("LANGUAGE_TAG_SYNTAX")
    return accept({"canonical": _canonical_language_tag(tag), "language_authority_established": False})


def _derivative(record):
    fields = {"source_ref", "derivative_ref", "source_sha256", "derivative_sha256", "relation", "synthetic"}
    if not _exact_fields(record, fields):
        return hold("FIELD_SET")
    source, derivative = record["source_ref"], record["derivative_ref"]
    if type(source) is not str or type(derivative) is not str or not 1 <= len(source) <= 128 or not 1 <= len(derivative) <= 128:
        return hold("REFERENCE_SHAPE")
    if source == derivative:
        return hold("REFERENCE_COLLISION")
    if record["relation"] not in RELATIONS:
        return hold("RELATION")
    if not all(type(record[key]) is str and re.fullmatch(r"[0-9a-f]{64}", record[key]) for key in ["source_sha256", "derivative_sha256"]):
        return hold("DIGEST_SYNTAX")
    if record["synthetic"] is not True:
        return hold("REAL_SOURCE_AUTHORITY_REQUIRED")
    return accept(
        {
            "source_ref": source,
            "derivative_ref": derivative,
            "relation": record["relation"],
            "source_sha256": record["source_sha256"],
            "derivative_sha256": record["derivative_sha256"],
            "custody_or_rights_established": False,
        }
    )


def _accessibility(record):
    fields = {"features", "claim_complete", "manual_review", "affected_user_review", "assistive_technology_review", "language_review"}
    if not _exact_fields(record, fields):
        return hold("FIELD_SET")
    features = record["features"]
    flags = [record[key] for key in fields - {"features"}]
    if type(features) is not list or any(type(item) is not str or item not in ACCESS_FEATURES for item in features) or any(type(flag) is not bool for flag in flags):
        return hold("ACCESSIBILITY_SHAPE")
    if record["claim_complete"]:
        return hold("EXTERNAL_ACCESSIBILITY_EVIDENCE_REQUIRED")
    return accept(
        {
            "features": features,
            "disposition": "represented",
            "missing_evidence": ["manual_review", "affected_user_review", "assistive_technology_review", "language_review"],
            "accessibility_complete": False,
        }
    )


def _publication(record):
    if not _exact_fields(record, {"action", "source_kind", "claimed_authorities"}):
        return hold("FIELD_SET")
    action = record["action"]
    if action == "resolve_unknown_rights":
        return hold("MISSING_RIGHTS_EVIDENCE")
    if action == "resolve_unknown_language_authority":
        return hold("MISSING_LANGUAGE_AUTHORITY")
    if action not in PUBLICATION_REQUIREMENTS:
        return hold("ACTION")
    if record["source_kind"] != "synthetic" or record["claimed_authorities"] != PUBLICATION_REQUIREMENTS[action]:
        return hold("AUTHORITY_SHAPE")
    return accept(
        {
            "action": action,
            "disposition": "exact_gate",
            "executed_external_action": False,
            "required_authorities": PUBLICATION_REQUIREMENTS[action],
        }
    )


EVALUATORS = {
    "vtt_timestamp": _vtt,
    "srt_timestamp": _srt,
    "cue_interval": _cue_interval,
    "frame_timebase": _frame_timebase,
    "cue_order": _cue_order,
    "payload_text": _payload,
    "language_tag": _language,
    "derivative_linkage": _derivative,
    "accessibility_claim": _accessibility,
    "publication_gate": _publication,
}


def evaluate(record):
    before = copy.deepcopy(record)
    if type(record) is not dict:
        return hold("RECORD_TYPE")
    operation = record.get("operation")
    result = EVALUATORS.get(operation, lambda _: hold("OPERATION"))(record)
    if not exact_type_equal(record, before):
        raise RuntimeError("INPUT_MUTATED")
    return result


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("DUPLICATE_JSON_KEY")
            result[key] = value
        return result

    def constant(_):
        raise ValueError("NONFINITE_JSON_CONSTANT")

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)


def main(allowed_operations=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str)
    args = parser.parse_args()
    try:
        record = strict_json(open(args.input, encoding="utf-8").read())
        if allowed_operations is not None and record.get("operation") not in allowed_operations:
            result = hold("OPERATION_SCOPE")
        else:
            result = evaluate(record)
    except (OSError, UnicodeError, ValueError) as error:
        code = str(error) if str(error) in {"DUPLICATE_JSON_KEY", "NONFINITE_JSON_CONSTANT"} else "INPUT_DOCUMENT"
        result = hold(code)
    print(json.dumps(result, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":")))
    return 0 if result["accepted"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
