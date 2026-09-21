---
name: ghc-family-belief-plausibility-transforms-v1
description: Use for declared finite synthetic belief-function calculations covering belief table, plausibility table, commonality table, mobius recovery.
---

# Finite belief-function operations

Read [the exact operation contracts](references/operations.json) and choose one of the four declared operations. Invoke `node <public-runner-root>/ghc_family_belief_plausibility_transforms_v1.txt <input.json>`. Only that wrapper is a supported entry point; the two runtime TXT files are dependencies. The wrapper reports one typed JSON envelope and exits zero on admitted requests or two on refusal. Extra operations are rejected by the scope gate.

The request has exactly operation, n, mass, other, event and reliability fields. Use three through five atoms, two 2^n arrays of integer percentage units, zero empty-set mass and total 100 for each array. Event is a mask within the frame and reliability is an integer percentage. Input JSON is at most one MiB, at most 32 nesting levels, and has unique keys. All outputs use reduced exact rational strings.

- `bba_belief_table`: Apply a finite subset zeta transform to obtain belief for every event mask.
- `bba_plausibility_table`: Use one minus belief of the complement for every event mask.
- `bba_commonality_table`: Apply the superset zeta transform; the empty-mask commonality is one.
- `bba_mobius_recovery`: Invert the subset transform exactly and compare recovered integer masses to the input.

Compare the full envelope with the frozen example before using the result. The source definitions were frozen before implementation. The merged package retains all four local guides and their callers; see [merge provenance](references/merge-sources.json). Algebraic source combination does not establish source independence. A pignistic projection does not establish empirical calibration or a person's beliefs. Keep invalid inputs at zero subject credit even when refusal is a passing software witness.

The accepting, malformed and outside-scope examples are retained alongside the contracts. A failed check stops selection of the dependency. Rollback selects the previous validated caller without overwriting or deleting this package, its local source guides, or its failure evidence. No package installation, external upload, decision affecting a person, or route send is performed by these runners.

Veylora Quen, she/her, evidence steward, and the hope to make each handoff clearer, more faithful and easier for Hamish to review are relational working language only. Finite same-owner synthetic software under shared infrastructure establishes no consciousness, personhood, identity continuity, qualification, independent agency, empirical GMUT confirmation, production THOS or Freed ID, professional, legal, cultural, affected-party or Maori authority, complete privacy or accessibility, exhaustive security, independent reproduction, AGI/ASI, Theory-of-Everything proof, canon or Stage 20 readiness. Maori concepts remain under Maori authority. NOT_READY_FOR_STAGE_20.
