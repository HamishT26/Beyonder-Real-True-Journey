# GHC Family Method Flow State

- Phase: v687-v3-final
- Owner: Sable Rook
- Methods: 5
- Passing witnesses: 5
- Failed witnesses retained: 5

## Preferred methods

### SR6873-POSTEVID-M001 — Resume-only collision-free promotion

- Trigger: post-evidence collision-free promotion; partial persisted state
- Method: Inspect exact destinations, validate the persisted skill, and copy only still-absent destinations with per-item acknowledgement.
- Recurrence guard: Inspect every destination before resuming and never overwrite an existing skill or runner.
- Rollback: Stop promotion; keep immutable evidence and any verified collision-free copy without deleting it.
- Witnesses: SR6873-POSTEVID-W001-F, SR6873-POSTEVID-W001-P

### SR6873-FINAL-M001 — Substantive overview floor recovery

- Trigger: generated final overview; frozen 1500-word minimum
- Method: Expand the integrated overview with substantive lifecycle, falsifier, and nonpromotion detail before repeating the bounded final test selection.
- Recurrence guard: Measure the generated overview after every final rebuild and require substantive content rather than padding.
- Rollback: Keep the failed 1382-word witness and stop finalization if the expanded overview does not remain within the 100000-word ceiling.
- Witnesses: SR6873-FINAL-W001-F, SR6873-FINAL-W001-P

### SR6873-FINAL-M002 — Exact scanner-definition adjudication

- Trigger: five-class scan; regex source definitions appear in immutable owner files
- Method: Classify scanner syntax only for the four exact owner scanner-definition filenames while leaving every other candidate eligible for payload confirmation.
- Recurrence guard: Use an exact filename allowlist for scanner implementations and never exempt a directory, suffix, or arbitrary source file.
- Rollback: Retain the eight-hit failed scan and stop finalization if any non-definition candidate remains confirmed.
- Witnesses: SR6873-FINAL-W002-F, SR6873-FINAL-W002-P

### SR6873-FINAL-M003 — Semantic JSON corpus gate

- Trigger: strict phase JSON parse; brittle cardinality assertion
- Method: Parse every discovered phase JSON document and assert required lifecycle artifacts instead of relying on a brittle raw-cardinality threshold.
- Recurrence guard: Bind corpus validation to parseability and named required artifacts; report cardinality without treating growth as quality.
- Rollback: Retain the 146-document failed witness and stop if any discovered JSON fails strict parsing or a required lifecycle artifact is absent.
- Witnesses: SR6873-FINAL-W003-F, SR6873-FINAL-W003-P

### SR6873-FINAL-M004 — Installed Method Flow verb discovery

- Trigger: Method Flow state change; unfamiliar installed CLI
- Method: Read the installed runner help and use its exact set-state subcommand rather than assuming a transition alias.
- Recurrence guard: Inspect the installed command help before invoking an unfamiliar Method Flow lifecycle verb.
- Rollback: Leave the ledger unchanged and retain the rejected command as a read-only zero-credit failure.
- Witnesses: SR6873-FINAL-W004-F, SR6873-FINAL-W004-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
