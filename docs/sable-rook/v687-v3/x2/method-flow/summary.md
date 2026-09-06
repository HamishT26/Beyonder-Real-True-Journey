# GHC Family Method Flow State

- Phase: v687-v3-x2
- Owner: Sable Rook
- Methods: 1
- Passing witnesses: 1
- Failed witnesses retained: 1

## Preferred methods

### SR6873-X2-M001 — Complete x2 validation-delta inclusion

- Trigger: Sable v687-v3 x2 staged review; normalized-LF Git-blob manifest
- Method: Include every x2-prefixed validation artifact in the delta before hashing while self-excluding only the manifest and staged review.
- Recurrence guard: Enumerate the exact lifecycle validation prefix before computing the manifest, then compare the complete staged set.
- Rollback: Stop before commit; preserve immutable x1 and the failed staged-review receipt.
- Witnesses: SR6873-X2-W001-F, SR6873-X2-W001-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
