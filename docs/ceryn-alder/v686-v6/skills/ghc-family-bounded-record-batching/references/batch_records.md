# Batch records

Make chunk width and incomplete-tail policy explicit before batching records.

Use the exact operation `batch_records` with `ghc_family_record_streams.py`. Read the matching input and expected result in `criteria.json` before choosing a fixture. The source contracts are examples of bounded software behavior; they are not observations about external records.

The key decision is the declared input domain. Preserve literal keys, nulls, JSON types, order, refusal reasons, and the complete source binding wherever the selected criterion requires them. A package helper that interprets punctuation differently must be adapted at this boundary rather than changing a frozen oracle.

Each criterion supplies its hypothesis, concrete input, complete expected result, falsifier, and rollback. Retain a rejected result with zero success credit and record the corrected dependency separately. Do not turn a local match into empirical, professional, production, legal, cultural, affected-party, Māori, identity, accessibility-complete, security-complete, independent-reproduction, or Stage 20 evidence.

## Frozen criteria

- `CA6866-N121`: Empty input yields no batches
- `CA6866-N122`: Width one preserves each element as its own batch
- `CA6866-N123`: A complete two-wide sequence yields exact batches
- `CA6866-N124`: A non-strict incomplete tail remains visible
- `CA6866-N125`: Strict batching accepts a complete tail
- `CA6866-N126`: Strict batching refuses an incomplete tail
- `CA6866-N127`: Oversized width retains the single partial batch
- `CA6866-N128`: Zero width is refused before chunking
- `CA6866-N129`: Negative width is refused before chunking
- `CA6866-N130`: Boolean width is not an integer size
