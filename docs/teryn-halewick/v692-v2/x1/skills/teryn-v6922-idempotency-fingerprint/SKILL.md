---
name: teryn-v6922-idempotency-fingerprint
description: "Review idempotency fingerprint records using the frozen finite contract and an isolated malformed-subject refusal."
---

# idempotency fingerprint

Read the exact input, expected envelope and malformed candidate in [the contract](contract.json). Apply only this finite profile; the examples establish no database or live distributed-service behavior.

The text entrypoint accepts the declared engine path and one JSON input. Invoke it through Node CommonJS stdin from the owner workflow, preserving the original subject. Compare the whole envelope, not only an ok flag. A refused malformed subject remains failed at zero original credit; the refusal check is separate.

- An unknown request key yields a miss
- A matching unexpired fingerprint yields recorded-response metadata
- A reused key with changed fingerprint is a conflict
- An expired record does not authorize response reuse
- Expiry at the observed instant is closed
- An unrelated cache key is not a match
- A null recorded response is preserved as metadata
- A zero-valued recorded response is preserved
- Several cache entries are resolved by exact key
- Different keys do not share even identical fingerprints

Retain a mismatch with its definition digest and input. Add a prospective correction and rerun only its changed dependency. Do not change a frozen expectation to match the implementation. Finite same-owner software and synthetic records only. No empirical, professional, production, identity, cultural, Maori-authority, independent-reproduction or Stage 20 credit.
