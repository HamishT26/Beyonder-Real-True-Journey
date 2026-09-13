# coercion_preview

Preview a named scalar conversion with an exact refusal reason.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## An integer converts only under an explicit text rule

Request:
```json
{
  "op": "coercion_preview",
  "record": {
    "n": 12
  },
  "args": {
    "field": "n",
    "conversion": "integer_to_text"
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
      "n": "12"
    },
    "reason": null,
    "input_type": "integer",
    "output_type": "string"
  },
  "error": null,
  "external_credit": false
}
```

## Canonical signed integer text converts exactly

Request:
```json
{
  "op": "coercion_preview",
  "record": {
    "n": "-3"
  },
  "args": {
    "field": "n",
    "conversion": "text_to_integer"
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
      "n": -3
    },
    "reason": null,
    "input_type": "string",
    "output_type": "integer"
  },
  "error": null,
  "external_credit": false
}
```

## Leading-zero text is held rather than silently normalized

Request:
```json
{
  "op": "coercion_preview",
  "record": {
    "n": "03"
  },
  "args": {
    "field": "n",
    "conversion": "text_to_integer"
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
      "n": "03"
    },
    "reason": "NONCANONICAL_INTEGER_TEXT",
    "input_type": "string",
    "output_type": "string"
  },
  "error": null,
  "external_credit": false
}
```

## A Boolean converts to its literal text spelling

Request:
```json
{
  "op": "coercion_preview",
  "record": {
    "n": true
  },
  "args": {
    "field": "n",
    "conversion": "boolean_to_text"
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
      "n": "true"
    },
    "reason": null,
    "input_type": "boolean",
    "output_type": "string"
  },
  "error": null,
  "external_credit": false
}
```

## Integer one is not coerced by a Boolean rule

Request:
```json
{
  "op": "coercion_preview",
  "record": {
    "n": 1
  },
  "args": {
    "field": "n",
    "conversion": "boolean_to_text"
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
      "n": 1
    },
    "reason": "TYPE_MISMATCH",
    "input_type": "integer",
    "output_type": "integer"
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
