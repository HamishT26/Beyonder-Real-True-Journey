# read_your_writes_check

Check whether one synthetic observation dominates a declared session write clock.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Empty session requirement is satisfied

Request:
```json
{
  "op": "read_your_writes_check",
  "record": {
    "write_clock": {},
    "observed_clock": {}
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
    "satisfied": true,
    "deficits": [],
    "actors": [],
    "empirical_latency": false
  },
  "error": null,
  "external_credit": false
}
```

## Equal observation satisfies the write

Request:
```json
{
  "op": "read_your_writes_check",
  "record": {
    "write_clock": {
      "a": 2
    },
    "observed_clock": {
      "a": 2
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
    "satisfied": true,
    "deficits": [],
    "actors": [
      "a"
    ],
    "empirical_latency": false
  },
  "error": null,
  "external_credit": false
}
```

## Newer observation satisfies the write

Request:
```json
{
  "op": "read_your_writes_check",
  "record": {
    "write_clock": {
      "a": 2
    },
    "observed_clock": {
      "a": 3,
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
    "satisfied": true,
    "deficits": [],
    "actors": [
      "a",
      "b"
    ],
    "empirical_latency": false
  },
  "error": null,
  "external_credit": false
}
```

## Older observation exposes one deficit

Request:
```json
{
  "op": "read_your_writes_check",
  "record": {
    "write_clock": {
      "a": 2
    },
    "observed_clock": {
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
    "satisfied": false,
    "deficits": [
      {
        "actor": "a",
        "required": 2,
        "observed": 1
      }
    ],
    "actors": [
      "a"
    ],
    "empirical_latency": false
  },
  "error": null,
  "external_credit": false
}
```

## Missing actor observation is zero

Request:
```json
{
  "op": "read_your_writes_check",
  "record": {
    "write_clock": {
      "a": 1,
      "b": 2
    },
    "observed_clock": {
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
    "satisfied": false,
    "deficits": [
      {
        "actor": "b",
        "required": 2,
        "observed": 0
      }
    ],
    "actors": [
      "a",
      "b"
    ],
    "empirical_latency": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
