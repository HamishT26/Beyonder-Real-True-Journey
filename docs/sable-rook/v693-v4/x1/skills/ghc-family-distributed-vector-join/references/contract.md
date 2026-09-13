# vector_clock_join

Compute a componentwise finite clock join with explicit actor coverage.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Two empty clocks join to empty

Request:
```json
{
  "op": "vector_clock_join",
  "record": {
    "clocks": [
      {},
      {}
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
    "clock": {},
    "actors": [],
    "input_count": 2,
    "dominates_all": true
  },
  "error": null,
  "external_credit": false
}
```

## Disjoint actors are retained

Request:
```json
{
  "op": "vector_clock_join",
  "record": {
    "clocks": [
      {
        "a": 1
      },
      {
        "b": 2
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
    "clock": {
      "a": 1,
      "b": 2
    },
    "actors": [
      "a",
      "b"
    ],
    "input_count": 2,
    "dominates_all": true
  },
  "error": null,
  "external_credit": false
}
```

## Largest component is retained per actor

Request:
```json
{
  "op": "vector_clock_join",
  "record": {
    "clocks": [
      {
        "a": 3,
        "b": 1
      },
      {
        "a": 2,
        "b": 4
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
    "clock": {
      "a": 3,
      "b": 4
    },
    "actors": [
      "a",
      "b"
    ],
    "input_count": 2,
    "dominates_all": true
  },
  "error": null,
  "external_credit": false
}
```

## Duplicate clocks do not inflate counters

Request:
```json
{
  "op": "vector_clock_join",
  "record": {
    "clocks": [
      {
        "a": 2
      },
      {
        "a": 2
      },
      {
        "a": 2
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
    "clock": {
      "a": 2
    },
    "actors": [
      "a"
    ],
    "input_count": 3,
    "dominates_all": true
  },
  "error": null,
  "external_credit": false
}
```

## Zero components remain explicit

Request:
```json
{
  "op": "vector_clock_join",
  "record": {
    "clocks": [
      {
        "a": 0,
        "b": 1
      },
      {
        "a": 2,
        "b": 0
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
    "clock": {
      "a": 2,
      "b": 1
    },
    "actors": [
      "a",
      "b"
    ],
    "input_count": 2,
    "dominates_all": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
