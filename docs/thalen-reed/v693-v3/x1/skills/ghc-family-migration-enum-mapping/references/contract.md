# enum_mapping

Apply an explicit enum correspondence and expose noninjective targets.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## A listed enum token maps explicitly

Request:
```json
{
  "op": "enum_mapping",
  "record": {
    "status": "new"
  },
  "args": {
    "field": "status",
    "mapping": {
      "new": "pending",
      "ready": "go"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "applied": true,
    "result": {
      "status": "pending"
    },
    "unmapped": null,
    "noninjective_targets": []
  },
  "error": null,
  "external_credit": false
}
```

## An unlisted enum token remains unchanged

Request:
```json
{
  "op": "enum_mapping",
  "record": {
    "status": "unknown"
  },
  "args": {
    "field": "status",
    "mapping": {
      "new": "pending"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "applied": false,
    "result": {
      "status": "unknown"
    },
    "unmapped": "unknown",
    "noninjective_targets": []
  },
  "error": null,
  "external_credit": false
}
```

## A many-to-one enum map exposes information loss

Request:
```json
{
  "op": "enum_mapping",
  "record": {
    "status": "a"
  },
  "args": {
    "field": "status",
    "mapping": {
      "a": "x",
      "b": "x"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "applied": true,
    "result": {
      "status": "x"
    },
    "unmapped": null,
    "noninjective_targets": [
      "x"
    ]
  },
  "error": null,
  "external_credit": false
}
```

## An empty enum token is literal rather than absent

Request:
```json
{
  "op": "enum_mapping",
  "record": {
    "status": ""
  },
  "args": {
    "field": "status",
    "mapping": {
      "": "blank"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "applied": true,
    "result": {
      "status": "blank"
    },
    "unmapped": null,
    "noninjective_targets": []
  },
  "error": null,
  "external_credit": false
}
```

## An identity enum mapping is a declared no-op

Request:
```json
{
  "op": "enum_mapping",
  "record": {
    "status": "done"
  },
  "args": {
    "field": "status",
    "mapping": {
      "done": "done"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "applied": true,
    "result": {
      "status": "done"
    },
    "unmapped": null,
    "noninjective_targets": []
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
