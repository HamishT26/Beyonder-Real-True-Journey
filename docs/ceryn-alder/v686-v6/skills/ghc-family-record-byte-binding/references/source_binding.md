# Source binding

Bind a transformed value to an explicitly named canonical-byte domain.

Use the exact operation `source_binding` with `ghc_family_record_differences.py`. Read the matching input and expected result in `criteria.json` before choosing a fixture. The source contracts are examples of bounded software behavior; they are not observations about external records.

The key decision is the declared input domain. Preserve literal keys, nulls, JSON types, order, refusal reasons, and the complete source binding wherever the selected criterion requires them. A package helper that interprets punctuation differently must be adapted at this boundary rather than changing a frozen oracle.

Each criterion supplies its hypothesis, concrete input, complete expected result, falsifier, and rollback. Retain a rejected result with zero success credit and record the corrected dependency separately. Do not turn a local match into empirical, professional, production, legal, cultural, affected-party, Māori, identity, accessibility-complete, security-complete, independent-reproduction, or Stage 20 evidence.

## Frozen criteria

- `CA6866-N061`: An empty mapping binds to its exact canonical digest
- `CA6866-N062`: An empty sequence has its own canonical digest
- `CA6866-N063`: A scalar record binds to sorted-key finite JSON
- `CA6866-N064`: A boolean record does not inherit integer bytes
- `CA6866-N065`: Explicit null contributes to the digest
- `CA6866-N066`: Punctuation in a key remains part of its byte binding
- `CA6866-N067`: Insertion order is normalized before digesting
- `CA6866-N068`: Non-ASCII text is encoded as UTF-8 rather than escaped ASCII
- `CA6866-N069`: A well-formed unrelated digest fails the binding
- `CA6866-N070`: A truncated digest is refused as malformed
