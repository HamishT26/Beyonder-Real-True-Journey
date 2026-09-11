# Four retained finite contracts

## Trace prefix projection

Operation `petri_trace_prefix`; ceiling `completed`. Project a declared prefix of a finite firing trace while retaining blocked-position evidence.

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

## Disjoint-support transition pairs

Operation `petri_independent_pairs`; ceiling `completed`. Identify pairs whose declared consume-and-produce supports are disjoint.

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

## Workflow source and sink projection

Operation `petri_workflow_source_sink`; ceiling `completed`. Project transitions adjacent to declared entry and exit places without certifying a real workflow.

Example request:

```json
{
  "op": "petri_workflow_source_sink",
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
  "entry_place": 0,
  "exit_place": 2
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "entry": "p0",
    "exit": "p2",
    "leaving_entry": [
      "t0"
    ],
    "entering_exit": [
      "t1"
    ],
    "real_workflow_certified": false
  },
  "authority": false
}
```

## Synthetic capacity envelope

Operation `petri_capacity_envelope`; ceiling `represented`. Compare one post-firing marking with declared token ceilings as a represented workload model.

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

Bounded same-owner synthetic software evidence only. No empirical, real-participant, professional, production-identity, deployment, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
