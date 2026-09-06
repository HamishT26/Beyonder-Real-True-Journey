# Jmes select

Keep JMESPath projection and null semantics explicit in a pure local query.

Use the exact operation `jmes_select` with `ghc_family_record_selection.py`. Read the matching input and expected result in `criteria.json` before choosing a fixture. The source contracts are examples of bounded software behavior; they are not observations about external records.

The key decision is the declared input domain. Preserve literal keys, nulls, JSON types, order, refusal reasons, and the complete source binding wherever the selected criterion requires them. A package helper that interprets punctuation differently must be adapted at this boundary rather than changing a frozen oracle.

Each criterion supplies its hypothesis, concrete input, complete expected result, falsifier, and rollback. Retain a rejected result with zero success credit and record the corrected dependency separately. Do not turn a local match into empirical, professional, production, legal, cultural, affected-party, Māori, identity, accessibility-complete, security-complete, independent-reproduction, or Stage 20 evidence.

## Frozen criteria

- `CA6866-N011`: An absent JMES field yields null
- `CA6866-N012`: Nested JMES selection preserves zero
- `CA6866-N013`: JMES list projection omits absent and null members
- `CA6866-N014`: JMES multi-select list preserves a missing position
- `CA6866-N015`: JMES boolean filtering retains only true rows
- `CA6866-N016`: JMES field sorting uses numeric values
- `CA6866-N017`: JMES length distinguishes empty sequence from null
- `CA6866-N018`: JMES contains tests an explicit list member
- `CA6866-N019`: JMES multiselect hash labels both projected values
- `CA6866-N020`: An unfinished JMES bracket is refused
