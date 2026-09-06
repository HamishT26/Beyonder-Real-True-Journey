# Recursive prune

Remove only the declared literal mapping keys while retaining every other JSON value.

Use the exact operation `recursive_prune` with `ghc_family_record_merging.py`. Read the matching input and expected result in `criteria.json` before choosing a fixture. The source contracts are examples of bounded software behavior; they are not observations about external records.

The key decision is the declared input domain. Preserve literal keys, nulls, JSON types, order, refusal reasons, and the complete source binding wherever the selected criterion requires them. A package helper that interprets punctuation differently must be adapted at this boundary rather than changing a frozen oracle.

Each criterion supplies its hypothesis, concrete input, complete expected result, falsifier, and rollback. Retain a rejected result with zero success credit and record the corrected dependency separately. Do not turn a local match into empirical, professional, production, legal, cultural, affected-party, Māori, identity, accessibility-complete, security-complete, independent-reproduction, or Stage 20 evidence.

## Frozen criteria

- `CA6866-N101`: An empty drop list keeps all fields
- `CA6866-N102`: One selected root field is omitted
- `CA6866-N103`: The same selected key is removed at every mapping depth
- `CA6866-N104`: Mappings nested inside arrays receive the same policy
- `CA6866-N105`: Array scalar values do not become field names
- `CA6866-N106`: Removing an absent key preserves the mapping
- `CA6866-N107`: A dotted drop key is not a deep path
- `CA6866-N108`: Pruning a container removes its entire subtree
- `CA6866-N109`: Empty nested containers remain after pruning
- `CA6866-N110`: A scalar root is outside the pruning container contract
