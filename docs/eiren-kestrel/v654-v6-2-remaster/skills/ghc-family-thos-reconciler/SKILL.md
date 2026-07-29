---
name: ghc-family-thos-reconciler
description: Validate owner-local deterministic desired/observed state, idempotence, stale-write refusal, and residual preservation.
---

# ghc-family-thos-reconciler

1. Read the selected proposal contract and its evidence lane.
2. Run `scripts/ghc_family_thos_reconciler.py` with an explicit owner-local output.
3. Require every accepting fixture and all rejecting mutations to pass.
4. Retain every failed attempt and stop on unsupported promotion.
5. Report only completed, represented, open_gap, or exact_gate.

Do not access real datasets, participants, accounts, credentials, keys, live
identity or training services, sibling lanes, production systems, or authority
decisions. Do not claim empirical confirmation, professional competence, legal
or cultural authority, Maori authority, complete privacy or accessibility,
exhaustive security, independent reproduction, consciousness or personhood,
AGI or ASI, Theory of Everything, or Stage 20 readiness.
