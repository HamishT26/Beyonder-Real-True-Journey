#!/usr/bin/env python3
"""Build Eiren Kestrel v648-v3 x1 by adapting the family-current v648-v1 builder."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "build_ghc_family_v648_v1_preregistration.py"


def transformed_source() -> str:
    source = TEMPLATE.read_text(encoding="utf-8")
    replacements = [
        ('ROOT / "docs" / "orin-thale" / "v647-v8"', 'ROOT / "docs" / "sylven-arc" / "v648-v2"'),
        ('"path": "docs/orin-thale/v647-v8/x1-proposals.json"', '"path": "docs/sylven-arc/v648-v2/x1-proposals.json"'),
        ("ghc_family_v648_v1_definitions", "ghc_family_v648_v3_definitions"),
        ("codex/GHC-Family/tamar-vey-full-tools", "codex/GHC-Family/eiren-kestrel-v643-v1-full-tools"),
        ("v648-v1", "v648-v3"),
        ("v648_v1", "v648_v3"),
        ("V6481", "V6483"),
        ("ghc.family.v648-v1", "ghc.family.v648-v3"),
        ("Tamar Vey", "Eiren Kestrel"),
        ("Tamar's", "Eiren's"),
        ("Tamar ", "Eiren "),
        ("Tamar\n", "Eiren\n"),
        ("tamar-vey", "eiren-kestrel"),
        ("tamar_new", "eiren_new"),
        (
            '["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Orin Thale", "Sylven Arc"]',
            '["Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"]',
        ),
        (
            "Orin v647-v8 verified closeout plus one later post-baton read-only continuity negative",
            "Sylven v648-v2 exact-final closeout plus four retained post-final operational negatives",
        ),
        ("Orin's exact v647-v8 final head", "Sylven's exact v648-v2 final head"),
        ("three Orin phase commits", "three Sylven phase commits"),
        (
            "Orin's sealed 3,835 negatives plus fourteen external operational negatives form the 3,849 activation continuity",
            "Sylven's sealed 4,028 negatives plus four external post-final operational negatives form the 4,032 activation continuity",
        ),
        ("Twenty-five open gaps and twenty-six exact gates", "Twenty-seven open gaps and twenty-eight exact gates"),
        ("semantic audit of 550 prior proposals", "semantic audit of 570 prior proposals"),
        ('"d_free_gib_at_preflight": 543.62', '"d_free_gib_at_preflight": 536.71'),
        ('"inherited_tracked_file_baseline": 37396', '"inherited_tracked_file_baseline": 37881'),
        ('"inherited_full_checkout_file_baseline": 37603', '"inherited_full_checkout_file_baseline": 38091'),
        (
            "real_workers_sites_cranes_lifts_incidents_or_emergency_actions",
            "real_people_accounts_credentials_providers_incidents_breaches_notifications_or_remedies",
        ),
        (
            "lifting authority, supervision or signalling authority",
            "identity-incident, notification, privacy, remedy or trust-governance authority",
        ),
        ('"frozen_chain_count_after_x1": 560', '"frozen_chain_count_after_x1": 580'),
        ('"frozen_after_x1": 560', '"frozen_after_x1": 580'),
        ('"frozen_after": 560', '"frozen_after": 580'),
        ('"target_title": "Sylven Arc"', '"target_title": "Ilyra Fen"'),
        ('"next_phase": "v648-gmut-thos-v2-x1-x2"', '"next_phase": "v648-gmut-thos-v4-x1-x2"'),
        (
            '"requires_one_named_replay": True,',
            '"requires_one_named_replay": False,\n            "replay_prohibited_by_latest_user_instruction": True,\n            "repeatability_credit": 0,\n            "independent_reproduction": False,',
        ),
        (
            '"cleanup": len(CLEAN_TASK_TITLES),\n    }\n    if floors != {"safe": 30, "candidate": 20, "skill": 20, "runner": 10, "cleanup": 30}:',
            '"cleanup": len(CLEAN_TASK_TITLES),\n    }\n    if floors != {"safe": 30, "candidate": 20, "skill": 20, "runner": 10, "cleanup": 60}:',
        ),
        ('"count": 30,\n            "tasks": portfolio_rows(CLEAN_TASK_TITLES, "CLEAN", 15),', '"count": 60,\n            "tasks": portfolio_rows(CLEAN_TASK_TITLES, "CLEAN", 30),'),
        ('"origin": "successor_seed_rewritten_after_review" if index == 10 else "eiren_new_core",', '"origin": "successor_seed_rewritten_after_review" if index > 5 else "eiren_new_core",'),
        (
            "The primary Trinity Mandala focus is {PRIMARY_FOCUS}; GMUT Mind and Freed ID/CBR Heart remain explicit.",
            "The primary Trinity Mandala focus is {PRIMARY_FOCUS}; GMUT Mind and THOS Body remain explicit.",
        ),
        (
            "The core surfaces are: an atomic-publication tribunal; typed Iyer-Wald obligations; a DES Y3 cosmic-shear zero-row adapter; synthetic mobile-crane lift handover; an OpenID Shared Signals profile; a crane-incident authority matrix; a CPIO newc tribunal; an accessible-name computation audit; a Prigogine domain guard; and an instrumental-variable Stage 20 nonpromotion board.",
            "The core surfaces are: a context-budget artifact-pointer tribunal; typed Tomita-Takesaki obligations; a DESI DR2 Lyman-alpha zero-row adapter; synthetic identity-incident handover; an OpenID Federation subordinate-events profile; an identity-incident authority matrix; a six-node Nexus threat model; an accessible artifact-pointer audit; a thermodynamic-length domain guard; and a proximal-causal Stage 20 nonpromotion board.",
        ),
        (
            "Thirty safe-now tasks, twenty bounded candidates, twenty skill proposals, ten runner proposals, and thirty cleanup proposals",
            "Thirty safe-now tasks, twenty bounded candidates, twenty skill proposals, ten runner proposals, and sixty cleanup proposals",
        ),
        (
            "workers, sites, cranes, lifts, incidents, emergency or safety decisions",
            "people, accounts, credentials, providers, incidents, breaches, notifications, or remedies",
        ),
        (
            "workers, sites, cranes, lifts, incidents, emergency actions, keys, signals, services, accounts, identifiers, or remedies",
            "people, accounts, credentials, providers, incidents, breaches, notifications, remedies, keys, federation entities, events, services, or identifiers",
        ),
        ("real lifting operation", "real identity-incident operation"),
        ('"observed_on": "2026-07-17"', '"observed_on": "2026-07-18"'),
        ('"desktop": "26.707.9981.0"', '"desktop": "not inspected in bounded CLI session"'),
        ('"sqlite": "3.49.1"', '"node": "v24.18.0"'),
        ('"feature_state": "unavailable_requires_elevation"', '"feature_state": "not_probed_beyond_executable_lookup"'),
        ('"checked_on": "2026-07-17"', '"checked_on": "2026-07-18"'),
        ("Checked 2026-07-17.", "Checked 2026-07-18."),
        (
            '"requires_exact_final": True,\n            "requires_one_named_replay":',
            '"requires_exact_final": True,\n            "requires_canonical_full_suite": True,\n            "requires_one_named_replay":',
        ),
    ]
    for old, new in replacements:
        source = source.replace(old, new)
    return source


def main() -> int:
    namespace = {
        "__name__": "ghc_family_v648_v3_preregistration_template",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(transformed_source(), str(Path(__file__).resolve()), "exec"), namespace)
    return int(namespace["main"]())


if __name__ == "__main__":
    raise SystemExit(main())
