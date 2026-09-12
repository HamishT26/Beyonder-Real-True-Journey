---
name: teryn-v6922-observed-remove-set
description: "Review observed remove set records using the frozen finite contract and an isolated malformed-subject refusal."
---

# observed remove set

Read the exact input, expected envelope and malformed candidate in [the contract](contract.json). Apply only this finite profile; the examples establish no database or live distributed-service behavior.

The text entrypoint accepts the declared engine path and one JSON input. Invoke it through Node CommonJS stdin from the owner workflow, preserving the original subject. Compare the whole envelope, not only an ok flag. A refused malformed subject remains failed at zero original credit; the refusal check is separate.

- An empty observed-remove set has no members
- One unremoved tag makes its element visible
- Removing the observed tag hides that occurrence
- A concurrent fresh tag preserves the element
- Removing every observed tag hides the element
- Unknown removed tags do not erase other adds
- Different elements retain independent tags
- One removed element does not hide another
- Duplicate removal observations do not multiply effects
- Tag identity is not inferred from element spelling

Retain a mismatch with its definition digest and input. Add a prospective correction and rerun only its changed dependency. Do not change a frozen expectation to match the implementation. Finite same-owner software and synthetic records only. No empirical, professional, production, identity, cultural, Maori-authority, independent-reproduction or Stage 20 credit.
