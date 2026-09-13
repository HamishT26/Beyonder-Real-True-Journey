# three_way_merge

Merge independent synthetic field edits and retain every unresolved conflict.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## A unilateral edit merges beside an unchanged field

Request:
```json
{
  "op": "three_way_merge",
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
  "disposition": "completed",
  "value": {
    "merged": {
      "k": 0,
      "v": 2
    },
    "conflicts": [],
    "resolved": [
      {
        "field": "k",
        "source": "unchanged"
      },
      {
        "field": "v",
        "source": "left"
      }
    ]
  },
  "error": null,
  "external_credit": false
}
```

## Equal concurrent edits coalesce

Request:
```json
{
  "op": "three_way_merge",
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
  "disposition": "completed",
  "value": {
    "merged": {
      "v": 2
    },
    "conflicts": [],
    "resolved": [
      {
        "field": "v",
        "source": "both"
      }
    ]
  },
  "error": null,
  "external_credit": false
}
```

## Different concurrent edits remain unresolved

Request:
```json
{
  "op": "three_way_merge",
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
  "disposition": "completed",
  "value": {
    "merged": {},
    "conflicts": [
      {
        "field": "v",
        "kind": "different_edits",
        "base": {
          "present": true,
          "value": 1
        },
        "left": {
          "present": true,
          "value": 2
        },
        "right": {
          "present": true,
          "value": 3
        }
      }
    ],
    "resolved": []
  },
  "error": null,
  "external_credit": false
}
```

## Delete-versus-modify keeps both contrary states

Request:
```json
{
  "op": "three_way_merge",
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
  "disposition": "completed",
  "value": {
    "merged": {},
    "conflicts": [
      {
        "field": "v",
        "kind": "delete_modify",
        "base": {
          "present": true,
          "value": 1
        },
        "left": {
          "present": false,
          "value": null
        },
        "right": {
          "present": true,
          "value": 2
        }
      }
    ],
    "resolved": []
  },
  "error": null,
  "external_credit": false
}
```

## Concurrent null and false additions remain a conflict

Request:
```json
{
  "op": "three_way_merge",
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
  "disposition": "completed",
  "value": {
    "merged": {},
    "conflicts": [
      {
        "field": "v",
        "kind": "concurrent_add",
        "base": {
          "present": false,
          "value": null
        },
        "left": {
          "present": true,
          "value": null
        },
        "right": {
          "present": true,
          "value": false
        }
      }
    ],
    "resolved": []
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
