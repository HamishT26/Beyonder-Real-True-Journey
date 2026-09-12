---
name: teryn-v6922-bounded-pn-counter
description: "Review bounded pn counter records using the frozen finite contract and an isolated malformed-subject refusal."
---

# bounded pn counter

Read the exact input, expected envelope and malformed candidate in [the contract](contract.json). Apply only this finite profile; the examples establish no database or live distributed-service behavior.

The text entrypoint accepts the declared engine path and one JSON input. Invoke it through Node CommonJS stdin from the owner workflow, preserving the original subject. Compare the whole envelope, not only an ok flag. A refused malformed subject remains failed at zero original credit; the refusal check is separate.

- An empty counter state has zero total
- One positive component contributes its declared count
- One negative component produces a signed total
- Positive and negative components remain separately visible
- Replica components merge by maximum rather than addition
- Disjoint actor components contribute separately
- Repeated counter snapshots do not double count
- Opposing maxima can yield zero
- An explicit zero component remains attributable
- Three replica maps preserve their independent extrema

Retain a mismatch with its definition digest and input. Add a prospective correction and rerun only its changed dependency. Do not change a frozen expectation to match the implementation. Finite same-owner software and synthetic records only. No empirical, professional, production, identity, cultural, Maori-authority, independent-reproduction or Stage 20 credit.
