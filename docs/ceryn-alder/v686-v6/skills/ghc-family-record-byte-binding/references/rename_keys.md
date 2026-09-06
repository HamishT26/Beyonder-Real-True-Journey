# Rename keys

Rename top-level fields atomically only when the resulting key set is collision-free.

Use the exact operation `rename_keys` with `ghc_family_record_differences.py`. Read the matching input and expected result in `criteria.json` before choosing a fixture. The source contracts are examples of bounded software behavior; they are not observations about external records.

The key decision is the declared input domain. Preserve literal keys, nulls, JSON types, order, refusal reasons, and the complete source binding wherever the selected criterion requires them. A package helper that interprets punctuation differently must be adapted at this boundary rather than changing a frozen oracle.

Each criterion supplies its hypothesis, concrete input, complete expected result, falsifier, and rollback. Retain a rejected result with zero success credit and record the corrected dependency separately. Do not turn a local match into empirical, professional, production, legal, cultural, affected-party, Māori, identity, accessibility-complete, security-complete, independent-reproduction, or Stage 20 evidence.

## Frozen criteria

- `CA6866-N071`: An empty rename map preserves the document
- `CA6866-N072`: One field can be renamed without changing its value
- `CA6866-N073`: Simultaneous key exchange uses original keys
- `CA6866-N074`: Identity renaming is harmless and explicit
- `CA6866-N075`: Renaming preserves nested payload structure
- `CA6866-N076`: Literal dotted source keys can be renamed
- `CA6866-N077`: An empty text destination remains an explicit key
- `CA6866-N078`: Collision with an untouched field is refused
- `CA6866-N079`: Two source fields cannot collapse into one destination
- `CA6866-N080`: A missing rename source is refused rather than invented
