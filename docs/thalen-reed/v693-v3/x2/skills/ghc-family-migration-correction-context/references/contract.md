# correction_context

Append a correction only to its retained predecessor and matching source context.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## A correction appends beside its rejected predecessor

Request:
```json
{
  "op": "correction_context",
  "record": {
    "prior": [
      {
        "id": "r1",
        "state": "rejected",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      }
    ],
    "correction": {
      "id": "r2",
      "supersedes": "r1",
      "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "state": "represented"
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
    "accepted": true,
    "reason": null,
    "records": [
      {
        "id": "r1",
        "state": "rejected",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      },
      {
        "id": "r2",
        "supersedes": "r1",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "state": "represented"
      }
    ],
    "predecessor_erased": false
  },
  "error": null,
  "external_credit": false
}
```

## A new source context cannot amend the old attempt

Request:
```json
{
  "op": "correction_context",
  "record": {
    "prior": [
      {
        "id": "r1",
        "state": "rejected",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      }
    ],
    "correction": {
      "id": "r2",
      "supersedes": "r1",
      "context": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "state": "represented"
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
    "accepted": false,
    "reason": "STALE_CONTEXT",
    "records": [
      {
        "id": "r1",
        "state": "rejected",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      }
    ],
    "predecessor_erased": false
  },
  "error": null,
  "external_credit": false
}
```

## An unknown predecessor prevents attachment

Request:
```json
{
  "op": "correction_context",
  "record": {
    "prior": [
      {
        "id": "r1",
        "state": "rejected",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      }
    ],
    "correction": {
      "id": "r2",
      "supersedes": "missing",
      "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "state": "represented"
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
    "accepted": false,
    "reason": "UNKNOWN_PREDECESSOR",
    "records": [
      {
        "id": "r1",
        "state": "rejected",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      }
    ],
    "predecessor_erased": false
  },
  "error": null,
  "external_credit": false
}
```

## A repeated correction identifier is refused

Request:
```json
{
  "op": "correction_context",
  "record": {
    "prior": [
      {
        "id": "r1",
        "state": "rejected",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      }
    ],
    "correction": {
      "id": "r1",
      "supersedes": "r1",
      "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "state": "represented"
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
    "accepted": false,
    "reason": "DUPLICATE_ID",
    "records": [
      {
        "id": "r1",
        "state": "rejected",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      }
    ],
    "predecessor_erased": false
  },
  "error": null,
  "external_credit": false
}
```

## A held predecessor stays held after an additive correction

Request:
```json
{
  "op": "correction_context",
  "record": {
    "prior": [
      {
        "id": "r1",
        "state": "held",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      }
    ],
    "correction": {
      "id": "r2",
      "supersedes": "r1",
      "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "state": "represented"
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
    "accepted": true,
    "reason": null,
    "records": [
      {
        "id": "r1",
        "state": "held",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      },
      {
        "id": "r2",
        "supersedes": "r1",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "state": "represented"
      }
    ],
    "predecessor_erased": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
