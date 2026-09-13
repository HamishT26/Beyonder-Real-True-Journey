# accessible_resolution_summary

Represent concrete conflict and resolution rows without claiming human review.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## Literal field summary for unilateral edit

Request:
```json
{
  "op": "accessible_resolution_summary",
  "record": {
    "base": {
      "v": 1,
      "k": 0
    },
    "left": {
      "v": 2,
      "k": 0
    },
    "right": {
      "v": 1,
      "k": 0
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "rows": [
      {
        "field": "k",
        "state": "resolved_unchanged"
      },
      {
        "field": "v",
        "state": "resolved_left"
      }
    ],
    "conflicts": 0,
    "manual_review": false,
    "operator_decision": false
  },
  "error": null,
  "external_credit": false
}
```

## Literal field summary for equal edits

Request:
```json
{
  "op": "accessible_resolution_summary",
  "record": {
    "base": {
      "v": 1
    },
    "left": {
      "v": 2
    },
    "right": {
      "v": 2
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "rows": [
      {
        "field": "v",
        "state": "resolved_both"
      }
    ],
    "conflicts": 0,
    "manual_review": false,
    "operator_decision": false
  },
  "error": null,
  "external_credit": false
}
```

## Literal field summary for different edits

Request:
```json
{
  "op": "accessible_resolution_summary",
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
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "rows": [
      {
        "field": "v",
        "state": "different_edits"
      }
    ],
    "conflicts": 1,
    "manual_review": false,
    "operator_decision": false
  },
  "error": null,
  "external_credit": false
}
```

## Literal field summary for delete versus modify

Request:
```json
{
  "op": "accessible_resolution_summary",
  "record": {
    "base": {
      "v": 1
    },
    "left": {},
    "right": {
      "v": 2
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "rows": [
      {
        "field": "v",
        "state": "delete_modify"
      }
    ],
    "conflicts": 1,
    "manual_review": false,
    "operator_decision": false
  },
  "error": null,
  "external_credit": false
}
```

## Literal field summary for contrary additions

Request:
```json
{
  "op": "accessible_resolution_summary",
  "record": {
    "base": {},
    "left": {
      "v": null
    },
    "right": {
      "v": false
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "rows": [
      {
        "field": "v",
        "state": "concurrent_add"
      }
    ],
    "conflicts": 1,
    "manual_review": false,
    "operator_decision": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
