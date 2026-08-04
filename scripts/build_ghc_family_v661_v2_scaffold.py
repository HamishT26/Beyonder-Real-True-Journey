#!/usr/bin/env python3
"""Create the additive Caelen Ash v661-v2 code scaffold from sealed v661-v1.

This is a bounded mechanical rewrite only. It refuses to overwrite targets,
does not execute a phase builder, and leaves all domain claims to the reviewed
v661-v2 data and validation contracts.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X1_PAIRS = (
    ("scripts/ghc_family_v661_v1_data.py", "scripts/ghc_family_v661_v2_data.py"),
    (
        "scripts/ghc_family_v661_v1_novelty_probe.py",
        "scripts/ghc_family_v661_v2_novelty_probe.py",
    ),
    ("scripts/build_ghc_family_v661_v1_x1.py", "scripts/build_ghc_family_v661_v2_x1.py"),
    ("tests/test_ghc_family_v661_v1_x1.py", "tests/test_ghc_family_v661_v2_x1.py"),
)
X2_PAIRS = (
    ("scripts/ghc_family_v661_v1_runtime.py", "scripts/ghc_family_v661_v2_runtime.py"),
    (
        "scripts/ghc_family_v661_v1_x2_data.py",
        "scripts/ghc_family_v661_v2_x2_data.py",
    ),
    ("scripts/build_ghc_family_v661_v1_x2.py", "scripts/build_ghc_family_v661_v2_x2.py"),
    (
        "scripts/build_ghc_family_v661_v1_closeout.py",
        "scripts/build_ghc_family_v661_v2_closeout.py",
    ),
    (
        "scripts/ghc_family_v661_v1_final_validator.py",
        "scripts/ghc_family_v661_v2_final_validator.py",
    ),
    ("tests/test_ghc_family_v661_v1_x2.py", "tests/test_ghc_family_v661_v2_x2.py"),
    (
        "tests/test_ghc_family_v661_v1_closeout.py",
        "tests/test_ghc_family_v661_v2_closeout.py",
    ),
)


def rewrite(text: str) -> str:
    """Shift phase, owner, successor, predecessor, and bounded-domain labels."""

    protected = (
        ("V6612", "__NEXT_PHASE_CODE__"),
        ("v661-v2", "__NEXT_PHASE_HYPHEN__"),
        ("v661_v2", "__NEXT_PHASE_UNDERSCORE__"),
        ("Caelen Ash", "__NEXT_OWNER__"),
        ("caelen-ash", "__NEXT_OWNER_SLUG__"),
    )
    for old, new in protected:
        text = text.replace(old, new)

    current = (
        ("V6611", "V6612"),
        ("v661-v1", "v661-v2"),
        ("v661_v1", "v661_v2"),
        ("Sable Rook", "Caelen Ash"),
        ("sable-rook", "caelen-ash"),
    )
    for old, new in current:
        text = text.replace(old, new)

    predecessor = (
        ("V6608", "V6611"),
        ("v660-v8", "v661-v1"),
        ("v660_v8", "v661_v1"),
        ("Auren Lark", "Sable Rook"),
        ("auren-lark", "sable-rook"),
    )
    for old, new in predecessor:
        text = text.replace(old, new)

    restored = (
        ("__NEXT_PHASE_CODE__", "V6613"),
        ("__NEXT_PHASE_HYPHEN__", "v661-v3"),
        ("__NEXT_PHASE_UNDERSCORE__", "v661_v3"),
        ("__NEXT_OWNER__", "Orin Thale"),
        ("__NEXT_OWNER_SLUG__", "orin-thale"),
    )
    for old, new in restored:
        text = text.replace(old, new)

    domain = (
        ("ghc_family_taxidermy_", "ghc_family_model_railway_"),
        ("ghc-family-taxidermy-", "ghc-family-model-railway-"),
        ("synthetic-taxidermy-documentation", "synthetic-model-railway-documentation"),
        ("Synthetic taxidermy documentation", "Synthetic model-railway documentation"),
        ("synthetic taxidermy documentation", "synthetic model-railway documentation"),
        ("Taxidermy", "Model-railway"),
        ("taxidermy", "model-railway"),
    )
    for old, new in domain:
        text = text.replace(old, new)
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
        raise SystemExit(f"refusing to overwrite v661-v2 targets: {existing}")

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
                "schema": "ghc.family.v661-v2.scaffold-receipt.v1",
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
