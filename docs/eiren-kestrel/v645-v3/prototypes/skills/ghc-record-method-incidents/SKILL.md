---
name: ghc-record-method-incidents
description: Record GHC workflow failures, bounded workaround witnesses, retry quarantine, recurrence guards, rollback, and sibling recommendations. Use whenever a command, validator, schema, or tool assumption fails.
---

# Record method incidents

1. Sanitize and record the negative before retrying.
2. Link one stable method identifier to every failed and passing witness.
3. Keep observed, candidate, validated, preferred, superseded, and deprecated states distinct.
4. Promote to preferred only with an in-scope passing witness.
5. Add a retry-quarantine condition, recurrence guard, rollback, and concise sibling recommendation.
6. Preserve failed witnesses and exclude private routes, identifiers, transcripts, credentials, paths, and application state.

Same-owner recovery is never independent reproduction.
