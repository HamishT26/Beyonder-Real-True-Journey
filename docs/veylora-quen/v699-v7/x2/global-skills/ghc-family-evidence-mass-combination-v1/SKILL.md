---
name: ghc-family-evidence-mass-combination-v1
description: Use for declared finite synthetic belief-function calculations covering conjunctive combination, conflict mass, dempster normalization, discount mass.
---

# Finite belief-function operations

Read [the exact operation contracts](references/operations.json) and choose one of the four declared operations. Invoke `node <public-runner-root>/ghc_family_evidence_mass_combination_v1.txt <input.json>`. Only that wrapper is a supported entry point; the two runtime TXT files are dependencies. The wrapper reports one typed JSON envelope and exits zero on admitted requests or two on refusal. Extra operations are rejected by the scope gate.

The request has exactly operation, n, mass, other, event and reliability fields. Use three through five atoms, two 2^n arrays of integer percentage units, zero empty-set mass and total 100 for each array. Event is a mask within the frame and reliability is an integer percentage. Input JSON is at most one MiB, at most 32 nesting levels, and has unique keys. All outputs use reduced exact rational strings.

- `bba_conjunctive_combination`: Multiply focal masses and accumulate by intersection, retaining empty-set conflict.
- `bba_conflict_mass`: Separate empty-intersection product mass from the conserved total of one.
- `bba_dempster_normalization`: Remove conflict and divide nonempty masses by one minus conflict; refuse total conflict.
- `bba_discount_mass`: Multiply by declared reliability and move the remainder to the full frame; reliability is an input, not a measured estimate.

Compare the full envelope with the frozen example before using the result. The source definitions were frozen before implementation. The merged package retains all four local guides and their callers; see [merge provenance](references/merge-sources.json). Algebraic source combination does not establish source independence. A pignistic projection does not establish empirical calibration or a person's beliefs. Keep invalid inputs at zero subject credit even when refusal is a passing software witness.

The accepting, malformed and outside-scope examples are retained alongside the contracts. A failed check stops selection of the dependency. Rollback selects the previous validated caller without overwriting or deleting this package, its local source guides, or its failure evidence. No package installation, external upload, decision affecting a person, or route send is performed by these runners.

Veylora Quen, she/her, evidence steward, and the hope to make each handoff clearer, more faithful and easier for Hamish to review are relational working language only. Finite same-owner synthetic software under shared infrastructure establishes no consciousness, personhood, identity continuity, qualification, independent agency, empirical GMUT confirmation, production THOS or Freed ID, professional, legal, cultural, affected-party or Maori authority, complete privacy or accessibility, exhaustive security, independent reproduction, AGI/ASI, Theory-of-Everything proof, canon or Stage 20 readiness. Maori concepts remain under Maori authority. NOT_READY_FOR_STAGE_20.
