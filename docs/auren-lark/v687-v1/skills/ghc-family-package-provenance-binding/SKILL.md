---
name: ghc-family-package-provenance-binding
description: Bind direct and transitive wheel provenance before installation. Use for Auren-style owner-local synthetic evidence review; do not use it to assert real-world authority or validation.
---

# Package Provenance Binding

## Purpose

Bind direct and transitive wheel provenance before installation. This package is reusable owner-local guidance. Its examples are synthetic and its evidence remains same-owner only.

## Workflow

1. Read `references/contracts.json` and select an exact declared operation case.
2. Read both `references/positive.json` and `references/adverse.json` before execution.
3. Run `python scripts/ghc_family_auren_lark_v687_v1_recovery_dependency.py --operation dependency_closure --input INPUT.json --output OUTPUT.json` in an isolated environment satisfying `references/requirements.lock`.
4. Compare the complete typed result with the independently frozen expectation.
5. Retain every invalid input and operational failure at zero original success credit; a rejecting-validator pass is a separate witness.
6. Preserve `completed`, `represented`, `open_gap`, and `exact_gate`, and stop at every protected evidence or authority boundary.

## Boundaries

This skill establishes no observation, empirical result, professional competence, production readiness, deployment, credential, consent, legal or cultural interpretation, affected-party legitimacy, Maori authority, complete privacy or accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything proof, canon, or Stage 20 readiness. Names and family language remain relational working language only.
