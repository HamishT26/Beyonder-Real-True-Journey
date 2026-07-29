---
name: ghc-family-selective-disclosure-minimizer
description: Reduce a credential request to purpose-sufficient predicates and flag unnecessary attributes or linkability. Use for selective-disclosure design, claim-request review, privacy threat modeling, and non-production credential fixtures.
---

# Selective Disclosure Minimizer

1. State the verifier purpose and the minimum decision predicate.
2. Map each requested attribute to that predicate.
3. Suppress attributes without a necessary mapping and flag global identifiers or status fields that can correlate holders.
4. Keep cryptographic deployment, unlinkability, interoperability, and privacy-complete claims open.

Use `ghc_family_selective_disclosure_minimizer.py` for the bounded fixture. Draft or watch standards may inform compatibility only.
