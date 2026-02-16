# Freed ID Dispute/Recourse Verification Report

- generated_utc: `2026-02-16T10:04:09+00:00`
- control_id: `GOV-004`
- overall_status: **PASS**

## Checks
| check | status | detail |
|---|---|---|
| open_case | PASS | status=opened |
| reject_invalid_transition | PASS | opened->resolved rejected |
| reject_missing_auth_proof | PASS | missing proof opened->review rejected |
| reject_missing_signature_verifier | PASS | missing signature_verifier rejected |
| reject_unauthorized_actor_role | PASS | subject opened->review rejected |
| reject_unknown_actor_role | PASS | unknown role opened->review rejected |
| reject_signer_mismatch | PASS | signer mismatch opened->review rejected |
| reject_invalid_signature_ref | PASS | invalid signature_ref rejected |
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
  "opened_utc": "2026-02-16T10:04:09+00:00",
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
      "at_utc": "2026-02-16T10:04:09+00:00",
      "actor": "did:freed:ombuds-1",
      "actor_role": "ombuds",
      "from_status": "none",
      "to_status": "opened",
      "note": "case opened",
      "auth_proof_id": null,
      "auth_signer_did": "did:freed:ombuds-1",
      "evidence_refs": [
        "evidence://submission/1"
      ]
    },
    {
      "event_id": "case-gov004-0001:event:0001",
      "event_seq": 1,
      "at_utc": "2026-02-16T10:04:09+00:00",
      "actor": "did:freed:reviewer-1",
      "actor_role": "reviewer",
      "from_status": "opened",
      "to_status": "review",
      "note": "intake accepted",
      "auth_proof_id": "proof-to_review",
      "auth_signer_did": "did:freed:reviewer-1",
      "evidence_refs": []
    },
    {
      "event_id": "case-gov004-0001:event:0002",
      "event_seq": 2,
      "at_utc": "2026-02-16T10:04:09+00:00",
      "actor": "did:freed:reviewer-1",
      "actor_role": "reviewer",
      "from_status": "review",
      "to_status": "escalated",
      "note": "needs council review",
      "auth_proof_id": "proof-to_escalated",
      "auth_signer_did": "did:freed:reviewer-1",
      "evidence_refs": []
    },
    {
      "event_id": "case-gov004-0001:event:0003",
      "event_seq": 3,
      "at_utc": "2026-02-16T10:04:09+00:00",
      "actor": "did:freed:council-1",
      "actor_role": "council",
      "from_status": "escalated",
      "to_status": "review",
      "note": "returned with findings",
      "auth_proof_id": "proof-escalation_back_to_review",
      "auth_signer_did": "did:freed:council-1",
      "evidence_refs": []
    },
    {
      "event_id": "case-gov004-0001:event:0004",
      "event_seq": 4,
      "at_utc": "2026-02-16T10:04:09+00:00",
      "actor": "did:freed:reviewer-1",
      "actor_role": "reviewer",
      "from_status": "review",
      "to_status": "resolved",
      "note": "credential update ordered",
      "auth_proof_id": "proof-resolve_case",
      "auth_signer_did": "did:freed:reviewer-1",
      "evidence_refs": []
    },
    {
      "event_id": "case-gov004-0001:event:0005",
      "event_seq": 5,
      "at_utc": "2026-02-16T10:04:09+00:00",
      "actor": "did:freed:subject-001",
      "actor_role": "subject",
      "from_status": "resolved",
      "to_status": "reopened",
      "note": "appeal on remediation scope",
      "auth_proof_id": "proof-reopen_case",
      "auth_signer_did": "did:freed:subject-001",
      "evidence_refs": []
    },
    {
      "event_id": "case-gov004-0001:event:0006",
      "event_seq": 6,
      "at_utc": "2026-02-16T10:04:09+00:00",
      "actor": "did:freed:reviewer-2",
      "actor_role": "reviewer",
      "from_status": "reopened",
      "to_status": "review",
      "note": "appeal accepted",
      "auth_proof_id": "proof-reopened_to_review",
      "auth_signer_did": "did:freed:reviewer-2",
      "evidence_refs": []
    },
    {
      "event_id": "case-gov004-0001:event:0007",
      "event_seq": 7,
      "at_utc": "2026-02-16T10:04:09+00:00",
      "actor": "did:freed:reviewer-2",
      "actor_role": "reviewer",
      "from_status": "review",
      "to_status": "dismissed",
      "note": "appeal concluded",
      "auth_proof_id": "proof-close_as_dismissed",
      "auth_signer_did": "did:freed:reviewer-2",
      "evidence_refs": []
    }
  ]
}
```
