---
name: ghc-family-caption-manual-evaluation-hold
description: Apply the bounded caption manual evaluation hold contract to synthetic cue, provenance, accessibility, or handover records while preserving evidence and authority vacancies.
---

# ghc-family-caption-manual-evaluation-hold

Use this skill when a synthetic caption record needs the manual evaluation hold contract. It does not authorize work on a live performance, a real transcript, a person, an identity, a rights decision, or an external system.

## Inputs

Require one owner-local JSON fixture with a nonempty title, one of `completed`, `represented`, `open_gap`, or `exact_gate`, `external_action: false`, and `authority_promotion: false`. Keep real identifiers, private routes, credentials, transcripts, and protected data out of the fixture.

## Workflow

1. Confirm the fixture is synthetic and owner-local.
2. Invoke `scripts/ghc_family_caption_accessibility_runner.py` with `--input` pointing to the exact fixture.
3. Retain a failed result before changing the fixture or method.
4. Treat a zero exit only as bounded structural evidence for this contract.
5. Keep manual evaluation, affected-user evidence, legal and cultural interpretation, Māori authority, professional signoff, production readiness, independent reproduction, and Stage 20 open or exact-gated.

## Output boundary

Return the runner's stable JSON result and the exact refusal reason. Never convert a rejected mutation into an original pass, and never treat this skill as standards conformance, complete accessibility, complete privacy, exhaustive security, empirical confirmation, or authority.
