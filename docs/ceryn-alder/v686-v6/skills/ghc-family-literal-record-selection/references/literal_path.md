# Literal path

Select an explicitly typed record path without treating punctuation as navigation.

Use the exact operation `literal_path` with `ghc_family_record_selection.py`. Read the matching input and expected result in `criteria.json` before choosing a fixture. The source contracts are examples of bounded software behavior; they are not observations about external records.

The key decision is the declared input domain. Preserve literal keys, nulls, JSON types, order, refusal reasons, and the complete source binding wherever the selected criterion requires them. A package helper that interprets punctuation differently must be adapted at this boundary rather than changing a frozen oracle.

Each criterion supplies its hypothesis, concrete input, complete expected result, falsifier, and rollback. Retain a rejected result with zero success credit and record the corrected dependency separately. Do not turn a local match into empirical, professional, production, legal, cultural, affected-party, Māori, identity, accessibility-complete, security-complete, independent-reproduction, or Stage 20 evidence.

## Frozen criteria

- `CA6866-N001`: Root selection retains the empty mapping
- `CA6866-N002`: A false field is present rather than absent
- `CA6866-N003`: A null field remains an explicit value
- `CA6866-N004`: Nested sequence selection preserves an empty list
- `CA6866-N005`: A dotted key is a literal mapping component
- `CA6866-N006`: A slash key does not become a JSON pointer
- `CA6866-N007`: A tilde key retains its spelling
- `CA6866-N008`: An integer component selects an array element
- `CA6866-N009`: A missing mapping component gives a bounded refusal
- `CA6866-N010`: An array index beyond the end is refused
