# Record delta

Apply and reverse an owner-local dictionary difference under exact JSON equality.

Use the exact operation `record_delta` with `ghc_family_record_differences.py`. Read the matching input and expected result in `criteria.json` before choosing a fixture. The source contracts are examples of bounded software behavior; they are not observations about external records.

The key decision is the declared input domain. Preserve literal keys, nulls, JSON types, order, refusal reasons, and the complete source binding wherever the selected criterion requires them. A package helper that interprets punctuation differently must be adapted at this boundary rather than changing a frozen oracle.

Each criterion supplies its hypothesis, concrete input, complete expected result, falsifier, and rollback. Retain a rejected result with zero success credit and record the corrected dependency separately. Do not turn a local match into empirical, professional, production, legal, cultural, affected-party, Māori, identity, accessibility-complete, security-complete, independent-reproduction, or Stage 20 evidence.

## Frozen criteria

- `CA6866-N041`: An unchanged mapping round-trips without edits
- `CA6866-N042`: A scalar replacement has a reversible preimage
- `CA6866-N043`: A newly added field reverses to absence
- `CA6866-N044`: A removed field reverses to its original value
- `CA6866-N045`: A nested scalar edit retains adjacent fields
- `CA6866-N046`: Appending a list item is reversible
- `CA6866-N047`: Removing the last list item preserves its recovery value
- `CA6866-N048`: A dotted dictionary key round-trips as one key
- `CA6866-N049`: Mixed additions removals and replacements retain a full preimage
- `CA6866-N050`: Boolean and integer equality cannot conceal a nonreversible diff
