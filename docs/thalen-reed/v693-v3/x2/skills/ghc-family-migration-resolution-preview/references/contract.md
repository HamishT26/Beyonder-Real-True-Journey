# resolution_preview

Apply explicit conflict choices or retain the unmodified base when a choice is missing.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## An explicit left choice selects only the left value

Request:
```json
{
  "op": "resolution_preview",
  "record": {
    "base": {
      "v": 1
    },
    "left": {
      "v": 2
    },
    "right": {
      "v": 3
    }
  },
  "args": {
    "choices": {
      "v": "left"
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
      "v": 2
    },
    "decisions": [
      {
        "field": "v",
        "choice": "left"
      }
    ],
    "unresolved": [],
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## An explicit right choice selects only the right value

Request:
```json
{
  "op": "resolution_preview",
  "record": {
    "base": {
      "v": 1
    },
    "left": {
      "v": 2
    },
    "right": {
      "v": 3
    }
  },
  "args": {
    "choices": {
      "v": "right"
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
      "v": 3
    },
    "decisions": [
      {
        "field": "v",
        "choice": "right"
      }
    ],
    "unresolved": [],
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## An explicit base choice retains the ancestor

Request:
```json
{
  "op": "resolution_preview",
  "record": {
    "base": {
      "v": 1
    },
    "left": {
      "v": 2
    },
    "right": {
      "v": 3
    }
  },
  "args": {
    "choices": {
      "v": "base"
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
      "v": 1
    },
    "decisions": [
      {
        "field": "v",
        "choice": "base"
      }
    ],
    "unresolved": [],
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## An explicit remove choice preserves absence

Request:
```json
{
  "op": "resolution_preview",
  "record": {
    "base": {
      "v": 1
    },
    "left": {
      "v": 2
    },
    "right": {
      "v": 3
    }
  },
  "args": {
    "choices": {
      "v": "remove"
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
    "result": {},
    "decisions": [
      {
        "field": "v",
        "choice": "remove"
      }
    ],
    "unresolved": [],
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## An unresolved field aborts the whole resolution preview

Request:
```json
{
  "op": "resolution_preview",
  "record": {
    "base": {
      "v": 1
    },
    "left": {
      "v": 2
    },
    "right": {
      "v": 3
    }
  },
  "args": {
    "choices": {}
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
      "v": 1
    },
    "decisions": [],
    "unresolved": [
      "v"
    ],
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
