---
name: ghc-family-dfa-provenance-authority
description: Inspect provenance, authority reservation for supplied deterministic finite tables; use for synthetic formal-record review, not live control or identity assurance.
---

# ghc-family-dfa-provenance-authority

This package supports only `dfa_provenance` and `dfa_authority_reservation`. Supply a complete table with distinct ASCII state labels, a nonempty alphabet of at most eight lowercase symbols, one initial state, final states, and every transition. The table has at most 32 states. Unknown fields and partial transitions are refused.

Run `python -X utf8 scripts/ghc_family_dfa_skill.py REQUEST.json`. The output preserves accepted, error, value, disposition, and the synthetic boundary. Refusal exits 2; acceptance exits 0. Never infer a protected action from acceptance of its reservation record.

For `dfa_provenance`, the frozen example is dfa provenance for empty language. Expected value: `{"digest_matches": true, "machine_sha256": "54517ea8b56999699bc4eb34a7153da09aa46b793395d7cbb98ff174d56c1ec5", "missing": [], "real_identity_assurance": false, "review": "same_owner", "source_label": "synthetic-table-0"}`. An added unknown field must be refused with error `fields`. An operation outside this package must be refused with error `operation`.

For `dfa_authority_reservation`, the frozen example is dfa authority reservation for deploy_parser. Expected value: `{"action": "deploy_parser", "authority_granted": false, "executed": false, "required": "fresh action-specific evidence and competent authority"}`. An added unknown field must be refused with error `fields`. An operation outside this package must be refused with error `operation`.

Complements and relations are relative to the declared alphabet and complete finite tables. Bounded word enumeration has a length limit and never proves unbounded equivalence. Product searches may establish only a relation between the supplied tables. Transition text is a structural representation with affected-user and assistive-technology review reserved.

Keep source digests, failed requests, correction lineage, and exact output envelopes. Roll back by selecting the prior validated caller and preserving this package and its negative evidence. Do not overwrite another package.

Relational names, roles, hopes, and family language grant no consciousness, personhood, identity continuity, qualification, or authority. GMUT remains a research-model family, THOS synthetic or proxy-only, and Freed ID nonproduction. Empirical, participant, professional, production, legal, cultural, Maori-authority, privacy, accessibility, exhaustive-security, independent-reproduction, and Stage 20 needs remain open or exact-gated. Maori concepts remain under Maori authority. NOT_READY_FOR_STAGE_20.
