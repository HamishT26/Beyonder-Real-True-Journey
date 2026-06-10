# v463A Minimum Disclosure Policy

Generated UTC: `2026-05-28T08:37:28.602947Z`

Status: `minimum_disclosure_policy_updated`

Policy:
- Disclose only requested, necessary, phase-scoped claims.
- Deny sensitive personal fields by default.
- Redact raw logs, session JSONL, secrets, screenshots, and private source documents from curated publication.
- Prefer hash, path, artifact ID, and status summary over raw private content.
- Every credential presentation must state issuer, subject, claim set, disclosed fields, redacted fields, policy version, and generated time.

This extends the existing Freed ID minimum-disclosure policy while preserving its local-prototype boundary.
