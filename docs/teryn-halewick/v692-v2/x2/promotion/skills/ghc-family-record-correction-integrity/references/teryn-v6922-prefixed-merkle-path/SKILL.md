---
name: teryn-v6922-prefixed-merkle-path
description: "Review prefixed merkle path records using the frozen finite contract and an isolated malformed-subject refusal."
---

# prefixed merkle path

Read the exact input, expected envelope and malformed candidate in [the contract](contract.json). Apply only this finite profile; the examples establish no database or live distributed-service behavior.

The text entrypoint accepts the declared engine path and one JSON input. Invoke it through Node CommonJS stdin from the owner workflow, preserving the original subject. Compare the whole envelope, not only an ok flag. A refused malformed subject remains failed at zero original credit; the refusal check is separate.

- A singleton leaf matches its declared root
- An empty UTF-8 leaf has its own prefixed hash
- A left leaf can be bound to a two-leaf root
- A right leaf preserves sibling order
- A wrong sibling direction does not verify
- A changed leaf does not borrow the original path
- A mismatched root remains unverified
- A two-level path folds from leaf toward root
- The third leaf uses the complete left subtree
- Unicode normalization is not silently applied to leaf bytes

Retain a mismatch with its definition digest and input. Add a prospective correction and rerun only its changed dependency. Do not change a frozen expectation to match the implementation. Finite same-owner software and synthetic records only. No empirical, professional, production, identity, cultural, Maori-authority, independent-reproduction or Stage 20 credit.
