# Four retained finite contracts

## Marking enabledness inventory

Operation `petri_enabled_transitions`; ceiling `completed`. List transitions whose declared input multiplicities are available at one synthetic marking.

Example request:

```json
{
  "op": "petri_enabled_transitions",
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
  ]
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "enabled": [
      "t0",
      "t1"
    ]
  },
  "authority": false
}
```

## Single transition firing

Operation `petri_fire_transition`; ceiling `completed`. Apply one enabled transition or retain an explicit disabled result without inventing tokens.

Example request:

```json
{
  "op": "petri_fire_transition",
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
  "transition_index": 0
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
    ]
  },
  "authority": false
}
```

## Bounded firing sequence

Operation `petri_fire_sequence`; ceiling `completed`. Execute a finite declared transition sequence until completion or the first disabled step.

Example request:

```json
{
  "op": "petri_fire_sequence",
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
  ]
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "fired_count": 2,
    "blocked_at": null,
    "marking": [
      0,
      1,
      3
    ]
  },
  "authority": false
}
```

## Enabled structural conflict pairs

Operation `petri_conflict_pairs`; ceiling `completed`. Identify enabled transition pairs that compete for at least one consumed place.

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

Bounded same-owner synthetic software evidence only. No empirical, real-participant, professional, production-identity, deployment, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
