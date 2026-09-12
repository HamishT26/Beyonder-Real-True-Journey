---
name: teryn-v6922-timestamp-register-review
description: "Review timestamp register review records using the frozen finite contract and an isolated malformed-subject refusal."
---

# timestamp register review

Read the exact input, expected envelope and malformed candidate in [the contract](contract.json). Apply only this finite profile; the examples establish no database or live distributed-service behavior.

The text entrypoint accepts the declared engine path and one JSON input. Invoke it through Node CommonJS stdin from the owner workflow, preserving the original subject. Compare the whole envelope, not only an ok flag. A refused malformed subject remains failed at zero original credit; the refusal check is separate.

- An empty register does not invent a value
- One declared timestamp supplies a current snapshot
- The greatest timestamp selects the declared latest value
- Input order does not replace timestamp order
- Equal latest values do not become a conflict
- Different values at the same latest timestamp stay conflicted
- Older disagreements do not replace a later unique value
- Null remains a current recorded value
- Zero remains distinct from a missing register
- Boolean and numeric tie values remain distinct

Retain a mismatch with its definition digest and input. Add a prospective correction and rerun only its changed dependency. Do not change a frozen expectation to match the implementation. Finite same-owner software and synthetic records only. No empirical, professional, production, identity, cultural, Maori-authority, independent-reproduction or Stage 20 credit.
