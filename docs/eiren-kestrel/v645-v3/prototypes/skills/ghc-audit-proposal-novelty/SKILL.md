---
name: ghc-audit-proposal-novelty
description: Audit proposed GHC phase titles and mission surfaces against frozen prior proposals. Use before x1 freeze when proposal identity, semantic duplication, or predecessor counts must be checked without rewriting history.
---

# Audit proposal novelty

1. Load every frozen prior `x1-proposals.json`; exclude the active phase using resolved paths.
2. Require the predecessor count and unique identifier count to match the verified baton.
3. Reject exact normalized-title collisions. Use token similarity only to triage a manual semantic comparison.
4. Record the three nearest prior titles, a concrete novelty distinction, and any unresolved overlap.
5. Stop x1 freeze on count drift, missing lineage, or unresolved duplication.

Never treat a similarity score as semantic proof or delete an earlier proposal.
