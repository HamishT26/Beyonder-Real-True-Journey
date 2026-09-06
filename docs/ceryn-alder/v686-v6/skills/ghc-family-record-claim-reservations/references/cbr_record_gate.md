# Cbr record gate

Keep competent and affected-party authority separate from local record transformations.

Use the exact operation `cbr_record_gate` with `ghc_family_record_evidence.py`. Read the matching input and expected result in `criteria.json` before choosing a fixture. The source contracts are examples of bounded software behavior; they are not observations about external records.

The key decision is the declared input domain. Preserve literal keys, nulls, JSON types, order, refusal reasons, and the complete source binding wherever the selected criterion requires them. A package helper that interprets punctuation differently must be adapted at this boundary rather than changing a frozen oracle.

Each criterion supplies its hypothesis, concrete input, complete expected result, falsifier, and rollback. Retain a rejected result with zero success credit and record the corrected dependency separately. Do not turn a local match into empirical, professional, production, legal, cultural, affected-party, Māori, identity, accessibility-complete, security-complete, independent-reproduction, or Stage 20 evidence.

## Frozen criteria

- `CA6866-N191`: Selecting fields does not establish disclosure consent
- `CA6866-N192`: A reversible patch does not ratify a contested correction
- `CA6866-N193`: A merge policy cannot authorize retention exceptions
- `CA6866-N194`: A source digest does not authorize rebinding a real credential
- `CA6866-N195`: Readable catalog ordering is not affected-user acceptance
- `CA6866-N196`: Passing software checks do not supply professional signoff
- `CA6866-N197`: A policy field does not establish legal interpretation
- `CA6866-N198`: A transformed label does not validate Māori terminology
- `CA6866-N199`: A source locator does not authorize an iwi data decision
- `CA6866-N200`: A provenance graph does not establish hapū stewardship consent
