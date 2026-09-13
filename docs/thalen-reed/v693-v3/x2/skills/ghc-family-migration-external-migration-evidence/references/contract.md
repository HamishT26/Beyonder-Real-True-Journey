# external_migration_evidence

Expose missing external migration evidence without promoting local assertions.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## Absent operator evidence remains an open gap

Request:
```json
{
  "op": "external_migration_evidence",
  "record": {
    "requirements": [
      "operator"
    ],
    "evidence": {}
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "open_gap",
  "value": {
    "missing": [
      "operator"
    ],
    "provided": [],
    "external_qualified": false,
    "release": false
  },
  "error": null,
  "external_credit": false
}
```

## A synthetic compatibility note does not supply rollback evidence

Request:
```json
{
  "op": "external_migration_evidence",
  "record": {
    "requirements": [
      "compatibility",
      "rollback"
    ],
    "evidence": {
      "compatibility": {
        "class": "synthetic"
      }
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "open_gap",
  "value": {
    "missing": [
      "rollback"
    ],
    "provided": [
      "compatibility"
    ],
    "external_qualified": false,
    "release": false
  },
  "error": null,
  "external_credit": false
}
```

## Null human review is still absent

Request:
```json
{
  "op": "external_migration_evidence",
  "record": {
    "requirements": [
      "human_review"
    ],
    "evidence": {
      "human_review": null
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "open_gap",
  "value": {
    "missing": [
      "human_review"
    ],
    "provided": [],
    "external_qualified": false,
    "release": false
  },
  "error": null,
  "external_credit": false
}
```

## Same-owner review is present metadata without independent qualification

Request:
```json
{
  "op": "external_migration_evidence",
  "record": {
    "requirements": [
      "independent_review"
    ],
    "evidence": {
      "independent_review": {
        "class": "same_owner"
      }
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "open_gap",
  "value": {
    "missing": [],
    "provided": [
      "independent_review"
    ],
    "external_qualified": false,
    "release": false
  },
  "error": null,
  "external_credit": false
}
```

## Rights and Maori authority require competent external evidence

Request:
```json
{
  "op": "external_migration_evidence",
  "record": {
    "requirements": [
      "rights",
      "maori_authority"
    ],
    "evidence": {
      "rights": null,
      "maori_authority": null
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "open_gap",
  "value": {
    "missing": [
      "maori_authority",
      "rights"
    ],
    "provided": [],
    "external_qualified": false,
    "release": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
