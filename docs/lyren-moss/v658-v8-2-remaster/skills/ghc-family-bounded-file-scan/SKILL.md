---
name: ghc-family-bounded-file-scan
description: Select and scan at most the latest 5000 currently tracked repository paths deterministically. Use for bounded privacy-pattern triage that must disclose selection order, byte caps, review candidates, and non-exhaustive assurance.
---

# Bounded file scan

1. Require a verified clean owner lane at the exact intended Git head.
2. Run `python -X utf8 scripts/ghc_family_latest_tracked_file_scan.py --output <owner-receipt.json>` from the repository root.
3. Verify the ordered-path digest, selected-file count, class counts, byte limits, and any review candidates.
4. Treat candidate matches as triage only; never publish matched secrets or private values.
5. Do not call the result privacy-complete, security-complete, accessibility-complete, or independent review.

The scan is bounded owner-local workflow evidence and grants no authority to delete, expose, or mutate repository content.
