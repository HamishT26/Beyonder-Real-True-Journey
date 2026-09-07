---
name: ghc-family-dual-reader-type-differences
description: "Reports exact difference paths under a declared type-strict JSON relation, with no implicit Unicode or numeric normalization."
---

# Dual Reader Equivalence

Reports exact difference paths under a declared type-strict JSON relation, with no implicit Unicode or numeric normalization.

Use the finite contracts in [references/contracts.json](references/contracts.json) to distinguish accepting samples from held previews. Read the input, complete expected output, and five changed-result submissions before execution. A local type-strict comparison is deliberately narrower than general JSON Schema numeric equivalence; it is not a standards conformance claim.

Run `python scripts/ghc_family_teryn_halewick_v687_v4_dual_reader_equivalence.py --input INPUT.json --output NEW_OUTPUT.json` in an isolated environment satisfying [references/requirements.lock](references/requirements.lock). The output path must be new; preserving old witnesses is part of the interface. No external reference is fetched, and no live record is patched.

Compare the complete typed output, verify the original input is unchanged, and retain every invalid submission at zero original success credit. Rejection is a separate witness. A mismatch requires an additive correction and a focused recovery; never change the frozen expectation to match the implementation.

Bounded same-owner synthetic software evidence under shared infrastructure. Names, roles, hopes, and pronouns are collaborative working language only. No empirical, participant, professional, production, legal, cultural, affected-party, Maori-authority, complete privacy or accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 authority is established.
