# Four retained finite contracts

## Petri record shape

Operation `petri_record_shape`; ceiling `completed`. Derive exact place, transition and nonzero arc counts from a bounded typed net record.

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

## Petri incidence matrix

Operation `petri_incidence_matrix`; ceiling `completed`. Construct the exact integer post-minus-pre incidence matrix without assigning physical meaning.

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

## Finite siphon candidate check

Operation `petri_siphon_candidate`; ceiling `completed`. Check one declared place subset against the finite siphon implication and list violations.

Example request:

```json
{
  "op": "petri_siphon_candidate",
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
  "subset": [
    0,
    2
  ]
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "candidate": false,
    "violations": [
      "t1"
    ],
    "subset": [
      "p0",
      "p2"
    ]
  },
  "authority": false
}
```

## Finite trap candidate check

Operation `petri_trap_candidate`; ceiling `completed`. Check one declared place subset against the finite trap implication and list violations.

Example request:

```json
{
  "op": "petri_trap_candidate",
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
  "subset": [
    0,
    2
  ]
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "candidate": false,
    "violations": [
      "t0"
    ],
    "subset": [
      "p0",
      "p2"
    ]
  },
  "authority": false
}
```

Bounded same-owner synthetic software evidence only. No empirical, real-participant, professional, production-identity, deployment, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
