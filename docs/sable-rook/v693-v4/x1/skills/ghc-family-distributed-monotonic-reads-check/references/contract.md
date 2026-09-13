# monotonic_reads_check

Find logical-clock regressions in a finite synthetic read sequence.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## No reads have no regression

Request:
```json
{
  "op": "monotonic_reads_check",
  "record": {
    "reads": []
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
    "monotonic": true,
    "violations": [],
    "read_count": 0,
    "wall_time_claim": false
  },
  "error": null,
  "external_credit": false
}
```

## One read has no predecessor

Request:
```json
{
  "op": "monotonic_reads_check",
  "record": {
    "reads": [
      {
        "a": 1
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
    "monotonic": true,
    "violations": [],
    "read_count": 1,
    "wall_time_claim": false
  },
  "error": null,
  "external_credit": false
}
```

## Equal clocks are monotonic

Request:
```json
{
  "op": "monotonic_reads_check",
  "record": {
    "reads": [
      {
        "a": 1
      },
      {
        "a": 1
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
    "monotonic": true,
    "violations": [],
    "read_count": 2,
    "wall_time_claim": false
  },
  "error": null,
  "external_credit": false
}
```

## Increasing clocks are monotonic

Request:
```json
{
  "op": "monotonic_reads_check",
  "record": {
    "reads": [
      {
        "a": 1
      },
      {
        "a": 2
      },
      {
        "a": 2,
        "b": 1
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
    "monotonic": true,
    "violations": [],
    "read_count": 3,
    "wall_time_claim": false
  },
  "error": null,
  "external_credit": false
}
```

## Concurrent and older reads expose regressions

Request:
```json
{
  "op": "monotonic_reads_check",
  "record": {
    "reads": [
      {
        "a": 1
      },
      {
        "b": 1
      },
      {
        "a": 0,
        "b": 1
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
    "monotonic": false,
    "violations": [
      {
        "from": 0,
        "to": 1,
        "relation": "concurrent"
      }
    ],
    "read_count": 3,
    "wall_time_claim": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
