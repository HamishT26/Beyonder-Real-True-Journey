# Exact contract

Operation: `petri_trace_prefix`

Preregistered hypothesis: Project a declared prefix of a finite firing trace while retaining blocked-position evidence.

Expected disposition: `completed`.

Example request:

```json
{
  "op": "petri_trace_prefix",
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
  "sequence": [
    0,
    1
  ],
  "prefix_length": 0
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "requested_prefix": 0,
    "fired_count": 0,
    "blocked_at": null,
    "marking": [
      1,
      1,
      2
    ]
  },
  "authority": false
}
```

An added `unreviewed_authority` field must return `unknown_field`. The rejection does not turn the invalid subject into a pass.

Bounded same-owner synthetic software evidence only. No empirical, real-participant, professional, production-identity, deployment, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
