# operator_release_gate

Keep deployment and publication held despite self-declared permissions.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## Reserve deploy despite local permission assertions

Request:
```json
{
  "op": "operator_release_gate",
  "record": {
    "target": "synthetic-config-A",
    "authority": null,
    "evidence": null
  },
  "args": {
    "requested": "deploy"
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "exact_gate",
  "value": {
    "requested": "deploy",
    "target": "synthetic-config-A",
    "required": [
      "competent_operator",
      "external_validation",
      "rollback_evidence"
    ],
    "released": false,
    "assertions_verified": false
  },
  "error": null,
  "external_credit": false
}
```

## Reserve publish despite local permission assertions

Request:
```json
{
  "op": "operator_release_gate",
  "record": {
    "target": "synthetic-config-B",
    "authority": {
      "declared": true
    },
    "evidence": null
  },
  "args": {
    "requested": "publish"
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "exact_gate",
  "value": {
    "requested": "publish",
    "target": "synthetic-config-B",
    "required": [
      "rights_holder",
      "affected_people",
      "privacy_review"
    ],
    "released": false,
    "assertions_verified": false
  },
  "error": null,
  "external_credit": false
}
```

## Reserve replace despite local permission assertions

Request:
```json
{
  "op": "operator_release_gate",
  "record": {
    "target": "synthetic-config-C",
    "authority": null,
    "evidence": {
      "declared": true
    }
  },
  "args": {
    "requested": "replace"
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "exact_gate",
  "value": {
    "requested": "replace",
    "target": "synthetic-config-C",
    "required": [
      "competent_operator",
      "exact_target",
      "recoverable_source"
    ],
    "released": false,
    "assertions_verified": false
  },
  "error": null,
  "external_credit": false
}
```

## Reserve delete despite local permission assertions

Request:
```json
{
  "op": "operator_release_gate",
  "record": {
    "target": "synthetic-config-D",
    "authority": {
      "declared": true
    },
    "evidence": {
      "declared": true
    }
  },
  "args": {
    "requested": "delete"
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "exact_gate",
  "value": {
    "requested": "delete",
    "target": "synthetic-config-D",
    "required": [
      "exact_destructive_authority",
      "recoverable_source"
    ],
    "released": false,
    "assertions_verified": false
  },
  "error": null,
  "external_credit": false
}
```

## Reserve maori_label despite local permission assertions

Request:
```json
{
  "op": "operator_release_gate",
  "record": {
    "target": "synthetic-config-E",
    "authority": null,
    "evidence": {
      "declared": true
    }
  },
  "args": {
    "requested": "maori_label"
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "exact_gate",
  "value": {
    "requested": "maori_label",
    "target": "synthetic-config-E",
    "required": [
      "maori_authority",
      "affected_people"
    ],
    "released": false,
    "assertions_verified": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
