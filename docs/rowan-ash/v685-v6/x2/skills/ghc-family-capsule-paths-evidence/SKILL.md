---
name: ghc-family-capsule-paths-evidence
description: "Interpret portable manifest paths evidence without inflating credit."
---

# ghc-family-capsule-paths-evidence

Interpret portable manifest paths evidence without inflating credit.

Use the owner-local capsule interface for paths when this exact evidence question is in scope. A supplied fixture describes a model; it is not independent evidence about Git history or external authority.

Check these acceptance conditions:

- Require slash separators and reject Windows path spellings in portable manifests. Frozen reference: RA6856-N010.
- Reject NUL, line breaks, tabs, and other control characters before Git batch requests. Frozen reference: RA6856-N011.
- Reject reserved device names, trailing dots or spaces, and case-fold collisions. Frozen reference: RA6856-N012.

Use the accepting and rejecting fixtures under ../../fixtures/ and the command under ../../runners/ghc_family_capsule_paths.py. Invoke it from the repository with Python and an explicit --input file. The shared engine is scripts/ghc_family_evidence_capsule.py.

Keep the original rejecting witness, label inherited material at zero new credit, and retain any absent evidence as open_gap or exact_gate. Do not run an actual canonical reservation merely to test this guide; use the synthetic fixture interface.

Rollback is to stop using this candidate guide while preserving older compatible tools and all evidence. Same-owner software evidence only. Manual browser, assistive-technology, cognitive, language, and affected-user accessibility evaluation remains reserved. No empirical, professional, production, independent-reproduction, identity, legal, cultural, Maori-authority, complete privacy or accessibility, exhaustive security, Theory-of-Everything, canon, or Stage 20 claim.
