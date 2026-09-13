# bounded_staleness_check

Compare finite logical counter lag to an explicit bound without making latency claims.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Equal empty clocks are within zero

Request:
```json
{
  "op": "bounded_staleness_check",
  "record": {
    "committed": {},
    "observed": {}
  },
  "args": {
    "max_lag": 0
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "within_bound": true,
    "lag": {},
    "maximum": 0,
    "max_lag": 0,
    "logical_only": true
  },
  "error": null,
  "external_credit": false
}
```

## Equal actor clock is within zero

Request:
```json
{
  "op": "bounded_staleness_check",
  "record": {
    "committed": {
      "a": 2
    },
    "observed": {
      "a": 2
    }
  },
  "args": {
    "max_lag": 0
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "within_bound": true,
    "lag": {
      "a": 0
    },
    "maximum": 0,
    "max_lag": 0,
    "logical_only": true
  },
  "error": null,
  "external_credit": false
}
```

## One logical step is within one

Request:
```json
{
  "op": "bounded_staleness_check",
  "record": {
    "committed": {
      "a": 3
    },
    "observed": {
      "a": 2
    }
  },
  "args": {
    "max_lag": 1
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "within_bound": true,
    "lag": {
      "a": 1
    },
    "maximum": 1,
    "max_lag": 1,
    "logical_only": true
  },
  "error": null,
  "external_credit": false
}
```

## Two logical steps exceed one

Request:
```json
{
  "op": "bounded_staleness_check",
  "record": {
    "committed": {
      "a": 4
    },
    "observed": {
      "a": 2
    }
  },
  "args": {
    "max_lag": 1
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "within_bound": false,
    "lag": {
      "a": 2
    },
    "maximum": 2,
    "max_lag": 1,
    "logical_only": true
  },
  "error": null,
  "external_credit": false
}
```

## Actorwise lag retains the maximum

Request:
```json
{
  "op": "bounded_staleness_check",
  "record": {
    "committed": {
      "a": 4,
      "b": 5
    },
    "observed": {
      "a": 3,
      "b": 2
    }
  },
  "args": {
    "max_lag": 3
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "within_bound": true,
    "lag": {
      "a": 1,
      "b": 3
    },
    "maximum": 3,
    "max_lag": 3,
    "logical_only": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
