---
name: teryn-v6922-saga-compensation-order
description: "Review saga compensation order records using the frozen finite contract and an isolated malformed-subject refusal."
---

# saga compensation order

Read the exact input, expected envelope and malformed candidate in [the contract](contract.json). Apply only this finite profile; the examples establish no database or live distributed-service behavior.

The text entrypoint accepts the declared engine path and one JSON input. Invoke it through Node CommonJS stdin from the owner workflow, preserving the original subject. Compare the whole envelope, not only an ok flag. A refused malformed subject remains failed at zero original credit; the refusal check is separate.

- An empty saga has no compensation
- One completed reversible step can be listed
- An unfinished step is excluded
- A completed irreversible step stays explicitly blocked
- A chain compensates dependents before prerequisites
- A diamond compensation order is deterministic
- Independent completed steps use reverse deterministic order
- A cycle yields a structural hold
- A missing dependency yields a structural hold
- Irreversible predecessors do not erase reversible descendants

Retain a mismatch with its definition digest and input. Add a prospective correction and rerun only its changed dependency. Do not change a frozen expectation to match the implementation. Finite same-owner software and synthetic records only. No empirical, professional, production, identity, cultural, Maori-authority, independent-reproduction or Stage 20 credit.
