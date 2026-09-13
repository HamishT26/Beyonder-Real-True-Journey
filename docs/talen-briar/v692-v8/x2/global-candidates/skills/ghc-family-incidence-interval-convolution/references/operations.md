# Operation contracts

## interval_elements

List every declared closed interval, retaining empty incomparable intervals. The plan binds five distinct cases under this operation. Input has exactly op, poset and args; poset has id, labels and covers. Args is an empty object.

## incidence_zeta

Materialize the upper-order indicator in declared label order. The plan binds five distinct cases under this operation. Input has exactly op, poset and args; poset has id, labels and covers. Args is an empty object.

## incidence_delta

Build the incidence identity with zero off-diagonal coefficients. The plan binds five distinct cases under this operation. Input has exactly op, poset and args; poset has id, labels and covers. Args is an empty object.

## incidence_convolution

Convolve two supported integer functions over each closed interval. The plan binds five distinct cases under this operation. Input has exactly op, poset and args; poset has id, labels and covers. The argument fields are left, right.

C3 tests a zero long-interval coefficient; B2 tests incomparable atoms and unique complements; M3 separates modularity from distributivity; N5 supplies a modular-law counterexample; V retains missing lattice operations. Numeric counterexamples are witnesses only for the declared finite input.

The corresponding runner is ghc_family_incidence_interval_convolution.txt. Its two implementation libraries receive no extra runner credit. Rollback selects the retained local capability and appends a correction; it never overwrites another global package.

Same-owner finite synthetic software evidence only; not independent reproduction, empirical GMUT confirmation, production THOS or Freed ID, professional, legal, cultural, affected-party or Maori authority, complete privacy or accessibility, exhaustive security, AGI/ASI, consciousness, personhood, identity continuity, Theory-of-Everything proof, canon, deployment or Stage 20 readiness.
