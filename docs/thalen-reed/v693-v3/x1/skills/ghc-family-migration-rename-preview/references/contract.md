# rename_preview

Preview simultaneous renames without overwriting an occupied destination.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## A fresh target receives the original value

Request:
```json
{
  "op": "rename_preview",
  "record": {
    "old": 1,
    "keep": true
  },
  "args": {
    "mapping": {
      "old": "new"
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
      "keep": true,
      "new": 1
    },
    "conflicts": [],
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## A two-field swap does not destroy either source

Request:
```json
{
  "op": "rename_preview",
  "record": {
    "left": "L",
    "right": "R"
  },
  "args": {
    "mapping": {
      "left": "right",
      "right": "left"
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
      "left": "R",
      "right": "L"
    },
    "conflicts": [],
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## An occupied unmapped destination blocks the preview

Request:
```json
{
  "op": "rename_preview",
  "record": {
    "a": 1,
    "b": 2,
    "c": 3
  },
  "args": {
    "mapping": {
      "a": "c"
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
      "a": 1,
      "b": 2,
      "c": 3
    },
    "conflicts": [
      "destination_occupied:c"
    ],
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## A duplicate target blocks both writes

Request:
```json
{
  "op": "rename_preview",
  "record": {
    "a": 1,
    "b": 2
  },
  "args": {
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
    "applied": false,
    "result": {
      "a": 1,
      "b": 2
    },
    "conflicts": [
      "duplicate_destination:x"
    ],
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## An identity rename preserves explicit null

Request:
```json
{
  "op": "rename_preview",
  "record": {
    "a": null,
    "keep": "k"
  },
  "args": {
    "mapping": {
      "a": "a"
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
      "a": null,
      "keep": "k"
    },
    "conflicts": [],
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
