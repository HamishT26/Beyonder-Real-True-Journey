# quorum_intersection

Inspect declared finite quorum membership and pairwise intersection without conferring authority.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Two majority quorums intersect

Request:
```json
{
  "op": "quorum_intersection",
  "record": {
    "members": [
      "a",
      "b",
      "c"
    ],
    "quorums": [
      [
        "a",
        "b"
      ],
      [
        "b",
        "c"
      ]
    ]
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "valid": true,
    "invalid_members": [],
    "intersections": [
      {
        "left": 0,
        "right": 1,
        "members": [
          "b"
        ]
      }
    ],
    "pairwise_intersect": true,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Disjoint declarations remain visible

Request:
```json
{
  "op": "quorum_intersection",
  "record": {
    "members": [
      "a",
      "b",
      "c",
      "d"
    ],
    "quorums": [
      [
        "a",
        "b"
      ],
      [
        "c",
        "d"
      ]
    ]
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "valid": true,
    "invalid_members": [],
    "intersections": [
      {
        "left": 0,
        "right": 1,
        "members": []
      }
    ],
    "pairwise_intersect": false,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Three quorums can share one member

Request:
```json
{
  "op": "quorum_intersection",
  "record": {
    "members": [
      "a",
      "b",
      "c",
      "d"
    ],
    "quorums": [
      [
        "a",
        "b"
      ],
      [
        "b",
        "c"
      ],
      [
        "b",
        "d"
      ]
    ]
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "valid": true,
    "invalid_members": [],
    "intersections": [
      {
        "left": 0,
        "right": 1,
        "members": [
          "b"
        ]
      },
      {
        "left": 0,
        "right": 2,
        "members": [
          "b"
        ]
      },
      {
        "left": 1,
        "right": 2,
        "members": [
          "b"
        ]
      }
    ],
    "pairwise_intersect": true,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Unknown member invalidates the declaration

Request:
```json
{
  "op": "quorum_intersection",
  "record": {
    "members": [
      "a",
      "b"
    ],
    "quorums": [
      [
        "a"
      ],
      [
        "z"
      ]
    ]
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "valid": false,
    "invalid_members": [
      {
        "quorum": 1,
        "member": "z"
      }
    ],
    "intersections": [
      {
        "left": 0,
        "right": 1,
        "members": []
      }
    ],
    "pairwise_intersect": false,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Single quorum has no pairwise counterexample

Request:
```json
{
  "op": "quorum_intersection",
  "record": {
    "members": [
      "a",
      "b"
    ],
    "quorums": [
      [
        "a"
      ]
    ]
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "valid": true,
    "invalid_members": [],
    "intersections": [],
    "pairwise_intersect": true,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
