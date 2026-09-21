---
name: ghc-family-random-set-refinement-v1
description: Use for declared finite synthetic belief-function calculations covering vacuous extension, coarsen partition, conditioning, random set coverage.
---

# Finite belief-function operations

Read [the exact operation contracts](references/operations.json) and choose one of the four declared operations. Invoke `node <public-runner-root>/ghc_family_random_set_refinement_v1.txt <input.json>`. Only that wrapper is a supported entry point; the two runtime TXT files are dependencies. The wrapper reports one typed JSON envelope and exits zero on admitted requests or two on refusal. Extra operations are rejected by the scope gate.

The request has exactly operation, n, mass, other, event and reliability fields. Use three through five atoms, two 2^n arrays of integer percentage units, zero empty-set mass and total 100 for each array. Event is a mask within the frame and reliability is an integer percentage. Input JSON is at most one MiB, at most 32 nesting levels, and has unique keys. All outputs use reduced exact rational strings.

- `bba_vacuous_extension`: Replace each original atom by two subatoms and move each focal mass to the union of its paired subatoms; infer no internal split.
- `bba_coarsen_partition`: Map atom i to parity i modulo two and sum equal image-mask masses; preserve total mass.
- `bba_conditioning`: Intersect each focal set with the supplied event, then normalize nonempty mass; refuse zero plausibility.
- `bba_random_set_coverage`: Represent a finite 100-outcome random-set ledger by hit and containment frequencies; do not infer sampling calibration.

Compare the full envelope with the frozen example before using the result. The source definitions were frozen before implementation. The merged package retains all four local guides and their callers; see [merge provenance](references/merge-sources.json). Algebraic source combination does not establish source independence. A pignistic projection does not establish empirical calibration or a person's beliefs. Keep invalid inputs at zero subject credit even when refusal is a passing software witness.

The accepting, malformed and outside-scope examples are retained alongside the contracts. A failed check stops selection of the dependency. Rollback selects the previous validated caller without overwriting or deleting this package, its local source guides, or its failure evidence. No package installation, external upload, decision affecting a person, or route send is performed by these runners.

Veylora Quen, she/her, evidence steward, and the hope to make each handoff clearer, more faithful and easier for Hamish to review are relational working language only. Finite same-owner synthetic software under shared infrastructure establishes no consciousness, personhood, identity continuity, qualification, independent agency, empirical GMUT confirmation, production THOS or Freed ID, professional, legal, cultural, affected-party or Maori authority, complete privacy or accessibility, exhaustive security, independent reproduction, AGI/ASI, Theory-of-Everything proof, canon or Stage 20 readiness. Maori concepts remain under Maori authority. NOT_READY_FOR_STAGE_20.
