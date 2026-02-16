# Freed ID Minimum-Disclosure Verification Report

- generated_utc: `2026-02-16T03:18:53+00:00`
- control: `GOV-002`
- overall_status: **PASS**

## Checks
| check | status | detail |
|---|---|---|
| required_fields_present | PASS | all required fields disclosed |
| forbidden_fields_absent | PASS | no forbidden fields disclosed |
| no_unrequested_extras | PASS | no extra claims disclosed |
| proof_commitment_binding | PASS | source commitment matches |

## Presentation sample
```json
{
  "purpose": "age_residency_eligibility",
  "disclosed_claims": {
    "subject_did": "did:freed:holder:abc123",
    "age_over_18": true,
    "residency_status": "resident"
  },
  "proof": {
    "scheme": "commitment-v0",
    "source_credential_sha256": "0c3d4aaf4944c588244ca83362f4cca9d08bc8953a179ea5988f4138380d4bc7"
  }
}
```
