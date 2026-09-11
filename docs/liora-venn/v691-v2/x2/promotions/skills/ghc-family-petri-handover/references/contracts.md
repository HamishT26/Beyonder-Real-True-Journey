# Four retained finite contracts

## Correction prefix replay plan

Operation `petri_correction_prefix`; ceiling `represented`. Find the shared prefix of two synthetic transition traces and identify the suffix requiring replay.

Example request:

```json
{
  "op": "petri_correction_prefix",
  "original": [
    0,
    1
  ],
  "corrected": [
    0,
    0
  ]
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "shared_prefix_length": 1,
    "replay_original_suffix": [
      1
    ],
    "apply_corrected_suffix": [
      0
    ],
    "operational_replay_performed": false
  },
  "authority": false
}
```

## Accessible marking text companion

Operation `petri_accessible_marking_summary`; ceiling `completed`. Render place labels and token counts as ordered text while retaining manual accessibility review.

Example request:

```json
{
  "op": "petri_accessible_marking_summary",
  "labels": [
    "synthetic place 1",
    "synthetic place 2",
    "synthetic place 3"
  ],
  "marking": [
    1,
    1,
    2
  ]
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "rows": [
      {
        "position": 1,
        "label": "synthetic place 1",
        "tokens": 1
      },
      {
        "position": 2,
        "label": "synthetic place 2",
        "tokens": 1
      },
      {
        "position": 3,
        "label": "synthetic place 3",
        "tokens": 2
      }
    ],
    "text": "1. synthetic place 1: 1 token\n2. synthetic place 2: 1 token\n3. synthetic place 3: 2 tokens",
    "manual_accessibility_review_required": true
  },
  "authority": false
}
```

## Real operator review vacancy

Operation `petri_operator_review_vacancy`; ceiling `open_gap`. Keep operator, usability and affected-user evaluation explicitly absent from a zero-row record.

Example request:

```json
{
  "op": "petri_operator_review_vacancy",
  "notes": {
    "operator": "synthetic protocol case 1",
    "usability": "structure reviewed for case 1",
    "affected_user": "",
    "safety": ""
  },
  "evaluation_count": 0
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "missing": [
      "affected_user",
      "safety"
    ],
    "evaluation_count": 0,
    "real_operator_review": false,
    "affected_user_review": false,
    "safety_review": false,
    "open_gap": true
  },
  "authority": false
}
```

## Operational release authority hold

Operation `petri_release_authority_hold`; ceiling `exact_gate`. Report declaration completeness while withholding every real operational release action.

Example request:

```json
{
  "op": "petri_release_authority_hold",
  "record": "synthetic-workflow-01",
  "declarations": {
    "provenance": true,
    "correction": true,
    "accessibility": false,
    "professional_review": false
  },
  "external_authority": false
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "record": "synthetic-workflow-01",
    "missing": [
      "accessibility",
      "professional_review"
    ],
    "external_action": false,
    "authority_verified": false,
    "exact_gate": true
  },
  "authority": false
}
```

Bounded same-owner synthetic software evidence only. No empirical, real-participant, professional, production-identity, deployment, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
