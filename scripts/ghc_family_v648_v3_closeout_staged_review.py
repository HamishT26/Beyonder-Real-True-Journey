#!/usr/bin/env python3
"""Review exact staged Eiren v648-v3 closeout blobs and owner parity."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "ghc_family_v648_v1_closeout_staged_review.py"


def transformed_source() -> str:
    source = TEMPLATE.read_text(encoding="utf-8")
    for old, new in [
        ("Tamar Vey", "Eiren Kestrel"),
        ("docs/tamar-vey/v648-v1/", "docs/eiren-kestrel/v648-v3/"),
        ("v648-v1", "v648-v3"),
        ("v648_v1", "v648_v3"),
        ("V6481", "V6483"),
    ]:
        source = source.replace(old, new)
    frozen = '''FROZEN = {
    PHASE_PREFIX + "x1-proposals.json",
    PHASE_PREFIX + "x1-preregistration.md",
    PHASE_PREFIX + "x1-gate-carry-forward.json",
    PHASE_PREFIX + "approval-packets/x1-approval-portfolio.json",
    PHASE_PREFIX + "approval-packets/x1-protected-packet-register.json",
    PHASE_PREFIX + "prototypes/x1-candidate-plan.json",
    PHASE_PREFIX + "prototypes/x1-skill-runner-plan.json",
    PHASE_PREFIX + "maintenance/x1-clean-refine-plan.json",
    PHASE_PREFIX + "provenance/frozen-chain-proposal-index.json",
    PHASE_PREFIX + "provenance/proposal-collision-audit.json",
    PHASE_PREFIX + "sources/source-ledger.json",
    PHASE_PREFIX + "sources/source-ledger.md",
    PHASE_PREFIX + "validation/x1-operational-negatives.json",
    PHASE_PREFIX + "validation/x1-review.json",
    PHASE_PREFIX + "validation/x1-staged-manifest.json",
    PHASE_PREFIX + "validation/x1-staged-review.json",
}
ALLOWED_OUTSIDE = {
    "scripts/build_ghc_family_v648_v3_closeout.py",
    "scripts/ghc_family_v648_v3_closeout_staged_review.py",
    "scripts/ghc_family_v648_v3_final_gate.py",
    "scripts/ghc_family_v648_v3_full_suite.py",
    "tests/test_ghc_family_v646_v1.py",
    "tests/test_ghc_family_v647_v6_closeout.py",
    "tests/test_ghc_family_v647_v7_closeout.py",
    "tests/test_ghc_family_v647_v8_closeout.py",
    "tests/test_ghc_family_v648_v1_closeout.py",
    "tests/test_ghc_family_v648_v2_closeout.py",
    "tests/test_ghc_family_v648_v3_closeout.py",
}'''
    source, count = re.subn(r"FROZEN = \{.*?\}\nALLOWED_OUTSIDE = \{.*?\}", frozen, source, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("could not replace staged-review scope")
    return source


def main() -> int:
    namespace = {
        "__name__": "ghc_family_v648_v3_closeout_staged_review_template",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(transformed_source(), str(Path(__file__).resolve()), "exec"), namespace)
    return int(namespace["main"]())


if __name__ == "__main__":
    raise SystemExit(main())
