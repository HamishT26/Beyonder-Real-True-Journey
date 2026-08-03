#!/usr/bin/env python3
"""Create the additive Neris v660-v4 code scaffold from sealed v660-v3 files.

This is a bounded mechanical rewrite only.  It refuses to overwrite targets,
does not execute a phase builder, and leaves all domain claims to the reviewed
v660-v4 data and validation contracts.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X1_PAIRS = (
    ("scripts/ghc_family_v660_v3_data.py", "scripts/ghc_family_v660_v4_data.py"),
    (
        "scripts/ghc_family_v660_v3_novelty_probe.py",
        "scripts/ghc_family_v660_v4_novelty_probe.py",
    ),
    ("scripts/build_ghc_family_v660_v3_x1.py", "scripts/build_ghc_family_v660_v4_x1.py"),
    ("tests/test_ghc_family_v660_v3_x1.py", "tests/test_ghc_family_v660_v4_x1.py"),
)
X2_PAIRS = (
    ("scripts/ghc_family_v660_v3_runtime.py", "scripts/ghc_family_v660_v4_runtime.py"),
    (
        "scripts/ghc_family_v660_v3_x2_data.py",
        "scripts/ghc_family_v660_v4_x2_data.py",
    ),
    ("scripts/build_ghc_family_v660_v3_x2.py", "scripts/build_ghc_family_v660_v4_x2.py"),
    (
        "scripts/build_ghc_family_v660_v3_closeout.py",
        "scripts/build_ghc_family_v660_v4_closeout.py",
    ),
    (
        "scripts/ghc_family_v660_v3_final_validator.py",
        "scripts/ghc_family_v660_v4_final_validator.py",
    ),
    ("tests/test_ghc_family_v660_v3_x2.py", "tests/test_ghc_family_v660_v4_x2.py"),
    (
        "tests/test_ghc_family_v660_v3_closeout.py",
        "tests/test_ghc_family_v660_v4_closeout.py",
    ),
)


def rewrite(text: str) -> str:
    protected = (
        ("V6604", "__NEXT_PHASE_CODE__"),
        ("v660-v4", "__NEXT_PHASE_HYPHEN__"),
        ("v660_v4", "__NEXT_PHASE_UNDERSCORE__"),
        ("Neris Solane", "__NEXT_OWNER__"),
        ("neris-solane", "__NEXT_OWNER_SLUG__"),
    )
    for old, new in protected:
        text = text.replace(old, new)

    current = (
        ("V6603", "V6604"),
        ("v660-v3", "v660-v4"),
        ("v660_v3", "v660_v4"),
        ("Elaren Kestrel", "Neris Solane"),
        ("elaren-kestrel", "neris-solane"),
    )
    for old, new in current:
        text = text.replace(old, new)

    predecessor = (
        ("V6602", "V6603"),
        ("v660-v2", "v660-v3"),
        ("v660_v2", "v660_v3"),
        ("Eiren Kestrel", "Elaren Kestrel"),
        ("eiren-kestrel", "elaren-kestrel"),
    )
    for old, new in predecessor:
        text = text.replace(old, new)

    restored = (
        ("__NEXT_PHASE_CODE__", "V6605"),
        ("__NEXT_PHASE_HYPHEN__", "v660-v5"),
        ("__NEXT_PHASE_UNDERSCORE__", "v660_v5"),
        ("__NEXT_OWNER__", "Vesper Arlen"),
        ("__NEXT_OWNER_SLUG__", "vesper-arlen"),
    )
    for old, new in restored:
        text = text.replace(old, new)

    identifier_rewrites = (
        ("ghc_family_lichen_", "ghc_family_ice_core_"),
        ("ghc-family-lichen-", "ghc-family-ice-core-"),
        ("synthetic-lichenarium", "synthetic-ice-core-archive"),
    )
    for old, new in identifier_rewrites:
        text = text.replace(old, new)

    text = re.sub(r"\bLichenarium\b", "Ice-core archive", text)
    text = re.sub(r"\blichenarium\b", "ice-core archive", text)
    text = re.sub(r"\bLichen\b", "Ice-core", text)
    text = re.sub(r"\blichen\b", "ice-core", text)
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
        raise SystemExit(f"refusing to overwrite v660-v4 targets: {existing}")

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
                "schema": "ghc.family.v660-v4.scaffold-receipt.v1",
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
