# Freed ID Auditability Verification Report

- generated_utc: `2026-02-16T05:02:40+00:00`
- control: `GOV-003`
- ledger_path: `docs/freed-id-audit-log.jsonl`
- overall_status: **PASS**

## Checks
| check | status | detail |
|---|---|---|
| register_did | PASS | registered did:freed:09d36c8f89d44663ad1cd1cf9d5067b4 |
| issue_credential | PASS | credential issued |
| update_did | PASS | did update recorded |
| revoke_did | PASS | did revoked |
| ledger_exists | PASS | ledger file present: docs/freed-id-audit-log.jsonl |
| ledger_entry_count | PASS | entries=4 |
| action_sequence | PASS | register,issue_credential,update,revoke |
| hash_chain_integrity | PASS | entries_verified=4 |
