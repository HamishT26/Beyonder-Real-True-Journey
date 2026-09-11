# Four retained finite contracts

## Weighted marking conservation witness

Operation `petri_place_invariant`; ceiling `completed`. Compare a declared weighted token sum before and after one transition as a local arithmetic witness.

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

## Capped reachability enumeration

Operation `petri_reachability_bfs`; ceiling `completed`. Enumerate distinct reachable markings under an explicit finite state cap and expose truncation.

Example request:

```json
{
  "op": "petri_reachability_bfs",
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
  "state_cap": 12
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "markings": [
      [
        1,
        1,
        2
      ],
      [
        0,
        2,
        2
      ],
      [
        1,
        0,
        3
      ],
      [
        0,
        1,
        3
      ],
      [
        0,
        0,
        4
      ]
    ],
    "truncated": false,
    "cap": 12
  },
  "authority": false
}
```

## Finite boundedness probe

Operation `petri_boundedness_probe`; ceiling `completed`. Report observed component maxima only inside a capped enumeration and refuse a universal boundedness claim.

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

## Local deadlock witness

Operation `petri_deadlock_witness`; ceiling `completed`. Classify one exact marking as locally deadlocked only when no declared transition is enabled.

Example request:

```json
{
  "op": "petri_deadlock_witness",
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
    0,
    0,
    0
  ]
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "enabled": [],
    "deadlocked": true,
    "marking_local_only": true
  },
  "authority": false
}
```

Bounded same-owner synthetic software evidence only. No empirical, real-participant, professional, production-identity, deployment, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
