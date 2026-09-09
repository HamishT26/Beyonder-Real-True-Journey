#!/usr/bin/env python3
"""Bounded positive and rejecting smokes for Eiren's three D-first packages."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
from pathlib import Path


def check_pint() -> dict:
    import pint
    from pint.errors import DimensionalityError

    registry = pint.UnitRegistry()
    converted = (2 * registry.kilometre).to(registry.metre)
    positive = converted.magnitude == 2000 and str(converted.units) == "meter"
    rejected = False
    error = None
    try:
        (1 * registry.metre).to(registry.second)
    except DimensionalityError as exc:
        rejected = True
        error = type(exc).__name__
    return {"name": "Pint", "version": importlib.metadata.version("Pint"), "positive": positive, "rejecting": rejected, "rejecting_error": error}


def check_uncertainties() -> dict:
    from uncertainties import ufloat
    from uncertainties.core import NegativeStdDev

    left = ufloat(20, 4)
    right = ufloat(12, 3)
    result = left + right
    positive = result.nominal_value == 32 and result.std_dev == 5 and (left - left).std_dev == 0
    rejected = False
    error = None
    try:
        ufloat(1, -1)
    except NegativeStdDev as exc:
        rejected = True
        error = type(exc).__name__
    return {"name": "uncertainties", "version": importlib.metadata.version("uncertainties"), "positive": positive, "rejecting": rejected, "rejecting_error": error}


def check_pydoe3() -> dict:
    from pyDOE3 import ff2n, fullfact

    binary = ff2n(3)
    mixed = fullfact([2, 3])
    positive = binary.shape == (8, 3) and set(binary.reshape(-1)) == {-1.0, 1.0} and mixed.shape == (6, 2)
    rejected = False
    error = None
    try:
        ff2n("two")
    except (TypeError, ValueError) as exc:
        rejected = True
        error = type(exc).__name__
    return {"name": "pyDOE3", "version": importlib.metadata.version("pyDOE3"), "positive": positive, "rejecting": rejected, "rejecting_error": error}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    checks = [check_pint(), check_uncertainties(), check_pydoe3()]
    payload = {
        "schema": "ghc.family.package-smoke.v1",
        "owner": "Eiren Kestrel",
        "phase": "v689-v3",
        "checks": checks,
        "positive_passed": sum(row["positive"] for row in checks),
        "rejecting_passed": sum(row["rejecting"] for row in checks),
        "valid": all(row["positive"] and row["rejecting"] for row in checks),
        "real_measurements": 0,
        "boundary": "Synthetic API behavior only; not empirical measurement, professional validation, exhaustive security, legal advice, or production certification.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, sort_keys=True))
    raise SystemExit(0 if payload["valid"] else 1)


if __name__ == "__main__":
    main()
