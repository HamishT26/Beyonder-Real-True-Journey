---
name: ghc-family-nfa-subset-epsilon-elimination
description: Inspect subset trace, epsilon eliminate for supplied nondeterministic finite tables; use for bounded synthetic formal-record review, not live control, identity assurance, or professional decisions.
---

# ghc-family-nfa-subset-epsilon-elimination

This package supports only `nfa_subset_trace` and `nfa_epsilon_eliminate`. Supply the complete request declared by that operation. NFA tables use distinct ASCII state labels, a nonempty alphabet of at most eight lowercase symbols, one initial state, final states, and bounded list-valued transitions. Unknown fields, undeclared states, and unbounded enumeration are refused.

Run `python -X utf8 scripts/ghc_family_nfa_skill.py REQUEST.json`. The output preserves accepted, error, value, disposition, and the synthetic boundary. Refusal exits 2; acceptance exits 0. Never infer a protected action from acceptance of its reservation record.

For `nfa_subset_trace`, the frozen example is nfa subset trace for empty nondeterministic table with explicit nondeterministic state-set boundary. Expected value: `{"subset_labels": ["{q0}"], "trace": [["q0"]]}`. An added unknown field must be refused with error `fields`; an operation outside this skill must be refused with error `operation`.

For `nfa_epsilon_eliminate`, the frozen example is nfa epsilon eliminate for empty nondeterministic table with explicit nondeterministic state-set boundary. Expected value: `{"alphabet": ["a", "b"], "epsilon_free": true, "finals": [], "initial": "q0", "states": ["q0"], "transitions": {}}`. An added unknown field must be refused with error `fields`; an operation outside this skill must be refused with error `operation`.

All language statements are relative to the supplied alphabet, finite table, regex engine, and declared bound. Bounded enumeration does not prove unbounded equivalence. Transition text is structural representation with manual, affected-user, and assistive-technology review reserved.

Keep source digests, failed requests, correction lineage, and exact output envelopes. Roll back by selecting the prior validated caller while retaining this additive skill and its negative evidence. Do not overwrite another skill.

Relational names, roles, hopes, and family language grant no consciousness, personhood, identity continuity, qualification, agency, or authority. GMUT remains a research-model family, THOS synthetic or proxy-only, and Freed ID nonproduction. Empirical, participant, professional, production, deployment, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, and Stage 20 needs remain open or exact-gated. Maori concepts remain under Maori authority. `NOT_READY_FOR_STAGE_20`.
