# Provenance coverage

Audit coverage of derived output locators without inventing source evidence.

Use the exact operation `provenance_coverage` with `ghc_family_record_evidence.py`. Read the matching input and expected result in `criteria.json` before choosing a fixture. The source contracts are examples of bounded software behavior; they are not observations about external records.

The key decision is the declared input domain. Preserve literal keys, nulls, JSON types, order, refusal reasons, and the complete source binding wherever the selected criterion requires them. A package helper that interprets punctuation differently must be adapted at this boundary rather than changing a frozen oracle.

Each criterion supplies its hypothesis, concrete input, complete expected result, falsifier, and rollback. Retain a rejected result with zero success credit and record the corrected dependency separately. Do not turn a local match into empirical, professional, production, legal, cultural, affected-party, Māori, identity, accessibility-complete, security-complete, independent-reproduction, or Stage 20 evidence.

## Frozen criteria

- `CA6866-N161`: Empty declared output scope is vacuously covered
- `CA6866-N162`: One output carries one declared source locator
- `CA6866-N163`: Two outputs can share one explicit source
- `CA6866-N164`: One output retains two declared source locators
- `CA6866-N165`: An unlinked output remains visibly uncovered
- `CA6866-N166`: A link outside output scope remains an orphan
- `CA6866-N167`: An unknown source prevents coverage credit
- `CA6866-N168`: An empty source list supplies no coverage
- `CA6866-N169`: Repeated output declarations are refused
- `CA6866-N170`: Conflicting repeated links are refused before selection
