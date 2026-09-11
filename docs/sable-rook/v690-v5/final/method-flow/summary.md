# GHC Family Method Flow State

- Phase: v690-v5-final
- Owner: Sable Rook
- Methods: 3
- Passing witnesses: 3
- Failed witnesses retained: 3

## Preferred methods

### SR6905-FINAL-M001 — Hash-preserving final-source hold

- Trigger: x2 correction committed; untracked final-stage source exists
- Method: Move only the four exact Sable-owned files to a verified D holding directory, prove the correction clean and fresh-four-way equal, then restore the same hashes.
- Recurrence guard: Do not author final-stage source until the preceding lifecycle commit is pushed clean and fresh-four-way equal.
- Rollback: Retain the failed clean-state witness; never delete, stash, rewrite, or include premature final files in the correction commit.
- Witnesses: SR6905-FINAL-W001-F, SR6905-FINAL-W001-P

### SR6905-FINAL-M002 — Separated paired-manifest verification

- Trigger: final pair written and staged; combined wrapper lacks terminal attribution
- Method: Inspect persisted manifest/index state, then run only pair verification and diff hygiene as a bounded scalar probe.
- Recurrence guard: Keep manifest construction and verification in separate attributable commands when the owner tree is large.
- Rollback: Retain the silent wrapper and do not infer manifest parity from file existence.
- Witnesses: SR6905-FINAL-W002-F, SR6905-FINAL-W002-P

### SR6905-FINAL-M003 — Lifecycle-state-aware parent-chain assertion

- Trigger: final tests run before final commit; same test also runs at exact final
- Method: Require final-to-correction only when an expected final is supplied; always verify correction-to-evidence-to-x1-to-root.
- Recurrence guard: Branch lifecycle assertions explicitly by precommit versus exact-final state rather than applying future edges to the current head.
- Rollback: Retain the 28-of-29 failed receipt and do not invoke the canonical until the corrected final-context test passes.
- Witnesses: SR6905-FINAL-W003-F, SR6905-FINAL-W003-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
