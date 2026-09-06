# Stream items

Read a bounded JSON stream with explicit prefix and strict duplicate-key validation.

Use the exact operation `stream_items` with `ghc_family_record_streams.py`. Read the matching input and expected result in `criteria.json` before choosing a fixture. The source contracts are examples of bounded software behavior; they are not observations about external records.

The key decision is the declared input domain. Preserve literal keys, nulls, JSON types, order, refusal reasons, and the complete source binding wherever the selected criterion requires them. A package helper that interprets punctuation differently must be adapted at this boundary rather than changing a frozen oracle.

Each criterion supplies its hypothesis, concrete input, complete expected result, falsifier, and rollback. Retain a rejected result with zero success credit and record the corrected dependency separately. Do not turn a local match into empirical, professional, production, legal, cultural, affected-party, Māori, identity, accessibility-complete, security-complete, independent-reproduction, or Stage 20 evidence.

## Frozen criteria

- `CA6866-N141`: A root array streams all scalar items
- `CA6866-N142`: An empty array streams no items
- `CA6866-N143`: Null false and zero remain distinct stream items
- `CA6866-N144`: A rows prefix selects a named object array
- `CA6866-N145`: Nested item containers retain their shape
- `CA6866-N146`: Finite decimal values remain JSON numbers
- `CA6866-N147`: UTF-8 text survives the stream boundary
- `CA6866-N148`: An unfinished JSON array is refused
- `CA6866-N149`: Duplicate object keys are refused before streaming
- `CA6866-N150`: A nonfinite JSON token is refused
