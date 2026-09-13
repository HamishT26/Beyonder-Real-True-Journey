---
name: ghc-family-distributed-authority-reservations
description: Use four finite distributed-consistency operations with exact source bindings, complete response comparison, and retained refusal evidence. Use when the named synthetic operation group is needed; do not use it as production or authority evidence.
---

# ghc-family-distributed-authority-reservations

Read [the bound contracts](references/contracts.md) before execution.

Allowed operations: `lease_epoch_fence`, `causal_claim_firewall`, `real_cluster_observation_gate`, `distributed_release_authority_gate`.

1. Preserve the complete UTF-8 JSON request and select only an allowed operation.
2. Run `ghc_family_distributed_authority_reservations.txt`; it hashes the fixed trusted TXT core before compilation.
3. Compare the complete response and preserve the source request.
4. Retain unsupported or malformed subjects separately from passing refusal checks.
5. Fall back to the retained local owner skill if the merged entry point is unavailable; do not delete a compatibility source.

Same-owner synthetic integration evidence only. No external deployment, independent reproduction, scientific, professional, legal, cultural, Maori, affected-party, identity, complete privacy or accessibility, exhaustive security, production or Stage 20 credit. NOT_READY_FOR_STAGE_20.
