# Typed difference

Expose structural difference categories without ignoring JSON type changes.

Use the exact operation `typed_difference` with `ghc_family_record_differences.py`. Read the matching input and expected result in `criteria.json` before choosing a fixture. The source contracts are examples of bounded software behavior; they are not observations about external records.

The key decision is the declared input domain. Preserve literal keys, nulls, JSON types, order, refusal reasons, and the complete source binding wherever the selected criterion requires them. A package helper that interprets punctuation differently must be adapted at this boundary rather than changing a frozen oracle.

Each criterion supplies its hypothesis, concrete input, complete expected result, falsifier, and rollback. Retain a rejected result with zero success credit and record the corrected dependency separately. Do not turn a local match into empirical, professional, production, legal, cultural, affected-party, Māori, identity, accessibility-complete, security-complete, independent-reproduction, or Stage 20 evidence.

## Frozen criteria

- `CA6866-N051`: Identical scalar fields have no difference category
- `CA6866-N052`: A value replacement is reported as a value change
- `CA6866-N053`: Boolean-to-integer replacement is a type change
- `CA6866-N054`: Integer-to-float replacement preserves the type distinction
- `CA6866-N055`: Adding a field reports dictionary addition
- `CA6866-N056`: Removing a field reports dictionary removal
- `CA6866-N057`: Appending a sequence item reports iterable addition
- `CA6866-N058`: Removing a sequence item reports iterable removal
- `CA6866-N059`: Mapping insertion order does not create a structural difference
- `CA6866-N060`: Null-to-empty-list replacement remains a type change
