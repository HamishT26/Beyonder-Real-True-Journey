---
name: ghc-family-chess-position-move-graph
description: Validate synthetic position-component and move-tree graph records. Use for position_graph and move_tree fixtures with explicit nodes, edges, cycle refusal, and no engine execution.
---

# GHC Family Chess Position and Move Graph

Invoke `scripts/ghc_family_chess_record_skill.py FIXTURE.json`. The package allowlist is `position_graph` and `move_tree` only.

Accept declared-node graphs with bounded valid edges. A move tree must be acyclic and give each non-root at most one parent. Reject undeclared endpoints, self edges, duplicate nodes, cycles, multiple parents, unknown fields, or any other operation. Keep accepting and rejecting receipts separate.

Graph structure is synthetic software evidence, not a real position, legal variation, engine result, strategy, rating, tournament or professional ruling, participant evidence, deployment, legal/cultural/Maori authority, independent reproduction, completeness, consciousness, Theory of Everything, or Stage 20. Use reversible additive rollback.
