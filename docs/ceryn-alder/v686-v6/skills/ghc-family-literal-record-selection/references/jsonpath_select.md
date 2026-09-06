# Jsonpath select

Project bounded JSONPath matches without changing the source or promoting a match into evidence.

Use the exact operation `jsonpath_select` with `ghc_family_record_selection.py`. Read the matching input and expected result in `criteria.json` before choosing a fixture. The source contracts are examples of bounded software behavior; they are not observations about external records.

The key decision is the declared input domain. Preserve literal keys, nulls, JSON types, order, refusal reasons, and the complete source binding wherever the selected criterion requires them. A package helper that interprets punctuation differently must be adapted at this boundary rather than changing a frozen oracle.

Each criterion supplies its hypothesis, concrete input, complete expected result, falsifier, and rollback. Retain a rejected result with zero success credit and record the corrected dependency separately. Do not turn a local match into empirical, professional, production, legal, cultural, affected-party, Māori, identity, accessibility-complete, security-complete, independent-reproduction, or Stage 20 evidence.

## Frozen criteria

- `CA6866-N031`: JSONPath root returns one whole-document match
- `CA6866-N032`: JSONPath field selects a scalar
- `CA6866-N033`: JSONPath missing field returns no matches
- `CA6866-N034`: JSONPath wildcard keeps null and false elements
- `CA6866-N035`: JSONPath nested arrays retain traversal order
- `CA6866-N036`: JSONPath positional selection chooses the second row
- `CA6866-N037`: JSONPath slice preserves its bounded interval
- `CA6866-N038`: JSONPath quoted dotted field remains literal
- `CA6866-N039`: JSONPath wildcard over empty array has no matches
- `CA6866-N040`: Malformed JSONPath is refused before traversal
