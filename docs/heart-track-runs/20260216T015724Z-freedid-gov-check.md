# Freed ID Governance Verification Report

- generated_utc: `2026-02-16T01:57:24+00:00`
- control: `GOV-005`
- overall_status: **PASS**

## Checks
| check | status | detail |
|---|---|---|
| register_did | PASS | registered did:freed:efd6c53d25e648e2b36a97fff924b22c |
| issue_credential_before_revoke | PASS | credential accepted |
| revoke_did | PASS | did marked revoked |
| issue_credential_after_revoke | PASS | rejected as expected for revoked did |
| verify_credential_after_revoke | PASS | revoked did does not verify |
