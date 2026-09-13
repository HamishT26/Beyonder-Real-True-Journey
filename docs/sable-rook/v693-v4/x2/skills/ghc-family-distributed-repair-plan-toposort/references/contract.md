# repair_plan_toposort

Order finite repair steps while exposing missing requirements and cycles.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Empty repair plan is ready

Request:
```json
{
  "op": "repair_plan_toposort",
  "record": {
    "steps": []
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
    "ready": true,
    "order": [],
    "missing": [],
    "cycle_members": [],
    "executed": false
  },
  "error": null,
  "external_credit": false
}
```

## One independent step is ready

Request:
```json
{
  "op": "repair_plan_toposort",
  "record": {
    "steps": [
      {
        "id": "inspect",
        "requires": []
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
    "ready": true,
    "order": [
      "inspect"
    ],
    "missing": [],
    "cycle_members": [],
    "executed": false
  },
  "error": null,
  "external_credit": false
}
```

## Dependencies determine order

Request:
```json
{
  "op": "repair_plan_toposort",
  "record": {
    "steps": [
      {
        "id": "verify",
        "requires": [
          "apply"
        ]
      },
      {
        "id": "apply",
        "requires": [
          "inspect"
        ]
      },
      {
        "id": "inspect",
        "requires": []
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
    "ready": true,
    "order": [
      "inspect",
      "apply",
      "verify"
    ],
    "missing": [],
    "cycle_members": [],
    "executed": false
  },
  "error": null,
  "external_credit": false
}
```

## Missing prerequisite holds the plan

Request:
```json
{
  "op": "repair_plan_toposort",
  "record": {
    "steps": [
      {
        "id": "apply",
        "requires": [
          "approve"
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
    "ready": false,
    "order": [],
    "missing": [
      "approve"
    ],
    "cycle_members": [],
    "executed": false
  },
  "error": null,
  "external_credit": false
}
```

## Repair cycle remains held

Request:
```json
{
  "op": "repair_plan_toposort",
  "record": {
    "steps": [
      {
        "id": "a",
        "requires": [
          "b"
        ]
      },
      {
        "id": "b",
        "requires": [
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
    "ready": false,
    "order": [],
    "missing": [],
    "cycle_members": [
      "a",
      "b"
    ],
    "executed": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
