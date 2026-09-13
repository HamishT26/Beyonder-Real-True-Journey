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
