---
name: teryn-v6922-two-phase-commit-projection
description: "Review two phase commit projection records using the frozen finite contract and an isolated malformed-subject refusal."
---

# two phase commit projection

Read the exact input, expected envelope and malformed candidate in [the contract](contract.json). Apply only this finite profile; the examples establish no database or live distributed-service behavior.

The text entrypoint accepts the declared engine path and one JSON input. Invoke it through Node CommonJS stdin from the owner workflow, preserving the original subject. Compare the whole envelope, not only an ok flag. A refused malformed subject remains failed at zero original credit; the refusal check is separate.

- No participant set authorizes no commit
- Prepared participants wait for a coordinator decision
- A declared commit with all prepared votes passes only the snapshot predicate
- An unknown vote keeps a commit decision waiting
- An abort vote conflicts with a declared commit
- An explicit abort remains an abort snapshot
- An abort decision conflicts with an already committed participant
- A committed participant without a recorded decision is inconsistent
- An abort vote without a decision demands an abort review
- Prepared and committed votes can agree with the declared commit

Retain a mismatch with its definition digest and input. Add a prospective correction and rerun only its changed dependency. Do not change a frozen expectation to match the implementation. Finite same-owner software and synthetic records only. No empirical, professional, production, identity, cultural, Maori-authority, independent-reproduction or Stage 20 credit.
