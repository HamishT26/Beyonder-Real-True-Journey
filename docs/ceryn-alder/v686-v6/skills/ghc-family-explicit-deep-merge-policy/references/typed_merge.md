# Typed merge

Apply a declared deep-merge strategy to fresh copies and reject incompatible types.

Use the exact operation `typed_merge` with `ghc_family_record_merging.py`. Read the matching input and expected result in `criteria.json` before choosing a fixture. The source contracts are examples of bounded software behavior; they are not observations about external records.

The key decision is the declared input domain. Preserve literal keys, nulls, JSON types, order, refusal reasons, and the complete source binding wherever the selected criterion requires them. A package helper that interprets punctuation differently must be adapted at this boundary rather than changing a frozen oracle.

Each criterion supplies its hypothesis, concrete input, complete expected result, falsifier, and rollback. Retain a rejected result with zero success credit and record the corrected dependency separately. Do not turn a local match into empirical, professional, production, legal, cultural, affected-party, Māori, identity, accessibility-complete, security-complete, independent-reproduction, or Stage 20 evidence.

## Frozen criteria

- `CA6866-N081`: Replacement merge combines disjoint fields
- `CA6866-N082`: Replacement merge chooses the right scalar explicitly
- `CA6866-N083`: Nested mapping merge preserves both children
- `CA6866-N084`: Replacement list semantics do not concatenate
- `CA6866-N085`: Additive list semantics retain both ordered sequences
- `CA6866-N086`: Typesafe scalar replacement accepts matching integer types
- `CA6866-N087`: Typesafe replacement refuses integer-to-text conflict
- `CA6866-N088`: Typesafe additive lists retain repeated values
- `CA6866-N089`: Typesafe additive merge refuses list-to-mapping conflict
- `CA6866-N090`: An undeclared merge strategy is refused
