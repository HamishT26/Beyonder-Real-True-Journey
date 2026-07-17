#!/usr/bin/env python3
"""Review staged v648-v2 closeout blobs and build the exact owner manifest."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "ghc_family_v648_v1_closeout_staged_review.py"


def transformed_source() -> str:
    source = TEMPLATE.read_text(encoding="utf-8")
    replacements = [
        ("Tamar Vey", "Sylven Arc"),
        ("docs/tamar-vey/v648-v1/", "docs/sylven-arc/v648-v2/"),
        ("v648-v1", "v648-v2"),
        ("v648_v1", "v648_v2"),
        ("V6481", "V6482"),
    ]
    for old, new in replacements:
        source = source.replace(old, new)
    return source


def main() -> int:
    namespace = {"__name__": "ghc_family_v648_v2_closeout_staged_review_template", "__file__": str(Path(__file__).resolve())}
    exec(compile(transformed_source(), str(Path(__file__).resolve()), "exec"), namespace)
    return int(namespace["main"]())


if __name__ == "__main__":
    raise SystemExit(main())
