# Exact contract

Operation: `petri_conflict_pairs`

Hypothesis: Identify enabled transition pairs that compete for at least one consumed place.

Ceiling: `completed`.

Example request:

```json
{
  "op": "petri_conflict_pairs",
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
        1,
        0,
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
  ]
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "pairs": [
      {
        "transitions": [
          "t0",
          "t1"
        ],
        "shared_places": [
          "p0"
        ]
      }
    ]
  },
  "authority": false
}
```

The named unknown-field subject must be rejected while remaining a failed subject at zero acceptance credit.

Bounded same-owner synthetic software evidence only. No empirical, real-participant, professional, production-identity, deployment, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
