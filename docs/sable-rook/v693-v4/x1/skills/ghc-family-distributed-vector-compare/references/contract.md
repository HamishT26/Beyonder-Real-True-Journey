# vector_clock_compare

Compare two finite logical clocks without inferring wall time or physical causality.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Equal empty clocks remain equal

Request:
```json
{
  "op": "vector_clock_compare",
  "record": {
    "left": {},
    "right": {}
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
    "relation": "equal",
    "actors": [],
    "incomparable": false
  },
  "error": null,
  "external_credit": false
}
```

## One actor increment is after

Request:
```json
{
  "op": "vector_clock_compare",
  "record": {
    "left": {
      "a": 2
    },
    "right": {
      "a": 1
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
    "relation": "after",
    "actors": [
      "a"
    ],
    "incomparable": false
  },
  "error": null,
  "external_credit": false
}
```

## A lower observation is before

Request:
```json
{
  "op": "vector_clock_compare",
  "record": {
    "left": {
      "a": 1,
      "b": 0
    },
    "right": {
      "a": 1,
      "b": 2
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
    "relation": "before",
    "actors": [
      "a",
      "b"
    ],
    "incomparable": false
  },
  "error": null,
  "external_credit": false
}
```

## Contrary actor advances are concurrent

Request:
```json
{
  "op": "vector_clock_compare",
  "record": {
    "left": {
      "a": 2,
      "b": 1
    },
    "right": {
      "a": 1,
      "b": 2
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
    "relation": "concurrent",
    "actors": [
      "a",
      "b"
    ],
    "incomparable": true
  },
  "error": null,
  "external_credit": false
}
```

## An absent actor component is logical zero

Request:
```json
{
  "op": "vector_clock_compare",
  "record": {
    "left": {
      "a": 1
    },
    "right": {
      "a": 1,
      "b": 1
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
    "relation": "before",
    "actors": [
      "a",
      "b"
    ],
    "incomparable": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
