---
name: teryn-v6922-snapshot-visible-versions
description: "Review snapshot visible versions records using the frozen finite contract and an isolated malformed-subject refusal."
---

# snapshot visible versions

Read the exact input, expected envelope and malformed candidate in [the contract](contract.json). Apply only this finite profile; the examples establish no database or live distributed-service behavior.

The text entrypoint accepts the declared engine path and one JSON input. Invoke it through Node CommonJS stdin from the owner workflow, preserving the original subject. Compare the whole envelope, not only an ok flag. A refused malformed subject remains failed at zero original credit; the refusal check is separate.

- An empty version history yields an empty snapshot
- A version later than the snapshot remains invisible
- A version at the exact snapshot boundary is visible
- The greatest visible revision wins
- A visible tombstone hides the earlier value
- A future tombstone does not hide an earlier snapshot
- A later value can follow a tombstone
- Each key has its own latest visible revision
- Null and false remain explicit stored values
- Input order does not replace revision order

Retain a mismatch with its definition digest and input. Add a prospective correction and rerun only its changed dependency. Do not change a frozen expectation to match the implementation. Finite same-owner software and synthetic records only. No empirical, professional, production, identity, cultural, Maori-authority, independent-reproduction or Stage 20 credit.
