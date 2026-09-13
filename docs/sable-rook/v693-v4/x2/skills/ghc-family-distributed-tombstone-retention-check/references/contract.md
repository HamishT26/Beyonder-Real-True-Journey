# tombstone_retention_check

Keep a tombstone until every required synthetic replica acknowledges its clock.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## No required replicas allow bounded collection

Request:
```json
{
  "op": "tombstone_retention_check",
  "record": {
    "clock": {
      "a": 1
    },
    "acknowledgements": {},
    "required": []
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
    "retain": false,
    "safe_to_collect": true,
    "missing": [],
    "behind": [],
    "required": [],
    "production_collection": false
  },
  "error": null,
  "external_credit": false
}
```

## One equal acknowledgement covers the tombstone

Request:
```json
{
  "op": "tombstone_retention_check",
  "record": {
    "clock": {
      "a": 1
    },
    "acknowledgements": {
      "r1": {
        "a": 1
      }
    },
    "required": [
      "r1"
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
    "retain": false,
    "safe_to_collect": true,
    "missing": [],
    "behind": [],
    "required": [
      "r1"
    ],
    "production_collection": false
  },
  "error": null,
  "external_credit": false
}
```

## A missing required replica retains it

Request:
```json
{
  "op": "tombstone_retention_check",
  "record": {
    "clock": {
      "a": 1
    },
    "acknowledgements": {
      "r1": {
        "a": 1
      }
    },
    "required": [
      "r1",
      "r2"
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
    "retain": true,
    "safe_to_collect": false,
    "missing": [
      "r2"
    ],
    "behind": [],
    "required": [
      "r1",
      "r2"
    ],
    "production_collection": false
  },
  "error": null,
  "external_credit": false
}
```

## A behind acknowledgement retains it

Request:
```json
{
  "op": "tombstone_retention_check",
  "record": {
    "clock": {
      "a": 2
    },
    "acknowledgements": {
      "r1": {
        "a": 1
      }
    },
    "required": [
      "r1"
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
    "retain": true,
    "safe_to_collect": false,
    "missing": [],
    "behind": [
      "r1"
    ],
    "required": [
      "r1"
    ],
    "production_collection": false
  },
  "error": null,
  "external_credit": false
}
```

## Actorwise acknowledgements must dominate

Request:
```json
{
  "op": "tombstone_retention_check",
  "record": {
    "clock": {
      "a": 1,
      "b": 2
    },
    "acknowledgements": {
      "r1": {
        "a": 1,
        "b": 2
      },
      "r2": {
        "a": 2,
        "b": 2
      }
    },
    "required": [
      "r2",
      "r1"
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
    "retain": false,
    "safe_to_collect": true,
    "missing": [],
    "behind": [],
    "required": [
      "r1",
      "r2"
    ],
    "production_collection": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
