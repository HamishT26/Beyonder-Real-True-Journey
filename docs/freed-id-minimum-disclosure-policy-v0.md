# Freed ID Minimum-Disclosure Policy v0 (GOV-002)

Purpose: enforce "privacy by design" by disclosing only requested, policy-allowed claims from a credential.

## Policy goals
1. Never disclose fields that were not explicitly requested.
2. Deny sensitive fields by default unless explicitly allowed by policy.
3. Emit machine-readable disclosure metadata for auditability and verification.

## Default sensitive fields
- `full_name`
- `legal_name`
- `government_id`
- `birth_date`
- `email`
- `phone`
- `home_address`

## Required presentation metadata
- `subject_did`
- `credential_id`
- `requested_fields`
- `disclosed_claims`
- `redacted_fields`
- `denied_sensitive_fields`
- `policy_version`
- `created_utc`

## Maturity note
This is a local policy scaffold for validation and iteration. It does not replace legal/privacy compliance reviews.
