# Freed ID Dispute/Recourse Verification Report

- generated_utc: `2026-02-16T05:24:07+00:00`
- control_id: `GOV-004`
- overall_status: **PASS**

## Checks
| check | status | detail |
|---|---|---|
| open_case | PASS | status=opened |
| reject_invalid_transition | PASS | opened->resolved rejected |
| reject_unauthorized_actor_role | PASS | subject opened->review rejected |
| reject_unknown_actor_role | PASS | unknown role opened->review rejected |
| to_review | PASS | status=review |
| to_escalated | PASS | status=escalated |
| escalation_back_to_review | PASS | status=review |
| resolve_case | PASS | status=resolved |
| reopen_case | PASS | status=reopened |
| reopened_to_review | PASS | status=review |
| close_as_dismissed | PASS | status=dismissed |
| history_depth | PASS | events=8 |
| final_status | PASS | dismissed |
| schema_required_fields | PASS | all required case fields present |
| schema_status_enum | PASS | status=dismissed |
| schema_event_status_enum | PASS | history_entries=8 |
| schema_event_actor_role_enum | PASS | history_entries=8 |

## Final case snapshot
```json
{
  "case_id": "case-gov004-0001",
  "subject_did": "did:freed:subject-001",
  "credential_id": "did:freed:subject-001#cred-0",
  "reason": "presentation denial dispute",
  "opened_utc": "2026-02-16T05:24:07+00:00",
  "opened_by": "did:freed:ombuds-1",
  "status": "dismissed",
  "evidence_refs": [
    "evidence://submission/1"
  ],
  "history": [
    {
      "at_utc": "2026-02-16T05:24:07+00:00",
      "actor": "did:freed:ombuds-1",
      "actor_role": "ombuds",
      "from_status": "none",
      "to_status": "opened",
      "note": "case opened",
      "evidence_refs": [
        "evidence://submission/1"
      ]
    },
    {
      "at_utc": "2026-02-16T05:24:07+00:00",
      "actor": "did:freed:reviewer-1",
      "actor_role": "reviewer",
      "from_status": "opened",
      "to_status": "review",
      "note": "intake accepted",
      "evidence_refs": []
    },
    {
      "at_utc": "2026-02-16T05:24:07+00:00",
      "actor": "did:freed:reviewer-1",
      "actor_role": "reviewer",
      "from_status": "review",
      "to_status": "escalated",
      "note": "needs council review",
      "evidence_refs": []
    },
    {
      "at_utc": "2026-02-16T05:24:07+00:00",
      "actor": "did:freed:council-1",
      "actor_role": "council",
      "from_status": "escalated",
      "to_status": "review",
      "note": "returned with findings",
      "evidence_refs": []
    },
    {
      "at_utc": "2026-02-16T05:24:07+00:00",
      "actor": "did:freed:reviewer-1",
      "actor_role": "reviewer",
      "from_status": "review",
      "to_status": "resolved",
      "note": "credential update ordered",
      "evidence_refs": []
    },
    {
      "at_utc": "2026-02-16T05:24:07+00:00",
      "actor": "did:freed:subject-001",
      "actor_role": "subject",
      "from_status": "resolved",
      "to_status": "reopened",
      "note": "appeal on remediation scope",
      "evidence_refs": []
    },
    {
      "at_utc": "2026-02-16T05:24:07+00:00",
      "actor": "did:freed:reviewer-2",
      "actor_role": "reviewer",
      "from_status": "reopened",
      "to_status": "review",
      "note": "appeal accepted",
      "evidence_refs": []
    },
    {
      "at_utc": "2026-02-16T05:24:07+00:00",
      "actor": "did:freed:reviewer-2",
      "actor_role": "reviewer",
      "from_status": "review",
      "to_status": "dismissed",
      "note": "appeal concluded",
      "evidence_refs": []
    }
  ]
}
```
