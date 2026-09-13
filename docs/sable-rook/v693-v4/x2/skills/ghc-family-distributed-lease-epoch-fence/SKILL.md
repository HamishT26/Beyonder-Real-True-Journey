---
name: ghc-family-distributed-lease-epoch-fence
description: Reject stale epoch or wrong-holder requests without claiming a production lock. Use for bounded synthetic distributed-consistency review with exact input and retained-refusal evidence.
---

# Reject stale epoch or wrong-holder requests without claiming a production lock.

Read [the frozen contract](references/contract.md) before using this skill.

1. Preserve the complete request with exactly `op`, `record`, and `args`.
2. Use operation `lease_epoch_fence` only for the finite synthetic data shape in the contract.
3. Run adjacent owner TXT runner `ghc_family_distributed_consistency_x2_2.txt`; it hashes its fixed trusted library before compilation.
4. Compare the complete response including `ok`, `disposition`, `value`, `error`, and `external_credit`.
5. Retain malformed subjects separately from passing refusal checks. A correction never erases its failed predecessor.

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
