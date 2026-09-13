# accessible_consistency_summary

Represent literal consistency rows while reserving human accessibility evaluation.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Empty summary has explicit status

Request:
```json
{
  "op": "accessible_consistency_summary",
  "record": {
    "rows": []
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "rows": [],
    "row_count": 0,
    "uses_color_only": false,
    "status_text": "0 consistency rows",
    "manual_review": false,
    "assistive_technology_review": false
  },
  "error": null,
  "external_credit": false
}
```

## Consistent key is named literally

Request:
```json
{
  "op": "accessible_consistency_summary",
  "record": {
    "rows": [
      {
        "replica": "a",
        "key": "k",
        "state": "consistent",
        "detail": "version 2"
      }
    ]
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "rows": [
      {
        "replica": "a",
        "key": "k",
        "state": "consistent",
        "detail": "version 2"
      }
    ],
    "row_count": 1,
    "uses_color_only": false,
    "status_text": "1 consistency rows",
    "manual_review": false,
    "assistive_technology_review": false
  },
  "error": null,
  "external_credit": false
}
```

## Conflict row names the contrary state

Request:
```json
{
  "op": "accessible_consistency_summary",
  "record": {
    "rows": [
      {
        "replica": "b",
        "key": "k",
        "state": "conflict",
        "detail": "equal version different value"
      }
    ]
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "rows": [
      {
        "replica": "b",
        "key": "k",
        "state": "conflict",
        "detail": "equal version different value"
      }
    ],
    "row_count": 1,
    "uses_color_only": false,
    "status_text": "1 consistency rows",
    "manual_review": false,
    "assistive_technology_review": false
  },
  "error": null,
  "external_credit": false
}
```

## Missing key is not shown as null

Request:
```json
{
  "op": "accessible_consistency_summary",
  "record": {
    "rows": [
      {
        "replica": "c",
        "key": "k",
        "state": "missing",
        "detail": "no observation"
      }
    ]
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "rows": [
      {
        "replica": "c",
        "key": "k",
        "state": "missing",
        "detail": "no observation"
      }
    ],
    "row_count": 1,
    "uses_color_only": false,
    "status_text": "1 consistency rows",
    "manual_review": false,
    "assistive_technology_review": false
  },
  "error": null,
  "external_credit": false
}
```

## Multiple rows retain stable input order

Request:
```json
{
  "op": "accessible_consistency_summary",
  "record": {
    "rows": [
      {
        "replica": "a",
        "key": "x",
        "state": "consistent",
        "detail": "v1"
      },
      {
        "replica": "b",
        "key": "y",
        "state": "behind",
        "detail": "lag 2"
      }
    ]
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "rows": [
      {
        "replica": "a",
        "key": "x",
        "state": "consistent",
        "detail": "v1"
      },
      {
        "replica": "b",
        "key": "y",
        "state": "behind",
        "detail": "lag 2"
      }
    ],
    "row_count": 2,
    "uses_color_only": false,
    "status_text": "2 consistency rows",
    "manual_review": false,
    "assistive_technology_review": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
