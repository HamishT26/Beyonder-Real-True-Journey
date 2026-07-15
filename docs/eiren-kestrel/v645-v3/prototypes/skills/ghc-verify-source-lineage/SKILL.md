---
name: ghc-verify-source-lineage
description: Verify a GHC source head, seal ancestry, single-parent lifecycle, clean owner state, and local-upstream-tracking-live-remote equality. Use before phase mutation, x2 start, closeout, sealing, or terminal handoff.
---

# Verify source lineage

1. Fetch the named branch read-only and resolve the exact expected revision.
2. Prove the seal and every declared lifecycle anchor are ancestors.
3. Require zero merge commits in the phase range and one parent for each lifecycle commit.
4. Require a clean owner lane before fast-forward or phase mutation.
5. After push, compare local, upstream, tracking, and a fresh live-remote query.
6. Refuse reset, force push, history rewrite, merge, or sibling-lane mutation.

Emit a bounded receipt; Git equality does not prove scientific truth or identity continuity.
