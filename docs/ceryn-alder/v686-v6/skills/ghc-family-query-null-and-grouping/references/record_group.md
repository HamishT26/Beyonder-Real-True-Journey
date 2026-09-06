# Record group

Partition records by a declared text field while preserving source order within each bucket.

Use the exact operation `record_group` with `ghc_family_record_selection.py`. Read the matching input and expected result in `criteria.json` before choosing a fixture. The source contracts are examples of bounded software behavior; they are not observations about external records.

The key decision is the declared input domain. Preserve literal keys, nulls, JSON types, order, refusal reasons, and the complete source binding wherever the selected criterion requires them. A package helper that interprets punctuation differently must be adapted at this boundary rather than changing a frozen oracle.

Each criterion supplies its hypothesis, concrete input, complete expected result, falsifier, and rollback. Retain a rejected result with zero success credit and record the corrected dependency separately. Do not turn a local match into empirical, professional, production, legal, cultural, affected-party, Māori, identity, accessibility-complete, security-complete, independent-reproduction, or Stage 20 evidence.

## Frozen criteria

- `CA6866-N021`: An empty record set has no groups
- `CA6866-N022`: A single record creates one labelled bucket
- `CA6866-N023`: Repeated bucket values preserve record order
- `CA6866-N024`: Bucket labels are emitted in lexical order
- `CA6866-N025`: Interleaved records stay ordered within their bucket
- `CA6866-N026`: Empty text is a valid explicit bucket label
- `CA6866-N027`: A different declared grouping field is honored
- `CA6866-N028`: Nested payloads survive grouping intact
- `CA6866-N029`: A record lacking the grouping field is refused
- `CA6866-N030`: A numeric grouping value is outside the declared text domain
