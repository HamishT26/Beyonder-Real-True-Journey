---
name: ghc-family-linkability-audit
description: Trace correlation paths across pairwise identifiers, credential status, caches, logs, and relying-party contexts. Use when reviewing identity or status designs for avoidable joins while reserving complete privacy assurance.
---

# Linkability Audit

1. Inventory identifiers, indexes, URLs, timestamps, logs, caches, and disclosure contexts.
2. Draw every direct and indirect join edge.
3. Test rotation, collision, cross-context reuse, small-population leakage, and retrieval observation.
4. Recommend minimization while preserving unresolved malicious-issuer, verifier, and deployment risks.

Use `ghc_family_linkability_audit.py` for the phase fixture. Do not call a zero-hit structural scan privacy-complete.
