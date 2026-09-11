# Exact contract

Operation: `petri_place_invariant`

Preregistered hypothesis: Compare a declared weighted token sum before and after one transition as a local arithmetic witness.

Expected disposition: `completed`.

Example request:

```json
{
  "op": "petri_place_invariant",
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
  "weights": [
    1,
    2,
    3
  ]
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "enabled": true,
    "before": 9,
    "after": 10,
    "conserved": false,
    "local_witness_only": true
  },
  "authority": false
}
```

An added `unreviewed_authority` field must return `unknown_field`. The rejection does not turn the invalid subject into a pass.

Bounded same-owner synthetic software evidence only. No empirical, real-participant, professional, production-identity, deployment, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
