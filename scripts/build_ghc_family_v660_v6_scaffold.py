#!/usr/bin/env python3
"""Create the additive Lyren v660-v6 code scaffold from sealed v660-v5 files.

This is a bounded mechanical rewrite only. It refuses to overwrite targets,
does not execute a phase builder, and leaves all domain claims to the reviewed
v660-v6 data and validation contracts.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X1_PAIRS = (
    ("scripts/ghc_family_v660_v5_data.py", "scripts/ghc_family_v660_v6_data.py"),
    (
        "scripts/ghc_family_v660_v5_novelty_probe.py",
        "scripts/ghc_family_v660_v6_novelty_probe.py",
    ),
    ("scripts/build_ghc_family_v660_v5_x1.py", "scripts/build_ghc_family_v660_v6_x1.py"),
    ("tests/test_ghc_family_v660_v5_x1.py", "tests/test_ghc_family_v660_v6_x1.py"),
)
X2_PAIRS = (
    ("scripts/ghc_family_v660_v5_runtime.py", "scripts/ghc_family_v660_v6_runtime.py"),
    (
        "scripts/ghc_family_v660_v5_x2_data.py",
        "scripts/ghc_family_v660_v6_x2_data.py",
    ),
    ("scripts/build_ghc_family_v660_v5_x2.py", "scripts/build_ghc_family_v660_v6_x2.py"),
    (
        "scripts/build_ghc_family_v660_v5_closeout.py",
        "scripts/build_ghc_family_v660_v6_closeout.py",
    ),
    (
        "scripts/ghc_family_v660_v5_final_validator.py",
        "scripts/ghc_family_v660_v6_final_validator.py",
    ),
    ("tests/test_ghc_family_v660_v5_x2.py", "tests/test_ghc_family_v660_v6_x2.py"),
    (
        "tests/test_ghc_family_v660_v5_closeout.py",
        "tests/test_ghc_family_v660_v6_closeout.py",
    ),
)


def rewrite(text: str) -> str:
    """Shift phase/owner labels while preserving the successor edge."""

    protected = (
        ("V6606", "__NEXT_PHASE_CODE__"),
        ("v660-v6", "__NEXT_PHASE_HYPHEN__"),
        ("v660_v6", "__NEXT_PHASE_UNDERSCORE__"),
        ("Lyren Moss", "__NEXT_OWNER__"),
        ("lyren-moss", "__NEXT_OWNER_SLUG__"),
    )
    for old, new in protected:
        text = text.replace(old, new)

    current = (
        ("V6605", "V6606"),
        ("v660-v5", "v660-v6"),
        ("v660_v5", "v660_v6"),
        ("Vesper Arlen", "Lyren Moss"),
        ("vesper-arlen", "lyren-moss"),
    )
    for old, new in current:
        text = text.replace(old, new)

    predecessor = (
        ("V6604", "V6605"),
        ("v660-v4", "v660-v5"),
        ("v660_v4", "v660_v5"),
        ("Neris Solane", "Vesper Arlen"),
        ("neris-solane", "vesper-arlen"),
    )
    for old, new in predecessor:
        text = text.replace(old, new)

    restored = (
        ("__NEXT_PHASE_CODE__", "V6607"),
        ("__NEXT_PHASE_HYPHEN__", "v660-v7"),
        ("__NEXT_PHASE_UNDERSCORE__", "v660_v7"),
        ("__NEXT_OWNER__", "Ilyra Fen"),
        ("__NEXT_OWNER_SLUG__", "ilyra-fen"),
    )
    for old, new in restored:
        text = text.replace(old, new)

    identifier_rewrites = (
        ("ghc_family_meteorite_", "ghc_family_origami_"),
        ("ghc-family-meteorite-", "ghc-family-origami-"),
        ("synthetic-meteorite-curation", "synthetic-origami-documentation"),
    )
    for old, new in identifier_rewrites:
        text = text.replace(old, new)

    text = re.sub(r"\bMeteorite curation\b", "Origami documentation", text)
    text = re.sub(r"\bmeteorite curation\b", "origami documentation", text)
    return text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("x1", "x2"), required=True)
    args = parser.parse_args()
    pairs = X1_PAIRS if args.stage == "x1" else X2_PAIRS
    missing = [source for source, _ in pairs if not (ROOT / source).is_file()]
    existing = [target for _, target in pairs if (ROOT / target).exists()]
    if missing:
        raise SystemExit(f"missing sealed templates: {missing}")
    if existing:
        raise SystemExit(f"refusing to overwrite v660-v6 targets: {existing}")

    rows: list[dict[str, object]] = []
    for source, target in pairs:
        source_path = ROOT / source
        target_path = ROOT / target
        payload = rewrite(source_path.read_text(encoding="utf-8"))
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(payload, encoding="utf-8", newline="\n")
        rows.append(
            {
                "source": source,
                "target": target,
                "bytes": target_path.stat().st_size,
                "mechanical_only": True,
            }
        )

    print(
        json.dumps(
            {
                "schema": "ghc.family.v660-v6.scaffold-receipt.v1",
                "created": rows,
                "stage": args.stage,
                "overwrite_permitted": False,
                "phase_build_executed": False,
                "review_required": True,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
