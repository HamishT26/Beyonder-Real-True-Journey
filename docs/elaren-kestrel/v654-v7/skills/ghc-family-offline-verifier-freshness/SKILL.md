---
name: ghc-family-offline-verifier-freshness
description: Bound offline credential verification by signed time, clock tolerance, cached status age, risk class, and refusal conditions. Use for verifier-readiness protocols without live resolution, status, or operational assurance.
---

# Offline Verifier Freshness

1. Record credential validity, signed time, local clock basis, tolerance, status-list age, and risk class.
2. Derive a maximum accepted age from explicit policy rather than a universal constant.
3. Reject missing time evidence, excessive age, ambiguous status, or a higher-risk use than the policy permits.
4. Keep live resolution, revocation effectiveness, interoperability, and production operation open.

Use `ghc_family_offline_verifier_freshness.py` for the synthetic fixture.
