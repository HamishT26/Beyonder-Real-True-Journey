---
name: ghc-family-capability-attenuation
description: Validate that each delegated task capability narrows scope, audience, duration, and data purpose. Use for THOS task envelopes, delegation chains, and least-privilege fixtures where privilege amplification must fail closed.
---

# Capability Attenuation

1. Record issuer, delegate, parent capability, scope, audience, purpose, expiry, and replay key.
2. Require each child to be a strict subset of the parent in every authority dimension.
3. Reject broader scope, longer duration, changed audience, missing provenance, or ambiguous conflict.
4. Keep real account, token, deployment, sibling, and operational authority at zero.

Use `ghc_family_capability_attenuation.py` for the bounded fixture. Passing data does not prove an ASI, production OS, or secure deployment.
