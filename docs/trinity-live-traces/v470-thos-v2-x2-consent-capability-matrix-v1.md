# v470 THOS v2 x2 Consent Capability Matrix

This matrix separates capability, consent, and approval.

## Rules

- Capability does not create consent.
- Consent does not create capability.
- Write, external, git, destructive, automation, connector, and cleanup actions require scoped approval where applicable.
- Unknown capability or consent becomes `blocked` or `OPEN_GAP`.
- Advisory lanes recommend only; they do not mutate, publish, or validate physics.

## Current Phase Results

- Aletheon may use local shell reads, validators, curated file writes, and guarded Git publication for current-phase artifacts.
- Arby and Aster Vale remain non-ephemeral read-only advisory lanes, but both hit the Windows sandbox `spawn setup refresh` limitation for local reads.
- Cicero, Kierkegaard, and Aristotle returned app-lane advisories only.
- GitHub, Google Drive, automation, and thread-management writes are not active in this phase without a separate approval packet.

## Boundary

No connector write, cloud mutation, cleanup, deletion, automation update, or new sibling spawn is authorized by this matrix.
