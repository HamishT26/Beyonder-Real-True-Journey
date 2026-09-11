# Exact contract

Operation: `petri_record_shape`

Preregistered hypothesis: Derive exact place, transition and nonzero arc counts from a bounded typed net record.

Expected disposition: `completed`.

Example request:

```json
{
  "op": "petri_record_shape",
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
    "place_count": 3,
    "transition_count": 2,
    "nonzero_pre_arcs": 2,
    "nonzero_post_arcs": 2,
    "shape_consistent": true
  },
  "authority": false
}
```

An added `unreviewed_authority` field must return `unknown_field`. The rejection does not turn the invalid subject into a pass.

Bounded same-owner synthetic software evidence only. No empirical, real-participant, professional, production-identity, deployment, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
