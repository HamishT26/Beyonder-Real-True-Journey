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
