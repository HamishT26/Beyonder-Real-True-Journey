---
name: ghc-family-capsule-manifest-intake
description: "Check exact capsule manifests input assumptions before processing."
---

# ghc-family-capsule-manifest-intake

Check exact capsule manifests input assumptions before processing.

Use the owner-local capsule interface for manifest when this exact evidence question is in scope. A supplied fixture describes a model; it is not independent evidence about Git history or external authority.

Check these acceptance conditions:

- Sort entries by literal path and reject nondeterministic duplicate entries. Frozen reference: RA6856-N013.
- Require equality between expected files and manifest targets, including missing and extra paths. Frozen reference: RA6856-N014.
- Verify SHA-256 and byte counts against the declared domain for every target. Frozen reference: RA6856-N015.

Use the accepting and rejecting fixtures under ../../fixtures/ and the command under ../../runners/ghc_family_capsule_manifest.py. Invoke it from the repository with Python and an explicit --input file. The shared engine is scripts/ghc_family_evidence_capsule.py.

Keep the original rejecting witness, label inherited material at zero new credit, and retain any absent evidence as open_gap or exact_gate. Do not run an actual canonical reservation merely to test this guide; use the synthetic fixture interface.

Rollback is to stop using this candidate guide while preserving older compatible tools and all evidence. Same-owner software evidence only. Manual browser, assistive-technology, cognitive, language, and affected-user accessibility evaluation remains reserved. No empirical, professional, production, independent-reproduction, identity, legal, cultural, Maori-authority, complete privacy or accessibility, exhaustive security, Theory-of-Everything, canon, or Stage 20 claim.
