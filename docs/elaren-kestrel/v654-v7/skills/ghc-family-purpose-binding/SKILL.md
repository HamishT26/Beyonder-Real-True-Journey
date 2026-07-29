---
name: ghc-family-purpose-binding
description: Bind a declared data or credential purpose to an exact set of allowed operations and fail closed on silent reuse. Use for privacy-purpose ledgers, purpose-change reviews, credential processing, or evidence packets that must distinguish specification from legal authority.
---

# Purpose Binding

1. Record the declared purpose, data classes, controller, evidence source, expiry, and allowed operations.
2. Enumerate prohibited reuse and the evidence required for any purpose change.
3. Reject missing purpose, undeclared operations, stale authority, or an absent rollback.
4. Emit a bounded receipt with zero legal, cultural, production, or affected-party approval credit.

Use `ghc_family_purpose_binding.py` for the v654-v7 deterministic fixture. Preserve every rejection as a synthetic negative. Never infer consent, lawful basis, Māori authority, or public legitimacy from a passing structure.
