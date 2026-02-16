# Freed ID Dispute/Recourse Adversarial Verification Report

- generated_utc: `2026-02-16T07:11:05+00:00`
- control_id: `GOV-004`
- mode: `adversarial`
- overall_status: **PASS**

## Checks
| check | status | detail |
|---|---|---|
| open_case | PASS | status=opened |
| baseline_to_review | PASS | status=review |
| reject_replayed_proof | PASS | replayed proof rejected |
| reject_signer_mismatch | PASS | mismatched signer rejected |
| reject_signature_tamper | PASS | tampered signature rejected |
| reject_payload_tamper | PASS | tampered payload digest rejected |
| reject_unknown_method | PASS | unknown verification method rejected |
| baseline_progression | PASS | status=resolved |
| baseline_history_integrity | PASS | integrity checks passed |
| detect_order_tamper | PASS | event_seq mismatch at index=2: got=3; event_id mismatch at index=2: got=case-gov004-adversarial-0001:event:0003 |
| detect_sequence_tamper | PASS | event_seq mismatch at index=1: got=99 |

## Detail snapshot
```json
{
  "final_status": "resolved",
  "history_length": 5,
  "used_auth_proof_ids": [
    "adv-proof-1",
    "adv-proof-3",
    "adv-proof-4",
    "adv-proof-5"
  ],
  "sample_case": {
    "case_id": "case-gov004-adversarial-0001",
    "subject_did": "did:freed:subject-adv-001",
    "credential_id": "did:freed:subject-adv-001#cred-0",
    "reason": "adversarial transition checks",
    "opened_utc": "2026-02-16T07:11:05+00:00",
    "opened_by": "did:freed:ombuds-1",
    "status": "resolved",
    "evidence_refs": [
      "evidence://adversarial/seed"
    ],
    "used_auth_proof_ids": [
      "adv-proof-1",
      "adv-proof-3",
      "adv-proof-4",
      "adv-proof-5"
    ],
    "history": [
      {
        "event_id": "case-gov004-adversarial-0001:event:0000",
        "event_seq": 0,
        "at_utc": "2026-02-16T07:11:05+00:00",
        "actor": "did:freed:ombuds-1",
        "actor_role": "ombuds",
        "from_status": "none",
        "to_status": "opened",
        "note": "case opened",
        "auth_proof_id": null,
        "auth_signer_did": "did:freed:ombuds-1",
        "verification_method_id": null,
        "payload_sha256": null,
        "signature_verified": false,
        "evidence_refs": [
          "evidence://adversarial/seed"
        ]
      },
      {
        "event_id": "case-gov004-adversarial-0001:event:0001",
        "event_seq": 1,
        "at_utc": "2026-02-16T07:11:05+00:00",
        "actor": "did:freed:reviewer-1",
        "actor_role": "reviewer",
        "from_status": "opened",
        "to_status": "review",
        "note": "baseline review transition",
        "auth_proof_id": "adv-proof-1",
        "auth_signer_did": "did:freed:reviewer-1",
        "verification_method_id": "did:freed:reviewer-1#hmac-1",
        "payload_sha256": "33babde3b55754776a99c908510f26dcb55538ae3aa895ab9e1512e3cec9ed28",
        "signature_verified": true,
        "evidence_refs": []
      },
      {
        "event_id": "case-gov004-adversarial-0001:event:0002",
        "event_seq": 2,
        "at_utc": "2026-02-16T07:11:05+00:00",
        "actor": "did:freed:reviewer-1",
        "actor_role": "reviewer",
        "from_status": "review",
        "to_status": "escalated",
        "note": "valid escalation",
        "auth_proof_id": "adv-proof-3",
        "auth_signer_did": "did:freed:reviewer-1",
        "verification_method_id": "did:freed:reviewer-1#hmac-1",
        "payload_sha256": "b62158dfcf1deb67696dfa5109c04c60139335a47a10c3ca7dd973f385965d1f",
        "signature_verified": true,
        "evidence_refs": []
      },
      {
        "event_id": "case-gov004-adversarial-0001:event:0003",
        "event_seq": 3,
        "at_utc": "2026-02-16T07:11:05+00:00",
        "actor": "did:freed:council-1",
        "actor_role": "council",
        "from_status": "escalated",
        "to_status": "review",
        "note": "valid escalation return",
        "auth_proof_id": "adv-proof-4",
        "auth_signer_did": "did:freed:council-1",
        "verification_method_id": "did:freed:council-1#hmac-1",
        "payload_sha256": "bd4c0977a846a64fc83097bd011eba43fcc16ac345825847798e8456de41538b",
        "signature_verified": true,
        "evidence_refs": []
      },
      {
        "event_id": "case-gov004-adversarial-0001:event:0004",
        "event_seq": 4,
        "at_utc": "2026-02-16T07:11:05+00:00",
        "actor": "did:freed:council-1",
        "actor_role": "council",
        "from_status": "review",
        "to_status": "resolved",
        "note": "valid resolution",
        "auth_proof_id": "adv-proof-5",
        "auth_signer_did": "did:freed:council-1",
        "verification_method_id": "did:freed:council-1#hmac-1",
        "payload_sha256": "478d3d26cd011a73411849116a0d4d4458ab907f930a5449672c3333d179acc1",
        "signature_verified": true,
        "evidence_refs": []
      }
    ]
  }
}
```
