# Exact contract

Operation: `petri_operator_review_vacancy`

Hypothesis: Keep operator, usability and affected-user evaluation explicitly absent from a zero-row record.

Ceiling: `open_gap`.

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

The named unknown-field subject must be rejected while remaining a failed subject at zero acceptance credit.

Bounded same-owner synthetic software evidence only. No empirical, real-participant, professional, production-identity, deployment, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
