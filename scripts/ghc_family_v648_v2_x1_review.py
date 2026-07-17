#!/usr/bin/env python3
"""Validate the Sylven Arc v648-v2 x1-only packet."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "ghc_family_v648_v1_x1_review.py"


def transformed_source() -> str:
    source = TEMPLATE.read_text(encoding="utf-8")
    replacements = [
        ("ghc_family_v648_v1_definitions", "ghc_family_v648_v2_definitions"),
        ("Tamar Vey", "Sylven Arc"),
        ("v648-v1", "v648-v2"),
        ("v648_v1", "v648_v2"),
        ("V6481", "V6482"),
        ("prior_frozen_550", "prior_frozen_560"),
        ("frozen_after_560", "frozen_after_570"),
        ('proposals["frozen_chain_count_after_x1"] == 560', 'proposals["frozen_chain_count_after_x1"] == 570'),
    ]
    for old, new in replacements:
        source = source.replace(old, new)
    return source


def main() -> int:
    namespace = {"__name__": "ghc_family_v648_v2_x1_review_template", "__file__": str(Path(__file__).resolve())}
    exec(compile(transformed_source(), str(Path(__file__).resolve()), "exec"), namespace)
    return int(namespace["main"]())


if __name__ == "__main__":
    raise SystemExit(main())
