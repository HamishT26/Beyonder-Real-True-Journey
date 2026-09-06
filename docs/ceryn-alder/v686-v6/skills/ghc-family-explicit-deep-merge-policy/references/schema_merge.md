# Schema merge

Limit schema-directed merging to four declared local strategies with no remote references.

Use the exact operation `schema_merge` with `ghc_family_record_merging.py`. Read the matching input and expected result in `criteria.json` before choosing a fixture. The source contracts are examples of bounded software behavior; they are not observations about external records.

The key decision is the declared input domain. Preserve literal keys, nulls, JSON types, order, refusal reasons, and the complete source binding wherever the selected criterion requires them. A package helper that interprets punctuation differently must be adapted at this boundary rather than changing a frozen oracle.

Each criterion supplies its hypothesis, concrete input, complete expected result, falsifier, and rollback. Retain a rejected result with zero success credit and record the corrected dependency separately. Do not turn a local match into empirical, professional, production, legal, cultural, affected-party, Māori, identity, accessibility-complete, security-complete, independent-reproduction, or Stage 20 evidence.

## Frozen criteria

- `CA6866-N091`: Overwrite strategy replaces the complete mapping
- `CA6866-N092`: Object merge combines disjoint object members
- `CA6866-N093`: Object merge replaces the conflicting leaf
- `CA6866-N094`: Object merge descends into nested objects
- `CA6866-N095`: Append strategy preserves repeated list members
- `CA6866-N096`: Appending an empty head preserves the base list
- `CA6866-N097`: Discard strategy preserves an existing base value
- `CA6866-N098`: Overwrite can replace a value with explicit null
- `CA6866-N099`: Append refuses non-array inputs
- `CA6866-N100`: External or unlisted schema strategy is refused
