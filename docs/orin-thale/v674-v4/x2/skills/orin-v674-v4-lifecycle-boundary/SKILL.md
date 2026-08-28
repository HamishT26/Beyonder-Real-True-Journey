---
name: orin-v674-v4-lifecycle-boundary
description: Review synthetic lifecycle-state transitions for Orin v674-v4 owner-local synthetic evidence; do not use it to infer a real-world result or authority.
---

# orin-v674-v4-lifecycle-boundary

Use this phase-local skill only for the bounded Orin v674-v4 synthetic contract surface. It is not globally installed and does not alter another owner's evidence.

## Decision rule

Require an explicit current state, permitted predecessor, and reversible next state; quarantine hidden jumps.

## Workflow

1. Read the complete target contract and its preregistered expected disposition.
2. Check the decision rule above and preserve any missing witness as a vacancy.
3. Reject an invalid mutation without rewriting it; record the smallest bounded recovery separately.
4. Return only `completed`, `represented`, `open_gap`, or `exact_gate` for a core outcome.

## Boundaries

Synthetic structure and same-owner software checks do not establish empirical confirmation, participant evidence, professional competence, production readiness, legal or cultural ratification, Maori authority, independent reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything proof, canon, or Stage 20 authority.
