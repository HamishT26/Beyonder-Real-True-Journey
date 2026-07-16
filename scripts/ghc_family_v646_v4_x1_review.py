#!/usr/bin/env python3
"""Run the strict Orin Thale v646-v4 x1 structural, privacy, and staged review."""

from __future__ import annotations

from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "scripts" / "ghc_family_v646_v3_x1_review.py"


def transformed_source() -> str:
    source = BASE.read_text(encoding="utf-8")
    replacements = [
        ('v646_v3', 'v646_v4'),
        ('"novelty_against_410_frozen_proposals"', '"novelty_against_420_frozen_proposals"'),
        ('if proposals.get("prior_frozen_proposal_count") != 410:', 'if proposals.get("prior_frozen_proposal_count") != 420:'),
        ('prior proposal count is not 410', 'prior proposal count is not 420'),
        ('if proposals.get("frozen_chain_count_after_x1") != 420:', 'if proposals.get("frozen_chain_count_after_x1") != 430:'),
        ('frozen chain count is not 420', 'frozen chain count is not 430'),
        ('if collision.get("prior_frozen_proposal_count") != 410', 'if collision.get("prior_frozen_proposal_count") != 420'),
        ('if len(sources.get("sources", [])) != 19:', 'if len(sources.get("sources", [])) != 17:'),
        ('expected_effective = 2619 + 70 + len(operational_rows)', 'expected_effective = 2704 + 70 + len(operational_rows)'),
        ('negatives.get("inherited_effective") != 2619', 'negatives.get("inherited_effective") != 2704'),
        ('safe_new_sable', 'safe_new_orin'),
        ('candidate_new_sable', 'candidate_new_orin'),
        ('V6463', 'V6464'),
        ('v646-v3', 'v646-v4'),
        ('Sable Rook', 'Orin Thale'),
        ('Sable', 'Orin'),
        ('sable-rook', 'orin-thale'),
    ]
    for old, new in replacements:
        source = source.replace(old, new)
    return source


def main() -> int:
    namespace: dict[str, Any] = {"__file__": str(Path(__file__).resolve()), "__name__": "ghc_family_v646_v4_x1_review_adapted"}
    exec(compile(transformed_source(), str(BASE), "exec"), namespace)
    return int(namespace["main"]())


if __name__ == "__main__":
    raise SystemExit(main())
