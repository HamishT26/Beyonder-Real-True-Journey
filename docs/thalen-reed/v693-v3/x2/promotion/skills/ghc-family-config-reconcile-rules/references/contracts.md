# Four retained source contracts

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


---

# default_overlay

Add defaults only to absent fields while retaining explicit null and contrary values.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## An absent field receives a declared default

Request:
```json
{
  "op": "default_overlay",
  "record": {},
  "args": {
    "defaults": {
      "a": 1
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
    "result": {
      "a": 1
    },
    "added": [
      "a"
    ],
    "retained": [],
    "already_equal": []
  },
  "error": null,
  "external_credit": false
}
```

## Null is retained while another absent field is added

Request:
```json
{
  "op": "default_overlay",
  "record": {
    "a": null
  },
  "args": {
    "defaults": {
      "a": 5,
      "b": false
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
    "result": {
      "a": null,
      "b": false
    },
    "added": [
      "b"
    ],
    "retained": [
      "a"
    ],
    "already_equal": []
  },
  "error": null,
  "external_credit": false
}
```

## An equal default is recorded without a change

Request:
```json
{
  "op": "default_overlay",
  "record": {
    "a": 1
  },
  "args": {
    "defaults": {
      "a": 1
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
    "result": {
      "a": 1
    },
    "added": [],
    "retained": [],
    "already_equal": [
      "a"
    ]
  },
  "error": null,
  "external_credit": false
}
```

## An existing empty array is not replaced

Request:
```json
{
  "op": "default_overlay",
  "record": {
    "arr": []
  },
  "args": {
    "defaults": {
      "arr": [
        1
      ],
      "object": {}
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
    "result": {
      "arr": [],
      "object": {}
    },
    "added": [
      "object"
    ],
    "retained": [
      "arr"
    ],
    "already_equal": []
  },
  "error": null,
  "external_credit": false
}
```

## Contrary Boolean and integer values remain present

Request:
```json
{
  "op": "default_overlay",
  "record": {
    "neg": -1,
    "flag": false
  },
  "args": {
    "defaults": {
      "neg": 0,
      "flag": true,
      "x": null
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
    "result": {
      "neg": -1,
      "flag": false,
      "x": null
    },
    "added": [
      "x"
    ],
    "retained": [
      "flag",
      "neg"
    ],
    "already_equal": []
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.


---

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


---

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
