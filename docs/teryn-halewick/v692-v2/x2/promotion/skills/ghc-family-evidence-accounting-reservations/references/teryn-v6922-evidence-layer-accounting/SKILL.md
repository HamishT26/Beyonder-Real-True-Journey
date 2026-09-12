---
name: teryn-v6922-evidence-layer-accounting
description: "Review evidence layer accounting records using the frozen finite contract and an isolated malformed-subject refusal."
---

# evidence layer accounting

Read the exact input, expected envelope and malformed candidate in [the contract](contract.json). Apply only this finite profile; the examples establish no database or live distributed-service behavior.

The text entrypoint accepts the declared engine path and one JSON input. Invoke it through Node CommonJS stdin from the owner workflow, preserving the original subject. Compare the whole envelope, not only an ok flag. A refused malformed subject remains failed at zero original credit; the refusal check is separate.

- An empty ledger contributes zero records
- One passing witness contributes one direct witness
- A failed subject retains its negative reference
- Identical duplicate witness records are counted once
- The same label under another owner is a distinct record
- The same label under another phase is a distinct record
- Multiple witnesses can support one scoped method
- Failure and refusal pass can share one retained negative
- Conflicting reused witness identifiers block aggregation
- Distinct methods retain their own support counts

Retain a mismatch with its definition digest and input. Add a prospective correction and rerun only its changed dependency. Do not change a frozen expectation to match the implementation. Finite same-owner software and synthetic records only. No empirical, professional, production, identity, cultural, Maori-authority, independent-reproduction or Stage 20 credit.
