# Four retained source contracts

# field_inventory

Inventory exact top-level field names and JSON types.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## Integer and Boolean fields stay distinct

Request:
```json
{
  "op": "field_inventory",
  "record": {
    "count": 1,
    "enabled": true
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
    "fields": [
      {
        "name": "count",
        "type": "integer"
      },
      {
        "name": "enabled",
        "type": "boolean"
      }
    ],
    "count": 2
  },
  "error": null,
  "external_credit": false
}
```

## Explicit null remains a present field

Request:
```json
{
  "op": "field_inventory",
  "record": {
    "label": "north",
    "flag": false,
    "detail": null
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
    "fields": [
      {
        "name": "detail",
        "type": "null"
      },
      {
        "name": "flag",
        "type": "boolean"
      },
      {
        "name": "label",
        "type": "string"
      }
    ],
    "count": 3
  },
  "error": null,
  "external_credit": false
}
```

## Array and object containers have separate types

Request:
```json
{
  "op": "field_inventory",
  "record": {
    "list": [
      1,
      2
    ],
    "opts": {
      "mode": "x"
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
    "fields": [
      {
        "name": "list",
        "type": "array"
      },
      {
        "name": "opts",
        "type": "object"
      }
    ],
    "count": 2
  },
  "error": null,
  "external_credit": false
}
```

## Empty object and empty string are not absence

Request:
```json
{
  "op": "field_inventory",
  "record": {
    "empty": {},
    "zero": 0,
    "blanks": ""
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
    "fields": [
      {
        "name": "blanks",
        "type": "string"
      },
      {
        "name": "empty",
        "type": "object"
      },
      {
        "name": "zero",
        "type": "integer"
      }
    ],
    "count": 3
  },
  "error": null,
  "external_credit": false
}
```

## Negative integer, empty array and null retain their types

Request:
```json
{
  "op": "field_inventory",
  "record": {
    "negative": -2,
    "tags": [],
    "nullable": null
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
    "fields": [
      {
        "name": "negative",
        "type": "integer"
      },
      {
        "name": "nullable",
        "type": "null"
      },
      {
        "name": "tags",
        "type": "array"
      }
    ],
    "count": 3
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.


---

# field_correspondence

Expose missing sources and duplicate destinations in a declared field correspondence.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## One declared field resolves to a new label

Request:
```json
{
  "op": "field_correspondence",
  "record": {
    "alpha": 1,
    "beta": 2
  },
  "args": {
    "mapping": {
      "alpha": "value"
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
    "resolved": [
      {
        "from": "alpha",
        "to": "value",
        "present": true,
        "source_type": "integer"
      }
    ],
    "target_collisions": [],
    "missing_sources": []
  },
  "error": null,
  "external_credit": false
}
```

## Swap correspondences remain simultaneous

Request:
```json
{
  "op": "field_correspondence",
  "record": {
    "left": true,
    "right": false
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
    "resolved": [
      {
        "from": "left",
        "to": "right",
        "present": true,
        "source_type": "boolean"
      },
      {
        "from": "right",
        "to": "left",
        "present": true,
        "source_type": "boolean"
      }
    ],
    "target_collisions": [],
    "missing_sources": []
  },
  "error": null,
  "external_credit": false
}
```

## Two sources targeting one field are exposed

Request:
```json
{
  "op": "field_correspondence",
  "record": {
    "a": 1,
    "b": "two"
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
    "resolved": [
      {
        "from": "a",
        "to": "x",
        "present": true,
        "source_type": "integer"
      },
      {
        "from": "b",
        "to": "x",
        "present": true,
        "source_type": "string"
      }
    ],
    "target_collisions": [
      {
        "target": "x",
        "sources": [
          "a",
          "b"
        ]
      }
    ],
    "missing_sources": []
  },
  "error": null,
  "external_credit": false
}
```

## An absent source cannot become a null value

Request:
```json
{
  "op": "field_correspondence",
  "record": {
    "a": 1
  },
  "args": {
    "mapping": {
      "z": "zeta"
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
    "resolved": [
      {
        "from": "z",
        "to": "zeta",
        "present": false,
        "source_type": "absent"
      }
    ],
    "target_collisions": [],
    "missing_sources": [
      "z"
    ]
  },
  "error": null,
  "external_credit": false
}
```

## Identity correspondence preserves an array field

Request:
```json
{
  "op": "field_correspondence",
  "record": {
    "x": [
      1
    ],
    "meta": null
  },
  "args": {
    "mapping": {
      "x": "x"
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
    "resolved": [
      {
        "from": "x",
        "to": "x",
        "present": true,
        "source_type": "array"
      }
    ],
    "target_collisions": [],
    "missing_sources": []
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.


---

# required_field_check

Distinguish missing required fields from present null or false values.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## A complete required set is present

Request:
```json
{
  "op": "required_field_check",
  "record": {
    "a": 1,
    "b": 2
  },
  "args": {
    "required": [
      "b",
      "a"
    ]
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "present": [
      "a",
      "b"
    ],
    "missing": [],
    "complete": true
  },
  "error": null,
  "external_credit": false
}
```

## A missing field remains distinct from null

Request:
```json
{
  "op": "required_field_check",
  "record": {
    "a": null
  },
  "args": {
    "required": [
      "a",
      "b"
    ]
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "present": [
      "a"
    ],
    "missing": [
      "b"
    ],
    "complete": false
  },
  "error": null,
  "external_credit": false
}
```

## False and zero satisfy presence only

Request:
```json
{
  "op": "required_field_check",
  "record": {
    "enabled": false,
    "retries": 0
  },
  "args": {
    "required": [
      "enabled",
      "retries"
    ]
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "present": [
      "enabled",
      "retries"
    ],
    "missing": [],
    "complete": true
  },
  "error": null,
  "external_credit": false
}
```

## No fields cannot satisfy a nonempty requirement

Request:
```json
{
  "op": "required_field_check",
  "record": {},
  "args": {
    "required": [
      "x"
    ]
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "present": [],
    "missing": [
      "x"
    ],
    "complete": false
  },
  "error": null,
  "external_credit": false
}
```

## An empty requirement list is explicitly vacuous

Request:
```json
{
  "op": "required_field_check",
  "record": {
    "x": 1
  },
  "args": {
    "required": []
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "present": [],
    "missing": [],
    "complete": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.


---

# schema_delta

Compare declared field types without inferring migration permission.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## A target schema adds one field

Request:
```json
{
  "op": "schema_delta",
  "record": {
    "a": "integer"
  },
  "args": {
    "target": {
      "a": "integer",
      "b": "string"
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
    "added": [
      "b"
    ],
    "removed": [],
    "changed": [],
    "unchanged": [
      "a"
    ]
  },
  "error": null,
  "external_credit": false
}
```

## A removed field remains an explicit obligation

Request:
```json
{
  "op": "schema_delta",
  "record": {
    "old": "string",
    "x": "boolean"
  },
  "args": {
    "target": {
      "x": "boolean"
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
    "added": [],
    "removed": [
      "old"
    ],
    "changed": [],
    "unchanged": [
      "x"
    ]
  },
  "error": null,
  "external_credit": false
}
```

## A scalar type change is not an automatic conversion

Request:
```json
{
  "op": "schema_delta",
  "record": {
    "value": "integer"
  },
  "args": {
    "target": {
      "value": "string"
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
    "added": [],
    "removed": [],
    "changed": [
      {
        "field": "value",
        "from": "integer",
        "to": "string"
      }
    ],
    "unchanged": []
  },
  "error": null,
  "external_credit": false
}
```

## Two empty schemas have no inferred fields

Request:
```json
{
  "op": "schema_delta",
  "record": {},
  "args": {
    "target": {}
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "added": [],
    "removed": [],
    "changed": [],
    "unchanged": []
  },
  "error": null,
  "external_credit": false
}
```

## Addition removal and type change remain separate

Request:
```json
{
  "op": "schema_delta",
  "record": {
    "x": "null",
    "y": "array"
  },
  "args": {
    "target": {
      "x": "object",
      "z": "array"
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
    "added": [
      "z"
    ],
    "removed": [
      "y"
    ],
    "changed": [
      {
        "field": "x",
        "from": "null",
        "to": "object"
      }
    ],
    "unchanged": []
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
