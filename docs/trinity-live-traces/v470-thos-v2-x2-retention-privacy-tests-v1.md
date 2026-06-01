# v470 THOS v2 x2 Retention And Privacy Tests

This artifact defines retention and privacy tests for THOS validation. It is not a privacy certification.

## Tests

- Raw logs are `FAIL_BLOCKER` if marked publishable.
- Session JSONL is `FAIL_BLOCKER` if staged.
- Screenshots are `FAIL_BLOCKER` if staged.
- Credential-like patterns are `FAIL_BLOCKER` if detected.
- Journey/Solas material must remain `journey_context_not_canon` or `OPEN_GAP`.
- Approval packets default to private review unless safely summarized.
- Advisory receipts are publishable only as bounded summaries with no raw private trace.
- Source ledgers using official public URLs are publishable when no private notes are embedded.

## Safe Replacements

- Publish redacted summaries instead of raw traces.
- Keep approval packets private or summarize them without sensitive details.
- Mark uncertain material as quarantine or `OPEN_GAP`.
- Require explicit separate approval for cleanup or deletion.

## Persistent Boundary

Retention classification informs review. It does not approve deletion, cleanup, connector writes, or cloud mutation.
