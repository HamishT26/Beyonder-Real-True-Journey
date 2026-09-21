---
name: ghc-family-binary-code-punctured-code-v1
description: Use for the punctured-code operation on explicit small systematic binary codes.
---

# punctured-code

Delete the selected coordinate from every codeword and deduplicate the image; measure any dimension loss.

Use the paired caller `ghc_family_binary_code_pair_07.txt` with one JSON request path. The request has exactly `op` and `profile`. A profile supplies `profile_id`, integer `n` and `k`, systematic binary `matrix`, binary `message` and `received`, distinct `erased` coordinates, one `coordinate`, `evidence_class` equal to `synthetic`, and integer `physical_observations` equal to zero. Coordinates begin at zero. Bounds are 2 <= n <= 8 and 1 <= k <= min(n,5). Boolean values are not binary integers.

Read the operation definition and example profile from the phase plan. Preserve all tied answers and distinguish puncturing from shortening. The response includes operation, profile, state, result and evidence scope. A malformed request returns `rejected` and CLI status 2; it does not execute a physical or identity action.

Validate a bounded accepting request and an adverse matrix before reuse. Keep the paired caller and its core dependency together. Recovery changes only an unsealed affected copy and retains failed evidence.

Finite synthetic same-owner evidence; no independent reproduction, empirical, production, identity, professional, legal, cultural, Maori authority, consciousness, personhood or Stage 20 claim.
