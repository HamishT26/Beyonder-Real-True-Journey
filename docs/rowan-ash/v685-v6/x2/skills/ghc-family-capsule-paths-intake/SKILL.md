---
name: ghc-family-capsule-paths-intake
description: "Check portable manifest paths input assumptions before processing."
---

# ghc-family-capsule-paths-intake

Check portable manifest paths input assumptions before processing.

Use the owner-local capsule interface for paths when this exact evidence question is in scope. A supplied fixture describes a model; it is not independent evidence about Git history or external authority.

Check these acceptance conditions:

- Accept NFC relative POSIX paths without rewriting the recorded spelling. Frozen reference: RA6856-N007.
- Reject empty, dot, and parent segments before any filesystem access. Frozen reference: RA6856-N008.
- Reject rooted paths, drive prefixes, network paths, and colon-bearing components. Frozen reference: RA6856-N009.

Use the accepting and rejecting fixtures under ../../fixtures/ and the command under ../../runners/ghc_family_capsule_paths.py. Invoke it from the repository with Python and an explicit --input file. The shared engine is scripts/ghc_family_evidence_capsule.py.

Keep the original rejecting witness, label inherited material at zero new credit, and retain any absent evidence as open_gap or exact_gate. Do not run an actual canonical reservation merely to test this guide; use the synthetic fixture interface.

Rollback is to stop using this candidate guide while preserving older compatible tools and all evidence. Same-owner software evidence only. Manual browser, assistive-technology, cognitive, language, and affected-user accessibility evaluation remains reserved. No empirical, professional, production, independent-reproduction, identity, legal, cultural, Maori-authority, complete privacy or accessibility, exhaustive security, Theory-of-Everything, canon, or Stage 20 claim.
