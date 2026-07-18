#!/usr/bin/env python3
"""Customize the 20 already initialized v648-v7 phase-local skills."""

from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
PHASE=ROOT/'docs/tamar-vey/v648-v7'
sys.path.insert(0,str(ROOT/'scripts'))
import ghc_family_v648_v7_definitions as d

GROUPS={
    'retry':('retry timing, idempotency, circuit, dead-letter, and evidence-credit','ghc_family_v648_v7_retry_policy.py'),
    'reeh':('local-algebra, vacuum-domain, cyclicity, separating, gauge, EFT, unit, and observation-firewall','ghc_family_v648_v7_reeh_obligations.py'),
    'tess':('official-product provenance, cadence, quality, crowding, uncertainty, and zero-row refusal','ghc_family_v648_v7_tess_refusal.py'),
    'postal':('synthetic item lineage, quarantine, address minimization, accessibility, authority reservation, and handover','ghc_family_v648_v7_postal_handover.py'),
    'address':('synthetic address minimization and exact authority reservation','ghc_family_v648_v7_postal_handover.py'),
    'scim':('SCIM schema, mutability, PATCH, version, budget, and minimization','ghc_family_v648_v7_scim_profile.py'),
    'ebml':('EBML variable integers, declared lengths, nesting, CRC, budget, and refusal','ghc_family_v648_v7_ebml_tribunal.py'),
    'combobox':('combobox name, value, popup, keyboard, focus, status, and fallback structure','ghc_family_v648_v7_accessibility_audit.py'),
    'fick':('Fick flux, gradient, diffusivity, unit, domain, boundary, and psyche nonconversion','ghc_family_v648_v7_domain_guards.py'),
    'its':('interruption, level, slope, autocorrelation, seasonality, uncertainty, falsification, and nonpromotion','ghc_family_v648_v7_domain_guards.py'),
    'terminal':('terminal evidence, negative retention, exact gates, and nonpromotion','build_ghc_family_v648_v7_closeout.py'),
}

def group(name):
    for key,value in GROUPS.items():
        if key in name: return value
    raise RuntimeError(name)

for name in d.SKILL_IDEAS:
    focus,runner=group(name)
    title=' '.join(part.upper() if part in {'ebml','scim','its'} else part.capitalize() for part in name.removeprefix('ghc-family-v648-v7-').split('-'))
    text=f'''---
name: {name}
description: Apply bounded v648-v7 {focus} checks. Use when Codex must inspect or execute this owner-scoped synthetic, symbolic, structural, proxy, or refusal workflow while preserving evidence and authority gates.
---

# {title}

1. Read the v648-v7 proposal, source ledger, protected gates, and retained-negative register before acting.
2. Use `{runner}` only on owner-scoped synthetic, symbolic, structural, proxy, or zero-row inputs.
3. Check {focus} obligations and reject missing or corrupted required fields.
4. Preserve every rejected mutation, tooling failure, rollback, and recurrence guard; recovery never becomes an initially clean pass.
5. Record a bounded use receipt and keep empirical, participant, production, professional, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, consciousness, personhood, Theory-of-Everything, and Stage 20 gates open.

Do not mutate sibling lanes, install globally, elevate, alter host security, use private material, or claim authority. A passing result is same-owner bounded workflow evidence only.
'''
    path=PHASE/'skills'/name/'SKILL.md'
    if not path.is_file(): raise RuntimeError(f'initializer output missing: {name}')
    path.write_text(text,encoding='utf-8',newline='\n')
print(f'customized={len(d.SKILL_IDEAS)}')
