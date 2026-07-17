#!/usr/bin/env python3
"""Build Sylven Arc v648-v2 x1 by adapting the family-current v648-v1 builder."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "build_ghc_family_v648_v1_preregistration.py"


def transformed_source() -> str:
    source = TEMPLATE.read_text(encoding="utf-8")
    replacements = [
        ('ROOT / "docs" / "orin-thale" / "v647-v8"', 'ROOT / "docs" / "tamar-vey" / "v648-v1"'),
        ('"path": "docs/orin-thale/v647-v8/x1-proposals.json"', '"path": "docs/tamar-vey/v648-v1/x1-proposals.json"'),
        ("ghc_family_v648_v1_definitions", "ghc_family_v648_v2_definitions"),
        ("codex/GHC-Family/tamar-vey-full-tools", "codex/GHC-Family/sylven-arc-v642-v8-full-tools"),
        ("v648-v1", "v648-v2"),
        ("v648_v1", "v648_v2"),
        ("V6481", "V6482"),
        ("ghc.family.v648-v1", "ghc.family.v648-v2"),
        ("Tamar Vey", "Sylven Arc"),
        ("Tamar's", "Sylven's"),
        ("Tamar ", "Sylven "),
        ("Tamar\n", "Sylven\n"),
        ("tamar-vey", "sylven-arc"),
        ('["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Orin Thale", "Sylven Arc"]', '["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey"]'),
        ("Orin v647-v8 verified closeout plus one later post-baton read-only continuity negative", "Tamar v648-v1 verified closeout plus its retained post-final read-only wrapper fault"),
        ("Orin's exact v647-v8 final head", "Tamar's exact v648-v1 final head"),
        ("three Orin phase commits", "three Tamar phase commits"),
        ("Orin's sealed 3,835 negatives plus fourteen external operational negatives form the 3,849 activation continuity", "Tamar's sealed 3,937 negatives plus one external read-only wrapper fault form the 3,938 activation continuity"),
        ("Twenty-five open gaps and twenty-six exact gates", "Twenty-six open gaps and twenty-seven exact gates"),
        ("semantic audit of 550 prior proposals", "semantic audit of 560 prior proposals"),
        ("clean and four-way equal before being fast-forwarded without a merge to", "clean and four-way equal before being fast-forwarded without a merge to"),
        ('"d_free_gib_at_preflight": 543.62', '"d_free_gib_at_preflight": 543.23'),
        ('"inherited_tracked_file_baseline": 37396', '"inherited_tracked_file_baseline": 37643'),
        ('"inherited_full_checkout_file_baseline": 37603', '"inherited_full_checkout_file_baseline": 37853'),
        ("cranes_lifts_incidents_or_emergency_actions", "machines_jobs_parts_measurements_incidents_or_emergency_actions"),
        ("lifting authority, supervision or signalling authority", "machining authority, metrology or isolation authority"),
        ('"frozen_chain_count_after_x1": 560', '"frozen_chain_count_after_x1": 570'),
        ('"frozen_after_x1": 560', '"frozen_after_x1": 570'),
        ('"frozen_after": 560', '"frozen_after": 570'),
        ('"target_title": "Sylven Arc"', '"target_title": "Eiren Kestrel"'),
        ('"next_phase": "v648-gmut-thos-v2-x1-x2"', '"next_phase": "v648-gmut-thos-v3-x1-x2"'),
        ("The primary Trinity Mandala focus is {PRIMARY_FOCUS}; GMUT Mind and Freed ID/CBR Heart remain explicit.", "The primary Trinity Mandala focus is {PRIMARY_FOCUS}; THOS Body and Freed ID/CBR Heart remain explicit."),
        ("The core surfaces are: an atomic-publication tribunal; typed Iyer-Wald obligations; a DES Y3 cosmic-shear zero-row adapter; synthetic mobile-crane lift handover; an OpenID Shared Signals profile; a crane-incident authority matrix; a CPIO newc tribunal; an accessible-name computation audit; a Prigogine domain guard; and an instrumental-variable Stage 20 nonpromotion board.", "The core surfaces are: an advisory-lock tribunal; typed KMS obligations; a LoTSS DR2 zero-row adapter; synthetic precision-machining handover; an OpenID JARM profile; a machining-incident authority matrix; a Zstandard frame tribunal; a progressbar structural audit; a Gibbs adsorption domain guard; and a synthetic-control Stage 20 nonpromotion board."),
        ("workers, sites, cranes, lifts, incidents, emergency or safety decisions", "workers, employers, machines, jobs, parts, measurements, incidents, emergency or safety decisions"),
        ("workers, sites, cranes, lifts, incidents, emergency actions, keys, signals, services, accounts, identifiers, or remedies", "workers, employers, machines, jobs, parts, measurements, incidents, emergency actions, keys, clients, authorization servers, tokens, services, identifiers, or remedies"),
        ("real lifting operation", "real machining operation"),
    ]
    for old, new in replacements:
        source = source.replace(old, new)
    source = source.replace(
        'ROOT / "docs" / "sylven-arc" / "v648-v2"',
        'ROOT / "docs" / "tamar-vey" / "v648-v1"',
        1,
    )
    source = source.replace(
        '"path": "docs/sylven-arc/v648-v2/x1-proposals.json"',
        '"path": "docs/tamar-vey/v648-v1/x1-proposals.json"',
    )
    return source


def main() -> int:
    namespace = {"__name__": "ghc_family_v648_v2_preregistration_template", "__file__": str(Path(__file__).resolve())}
    exec(compile(transformed_source(), str(Path(__file__).resolve()), "exec"), namespace)
    return int(namespace["main"]())


if __name__ == "__main__":
    raise SystemExit(main())
