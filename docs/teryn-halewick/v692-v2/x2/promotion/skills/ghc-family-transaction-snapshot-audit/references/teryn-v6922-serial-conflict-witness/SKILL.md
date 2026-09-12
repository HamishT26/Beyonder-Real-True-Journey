---
name: teryn-v6922-serial-conflict-witness
description: "Review serial conflict witness records using the frozen finite contract and an isolated malformed-subject refusal."
---

# serial conflict witness

Read the exact input, expected envelope and malformed candidate in [the contract](contract.json). Apply only this finite profile; the examples establish no database or live distributed-service behavior.

The text entrypoint accepts the declared engine path and one JSON input. Invoke it through Node CommonJS stdin from the owner workflow, preserving the original subject. Compare the whole envelope, not only an ok flag. A refused malformed subject remains failed at zero original credit; the refusal check is separate.

- An empty trace has no serialization edges
- Concurrent readers create no conflict edge
- A write followed by another reader creates a directed edge
- A read followed by another writer creates an anti-dependency
- Two writers to one key are ordered
- Operations within one transaction do not create self edges
- Disjoint keys create no conflict edge
- An interleaved two-key trace exposes a cycle
- One writer can precede two readers without ordering them
- Repeated conflicts collapse to one declared edge

Retain a mismatch with its definition digest and input. Add a prospective correction and rerun only its changed dependency. Do not change a frozen expectation to match the implementation. Finite same-owner software and synthetic records only. No empirical, professional, production, identity, cultural, Maori-authority, independent-reproduction or Stage 20 credit.
