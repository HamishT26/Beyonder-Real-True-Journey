# Field projection

Project a literal top-level allowlist or denylist without deep-path interpretation.

Use the exact operation `field_projection` with `ghc_family_record_merging.py`. Read the matching input and expected result in `criteria.json` before choosing a fixture. The source contracts are examples of bounded software behavior; they are not observations about external records.

The key decision is the declared input domain. Preserve literal keys, nulls, JSON types, order, refusal reasons, and the complete source binding wherever the selected criterion requires them. A package helper that interprets punctuation differently must be adapted at this boundary rather than changing a frozen oracle.

Each criterion supplies its hypothesis, concrete input, complete expected result, falsifier, and rollback. Retain a rejected result with zero success credit and record the corrected dependency separately. Do not turn a local match into empirical, professional, production, legal, cultural, affected-party, Māori, identity, accessibility-complete, security-complete, independent-reproduction, or Stage 20 evidence.

## Frozen criteria

- `CA6866-N111`: Pick mode selects a declared field
- `CA6866-N112`: Omit mode retains fields outside the declared list
- `CA6866-N113`: Picking an absent field does not synthesize null
- `CA6866-N114`: Picking an explicit null retains the field
- `CA6866-N115`: Picking false does not discard a present value
- `CA6866-N116`: An empty pick list yields an empty mapping
- `CA6866-N117`: An empty omit list preserves all fields
- `CA6866-N118`: Punctuation in projected keys remains literal
- `CA6866-N119`: Nested values are preserved without recursive filtering
- `CA6866-N120`: An unlisted projection mode is refused
