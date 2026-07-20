---
name: ghc-family-v651-v1-ground-deicing-audit
description: Audit the bounded v651-v1 aircraft ground deicing workflow contract and reject evidence promotion. Use for this phase's synthetic contract, mutation, and protected-gate checks.
---

# aircraft ground deicing workflow audit

1. Load `../../surfaces/ground-deicing/contract.json` from the phase root.
2. Require every declared obligation and the exact expected disposition.
3. Run `scripts/audit.py` against the contract before crediting the skill use.
4. Keep empirical, participant, professional, production, legal, cultural, Māori-authority, privacy-complete, security-complete, accessibility-complete, independent-reproduction, and Stage 20 gates visible.
5. Retain every failed witness and stop on a missing field or promotion attempt.

Credit only the bounded software or synthetic witness. Do not infer real-world truth, authority, deployment readiness, complete conformance, or independent reproduction.
