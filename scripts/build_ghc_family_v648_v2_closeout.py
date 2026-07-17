#!/usr/bin/env python3
"""Build the combined Sylven Arc v648-v2 closeout and seal candidate."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "build_ghc_family_v648_v1_closeout.py"
SOURCE = "8755893971135b67322abb4b3acd93f07afc34c9"
X1 = "d59281ce9b30adc8adb78039920c44147bfc37e6"
EVIDENCE = "75e41d23fd3c068abcadca4454b0c939ba847c33"


def transformed_source() -> str:
    source = TEMPLATE.read_text(encoding="utf-8")
    lifecycle = '''LIFECYCLE_NEGATIVES = [
    {
        "negative_id": "V6482-LC-N01",
        "method_id": "V6482-M16",
        "failure": "The evidence push and four equality hashes were correct, but a PowerShell wrapper compared an actual tab to a literal escape sequence and returned nonzero.",
        "recovery": "Retain the wrapper failure, parse divergence as two integer fields, compare the four hashes independently, and require a clean tree.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6482-LC-N02",
        "method_id": "V6482-M17",
        "failure": "A read-only source search passed a wildcard-bearing Windows path directly to ripgrep, which rejected the path before searching.",
        "recovery": "Retain the failed invocation and replay with literal roots plus ripgrep's tool-native filename glob.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6482-LC-N03",
        "method_id": "V6482-M18",
        "failure": "The first closeout candidate retained one inherited lifting-practice phrase in its otherwise current machining boundary.",
        "recovery": "Withhold staging, retain the adaptation miss, transform the split boundary literals, and regenerate the owner-only candidate.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6482-LC-N04",
        "method_id": "V6482-M19",
        "failure": "A combined eight-file ripgrep stale-topic scan exceeded its thirty-second bound without usable output.",
        "recovery": "Grant no scan credit, retain the timeout, and replay exact per-file matching over the bounded closeout surface.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6482-LC-N05",
        "method_id": "V6482-M20",
        "failure": "The first recovered stale-topic gate counted the intentionally retained lifting-practice failure description as current phase truth and returned nonzero.",
        "recovery": "Retain the false-positive gate, scan current truth surfaces separately, and adjudicate retained-negative historical wording in its declared witness context.",
        "result": "retained_then_recovered",
    },
]
FINAL_EFFECTIVE_NEGATIVES'''
    source = re.sub(
        r"LIFECYCLE_NEGATIVES = \[.*?\]\nFINAL_EFFECTIVE_NEGATIVES",
        lifecycle,
        source,
        count=1,
        flags=re.S,
    )
    replacements = [
        ('SOURCE = "4ada48d3142a6d33e4c723184edbb84e59e22aa4"', f'SOURCE = "{SOURCE}"'),
        ('X1 = "3e2904ec02c893d91c16e9a48fbb2485fc5d824f"', f'X1 = "{X1}"'),
        ('EVIDENCE = "b09681afe5a4cac101bab367ef761e4ac1a7b57e"', f'EVIDENCE = "{EVIDENCE}"'),
        ("EVIDENCE_NEGATIVES = 3926", "EVIDENCE_NEGATIVES = 4023"),
        ("OPEN_GAPS = 26", "OPEN_GAPS = 27"),
        ("EXACT_GATES = 27", "EXACT_GATES = 28"),
        ("METHODS = 11", "METHODS = 20"),
        ("FAILED_WITNESSES = 15", "FAILED_WITNESSES = 20"),
        ("PASSING_WITNESSES = 15", "PASSING_WITNESSES = 20"),
        ('validation["test_result"]["tests"] != 68', 'validation["test_result"]["tests"] != 76'),
        ("Tamar Vey", "Sylven Arc"),
        ("Tamar's", "Sylven's"),
        ("tamar-vey", "sylven-arc"),
        ("v648-v1", "v648-v2"),
        ("v648_v1", "v648_v2"),
        ("V6481", "V6482"),
        ('"target_existing_task_title": "Sylven Arc"', '"target_existing_task_title": "Eiren Kestrel"'),
        ('"target_phase": "v648-gmut-thos-v2-x1-x2"', '"target_phase": "v648-gmut-thos-v3-x1-x2"'),
        ("single verified Sylven Arc baton", "single verified Eiren Kestrel baton"),
        ("real DES Y3 analysis or GMUT likelihood", "real LoTSS DR2 analysis or GMUT likelihood"),
        ("lifting safety, emergency response, worker and site privacy", "machining safety, worker and workplace privacy"),
        ("CBR, lifting safety, emergency response, worker ", "CBR, machining safety, worker "),
        ("and site privacy, remedy", "and workplace privacy, remedy"),
        ("professional, lifting-safety", "professional, machining-safety"),
        ("lifting-safety", "machining-safety"),
        ("MÄori", "Māori"),
        ("hapÅ«", "hapū"),
    ]
    for old, new in replacements:
        source = source.replace(old, new)
    return source


def main() -> int:
    namespace = {"__name__": "ghc_family_v648_v2_closeout_template", "__file__": str(Path(__file__).resolve())}
    exec(compile(transformed_source(), str(Path(__file__).resolve()), "exec"), namespace)
    namespace["build"]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
