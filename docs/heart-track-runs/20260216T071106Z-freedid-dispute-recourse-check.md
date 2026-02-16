# Freed ID Dispute/Recourse Verification Report

- generated_utc: `2026-02-16T07:11:06+00:00`
- control_id: `GOV-004`
- overall_status: **PASS**

## Checks
| check | status | detail |
|---|---|---|
| open_case | PASS | status=opened |
| reject_invalid_transition | PASS | opened->resolved rejected |
| reject_missing_auth_proof | PASS | missing proof opened->review rejected |
| reject_unauthorized_actor_role | PASS | subject opened->review rejected |
| reject_unknown_actor_role | PASS | unknown role opened->review rejected |
| reject_signer_mismatch | PASS | signer mismatch opened->review rejected |
| reject_invalid_signature | PASS | tampered signature opened->review rejected |
| reject_unknown_verification_method | PASS | unknown verification method opened->review rejected |
| to_review | PASS | status=review |
| to_escalated | PASS | status=escalated |
| reject_replayed_proof | PASS | replayed proof rejected: proof-to_escalated |
| escalation_back_to_review | PASS | status=review |
| resolve_case | PASS | status=resolved |
| reopen_case | PASS | status=reopened |
| reopened_to_review | PASS | status=review |
| close_as_dismissed | PASS | status=dismissed |
| history_integrity_chain | PASS | event sequence and status chain verified |
| history_depth | PASS | events=8 |
| final_status | PASS | dismissed |
| auth_proof_presence | PASS | all transition events include auth_proof_id |
| verification_method_presence | PASS | all transition events include method id |
| signature_verified_flags | PASS | all transition events marked signature_verified=true |
| auth_proof_registry_consistency | PASS | proof_count=7 |
| schema_required_fields | PASS | all required case fields present |
| schema_status_enum | PASS | status=dismissed |
| schema_event_status_enum | PASS | history_entries=8 |
| schema_event_actor_role_enum | PASS | history_entries=8 |
| schema_event_sequence | PASS | history_entries=8 |
| schema_event_id_pattern | PASS | history_entries=8 |

## Final case snapshot
```json
{
  "case_id": "case-gov004-0001",
  "subject_did": "did:freed:subject-001",
  "credential_id": "did:freed:subject-001#cred-0",
  "reason": "presentation denial dispute",
  "opened_utc": "2026-02-16T07:11:06+00:00",
  "opened_by": "did:freed:ombuds-1",
  "status": "dismissed",
  "evidence_refs": [
    "evidence://submission/1"
  ],
  "used_auth_proof_ids": [
    "proof-to_review",
    "proof-to_escalated",
    "proof-escalation_back_to_review",
    "proof-resolve_case",
    "proof-reopen_case",
    "proof-reopened_to_review",
    "proof-close_as_dismissed"
  ],
  "history": [
    {
      "event_id": "case-gov004-0001:event:0000",
      "event_seq": 0,
      "at_utc": "2026-02-16T07:11:06+00:00",
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
        "evidence://submission/1"
      ]
    },
    {
      "event_id": "case-gov004-0001:event:0001",
      "event_seq": 1,
      "at_utc": "2026-02-16T07:11:06+00:00",
      "actor": "did:freed:reviewer-1",
      "actor_role": "reviewer",
      "from_status": "opened",
      "to_status": "review",
      "note": "intake accepted",
      "auth_proof_id": "proof-to_review",
      "auth_signer_did": "did:freed:reviewer-1",
      "verification_method_id": "did:freed:reviewer-1#hmac-1",
      "payload_sha256": "599c7a98e4418d7d3b9c07fc7704c36e88bef03a9c81962fd4f807622bc07e87",
      "signature_verified": true,
      "evidence_refs": []
    },
    {
      "event_id": "case-gov004-0001:event:0002",
      "event_seq": 2,
      "at_utc": "2026-02-16T07:11:06+00:00",
      "actor": "did:freed:reviewer-1",
      "actor_role": "reviewer",
      "from_status": "review",
      "to_status": "escalated",
      "note": "needs council review",
      "auth_proof_id": "proof-to_escalated",
      "auth_signer_did": "did:freed:reviewer-1",
      "verification_method_id": "did:freed:reviewer-1#hmac-1",
      "payload_sha256": "cef653c00aaaea1297828232bf4401941499832d2439b5c04afced7088bb3b87",
      "signature_verified": true,
      "evidence_refs": []
    },
    {
      "event_id": "case-gov004-0001:event:0003",
      "event_seq": 3,
      "at_utc": "2026-02-16T07:11:06+00:00",
      "actor": "did:freed:council-1",
      "actor_role": "council",
      "from_status": "escalated",
      "to_status": "review",
      "note": "returned with findings",
      "auth_proof_id": "proof-escalation_back_to_review",
      "auth_signer_did": "did:freed:council-1",
      "verification_method_id": "did:freed:council-1#hmac-1",
      "payload_sha256": "0d42f13db64cad63f10d9f6412509a793bc44cf91e7cfddd5917449b36f4e43d",
      "signature_verified": true,
      "evidence_refs": []
    },
    {
      "event_id": "case-gov004-0001:event:0004",
      "event_seq": 4,
      "at_utc": "2026-02-16T07:11:06+00:00",
      "actor": "did:freed:reviewer-1",
      "actor_role": "reviewer",
      "from_status": "review",
      "to_status": "resolved",
      "note": "credential update ordered",
      "auth_proof_id": "proof-resolve_case",
      "auth_signer_did": "did:freed:reviewer-1",
      "verification_method_id": "did:freed:reviewer-1#hmac-1",
      "payload_sha256": "e76f25b12f8b5c4b75b538c6e3c2c6b08c51141631658c871b34fb647c5cd590",
      "signature_verified": true,
      "evidence_refs": []
    },
    {
      "event_id": "case-gov004-0001:event:0005",
      "event_seq": 5,
      "at_utc": "2026-02-16T07:11:06+00:00",
      "actor": "did:freed:subject-001",
      "actor_role": "subject",
      "from_status": "resolved",
      "to_status": "reopened",
      "note": "appeal on remediation scope",
      "auth_proof_id": "proof-reopen_case",
      "auth_signer_did": "did:freed:subject-001",
      "verification_method_id": "did:freed:subject-001#hmac-1",
      "payload_sha256": "9f9ab2dcd342e37d1c0239eaae41fa707b2ae31565d3ad2f77ab8974e5f30e45",
      "signature_verified": true,
      "evidence_refs": []
    },
    {
      "event_id": "case-gov004-0001:event:0006",
      "event_seq": 6,
      "at_utc": "2026-02-16T07:11:06+00:00",
      "actor": "did:freed:reviewer-2",
      "actor_role": "reviewer",
      "from_status": "reopened",
      "to_status": "review",
      "note": "appeal accepted",
      "auth_proof_id": "proof-reopened_to_review",
      "auth_signer_did": "did:freed:reviewer-2",
      "verification_method_id": "did:freed:reviewer-2#hmac-1",
      "payload_sha256": "4c1e61c52feabc54d8465a138baa21b42999f9e00ce3dc6a1d189b34feb60ed1",
      "signature_verified": true,
      "evidence_refs": []
    },
    {
      "event_id": "case-gov004-0001:event:0007",
      "event_seq": 7,
      "at_utc": "2026-02-16T07:11:06+00:00",
      "actor": "did:freed:reviewer-2",
      "actor_role": "reviewer",
      "from_status": "review",
      "to_status": "dismissed",
      "note": "appeal concluded",
      "auth_proof_id": "proof-close_as_dismissed",
      "auth_signer_did": "did:freed:reviewer-2",
      "verification_method_id": "did:freed:reviewer-2#hmac-1",
      "payload_sha256": "67792e286e572a1c22ae755c51ebc42b1a67afefea38f5acb58133c337fe56c7",
      "signature_verified": true,
      "evidence_refs": []
    }
  ]
}
```
