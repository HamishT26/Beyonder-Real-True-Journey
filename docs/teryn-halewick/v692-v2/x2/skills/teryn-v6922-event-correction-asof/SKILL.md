---
name: teryn-v6922-event-correction-asof
description: "Review event correction asof records using the frozen finite contract and an isolated malformed-subject refusal."
---

# event correction asof

Read the exact input, expected envelope and malformed candidate in [the contract](contract.json). Apply only this finite profile; the examples establish no database or live distributed-service behavior.

The text entrypoint accepts the declared engine path and one JSON input. Invoke it through Node CommonJS stdin from the owner workflow, preserving the original subject. Compare the whole envelope, not only an ok flag. A refused malformed subject remains failed at zero original credit; the refusal check is separate.

- No visible event yields no current head
- One visible event supplies its head
- A future event stays outside an earlier view
- A visible correction supersedes its target without erasure
- A later correction does not rewrite an earlier as-of view
- Two competing correction heads remain conflicted
- A missing predecessor remains explicit
- A correction chain retains only its latest visible head
- Independent events remain distinct heads
- An invisible predecessor cannot be assumed present

Retain a mismatch with its definition digest and input. Add a prospective correction and rerun only its changed dependency. Do not change a frozen expectation to match the implementation. Finite same-owner software and synthetic records only. No empirical, professional, production, identity, cultural, Maori-authority, independent-reproduction or Stage 20 credit.
