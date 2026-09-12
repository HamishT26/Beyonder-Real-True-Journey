---
name: teryn-v6922-version-vector-join
description: "Review version vector join records using the frozen finite contract and an isolated malformed-subject refusal."
---

# version vector join

Read the exact input, expected envelope and malformed candidate in [the contract](contract.json). Apply only this finite profile; the examples establish no database or live distributed-service behavior.

The text entrypoint accepts the declared engine path and one JSON input. Invoke it through Node CommonJS stdin from the owner workflow, preserving the original subject. Compare the whole envelope, not only an ok flag. A refused malformed subject remains failed at zero original credit; the refusal check is separate.

- An empty vector collection has an empty join
- A single vector is retained
- The larger component survives two replica states
- Disjoint components are retained together
- Explicit zero components remain explicit
- Repeated identical vectors are idempotent
- Three states merge componentwise
- Reordering replicas leaves the same declared join
- An empty replica state contributes no invented component
- Concurrent incomparable states preserve both maxima

Retain a mismatch with its definition digest and input. Add a prospective correction and rerun only its changed dependency. Do not change a frozen expectation to match the implementation. Finite same-owner software and synthetic records only. No empirical, professional, production, identity, cultural, Maori-authority, independent-reproduction or Stage 20 credit.
