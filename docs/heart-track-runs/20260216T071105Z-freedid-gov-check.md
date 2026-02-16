# Freed ID Governance Verification Report

- generated_utc: `2026-02-16T07:11:05+00:00`
- control: `GOV-005`
- overall_status: **PASS**

## Checks
| check | status | detail |
|---|---|---|
| register_did | PASS | registered did:freed:7b26a34f232d4e3d87a27f196f185ac6 |
| issue_credential_before_revoke | PASS | credential accepted |
| revoke_did | PASS | did marked revoked |
| issue_credential_after_revoke | PASS | rejected as expected for revoked did |
| verify_credential_after_revoke | PASS | revoked did does not verify |
