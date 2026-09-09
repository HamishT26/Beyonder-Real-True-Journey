---
name: ghc-family-weighted-handoff-composer
description: Combine a weighted roster, cost scenario, context batches and checkpoint state into a local handoff review without sending messages.
---

# Weighted handoff composer

Use this capability when an existing GHC task needs a compact review of a weighted route. Read references/contract.json for the exact fields and references/merge-sources.json for the four retained source skills. The consolidation reuses their pure implementations and preserves their separate assumptions.

Run ghc_family_weighted_handoff_composer.py from repository scripts or the D-drive global-tools/family-capacity-lab/scripts directory with --input request.json and an optional new --output result.json. Keep both cores and the weighted route reviewer beside it. Supply the complete profile and route objects, relative_astra_cost, sizes, prefix, limit and events. Unknown fields are refused.

Inspect every component. Context units are caller supplied and are not inferred model tokens. A cost scenario is not billing evidence. An accepted checkpoint is never reset to make a resend possible. The composer performs no task lookup, message, model change, permission grant or host configuration action. Native delivery remains a separately authorized terminal action after current target guards.

If the composition fails, retain the input and result and review the failing component. A passing model does not establish empirical confirmation, real consent, public authority, independent reproduction or Stage 20 readiness.
