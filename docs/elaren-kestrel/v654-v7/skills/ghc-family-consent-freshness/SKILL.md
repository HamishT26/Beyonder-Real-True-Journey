---
name: ghc-family-consent-freshness
description: Audit authorization or consent freshness across scope, delegation, withdrawal, expiry, and conflicting grants. Use when a bounded identity, privacy, or task contract must refuse stale or ambiguous permission without claiming legal validity.
---

# Consent Freshness

1. Identify the grant class, scope, controller, delegate, issue time, expiry, and withdrawal state.
2. Compare the requested action with the exact current scope.
3. Fail closed on ambiguity, conflict, missing provenance, or stale state.
4. Reserve legal basis, affected-party acceptance, and real-world effectiveness to competent review.

Use `ghc_family_consent_freshness.py` for the phase fixture. A passing row is protocol evidence only; it is not consent, authorization, or authority in the real world.
