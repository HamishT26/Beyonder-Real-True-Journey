---
name: teryn-v6922-lease-fencing-sequence
description: "Review lease fencing sequence records using the frozen finite contract and an isolated malformed-subject refusal."
---

# lease fencing sequence

Read the exact input, expected envelope and malformed candidate in [the contract](contract.json). Apply only this finite profile; the examples establish no database or live distributed-service behavior.

The text entrypoint accepts the declared engine path and one JSON input. Invoke it through Node CommonJS stdin from the owner workflow, preserving the original subject. Compare the whole envelope, not only an ok flag. A refused malformed subject remains failed at zero original credit; the refusal check is separate.

- No event creates no lease
- A higher epoch establishes a declared lease
- A write without a prior grant is denied
- The current holder and epoch can pass the write predicate
- An old epoch is fenced after a newer grant
- A different holder cannot use the current epoch
- A repeated grant epoch is denied
- A lower grant does not rewind the epoch
- A higher ungranted write epoch is not accepted
- A current replacement holder may write after fencing

Retain a mismatch with its definition digest and input. Add a prospective correction and rerun only its changed dependency. Do not change a frozen expectation to match the implementation. Finite same-owner software and synthetic records only. No empirical, professional, production, identity, cultural, Maori-authority, independent-reproduction or Stage 20 credit.
