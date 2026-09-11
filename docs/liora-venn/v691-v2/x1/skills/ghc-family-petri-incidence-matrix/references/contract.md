# Exact contract

Operation: `petri_incidence_matrix`

Preregistered hypothesis: Construct the exact integer post-minus-pre incidence matrix without assigning physical meaning.

Expected disposition: `completed`.

Example request:

```json
{
  "op": "petri_incidence_matrix",
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
    "matrix": [
      [
        -1,
        0
      ],
      [
        1,
        -1
      ],
      [
        0,
        1
      ]
    ],
    "orientation": "places_by_transitions"
  },
  "authority": false
}
```

An added `unreviewed_authority` field must return `unknown_field`. The rejection does not turn the invalid subject into a pass.

Bounded same-owner synthetic software evidence only. No empirical, real-participant, professional, production-identity, deployment, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
