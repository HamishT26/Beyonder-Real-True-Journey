# Exact contract

Operation: `petri_capacity_envelope`

Hypothesis: Compare one post-firing marking with declared token ceilings as a represented workload model.

Ceiling: `represented`.

Example request:

```json
{
  "op": "petri_capacity_envelope",
  "places": [
    "p0",
    "p1",
    "p2"
  ],
  "transitions": [
    {
      "id": "t0",
      "consume": [
        1,
        0,
        0
      ],
      "produce": [
        0,
        1,
        0
      ]
    },
    {
      "id": "t1",
      "consume": [
        0,
        1,
        0
      ],
      "produce": [
        0,
        0,
        1
      ]
    }
  ],
  "marking": [
    1,
    1,
    2
  ],
  "transition_index": 0,
  "capacities": [
    1,
    2,
    2
  ]
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "enabled": true,
    "next_marking": [
      0,
      2,
      2
    ],
    "within_declared_capacity": true,
    "represented_model_only": true
  },
  "authority": false
}
```

The named unknown-field subject must be rejected while remaining a failed subject at zero acceptance credit.

Bounded same-owner synthetic software evidence only. No empirical, real-participant, professional, production-identity, deployment, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
