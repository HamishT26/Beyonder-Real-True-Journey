# Exact contract

Operation: `petri_boundedness_probe`

Preregistered hypothesis: Report observed component maxima only inside a capped enumeration and refuse a universal boundedness claim.

Expected disposition: `completed`.

Example request:

```json
{
  "op": "petri_boundedness_probe",
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
  "state_cap": 12,
  "token_limit": 3
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "observed_maxima": [
      1,
      2,
      4
    ],
    "within_declared_limit": false,
    "truncated": false,
    "universal_boundedness_proved": false
  },
  "authority": false
}
```

An added `unreviewed_authority` field must return `unknown_field`. The rejection does not turn the invalid subject into a pass.

Bounded same-owner synthetic software evidence only. No empirical, real-participant, professional, production-identity, deployment, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
