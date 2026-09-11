---
name: ghc-family-transition-equivalence
description: Review recurrent component structure, nondeterministic action conflicts, strong simulation relation, strong bisimulation partition, bounded trace inclusion counterexample, bisimulation quotient readback. Use for bounded labelled transition models and explicit counterexamples.
---

# transition equivalence

Send one JSON request on stdin to `node scripts/ghc_family_transition_equivalence.txt`. The runner returns a complete `ok`, `value`, `error` envelope and exits 2 on a declared refusal. It performs no network, credential, task, or external release action.

Select the matching source guide before building a request:

- [Recurrent component structure](references/ghc-family-lts-scc.md): `lts_scc`.
- [Nondeterministic action conflicts](references/ghc-family-lts-conflicts.md): `lts_conflicts`.
- [Strong simulation relation](references/ghc-family-lts-simulation.md): `lts_simulation`.
- [Strong bisimulation partition](references/ghc-family-lts-bisimulation.md): `lts_bisimulation`.
- [Bounded trace inclusion counterexample](references/ghc-family-lts-trace-difference.md): `lts_trace_difference`.
- [Bisimulation quotient readback](references/ghc-family-lts-quotient.md): `lts_quotient`.

Models have 1 to 16 ordered states, at most 64 distinct action edges, and explicit start state. State and action tokens are ASCII letters followed by up to 31 letters, digits, underscores or hyphens. Set fields must be arrays; null, booleans, strings, duplicate states, dangling edges and unknown fields are refused. Raw deadlocks are visible; temporal properties use stuttering at deadlocks. No fairness is assumed. Trace difference has a maximum depth of eight and does not establish equivalence beyond that bound. Strong bisimulation requires two-sided action matching; mutual simulation is not a substitute.

The strict dispatcher is an additive correction for four malformed set requests accepted by the original x1 module. Original x1 bytes, failed subjects and all two hundred earlier accepted/refused fixture contracts remain preserved. Use this strict entrypoint for new work.

Retain the request, complete result, evidence limit and failed subject before recovery. A passing refusal guard gives zero success credit to that subject. Rollback selects the previous compatible source only within its validated domain and preserves this package and its receipts. Source guide hashes are in [merge-sources.json](references/merge-sources.json).

Bounded same-owner synthetic evidence only; no empirical, participant, identity, professional, production, legal, cultural, affected-party, Maori-authority, complete privacy/accessibility, exhaustive-security, independent-reproduction, consciousness/personhood, AGI/ASI, Theory-of-Everything or Stage 20 claim. NOT_READY_FOR_STAGE_20.
