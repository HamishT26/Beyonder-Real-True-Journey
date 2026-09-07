"""Verify Liora's three isolated, hash-locked caption package additions."""
from __future__ import annotations

import argparse
import importlib.metadata
import io
import json
from pathlib import Path

import langcodes
import pysubs2
import webvtt


EXPECTED = {"webvtt-py": "0.5.1", "pysubs2": "1.9.0", "langcodes": "3.5.1"}


def vtt_milliseconds(value):
    hours, minutes, remainder = value.split(":")
    seconds, milliseconds = remainder.split(".")
    return ((int(hours) * 60 + int(minutes)) * 60 + int(seconds)) * 1000 + int(milliseconds)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()

    installed = {
        distribution.metadata["Name"]: distribution.version
        for distribution in importlib.metadata.distributions()
    }
    selected = {name: installed[name] for name in EXPECTED}
    assert selected == EXPECTED, selected
    assert set(installed) == set(EXPECTED), installed

    vtt = webvtt.from_buffer(
        io.StringIO(
            "WEBVTT\n\n00:00:00.000 --> 00:00:01.250\nSynthetic A\n\n"
            "00:00:01.250 --> 00:00:02.500\nSynthetic B\n"
        )
    )
    assert len(vtt) == 2
    vtt_bounds = [
        [vtt_milliseconds(cue.start), vtt_milliseconds(cue.end)] for cue in vtt
    ]
    assert vtt_bounds == [[0, 1250], [1250, 2500]]
    malformed_vtt = webvtt.from_buffer(io.StringIO("WEBVTT\n\nBAD --> TIME\nSynthetic\n"))
    assert len(malformed_vtt) == 0

    subtitles = pysubs2.SSAFile.from_string(
        "1\n00:00:00,000 --> 00:00:01,250\nSynthetic A\n\n"
        "2\n00:00:01,250 --> 00:00:02,500\nSynthetic B\n",
        format_="srt",
    )
    assert [(event.start, event.end) for event in subtitles] == [(0, 1250), (1250, 2500)]
    reparsed = pysubs2.SSAFile.from_string(subtitles.to_string("srt"), format_="srt")
    assert [(event.start, event.end) for event in reparsed] == [(0, 1250), (1250, 2500)]
    try:
        pysubs2.SSAFile.from_string("synthetic", format_="unsupported")
    except Exception as error:
        pysubs2_rejection = type(error).__name__
    else:
        raise AssertionError("UNSUPPORTED_FORMAT_ACCEPTED")

    assert langcodes.standardize_tag("en-nz") == "en-NZ"
    assert langcodes.standardize_tag("zh-hant-tw") == "zh-Hant-TW"
    assert langcodes.tag_is_valid("en--NZ") is False

    receipt = {
        "schema": "ghc.family.isolated-package-smoke.v1",
        "environment_scope": "new isolated Liora v688-v1 D-drive environment",
        "network_install": False,
        "host_environment_mutated": False,
        "selected_distributions": selected,
        "distribution_count": len(installed),
        "positive": {
            "webvtt-py": {"cue_count": 2, "timestamp_text_preserved": True, "millisecond_bounds": vtt_bounds},
            "pysubs2": {"event_count": 2, "roundtrip": True, "millisecond_bounds": [[0, 1250], [1250, 2500]]},
            "langcodes": {"en-nz": "en-NZ", "zh-hant-tw": "zh-Hant-TW"},
        },
        "adverse": {
            "webvtt-py": {"malformed_timing_cue_count": 0, "rejected_by_empty_parse": True},
            "pysubs2": {"unsupported_format_error": pysubs2_rejection},
            "langcodes": {"invalid_tag": "en--NZ", "accepted": False},
        },
        "scope_boundary": "Package parsing and metadata evidence only; no media, participant, accessibility-complete, production, legal, cultural, or authority claim.",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"state": "PACKAGE_SMOKES_PASS", "packages": 3, "positive": 3, "adverse": 3}, sort_keys=True))


if __name__ == "__main__":
    main()
