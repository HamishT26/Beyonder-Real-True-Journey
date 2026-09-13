---
name: ghc-family-accessible-consistency-handover-v2
description: Use four finite distributed-consistency operations with a raw-byte-bound corrected core while retaining the failed v1 entry point. Use after the v1 Buffer-serialization failure; do not treat it as production or authority evidence.
---

# ghc-family-accessible-consistency-handover-v2

Read [the retained contracts](references/contracts.md) before execution.

Allowed operations: `monotonic_reads_check`, `bounded_staleness_check`, `accessible_consistency_summary`, `handover_snapshot_projection`.

1. Preserve the complete request and select only an allowed operation.
2. Run `ghc_family_accessible_consistency_handover_v2.txt`; it binds `consistency-core-v2.txt` by raw SHA-256.
3. Compare the complete response and preserve every failed v1 witness.
4. Retain unsupported subjects separately from their passing refusal checks.
5. Use the local owner source as rollback; do not overwrite or delete v1.

Additive correction with the failed v1 entry points retained byte-for-byte. Same-owner synthetic integration evidence only; no independent reproduction, deployment, authority, complete privacy or accessibility, exhaustive security, or Stage 20 credit.
