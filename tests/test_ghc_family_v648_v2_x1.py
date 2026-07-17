from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "tests" / "test_ghc_family_v648_v1_x1.py"
source = TEMPLATE.read_text(encoding="utf-8")
for old, new in [
    ("ghc_family_v648_v1_definitions", "ghc_family_v648_v2_definitions"),
    ("tamar-vey", "sylven-arc"),
    ("v648-v1", "v648-v2"),
    ("V648V1", "V648V2"),
    ("SOURCE_FINAL = \"4ada48d3142a6d33e4c723184edbb84e59e22aa4\"", "SOURCE_FINAL = \"8755893971135b67322abb4b3acd93f07afc34c9\""),
    ('payload["prior_frozen_proposal_count"], 550', 'payload["prior_frozen_proposal_count"], 560'),
    ('payload["frozen_chain_count_after_x1"], 560', 'payload["frozen_chain_count_after_x1"], 570'),
    ("len(X1_OPERATIONAL_NEGATIVES), 4", "len(X1_OPERATIONAL_NEGATIVES), 5"),
]:
    source = source.replace(old, new)
exec(compile(source, str(Path(__file__).resolve()), "exec"), globals())
