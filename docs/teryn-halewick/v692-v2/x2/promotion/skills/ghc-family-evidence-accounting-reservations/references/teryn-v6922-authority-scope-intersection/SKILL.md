---
name: teryn-v6922-authority-scope-intersection
description: "Review authority scope intersection records using the frozen finite contract and an isolated malformed-subject refusal."
---

# authority scope intersection

Read the exact input, expected envelope and malformed candidate in [the contract](contract.json). Apply only this finite profile; the examples establish no database or live distributed-service behavior.

The text entrypoint accepts the declared engine path and one JSON input. Invoke it through Node CommonJS stdin from the owner workflow, preserving the original subject. Compare the whole envelope, not only an ok flag. A refused malformed subject remains failed at zero original credit; the refusal check is separate.

- No approval records imply no declared intersection
- A matching declared scope still grants no real authority
- An unlisted action stays outside the intersection
- All required scopes must overlap
- An expired required record blocks the whole intersection
- A revoked required record cannot be dropped to widen scope
- The expiry endpoint is not current permission
- Several unusable required records remain separately visible
- Scope union must not be mistaken for intersection
- No requested action creates no implicit execution

Retain a mismatch with its definition digest and input. Add a prospective correction and rerun only its changed dependency. Do not change a frozen expectation to match the implementation. Finite same-owner software and synthetic records only. No empirical, professional, production, identity, cultural, Maori-authority, independent-reproduction or Stage 20 credit.
