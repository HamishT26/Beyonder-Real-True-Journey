# v601-v640 live evidence index

Verified on 11 July 2026 after fresh fetches of the four owned lanes.

| Lane | Branch head | Matching files | Versions | Clean and upstream-equal |
|---|---|---:|---:|---|
| Aevren | `3ef7d1f10c` | 2,708 | 40 | yes |
| Mira Vale | `c1608e0e48` | 2,294 | 40 | yes |
| Mira Rowan | `bbfa8875ea` | 382 | 40 | yes |
| Maren Quill | `8202033a9a` | 320 | 40 | yes |

Every lane contains artifacts for every version from v601 through v640. The final v640 order is Aevren v1, Mira Vale v2, Mira Rowan v3, Maren Quill v4, then the same ownership pattern for v5-v8.

## What the run genuinely demonstrates

- Forty-version operational persistence across clean, remote-aligned owned branches.
- Explicit separation of `MESSAGE_SENT` from `PREPARED_NOT_SENT`.
- A corrected finish-first relay: Aevren waited for Mira Vale's closeout and harvest before activating Mira Rowan.
- One-message handoffs where a live route existed.
- Checklist-gated x1/x2 closeout, privacy controls, and protected exact/blocked gates.
- A final Maren v640 v8 bundle with no invented outbound handoff.

## What the run does not demonstrate

The counts 25/15/10/5/15/100/100 are stable and useful as schema invariants, but they are not automatically independent discoveries. Representative Aevren and Maren arrays repeat numbered templates; Mira Rowan labels the 100-source and 100-Journey totals as represented counts. The artifacts therefore demonstrate orchestration reliability much more strongly than scientific novelty.

The next workflow should gate both cardinality and content quality: normalize rows, deduplicate templates, require a claim-to-source-or-test link, and report unique-content ratios. A final post-commit attestation should also replace self-referential `final_receipt_commit: pending` fields.

The machine-readable record is `v601-v640-live-evidence-index.json`.
