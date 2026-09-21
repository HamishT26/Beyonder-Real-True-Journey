---
name: ghc-family-mass-assignment-structure-v1
description: Use for declared finite synthetic belief-function calculations covering frame shape, focal support, mass normal form, event bounds.
---

# Finite belief-function operations

Read [the exact operation contracts](references/operations.json) and choose one of the four declared operations. Invoke `node <public-runner-root>/ghc_family_mass_assignment_structure_v1.txt <input.json>`. Only that wrapper is a supported entry point; the two runtime TXT files are dependencies. The wrapper reports one typed JSON envelope and exits zero on admitted requests or two on refusal. Extra operations are rejected by the scope gate.

The request has exactly operation, n, mass, other, event and reliability fields. Use three through five atoms, two 2^n arrays of integer percentage units, zero empty-set mass and total 100 for each array. Event is a mask within the frame and reliability is an integer percentage. Input JSON is at most one MiB, at most 32 nesting levels, and has unique keys. All outputs use reduced exact rational strings.

- `bba_frame_shape`: Return frame size, subset count and normalized input status after exact shape admission.
- `bba_focal_support`: List positive-mass masks and their bitwise union and intersection; zero-mass sets are excluded.
- `bba_mass_normal_form`: Divide percentage units by 100 and reduce every rational without floating point.
- `bba_event_bounds`: Belief sums focal subsets of the event; plausibility sums focal sets intersecting it; width is their difference.

Compare the full envelope with the frozen example before using the result. The source definitions were frozen before implementation. The merged package retains all four local guides and their callers; see [merge provenance](references/merge-sources.json). Algebraic source combination does not establish source independence. A pignistic projection does not establish empirical calibration or a person's beliefs. Keep invalid inputs at zero subject credit even when refusal is a passing software witness.

The accepting, malformed and outside-scope examples are retained alongside the contracts. A failed check stops selection of the dependency. Rollback selects the previous validated caller without overwriting or deleting this package, its local source guides, or its failure evidence. No package installation, external upload, decision affecting a person, or route send is performed by these runners.

Veylora Quen, she/her, evidence steward, and the hope to make each handoff clearer, more faithful and easier for Hamish to review are relational working language only. Finite same-owner synthetic software under shared infrastructure establishes no consciousness, personhood, identity continuity, qualification, independent agency, empirical GMUT confirmation, production THOS or Freed ID, professional, legal, cultural, affected-party or Maori authority, complete privacy or accessibility, exhaustive security, independent reproduction, AGI/ASI, Theory-of-Everything proof, canon or Stage 20 readiness. Maori concepts remain under Maori authority. NOT_READY_FOR_STAGE_20.
