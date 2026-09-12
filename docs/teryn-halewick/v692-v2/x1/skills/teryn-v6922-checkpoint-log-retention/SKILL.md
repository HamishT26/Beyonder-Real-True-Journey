---
name: teryn-v6922-checkpoint-log-retention
description: "Review checkpoint log retention records using the frozen finite contract and an isolated malformed-subject refusal."
---

# checkpoint log retention

Read the exact input, expected envelope and malformed candidate in [the contract](contract.json). Apply only this finite profile; the examples establish no database or live distributed-service behavior.

The text entrypoint accepts the declared engine path and one JSON input. Invoke it through Node CommonJS stdin from the owner workflow, preserving the original subject. Compare the whole envelope, not only an ok flag. A refused malformed subject remains failed at zero original credit; the refusal check is separate.

- An empty segment inventory yields no cleanup action
- Archived segments strictly before the checkpoint can be reviewed
- A segment touching the checkpoint remains retained
- Unarchived segments remain retained even when old
- An active undo floor tightens the retention boundary
- Segments before both boundaries remain review candidates
- A zero checkpoint prevents historical deletion inference
- Mixed archived and unarchived ranges remain separate
- A future segment stays retained
- The exact undo-floor endpoint stays retained

Retain a mismatch with its definition digest and input. Add a prospective correction and rerun only its changed dependency. Do not change a frozen expectation to match the implementation. Finite same-owner software and synthetic records only. No empirical, professional, production, identity, cultural, Maori-authority, independent-reproduction or Stage 20 credit.
