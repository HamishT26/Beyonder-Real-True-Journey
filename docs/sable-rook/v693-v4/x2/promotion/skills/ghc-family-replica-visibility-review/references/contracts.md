# Bound visibility contracts

## ghc-family-distributed-causal-dependency-closure

Source bindings:

- `x1/skills/ghc-family-distributed-causal-dependency-closure/SKILL.md` — `b6d6130b3fa5a05842334bb985344d15234a98c9a095879dd08b09db6d3ad7e9`
- `x1/skills/ghc-family-distributed-causal-dependency-closure/references/contract.md` — `f5ea4b1a39ae8de1b103261b09b2c3b709bba6481e485dc3696386567eeaccd7`

# causal_dependency_closure

Expose missing dependencies, cycles, and one deterministic order in a finite event set.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Empty event set is closed

Request:
```json
{
  "op": "causal_dependency_closure",
  "record": {
    "events": []
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
    "closed": true,
    "order": [],
    "missing": [],
    "cycle_members": []
  },
  "error": null,
  "external_credit": false
}
```

## One root event is ordered

Request:
```json
{
  "op": "causal_dependency_closure",
  "record": {
    "events": [
      {
        "id": "a",
        "deps": []
      }
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
    "closed": true,
    "order": [
      "a"
    ],
    "missing": [],
    "cycle_members": []
  },
  "error": null,
  "external_credit": false
}
```

## A chain follows dependencies

Request:
```json
{
  "op": "causal_dependency_closure",
  "record": {
    "events": [
      {
        "id": "c",
        "deps": [
          "b"
        ]
      },
      {
        "id": "a",
        "deps": []
      },
      {
        "id": "b",
        "deps": [
          "a"
        ]
      }
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
    "closed": true,
    "order": [
      "a",
      "b",
      "c"
    ],
    "missing": [],
    "cycle_members": []
  },
  "error": null,
  "external_credit": false
}
```

## A missing dependency remains visible

Request:
```json
{
  "op": "causal_dependency_closure",
  "record": {
    "events": [
      {
        "id": "b",
        "deps": [
          "a"
        ]
      }
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
    "closed": false,
    "order": [],
    "missing": [
      "a"
    ],
    "cycle_members": []
  },
  "error": null,
  "external_credit": false
}
```

## A two-event cycle is retained

Request:
```json
{
  "op": "causal_dependency_closure",
  "record": {
    "events": [
      {
        "id": "a",
        "deps": [
          "b"
        ]
      },
      {
        "id": "b",
        "deps": [
          "a"
        ]
      }
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
    "closed": false,
    "order": [],
    "missing": [],
    "cycle_members": [
      "a",
      "b"
    ]
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

## ghc-family-distributed-replica-observation-matrix

Source bindings:

- `x1/skills/ghc-family-distributed-replica-observation-matrix/SKILL.md` — `db82e27577c10656a51d55d39c34c559cb50b7369b4c46bdaa692bd74abd0a5e`
- `x1/skills/ghc-family-distributed-replica-observation-matrix/references/contract.md` — `79a495a5ab85656718f926e9c5b05c6024ef614a474ff40ed98b171c16bacacd`

# replica_observation_matrix

Separate unanimous, divergent, and missing synthetic key observations across replicas.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Two empty replicas agree

Request:
```json
{
  "op": "replica_observation_matrix",
  "record": {
    "replicas": {
      "a": {},
      "b": {}
    }
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
    "replicas": [
      "a",
      "b"
    ],
    "keys": [],
    "unanimous": [],
    "divergent": [],
    "missing": []
  },
  "error": null,
  "external_credit": false
}
```

## Equal scalar observations are unanimous

Request:
```json
{
  "op": "replica_observation_matrix",
  "record": {
    "replicas": {
      "a": {
        "k": 1
      },
      "b": {
        "k": 1
      }
    }
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
    "replicas": [
      "a",
      "b"
    ],
    "keys": [
      "k"
    ],
    "unanimous": [
      "k"
    ],
    "divergent": [],
    "missing": []
  },
  "error": null,
  "external_credit": false
}
```

## Different scalar observations diverge

Request:
```json
{
  "op": "replica_observation_matrix",
  "record": {
    "replicas": {
      "a": {
        "k": 1
      },
      "b": {
        "k": 2
      }
    }
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
    "replicas": [
      "a",
      "b"
    ],
    "keys": [
      "k"
    ],
    "unanimous": [],
    "divergent": [
      "k"
    ],
    "missing": []
  },
  "error": null,
  "external_credit": false
}
```

## Missing observation is distinct from null

Request:
```json
{
  "op": "replica_observation_matrix",
  "record": {
    "replicas": {
      "a": {
        "k": null
      },
      "b": {}
    }
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
    "replicas": [
      "a",
      "b"
    ],
    "keys": [
      "k"
    ],
    "unanimous": [],
    "divergent": [
      "k"
    ],
    "missing": [
      {
        "key": "k",
        "replicas": [
          "b"
        ]
      }
    ]
  },
  "error": null,
  "external_credit": false
}
```

## Multiple keys retain separate states

Request:
```json
{
  "op": "replica_observation_matrix",
  "record": {
    "replicas": {
      "a": {
        "x": true,
        "y": 1
      },
      "b": {
        "x": true,
        "y": 2
      },
      "c": {
        "x": true
      }
    }
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
    "replicas": [
      "a",
      "b",
      "c"
    ],
    "keys": [
      "x",
      "y"
    ],
    "unanimous": [
      "x"
    ],
    "divergent": [
      "y"
    ],
    "missing": [
      {
        "key": "y",
        "replicas": [
          "c"
        ]
      }
    ]
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

## ghc-family-distributed-quorum-intersection

Source bindings:

- `x1/skills/ghc-family-distributed-quorum-intersection/SKILL.md` — `07c43bd248e5ec35a896a36f5307dda8e3214fc1834f1ea6b2093c4eea4fca4e`
- `x1/skills/ghc-family-distributed-quorum-intersection/references/contract.md` — `ee70b6bfa818d16f21b4c7c73bc14fa987ab28d5af420ae4c114457b3a1316c3`

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

## ghc-family-distributed-partition-frontier

Source bindings:

- `x1/skills/ghc-family-distributed-partition-frontier/SKILL.md` — `271c0268869136966d5eb8127e1b09ab54e3732e864d2e9e408284c59c47b458`
- `x1/skills/ghc-family-distributed-partition-frontier/references/contract.md` — `fdc5b9e16d762377ac53c95d71a78197068ed460f84cfa6ea5488a676ce00136`

# partition_frontier

Compute finite undirected reachability from one declared replica and retain isolated members.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## One replica reaches itself

Request:
```json
{
  "op": "partition_frontier",
  "record": {
    "replicas": [
      "a"
    ],
    "links": [],
    "origin": "a"
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
    "origin": "a",
    "reachable": [
      "a"
    ],
    "isolated": [],
    "connected": true,
    "network_observed": false
  },
  "error": null,
  "external_credit": false
}
```

## One link joins two replicas

Request:
```json
{
  "op": "partition_frontier",
  "record": {
    "replicas": [
      "a",
      "b"
    ],
    "links": [
      [
        "a",
        "b"
      ]
    ],
    "origin": "a"
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
    "origin": "a",
    "reachable": [
      "a",
      "b"
    ],
    "isolated": [],
    "connected": true,
    "network_observed": false
  },
  "error": null,
  "external_credit": false
}
```

## A chain reaches its far endpoint

Request:
```json
{
  "op": "partition_frontier",
  "record": {
    "replicas": [
      "a",
      "b",
      "c"
    ],
    "links": [
      [
        "a",
        "b"
      ],
      [
        "b",
        "c"
      ]
    ],
    "origin": "a"
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
    "origin": "a",
    "reachable": [
      "a",
      "b",
      "c"
    ],
    "isolated": [],
    "connected": true,
    "network_observed": false
  },
  "error": null,
  "external_credit": false
}
```

## An isolated replica remains visible

Request:
```json
{
  "op": "partition_frontier",
  "record": {
    "replicas": [
      "a",
      "b",
      "c"
    ],
    "links": [
      [
        "a",
        "b"
      ]
    ],
    "origin": "a"
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
    "origin": "a",
    "reachable": [
      "a",
      "b"
    ],
    "isolated": [
      "c"
    ],
    "connected": false,
    "network_observed": false
  },
  "error": null,
  "external_credit": false
}
```

## Origin inside a separate component sees only that component

Request:
```json
{
  "op": "partition_frontier",
  "record": {
    "replicas": [
      "a",
      "b",
      "c",
      "d"
    ],
    "links": [
      [
        "a",
        "b"
      ],
      [
        "c",
        "d"
      ]
    ],
    "origin": "c"
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
    "origin": "c",
    "reachable": [
      "c",
      "d"
    ],
    "isolated": [
      "a",
      "b"
    ],
    "connected": false,
    "network_observed": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

Same-owner synthetic integration evidence only. No external deployment, independent reproduction, scientific, professional, legal, cultural, Maori, affected-party, identity, complete privacy or accessibility, exhaustive security, production or Stage 20 credit. NOT_READY_FOR_STAGE_20.
