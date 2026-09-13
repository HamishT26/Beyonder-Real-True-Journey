# Operation contracts

## order_ideals

Enumerate all downward-closed subsets with the empty ideal retained. The plan binds five distinct cases under this operation. Input has exactly op, poset and args; poset has id, labels and covers. Args is an empty object.

## join_irreducible_embedding

Map lattice elements to ideals of their nonzero join-irreducibles and report missing ideals. The plan binds five distinct cases under this operation. Input has exactly op, poset and args; poset has id, labels and covers. Args is an empty object.

## distributivity_witness

Return the first deterministic distributive-law counterexample, or finite exhaustive satisfaction. The plan binds five distinct cases under this operation. Input has exactly op, poset and args; poset has id, labels and covers. Args is an empty object.

## modularity_witness

Return the first modular-law counterexample under its order premise. The plan binds five distinct cases under this operation. Input has exactly op, poset and args; poset has id, labels and covers. Args is an empty object.

C3 tests a zero long-interval coefficient; B2 tests incomparable atoms and unique complements; M3 separates modularity from distributivity; N5 supplies a modular-law counterexample; V retains missing lattice operations. Numeric counterexamples are witnesses only for the declared finite input.

The corresponding runner is ghc_family_lattice_ideal_counterexamples.txt. Its two implementation libraries receive no extra runner credit. Rollback selects the retained local capability and appends a correction; it never overwrites another global package.

Same-owner finite synthetic software evidence only; not independent reproduction, empirical GMUT confirmation, production THOS or Freed ID, professional, legal, cultural, affected-party or Maori authority, complete privacy or accessibility, exhaustive security, AGI/ASI, consciousness, personhood, identity continuity, Theory-of-Everything proof, canon, deployment or Stage 20 readiness.
