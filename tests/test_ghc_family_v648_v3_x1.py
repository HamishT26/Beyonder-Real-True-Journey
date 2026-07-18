from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "tests" / "test_ghc_family_v648_v1_x1.py"
source = TEMPLATE.read_text(encoding="utf-8")
for old, new in [
    ("ghc_family_v648_v1_definitions", "ghc_family_v648_v3_definitions"),
    ("tamar-vey", "eiren-kestrel"),
    ("v648-v1", "v648-v3"),
    ("V648V1", "V648V3"),
    ("SOURCE_FINAL = \"4ada48d3142a6d33e4c723184edbb84e59e22aa4\"", "SOURCE_FINAL = \"227a764b2bfad7a601bf45dcbacc1e37ffa5bb62\""),
    ('payload["prior_frozen_proposal_count"], 550', 'payload["prior_frozen_proposal_count"], 570'),
    ('payload["frozen_chain_count_after_x1"], 560', 'payload["frozen_chain_count_after_x1"], 580'),
    ("len(X1_OPERATIONAL_NEGATIVES), 4", "len(X1_OPERATIONAL_NEGATIVES), 10"),
    ("(30, 20, 20, 10, 30)", "(30, 20, 20, 10, 60)"),
    ("len(SOURCES), 19", "len(SOURCES), 20"),
]:
    source = source.replace(old, new)
exec(compile(source, str(Path(__file__).resolve()), "exec"), globals())
