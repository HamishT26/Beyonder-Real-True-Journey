---
name: ghc-family-matroid-minmax-bound
description: Check finite rank-sum bounds and corrections using explicit finite matroid pairs and complete JSON outputs.
---

# Check finite rank-sum bounds and corrections

Use this skill for rank split bound, minmax certificate, common restriction, pair correction. The public runner is global-tools/family-common-independent-lab/runners/ghc_family_matroid_minmax_bound.txt. Resolve that logical path under the current D-first archive root. Supply a JSON request with operation and input on stdin to an installed CommonJS Node loader. Load the .txt runner with require rather than relying on direct filename module inference.

Inputs contain pair with ground, left and right. Each family explicitly lists every independent set. Ground is bounded by eight distinct lower-case synthetic labels; weights are integers within one million and align with sorted ground order. The empty set, complete heredity and augmentation checks precede computation. Extra fields, duplicate labels or sets, missing fields and unsupported operations are refused. Keep the request unchanged and compare the entire returned envelope, including authority false.

Set lists use shortlex order. For exchange graphs, a left-matroid swap points from the selected element to the outside element; a right-matroid swap points back. Use a shortest path before toggling; arbitrary long alternating walks do not carry the same guarantee. Weighted comparisons maximize weight, then cardinality, then lexical order. The engine is deliberately bounded; it makes no scaling claim for large oracle-defined systems.

A common maximal set need not be a maximum set. A greedy weighted selection may be worse than a common optimum. The rank-sum calculation is a finite certificate check using classical matroid intersection. Selection gaps and authority holds remain open or exact-gated even when their JSON envelopes validate. A rejected subject stays failed; the rejection guard is a separate passing witness.

Merged source guides: docs/saelin-reed/v691-v4/x2/skills/rank_split_bound/SKILL.md, docs/saelin-reed/v691-v4/x2/skills/minmax_certificate/SKILL.md, docs/saelin-reed/v691-v4/x2/skills/common_restriction/SKILL.md, docs/saelin-reed/v691-v4/x2/skills/pair_correction/SKILL.md. Merged paired runner sources: docs/saelin-reed/v691-v4/x2/runners/runner-2.txt, docs/saelin-reed/v691-v4/x2/runners/runner-3.txt, docs/saelin-reed/v691-v4/x2/runners/runner-4.txt. Their exact hashes are in the owner promotion receipt. Example frozen contract: SR6914-150. Retain the original source guides, failed engine, manifests and receipts. Use additive replacement after caller review if a correction is needed; do not overwrite a sealed historical source.

This skill authorizes no external write, real allocation, scientific claim, identity issuance, legal or cultural interpretation, professional judgment or release. Bounded same-owner synthetic software and documentation evidence only. No empirical confirmation, real participants, professional judgment, production identity, deployment, legal or cultural ratification, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything proof, canon or Stage 20 claim. Maori concepts remain under Maori authority. NOT_READY_FOR_STAGE_20.
