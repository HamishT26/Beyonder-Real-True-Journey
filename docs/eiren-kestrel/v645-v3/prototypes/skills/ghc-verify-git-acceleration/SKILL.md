---
name: ghc-verify-git-acceleration
description: Verify Git multi-pack-index, commit-graph, and reachability-bitmap behavior in disposable repositories. Use when testing acceleration integrity without touching canonical object storage or sibling lanes.
---

# Verify Git acceleration

1. Create one additive temporary repository outside every canonical worktree.
2. Add deterministic synthetic commits and packs only.
3. Run supported commit-graph and multi-pack-index write and verify operations.
4. Capture valid and deliberately missing or malformed fixture outcomes without modifying canonical refs or objects.
5. Compare canonical head before and after; require equality.
6. Remove or retain the temporary fixture only under the declared cleanup rule.

Temporary-fixture success is same-owner software evidence, not repository-wide or independent security certification.
