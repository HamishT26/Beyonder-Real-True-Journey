# Natural labels

Sort bounded catalog labels by integer runs without changing or deduplicating labels.

Use the exact operation `natural_labels` with `ghc_family_record_streams.py`. Read the matching input and expected result in `criteria.json` before choosing a fixture. The source contracts are examples of bounded software behavior; they are not observations about external records.

The key decision is the declared input domain. Preserve literal keys, nulls, JSON types, order, refusal reasons, and the complete source binding wherever the selected criterion requires them. A package helper that interprets punctuation differently must be adapted at this boundary rather than changing a frozen oracle.

Each criterion supplies its hypothesis, concrete input, complete expected result, falsifier, and rollback. Retain a rejected result with zero success credit and record the corrected dependency separately. Do not turn a local match into empirical, professional, production, legal, cultural, affected-party, Māori, identity, accessibility-complete, security-complete, independent-reproduction, or Stage 20 evidence.

## Frozen criteria

- `CA6866-N131`: Numeric label suffixes use natural order
- `CA6866-N132`: Empty label input remains empty
- `CA6866-N133`: A single label is retained exactly
- `CA6866-N134`: Equal natural keys preserve leading-zero input order
- `CA6866-N135`: Reverse natural order is explicitly requested
- `CA6866-N136`: Case-sensitive ordering preserves original spelling
- `CA6866-N137`: Repeated exact labels remain repeated
- `CA6866-N138`: Multiple numeric runs are compared in sequence
- `CA6866-N139`: An empty label has a defined place before nonempty text
- `CA6866-N140`: Non-text labels are refused rather than coerced
