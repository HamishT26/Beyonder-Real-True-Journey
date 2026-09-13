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
