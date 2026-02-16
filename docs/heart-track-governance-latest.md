# Freed ID Governance Verification Report

- generated_utc: `2026-02-16T05:02:40+00:00`
- control: `GOV-005`
- overall_status: **PASS**

## Checks
| check | status | detail |
|---|---|---|
| register_did | PASS | registered did:freed:53f088c7577f4f808ac7565667a6fe51 |
| issue_credential_before_revoke | PASS | credential accepted |
| revoke_did | PASS | did marked revoked |
| issue_credential_after_revoke | PASS | rejected as expected for revoked did |
| verify_credential_after_revoke | PASS | revoked did does not verify |
