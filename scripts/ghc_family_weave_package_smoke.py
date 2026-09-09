#!/usr/bin/env python3
"""Bounded API smokes for the four hash-locked x1 wheels."""
from __future__ import annotations

from bitarray import bitarray
from more_itertools import run_length
import portion as P


def run() -> dict[str, object]:
    bits = bitarray("101001", endian="big")
    accepting = {
        "bitarray": bits.to01() == "101001" and bits.count(1) == 3,
        "portion": str(P.closed(0, 2) | P.openclosed(2, 4)) == "[0,4]",
        "more_itertools": list(run_length.encode("AABCCC"))
        == [("A", 2), ("B", 1), ("C", 3)],
    }
    rejecting: list[str] = []
    try:
        bitarray("10x")
    except ValueError:
        rejecting.append("bitarray_invalid_symbol")
    try:
        P.from_string("not-an-interval", int)
    except ValueError:
        rejecting.append("portion_malformed_interval")
    try:
        list(run_length.decode([("A", "bad")]))
    except TypeError:
        rejecting.append("more_itertools_nonnumeric_run")
    return {
        "accepting": accepting,
        "rejecting": rejecting,
        "unsafe_serialization_used": False,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), sort_keys=True))
