---
name: ilyra-maximal-obligations
description: Identify obligations with no declared successor. Use for bounded finite synthetic evidence-obligation graph records.
---

# maximal obligations

Identify obligations with no declared successor.

Accept a JSON object with exactly `op`, `graph`, and `args`. The graph has exactly `id`, `nodes`, and `edges`; labels are unique, the graph is acyclic, and its maximum size is eight nodes. Reject extra fields, duplicate JSON keys, unsafe numbers, invalid edges, unknown labels, and unavailable arguments before computation. Preserve declared label order and explicit disconnected or isolated states.

The frozen discriminating cases are:

- C4: A four-node chain has one root, one leaf, three singleton cutsets and no parallel frontier. Expected disposition `completed`.
- D4: A diamond requires both middle reviews for an internal cut and exposes a two-node antichain. Expected disposition `completed`.
- F5: A three-way review fork separates independent review obligations before a shared release leaf. Expected disposition `completed`.
- M5: Three source roots merge through reconciliation, keeping provenance multiplicity explicit. Expected disposition `completed`.
- X5: Two disconnected chains and an isolated vacancy require explicit path absence and multiple roots and leaves. Expected disposition `completed`.

Compare the entire output envelope with the frozen proposal. Preserve input bytes. A rejected candidate remains a failed witness at zero completion credit even when the refusal behaves as expected. Recovery appends a new receipt and keeps the original failure.

Same-owner finite synthetic software and documentation evidence only; not independent reproduction, empirical GMUT confirmation, production THOS or Freed ID, professional, legal, cultural, affected-party or Maori authority, complete privacy or accessibility, exhaustive security, AGI/ASI, consciousness, personhood, identity continuity, Theory-of-Everything proof, canon, deployment or Stage 20 readiness.
