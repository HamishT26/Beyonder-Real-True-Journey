# Resource budget

Measure declared depth, node, and canonical-byte budgets without treating size as quality.

Use the exact operation `resource_budget` with `ghc_family_record_streams.py`. Read the matching input and expected result in `criteria.json` before choosing a fixture. The source contracts are examples of bounded software behavior; they are not observations about external records.

The key decision is the declared input domain. Preserve literal keys, nulls, JSON types, order, refusal reasons, and the complete source binding wherever the selected criterion requires them. A package helper that interprets punctuation differently must be adapted at this boundary rather than changing a frozen oracle.

Each criterion supplies its hypothesis, concrete input, complete expected result, falsifier, and rollback. Retain a rejected result with zero success credit and record the corrected dependency separately. Do not turn a local match into empirical, professional, production, legal, cultural, affected-party, Māori, identity, accessibility-complete, security-complete, independent-reproduction, or Stage 20 evidence.

## Frozen criteria

- `CA6866-N151`: An empty mapping fits exact one-node limits
- `CA6866-N152`: A one-element array includes its scalar node
- `CA6866-N153`: Depth below the nested payload is reported
- `CA6866-N154`: Node count includes all list elements
- `CA6866-N155`: UTF-8 byte ceiling counts non-ASCII encoding
- `CA6866-N156`: A scalar fits its exact canonical byte length
- `CA6866-N157`: All three exceeded limits remain independently visible
- `CA6866-N158`: A nested empty container has a second depth level
- `CA6866-N159`: Zero-valued content does not reduce structural node count
- `CA6866-N160`: Boundary equality remains accepting for nested records
