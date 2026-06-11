# v507 GMUT/THOS v43 v6 x1 Arby Repair2 Stderr Phase-Drift Blocker

- overall_status: `OPEN_GAP_REPAIR2_STDERR_PHASE_DRIFT`
- lane: `Arby`
- repair attempt: `repair2`
- process stopped: `true`
- expected last-message file ready: `false`
- stderr stream stopped growing: `true`
- raw stderr published: `false`

## Classification

Repair2 is not a valid v507 v6 x1 elaboration repair. The temp-only stderr stream contained older advisory material and did not contain the required v507 heading set, while the expected last-message file remained empty.

## Next Retry

- Use the strict stdin launcher.
- Keep the read-only authorization active.
- Disable plugins for the retry.
- Publish status-only receipts only.

## Boundary

No raw lane text, raw transport, raw stderr, screenshots, credentials, local absolute paths, GMUT validation, final physics claim, consciousness proof, or canon-promotion claim is published.
