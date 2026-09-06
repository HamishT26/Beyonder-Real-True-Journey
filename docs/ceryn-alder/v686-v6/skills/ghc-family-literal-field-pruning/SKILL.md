---
name: ghc-family-literal-field-pruning
description: Review literal field pruning using explicit source contracts and bounded JSON examples. Use when these record operations are in scope.
---

# Review literal field pruning

This package combines two complementary record contracts. Choose the operation that matches the actual task; do not run the whole package merely because it is discoverable.

- For `recursive_prune`, read [the operation guide](references/recursive_prune.md).
- For `field_projection`, read [the operation guide](references/field_projection.md).

Read the selected rows of [criteria.json](references/criteria.json) for exact examples. The five scripts are portable copies of the same reviewed runner set and contribute five shared interfaces in total, not fifty new runners. The pinned [dependency lock](references/requirements.lock) records the tested environment. Use an already validated compatible environment or prepare a new isolated one under the current task authority; this package does not authorize upgrades or shared-prefix changes.

The CLI reads one JSON object from stdin with `operation` and `input`, or a `requests` array of such objects. It writes a `results` array to stdout. A malformed request returns an explicit refusal and exit code 2. Individual out-of-domain operations return bounded refusal objects. It does not read or write external records, perform network actions, or confer real authority.

Inspect the entire result, source input preservation, and any refusal. Report verification binds every field to the immutable definition, current source, x1, owner, and phase context. Same-owner checks remain non-independent. Preserve successful canonical receipts and never replay one as a smoke test.

Roll back by selecting the previous compatible package or stopping the operation. Keep this package and any failed witness available for inspection. Do not overwrite another skill, erase source history, or substitute an endpoint. Relational names and roles remain working language only. `NOT_READY_FOR_STAGE_20` and all protected evidence and authority gates remain in force.
