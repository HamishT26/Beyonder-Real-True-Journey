---
name: teryn-v6922-write-ahead-redo-projection
description: "Review write ahead redo projection records using the frozen finite contract and an isolated malformed-subject refusal."
---

# write ahead redo projection

Read the exact input, expected envelope and malformed candidate in [the contract](contract.json). Apply only this finite profile; the examples establish no database or live distributed-service behavior.

The text entrypoint accepts the declared engine path and one JSON input. Invoke it through Node CommonJS stdin from the owner workflow, preserving the original subject. Compare the whole envelope, not only an ok flag. A refused malformed subject remains failed at zero original credit; the refusal check is separate.

- An empty log retains the declared base
- An uncommitted update is excluded
- A committed update can introduce a page
- An already applied LSN is skipped
- An older LSN cannot overwrite the newer page
- A newer committed LSN advances the page
- Out-of-order log input is processed by LSN
- Only declared committed transactions participate
- Committed null is retained as data
- Independent pages retain separate recovery positions

Retain a mismatch with its definition digest and input. Add a prospective correction and rerun only its changed dependency. Do not change a frozen expectation to match the implementation. Finite same-owner software and synthetic records only. No empirical, professional, production, identity, cultural, Maori-authority, independent-reproduction or Stage 20 credit.
