# Exact contract

Operation: `petri_accessible_marking_summary`

Hypothesis: Render place labels and token counts as ordered text while retaining manual accessibility review.

Ceiling: `completed`.

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

The named unknown-field subject must be rejected while remaining a failed subject at zero acceptance credit.

Bounded same-owner synthetic software evidence only. No empirical, real-participant, professional, production-identity, deployment, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
