---
name: ghc-family-binary-code-encoding-v1
description: Evaluate exact encoding contracts for small systematic binary codes with retained ambiguity and explicit evidence limits.
---

# Binary-code encoding

Select this group for: minimum-distance, weight-distribution, systematic-encode, parity-check.

Use `ghc_family_binary_code_encoding.txt` from the matching group in the GHC-Archives/family-tools/binary-code-v1 tool bank on D:. Run it with the existing Python interpreter and one JSON request path. Keep the core and extension TXT dependencies together.

The request has exactly `op` and `profile`. A profile contains `profile_id`, integer `n` and `k`, systematic binary `matrix`, binary `message` and `received`, distinct zero-based `erased` coordinates, integer `coordinate`, `evidence_class` set to `synthetic`, and integer `physical_observations` set to zero. Bounds: 2 <= n <= 8 and 1 <= k <= min(n,5). Reject boolean bits, ragged matrices, unknown fields and physical-evidence claims.

The response retains all minimum-distance ties, all consistent erasure completions, and the four evidence dispositions. The exact integer transform can be checked against direct dual enumeration; passing arithmetic is not channel validation. Read the operation-specific phase definition before choosing an action.

Use an accepting and an adverse bounded request when adopting the caller for new work. CLI status 2 means the subject was rejected, with zero completion credit. Recover only an affected unsealed copy; never overwrite a preexisting global destination silently. Installation and byte parity do not authorize real-world action.

Finite synthetic same-owner evidence; no independent reproduction, empirical, production, identity, professional, legal, cultural, Maori authority, consciousness, personhood or Stage 20 claim.
