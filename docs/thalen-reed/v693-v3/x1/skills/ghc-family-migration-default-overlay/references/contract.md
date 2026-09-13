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
