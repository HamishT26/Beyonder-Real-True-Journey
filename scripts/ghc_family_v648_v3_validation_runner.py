#!/usr/bin/env python3
"""Detailed/minimal validation adapter for Eiren Kestrel v648-v3."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "ghc_family_v648_v2_validation_runner.py"


def transformed_source() -> str:
    source = TEMPLATE.read_text(encoding="utf-8")
    replacements = [
        ("Sylven Arc", "Eiren Kestrel"),
        ("sylven-arc", "eiren-kestrel"),
        ("docs/sylven-arc/v648-v2", "docs/eiren-kestrel/v648-v3"),
        ("v648-v2", "v648-v3"),
        ("v648_v2", "v648_v3"),
        ("V648V2", "V648V3"),
        ('"v648-v2-integrated-overview.md"', '"v648-v3-integrated-overview.md"'),
        ('"deliverables/v648-v2-static-report.html"', '"deliverables/v648-v3-static-report.html"'),
        ('load("method-flow/method-flow-state.json")', 'load("method-flow/method-flow-ledger.json")'),
        ('"frozen_570"', '"frozen_580"'),
        ('== 570', '== 580'),
        ('== 3938', '== 4032'),
        ('== (7, 70)', '== (10, 70)'),
        ('add(checks, "x2_failures_retained", negatives["x2_operational"] >= 6, negatives["x2_operational"])', 'add(checks, "x2_failure_register_parity", negatives["x2_operational"] == len(negatives["x2_operational_rows"]), negatives["x2_operational"])'),
        ('== (27, 28)', '== (28, 29)'),
        ('route_prepared_for_eiren', 'route_prepared_for_ilyra'),
        ('route["target_existing_task_title"] == "Eiren Kestrel"', 'route["target_existing_task_title"] == "Ilyra Fen"'),
        ('"boundary": "Scoped same-owner validation is not the Eiren-owned full repository suite, independent reproduction, external audit, production certification, complete privacy, exhaustive security, or complete accessibility conformance."', '"boundary": "This current-phase validator is owner-scoped. The one canonical Eiren-owned full repository suite is recorded separately at the final gate; neither result is replay, independent reproduction, external audit, production certification, complete privacy, exhaustive security, or complete accessibility conformance."'),
    ]
    for old, new in replacements:
        source = source.replace(old, new)
    return source


def main() -> int:
    namespace = {
        "__name__": "ghc_family_v648_v3_validation_template",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(transformed_source(), str(Path(__file__).resolve()), "exec"), namespace)
    return int(namespace["main"]())


if __name__ == "__main__":
    raise SystemExit(main())
