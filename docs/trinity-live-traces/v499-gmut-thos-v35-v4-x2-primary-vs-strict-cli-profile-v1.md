# v499 GMUT/THOS v35 v4 x2 Primary vs Strict CLI Profile

- generated_utc: `2026-06-07T07:56:22Z`
- overall_status: `PASS_STRICT_STDIN_PROFILE_PROMOTED_FOR_NEXT_X1`
- source_phase_slug: `v499-gmut-thos-v35-v4-x1`

## Comparison

The primary stdin/no-plugin CLI run structurally passed but remained below the strict elaboration target. The strict stdin/no-plugin repair run produced stronger and usable artifacts: Arby reached `3500` words, Aster Vale reached `4910` words, both retained the required category depth, and strict sensitive/path marker counts stayed at zero.

## Next Primary Profile

- Use existing CLI lanes only.
- Deliver the prompt through stdin.
- Keep the run read-only and no-plugin.
- Require 2500+ words, exact headings, and enough category items for review.
- Store raw output in temp-only space and publish only status receipts.
- Treat marker review as a precision step, not a generic-word panic button.

This promotes the strict stdin/no-plugin shape as the v499 v5 x1 primary CLI profile.
