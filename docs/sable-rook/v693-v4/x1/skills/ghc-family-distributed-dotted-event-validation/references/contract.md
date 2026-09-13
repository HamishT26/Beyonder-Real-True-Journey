# dotted_event_validation

Check whether one synthetic event dot is the next local actor event after its context.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## First actor event follows empty context

Request:
```json
{
  "op": "dotted_event_validation",
  "record": {
    "context": {},
    "dot": {
      "actor": "a",
      "counter": 1
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
    "accepted": true,
    "reason": null,
    "next_clock": {
      "a": 1
    },
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Next actor counter advances exactly once

Request:
```json
{
  "op": "dotted_event_validation",
  "record": {
    "context": {
      "a": 2,
      "b": 1
    },
    "dot": {
      "actor": "a",
      "counter": 3
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
    "accepted": true,
    "reason": null,
    "next_clock": {
      "a": 3,
      "b": 1
    },
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Repeated actor counter is refused

Request:
```json
{
  "op": "dotted_event_validation",
  "record": {
    "context": {
      "a": 2
    },
    "dot": {
      "actor": "a",
      "counter": 2
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
    "accepted": false,
    "reason": "DOT_NOT_NEXT",
    "next_clock": {
      "a": 2
    },
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Skipped actor counter is refused

Request:
```json
{
  "op": "dotted_event_validation",
  "record": {
    "context": {
      "a": 2
    },
    "dot": {
      "actor": "a",
      "counter": 4
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
    "accepted": false,
    "reason": "DOT_NOT_NEXT",
    "next_clock": {
      "a": 2
    },
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Other actor context remains unchanged

Request:
```json
{
  "op": "dotted_event_validation",
  "record": {
    "context": {
      "a": 0,
      "b": 5
    },
    "dot": {
      "actor": "a",
      "counter": 1
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
    "accepted": true,
    "reason": null,
    "next_clock": {
      "a": 1,
      "b": 5
    },
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
