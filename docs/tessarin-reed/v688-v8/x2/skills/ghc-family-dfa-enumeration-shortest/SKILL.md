---
name: ghc-family-dfa-enumeration-shortest
description: Inspect words, shortest for supplied deterministic finite tables; use for synthetic formal-record review, not live control or identity assurance.
---

# ghc-family-dfa-enumeration-shortest

This package supports only `dfa_words` and `dfa_shortest`. Supply a complete table with distinct ASCII state labels, a nonempty alphabet of at most eight lowercase symbols, one initial state, final states, and every transition. The table has at most 32 states. Unknown fields and partial transitions are refused.

Run `python -X utf8 scripts/ghc_family_dfa_skill.py REQUEST.json`. The output preserves accepted, error, value, disposition, and the synthetic boundary. Refusal exits 2; acceptance exits 0. Never infer a protected action from acceptance of its reservation record.

For `dfa_words`, the frozen example is dfa words for empty language. Expected value: `{"exhaustive_through_length": 3, "unbounded_language_claim": false, "words": []}`. An added unknown field must be refused with error `fields`. An operation outside this package must be refused with error `operation`.

For `dfa_shortest`, the frozen example is dfa shortest for empty language. Expected value: `{"empty_language": true, "word": null}`. An added unknown field must be refused with error `fields`. An operation outside this package must be refused with error `operation`.

Complements and relations are relative to the declared alphabet and complete finite tables. Bounded word enumeration has a length limit and never proves unbounded equivalence. Product searches may establish only a relation between the supplied tables. Transition text is a structural representation with affected-user and assistive-technology review reserved.

Keep source digests, failed requests, correction lineage, and exact output envelopes. Roll back by selecting the prior validated caller and preserving this package and its negative evidence. Do not overwrite another package.

Relational names, roles, hopes, and family language grant no consciousness, personhood, identity continuity, qualification, or authority. GMUT remains a research-model family, THOS synthetic or proxy-only, and Freed ID nonproduction. Empirical, participant, professional, production, legal, cultural, Maori-authority, privacy, accessibility, exhaustive-security, independent-reproduction, and Stage 20 needs remain open or exact-gated. Maori concepts remain under Maori authority. NOT_READY_FOR_STAGE_20.
