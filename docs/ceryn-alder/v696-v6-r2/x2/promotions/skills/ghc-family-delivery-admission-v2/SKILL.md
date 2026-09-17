---
name: ghc-family-delivery-admission-v2
description: Inspect delivery admission using four bounded JSON operations and retained evidence limits.
---

# delivery admission

Use this package for weighted_roster, exact_title_resolution, freshness_gate, authority_gate. It consolidates four exact operation guides; the original local callers remain compatible. Read references/merge-sources.json for source hashes and phase examples.

Run Node with family-evidence-observatory-v2/runners/delivery-admission.txt beneath the configured D-first global-tools root. Supply one UTF-8 JSON object on standard input with op and input. The interface returns one complete disposition/op/result/boundary envelope, or a refused/code envelope and exit status two. Request bytes are capped at 262,144 and nesting at 32; records, events and projections have separate finite limits. Unknown fields and duplicate JSON keys are refused.

Before interpreting a result, distinguish a content hash from authentication, a projection from activation, a rejected subject from its passing refusal guard, and accepted delivery from completed work. Unknown or pending delivery requires status reconciliation. This package performs no network, account, credential or task mutation and cannot itself authorize a send.

On a failed result, retain the source input and exact package version. Make the smallest compatible correction and retain a separate witness. Use the previous compatible caller for rollback; do not erase a predecessor or overwrite this immutable package. The current family workflow and the latest direct user instruction govern real actions.

This is same-owner synthetic software evidence, not independent reproduction, empirical physics, production identity assurance, professional or public authority, complete accessibility/security, consciousness or Stage 20 readiness.
