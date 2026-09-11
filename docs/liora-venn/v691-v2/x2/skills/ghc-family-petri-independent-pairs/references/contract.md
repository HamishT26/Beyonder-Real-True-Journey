# Exact contract

Operation: `petri_independent_pairs`

Hypothesis: Identify pairs whose declared consume-and-produce supports are disjoint.

Ceiling: `completed`.

Example request:

```json
{
  "op": "petri_independent_pairs",
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
  ]
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "pairs": [],
    "criterion": "disjoint_declared_support"
  },
  "authority": false
}
```

The named unknown-field subject must be rejected while remaining a failed subject at zero acceptance credit.

Bounded same-owner synthetic software evidence only. No empirical, real-participant, professional, production-identity, deployment, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
