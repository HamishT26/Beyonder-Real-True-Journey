---
name: teryn-v6922-optimistic-read-validation
description: "Review optimistic read validation records using the frozen finite contract and an isolated malformed-subject refusal."
---

# optimistic read validation

Read the exact input, expected envelope and malformed candidate in [the contract](contract.json). Apply only this finite profile; the examples establish no database or live distributed-service behavior.

The text entrypoint accepts the declared engine path and one JSON input. Invoke it through Node CommonJS stdin from the owner workflow, preserving the original subject. Compare the whole envelope, not only an ok flag. A refused malformed subject remains failed at zero original credit; the refusal check is separate.

- An empty read set has no version conflict
- An unchanged read version remains valid
- A newer current revision conflicts with the read
- An expected absence matches actual absence
- A newly present zero revision violates an absence read
- A missing current key conflicts with a prior version
- Revision zero is a value rather than missingness
- One conflict does not erase the other read evidence
- Multiple conflict labels have deterministic order
- Unrelated current keys do not enter the read conflict set

Retain a mismatch with its definition digest and input. Add a prospective correction and rerun only its changed dependency. Do not change a frozen expectation to match the implementation. Finite same-owner software and synthetic records only. No empirical, professional, production, identity, cultural, Maori-authority, independent-reproduction or Stage 20 credit.
