# Freed ID Minimum-Disclosure Policy v0 (GOV-002)

Purpose: define a concrete, testable minimum-disclosure policy for credential presentation workflows.

## Policy statement
When a verifier requests proof for a specific purpose, the holder should disclose only the minimum required attributes and no additional personally identifying fields.

## v0 presentation schema (example)

### Source credential (holder vault)
- `subject_did`
- `full_name`
- `date_of_birth`
- `national_id`
- `email`
- `residency_status`
- `age_over_18`

### Minimum-disclosure presentation for "age+residency eligibility" purpose
- required fields:
  - `subject_did`
  - `age_over_18`
  - `residency_status`
- forbidden fields:
  - `full_name`
  - `date_of_birth`
  - `national_id`
  - `email`

## Verification rule
A presentation is compliant when:
1. all required fields are present,
2. forbidden fields are absent,
3. no unrequested extra fields are included (except metadata/proof container fields),
4. proof metadata binds the presentation to a source credential commitment.

## v0 scope boundary
- This is a local policy scaffold for reproducible governance checks.
- It is not yet a full cryptographic zero-knowledge implementation.
- Promotion from implemented -> verified requires automated, repeatable PASS evidence artifacts.
