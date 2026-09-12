---
name: teryn-v6922-undo-compensation-projection
description: "Review undo compensation projection records using the frozen finite contract and an isolated malformed-subject refusal."
---

# undo compensation projection

Read the exact input, expected envelope and malformed candidate in [the contract](contract.json). Apply only this finite profile; the examples establish no database or live distributed-service behavior.

The text entrypoint accepts the declared engine path and one JSON input. Invoke it through Node CommonJS stdin from the owner workflow, preserving the original subject. Compare the whole envelope, not only an ok flag. A refused malformed subject remains failed at zero original credit; the refusal check is separate.

- An empty undo history has no compensation
- An applied target record produces a restoration instruction
- Unapplied records need no compensation
- A compensation already recorded is not repeated
- Other transaction records are preserved
- Compensation order is descending LSN
- A null predecessor remains an explicit restoration value
- An absence marker is carried without being executed
- A partly compensated history retains only its outstanding step
- Input order does not determine compensation order

Retain a mismatch with its definition digest and input. Add a prospective correction and rerun only its changed dependency. Do not change a frozen expectation to match the implementation. Finite same-owner software and synthetic records only. No empirical, professional, production, identity, cultural, Maori-authority, independent-reproduction or Stage 20 credit.
