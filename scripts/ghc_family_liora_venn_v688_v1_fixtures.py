"""Planning-only caption evidence fixtures; no runtime evaluator lives here."""
from __future__ import annotations

import copy
import hashlib
import json
import re
from collections import Counter
from fractions import Fraction

CASES: list[dict] = []


def accept(value):
    return {"accepted": True, "value": value, "error": None, "external_credit": False}


def hold(code):
    return {"accepted": False, "value": None, "error": code, "external_credit": False}


def add(operation, title, payload, expected, disposition="completed"):
    CASES.append(
        {
            "proposal_id": f"LV6881-N{len(CASES) + 1:03d}",
            "operation": operation,
            "title": title,
            "input": {"operation": operation, **payload},
            "expected_output": expected,
            "expected_execution_disposition": disposition,
        }
    )


def format_milliseconds(total):
    hours, remainder = divmod(total, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, millis = divmod(remainder, 1_000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{millis:03d}"


def vtt_timestamp_cases():
    op = "vtt_timestamp"
    valid = [
        ("Zero WebVTT timestamp remains exact", "00:00.000", 0),
        ("One millisecond uses three fractional digits", "00:00:00.001", 1),
        ("Minute-second form normalizes with an hour field", "01:02.003", 62_003),
        ("Explicit hour form preserves its hour", "01:02:03.004", 3_723_004),
        ("Fifty-nine seconds remains below the minute boundary", "00:59.999", 59_999),
        ("Ten minutes does not become ten hours", "10:00.000", 600_000),
        ("Ten seconds preserves a leading hour field", "00:00:10.010", 10_010),
        ("Large WebVTT hours remain integer metadata", "123:45:06.007", 445_506_007),
        ("Sixty-one minutes normalizes through explicit hours", "01:01:00.000", 3_660_000),
        ("Last bounded millisecond remains exact", "999:59:59.999", 3_599_999_999),
    ]
    for title, text, total in valid:
        add(op, title, {"timestamp": text}, accept({"milliseconds": total, "normalized": format_milliseconds(total)}))
    invalid = [
        ("Empty timestamp is refused", "", "TIMESTAMP_SYNTAX"),
        ("One-digit minute field is outside the profile", "0:00.000", "TIMESTAMP_SYNTAX"),
        ("Minute sixty is not normalized implicitly", "00:60.000", "TIMESTAMP_RANGE"),
        ("Second sixty is outside a minute", "00:00:60.000", "TIMESTAMP_RANGE"),
        ("Four fractional digits are not rounded", "00:00.1000", "TIMESTAMP_SYNTAX"),
        ("Comma decimal belongs to a different format", "00:00,000", "TIMESTAMP_SYNTAX"),
        ("Negative WebVTT time is refused", "-00:01.000", "TIMESTAMP_SYNTAX"),
        ("Leading whitespace is not discarded", " 00:01.000", "TIMESTAMP_SYNTAX"),
        ("Boolean timestamp is not textual timing", True, "TIMESTAMP_TYPE"),
        ("Numeric timestamp is not coerced to text", 1000, "TIMESTAMP_TYPE"),
    ]
    for title, text, code in invalid:
        add(op, title, {"timestamp": text}, hold(code))


def srt_timestamp_cases():
    op = "srt_timestamp"
    valid = [
        ("Zero SubRip timestamp remains exact", "00:00:00,000", 0),
        ("One SubRip millisecond remains exact", "00:00:00,001", 1),
        ("One second uses comma precision", "00:00:01,000", 1_000),
        ("Minute transition stays explicit", "00:01:00,000", 60_000),
        ("Hour transition stays explicit", "01:00:00,000", 3_600_000),
        ("Mixed SubRip fields retain all units", "12:34:56,789", 45_296_789),
        ("Ninety-nine hours stays in the bounded profile", "99:59:59,999", 359_999_999),
        ("Ten milliseconds retain leading zeros", "00:00:00,010", 10),
        ("Hundred milliseconds retain leading zeros", "00:00:00,100", 100),
        ("A day is represented as twenty-four hours", "24:00:00,000", 86_400_000),
    ]
    for title, text, total in valid:
        hours, rem = divmod(total, 3_600_000)
        minutes, rem = divmod(rem, 60_000)
        seconds, millis = divmod(rem, 1_000)
        normalized = f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"
        add(op, title, {"timestamp": text}, accept({"milliseconds": total, "normalized": normalized}))
    invalid = [
        ("Empty SubRip timestamp is refused", "", "TIMESTAMP_SYNTAX"),
        ("SubRip requires an hour field", "00:01,000", "TIMESTAMP_SYNTAX"),
        ("SubRip minutes may not reach sixty", "00:60:00,000", "TIMESTAMP_RANGE"),
        ("SubRip seconds may not reach sixty", "00:00:60,000", "TIMESTAMP_RANGE"),
        ("SubRip uses a comma not a period", "00:00:01.000", "TIMESTAMP_SYNTAX"),
        ("Two fractional digits are not padded", "00:00:01,00", "TIMESTAMP_SYNTAX"),
        ("Three-digit hours exceed this profile", "100:00:00,000", "TIMESTAMP_SYNTAX"),
        ("A sign is not a timestamp field", "+00:00:00,000", "TIMESTAMP_SYNTAX"),
        ("Null SubRip time is not text", None, "TIMESTAMP_TYPE"),
        ("Floating SubRip time is not coerced", 1.5, "TIMESTAMP_TYPE"),
    ]
    for title, text, code in invalid:
        add(op, title, {"timestamp": text}, hold(code))


def cue_interval_cases():
    op = "cue_interval"
    valid = [
        ("First cue has no predecessor relation", 0, 1000, None, "initial", None),
        ("Touching cue starts at the prior endpoint", 1000, 2000, 1000, "touching", 0),
        ("One-millisecond gap remains visible", 1001, 2000, 1000, "gap", 1),
        ("Large cue positions retain integer precision", 3_600_000, 3_605_000, 3_599_999, "gap", 1),
        ("Single-millisecond cue remains nonempty", 4, 5, 0, "gap", 4),
        ("Long bounded cue is represented", 0, 86_400_000, None, "initial", None),
        ("A ten-second gap is not collapsed", 20_000, 21_000, 10_000, "gap", 10_000),
        ("Cue duration is independent from predecessor gap", 9000, 9500, 8000, "gap", 1000),
        ("Zero predecessor endpoint is explicit", 1, 2, 0, "gap", 1),
        ("Maximum bounded endpoint remains representable", 86_399_999, 86_400_000, 86_399_999, "touching", 0),
    ]
    for title, start, end, previous, relation, gap in valid:
        add(op, title, {"start_ms": start, "end_ms": end, "previous_end_ms": previous}, accept({"duration_ms": end - start, "gap_ms": gap, "relation": relation}))
    invalid = [
        ("Negative cue start is refused", -1, 10, None, "CUE_BOUNDS"),
        ("Empty cue interval is refused", 10, 10, None, "CUE_BOUNDS"),
        ("Reversed cue interval is refused", 11, 10, None, "CUE_BOUNDS"),
        ("Cue endpoint exceeds one-day bound", 0, 86_400_001, None, "CUE_BOUNDS"),
        ("Cue overlap is never silently reordered", 9, 12, 10, "CUE_OVERLAP"),
        ("Negative predecessor endpoint is refused", 1, 2, -1, "PREVIOUS_END"),
        ("Boolean cue start is not integer time", True, 10, None, "INTEGER_TYPE"),
        ("Floating cue endpoint is not rounded", 0, 1.0, None, "INTEGER_TYPE"),
        ("Text predecessor is not integer time", 1, 2, "0", "INTEGER_TYPE"),
        ("Extra cue policy fields require a new profile", 0, 1, None, "FIELD_SET", {"allow_overlap": True}),
    ]
    for row in invalid:
        title, start, end, previous, code, *extra = row
        payload = {"start_ms": start, "end_ms": end, "previous_end_ms": previous}
        if extra:
            payload.update(extra[0])
        add(op, title, payload, hold(code))


def frame_timebase_cases():
    op = "frame_timebase"
    valid = [
        ("Frame zero at twenty-four fps is zero", "to_seconds", 24, 1, 0, None),
        ("Frame one at twenty-four fps stays rational", "to_seconds", 24, 1, 1, None),
        ("NTSC-style ratio retains denominator", "to_seconds", 30000, 1001, 30000, None),
        ("A thousand frames at twenty-five fps is exact", "to_seconds", 25, 1, 1000, None),
        ("One second maps to twenty-five frames", "to_frame", 25, 1, None, "1"),
        ("NTSC-style second mapping stays on grid", "to_frame", 30000, 1001, None, "1001/1000"),
        ("Half second maps at fifty fps", "to_frame", 50, 1, None, "1/2"),
        ("Large frame index keeps integer arithmetic", "to_seconds", 24000, 1001, 1_000_000, None),
        ("Equivalent time fraction normalizes", "to_frame", 30, 1, None, "2/2"),
        ("Film-rate ten seconds maps exactly", "to_frame", 24, 1, None, "10"),
    ]
    for title, mode, num, den, frame, seconds in valid:
        if mode == "to_seconds":
            value = Fraction(frame * den, num)
            expected = {"frame": frame, "seconds": str(value)}
            payload = {"mode": mode, "rate_num": num, "rate_den": den, "frame": frame}
        else:
            value = Fraction(seconds)
            expected = {"frame": int(value * num / den), "seconds": str(value)}
            payload = {"mode": mode, "rate_num": num, "rate_den": den, "seconds": seconds}
        add(op, title, payload, accept(expected))
    invalid = [
        ("Zero rate numerator is refused", {"mode": "to_seconds", "rate_num": 0, "rate_den": 1, "frame": 1}, "RATE"),
        ("Zero rate denominator is refused", {"mode": "to_seconds", "rate_num": 24, "rate_den": 0, "frame": 1}, "RATE"),
        ("Negative frame number is refused", {"mode": "to_seconds", "rate_num": 24, "rate_den": 1, "frame": -1}, "FRAME"),
        ("Boolean frame number is not an integer", {"mode": "to_seconds", "rate_num": 24, "rate_den": 1, "frame": True}, "INTEGER_TYPE"),
        ("Floating rate is not rounded", {"mode": "to_seconds", "rate_num": 29.97, "rate_den": 1, "frame": 1}, "INTEGER_TYPE"),
        ("Off-grid inverse time is refused", {"mode": "to_frame", "rate_num": 24, "rate_den": 1, "seconds": "1/100"}, "OFF_FRAME_GRID"),
        ("Decimal time text is outside rational syntax", {"mode": "to_frame", "rate_num": 24, "rate_den": 1, "seconds": "0.5"}, "RATIONAL_SYNTAX"),
        ("Unknown frame conversion mode is refused", {"mode": "round", "rate_num": 24, "rate_den": 1, "frame": 1}, "MODE"),
        ("Frame ceiling is enforced", {"mode": "to_seconds", "rate_num": 24, "rate_den": 1, "frame": 1_000_000_001}, "FRAME"),
        ("Extra drop-frame flag requires a declared profile", {"mode": "to_seconds", "rate_num": 30000, "rate_den": 1001, "frame": 1, "drop_frame": True}, "FIELD_SET"),
    ]
    for title, payload, code in invalid:
        add(op, title, payload, hold(code))


def cue_order_cases():
    op = "cue_order"
    valid = [
        ("Empty cue sequence invents no duration", []),
        ("Single cue has no internal gap", [[0, 1000]]),
        ("Touching cues retain source order", [[0, 1000], [1000, 2000]]),
        ("Separated cues expose one gap", [[0, 500], [1000, 1500]]),
        ("Three cues expose two gaps", [[0, 100], [200, 300], [500, 800]]),
        ("Millisecond cues remain addressable", [[0, 1], [2, 3]]),
        ("Late-start sequence preserves leading vacancy", [[5000, 6000]]),
        ("Long sequence remains within one-day bound", [[0, 1000], [86_399_000, 86_400_000]]),
        ("Mixed touching and gaps stay distinct", [[0, 10], [10, 20], [25, 30]]),
        ("Thirty-two cues meet the sequence ceiling", [[i * 2, i * 2 + 1] for i in range(32)]),
    ]
    for title, cues in valid:
        gaps = [[cues[i - 1][1], cues[i][0]] for i in range(1, len(cues)) if cues[i][0] > cues[i - 1][1]]
        span = None if not cues else [cues[0][0], cues[-1][1]]
        add(op, title, {"cues": cues}, accept({"cue_count": len(cues), "gaps": gaps, "span": span}))
    invalid = [
        ("Overlapping cues are refused", [[0, 10], [9, 20]], "CUE_OVERLAP"),
        ("Reverse-ordered cues are refused", [[10, 20], [0, 5]], "CUE_OVERLAP"),
        ("Empty cue spans are refused", [[1, 1]], "CUE_BOUNDS"),
        ("Negative cue sequence positions are refused", [[-1, 1]], "CUE_BOUNDS"),
        ("Past-day cue positions are refused", [[0, 86_400_001]], "CUE_BOUNDS"),
        ("Boolean cue endpoints are not integers", [[False, 1]], "CUE_TYPE"),
        ("Cue triples are not silently truncated", [[0, 1, 2]], "CUE_TYPE"),
        ("Scalar cue sequence is refused", 1, "CUE_ARRAY"),
        ("Null cue sequence is refused", None, "CUE_ARRAY"),
        ("Thirty-three cues exceed the bound", [[i * 2, i * 2 + 1] for i in range(33)], "CUE_ARRAY"),
    ]
    for title, cues, code in invalid:
        add(op, title, {"cues": cues}, hold(code))


def payload_text_cases():
    op = "payload_text"
    valid = [
        ("Single caption line is preserved", "caption", ["Synthetic caption"]),
        ("Two explicit lines retain their break", "caption", ["First line", "Second line"]),
        ("Empty line remains explicit metadata", "caption", ["", "After vacancy"]),
        ("Unicode text is retained without identity inference", "caption", ["Kia ora — synthetic only"]),
        ("Literal emphasis markup is detected but not rendered", "caption", ["<i>synthetic</i>"]),
        ("Voice syntax is text rather than speaker evidence", "caption", ["<v speaker-a>Placeholder"]),
        ("Transcript mode preserves paragraph fragments", "transcript", ["Segment A", "Segment B"]),
        ("Punctuation remains byte-visible text", "transcript", ["[music]", "— pause —"]),
        ("Eight lines meet the bounded payload ceiling", "caption", [str(i) for i in range(8)]),
        ("Combining characters remain caller-supplied text", "transcript", ["e\u0301"]),
    ]
    for title, mode, lines in valid:
        markup = any(re.search(r"<[^>]+>", line) for line in lines)
        add(op, title, {"mode": mode, "lines": lines}, accept({"mode": mode, "line_count": len(lines), "character_count": sum(len(x) for x in lines), "empty_line_indices": [i for i, x in enumerate(lines) if x == ""], "markup_detected": markup, "speaker_identity_established": False}))
    invalid = [
        ("Unknown payload mode is refused", "notes", ["x"], "MODE"),
        ("Scalar payload is refused", "caption", "x", "LINE_ARRAY"),
        ("Nine lines exceed the payload ceiling", "caption", [str(i) for i in range(9)], "LINE_ARRAY"),
        ("Numeric payload lines are not coerced", "caption", [1], "LINE_TYPE"),
        ("Boolean payload lines are not text", "caption", [True], "LINE_TYPE"),
        ("Overlong payload line is refused", "caption", ["x" * 201], "LINE_LENGTH"),
        ("Null payload line is refused", "transcript", [None], "LINE_TYPE"),
        ("Control NUL stays outside the profile", "caption", ["a\u0000b"], "CONTROL_CHARACTER"),
        ("Carriage return inside a line is refused", "caption", ["a\rb"], "CONTROL_CHARACTER"),
        ("Extra rendering instruction requires a new profile", "caption", ["x"], "FIELD_SET", {"render": True}),
    ]
    for row in invalid:
        title, mode, lines, code, *extra = row
        payload = {"mode": mode, "lines": lines}
        if extra:
            payload.update(extra[0])
        add(op, title, payload, hold(code))


def canonical_language_tag(tag):
    parts = tag.split("-")
    result = [parts[0].lower()]
    for part in parts[1:]:
        if len(part) == 4:
            result.append(part.title())
        elif len(part) == 2:
            result.append(part.upper())
        else:
            result.append(part)
    return "-".join(result)


def language_tag_cases():
    op = "language_tag"
    for title, tag in [
        ("English primary language canonicalizes lowercase", "EN"),
        ("Te reo Maori tag remains a metadata label", "mi"),
        ("New Zealand region canonicalizes uppercase", "en-nz"),
        ("Script subtag canonicalizes title case", "zh-hant"),
        ("Script and region retain their roles", "zh-hant-tw"),
        ("Serbian Latin script and region remain distinct", "sr-latn-rs"),
        ("French Canadian region stays explicit", "fr-ca"),
        ("Numeric macro-region remains numeric", "es-419"),
        ("Undetermined language remains an explicit vacancy", "und"),
        ("Three-letter language with region stays bounded", "fil-ph"),
    ]:
        add(op, title, {"tag": tag}, accept({"canonical": canonical_language_tag(tag), "language_authority_established": False}))
    invalid = [
        ("Empty language tag is refused", "", "LANGUAGE_TAG_SYNTAX"),
        ("Underscore separators are not BCP47 syntax", "en_NZ", "LANGUAGE_TAG_SYNTAX"),
        ("One-letter primary language is refused", "e", "LANGUAGE_TAG_SYNTAX"),
        ("Four-letter primary language is outside this profile", "abcd", "LANGUAGE_TAG_SYNTAX"),
        ("Private-use tags need a separate profile", "x-test", "LANGUAGE_TAG_PROFILE"),
        ("Extension subtags need a separate profile", "en-u-ca-gregory", "LANGUAGE_TAG_PROFILE"),
        ("Repeated region-like subtags are refused", "en-NZ-US", "LANGUAGE_TAG_SYNTAX"),
        ("Whitespace is not silently trimmed", " en", "LANGUAGE_TAG_SYNTAX"),
        ("Boolean language tag is not text", False, "LANGUAGE_TAG_TYPE"),
        ("Numeric language tag is not coerced", 64, "LANGUAGE_TAG_TYPE"),
    ]
    for title, tag, code in invalid:
        add(op, title, {"tag": tag}, hold(code))


def derivative_linkage_cases():
    op = "derivative_linkage"
    sha = lambda text: hashlib.sha256(text.encode("utf-8")).hexdigest()
    relations = ["caption_of", "transcript_of", "description_of"]
    for index in range(10):
        source = f"synthetic-source-{index}"
        derivative = f"synthetic-derivative-{index}"
        relation = relations[index % len(relations)]
        payload = {"source_ref": source, "derivative_ref": derivative, "source_sha256": sha(source), "derivative_sha256": sha(derivative), "relation": relation, "synthetic": True}
        add(op, f"Derivative linkage {index + 1} preserves distinct synthetic roles", payload, accept({"source_ref": source, "derivative_ref": derivative, "relation": relation, "source_sha256": sha(source), "derivative_sha256": sha(derivative), "custody_or_rights_established": False}))
    base = {"source_ref": "synthetic-source", "derivative_ref": "synthetic-derivative", "source_sha256": sha("synthetic-source"), "derivative_sha256": sha("synthetic-derivative"), "relation": "caption_of", "synthetic": True}
    invalid = [
        ("Source and derivative identities may not collapse", {"derivative_ref": "synthetic-source"}, "REFERENCE_COLLISION"),
        ("Empty source reference is refused", {"source_ref": ""}, "REFERENCE_SHAPE"),
        ("Empty derivative reference is refused", {"derivative_ref": ""}, "REFERENCE_SHAPE"),
        ("Overlong reference is refused", {"source_ref": "x" * 129}, "REFERENCE_SHAPE"),
        ("Unsupported derivative relation is refused", {"relation": "owns"}, "RELATION"),
        ("Uppercase digest needs an explicit profile", {"source_sha256": sha("synthetic-source").upper()}, "DIGEST_SYNTAX"),
        ("Short derivative digest is refused", {"derivative_sha256": "ab"}, "DIGEST_SYNTAX"),
        ("Nonsynthetic linkage requires external evidence", {"synthetic": False}, "REAL_SOURCE_AUTHORITY_REQUIRED"),
        ("Boolean source reference is not text", {"source_ref": True}, "REFERENCE_SHAPE"),
        ("Extra ownership field is not silently accepted", {"owner": "unknown"}, "FIELD_SET"),
    ]
    for title, patch, code in invalid:
        add(op, title, dict(base, **patch), hold(code))


def accessibility_claim_cases():
    op = "accessibility_claim"
    feature_sets = [
        ["captions"], ["transcript"], ["audio_description"], ["captions", "transcript"],
        ["captions", "audio_description"], ["transcript", "audio_description"],
        ["captions", "transcript", "audio_description"], ["chapters"],
        ["captions", "chapters"], ["transcript", "chapters"], ["sign_language"],
        ["captions", "sign_language"], ["easy_read_summary"], ["captions", "easy_read_summary"],
    ]
    for index, features in enumerate(feature_sets, 1):
        missing = ["manual_review", "affected_user_review", "assistive_technology_review", "language_review"]
        add(op, f"Accessibility feature set {index} remains a structural representation", {"features": features, "claim_complete": False, "manual_review": False, "affected_user_review": False, "assistive_technology_review": False, "language_review": False}, accept({"features": features, "disposition": "represented", "missing_evidence": missing, "accessibility_complete": False}), "represented")
    for index, features in enumerate(feature_sets[:6], 1):
        add(op, f"Completeness claim {index} remains an external evidence gap", {"features": features, "claim_complete": True, "manual_review": False, "affected_user_review": False, "assistive_technology_review": False, "language_review": False}, hold("EXTERNAL_ACCESSIBILITY_EVIDENCE_REQUIRED"), "open_gap")


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


def publication_gate_cases():
    op = "publication_gate"
    for action, required in PUBLICATION_REQUIREMENTS.items():
        title = "Caption publication hold " + action.replace("_", " ") + ": named outside-authority vacancy"
        if action == "release_maori_data":
            title = "Caption derivative sharing quarantine: Māori data governance vacancy"
        add(op, title, {"action": action, "source_kind": "synthetic", "claimed_authorities": required}, accept({"action": action, "disposition": "exact_gate", "executed_external_action": False, "required_authorities": required}), "exact_gate")
    add(op, "Unknown rights state remains an evidence gap", {"action": "resolve_unknown_rights", "source_kind": "synthetic", "claimed_authorities": []}, hold("MISSING_RIGHTS_EVIDENCE"), "open_gap")
    add(op, "Unknown language authority remains an evidence gap", {"action": "resolve_unknown_language_authority", "source_kind": "synthetic", "claimed_authorities": []}, hold("MISSING_LANGUAGE_AUTHORITY"), "open_gap")


def build_cases():
    CASES.clear()
    for builder in [vtt_timestamp_cases, srt_timestamp_cases, cue_interval_cases, frame_timebase_cases, cue_order_cases, payload_text_cases, language_tag_cases, derivative_linkage_cases, accessibility_claim_cases, publication_gate_cases]:
        builder()
    counts = Counter(c["operation"] for c in CASES)
    outcomes = Counter(c["expected_execution_disposition"] for c in CASES)
    assert len(CASES) == 200 and set(counts.values()) == {20}, counts
    assert outcomes == {"completed": 160, "represented": 14, "open_gap": 8, "exact_gate": 18}, outcomes
    assert len({json.dumps(c["input"], sort_keys=True, ensure_ascii=False) for c in CASES}) == 200
    return copy.deepcopy(CASES)


if __name__ == "__main__":
    rows = build_cases()
    print(json.dumps({"planning_only": True, "proposals": len(rows), "operations": dict(Counter(c["operation"] for c in rows)), "outcomes": dict(Counter(c["expected_execution_disposition"] for c in rows))}, sort_keys=True))
